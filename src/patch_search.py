import webbrowser
import requests
from typing import List
from oop_utils import VulnerablePackage
from search_utils import scrape_updatestar_results, extract_sourceforge_links
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time

# handling non-MSU updates
def hierarchical_update_search(query: str, threshold: int = 70):
    """
    Search for updates using UpdateStar, SourceForge, and Google as fallback.
    Performs fuzzy matching on the results to filter relevant ones.
    
    Args:
        query (str): The search query (e.g., "PackageName").
        threshold (int): Fuzzy match threshold for result relevance.
    
    Returns:
        None
    """
    # Check UpdateStar
    print(f"Checking UpdateStar for updates for: {query}")
    updatestar_results = scrape_updatestar_results(query)
    
    if isinstance(updatestar_results, list) and updatestar_results:
        # Perform fuzzy matching on UpdateStar results
        print("Performing fuzzy search on UpdateStar results...")
        if isinstance(updatestar_results, list):
            best_match = process.extractOne(query, updatestar_results, scorer=fuzz.partial_ratio)

            if best_match and best_match[1] >= threshold:
                print(f"Best match found on UpdateStar: {best_match[0]}")
                return best_match[0]
            else:
                print("No sufficiently relevant match found on UpdateStar.")
        else:
            best_match = None
            print("No results found on UpdateStar.")
    
    # Check SourceForge
    print(f"Checking SourceForge for updates for: {query}")
    sourceforge_links = extract_sourceforge_links(query)
    if sourceforge_links:
        print("Performing fuzzy search on SourceForge results...")
        best_match = process.extractOne(query, [link["name"] for link in sourceforge_links], scorer=fuzz.partial_ratio)
        
        if best_match and best_match[1] >= 80:
            matched_project = next(link for link in sourceforge_links if link["name"] == best_match[0])
            print(f"Best match found on SourceForge: {matched_project['name']}")
            return matched_project['url']
        else:
            print("No sufficiently relevant match found on SourceForge.")
    
    # Fallback to Google Search
    print("Falling back to Google Search...")
    google_search_url = f"https://www.google.com/search?q=Patch+for+{query.replace(' ', '+')}"
    return google_search_url


def open_links(results):
    for url in results:
        webbrowser.open_new_tab(url)


def search_for_updates(ostype, dependencies: List[VulnerablePackage]):
    """
    Search for updates for the given dependencies.

    Args:
        dependencies (list of tuple): List of dependencies as (package_name, version).
    """
    if ostype == "Windows":
        # Generate search links and prompts.
        # search updatestar for non-MSU updates
        results = None
        try:
            for dependency in dependencies:
                results = hierarchical_update_search(dependency.name)
                print(f"Opening link: {results}")
                time.sleep(1)
                open_links([results])
        except Exception as e:
            print(f"Error: {e}")
    # results = generate_search_links(dependencies)
    # open_links(results)
    return results

