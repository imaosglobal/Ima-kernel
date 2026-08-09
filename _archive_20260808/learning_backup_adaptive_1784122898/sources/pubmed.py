
from learning.sources.html_extractor import extract_text
import urllib.request

def search(question):
    try:
        with urllib.request.urlopen(
            "https://pubmed.ncbi.nlm.nih.gov",
            timeout=5
        ) as r:
            text=r.read().decode("utf8","ignore")

        return {
            "content": text[:2000],
            "source":"PubMed",
            "url":"https://pubmed.ncbi.nlm.nih.gov",
            "confidence":0.7
        }

    except Exception:
        return None
