from pathlib import Path

p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

if "import subprocess" not in text:
    text = text.replace(
        "from pathlib import Path\nimport json\nfrom datetime import datetime\n",
        "from pathlib import Path\nimport json\nimport subprocess\nfrom datetime import datetime\n"
    )

p.write_text(text, encoding="utf8")

print("[OK] guardian imports restored")
