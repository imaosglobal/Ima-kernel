from pathlib import Path

p = Path("ima_guardian_watch.py")

if not p.exists():
    print("[FAIL] ima_guardian_watch.py missing")
    raise SystemExit(1)

text = p.read_text(encoding="utf8")

if "--once" in text:
    print("[OK] watcher already upgraded")
    raise SystemExit(0)

text = text.replace(
    "import time",
    "import time\nimport sys"
)

text += r'''

# --- IMA Guardian modes ---

def guardian_status():
    print("=== IMA GUARDIAN STATUS ===")
    print("watcher:", Path("ima_guardian_watch.py").exists())
    print("controller:", Path("ima_guardian_controller.py").exists())
    print("audit:", Path("IMA_AUDIT_REPORT.json").exists())


def run_once():
    import subprocess
    subprocess.run(
        ["python3", "ima_guardian_controller.py"]
    )


_original_watch = watch

def watch_mode():
    if "--status" in sys.argv:
        guardian_status()
        return

    if "--once" in sys.argv:
        run_once()
        return

    _original_watch()


watch = watch_mode
'''

p.write_text(text, encoding="utf8")

print("[OK] watcher modes added")
