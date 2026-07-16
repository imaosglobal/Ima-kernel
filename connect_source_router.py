from pathlib import Path
import py_compile

p=Path("learning/knowledge_runtime_bridge.py")

text=p.read_text(encoding="utf8")

if "source_router" not in text:

    text=text.replace(
        "from learning.source_manager import collect",
        "from learning.source_manager import collect\nfrom learning.knowledge_core.source_router import choose_sources"
    )

    text=text.replace(
        "sources = collect(question)",
        "route = choose_sources(question)\n    sources = collect(question)"
    )

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] router connected")
