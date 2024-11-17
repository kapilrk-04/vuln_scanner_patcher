from utils import VulnerablePackage
from typing import List
import random

def get_vulnerable_packages(installed_pkgs) -> List[VulnerablePackage]:
    vulnerable_packages = []

    for i in range(10):
        pkg = random.choice(installed_pkgs)
        vulnerable_packages.append(VulnerablePackage(
            name=pkg.name,
            version=pkg.version,
            providerName=pkg.providerName,
            severity="High",
            severity_score=random.uniform(7.0, 10.0)
        ))

    return vulnerable_packages