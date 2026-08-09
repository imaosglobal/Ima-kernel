from pathlib import Path

p = Path("ima_guardian_self_repair.py")
text = p.read_text(encoding="utf8")

insert = r'''

def repair_unterminated_string(path):
    p = Path(path)

    if p.name != "daily_evolution.py":
        return False

    lines = p.read_text(encoding="utf8").splitlines()

    out = []
    skip = False
    changed = False

    for line in lines:
        if "IMA DAILY EVOLUTION SAVED" in line:
            out.extend([
                '    print(',
                '        "IMA DAILY EVOLUTION SAVED"',
                '    )'
            ])
            skip = True
            changed = True
            continue

        if skip:
            if line.strip().startswith("import ") or line.strip().startswith("os."):
                skip = False
                out.append(line)
            continue

        if line.strip() == ')"':
            changed = True
            continue

        out.append(line)

    if changed:
        p.write_text("\n".join(out)+"\n", encoding="utf8")
        print("[REPAIRED STRING]", path)

    return changed
'''

if "def repair_unterminated_string" not in text:
    text += insert

text = text.replace(
    "def repair_target(path):",
    "def repair_target(path):\n    repair_unterminated_string(path)"
)

p.write_text(text, encoding="utf8")

print("[OK] guardian string repair added")
