from pathlib import Path

p=Path("ima_master_runtime.py")
s=p.read_text(encoding="utf-8")

if "def sanitize_memory_write" not in s:

    insert=r'''

def sanitize_memory_write(text):
    if not isinstance(text,str):
        return text

    bad=[
        "זיכרון משתמש:",
        "הקשר משתמש:",
        "הודעת משתמש:",
        "USER CONTEXT:",
        "Memory:",
        "את IMA.",
    ]

    for marker in bad:
        if marker in text:
            text=text.split(marker)[0]

    return text.strip()

'''

    s=s.replace(
        "IMA=IMAMaster()",
        insert+"\n\nIMA=IMAMaster()"
    )


# מנקה כל כתיבה של last_response
old='remember_user(\n            user_id,\n            "last_response",\n            reply\n        )'

new='remember_user(\n            user_id,\n            "last_response",\n            sanitize_memory_write(reply)\n        )'


if old in s:
    s=s.replace(old,new)

p.write_text(
    s,
    encoding="utf-8"
)

print("MEMORY POLLUTION PREVENTION INSTALLED")
