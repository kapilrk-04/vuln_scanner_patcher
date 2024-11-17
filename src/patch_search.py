import webbrowser
from typing import List
from utils import VulnerablePackage

# handle MSU updates?


def generate_search_links(dependencies: List[VulnerablePackage]) -> dict:
    """
    Generates Google search links for user-selected dependencies with version updates.

    Args:
        dependencies (list of tuple): List of dependencies as (package_name, version).

    Returns:
        dict: A dictionary of package names with their search prompts and URLs.
    """
    google_url = "https://www.google.com/search?q=" # last ditch effort
    microsoft_url = "https://www.catalog.update.microsoft.com/Search.aspx?q=" # for MSU updates
    updatestar_url = "https://www.updatestar.com/search?query=" # for non-MSU updates
    results = {}

    for package in dependencies:
        # Construct the search query
        # search_query = f"Patch for {package.name} {package.version}"
        if package.providerName == "msu":
            search_url = microsoft_url + "+".join(package.name.split())
        else:
            search_url = updatestar_url + "+".join(package.name.split())
        prompt = f"Search for: Patch for {package.name} {package.version}"
        results[package.name] = {"prompt": prompt, "url": search_url}

    return results


def open_links(results):
    """
    Open search links in the web browser and print prompts.

    Args:
        results (dict): Dictionary containing search prompts and URLs.
    """
    for package, details in results.items():
        print(details["prompt"])
        print(f"URL: {details['url']}\n")
        # Open the URL in the default web browser
        webbrowser.open(details["url"])


if __name__ == "__main__":
    # Example list of dependencies as (package_name, version).
    dependencies = [
        ("qbittorent", "5.0.1")
    ]

    # Generate search links and prompts.
    results = generate_search_links(dependencies)

    # Print and open the links.
    open_links(results)
