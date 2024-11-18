import sys
import os

src_path = os.join(os.path.dirname(__file__), '../src')

sys.path.append(src_path)

import pytest

from get_assets import *

def test_translate_cmd():
    windows = Windows()
    assert windows.translate_cmd("Get-WmiObject Win32_Product") == "Get-WmiObject Win32_Product"

def test_parse_get_package():
    windows = Windows()
    stdout = "Name : Package1\nVersion : 1.0.0\nProviderName : Microsoft\n\nName : Package2\nVersion : 2.0.0\nProviderName : Microsoft\n"
    names, versions, providerNames = windows.parse_get_package(stdout)
    assert names == ["Package1", "Package2"]
    assert versions == ["1.0.0", "2.0.0"]
    assert providerNames == ["Microsoft", "Microsoft"]

def test_parse_get_package_wmi():
    windows = Windows()
    stdout = "Name : Package1\nVersion : 1.0.0\n\nName : Package2\nVersion : 2.0.0\n"
    names, versions = windows.parse_get_package_wmi(stdout)
    assert names == ["Package1", "Package2"]
    assert versions == ["1.0.0", "2.0.0"]

def test_exec_command():
    windows = Windows()
    result = windows.exec_command("Get-Command")
    assert result['success'] == True
    assert result['stdout'] != ''
    assert result['stderr'] == ''