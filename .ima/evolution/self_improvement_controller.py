#!/usr/bin/env python3
"""Bounded autonomous self-improvement controller for the single canonical IMA loop.

It does not create a second scheduler or runtime. It consumes canonical diagnostics,
asks an authorized intelligence for a proposed patch, validates the patch, runs tests,
and keeps or reverts the change. No provider credentials are stored in the repository.
"""
from __future__ import annotations
import json, os, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STATE=ROOT/".ima/evolution/SELF_APPLICATION_STATE.json"
GATEWAY=ROOT/".ima/intelligence/universal_intelligence_gateway.py"
ALLOWED=("ima-ui/","scripts/","tests/","learning/","connectors/","docs/")
DENIED=(".github/","supabase/","render.yaml",".env",".ima/intelligence/PROVIDER_REGISTRY.json")

def run(cmd,check=False):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=900)
    if check and p.returncode: raise RuntimeError(p.stderr[-3000:] or p.stdout[-3000:])
    return p

def gateway(prompt):
    import importlib.util
    spec=importlib.util.spec_from_file_location("ima_gateway",GATEWAY)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.route(prompt,private=False,preferred=os.getenv("IMA_SELF_IMPROVEMENT_PROVIDER") or None)

def allowed_diff(diff:str):
    if not diff.strip(): return False,"empty diff"
    for line in diff.splitlines():
        if line.startswith("+++ b/") or line.startswith("--- a/"):
            path=line[6:] if line.startswith("+++ b/") else line[6:]
            if any(path==d or path.startswith(d) for d in DENIED): return False,"denied path: "+path
            if not any(path.startswith(a) for a in ALLOWED): return False,"path outside allowlist: "+path
    return True,"ok"

def main():
    prompt="""You are IMA's bounded self-improvement engineer inside its canonical loop.
Use the repository's actual diagnostics and public product direction. Propose ONE smallest
high-value improvement that makes IMA more usable, reliable, accessible, truthful or
self-maintaining. Do not add a parallel system. Do not expose internal architecture in
the public UI. Do not change credentials, secrets, payments, auth policy, deployment
workflows, provider registry, or safety policy. Return ONLY a unified git diff.
Allowed source areas: ima-ui/, scripts/, tests/, learning/, connectors/, docs/.
The public product should remain: user arrives, sees IMA, talks to IMA; internals stay hidden.
Diagnostics:"""
    result=gateway(prompt)
    if result.get("status")!="OK":
        state={"status":"BLOCKED","reason":"NO_AUTHORIZED_PROVIDER","gateway":result.get("reason")}
        STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(state,indent=2)+"\n")
        print(json.dumps(state)); return 0
    diff=result.get("response","")
    ok,reason=allowed_diff(diff)
    if not ok:
        state={"status":"REJECTED","reason":reason}; STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(state,indent=2)+"\n"); print(json.dumps(state)); return 0
    with tempfile.NamedTemporaryFile("w",delete=False,suffix=".patch") as f:
        f.write(diff); patch=f.name
    try:
        check=run(["git","apply","--check",patch])
        if check.returncode:
            state={"status":"REJECTED","reason":"git apply --check failed","evidence":check.stderr[-3000:]}
            return write(state)
        before=run(["git","status","--porcelain"]).stdout
        applied=run(["git","apply",patch])
        if applied.returncode:
            return write({"status":"REJECTED","reason":"git apply failed","evidence":applied.stderr[-3000:]})
        test=run(["python","-m","unittest","discover","-s","tests","-t",".","-p","test_*.py"])
        if test.returncode:
            run(["git","reset","--hard","HEAD"])
            return write({"status":"REVERTED","reason":"canonical tests failed","evidence":test.stdout[-2500:]+test.stderr[-2500:]})
        write({"status":"APPLIED_AND_TESTED","provider":result.get("provider"),"changed":run(["git","diff","--name-only"]).stdout.splitlines(),"previous_worktree":before})
        return 0
    finally:
        try: Path(patch).unlink()
        except OSError: pass

def write(state):
    STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(state,ensure_ascii=False)); return 0

if __name__=="__main__": raise SystemExit(main())
