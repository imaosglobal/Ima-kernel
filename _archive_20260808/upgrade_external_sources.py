from pathlib import Path
import py_compile

p=Path("learning/sources/external_registry.py")

p.write_text("""
from urllib.request import urlopen
from urllib.parse import quote


def fetch(url):
    try:
        data=urlopen(
            url,
            timeout=5
        ).read()

        return data.decode(
            "utf8",
            errors="ignore"
        )[:5000]

    except Exception:
        return ""


def wikipedia(question):

    url="https://en.wikipedia.org/wiki/" + quote(
        question.replace(" ","_")
    )

    return {
        "source":"Wikipedia",
        "content":fetch(url),
        "confidence":8,
        "url":url
    }


def britannica(question):

    return {
        "source":"Britannica",
        "content":fetch("https://www.britannica.com"),
        "confidence":8,
        "url":"https://www.britannica.com"
    }


def nature(question):

    return {
        "source":"Nature",
        "content":fetch("https://www.nature.com"),
        "confidence":9,
        "url":"https://www.nature.com"
    }


def pubmed(question):

    return {
        "source":"PubMed",
        "content":fetch("https://pubmed.ncbi.nlm.nih.gov"),
        "confidence":8,
        "url":"https://pubmed.ncbi.nlm.nih.gov"
    }


def register_external(registry):

    registry.register(
        "Wikipedia",
        wikipedia,
        priority=90
    )

    registry.register(
        "Britannica",
        britannica,
        priority=85
    )

    registry.register(
        "Nature",
        nature,
        priority=90
    )

    registry.register(
        "PubMed",
        pubmed,
        priority=85
    )
""",encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

