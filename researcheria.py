# Importing necessary libraries and modules
import requests
from bs4 import BeautifulSoup
import popup
from cachetools import cached, TTLCache

# Variable initialization
RESULT = []  # List to store the results

# Cache initialization (TTL 10 minutes)
cache = TTLCache(maxsize = 100, ttl = 600)

@cached(cache)
def get_sinta_ranking(session, journal):
    """
    Function to get Sinta ranking of a journal.
    
    Parameters:
    - session: The requests session object.
    - journal: The name of the journal to search for.

    Returns:
    - The Sinta ranking of the journal if found, otherwise False.
    """

    url = f"https://sinta.kemdikbud.go.id/journals/?q={journal}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = session.get(url, headers = headers)  # Send HTTP GET request

        if response.status_code == 200:  # Check if request was successful
            soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML content
            ranking_div = soup.find("div", class_ = "stat-prev mt-2")  # Find the ranking div

            if ranking_div:
                ranking = ranking_div.text.strip()  # Extract and clean the ranking text

                return ranking[:2]  # Return the first 2 characters of the ranking

    except requests.RequestException:
        popup.open_popup("Unable to perform request.\nPlease check your internet connection", True) # Show error popup

    return False  # Return False if ranking not found or request failed

def get_apa_citation(authors, title, journal, year, volume, issue, page):
    """
    Function to format APA citation.
    
    Parameters:
    - authors: List of authors.
    - title: Title of the journal article.
    - journal: Name of the journal.
    - year: Year of publication.
    - volume: Volume of the journal.
    - issue: Issue number of the journal.
    - page: Page numbers of the journal article.

    Returns:
    - Formatted APA citation string.
    """

    authors_str = ", ".join(authors)
    
    return f"{authors_str}. ({year}). {title}. {journal}, {volume}({issue}), {page}."

def search_journal(query, rows = 100):
    """
    Function to search for journal articles using Crossref API.
    
    Parameters:
    - query: Search query string.

    Returns:
    - JSON response if the request is successful, otherwise None.
    """

    url = "https://api.crossref.org/works"
    params = {"query" : query,
              "rows" : rows}

    try:
        response = requests.get(url, params = params)  # Send HTTP GET request

        if response.status_code == 200:  # Check if request was successful
            return response.json()  # Return JSON response

    except requests.RequestException:
        popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)  # Show error popup

    return None  # Return None if request failed

def researcheria(query):
    """
    Function to perform research based on a query.
    
    Parameters:
    - query: The search query string.

    Returns:
    - List of formatted results.
    """

    global RESULT

    RESULT.clear()  # Clear previous results

    results = search_journal(query)  # Search for journal articles
    
    if results and "message" in results and "items" in results["message"]:
        items = results["message"]["items"]
        
        with requests.Session() as session:
            for item in items:
                title = item.get("title", ["N/A"])[0]
                doi = item.get("DOI", "N/A")
                published_date = item.get("published-online", {}).get("date-parts", [[0]])[0][0]
                volume = item.get("volume", "N/A")
                page = item.get("page", "N/A")
                issue = item.get("issue", "N/A")
                publisher = item.get("publisher", "N/A")
                authors = [f'{author.get("family", "")}, {author.get("given", "")}' for author in item.get("author", [])]

                if not authors:
                    authors = ["N/A"]

                journal = item.get("container-title", ["N/A"])[0]
                    
                # Get Sinta ranking if not ranking: 
                ranking = get_sinta_ranking(session, journal)
                
                if not ranking:  # If Sinta ranking not found, use alternative ranking source
                    ranking = f"https://www.scimagojr.com/journalsearch.php?q={journal}"

                apa_citation = get_apa_citation(authors, title, journal, published_date, volume, issue, page)
                url = f"https://doi.org/{doi}"

                # Append formatted result to the RESULT list
                RESULT.append(f"{title}; {doi}; {published_date}; {', '.join(authors)}; {apa_citation}; {ranking}; {url}")

    else:
        # Log error if no results found or request failed
        with open("bin/log/error_log.bin", "wb") as file:
            text = "No results found or there was an error with the request"

            file.write(text.encode("utf-8"))

    return RESULT
