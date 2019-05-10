from googlesearch import search
from setup import query, maxresults

# Create empty list to store all google results
google_results = []


# Find homepages to scrape based on inputs from setup.py
def search_google():
    for url in search(query, stop=maxresults, pause=5):
        google_results.append(url)
    return google_results
