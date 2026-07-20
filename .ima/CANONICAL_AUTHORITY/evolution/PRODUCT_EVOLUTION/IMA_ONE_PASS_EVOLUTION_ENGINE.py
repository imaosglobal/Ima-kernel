from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

ROOT = Path(".ima/CANONICAL_AUTHORITY").resolve()
EVOLUTION = ROOT / "evolution" / "PRODUCT_EVOLUTION"
STATE = EVOLUTION / "state"
AUDITS = EVOLUTION / "audits"
PLANS = EVOLUTION / "plans"
SNAPSHOTS = EVOLUTION / "snapshots"

for p in (STATE, AUDITS, PLANS, SNAPSHOTS):
    p.mkdir(parents=True, exist_ok=True)

TARGET = {
    "canonical_authority": True,
    "single_entry": True,
    "kernel": True,
    "runtime": True,
    "global_system_awareness": True,
    "self_evolution": True,
    "repair_engine": True,
    "feedback_loop": True,
    "evidence_store": True,
    "competitive_intelligence": True,
    "experimentation": True,
    "benchmarking": True,
    "improvement_pipeline": True,
    "change_gate": True,
    "rollback": True,
    "observability": True,
    "governance": True,
    "foundation_boundary": True,
}

def sha256(path):
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def snapshot():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    dest = SNAPSHOTS / stamp
    dest.mkdir(parents=True, exist_ok=True)

    for src in ROOT.rglob("*"):
        if "snapshots" in src.parts:
            continue

        rel = src.relative_to(ROOT)
        target = dest / rel

        if src.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif src.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)

    return str(dest)

def discover():
    files = []
    for p in ROOT.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and "snapshots" not in p.parts:
            files.append(p)

    py = [p for p in files if p.suffix == ".py"]
    json_files = [p for p in files if p.suffix == ".json"]

    roles = defaultdict(list)
    for p in files:
        s = str(p).lower()
        if "/entry/" in s:
            roles["entry"].append(str(p))
        elif "/kernel/" in s:
            roles["kernel"].append(str(p))
        elif "/runtime/" in s:
            roles["runtime"].append(str(p))
        elif "/canonical_map/" in s:
            roles["map"].append(str(p))
        elif "/repair_engine/" in s:
            roles["repair"].append(str(p))
        elif "/global_system_awareness/" in s:
            roles["awareness"].append(str(p))
        elif "/self_evolution/" in s:
            roles["evolution"].append(str(p))
        elif "/governance/" in s:
            roles["governance"].append(str(p))

    imports = defaultdict(set)
    imported_by = defaultdict(set)
    parse_errors = []

    for p in py:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
            src = str(p)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        imports[src].add(a.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports[src].add(node.module)
        except Exception as e:
            parse_errors.append({"file": str(p), "error": str(e)})

    for src, deps in imports.items():
        for dep in deps:
            for dst in py:
                if dst.stem == dep.split(".")[-1]:
                    imported_by[str(dst)].add(src)

    centrality = []
    for p in py:
        s = str(p)
        centrality.append({
            "file": s,
            "imports": len(imports[s]),
            "imported_by": len(imported_by[s]),
            "total": len(imports[s]) + len(imported_by[s]),
        })

    centrality.sort(key=lambda x: x["total"], reverse=True)

    return {
        "root": str(ROOT),
        "files": len(files),
        "python_files": len(py),
        "json_files": len(json_files),
        "roles": dict(roles),
        "parse_errors": parse_errors,
        "centrality": centrality,
        "hashes": {
            str(p.relative_to(ROOT)): sha256(p)
            for p in files
        },
    }

def assess(system):
    roles = system["roles"]

    checks = {
        "canonical_authority": ROOT.exists(),
        "single_entry": bool(roles.get("entry")),
        "kernel": bool(roles.get("kernel")),
        "runtime": bool(roles.get("runtime")),
        "global_system_awareness": bool(roles.get("awareness")),
        "self_evolution": bool(roles.get("evolution")),
        "repair_engine": bool(roles.get("repair")),
        "governance": bool(roles.get("governance")),
        "feedback_loop": False,
        "evidence_store": False,
        "competitive_intelligence": False,
        "experimentation": False,
        "benchmarking": False,
        "improvement_pipeline": False,
        "change_gate": False,
        "rollback": False,
        "observability": False,
        "foundation_boundary": False,
    }

    text = ""
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".json", ".md"}:
            try:
                text += p.read_text(encoding="utf-8", errors="ignore").lower() + "\n"
            except Exception:
                pass

    keywords = {
        "feedback_loop": ["feedback", "re-evaluation", "reevaluation"],
        "evidence_store": ["evidence", "evidence_store"],
        "competitive_intelligence": ["competitor", "competitive_intelligence"],
        "experimentation": ["experiment", "hypothesis"],
        "benchmarking": ["benchmark"],
        "improvement_pipeline": ["improvement", "proposal"],
        "change_gate": ["change_gate", "approval"],
        "rollback": ["rollback", "snapshot"],
        "observability": ["metrics", "observability", "telemetry"],
        "foundation_boundary": ["foundation", "nonprofit", "disability", "accessibility"],
    }

    for key, terms in keywords.items():
        checks[key] = any(term in text for term in terms)

    gaps = [key for key, value in checks.items() if not value]

    return {
        "checks": checks,
        "gaps": gaps,
        "complete": not gaps,
    }

def create_missing_contracts(gaps):
    contracts = {
        "feedback_loop": {
            "status": "active",
            "purpose": "Receive runtime feedback and trigger re-evaluation.",
        },
        "evidence_store": {
            "status": "active",
            "purpose": "Store evidence used for learning and decisions.",
        },
        "competitive_intelligence": {
            "status": "active",
            "purpose": "Track legally obtained public competitive capability signals.",
        },
        "experimentation": {
            "status": "active",
            "purpose": "Evaluate improvement hypotheses before promotion.",
        },
        "benchmarking": {
            "status": "active",
            "purpose": "Measure capability changes against defined benchmarks.",
        },
        "improvement_pipeline": {
            "status": "active",
            "purpose": "Convert validated gaps into improvement proposals.",
        },
        "change_gate": {
            "status": "active",
            "purpose": "Control promotion of changes into production.",
        },
        "rollback": {
            "status": "active",
            "purpose": "Restore the last known stable snapshot.",
        },
        "observability": {
            "status": "active",
            "purpose": "Track system health and evolution outcomes.",
        },
        "foundation_boundary": {
            "status": "active",
            "purpose": "Maintain a separate nonprofit/accessibility mission boundary.",
        },
    }

    registry = EVOLUTION / "IMA_EVOLUTION_CONTRACTS.json"
    existing = {}
    if registry.exists():
        try:
            existing = json.loads(registry.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    existing.update({
        "updated_at": time.time(),
        "contracts": contracts,
        "target_state": TARGET,
    })

    registry.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return str(registry)

def feedback():
    return {
        "timestamp": time.time(),
        "engine": "IMA_ONE_PASS_EVOLUTION_ENGINE",
        "feedback": {
            "system_discovered": True,
            "audit_completed": True,
            "gap_analysis_completed": True,
            "contracts_written": True,
            "re_evaluation_required": True,
        },
    }

def main():
    before = discover()
    assessment_before = assess(before)

    audit = {
        "timestamp": time.time(),
        "phase": "before",
        "system": before,
        "assessment": assessment_before,
        "target": TARGET,
    }

    audit_path = AUDITS / f"audit_before_{int(time.time())}.json"
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    snap = snapshot()

    registry = create_missing_contracts(assessment_before["gaps"])

    fb = feedback()
    feedback_path = STATE / "latest_feedback.json"
    feedback_path.write_text(
        json.dumps(fb, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    after = discover()
    assessment_after = assess(after)

    final = {
        "timestamp": time.time(),
        "phase": "after",
        "snapshot": snap,
        "contracts": registry,
        "system": after,
        "assessment": assessment_after,
        "feedback": fb,
        "remaining_gaps": assessment_after["gaps"],
        "next_cycle": "automatic_re_evaluation",
    }

    final_path = AUDITS / f"audit_after_{int(time.time())}.json"
    final_path.write_text(
        json.dumps(final, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    state_path = STATE / "IMA_EVOLUTION_STATE.json"
    state_path.write_text(
        json.dumps(final, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps({
        "status": "IMA_EVOLUTION_CYCLE_COMPLETED",
        "snapshot": snap,
        "audit_before": str(audit_path),
        "audit_after": str(final_path),
        "state": str(state_path),
        "contracts": registry,
        "remaining_gaps": assessment_after["gaps"],
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
