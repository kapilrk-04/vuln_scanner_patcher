import requests
from bs4 import BeautifulSoup
import time

# check updatestar repo for non-MSU updates
def scrape_updatestar_results(query):
    print(f"Searching UpdateStar for updates for: {query}")
    try:
        url = f"https://www.updatestar.com/search?query={'+'.join(query.split())}"
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results_list = soup.select('div#main2 ul.media-list li.media a')
            if results_list:
                # Extract and return links if results exist
                print("Results found.")

                return [result['href'] for result in soup.find_all('a', href=True)]
            else:
                return "No results found."
    except Exception as e:
        print(f"Error fetching or parsing webpage: {e}")
    
    return "Failed to fetch or parse the webpage."
    
def extract_sourceforge_links(query):
    search_url = f"https://sourceforge.net/directory/?q={'+'.join(query.split())}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    project_links = soup.find_all('a', class_='result-heading-title')
    
    projects = []
    for link in project_links:
        href = link.get('href')
        name_tag = link.find('h3')
        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        
        projects.append({
            "name": name,
            "url": f"https://sourceforge.net{href}"
        })
    
    # for project in projects:
    #     print(f"Project Name: {project['name']}")
    #     print(f"Project URL: {project['url']}")
    #     print("-" * 40)

    return projects