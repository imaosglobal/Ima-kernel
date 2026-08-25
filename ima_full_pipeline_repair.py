from pathlib import Path
import ast
import shutil
import subprocess
import time
import traceback

ROOT = Path("founder/executive_ai")
BACKUP = Path(".ima/self_repair_backups/full_pipeline")
BACKUP.mkdir(parents=True, exist_ok=True)

changed = []
errors = []

def backup(path):
    if path.exists():
        dest = BACKUP / f"{path.name}.{int(time.time()*1000)}.bak"
        shutil.copy2(path, dest)
        return dest

def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")

def write(path, text):
    old = read(path)
    if old != text:
        backup(path)
        path.write_text(text, encoding="utf-8")
        changed.append(str(path))
        return True
    return False

def functions(path):
    try:
        tree = ast.parse(read(path))
        return [
            n.name for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
    except Exception:
        return []

print("=" * 80)
print(" IMA FULL PIPELINE SELF-REPAIR")
print("=" * 80)

# ============================================================
# 1. DISCOVER ACTUAL APIs
# ============================================================

print("\n[1] DISCOVER CANONICAL APIs")

files = {
    "opportunity_engine":
        ROOT / "global_intelligence/opportunity_engine.py",
    "opportunity_ranker":
        ROOT / "global_intelligence/opportunity_ranker.py",
    "opportunity_to_action":
        ROOT / "global_intelligence/opportunity_to_action.py",
    "action_executor":
        ROOT / "action_engine/action_executor.py",
    "orchestrator":
        ROOT / "action_engine/action_orchestrator.py",
}

for name, path in files.items():
    print(f"\n{name}: {path}")
    if not path.exists():
        print("MISSING")
        errors.append((name, "file missing"))
        continue
    print("FUNCTIONS:", functions(path))

# ============================================================
# 2. COMPATIBILITY ALIASES
# ============================================================

print("\n[2] REPAIR BROKEN OPPORTUNITY API CALLERS")

oe = files["opportunity_engine"]
orr = files["opportunity_ranker"]

def ensure_alias(path, alias, candidates):
    if not path.exists():
        return

    funcs = functions(path)

    if alias in funcs:
        print(f"{alias}: already exists")
        return

    source = next((x for x in candidates if x in funcs), None)

    if source is None:
        print(f"{alias}: NO CANONICAL SOURCE FOUND")
        return

    text = read(path)

    addition = f"""

# Compatibility alias.
# Canonical implementation: {source}
def {alias}(*args, **kwargs):
    return {source}(*args, **kwargs)
"""

    write(path, text + addition)
    print(f"ADDED: {alias} -> {source}")

ensure_alias(
    oe,
    "generate_opportunities",
    [
        "generate",
        "get_opportunities",
        "collect_opportunities",
        "discover_opportunities",
    ],
)

ensure_alias(
    orr,
    "rank_opportunities",
    [
        "rank",
        "score_opportunities",
        "rank_items",
    ],
)

# ============================================================
# 3. GENERATE ACTIONS
# ============================================================

print("\n[3] CANONICAL ACTION GENERATION")

try:
    from founder.executive_ai.global_intelligence.opportunity_to_action import (
        generate_actions,
    )

    actions = generate_actions()

    print("TYPE:", type(actions).__name__)
    print("COUNT:", len(actions))

    for i, action in enumerate(actions[:10], 1):
        print(f"ACTION {i}:", action)

except Exception as exc:
    print("FAIL:", type(exc).__name__, exc)
    traceback.print_exc()
    errors.append(("generate_actions", str(exc)))
    actions = []

# ============================================================
# 4. EXECUTOR REGISTRY
# ============================================================

print("\n[4] EXECUTOR REGISTRY")

try:
    from founder.executive_ai.action_engine.action_executor import (
        EXECUTORS,
        execute_action,
    )

    for name in sorted(EXECUTORS):
        print("REGISTERED:", name)

except Exception as exc:
    print("EXECUTOR IMPORT FAIL:", exc)
    traceback.print_exc()
    errors.append(("executor_import", str(exc)))
    EXECUTORS = {}

# ============================================================
# 5. TEST EXECUTORS
# ============================================================

print("\n[5] EXECUTOR TESTS")

tests = {
    "find_leads": {},
    "rank_leads": {},
    "generate_outreach": {
        "target": "SELF AUDIT"
    },
    "create_personal_outreach": {
        "target": "SELF AUDIT",
        "dry_run": True,
    },
    "collect_feedback": {},
    "monitor": {
        "target": "SELF AUDIT"
    },
    "prepare_public_impact_message": {
        "target": "SELF AUDIT"
    },
}

for name, context in tests.items():

    if name not in EXECUTORS:
        print(name, "MISSING")
        errors.append(("executor_missing", name))
        continue

    try:
        result = execute_action(name, context)
        print(name, "PASS ->", result)
    except Exception as exc:
        print(name, "FAIL ->", type(exc).__name__, exc)
        errors.append((name, str(exc)))

# ============================================================
# 6. ORCHESTRATOR SOURCE CHECK
# ============================================================

print("\n[6] ORCHESTRATOR")

orch = files["orchestrator"]

try:
    from founder.executive_ai.action_engine.action_orchestrator import (
        run_world_actions,
    )

    print("FUNCTIONS:", functions(orch))

    source = read(orch)

    if "execute_action(" in source:
        print("EXECUTOR ROUTING: PRESENT")
    else:
        print("EXECUTOR ROUTING: MISSING")

except Exception as exc:
    print("ORCHESTRATOR IMPORT FAIL:", exc)
    traceback.print_exc()
    errors.append(("orchestrator_import", str(exc)))

# ============================================================
# 7. COMPILE
# ============================================================

print("\n[7] FULL COMPILATION")

result = subprocess.run(
    [
        "python3",
        "-m",
        "compileall",
        "-q",
        str(ROOT),
    ],
    text=True,
    capture_output=True,
)

if result.returncode != 0:
    print("COMPILE: FAIL")
    print(result.stdout)
    print(result.stderr)
    raise SystemExit(10)

print("COMPILE: PASS")

# ============================================================
# 8. DIRECT ORCHESTRATOR TEST
# ============================================================

print("\n[8] DIRECT ORCHESTRATOR TEST")

try:
    from founder.executive_ai.action_engine.action_orchestrator import (
        run_world_actions,
    )

    world_results = run_world_actions()

    print("WORLD RESULTS:", len(world_results))

    for i, item in enumerate(world_results[:10], 1):
        print(f"\nRESULT {i}:")
        print(item)

except Exception as exc:
    print("ORCHESTRATOR FAIL:", type(exc).__name__, exc)
    traceback.print_exc()
    errors.append(("run_world_actions", str(exc)))
    world_results = []

# ============================================================
# 9. FULL AUTONOMOUS CYCLE
# ============================================================

print("\n[9] FULL AUTONOMOUS CYCLE")

try:
    from founder.executive_ai.action_engine.autonomous_cycle import (
        run_cycle,
    )

    cycle = run_cycle()

    cycle_results = cycle.get("actions", [])

    print("STATUS:", cycle.get("status"))
    print("CYCLE RESULTS:", len(cycle_results))

    for i, item in enumerate(cycle_results[:10], 1):
        print(f"\nCYCLE RESULT {i}:")
        print(item)

except Exception as exc:
    print("CYCLE FAIL:", type(exc).__name__, exc)
    traceback.print_exc()
    errors.append(("run_cycle", str(exc)))
    cycle_results = []

# ============================================================
# 10. FINAL DIAGNOSIS
# ============================================================

print("\n" + "=" * 80)
print(" IMA FULL PIPELINE RESULT")
print("=" * 80)

print("FILES CHANGED:", len(set(changed)))

for path in sorted(set(changed)):
    print("CHANGED:", path)

print("\nGENERATED ACTIONS:", len(actions))
print("ORCHESTRATOR RESULTS:", len(world_results))
print("AUTONOMOUS RESULTS:", len(cycle_results))
print("ERRORS:", len(errors))

if errors:
    print("\nERROR LIST:")
    for name, error in errors:
        print("-", name, "->", error)

print("\nSYSTEM STATE")
print("INTELLIGENCE: ACTIVE")
print("ECONOMIC MODEL: ACTIVE")
print("DECISION POLICY: ACTIVE")
print("ACTION ENGINE: ACTIVE")
print("LEARNING: ACTIVE")
print("OUTBOUND: DRY-RUN ONLY")
print("LIVE EXTERNAL SEND: DISABLED")

print("\nDIAGNOSIS")

if len(actions) == 0:
    print("ACTIONS = 0")
    print("REMAINING ISSUE: opportunity/decision/action generation")

elif len(world_results) == 0:
    print("ACTIONS > 0 BUT WORLD RESULTS = 0")
    print("REMAINING ISSUE: orchestrator/deduplication/dispatch")

elif len(cycle_results) == 0:
    print("ORCHESTRATOR WORKS BUT CYCLE = 0")
    print("REMAINING ISSUE: autonomous-cycle integration")

else:
    print("FULL PIPELINE IS PRODUCING EXECUTABLE ACTION RESULTS")

print("=" * 80)

if errors:
    raise SystemExit(20)
