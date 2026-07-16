from pathlib import Path
import shutil
import time
import py_compile

target = Path("learning/web_knowledge_collector.py")

if not target.exists():
    raise SystemExit("collector missing")

backup = target.with_name(
    target.stem + "_final_backup_" + str(int(time.time())) + ".py"
)

shutil.copy(target, backup)

print("[1] BACKUP CREATED")
print(backup)

print("[2] COMPILE CHECK")
py_compile.compile(str(target), doraise=True)

print("[3] IMPORT CHECK")
import importlib.util

spec = importlib.util.spec_from_file_location(
    "web_knowledge_collector",
    target
)

mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

tests = [
    "מה זה חתול",
    "קוואנטום",
    "ביולוגיה",
    "פיזיקה",
    "איינשטיין"
]

print("[4] KNOWLEDGE TEST")

for q in tests:
    r = mod.best_answer(q)

    if r:
        print("\nOK:", q)
        print("SOURCE:", r.get("source"))
        print("URL:", r.get("url"))
        print("TEXT:", r.get("content","")[:80])
    else:
        print("\nNO RESULT:", q)

print("\n[5] LOCK")

try:
    import os
    os.chmod(target, 0o444)
    print("LOCKED:", target)
except Exception as e:
    print("LOCK FAILED:", e)

print("\nFINAL STATUS: COMPLETE")
