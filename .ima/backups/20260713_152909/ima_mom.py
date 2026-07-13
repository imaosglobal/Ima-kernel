#!/usr/bin/env python3
import json, os, time

MEM_FILE = ".ima_mom_memory.json"

def load():
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE, "r") as f:
            return json.load(f)
    return {"qa": []}

def save(mem):
    with open(MEM_FILE, "w") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

def generate_answer(q, mem):
    ql = q.lower()

    # מניעת חזרות
    recent_q = [x["q"] for x in mem["qa"][-10:]]
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
        a = "אני שומעת אותך. תוכל להסביר קצת יותר?"

    mem["qa"].append({"t": time.time(), "q": q, "a": a})
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
