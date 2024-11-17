from get_assets import *
from get_vulnpackages import *
from patch_search import *
import platform

def get_assets(op_sys):
    if op_sys == 'Windows':
        print("Detected Windows OS")
        print("Scanning Windows packages...")
        windows = Windows()
        installed_pkgs, err = windows.scan_pkgs()
        if err:
            return None, err
        return installed_pkgs, None
    else:
        return None, f"Unsupported OS: {op_sys}"

def main():
    try:
        op_sys = platform.system()
    except Exception as e:
        print(f"Error: {e}")
        return
    
    installed_pkgs, err = get_assets(op_sys)
    if err:
        print(f"Error: {err}")
        return
    
    # logic for sending installed packages to the vulnerability scanner
    vulnerable_packages = get_vulnerable_packages(installed_pkgs)

    # display the vulnerable packages
    print("Vulnerable Packages:")
    for i, pkg in enumerate(vulnerable_packages, 1):
        print(f"{i}. {pkg.name} ({pkg.version}) - Severity: {pkg.severity}, Severity Score: {pkg.severity_score}")

    while True:
        response = input("Select packages to search for updates. If you want to select multiple packages, separate them by commas. Enter 0 to exit: ")
        if response.strip() == '0':
            break
        try:
            choices = list(map(int, response.split(',')))
            if any(choice < 1 or choice > len(vulnerable_packages) for choice in choices):
                raise ValueError
            selected_packages = [vulnerable_packages[choice - 1] for choice in choices]
            results = generate_search_links(selected_packages)
            open_links(results)
        except ValueError:
            print("Invalid input. Please enter valid package numbers.")
            continue

if __name__ == '__main__':
    main()


    