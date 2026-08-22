from pathlib import Path
import shutil
import time
import json

ROOT = Path(".")
BACKUP = ROOT / ".ima" / "backup_before_brain_network"
LOCK = ROOT / ".ima" / "brain_network.lock"


def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)

    for f in [
        "ima_master_runtime.py",
        "ima_brain.py",
        ".ima/runtime/memory_bus.py"
    ]:
        p = ROOT / f
        if p.exists():
            shutil.copy2(
                p,
                BACKUP / p.name.replace("/", "_")
            )


def create_sync():

    p = ROOT / "brain_sync.py"

    if p.exists():
        return

    p.write_text(
'''import time
import json
from pathlib import Path

LOG = Path(".ima/brain_sync.jsonl")


BRAINS = []


def register(name, brain):
    BRAINS.append({
        "name": name,
        "brain": brain
    })


def broadcast(event):

    LOG.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LOG,"a") as f:
        f.write(
            json.dumps(event,ensure_ascii=False)
            +"\\n"
        )

    results=[]

    for item in BRAINS:
        try:
            obj=item["brain"]

            if hasattr(obj,"learn"):
                results.append(
                    item["name"]+":learn"
                )

        except Exception:
            pass

    return results


def status():
    return [
        x["name"]
        for x in BRAINS
    ]
''',
encoding="utf8"
)


def create_lock():

    LOCK.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    LOCK.write_text(
        json.dumps({
            "locked":True,
            "time":time.time(),
            "reason":
            "brain network stabilized"
        },indent=2),
        encoding="utf8"
    )


def verify():

    import importlib

    modules=[
        "ima_master_runtime",
        "ima_brain",
        "brain_sync"
    ]


    for m in modules:
        try:
            importlib.import_module(m)

        except Exception as e:


    import ima_master_runtime

    master=ima_master_runtime.IMAMaster()

    for q in [
        "אני עייף",
        "איך עובד מנוע בעירה",
        "מה זה חתול"
    ]:
        r=master.ask(q)

            "A:",
            r.get("response","")[:120]
        )


backup()
create_sync()
verify()
create_lock()

