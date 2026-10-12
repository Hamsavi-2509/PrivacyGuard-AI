from pypdf import PdfReader
import requests
from bs4 import BeautifulSoup


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF."""

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_url(url):
    """Extract readable text from a privacy policy webpage."""

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unnecessary webpage elements
    for element in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header"
        ]
    ):
        element.decompose()

    text = soup.get_text(
        separator="\n"
    )

    return text.strip()