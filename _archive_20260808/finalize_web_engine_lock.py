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


py_compile.compile(str(target), doraise=True)

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


for q in tests:
    r = mod.best_answer(q)

    if r:
    else:


try:
    import os
    os.chmod(target, 0o444)
except Exception as e:

