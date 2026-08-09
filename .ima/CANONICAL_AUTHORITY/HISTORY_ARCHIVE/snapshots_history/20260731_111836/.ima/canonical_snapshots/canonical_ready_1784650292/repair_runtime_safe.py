from pathlib import Path
import shutil
import time

target=Path("ima_master_runtime.py")
backup=Path(f"ima_master_runtime.py.safe_backup_{int(time.time())}")

print("[1] backup")
shutil.copy2(target, backup)
print("backup:", backup)

text=target.read_text(encoding="utf-8")

# remove broken injected loader block if it exists
start=text.find("def load_system_learning()")
end=text.find("def ask(self,message):")

if start != -1 and end != -1 and start < end:
    print("[2] removing broken loader injection")
    text=text[:start]+text[end:]

# repair accidental duplicate empty function area
text=text.replace(
    "def ask(self,message):\n\n\n",
    "def ask(self,message):\n"
)

target.write_text(text,encoding="utf-8")

print("[3] compile test")
import py_compile
py_compile.compile(
    str(target),
    doraise=True
)

print("[OK] runtime restored")
