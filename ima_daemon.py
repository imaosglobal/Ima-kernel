import time
from ima_system import load_events, ask, git_snapshot, emit

seen = set()

def run():
    print("[IMA DAEMON] stable brain started")

    while True:
        try:
            events = load_events()

            for e in events:
                if e["type"] != "QUESTION":
                    continue

                qid = e["data"].get("id")
                if qid in seen:
                    continue

                seen.add(qid)

                question = e["data"].get("text", "")

                result = ask(question)

                # prevent duplicate ANSWER loops
                if result:
                    emit("ANSWER",
                         id=result["id"],
                         text=result["text"],
                         confidence=result["confidence"])

            git_snapshot()
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break
        except Exception as e:
            emit("ERROR", text=str(e))
            time.sleep(1)


if __name__ == "__main__":
    run()
