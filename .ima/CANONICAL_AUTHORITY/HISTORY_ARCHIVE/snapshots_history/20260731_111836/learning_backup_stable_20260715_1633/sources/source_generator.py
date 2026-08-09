from pathlib import Path

def generate_source(name,url):
    slug=name.lower().replace(" ","_")

    file=Path(f"learning/sources/{slug}.py")

    code=f'''
import urllib.request

def search(question):
    try:
        with urllib.request.urlopen(
            "{url}",
            timeout=5
        ) as r:
            text=r.read().decode("utf8","ignore")

        return {{
            "content": text[:2000],
            "source":"{name}",
            "url":"{url}",
            "confidence":0.7
        }}

    except Exception:
        return None
'''

    file.write_text(code,encoding="utf8")
    return f"learning.sources.{slug}"

