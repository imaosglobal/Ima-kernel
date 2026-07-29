from pathlib import Path

path = Path(
"founder/executive_ai/community/unified_crm.py"
)

content = path.read_text(
    encoding="utf8"
)

if "import time" not in content:
    content = "import time\n" + content

path.write_text(
    content,
    encoding="utf8"
)

print("UNIFIED CRM TIME IMPORT FIXED")
