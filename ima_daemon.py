import time
import os
import atexit

from ima_system import load_events, ask, git_snapshot, emit


LOCK_FILE = ".ima/daemon.lock"

def acquire_lock():
    os.makedirs(".ima", exist_ok=True)

    if os.path.exists(LOCK_FILE):
        print("[IMA DAEMON] already running")
        raise SystemExit(1)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    atexit.register(release_lock)


def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


seen = set()

def run():
    acquire_lock()
    print("[IMA DAEMON] stable brain started")

    seen_questions = set()
    answered = set()

    while True:
        try:
            events = load_events()

            for e in events:
                if e.get("type") != "QUESTION":
                    continue

                data = e.get("data", {})

                qid = data.get("id", e.get("ts"))

                if any(
                    x.get("type") == "ANSWER"
                    and x.get("data", {}).get("id") == qid
                    for x in events
                ):
                    continue

                if qid in answered:
                    continue

                if qid in seen_questions:
                    continue

                seen_questions.add(qid)

                question = data.get("text", e.get("text", ""))

                print("PROCESSING:", qid, question)
                ask(question, qid=qid)

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break

        except Exception as e:
            emit("ERROR", text=str(e))
            time.sleep(1)


if __name__ == "__main__":
    run()
