from pathlib import Path
import shutil
import time

target=Path("ima_master_runtime.py")
backup=Path(f"ima_master_runtime.py.safe_backup_{int(time.time())}")

shutil.copy2(target, backup)

text=target.read_text(encoding="utf-8")

# remove broken injected loader block if it exists
start=text.find("def load_system_learning()")
end=text.find("def ask(self,message):")

if start != -1 and end != -1 and start < end:
    text=text[:start]+text[end:]

# repair accidental duplicate empty function area
text=text.replace(
    "def ask(self,message):\n\n\n",
    "def ask(self,message):\n"
)

target.write_text(text,encoding="utf-8")

import py_compile
py_compile.compile(
    str(target),
    doraise=True
)

