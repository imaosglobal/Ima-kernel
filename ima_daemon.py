import time, json, os
from ima_system import answer, emit, load_events, git_snapshot

LEDGER = ".ima/ledger.jsonl"

last_size = 0


def run():
    global last_size

    print("[IMA DAEMON] live brain started")

    while True:
        if os.path.exists(LEDGER):
            size = os.path.getsize(LEDGER)

            if size != last_size:
                last_size = size

                events = load_events()
                last = events[-1]

                if last["type"] == "QUESTION":
                    q = last["data"]["text"]

                    response = answer(q, events)

                    emit("ANSWER", text=response)
                    print("[A]", response)

                    git_snapshot()

        time.sleep(0.5)


if __name__ == "__main__":
    run()
