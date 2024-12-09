import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '../src')
sys.path.append(src_path)

import pytest
import requests

from search_utils import scrape_updatestar_results, extract_sourceforge_links
from oop_utils import VulnerablePackage, Package
from patch_search import WindowsUpdateSearcher

def test_vulnerability_and_update_workflow():
    # Test applications for analysis
    test_applications = [
        {
            "product": "Steam",
            "version": "2.10.91.91",
            "vendor": "WMI"
        },
        {
            "product": "Slack",
            "version": "5.29.0",
            "vendor": "WMI"
        }
    ]

    # Step 1: API Vulnerability Analysis
    resp = requests.post("http://localhost:3000/api/analyze", json={"applications": test_applications})
    
    # Assertions for API response
    assert resp.status_code == 200
    api_results = resp.json()['results']
    
    # Check vulnerability analysis results
    assert len(api_results) > 0  # At least one vulnerable application
    
    # Step 2: Patch Search for Vulnerable Applications
    vulnerable_apps = []
    for result in api_results:
        vulnerable_apps.append(VulnerablePackage(
            name=result['application']['product'],
            version=result['application']['version'],
            providerName=result['application']['vendor'],
            cpe=result['cpe'],
            vulnerability_summary=result['vulnerability_summary']
        ))
    
    # Initialize Update Searcher
    searcher = WindowsUpdateSearcher()
    
    # Perform Update Search for Vulnerable Applications
    update_links = []
    for app in vulnerable_apps:
        update_result = searcher.hierarchical_update_search(app.name)
        
        # Assert that update search was successful
        assert update_result != "Failed to fetch or parse the webpage."
        assert update_result != "No results found."
        
        # Collect update links
        if update_result:
            update_links.append(update_result)
    
    # Additional Assertions
    assert len(update_links) > 0  # Ensure at least one update link was found
    
    # Optional: Print found update links for manual review
    print("Found Update Links:", update_links)

def test_multi_application_workflow():
    # Comprehensive test with multiple applications
    test_applications = [
        {
            "product": "Steam",
            "version": "2.10.91.91",
            "vendor": "WMI"
        },
        {
            "product": "Microsoft Visual C++ 2022 X86 Additional",
            "version": "14.34.31938",
            "vendor": "WMI"
        },
        {
            "product": "Slack",
            "version": "5.29.0",
            "vendor": "WMI"
        }
    ]

    # Perform API analysis
    resp = requests.post("http://localhost:3000/api/analyze", json={"applications": test_applications})
    
    # Assertions
    assert resp.status_code == 200
    api_results = resp.json()['results']
    
    # Track update search results
    comprehensive_update_results = {}
    
    # Initialize Update Searcher
    searcher = WindowsUpdateSearcher()
    
    # Process each application
    for app in test_applications:
        # Perform vulnerability analysis
        resp = requests.post("http://localhost:3000/api/analyze", json={"applications": [app]})
        results = resp.json()['results']
        
        # If vulnerable, search for updates
        if results:
            update_result = searcher.hierarchical_update_search(app['product'])
            comprehensive_update_results[app['product']] = update_result
    
    # Assertions for comprehensive workflow
    assert len(comprehensive_update_results) > 0
    for product, update_link in comprehensive_update_results.items():
        assert update_link != "Failed to fetch or parse the webpage."
        assert update_link != "No results found."