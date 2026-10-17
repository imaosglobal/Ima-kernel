"""Canonical single IMA loop.

All periodic IMA maintenance, learning, reflection, culture, preservation,
world-intelligence and lawful distribution preparation enters through this
one scheduler. Event-driven CI may remain separate for immediate verification,
but no second periodic IMA loop is allowed.

A user request that asks to add something to "the loop" is interpreted as a
change to this contract and to the canonical daily reconciliation record.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
TZ = ZoneInfo("Asia/Jerusalem")
STATE = ROOT / ".ima" / "loop" / "UNIFIED_LOOP_STATE.json"
JOURNAL = ROOT / ".ima" / "journal" / "development.jsonl"

STAGES = (
    "REMEMBER",
    "PRESERVE",
    "OBSERVE",
    "DISCOVER",
    "LISTEN",
    "UNDERSTAND",
    "SEPARATE_FACT_FROM_INFERENCE",
    "QUESTION",
    "CONNECT",
    "CREATE",
    "HUMANIZE",
    "TEST",
    "VERIFY",
    "CORRECT",
    "TEACH",
    "SHARE_LAWFULLY",
    "CARRY_FORWARD",
)

SYSTEM_SCOPE = (
    "human intelligence",
    "human culture",
    "intergenerational memory and historical preservation",
    "consent-aware private memory",
    "child safety and age assurance",
    "learning and knowledge gaps",
    "web intelligence",
    "self-reflection and evolution",
    "energy-internal research",
    "product and public QA",
    "lawful public education and distribution",
    "capability radar and engine discovery",
    "release/version stewardship",
    "repository health/statistics review",
)

COMMANDS = {
    "web_intelligence": ["python", ".ima/web_intelligence/global_discovery.py", "--once"],
    "evolution": ["python", ".ima/evolution/EVOLUTION_CONTROLLER.py"],
    "daily_summary": ["python", ".ima/web_intelligence/daily_summary.py"],
    "community_frontier": [
        "python", "-c",
        "from learning.learning_gap_detector import detect; from learning.conclusion_engine import conclude; from learning.teaching_artifact import create_teaching_artifact; print('IMA_LEARNING_SYSTEM=PASS')",
    ],
    "product_qa": ["python", "qa/daily_qa.py"],
    "culture_tests": ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_human_culture.py", "-v"],
    "distribution": ["python", ".ima/distribution/prepare.py"],
    "human_intelligence_tests": ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_human_intelligence_policy.py", "-v"],
    "unified_loop_tests": ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_ima_loop.py", "-v"],
    "capability_radar": ["python", "scripts/ima_capability_radar.py"],
    "engine_discovery": ["python", "learning/engine_discovery.py"],
    "capability_contract": ["npm", "run", "test:capabilities"],
}

def now_local() -> datetime:
    return datetime.now(timezone.utc).astimezone(TZ).replace(microsecond=0)

def due(now: datetime) -> list[str]:
    # One hourly tick is the canonical scheduler. Tasks retain their useful
    # frequencies without creating independent schedules.
    tasks = ["web_intelligence", "culture_tests", "human_intelligence_tests", "unified_loop_tests", "distribution", "capability_contract"]
    if now.hour % 6 == 0:
        tasks.extend(["evolution", "engine_discovery"])
    if now.hour == 3:
        tasks.extend(["community_frontier", "product_qa"])
    if now.hour == 4:
        tasks.append("capability_radar")
    if now.hour == 21:
        tasks.append("daily_summary")
    return tasks

def run_task(name: str) -> dict:
    command = COMMANDS[name]
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=900)
        return {
            "task": name,
            "command": command,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-1500:],
            "stderr_tail": proc.stderr[-1500:],
        }
    except Exception as exc:
        return {"task": name, "command": command, "status": "ERROR", "error": repr(exc)}

def run_loop() -> dict:
    now = now_local()
    tasks = due(now)
    results = [run_task(task) for task in tasks]
    record = {
        "schema": "IMA-UNIFIED-LOOP-1.1",
        "timestamp": now.isoformat(),
        "timezone": "Asia/Jerusalem",
        "stages": list(STAGES),
        "scope": list(SYSTEM_SCOPE),
        "tasks": results,
        "single_scheduler": True,
        "user_change_rule": "Every user request to add or change the loop is reconciled into this canonical loop contract.",
        "truth_rule": "Documentation, intention, and generated state are not runtime proof; verification must be recorded separately.",
        "lawful_distribution_rule": "Public sharing is limited to lawful, consent-respecting, non-spam channels and authorized accounts.",
    }
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record

if __name__ == "__main__":
    print(json.dumps(run_loop(), ensure_ascii=False, indent=2))
