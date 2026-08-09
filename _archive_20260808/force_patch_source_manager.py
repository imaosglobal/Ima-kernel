from pathlib import Path
import py_compile
import re

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

if "choose_sources" not in text:
    text=text.replace(
        "from learning.sources.auto_loader import load_sources",
        "from learning.sources.auto_loader import load_sources\nfrom learning.knowledge_core.source_router import choose_sources"
    )

pattern=r"def collect\(question\):.*?(?=\ndef source_status)"

replacement="""
def collect(question):

    route = choose_sources(question)

    allowed = set(
        route.get("sources", [])
    )

    results=[]

    for item in registry.collect(question):

        name=item.get(
            "source",
            item.get(
                "registry_source",
                ""
            )
        )

        if not allowed or name in allowed:
            results.append(item)

    return results


"""

new_text, count = re.subn(
    pattern,
    replacement,
    text,
    flags=re.S
)

if count == 0:
    print("[FAIL] collect function not found")
else:
    p.write_text(new_text, encoding="utf8")
    py_compile.compile(
        str(p),
        doraise=True
    )
    print("[OK] collect replaced")

