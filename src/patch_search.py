import webbrowser
import requests
from typing import List
from oop_utils import VulnerablePackage, UpdateSearcher
from search_utils import scrape_updatestar_results, extract_sourceforge_links
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time

class WindowsUpdateSearcher(UpdateSearcher):
    def __init__(self, threshold: int = 70):
        """
        Initialize the WindowsUpdateSearcher with a fuzzy match threshold.
        
        Args:
            threshold (int): Fuzzy match threshold for result relevance.
        """
        self.threshold = threshold

    def hierarchical_update_search(self, query: str) -> str:
        """
        Search for updates using UpdateStar, SourceForge, and Google as fallback.
        Performs fuzzy matching on the results to filter relevant ones.
        
        Args:
            query (str): The search query (e.g., "PackageName").
        
        Returns:
            str: URL of the best match or Google Search link as a fallback.
        """
        # Check UpdateStar
        print(f"Checking UpdateStar for updates for: {query}")
        updatestar_results = scrape_updatestar_results(query)

        if isinstance(updatestar_results, list) and updatestar_results:
            print("Performing fuzzy search on UpdateStar results...")
            best_match = process.extractOne(query, updatestar_results, scorer=fuzz.partial_ratio)
            if best_match and best_match[1] >= self.threshold:
                print(f"Best match found on UpdateStar: {best_match[0]}")
                return best_match[0]
            else:
                print("No sufficiently relevant match found on UpdateStar.")

        # Check SourceForge
        print(f"Checking SourceForge for updates for: {query}")
        sourceforge_links = extract_sourceforge_links(query)
        if isinstance(sourceforge_links, list) and sourceforge_links:
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

    def search_for_updates(self, packages: List[VulnerablePackage]) -> List[str]:
        """
        Search for updates for the given packages.
        
        Args:
            packages (List[VulnerablePackage]): List of vulnerable packages to search for updates.
        
        Returns:
            List[str]: List of URLs pointing to potential updates.
        """
        results = []
        for package in packages:
            try:
                print(f"Searching for updates for package: {package.name}")
                result = self.hierarchical_update_search(package.name)
                results.append(result)
            except Exception as e:
                print(f"Error while searching for {package.name}: {e}")
        return results

    def open_links(self, links: List[str]):
        """
        Open the given links in a web browser.
        
        Args:
            links (List[str]): List of URLs to open.
        """
        for url in links:
            print(f"Opening link: {url}")
            webbrowser.open_new_tab(url)
            time.sleep(1) 

