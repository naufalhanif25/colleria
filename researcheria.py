# Importing necessary libraries and modules
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import popup
from cachetools import cached, TTLCache

# Cache initialization (TTL 10 minutes)
cache = TTLCache(maxsize = 100, ttl = 600)

async def get_sinta_ranking(session, journal):
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
        async with session.get(url, headers = headers) as response:  # Send HTTP GET request
            if response.status == 200:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")  # Parse the HTML content
                ranking_div = soup.find("div", class_ = "stat-prev mt-2")  # Find the ranking div

                if ranking_div:
                    ranking = ranking_div.text.strip()  # Extract and clean the ranking text

                    return ranking[:2]  # Return the first 2 characters of the ranking

    except aiohttp.ClientError:
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

async def search_journal(query, rows = 100):
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
        async with aiohttp.ClientSession() as session:  # Send HTTP GET request
            async with session.get(url, params = params) as response:
                if response.status == 200:  # Check if request was successful
                    return await response.json()  # Return JSON response

    except aiohttp.ClientError:
        popup.open_popup("Unable to perform request.\nPlease check your internet connection", True)  # Show error popup

    return None  # Return None if request failed

async def process_item(session, item):
    """
    This function processes received items and extracts relevant information.

    Parameters:
    - session: The aiohttp.ClientSession object used for making HTTP requests.
    - item: The item dictionary containing information about a journal article.

    Returns:
    - A formatted string containing the title, DOI, publication date, authors, APA citation,
      Sinta ranking or alternative ranking, and the URL of the journal article.
    """
    
    # Get the informations and details of the journal article
    title = item.get("title", ["N/A"])[0]
    doi = item.get("DOI", "N/A")
    published_date = item.get("published-online", {}).get("date-parts", [[0]])[0][0]
    volume = item.get("volume", "N/A")
    page = item.get("page", "N/A")
    issue = item.get("issue", "N/A")
    publisher = item.get("publisher", "N/A")
    authors = [f'{author.get("family", "")}, {author.get("given", "")}' for author in item.get("author", [])]

    # If no authors are found, use "N/A"
    if not authors:
        authors = ["N/A"]
    
    journal = item.get("container-title", ["N/A"])[0]
    ranking = await get_sinta_ranking(session, journal)

    # If Sinta ranking is not found, use an alternative ranking source
    if not ranking:
        ranking = f"https://www.scimagojr.com/journalsearch.php?q={journal}"

    # Create an APA citation for the journal article
    apa_citation = get_apa_citation(authors, title, journal, published_date, volume, issue, page)

    # Create the URL for the DOI of the journal article
    url = f"https://doi.org/{doi}"

    # Return the result in the specified format
    return f"{title}; {doi}; {published_date}; {', '.join(authors)}; {apa_citation}; {ranking}; {url}"

async def researcheria(query):
    """
    Function to perform research based on a query.
    
    Parameters:
    - query: The search query string.

    Returns:
    - List of formatted results.
    """

    # Search for journal articles using the query string
    results = await search_journal(query)

    # Check if results are found and the expected keys are present in the response
    if results and "message" in results and "items" in results["message"]:
        items = results["message"]["items"]  # Extract the list of items (journal articles) from the results

        # Create an aiohttp session for making HTTP requests
        async with aiohttp.ClientSession() as session:
            # Create a list of tasks to process each item concurrently
            tasks = [asyncio.create_task(process_item(session, item)) for item in items]
            
            # Wait for all tasks to complete and gather the results
            return await asyncio.gather(*tasks)
    else:
        # If no results found or there was an error with the request, log the error
        with open("bin/log/error_log.bin", "wb") as file:
            text = "No results found or there was an error with the request"

            file.write(text.encode("utf-8"))

        return []  # Return an empty list if no results are found

