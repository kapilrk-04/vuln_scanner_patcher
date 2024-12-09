import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '../src')

sys.path.append(src_path)

import pytest

from search_utils import *

def test_scrape_updatestar_results():
    results = scrape_updatestar_results("Slack")
    assert results != "Failed to fetch or parse the webpage."
    assert results != "No results found."

def test_extract_sourceforge_links():
    results = extract_sourceforge_links("qBittorrent")
    assert results != "Failed to fetch the webpage."
    assert len(results) > 0

def test_scrape_updatestar_results_no_results():
    results = scrape_updatestar_results("asdfasdfasdf")
    assert results == "No results found."

def test_extract_sourceforge_links_error():
    results = extract_sourceforge_links("afefefededefefefefefdeefefedfedfef")
    assert results == "Failed to fetch the webpage."

def test_no_updatestar_in_link():
    results = scrape_updatestar_results("https://www.google.com")
    assert results == "No results found."


