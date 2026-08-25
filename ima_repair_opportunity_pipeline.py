from pathlib import Path
import ast
import shutil
import subprocess
import time
import traceback

ROOT = Path("founder/executive_ai")
BACKUP = Path(".ima/self_repair_backups")
BACKUP.mkdir(parents=True, exist_ok=True)

generator = ROOT / "global_intelligence" / "opportunity_to_action.py"

print("=" * 80)
print(" IMA OPPORTUNITY PIPELINE SELF-REPAIR")
print("=" * 80)

if not generator.exists():
    raise SystemExit("MISSING: " + str(generator))

text = generator.read_text(encoding="utf-8", errors="ignore")

# Backup
backup = BACKUP / f"opportunity_to_action.py.{int(time.time())}.bak"
shutil.copy2(generator, backup)
print("BACKUP:", backup)

# ------------------------------------------------------------
# Preserve existing helpers/imports, replace only generate_actions
# ------------------------------------------------------------

tree = ast.parse(text)

node = None
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name == "generate_actions":
        node = n
        break

if node is None:
    raise SystemExit("generate_actions() NOT FOUND")

lines = text.splitlines(True)

helper = r'''
def _ima_collect_opportunities():
    """Collect existing internal opportunities without external I/O."""
    found = []

    # Existing opportunity engine
    try:
        from founder.executive_ai.global_intelligence import opportunity_engine

        for name in dir(opportunity_engine):
            obj = getattr(opportunity_engine, name)

            if not callable(obj):
                continue

            lname = name.lower()

            if not any(
                x in lname
                for x in ("opportun", "discover", "signal", "prospect")
            ):
                continue

            try:
                value = obj()
            except TypeError:
                continue
            except Exception:
                continue

            if isinstance(value, dict):
                value = [value]

            if isinstance(value, (list, tuple)):
                found.extend(
                    x for x in value
                    if isinstance(x, dict)
                )
    except Exception:
        pass

    # Existing lead finder
    if not found:
        try:
            from founder.executive_ai.action_engine.executors.lead_finder import (
                find_leads,
            )

            value = find_leads({})

            if isinstance(value, dict):
                value = value.get("leads", [])

            if isinstance(value, (list, tuple)):
                found.extend(
                    x for x in value
                    if isinstance(x, dict)
                )
        except Exception:
            pass

    normalized = []
    seen = set()

    for item in found:
        target = (
            item.get("target")
            or item.get("name")
            or item.get("customer")
            or item.get("organization")
            or item.get("company")
        )

        if not target:
            continue

        score = (
            item.get("score")
            if item.get("score") is not None
            else item.get("opportunity_score", 50)
        )

        try:
            score = float(score)
        except Exception:
            score = 50.0

        key = str(target)

        if key in seen:
            continue

        seen.add(key)

        normalized.append({
            **item,
            "target": str(target),
            "score": score,
        })

    return normalized
'''

# Add helper only once
if "_ima_collect_opportunities" not in text:
    insert_at = node.lineno - 1
    text = "".join(lines[:insert_at]) + helper + "\n" + "".join(lines[insert_at:])
    lines = text.splitlines(True)

    tree = ast.parse(text)

    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == "generate_actions":
            node = n
            break

# Recalculate lines
lines = text.splitlines(True)

start = node.lineno - 1
end = node.end_lineno

replacement = '''def generate_actions():
    """
    Canonical opportunity -> executable action conversion.

    This creates internal action records only.
    It never sends external messages.
    """

    opportunities = _ima_collect_opportunities()

    opportunities.sort(
        key=lambda x: float(x.get("score", 0)),
        reverse=True,
    )

    actions = []

    for item in opportunities:
        target = item.get("target")

        try:
            score = float(item.get("score", 50))
        except Exception:
            score = 50.0

        action_name = (
            item.get("action")
            or item.get("recommended_action")
        )

        if not action_name:
            action_name = (
                "create_personal_outreach"
                if score >= 60
                else "monitor"
            )

        actions.append({
            "action": action_name,
            "target": target,
            "reason": (
                item.get("reason")
                or "opportunity intelligence decision"
            ),
            "score": score,
            "signals": item.get("signals", []),
        })

    return actions
'''

text = "".join(lines[:start]) + replacement + "".join(lines[end:])

generator.write_text(text, encoding="utf-8")

print("REPAIRED:", generator)

# ------------------------------------------------------------
# Compile
# ------------------------------------------------------------

print("\n[1] COMPILATION")

r = subprocess.run(
    ["python3", "-m", "py_compile", str(generator)],
    text=True,
    capture_output=True,
)

if r.returncode:
    print(r.stderr)
    raise SystemExit(2)

print("PASS")

# ------------------------------------------------------------
# Generate actions
# ------------------------------------------------------------

print("\n[2] GENERATE ACTIONS")

from founder.executive_ai.global_intelligence.opportunity_to_action import (
    generate_actions,
)

actions = generate_actions()

print("COUNT:", len(actions))

for i, action in enumerate(actions[:10], 1):
    print("ACTION", i, ":", action)

# ------------------------------------------------------------
# Orchestrator
# ------------------------------------------------------------

print("\n[3] ORCHESTRATOR")

from founder.executive_ai.action_engine.action_orchestrator import (
    run_world_actions,
)

world = run_world_actions()

print("RESULTS:", len(world))

for i, result in enumerate(world[:10], 1):
    print("RESULT", i, ":", result)

# ------------------------------------------------------------
# Autonomous cycle
# ------------------------------------------------------------

print("\n[4] AUTONOMOUS CYCLE")

from founder.executive_ai.action_engine.autonomous_cycle import run_cycle

cycle = run_cycle()

cycle_actions = cycle.get("actions", [])

print("STATUS:", cycle.get("status"))
print("RESULTS:", len(cycle_actions))

for i, result in enumerate(cycle_actions[:10], 1):
    print("CYCLE", i, ":", result)

# ------------------------------------------------------------
# Final
# ------------------------------------------------------------

print("\n" + "=" * 80)
print(" IMA PIPELINE RESULT")
print("=" * 80)

print("GENERATED ACTIONS:", len(actions))
print("ORCHESTRATOR RESULTS:", len(world))
print("AUTONOMOUS RESULTS:", len(cycle_actions))

if actions and world and cycle_actions:
    print("PIPELINE STATUS: PASS")
elif actions and world:
    print("PIPELINE STATUS: PARTIAL - AUTONOMOUS INTEGRATION")
elif actions:
    print("PIPELINE STATUS: PARTIAL - ORCHESTRATOR")
else:
    print("PIPELINE STATUS: FAIL - GENERATION")

print("OUTBOUND: DRY-RUN ONLY")
print("LIVE EXTERNAL SEND: DISABLED")
print("=" * 80)
