from pathlib import Path
import py_compile

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

if "register_external" not in text:

    text=text.replace(
        "registry = SourceRegistry()",
        "registry = SourceRegistry()\nfrom learning.sources.external_registry import register_external\nregister_external(registry)"
    )

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] external sources connected")
