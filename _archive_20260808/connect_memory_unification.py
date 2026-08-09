from pathlib import Path
import subprocess

target = Path(".ima/runtime/memory_bus_v2.py")

backup = Path(".ima/runtime/memory_bus_v2.before_unification_connect.py")

if not backup.exists():
    backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
    print("[BACKUP]", backup)

text = target.read_text(encoding="utf-8")

if "memory_unification_layer" not in text:

    text = text.replace(
        "from pathlib import Path",
        "from pathlib import Path\n\nfrom .memory_unification_layer import sync as memory_sync"
    )

    text = text.replace(
        "def remember(event_type, data):",
        "def remember(event_type, data):\n    try:\n        memory_sync()\n    except Exception:\n        pass\n"
    )

    target.write_text(text, encoding="utf-8")
    print("[CONNECTED]")
else:
    print("[ALREADY CONNECTED]")

print("[COMPILE]")

r = subprocess.run(
    ["python3","-m","py_compile",str(target)],
    capture_output=True,
    text=True
)

if r.returncode:
    print("[FAILED]")
    print(r.stderr)
else:
    print("[COMPILE OK]")

print("=== MEMORY BUS CONNECTION COMPLETE ===")
