import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '../src')
sys.path.append(src_path)

import pytest
import requests

from search_utils import scrape_updatestar_results, extract_sourceforge_links
from oop_utils import VulnerablePackage, Package

def test_api():

    inp1 = {
        "product": "Steam",
        "version": "2.10.91.91",
        "vendor": "WMI"
    }

    inp2 = {
        "product": "Microsoft Visual C++ 2022 X86 Additional",
        "version": "14.34.31938",
        "vendor": "WMI"
    }

    # Test the API
    resp1 = requests.post("http://localhost:3000/api/analyze", json={"applications": [inp1]})
    resp2 = requests.post("http://localhost:3000/api/analyze", json={"applications": [inp2]})
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert len(resp1.json()['results']) == 1
    assert len(resp2.json()['results']) == 0
