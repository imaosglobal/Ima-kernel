import urllib.request
import urllib.parse
import json
import time

from learning.sources.discovery_engine import discover_url
from learning.sources.source_inspector import inspect_candidate
from learning.sources.update_candidates import update_candidate
from learning.sources.source_promoter import promote


SEARCH_TARGETS = [
    ("Google Scholar","https://scholar.google.com","research"),
    ("PubMed","https://pubmed.ncbi.nlm.nih.gov","medical"),
    ("NASA","https://www.nasa.gov","science"),
    ("Nature","https://www.nature.com","research"),
    ("IEEE","https://www.ieee.org","technology"),
    ("MIT","https://www.mit.edu","education")
]


def discover_cycle():

    print("=== WEB DISCOVERY CYCLE ===")

    approved=[]

    for name,url,category in SEARCH_TARGETS:

        print("[CHECK]",name)

        candidate=discover_url(
            name,
            url,
            category
        )

        checked=inspect_candidate(candidate)

        update_candidate(checked)

        print(
            checked["status"],
            checked.get("trust_score")
        )

        if checked.get("trusted"):
            approved.append(name)


    added=promote()

    print("APPROVED:",approved)
    print("PROMOTED:",added)

    return added


if __name__=="__main__":
    discover_cycle()
