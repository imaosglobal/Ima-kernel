from pathlib import Path

p = Path("daily_evolution.py")

lines = p.read_text(encoding="utf8").splitlines()

out = []
skip = False

for line in lines:
    if 'IMA DAILY EVOLUTION SAVED' in line:
        skip = True
        out.extend([
            '        "IMA DAILY EVOLUTION SAVED"',
            '    )'
        ])
        continue

    if skip:
        # מדלגים על שאר בלוק ההדפסה השבור
        if 'import os' in line:
            skip = False
            out.append(line)
        continue

    out.append(line)

p.write_text(
    "\n".join(out) + "\n",
    encoding="utf8"
)

