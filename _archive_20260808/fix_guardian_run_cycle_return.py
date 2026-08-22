from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

    except Exception as e:

    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

            return
    except Exception as e:

    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

if old not in text:
else:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf8")
