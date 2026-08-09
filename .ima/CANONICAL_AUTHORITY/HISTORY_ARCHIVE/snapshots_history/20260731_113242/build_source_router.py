from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/source_router.py")

p.write_text("""
import re


SOURCE_MAP = {

    "person": [
        "Wikipedia",
        "DuckDuckGo",
        "Britannica"
    ],

    "definition": [
        "Wikipedia",
        "DuckDuckGo",
        "MIT"
    ],

    "science": [
        "Nature",
        "PubMed",
        "NASA",
        "arXiv"
    ],

    "technology": [
        "IEEE",
        "arXiv",
        "MIT"
    ],

    "general": [
        "Wikipedia",
        "DuckDuckGo",
        "Nature",
        "arXiv"
    ]

}


def detect_topic(question):

    q=question.lower()

    if any(x in q for x in [
        "who was",
        "who is",
        "biography",
        "born"
    ]):
        return "person"


    if any(x in q for x in [
        "quantum",
        "physics",
        "science",
        "research"
    ]):
        return "science"


    if any(x in q for x in [
        "computer",
        "ai",
        "software",
        "technology"
    ]):
        return "technology"


    if "what is" in q:
        return "definition"


    return "general"



def choose_sources(question):

    topic=detect_topic(question)

    return {
        "topic":topic,
        "sources":SOURCE_MAP.get(
            topic,
            SOURCE_MAP["general"]
        )
    }

""",encoding="utf8")


py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] source router created")
