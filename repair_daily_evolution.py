from pathlib import Path

p = Path("daily_evolution.py")
text = p.read_text(encoding="utf8")

old = '''    print(
        "IMA DAILY EVOLUTION SAVED

    import os
    os.system(
        "python system_truth_layer.py"
    )"
    )
'''

new = '''    print(
        "IMA DAILY EVOLUTION SAVED"
    )

    import os
    os.system(
        "python system_truth_layer.py"
    )
'''

if old not in text:
    print("[WARN] exact block not found, using line repair")

    lines = text.splitlines()

    start = None
    end = None

    for i,line in enumerate(lines):
        if 'print(' in line and i > 150:
            start = i
            break

    if start is not None:
        for i in range(start, len(lines)):
            if 'os.system(' in lines[i]:
                end = i
                break

    if start is not None and end is not None:
        lines[start:end] = [
            '    print(',
            '        "IMA DAILY EVOLUTION SAVED"',
            '    )',
            '',
        ]

        text="\n".join(lines)+"\n"

p.write_text(text,encoding="utf8")

print("[OK] daily evolution repaired")
