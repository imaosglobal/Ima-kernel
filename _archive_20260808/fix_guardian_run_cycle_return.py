from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            print("[OK] incremental cycle executed")
    except Exception as e:
        print("[INCREMENTAL ERROR]", e)

    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

new = '''            print("[OK] incremental cycle executed")
            return
    except Exception as e:
        print("[INCREMENTAL ERROR]", e)

    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

if old not in text:
    print("[FAIL] target not found")
else:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf8")
    print("[OK] master bypass connected")
