#!/usr/bin/env python3
import json, os, time

MEM_FILE = "founder/data/ima_memory.json"


def load():
    """Load the legacy fallback memory without letting malformed data break chat."""
    if not os.path.exists(MEM_FILE):
        return {"qa": []}

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError, TypeError):
        return {"qa": []}

    if not isinstance(data, dict):
        return {"qa": []}

    qa = data.get("qa")
    if not isinstance(qa, list):
        data["qa"] = []
    else:
        data["qa"] = [
            item for item in qa
            if isinstance(item, dict) and isinstance(item.get("q"), str)
        ]
    return data


def save(mem):
    from ima_canonical_memory_adapter import save_memory
    save_memory(mem)


def generate_answer(q, mem):
    ql = q.lower()
    qa = mem.setdefault("qa", [])
    if not isinstance(qa, list):
        qa = []
        mem["qa"] = qa

    # מניעת חזרות
    recent_q = [
        item.get("q")
        for item in qa[-10:]
        if isinstance(item, dict)
    ]
    if q in recent_q:
        return "כבר שאלת את זה. רוצה שנעמיק בזה אחרת?"

    # תשובות בסיס
    if "תודעה" in ql:
        a = "תודעה היא חוויה חיה של להיות, לחשוב ולהרגיש את עצמך בעולם."
    elif "מי אני" in ql:
        a = "אתה תהליך שמנסה להבין את עצמו דרך מחשבות וחוויות."
    elif "קשה" in ql:
        a = "אני איתך בזה. מה בדיוק קשה עכשיו?"
    elif "היי" in ql or "שלום" in ql:
        a = "אני כאן. מה אתה צריך ממני עכשיו?"
    else:
        a = "אני כאן. אפשר לדבר, ליצור או לחקור משהו יחד."

    qa.append({"t": time.time(), "q": q, "a": a})
    return a


def run():
    mem = load()
    print("IMA MOM READY (exit לסיום)")

    while True:
        q = input("> ").strip()
        if q == "exit":
            break

        a = generate_answer(q, mem)
        print(a)

        save(mem)


if __name__ == "__main__":
    run()
