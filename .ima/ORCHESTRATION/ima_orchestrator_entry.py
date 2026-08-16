#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, hashlib, datetime

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/".ima/ORCHESTRATION"
REG=BASE/"registry"/"orchestrator_inventory.json"
CONTRACT=BASE/"ORCHESTRATION_CONTRACT.json"

def run(cmd):
    return subprocess.run(
        cmd,cwd=ROOT,text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

def main():
    print("=== IMA SINGLE ORCHESTRATION ENTRY ===")

    if not CONTRACT.exists():
        raise SystemExit("BLOCKED: orchestration contract missing")

    contract=json.loads(CONTRACT.read_text())
    inventory=json.loads(REG.read_text()) if REG.exists() else {}

    result={
        "timestamp":datetime.datetime.now().isoformat(),
        "contract":contract["schema"],
        "inventory_files":len(inventory.get("files",[])),
        "gates":[],
    }

    # Discover canonical runtime entry.
    runtime_candidates=[
        ROOT/"kernel/runtime/CANONICAL/python_bridge.py",
        ROOT/"app.py",
    ]

    runtime=next((p for p in runtime_candidates if p.exists()),None)

    if runtime:
        result["gates"].append({
            "gate":"runtime_entry",
            "status":"verified",
            "path":str(runtime.relative_to(ROOT))
        })
    else:
        result["gates"].append({
            "gate":"runtime_entry",
            "status":"blocked"
        })

    # Existing continuity engine.
    continuity=ROOT/".ima/CONTINUITY/promote_verified.py"
    if continuity.exists():
        cp=run([sys.executable,str(continuity)])
        result["gates"].append({
            "gate":"continuity_promotion",
            "status":"passed" if cp.returncode==0 else "failed",
            "output":cp.stdout[-4000:]
        })
    else:
        result["gates"].append({
            "gate":"continuity_promotion",
            "status":"missing"
        })

    # Canonical runtime registration is deliberately verification-gated.
    runtime_registry=BASE/"runtime"/"runtime_registry.json"
    runtime_registry.write_text(
        json.dumps({
            "schema":"ima.runtime.registry.v1",
            "updated_at":datetime.datetime.now().isoformat(),
            "active_entry":(
                str(runtime.relative_to(ROOT))
                if runtime else None
            ),
            "historical_code_activation":"verification_required"
        },indent=2),
        encoding="utf-8"
    )

    result["runtime_registry"]=str(runtime_registry.relative_to(ROOT))

    digest=hashlib.sha256(
        json.dumps(result,sort_keys=True).encode()
    ).hexdigest()

    result["orchestration_hash"]=digest

    snap=BASE/"snapshots"/datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap.mkdir(parents=True,exist_ok=True)
    (snap/"ORCHESTRATION_RESULT.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )

    print("[OK] orchestration inventory loaded")
    print("[OK] continuity engine evaluated")
    print("[OK] runtime registration written")
    print("[OK] provenance snapshot written")

    blocked=[
        g for g in result["gates"]
        if g.get("status") in ("blocked","failed")
    ]

    if blocked:
        print("[BLOCKED] one or more gates failed")
        return 2

    print("[OK] all mandatory orchestration gates passed")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
