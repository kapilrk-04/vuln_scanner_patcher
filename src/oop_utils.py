from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Package:
    def __init__(self, name: str, version: str, providerName: str):
        self.name = name
        self.version = version
        self.providerName = providerName


class VulnerablePackage:
    # package name, version (this depends  completely on the package and formatting is different for each), severity, severity score (these two depends) on the cvss version
    def __init__(self, name: str, version: str, providerName: str, cpe: str, vulnerability_summary: dict):
        self.name = name
        self.version = version
        self.providerName = providerName
        self.cpe = cpe
        self.vulnerability_summary = vulnerability_summary


class OSInterface(ABC):
    def __init__(self):
        self.installed_pkgs = set()

    @abstractmethod
    def scan_pkgs(self) -> Tuple[Optional[List[Package]], Optional[Exception]]:
        """Scan and retrieve installed packages."""
        pass

    @abstractmethod
    def exec_command(self, command: str) -> dict:
        """Execute a system command."""
        pass

    @abstractmethod
    def translate_cmd(self, command: str) -> str:
        """Translate a generic command into an OS-specific command."""
        pass


class UpdateSearcher(ABC):
    @abstractmethod
    def search_for_updates(self, packages: List[VulnerablePackage]) -> List[str]:
        """Search for updates for the given packages."""
        pass

    @abstractmethod
    def open_links(self, links: List[str]):
        """Open the given links in a web browser."""
        pass
