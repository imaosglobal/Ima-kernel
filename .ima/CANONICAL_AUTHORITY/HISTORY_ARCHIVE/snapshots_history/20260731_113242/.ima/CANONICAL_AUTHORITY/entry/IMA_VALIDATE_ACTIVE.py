import importlib.util, json, hashlib, subprocess, sys
from pathlib import Path

ROOT = Path.cwd()
REG = ROOT / ".ima/CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json"
CAP = ROOT / ".ima/agi_evolution/CAPABILITY_REGISTRY.json"

def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)

r = json.loads(REG.read_text())

for x in r["allowed_components"]:
    p = ROOT / x["file"]
    if not p.exists():
        fail(f"MISSING {p}")
    if hashlib.sha256(p.read_bytes()).hexdigest() != x["sha256"]:
        fail(f"HASH {p}")

c = json.loads(CAP.read_text())

def load(name):
    p = ROOT / c["capabilities"][name]["source"]
    s = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

runtime = load("runtime")
decision = load("decision")

runtime.detect("status check")
runtime.choose("system_stability", "status check")
decision.decide()

print("VALIDATION_OK")
