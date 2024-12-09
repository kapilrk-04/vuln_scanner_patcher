from oop_utils import VulnerablePackage
from typing import List
import random
# import nvdlib
import json
from tqdm import tqdm
from requests import post


def get_vulnerable_packages(installed_pkgs) -> List[VulnerablePackage]:
    vulnerable_packages = []

    print("Searching for vulnerable packages...")
    # for i in tqdm(range(len(installed_pkgs)), desc="Searching for vulnerable packages", unit="package"):
    #     pkg = installed_pkgs[i]
    #     print(f"""Searching for vulnerabilities in {
    #           pkg.name} ({pkg.version})...""")
    #     # vulnerable_packages.append(VulnerablePackage(
    #     #     name=pkg.name,
    #     #     version=pkg.version,
    #     #     providerName=pkg.providerName,
    #     #     severity="High",
    #     #     severity_score=random.uniform(7.0, 10.0)
    #     # ))
    #
    #     cpe = nvdlib.searchCPE_V2(
    #         keywordSearch=pkg.name, key='313be7e4-942c-490b-8a09-e683b2c33db3')
    #     for c in cpe:
    #         vsn = c.cpeName.split(':')[4]
    #         if vsn >= str(pkg.version):
    #             vulnerable_packages.append(VulnerablePackage(
    #                 name=pkg.name,
    #                 version=pkg.version,
    #                 providerName=pkg.providerName,
    #                 severity="High",
    #                 severity_score=random.uniform(7.0, 10.0)
    #             ))
    #             # json.dump(c.toJSON(), fl)
    #             print(c)
    #             break

    installed_pkgs_json = []
    for pkg in installed_pkgs:
        installed_pkgs_json.append({
            "product": pkg.name,
            "version": pkg.version,
            "vendor": pkg.providerName
        })

    post_data = {
        "applications": installed_pkgs_json
    }
    response = post("http://localhost:3000/api/analyze", json=post_data)

    # print(response.json()['results'])

    for result in response.json()['results']:
        vulnerable_packages.append(VulnerablePackage(
            name=result['application']['product'],
            version=result['application']['version'],
            providerName=result['application']['vendor'],
            cpe=result['cpe'],
            vulnerability_summary=result['vulnerability_summary']
        ))

    return vulnerable_packages
