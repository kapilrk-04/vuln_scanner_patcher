from oop_utils import VulnerablePackage
from typing import List
import random
import nvdlib
import json
from tqdm import tqdm

def get_vulnerable_packages(installed_pkgs) -> List[VulnerablePackage]:
    vulnerable_packages = []
    
    print("Searching for vulnerable packages...")
    for i in tqdm(range(len(installed_pkgs)), desc="Searching for vulnerable packages", unit="package"):
        pkg = installed_pkgs[i]
        print(f"Searching for vulnerabilities in {pkg.name} ({pkg.version})...")
        # vulnerable_packages.append(VulnerablePackage(
        #     name=pkg.name,
        #     version=pkg.version,
        #     providerName=pkg.providerName,
        #     severity="High",
        #     severity_score=random.uniform(7.0, 10.0)
        # ))
        fl = open('nvdlib.json', 'r')
        cpe = nvdlib.searchCPE_V2(keywordSearch=pkg.name)
        for c in cpe:
            vsn = c.cpeName.split(':')[4]
            if vsn >= str(pkg.version):
                vulnerable_packages.append(VulnerablePackage(
                    name=pkg.name,
                    version=pkg.version,
                    providerName=pkg.providerName,
                    severity="High",
                    severity_score=random.uniform(7.0, 10.0)
                ))
                # json.dump(c.toJSON(), fl)
                print(c)
                break

    return vulnerable_packages