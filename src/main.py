from get_assets import *
from get_vulnpackages import *
from patch_search import *
import platform


def get_os():
    try:
        op_sys = platform.system()
        if op_sys == 'Windows':
            print("Detected Windows OS")
            pkg_mgr = Windows()
            update_searcher = WindowsUpdateSearcher()
        else:
            return None, None, None, "Unsupported OS"
    except Exception as e:
        return None, None, None, f"Error: {e}"
    return op_sys, pkg_mgr, update_searcher, None


def get_assets(pkg_mgr):
    try:
        installed_pkgs, err = pkg_mgr.scan_pkgs()
        if err:
            return None, err
    except Exception as e:
        return None, f"Error: {e}"
    return installed_pkgs, None


def main():
    try:
        op_sys, pkg_mgr, update_searcher, err = get_os()
        if err:
            print(err)
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    installed_pkgs, err = get_assets(pkg_mgr)
    if err:
        print(f"Error: {err}")
        return

    # logic for sending installed packages to the vulnerability scanner
    vulnerable_packages = get_vulnerable_packages(installed_pkgs)

    # display the vulnerable packages
    print("Vulnerable Packages:")
    for i, pkg in enumerate(vulnerable_packages, 1):
        print(f"""{i}. {pkg.name} ({
              pkg.version}) - Severity: {pkg.vulnerability_summary['most_critical']['cvssScore']}""")

    while True:
        response = input(
            "Select packages to search for updates. If you want to select multiple packages, separate them by commas. Enter 0 to exit: ")
        if response.strip() == '0':
            break
        try:
            choices = list(map(int, response.split(',')))
            if any(choice < 1 or choice > len(vulnerable_packages) for choice in choices):
                raise ValueError
            selected_packages = [vulnerable_packages[choice - 1]
                                 for choice in choices]
            results = update_searcher.search_for_updates(selected_packages)
            update_searcher.open_links(results)
        except ValueError:
            print("Invalid input. Please enter valid package numbers.")
            continue


if __name__ == '__main__':
    main()
