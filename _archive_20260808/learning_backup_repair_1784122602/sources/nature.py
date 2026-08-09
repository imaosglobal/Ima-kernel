
import urllib.request

def search(question):
    try:
        with urllib.request.urlopen(
            "https://www.nature.com",
            timeout=5
        ) as r:
            text=r.read().decode("utf8","ignore")

        return {
            "content": text[:2000],
            "source":"Nature",
            "url":"https://www.nature.com",
            "confidence":0.7
        }

    except Exception:
        return None
