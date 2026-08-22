from pathlib import Path
import py_compile

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

old='''name=item.get(
                                    "source",
            item.get(
                                         "registry_source",
                            ""
                                        )
                                         )'''

new='''name=item.get("source") or item.get("registry_source") or ""'''

if old in text:
    text=text.replace(old,new)
else:
    import re
    text=re.sub(
        r'name=item\.get\([\s\S]*?\)\s*',
        'name=item.get("source") or item.get("registry_source") or ""\n',
        text,
        count=1
    )

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

