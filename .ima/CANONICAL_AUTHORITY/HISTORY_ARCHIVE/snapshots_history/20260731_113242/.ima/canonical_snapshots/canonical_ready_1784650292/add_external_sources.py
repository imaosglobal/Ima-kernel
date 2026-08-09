from pathlib import Path
import py_compile

base=Path("learning/sources")
base.mkdir(parents=True,exist_ok=True)

p=base/"external_registry.py"

p.write_text("""
def wikipedia(question):
    return {
        "source":"Wikipedia",
        "content":"",
        "confidence":8,
        "url":"https://en.wikipedia.org"
    }


def britannica(question):
    return {
        "source":"Britannica",
        "content":"",
        "confidence":8,
        "url":"https://britannica.com"
    }


def nature(question):
    return {
        "source":"Nature",
        "content":"",
        "confidence":9,
        "url":"https://nature.com"
    }


def pubmed(question):
    return {
        "source":"PubMed",
        "content":"",
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

print("[OK] external registry created")
