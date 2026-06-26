import time, json, os

STATE_DIR = ".ima"
LEDGER = ".ima/ledger.jsonl"

os.makedirs(STATE_DIR, exist_ok=True)


def load():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(x) for x in f if x.strip()]


def emit(event):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")


def dedupe(events, text):
    return text in [e.get("text") for e in events[-30:] if e.get("type") == "QUESTION"]


def brain(text, events):
    if dedupe(events, text):
        return "כבר שאלת את זה. רוצה להמשיך משם?"

    if "היי" in text:
        return "אני כאן. מה באמת קורה אצלך עכשיו?"

    if "תודעה" in text:
        return "תודעה היא חוויה מתמשכת של קיום ועיבוד פנימי של המציאות."

    return "אני איתך. תמשיך."


def ask(text):
    events = load()

    emit({"ts": time.time(), "type": "QUESTION", "text": text})
    reply = brain(text, events)
    emit({"ts": time.time(), "type": "ANSWER", "text": reply})

    return reply


def status():
    events = load()
    print("=== IMA STABLE CORE ===")
    print("EVENTS:", len(events))


def run_daemon():
    last = 0
    print("[IMA DAEMON] started")

    while True:
        events = load()

        if len(events) != last:
            last = len(events)
            print("[IMA DAEMON] event update:", last)

            # מניעת לופי git / snapshot (קריטי!)
            # אין auto git commit יותר

        time.sleep(0.5)


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
    elif cmd == "daemon":
        run_daemon()
    else:
        status()
