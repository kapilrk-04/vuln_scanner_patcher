import subprocess
import re
from typing import Tuple, List, Dict, Optional
from oop_utils import Package, OSInterface

class Windows(OSInterface):
    def __init__(self):
        self.installed_pkgs = set()

    def scan_pkgs(self) -> Tuple[Optional[List[Package]], Optional[Exception]]:
        # Check for MSU packages using Get-Package
        result = self.exec_command(self.translate_cmd("Get-Package | Format-List -Property Name, Version, ProviderName"))
        if result['success']:
            _, err = self.parse_get_package(result['stdout'])
            if err:
                return None, Exception(f"Failed to parse Get-Package. err: {err}")

        # Check for packages using Get-WmiObject
        wmi_result = self.exec_command(self.translate_cmd("Get-WmiObject -Query 'SELECT * FROM Win32_Product' | Format-List -Property Name, Version"))
        if wmi_result['success']:
            _, wmi_err = self.parse_get_package_wmi(wmi_result['stdout'])
            if wmi_err:
                return None, Exception(f"Failed to parse Get-WmiObject. err: {wmi_err}")

        return list(self.installed_pkgs), None

    def exec_command(self, command: str) -> dict:
        # Run the command within PowerShell
        powershell_command = f"powershell -Command \"{command}\""
        try:
            result = subprocess.run(powershell_command, shell=True, capture_output=True, text=True)
            return {'stdout': result.stdout, 'stderr': result.stderr, 'success': result.returncode == 0}
        except Exception as e:
            return {'stdout': '', 'stderr': str(e), 'success': False}

    def translate_cmd(self, command: str) -> str:
        # Placeholder for any required command translation
        return command

    def parse_get_package(self, stdout: str) -> Tuple[List[str], Optional[Exception]]:
        lines = stdout.split('\n')
        err = None
        names, versions, providerNames = [], [], []
        try:
            for line in lines:
                if line.startswith('Name'):
                    name = line.split(': ')[1]
                    version = ''
                    # Check for version in the name format "Name (Version x)"
                    match = re.search(r'\(Version ([^)]+)\)', name)
                    if match:
                        version = match.group(1)
                        name = re.sub(r' \(Version [^)]+\)', '', name)  # Remove version info from name
                        version = version.strip()
                        versions.append(version)
                    if name.strip() != '':
                        names.append(name.strip())
                elif line.startswith('Version'):
                    if line.split(': ')[1].strip() != '':
                        versions.append(line.split(': ')[1].strip())
                    else:
                        if len(names) > len(versions):
                            versions.append('')
                elif line.startswith('ProviderName'):
                    providerNames.append(line.split(': ')[1].strip())
        except Exception as e:
            err = str(e)

        if len(names) == len(versions) == len(providerNames):
            for i in range(len(names)):
                if providerNames[i] != 'msu':
                    self.installed_pkgs.add(Package(names[i], versions[i], providerNames[i]))

        return names, err

    def parse_get_package_wmi(self, stdout: str) -> Tuple[List[str], Optional[Exception]]:
        lines = stdout.split('\n')
        err = None
        try:
            name, version = '', ''
            for line in lines:
                if line.startswith('Name'):
                    name = line.split(': ')[1].strip()
                elif line.startswith('Version'):
                    version = line.split(': ')[1].strip()
                    if name and version:
                        self.installed_pkgs.add(Package(name, version, 'WMI'))
                        name, version = '', ''
        except Exception as e:
            err = str(e)

        return [], err
