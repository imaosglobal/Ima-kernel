from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

if "def auto_learn_from_question" not in s:

    s += r'''

# -------------------------
# IMA AUTO LEARNING LAYER
# -------------------------

def auto_learn_from_question(question):
    import re

    memory = load_state_memory()

    known = [
        "כאב",
        "פחד",
        "עומס",
        "בדידות",
        "שמחה",
        "כעס"
    ]

    for word in known:
        if word in question:
            if word not in memory["states"]:
                learn_state(
                    word,
                    [word],
                    "warm"
                )

    return memory
'''

    p.write_text(s)

else:
