import time

DISCOVERY_INDEX = [
    ("Semantic Scholar",
     "https://www.semanticscholar.org",
     "research"),

    ("CERN",
     "https://home.cern",
     "science"),

    ("WHO",
     "https://www.who.int",
     "medical"),

    ("NOAA",
     "https://www.noaa.gov",
     "science"),

    ("Stanford",
     "https://www.stanford.edu",
     "education"),

]

def generate_candidates():

    from learning.sources.discovery_engine import discover_url

    results=[]

    for name,url,category in DISCOVERY_INDEX:

        results.append(
            discover_url(
                name,
                url,
                category
            )
        )

    return results
