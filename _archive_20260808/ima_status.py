#!/usr/bin/env python3

from pathlib import Path
import subprocess
import json
import time


ROOT=Path(".")

STATUS=[]


def add(name,state,info=""):
    STATUS.append({
        "name":name,
        "state":state,
        "info":info
    })


def exists_check(name,path):
    p=Path(path)
    add(
        name,
        "ONLINE" if p.exists() else "MISSING",
        str(p)
    )


def run_check(name,cmd):

    try:
        r=subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        out=r.stdout.strip()

        add(
            name,
            "ONLINE" if r.returncode==0 else "FAIL",
            out[-200:]
        )

    except Exception as e:
        add(name,"FAIL",str(e))


def main():


    exists_check(
        "CANONICAL RUNTIME",
        "kernel/runtime/CANONICAL/IMA_RUNTIME.js"
    )

    exists_check(
        "STATE",
        "kernel/runtime/CANONICAL/IMA_STATE.js"
    )

    exists_check(
        "POLICY",
        "kernel/runtime/CANONICAL/IMA_POLICY.js"
    )

    exists_check(
        "SUPERVISOR",
        "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py"
    )

    exists_check(
        "WATCHDOG",
        "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"
    )

    exists_check(
        "MEMORY",
        ".ima/memory.json"
    )

    exists_check(
        "LEDGER",
        ".ima/ledger.jsonl"
    )

    exists_check(
        "PERSONALITY",
        ".ima/personality.json"
    )

    exists_check(
        "VOICE",
        ".ima/voice.json"
    )


    run_check(
        "RUNTIME ENGINE",
        [
            "python3",
            "-c",
        ]
    )


    run_check(
        "WATCHDOG",
        [
            "python3",
            "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"
        ]
    )


    for s in STATUS:
            "[{}] {:18} {}".format(
                s["state"],
                s["name"],
                s["info"]
            )
        )

    fails=[
        x for x in STATUS
        if x["state"]=="FAIL" or x["state"]=="MISSING"
    ]

    if fails:
        return 1

    return 0


if __name__=="__main__":
    raise SystemExit(main())
