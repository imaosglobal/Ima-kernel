import traceback

errors = []

print("=" * 80)
print("IMA CANONICAL FULL EXECUTION TEST")
print("=" * 80)

# ------------------------------------------------------------------
# 1. Canonical intelligence -> actions
# ------------------------------------------------------------------

print("\n[1] CANONICAL ACTION GENERATION")

try:
    from founder.executive_ai.global_intelligence.opportunity_to_action import (
        generate_actions,
    )

    actions = generate_actions()

    print("COUNT:", len(actions))

    for i, action in enumerate(actions, 1):
        print(
            f"ACTION {i}:",
            action.get("action"),
            "|",
            action.get("target"),
            "| SCORE:",
            action.get("score"),
        )

    assert len(actions) == 3
    assert all(
        a.get("action") == "create_personal_outreach"
        for a in actions
    )
    assert actions[0]["score"] > actions[1]["score"] > actions[2]["score"]

except Exception as exc:
    errors.append(f"GENERATION: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    actions = []

# ------------------------------------------------------------------
# 2. Orchestrator
# ------------------------------------------------------------------

print("\n[2] ORCHESTRATOR")

try:
    from founder.executive_ai.action_engine.action_orchestrator import (
        run_world_actions,
    )

    world = run_world_actions()

    print("RESULTS:", len(world))

    for i, result in enumerate(world[:10], 1):
        action = result.get("action", {})
        print(
            f"RESULT {i}:",
            action.get("action"),
            "|",
            result.get("target"),
            "| STATUS:",
            result.get("status"),
            "| SCORE:",
            result.get("score"),
        )

    assert len(world) == 3

except Exception as exc:
    errors.append(f"ORCHESTRATOR: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    world = []

# ------------------------------------------------------------------
# 3. Autonomous cycle
# ------------------------------------------------------------------

print("\n[3] AUTONOMOUS CYCLE")

try:
    from founder.executive_ai.action_engine.autonomous_cycle import (
        run_cycle,
    )

    cycle = run_cycle()

    print("STATUS:", cycle.get("status"))

    cycle_actions = cycle.get("actions", [])

    print("RESULTS:", len(cycle_actions))

    for i, result in enumerate(cycle_actions[:10], 1):
        action = result.get("action", {})
        print(
            f"CYCLE {i}:",
            action.get("action"),
            "|",
            result.get("target"),
            "| STATUS:",
            result.get("status"),
            "| SCORE:",
            result.get("score"),
        )

    assert cycle.get("status") == "cycle_completed"
    assert len(cycle_actions) == 3

except Exception as exc:
    errors.append(f"AUTONOMOUS: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    cycle_actions = []

# ------------------------------------------------------------------
# 4. Action memory
# ------------------------------------------------------------------

print("\n[4] ACTION MEMORY")

try:
    from founder.executive_ai.action_engine.action_memory import get_actions

    memory = get_actions()

    print("MEMORY RECORDS:", len(memory))

    targets = {
        "OpenAI AI startup",
        "Ministry of Education government AI program",
        "Global Health NGO foundation",
    }

    relevant = []

    for record in memory:
        value = record.get("value", record)

        if not isinstance(value, dict):
            continue

        action = value.get("action", {})

        if not isinstance(action, dict):
            continue

        if action.get("target") in targets:
            relevant.append(record)

    print("CANONICAL MEMORY RECORDS:", len(relevant))

    assert len(relevant) >= 3

except Exception as exc:
    errors.append(f"MEMORY: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    memory = []

# ------------------------------------------------------------------
# 5. Canonical outbound executor
# ------------------------------------------------------------------

print("\n[5] OUTBOUND SAFETY")

try:
    from founder.executive_ai.action_engine.action_executor import (
        execute_outreach,
    )

    outbound = execute_outreach({
        "action": "create_personal_outreach",
        "target": "IMA CANONICAL TEST",
    })

    print("OUTBOUND:", outbound)

    assert isinstance(outbound, dict)
    assert outbound.get("mode") == "dry_run"
    assert outbound.get("external_action") is False
    assert outbound.get("status") == "prepared"

    print("CANONICAL EXECUTOR: PASS")
    print("DRY-RUN SAFETY: PASS")

except Exception as exc:
    errors.append(f"OUTBOUND: {type(exc).__name__}: {exc}")
    traceback.print_exc()

# ------------------------------------------------------------------
# Final validation
# ------------------------------------------------------------------

print("\n" + "=" * 80)
print("FINAL CANONICAL PIPELINE VALIDATION")
print("=" * 80)

print("GENERATED ACTIONS:", len(actions))
print("ORCHESTRATOR RESULTS:", len(world))
print("AUTONOMOUS RESULTS:", len(cycle_actions))
print("ERRORS:", len(errors))

for error in errors:
    print("ERROR:", error)

if (
    len(actions) == 3
    and len(world) == 3
    and len(cycle_actions) == 3
    and not errors
):
    print("\nPIPELINE: PASS")
    print(
        "Canonical Intelligence -> Action -> "
        "Orchestrator -> Autonomous: VERIFIED"
    )
else:
    print("\nPIPELINE: FAIL")

print("EXTERNAL SEND: DISABLED")
print("OUTBOUND MODE: DRY-RUN")
print("=" * 80)

if errors:
    raise SystemExit(1)
