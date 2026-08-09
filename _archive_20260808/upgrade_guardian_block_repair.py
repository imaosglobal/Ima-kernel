from pathlib import Path

p = Path("ima_guardian_self_repair.py")
text = p.read_text(encoding="utf8")

start = text.find("def repair_unterminated_string")
end = text.find("def run()")

if start == -1:
    raise SystemExit("repair function missing")

new = r'''
def repair_unterminated_string(path):
    p = Path(path)

    if p.name != "daily_evolution.py":
        return False

    lines = p.read_text(encoding="utf8").splitlines()

    out = []
    inside_main = False
    cleaned = False

    for line in lines:

        if 'if __name__=="__main__":' in line:
            inside_main = True
            out.append(line)
            continue

        if inside_main:

            if "build_summary()" in line:
                out.append(line)
                continue

            if "import os" in line:
                out.extend([
                    "",
                    '    print("IMA DAILY EVOLUTION SAVED")',
                    ""
                ])
                inside_main = False
                out.append(line)
                cleaned = True
                continue

            if (
                line.lstrip().startswith("print(")
                or "IMA DAILY EVOLUTION SAVED" in line
                or line.strip() == ")"
            ):
                cleaned = True
                continue

        out.append(line)

    if cleaned:
        p.write_text(
            "\n".join(out)+"\n",
            encoding="utf8"
        )
        print("[GUARDIAN BLOCK REPAIR]", p)
        return True

    return False
'''

text = text[:start] + new + "\n\n" + text[end:]

p.write_text(text, encoding="utf8")

print("[OK] guardian block repair upgraded")
