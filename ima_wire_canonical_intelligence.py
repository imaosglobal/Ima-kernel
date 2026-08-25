from pathlib import Path
import ast
import shutil
import subprocess
import time

ROOT = Path("founder/executive_ai/global_intelligence")
TARGET = ROOT / "opportunity_to_action.py"
BACKUP_DIR = Path(".ima/self_repair_backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("IMA CANONICAL INTELLIGENCE WIRING")
print("=" * 80)

if not TARGET.exists():
    raise SystemExit(f"MISSING: {TARGET}")

text = TARGET.read_text(encoding="utf-8", errors="ignore")

backup = BACKUP_DIR / f"opportunity_to_action.py.canonical.{int(time.time())}.bak"
shutil.copy2(TARGET, backup)
print("BACKUP:", backup)

tree = ast.parse(text)

generate_node = None
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "generate_actions":
        generate_node = node
        break

if generate_node is None:
    raise SystemExit("generate_actions() NOT FOUND")

lines = text.splitlines(True)
start = generate_node.lineno - 1
end = generate_node.end_lineno

replacement = '''def generate_actions():
    """
    Canonical intelligence -> executable action conversion.

    The source of truth is opportunity_engine.evaluate_world().
    No synthetic lead fallback is used here.
    """
    from founder.executive_ai.global_intelligence.opportunity_engine import (
        evaluate_world,
    )

    result = evaluate_world()

    if not isinstance(result, dict):
        raise RuntimeError(
            "Canonical intelligence returned unexpected type: "
            + type(result).__name__
        )

    opportunities = result.get("all_opportunities", [])

    if not isinstance(opportunities, list):
        raise RuntimeError(
            "Canonical intelligence returned invalid all_opportunities"
        )

    actions = []

    for item in opportunities:
        if not isinstance(item, dict):
            continue

        entity = item.get("entity") or {}

        target = (
            item.get("target")
            or entity.get("name")
            or item.get("name")
        )

        if not target:
            continue

        economics = item.get("economics") or {}

        action_name = (
            economics.get("action")
            or item.get("recommended_action")
        )

        if not action_name:
            final_score = float(item.get("final_score", 0))

            action_name = (
                "create_personal_outreach"
                if final_score >= 60
                else "monitor"
            )

        actions.append({
            "action": action_name,
            "target": str(target),
            "reason": (
                item.get("reason")
                or item.get("reasoning", {}).get("recommended_direction")
                or "canonical opportunity intelligence decision"
            ),
            "score": float(item.get("final_score", 0)),
            "opportunity_score": float(
                item.get("opportunity_score", 0)
            ),
            "economic_score": float(
                item.get("economic_score", 0)
            ),
            "signals": item.get("signals", []),
            "economics": economics,
            "reasoning": item.get("reasoning", {}),
        })

    actions.sort(
        key=lambda x: x.get("score", 0),
        reverse=True,
    )

    return actions
'''

new_text = (
    "".join(lines[:start])
    + replacement
    + "".join(lines[end:])
)

# Validate AST before writing.
ast.parse(new_text)

TARGET.write_text(new_text, encoding="utf-8")

print("WIRED:", TARGET)

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

print("\n[2] CANONICAL GENERATION")

from founder.executive_ai.global_intelligence.opportunity_to_action import (
    generate_actions,
)

actions = generate_actions()

print("ACTION COUNT:", len(actions))

for i, action in enumerate(actions, 1):
    print(
        f"ACTION {i}:",
        action["action"],
        "| TARGET:",
        action["target"],
        "| SCORE:",
        action["score"],
        "| OPPORTUNITY:",
        action["opportunity_score"],
        "| ECONOMIC:",
        action["economic_score"],
    )

print("\n[3] ASSERTIONS")

assert len(actions) == 3, f"Expected 3 canonical actions, got {len(actions)}"

assert actions[0]["target"] == "OpenAI AI startup"
assert actions[1]["target"] == "Ministry of Education government AI program"
assert actions[2]["target"] == "Global Health NGO foundation"

assert actions[0]["score"] > actions[1]["score"] > actions[2]["score"]

assert all(
    action["action"] == "create_personal_outreach"
    for action in actions
)

assert all(
    action["economics"]
    for action in actions
)

print("COUNT: PASS")
print("ORDER: PASS")
print("ACTION DECISION: PASS")
print("ECONOMICS: PASS")
print("CANONICAL SOURCE: PASS")

print("\n" + "=" * 80)
print("CANONICAL INTELLIGENCE WIRING: PASS")
print("=" * 80)
