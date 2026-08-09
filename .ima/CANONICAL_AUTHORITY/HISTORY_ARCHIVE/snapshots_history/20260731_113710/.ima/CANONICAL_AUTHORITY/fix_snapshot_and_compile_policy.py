from pathlib import Path
import json

controller = Path(".ima/self_repair/ima_autonomous_controller.py")

if not controller.exists():
    raise SystemExit("controller missing")

s = controller.read_text(encoding="utf-8")

backup = controller.with_suffix(".py.before_single_snapshot")
backup.write_text(s, encoding="utf-8")

# הוספת החרגות אם לא קיימות
marker = "HISTORY_EXCLUDE_PATHS"

if marker not in s:
    inject = '''

HISTORY_EXCLUDE_PATHS = [
    ".ima/self_repair/snapshots",
    ".ima/runtime_snapshots",
    ".ima/canonical_snapshots",
    ".ima/REPAIR_BACKUPS",
    "backup",
    "backups"
]

def is_history_file(path):
    p = str(path)
    return any(x in p for x in HISTORY_EXCLUDE_PATHS)

'''
    s = inject + s


# החלפה של בדיקות compile כדי לדלג על היסטוריה
if "is_history_file" in s:
    s = s.replace(
        "for file in files:",
        "for file in files:\n        if is_history_file(file):\n            continue"
    )

controller.write_text(s, encoding="utf-8")


policy = Path(".ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT_POLICY.json")

policy.write_text(
json.dumps(
{
 "snapshot_mode":"single_canonical",
 "max_active_snapshots":1,
 "nested_snapshots":False,
 "compile_history":False
},
indent=2
),
encoding="utf-8"
)

print("SINGLE SNAPSHOT POLICY INSTALLED")
print(policy)
print("backup:")
print(backup)

