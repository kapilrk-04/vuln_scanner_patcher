import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '../src')

sys.path.append(src_path)

import pytest

from get_assets import *
from oop_utils import Package

def test_translate_cmd():
    windows = Windows()
    assert windows.translate_cmd("Get-WmiObject Win32_Product") == "Get-WmiObject Win32_Product"

def test_parse_get_package():
    windows = Windows()
    stdout = "Name : Package1\nVersion : 1.0.0\nProviderName : Microsoft\n\nName : Package2\nVersion : 2.0.0\nProviderName : Microsoft\n"
    names, _ = windows.parse_get_package(stdout)
    assert type(names) == list
    assert names == ["Package1", "Package2"]
    assert _ is None

def test_parse_get_package_wmi():
    windows = Windows()
    stdout = "Name : Package1\nVersion : 1.0.0\n\nName : Package2\nVersion : 2.0.0\n"
    names, err = windows.parse_get_package_wmi(stdout)
    assert names == []
    assert err is None



