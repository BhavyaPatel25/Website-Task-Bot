import requests
from bs4 import BeautifulSoup
from langchain.tools import tool


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


@tool("web_loader")
def load_web_page(url: str) -> str:
    """
    Fetches a web page and returns cleaned HTML content.
    Strips scripts, styles, and non-visible elements.
    """

    try:
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=15
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.text, "lxml")

    # Remove scripts, styles, and irrelevant tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "iframe",
        "svg",
        "canvas"
    ]):
        tag.decompose()

    # Normalize whitespace-heavy tags
    for br in soup.find_all("br"):
        br.replace_with("\n")

    cleaned_html = soup.prettify()

    return cleaned_html
