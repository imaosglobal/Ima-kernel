from pathlib import Path
import shutil
import time
import py_compile
import subprocess


backup = Path(".ima/snapshots/before_evolution_upgrade")
backup.mkdir(parents=True, exist_ok=True)

timestamp = str(int(time.time()))

# backup
for file in [
    "learning/learning_memory.py",
    "learning/evaluation_engine.py"
]:
    src = Path(file)
    if src.exists():
        dst = backup / f"{timestamp}_{src.name}"
        shutil.copy(src, dst)


# duplicate protection
memory = Path("learning/learning_memory.py")

text = memory.read_text(encoding="utf-8")

old = """def store_pattern(pattern):
    data = load_memory()
    data["patterns"].append({
        "time": str(datetime.now()),
        "pattern": pattern
    })
    save_memory(data)
"""

new = """def store_pattern(pattern):
    data = load_memory()

    existing = [
        x.get("pattern")
        for x in data.get("patterns", [])
    ]

    if pattern in existing:
        return {
            "status": "duplicate",
            "pattern": pattern
        }

    data["patterns"].append({
        "time": str(datetime.now()),
        "pattern": pattern
    })

    save_memory(data)

    return {
        "status": "stored",
        "pattern": pattern
    }
"""

if old in text:
    memory.write_text(text.replace(old,new), encoding="utf-8")
else:


# evolution cycle
cycle = Path("learning/ima_evolution_cycle.py")

cycle.write_text(
"""from learning.meta_orchestrator import run_meta_analysis
from learning.health_check import health_report
from learning.system_improvement_memory import summarize_improvements


def run_evolution_cycle():


    health = health_report()

    failed = [
        x for x in health
        if x["status"] != "ok"
    ]


    meta = run_meta_analysis()




if __name__ == "__main__":
    run_evolution_cycle()
""",
encoding="utf-8"
)




for file in [
    "learning/learning_memory.py",
    "learning/ima_evolution_cycle.py"
]:
    try:
        py_compile.compile(file, doraise=True)
    except Exception as e:



result = subprocess.run(
    ["python3", "learning/ima_evolution_cycle.py"],
    capture_output=True,
    text=True
)


if result.stderr:

