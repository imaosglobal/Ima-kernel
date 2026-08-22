import time

from learning.sources.discovery_engine import discover_url
from learning.sources.source_inspector import inspect_candidate
from learning.sources.update_candidates import update_candidate
from learning.sources.source_promoter import promote
from learning.source_manager import source_status
from learning.sources.runtime_refresh import refresh_sources
from learning.sources.web_discovery_daemon import discover_cycle


DEFAULT_SOURCES = [
    {
        "name":"PubMed",
        "url":"https://pubmed.ncbi.nlm.nih.gov",
        "category":"medical"
    },
    {
        "name":"NASA",
        "url":"https://www.nasa.gov",
        "category":"science"
    },
    {
        "name":"Nature",
        "url":"https://www.nature.com",
        "category":"research"
    },
    {
        "name":"IEEE",
        "url":"https://www.ieee.org",
        "category":"technology"
    }
]


def scan_sources():


    approved=[]

    for item in DEFAULT_SOURCES:

        candidate=discover_url(
            item["name"],
            item["url"],
            item["category"]
        )

        checked=inspect_candidate(candidate)

        update_candidate(checked)

            checked["name"],
            checked["status"],
            checked.get("trust_score")
        )

        if checked.get("trusted"):
            approved.append(
                checked["name"]
            )

    return approved



def learning_cycle():

    try:
        from learning.adaptive_learning_daemon import learning_cycle as adaptive_cycle
        adaptive_cycle()
    except Exception as e:


    scan_sources()

    discover_cycle()

    added=promote()

        "PROMOTED:",
        added
    )

    for s in refresh_sources():

        "ACTIVE SOURCES:"
    )

    for s in source_status():

        "=== COMPLETE ==="
    )


if __name__=="__main__":

    while True:

        try:
            learning_cycle()

        except Exception as e:
                "ERROR:",
                e
            )

        time.sleep(
            86400
        )
