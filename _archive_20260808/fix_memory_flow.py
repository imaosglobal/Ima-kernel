from pathlib import Path
import shutil
import time

ROOT = Path(".")

def backup(path):
    if path.exists():
        b = path.with_suffix(path.suffix + f".backup_{int(time.time())}")
        shutil.copy2(path, b)
        print("[BACKUP]", b)

# -------------------------
# Fix conversation_layer.py
# -------------------------

p = ROOT / "conversation_layer.py"

if p.exists():
    backup(p)

    text = p.read_text(encoding="utf-8")

    old = '''    if any(cmd in q for cmd in memory_commands):
        return data[-10:]
'''

    new = '''    if any(cmd in q for cmd in memory_commands):

        filtered = []

        for item in reversed(data):
            question = item.get("question", "")

            # Ignore memory commands themselves
            if any(cmd in question for cmd in memory_commands):
                continue

            filtered.append(item)

            if len(filtered) >= 10:
                break

        return list(reversed(filtered))
'''

    if old in text:
        text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
        print("[OK] conversation_layer recall fixed")
    else:
        print("[SKIP] recall block not found")


# -------------------------
# Fix ima_master_runtime.py
# -------------------------

p = ROOT / "ima_master_runtime.py"

if p.exists():
    backup(p)

    text = p.read_text(encoding="utf-8")

    old = '''result["response"] = str(memory_hits[-5:])
'''

    new = '''result["response"] = "\\n\\n".join(
    [
        f"אתה שאלת: {x.get('question','')}\\nעניתי: {x.get('response','')}"
        for x in memory_hits
    ]
)
'''

    if old in text:
        text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
        print("[OK] IMAMaster memory output fixed")
    else:
        print("[SKIP] master memory block not found")


print()
print("=== VERIFY ===")

import subprocess
import sys

for f in [
    "conversation_layer.py",
    "ima_master_runtime.py"
]:
    if Path(f).exists():
        r = subprocess.run(
            [sys.executable, "-m", "py_compile", f],
            capture_output=True,
            text=True
        )

        if r.returncode == 0:
            print("[PASS]", f)
        else:
            print("[FAIL]", f)
            print(r.stderr)

print("DONE")
