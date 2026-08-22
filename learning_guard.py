from pathlib import Path
import hashlib
import json
import time

STATE = Path(".ima/learning_guard_state.json")
STATE.parent.mkdir(exist_ok=True)

BLOCK_PATTERNS = [
    "תוכנית שיפור מערכת:",
    "suggestion:",
    "improvement_plan",
    "meta_analysis_completed"
]

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

def should_learn(text):
    if not text:
        return False

    for pattern in BLOCK_PATTERNS:
        if pattern in text:
            return False

    return True

def filter_learning(event):
    text = str(event.get("text",""))

    result = {
        "allowed": should_learn(text),
        "timestamp": time.time(),
    }

    save_state(result)

    return result["allowed"]

def save_state(data):
    old=[]

    if STATE.exists():
        try:
            old=json.loads(
                STATE.read_text(encoding="utf-8")
            )
        except:
            old=[]

    old.append(data)

    STATE.write_text(
        json.dumps(
            old[-500:],
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

