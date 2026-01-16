from langchain.tools import tool
import trafilatura
from bs4 import BeautifulSoup
from readability import Document


@tool("content_extractor")
def extract_content(html: str) -> str:
    """
    Extracts readable text content from cleaned HTML.
    Uses layered fallback strategy.
    """

    try:
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_links=False,
            output_format="txt"
        )
        if extracted and len(extracted.strip()) > 200:
            return extracted.strip()
    except Exception:
        pass

    try:
        doc = Document(html)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "html.parser")
        text = soup.get_text(separator="\n")
        if text and len(text.strip()) > 200:
            return text.strip()
    except Exception:
        pass

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")

    return "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )
