#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
AUTO = ROOT / ".ima" / "automation"

def now():
    return datetime.now(timezone.utc).isoformat()

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd):
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True
    )

def log(event, data=None):
    record = {
        "time": now(),
        "event": event,
        "data": data or {}
    }
    path = AUTO / "logs" / "continuous_improvement.jsonl"
    with path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def quality_gate():
    checks = []

    status = run(["git", "status", "--porcelain"]).stdout.splitlines()

    allowed_runtime_prefixes = (
        " M .ima/runtime/",
        "?? .ima/automation/backups/",
        "?? .ima/automation/logs/",
        "?? .ima/automation/metrics/",
        "?? .ima/metrics/",
    )

    unexpected_changes = [
        line for line in status
        if not line.startswith(allowed_runtime_prefixes)
    ]

    checks.append((
        "no_unexpected_changes",
        len(unexpected_changes) == 0
    ))

    py = run([
        "python3",
        "-m",
        "py_compile",
        "ima_master_runtime.py"
    ])

    checks.append(("python_syntax", py.returncode == 0))

    boot = run(["python3", "IMA_START.py"])

    checks.append((
        "boot",
        "IMA SYSTEM READY" in boot.stdout
    ))

    result = {
        "time": now(),
        "checks": dict(checks),
        "unexpected_changes": unexpected_changes,
        "passed": all(ok for _, ok in checks)
    }

    path = AUTO / "metrics" / "quality_latest.json"
    path.write_text(json.dumps(result, indent=2))

    log("QUALITY_GATE", result)
    return result


def snapshot():
    files = [
        ROOT / "ima_master_runtime.py",
        ROOT / "IMA_START.py",
    ]

    data = {
        "time": now(),
        "files": {
            str(p.relative_to(ROOT)): sha256(p)
            for p in files
            if p.exists()
        }
    }

    path = AUTO / "backups" / f"snapshot-{int(time.time())}.json"
    path.write_text(json.dumps(data, indent=2))
    return data

def observe():
    feedback = list((AUTO / "feedback").glob("*.json"))
    proposals = list((AUTO / "proposals").glob("*.json"))

    result = {
        "time": now(),
        "feedback_items": len(feedback),
        "proposal_items": len(proposals),
        "status": "OBSERVING"
    }

    log("OBSERVATION", result)
    return result


# IMA_POLICY_GATE_V1
POLICY_FILE = ROOT / ".ima" / "policy" / "universal_human_flourishing_policy.json"
INTEGRATION_CONTRACT_FILE = ROOT / ".ima" / "policy" / "integration_contract.json"

def load_policy():
    try:
        return json.loads(POLICY_FILE.read_text())
    except Exception as exc:
        log("POLICY_LOAD_FAILED", {"error": str(exc)})
        return None

def policy_gate():
    policy = load_policy()

    if not policy:
        result = {
            "passed": False,
            "reason": "policy_unavailable"
        }
        log("POLICY_GATE", result)
        return result

    required = [
        "primary_objective",
        "evaluation_order",
        "mandatory_human_review",
        "success_metrics"
    ]

    missing = [key for key in required if key not in policy]

    result = {
        "passed": len(missing) == 0,
        "missing": missing,
        "policy": str(POLICY_FILE.relative_to(ROOT)),
        "objective": policy.get("primary_objective"),
        "evaluation_order": policy.get("evaluation_order", []),
        "success_metrics": policy.get("success_metrics", [])
    }

    log("POLICY_GATE", result)

    (ROOT / ".ima" / "metrics" / "policy_gate_latest.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False)
    )

    return result



def auto_commit():
    run(["git", "add", "."])

    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()

    ignored_prefixes = (
        ".ima/runtime/",
        ".ima/automation/backups/",
        ".ima/automation/logs/",
        ".ima/automation/metrics/",
        ".ima/metrics/",
    )

    canonical = [
        path for path in staged
        if not path.startswith(ignored_prefixes)
    ]

    if not canonical:
        run(["git", "reset"])
        return {
            "committed": False,
            "reason": "no_canonical_changes",
            "files": []
        }

    check = run(["git", "diff", "--cached", "--check"])
    if check.returncode != 0:
        run(["git", "reset"])
        return {
            "committed": False,
            "reason": "staged_diff_check_failed",
            "files": canonical
        }

    message = "IMA automatic synchronization: " + ", ".join(canonical[:5])
    if len(canonical) > 5:
        message += f" (+{len(canonical) - 5} more)"

    commit = run(["git", "commit", "-m", message])

    return {
        "committed": commit.returncode == 0,
        "reason": "commit_created" if commit.returncode == 0 else "commit_failed",
        "files": canonical
    }

def main():
    log("CYCLE_START")

    snapshot()
    policy = policy_gate()
    quality = quality_gate()
    observation = observe()

    result = {
        "time": now(),
        "policy": policy,
        "quality": quality,
        "observation": observation,
        "next_step": (
            "WAIT_FOR_REVIEW"
            if quality["passed"]
            else "STOP_AND_REPAIR"
        )
    }

    if policy["passed"] and quality["passed"]:
        result["auto_commit"] = auto_commit()

    (AUTO / "metrics" / "cycle_latest.json").write_text(
        json.dumps(result, indent=2)
    )

    log("CYCLE_COMPLETE", result)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()


# IMA_POLICY_GATE_V1
POLICY_FILE = ROOT / ".ima" / "policy" / "universal_human_flourishing_policy.json"
INTEGRATION_CONTRACT_FILE = ROOT / ".ima" / "policy" / "integration_contract.json"

def load_policy():
    try:
        return json.loads(POLICY_FILE.read_text())
    except Exception as exc:
        log("POLICY_LOAD_FAILED", {"error": str(exc)})
        return None
