from urllib.request import urlopen


URL = "https://www.britannica.com"


def search(question):
    try:
        data = urlopen(URL, timeout=5).read()
        content = data.decode("utf-8", errors="ignore")[:5000]
        return {
            "source": "Britannica",
            "content": content,
            "confidence": 8,
            "url": URL,
        }
    except Exception:
        return None
