from pathlib import Path
import ast
import shutil
import time
import subprocess

TARGET = Path("founder/executive_ai/action_engine/action_memory.py")

if not TARGET.exists():
    raise SystemExit(f"MISSING: {TARGET}")

backup = TARGET.with_name(
    TARGET.name + f".dedup.{int(time.time())}.bak"
)

shutil.copy2(TARGET, backup)

new_text = '''from founder.executive_ai.memory.memory_store import (
    save_memory,
    query_memory,
)


def _action_identity(action):
    """
    Canonical action identity.

    Identity is action + target only.
    Score/economics/reasoning are deliberately excluded.
    """
    if not isinstance(action, dict):
        return None

    action_name = action.get("action")
    target = action.get("target")

    if action_name is None or target is None:
        return None

    return (
        str(action_name),
        str(target),
    )


def save_action(action, result, reason):
    """
    Persist an action exactly once per canonical action identity.
    """

    identity = _action_identity(action)

    if identity is not None:
        try:
            existing = query_memory("actions")

            for record in existing:
                if not isinstance(record, dict):
                    continue

                value = record.get("value", record)

                if not isinstance(value, dict):
                    continue

                existing_action = value.get("action")

                if not isinstance(existing_action, dict):
                    continue

                if _action_identity(existing_action) == identity:
                    return record

        except Exception:
            # Memory lookup failure must not break action execution.
            pass

    return save_memory(
        "actions",
        {
            "action": action,
            "result": result,
            "reason": reason,
        },
    )


def get_actions():
    return query_memory("actions")
'''

ast.parse(new_text)
TARGET.write_text(new_text, encoding="utf-8")

print("=" * 80)
print("IMA ACTION MEMORY DEDUP REPAIR")
print("=" * 80)
print("BACKUP:", backup)
print("REPAIRED:", TARGET)

print("\n[1] AST")
ast.parse(TARGET.read_text(encoding="utf-8"))
print("AST: PASS")

print("\n[2] COMPILE")
r = subprocess.run(
    ["python3", "-m", "py_compile", str(TARGET)],
    text=True,
    capture_output=True,
)

if r.returncode:
    print(r.stderr)
    raise SystemExit(2)

print("COMPILE: PASS")

print("\n[3] IDENTITY TEST")

from founder.executive_ai.action_engine.action_memory import _action_identity

assert _action_identity({
    "action": "create_personal_outreach",
    "target": "OpenAI AI startup",
    "score": 100,
}) == (
    "create_personal_outreach",
    "OpenAI AI startup",
)

assert _action_identity({
    "action": "create_personal_outreach",
    "target": "OpenAI AI startup",
    "score": 999,
}) == (
    "create_personal_outreach",
    "OpenAI AI startup",
)

assert _action_identity({
    "action": "create_personal_outreach",
    "target": "Other target",
}) != (
    "create_personal_outreach",
    "OpenAI AI startup",
)

print("IDENTITY: PASS")
print("ACTION + TARGET ONLY: PASS")

print("\n" + "=" * 80)
print("ACTION MEMORY DEDUP REPAIR: PASS")
print("=" * 80)
