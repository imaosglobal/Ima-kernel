from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

start = text.find("def smart_diff():")
end = text.find("def update_smart_state():")

if start == -1 or end == -1:
    raise SystemExit("smart_diff block not found")

new = r'''
def smart_diff():

    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True
        )

        files = [
            x.strip()
            for x in result.stdout.splitlines()
            if x.strip()
        ]

        return files

    except Exception as e:
        return []



'''

text = text[:start] + new + text[end:]

p.write_text(text, encoding="utf8")

