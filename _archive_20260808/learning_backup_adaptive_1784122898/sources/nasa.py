
from learning.sources.html_extractor import extract_text
import urllib.request

def search(question):
    try:
        with urllib.request.urlopen(
            "https://www.nasa.gov",
            timeout=5
        ) as r:
            text=r.read().decode("utf8","ignore")

        return {
            "content": text[:2000],
            "source":"NASA",
            "url":"https://www.nasa.gov",
            "confidence":0.7
        }

    except Exception:
        return None
