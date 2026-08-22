from pathlib import Path

p = Path("daily_evolution.py")
lines = p.read_text(encoding="utf8").splitlines()

out = []
i = 0

while i < len(lines):
    line = lines[i]

        # מדלגים על בלוק print שבור עד סגירת הקטע לפני import os
        if i+1 < len(lines) and 'IMA DAILY EVOLUTION SAVED' in lines[i+1]:
            out.extend([
                '        "IMA DAILY EVOLUTION SAVED"',
                '    )'
            ])

            i += 1
            while i < len(lines) and 'import os' not in lines[i]:
                i += 1

            continue

    out.append(line)
    i += 1

p.write_text("\n".join(out)+"\n", encoding="utf8")

