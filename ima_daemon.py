#!/usr/bin/env python3
import time, json
from ima_system import load_events, emit, ask, git_snapshot

LEDGER = ".ima/ledger.jsonl"

def run():
    last_len = 0

    print("[IMA DAEMON] started")

    while True:
        try:
            events = load_events()

            if len(events) != last_len:
                last_len = len(events)

                print("[IMA DAEMON] event update:", last_len)

                # find new questions
                for e in events[-5:]:
                    if e["type"] == "QUESTION":
                        q = e["data"]["text"]
                        qid = e["data"].get("id", str(int(time.time())))

                        result = ask(q)

                        emit("ANSWER",
                             id=qid,
                             text=str(result["answers"]))

                git_snapshot()

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break

if __name__ == "__main__":
    run()
