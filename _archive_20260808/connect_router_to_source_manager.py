from pathlib import Path
import py_compile

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

if "choose_sources" not in text:
    text=text.replace(
        "from learning.sources.auto_loader import load_sources",
        "from learning.sources.auto_loader import load_sources\nfrom learning.knowledge_core.source_router import choose_sources"
    )


old="""def collect(question):
    return registry.collect(
        question
    )
"""


new="""def collect(question):

    route = choose_sources(question)

    allowed = set(
        route.get("sources", [])
    )

    results=[]

    for item in registry.collect(question):

        name = item.get(
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


if old in text:
    text=text.replace(old,new)
else:
    print("[WARN] collect block not found")


p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] source manager router connected")
