
# CANONICAL REGISTRY BOOT GUARD
from pathlib import Path
import json, hashlib

REG=Path(".ima/CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json")

if not REG.exists():
    raise SystemExit("CANONICAL REGISTRY MISSING")

registry=json.loads(REG.read_text())

if registry.get("mode") != "canonical_only":
    raise SystemExit("INVALID CANONICAL MODE")

for item in registry.get("allowed_components", []):
    f=Path(item["file"])
    if not f.exists():
        raise SystemExit(f"MISSING CANONICAL COMPONENT: {f}")

    h=hashlib.sha256(f.read_bytes()).hexdigest()

    if h != item["sha256"]:
        raise SystemExit(f"HASH MISMATCH: {f}")

print("[OK] BOOT CANONICAL REGISTRY VERIFIED")

from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def load(name):
    p=ROOT/name
    if p.exists():
        return json.loads(p.read_text())
    return {}

def boot():

    state={
        "time":time.time(),
        "boot":"active",
        "source":"ima_boot_gate",
        "runtime":load("ima_master_state.json"),
        "brain":load("brain_state.json"),
        "decision":load("decision_state.json"),
        "handoff":"kernel_ready"
    }

    (ROOT/"boot_gate_state.json").write_text(
        json.dumps(state,indent=2,ensure_ascii=False)
    )

    return state


if __name__=="__main__":
    print(json.dumps(boot(),indent=2,ensure_ascii=False))
