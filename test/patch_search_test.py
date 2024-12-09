import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '../src')
sys.path.append(src_path)

import pytest

from search_utils import *
from oop_utils import VulnerablePackage
from patch_search import WindowsUpdateSearcher
from typing import List

def test_search_for_updates():
    searcher = WindowsUpdateSearcher()
    result = searcher.hierarchical_update_search("Slack")
    assert result != "Failed to fetch or parse the webpage."
    assert result != "No results found."
