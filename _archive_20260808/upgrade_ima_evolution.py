from pathlib import Path
import shutil
import time
import py_compile
import subprocess

print("=== IMA EVOLUTION UPGRADE ===")

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
        print("BACKUP:", dst)


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
    print("UPDATED: duplicate protection")
else:
    print("duplicate block already updated or not found")


# evolution cycle
cycle = Path("learning/ima_evolution_cycle.py")

cycle.write_text(
"""from learning.meta_orchestrator import run_meta_analysis
from learning.health_check import health_report
from learning.system_improvement_memory import summarize_improvements


def run_evolution_cycle():

    print("=== IMA EVOLUTION CYCLE ===")

    health = health_report()

    failed = [
        x for x in health
        if x["status"] != "ok"
    ]

    print("HEALTH FAILED:", len(failed))

    meta = run_meta_analysis()

    print("CAPABILITIES:", meta["capabilities"])
    print("SUGGESTIONS:", len(meta["suggestions"]))

    print()
    print("SYSTEM HISTORY:")
    print(summarize_improvements())


if __name__ == "__main__":
    run_evolution_cycle()
""",
encoding="utf-8"
)

print("CREATED: learning/ima_evolution_cycle.py")


print()
print("=== COMPILE CHECK ===")

for file in [
    "learning/learning_memory.py",
    "learning/ima_evolution_cycle.py"
]:
    try:
        py_compile.compile(file, doraise=True)
        print("OK:", file)
    except Exception as e:
        print("ERROR:", file, e)


print()
print("=== EVOLUTION TEST ===")

result = subprocess.run(
    ["python3", "learning/ima_evolution_cycle.py"],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

print("=== COMPLETE ===")
