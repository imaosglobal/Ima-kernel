from pathlib import Path

files=[
    "evolution_brain.py",
    "goal_engine.py",
    "decision_engine.py"
]

old='Path.home()/"ima_kernel/.ima/evolution/evolution_brain.json"'
new='Path.home()/".ima/evolution/evolution_brain.json"'

for file in files:
    p=Path(file)

    if not p.exists():
        continue

    text=p.read_text()

    text=text.replace(old,new)

    if "mkdir(parents=True, exist_ok=True)" not in text:
        text=text.replace(
            'p=Path.home()/".ima/evolution/evolution_brain.json"',
            'p=Path.home()/".ima/evolution/evolution_brain.json"\n'
            'p.parent.mkdir(parents=True, exist_ok=True)'
        )

        text=text.replace(
            'OUT=BASE/".ima/evolution/evolution_brain.json"',
            'OUT=BASE/".ima/evolution/evolution_brain.json"\n'
            'OUT.parent.mkdir(parents=True, exist_ok=True)'
        )

    p.write_text(text)

