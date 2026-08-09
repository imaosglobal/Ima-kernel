import subprocess
import json
from pathlib import Path
from datetime import datetime


BASE=Path.home()/"ima_kernel"

OUT=BASE/".ima/evolution/git_history_memory.jsonl"


def git(cmd):

    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            cwd=BASE,
            text=True
        )
    except:
        return ""


def analyze():

    logs=git(
        "git log --pretty=format:'%h|%ad|%s' --date=short"
    )

    if not logs:
        print("NO GIT HISTORY FOUND")
        return


    OUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    seen=set()

    with open(
        OUT,
        "w",
        encoding="utf-8"
    ) as f:

        for line in logs.splitlines():

            parts=line.split("|",2)

            if len(parts)!=3:
                continue

            commit,date,msg=parts


            # דחיסת מידע
            key=msg.lower()

            if key in seen:
                continue

            seen.add(key)


            event={
                "date":date,
                "commit":commit,
                "event":msg,

                "learned_from":
                "git_history",

                "importance":
                "unknown"
            }


            text=msg.lower()

            if any(
                x in text
                for x in [
                    "memory",
                    "knowledge",
                    "learning",
                    "brain"
                ]
            ):
                event["domain"]="learning"

            elif any(
                x in text
                for x in [
                    "kernel",
                    "runtime",
                    "system"
                ]
            ):
                event["domain"]="kernel"

            elif any(
                x in text
                for x in [
                    "ui",
                    "app",
                    "frontend"
                ]
            ):
                event["domain"]="interface"

            else:
                event["domain"]="general"


            f.write(
                json.dumps(
                    event,
                    ensure_ascii=False
                )
                + "\n"
            )


    print(
        "GIT HISTORY COMPRESSED"
    )


if __name__=="__main__":
    analyze()
