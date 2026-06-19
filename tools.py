from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


#creating tavily api tool

tavily =  TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for a recent and a reliable information on a topic. Returns Titles , URL and sippets"""
    results = tavily.search(query = query , max_results = 5)


    out = []

    for result in results['results']:
        out.append(
            f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n\n"
        )

    return "\n-----\n".join(out)


# print(web_search.invoke("What is the recent news of G7 summit?"))



# scrapper tool

@tool
def scrap_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:
        resp = requests.get(url , timeout=10 , headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]  # Limit to first 30,000 characters
    except Exception as e:
        return f"Error scraping the URL: {str(e)}"


# scrap_url = web_scraper.invoke("https://www.bbc.com/news/world-europe-66844149")
# print(scrap_url)
