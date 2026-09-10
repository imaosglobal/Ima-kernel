SOURCES = [
    {
        "name": "wikipedia",
        "type": "encyclopedia",
        "languages": "all",
        "enabled": True,
        "priority": 1
    },
    {
        "name": "wikidata",
        "type": "knowledge_graph",
        "languages": "all",
        "enabled": True,
        "priority": 2
    },
    {
        "name": "arxiv",
        "type": "scientific",
        "languages": "en",
        "enabled": True,
        "priority": 3
    },
    {
        "name": "openalex",
        "type": "research",
        "languages": "all",
        "enabled": True,
        "priority": 4
    },
    {
        "name": "pubmed",
        "type": "medical_research",
        "languages": "en",
        "enabled": True,
        "priority": 5
    },
    {
        "name": "open_library",
        "type": "books",
        "languages": "all",
        "enabled": True,
        "priority": 6
    }
]


def get_sources():
    return [
        s for s in SOURCES
        if s["enabled"]
    ]
