#!/usr/bin/env python3

import os
import json
import time
import shutil
import importlib.util
from pathlib import Path

ROOT = Path.home() / "ima_kernel"
IMA = ROOT / ".ima"

REPORT = ROOT / "ima_universal_report.json"


def log(msg):
    print("[IMA]", msg)


def backup_file(path):
    try:
        if path.exists():
            b = path.with_suffix(path.suffix + ".backup")
            shutil.copy2(path, b)
    except Exception:
        pass


def check_python_files():
    broken=[]
    count=0

    for p in ROOT.rglob("*.py"):
        if any(x in str(p) for x in [
            "__pycache__",
            "node_modules"
        ]):
            continue

        count+=1

        try:
            compile(
                p.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ),
                str(p),
                "exec"
            )
        except Exception as e:
            broken.append({
                "file":str(p),
                "error":str(e)
            })

    return {
        "python_files":count,
        "broken":broken
    }


def clean_memory():

    targets=list(ROOT.rglob("user_memory.json"))

    fixed=[]

    for file in targets:

        try:
            data=json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            changed=False

            if isinstance(data,dict):

                for key,value in data.items():

                    if isinstance(value,dict):

                        if "last_response" in value:

                            old=value["last_response"]

                            if isinstance(old,dict):
                                text=old.get("value","")

                                for bad in [
                                    "הקשר משתמש:",
                                    "הודעת משתמש:",
                                    "USER CONTEXT:"
                                ]:
                                    if bad in text:
                                        text=text.split(bad)[0]
                                        changed=True

                                old["value"]=text.strip()

            if changed:

                backup_file(file)

                file.write_text(
                    json.dumps(
                        data,
                        ensure_ascii=False,
                        indent=2
                    ),
                    encoding="utf-8"
                )

                fixed.append(str(file))

        except Exception:
            pass


    return fixed


def check_runtime():

    result={}

    runtime=ROOT/"ima_master_runtime.py"

    result["exists"]=runtime.exists()

    if runtime.exists():

        text=runtime.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        result["has_ask"]="def ask" in text
        result["has_memory"]="memory" in text
        result["has_agi"]="IMA_AGI" in text

    return result


def scan_connectors():

    folder=ROOT/"connectors"

    result=[]

    if folder.exists():

        for x in folder.rglob("*"):
            if x.is_file():
                result.append(str(x.relative_to(ROOT)))

    return result


def create_gateway():

    gateway=IMA/"universal_gateway.json"

    data={
        "version":1,
        "created":time.time(),
        "services":{
            "chatgpt":{
                "status":"awaiting_api_key"
            },
            "whatsapp":{
                "status":"awaiting_meta_api"
            },
            "meta":{
                "status":"awaiting_oauth"
            },
            "future":{
                "status":"connector_ready"
            }
        }
    }

    IMA.mkdir(exist_ok=True)

    gateway.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return str(gateway)


def main():

    log("Starting universal repair")

    report={}

    report["python"]=check_python_files()

    report["memory_fixed"]=clean_memory()

    report["runtime"]=check_runtime()

    report["connectors"]=scan_connectors()

    report["gateway"]=create_gateway()

    REPORT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    log("DONE")
    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        )
    )


if __name__=="__main__":
    main()

