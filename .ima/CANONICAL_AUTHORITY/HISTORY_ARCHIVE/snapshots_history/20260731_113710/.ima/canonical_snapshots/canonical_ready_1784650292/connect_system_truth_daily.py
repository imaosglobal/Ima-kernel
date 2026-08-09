from pathlib import Path

p=Path("daily_evolution.py")

if p.exists():

    text=p.read_text()

    marker='''IMA DAILY EVOLUTION SAVED'''

    if "system_truth_layer.py" not in text:

        text=text.replace(
            marker,
            marker+'''

    import os
    os.system(
        "python system_truth_layer.py"
    )'''
        )

        p.write_text(text)

print("SYSTEM TRUTH CONNECTED TO DAILY EVOLUTION")
