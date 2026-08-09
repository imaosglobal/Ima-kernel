from pathlib import Path
import py_compile
import json
import time

p=Path("learning/source_router.py")

text=p.read_text(encoding="utf8")

if "SOURCES =" not in text:
    text=text.replace(
        "import json",
        """import json

SOURCES = [
    "local",
    "wikidata",
    "wikipedia",
    "duckduckgo",
    "crossref",
    "arxiv"
]
"""
    )

p.write_text(text,encoding="utf8")

py_compile.compile(
    "learning/source_router.py",
    doraise=True
)

Path(".ima/web_source_router_fix.lock").write_text(
    json.dumps(
        {
            "state":"FIXED",
            "sources":[
                "local",
                "wikidata",
                "wikipedia",
                "duckduckgo",
                "crossref",
                "arxiv"
            ],
            "time":time.time()
        },
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)

print("WEB SOURCE ROUTER FIXED")
