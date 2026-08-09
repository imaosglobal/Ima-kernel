from pathlib import Path
import shutil
import time
import json
import py_compile
import importlib

ROOT = Path(".")
BACKUP = ROOT / ".ima" / "backup_brain_network_finalize"
LOCK = ROOT / ".ima" / "FINAL_BRAIN_NETWORK_LOCK.json"


def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)

    files = [
        "ima_master_runtime.py",
        "ima_brain.py",
        "brain_sync.py",
        ".ima/runtime/memory_bus.py",
        "learning/learning_router.py",
        "learning/learning_loop.py"
    ]

    for f in files:
        src = ROOT / f
        if src.exists():
            shutil.copy2(
                src,
                BACKUP / src.name
            )


def patch_runtime():

    p = ROOT / "ima_master_runtime.py"

    if not p.exists():
        raise Exception("missing runtime")

    text = p.read_text(encoding="utf8")

    marker = "# BRAIN_NETWORK_SYNC"

    if marker in text:
        return "already"

    inject = '''

# BRAIN_NETWORK_SYNC
try:
    import brain_sync

    brain_sync.broadcast({
        "type": "ANSWER",
        "question": message,
        "answer": result.get("response",""),
        "time": time.time()
    })

except Exception:
    pass

'''

    text = text.replace(
        "return result",
        inject + "\n        return result",
        1
    )

    p.write_text(text,encoding="utf8")

    return "patched"


def verify_compile():

    files = [
        "ima_master_runtime.py",
        "ima_brain.py",
        "brain_sync.py"
    ]

    for f in files:
        py_compile.compile(
            f,
            doraise=True
        )

    return True


def verify_runtime():

    import ima_master_runtime

    m = ima_master_runtime.IMAMaster()

    tests = [
        "אני עייף",
        "איך עובד מנוע בעירה",
        "מה זה חתול"
    ]

    results=[]

    for q in tests:

        r=m.ask(q)

        results.append({
            "q":q,
            "ok":bool(r.get("response"))
        })

    return results


def lock():

    LOCK.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    LOCK.write_text(
        json.dumps({
            "status":"LOCKED",
            "time":time.time(),
            "system":
            "brain-network-finalized"
        },indent=2),
        encoding="utf8"
    )


backup()

print("BACKUP OK")

print(
    "RUNTIME:",
    patch_runtime()
)

print(
    "COMPILE:",
    verify_compile()
)

print(
    "TEST:",
    json.dumps(
        verify_runtime(),
        ensure_ascii=False,
        indent=2
    )
)

lock()

print("FINAL LOCK CREATED")
