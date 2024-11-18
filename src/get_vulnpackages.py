from oop_utils import VulnerablePackage
from typing import List
import random

def get_vulnerable_packages(installed_pkgs) -> List[VulnerablePackage]:
    vulnerable_packages = []

    for i in range(len(installed_pkgs)):
        pkg = installed_pkgs[i]
        vulnerable_packages.append(VulnerablePackage(
            name=pkg.name,
            version=pkg.version,
            providerName=pkg.providerName,
            severity="High",
            severity_score=random.uniform(7.0, 10.0)
        ))

    return vulnerable_packages