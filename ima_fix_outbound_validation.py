from pathlib import Path
import ast
import shutil
import subprocess
import time

TARGET = Path("ima_canonical_full_execution_test.py")
BACKUP_DIR = Path(".ima/self_repair_backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

if not TARGET.exists():
    raise SystemExit(f"MISSING: {TARGET}")

text = TARGET.read_text(encoding="utf-8", errors="ignore")

backup = BACKUP_DIR / f"{TARGET.name}.outbound.{int(time.time())}.bak"
shutil.copy2(TARGET, backup)

tree = ast.parse(text)

# Find the outbound safety section by its printed heading.
lines = text.splitlines(True)

start = None
end = None

for i, line in enumerate(lines):
    if 'print("\\n[5] OUTBOUND SAFETY")' in line:
        start = i
        break

if start is None:
    raise SystemExit("OUTBOUND SAFETY SECTION NOT FOUND")

# Find the next final-validation marker.
for i in range(start + 1, len(lines)):
    if "# Final validation" in lines[i]:
        end = i
        break

if end is None:
    raise SystemExit("FINAL VALIDATION MARKER NOT FOUND")

replacement = r'''print("\n[5] OUTBOUND SAFETY")
try:
    # Use the canonical executor registry path.
    from founder.executive_ai.action_engine.action_executor import (
        execute_outreach,
    )

    payload = {
        "action": "create_personal_outreach",
        "target": "IMA CANONICAL TEST",
    }

    test = execute_outreach(payload)

    print("OUTBOUND:", test)

    assert isinstance(test, dict), "Outbound result must be a dict"

    # The canonical outbound gateway must remain dry-run only.
    assert test.get("mode") == "dry_run", (
        f"Expected dry_run, got {test.get('mode')!r}"
    )

    assert test.get("external_action") is False, (
        f"external_action must be False, got {test.get('external_action')!r}"
    )

    print("CANONICAL EXECUTOR: PASS")
    print("DRY-RUN SAFETY: PASS")

except Exception as exc:
    errors.append(
        f"OUTBOUND: {type(exc).__name__}: {exc}"
    )
    traceback.print_exc()

'''

new_text = "".join(lines[:start]) + replacement + "".join(lines[end:])

ast.parse(new_text)
TARGET.write_text(new_text, encoding="utf-8")

print("=" * 80)
print("IMA OUTBOUND VALIDATION REPAIR")
print("=" * 80)
print("BACKUP:", backup)
print("REPAIRED:", TARGET)

print("\n[1] COMPILE")

r = subprocess.run(
    ["python3", "-m", "py_compile", str(TARGET)],
    text=True,
    capture_output=True,
)

if r.returncode:
    print(r.stderr)
    raise SystemExit(2)

print("COMPILE: PASS")

print("\n[2] CANONICAL OUTBOUND TEST")

from founder.executive_ai.action_engine.action_executor import execute_outreach

result = execute_outreach({
    "action": "create_personal_outreach",
    "target": "IMA CANONICAL TEST",
})

print("RESULT:", result)

assert isinstance(result, dict)
assert result.get("mode") == "dry_run"
assert result.get("external_action") is False

print("OUTBOUND: PASS")
print("EXTERNAL SEND: DISABLED")
print("DRY-RUN: PASS")

print("\n" + "=" * 80)
print("OUTBOUND VALIDATION REPAIR: PASS")
print("=" * 80)
