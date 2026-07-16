from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''if __name__ == "__main__":
    watch()
'''

new = '''if __name__ == "__main__":
    if "--status" in sys.argv:
        guardian_status()
    elif "--once" in sys.argv:
        run_once()
    elif "--daemon" in sys.argv:
        _original_watch()
    else:
        print("IMA Guardian Watch")
        print("use: --once | --daemon | --status")
'''

if old not in text:
    print("[FAIL] entry point not found")
else:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf8")
    print("[OK] watcher entry fixed")
