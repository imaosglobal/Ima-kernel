"""Canonical single IMA loop with universal learning and self-application."""
from __future__ import annotations
import json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from core.long_horizon_foresight import system_foresight, prioritize_actions

ROOT=Path(__file__).resolve().parents[2]
TZ=ZoneInfo("Asia/Jerusalem")
STATE=ROOT/".ima/loop/UNIFIED_LOOP_STATE.json"
JOURNAL=ROOT/".ima/journal/development.jsonl"

STAGES=("REMEMBER","PRESERVE","OBSERVE","DISCOVER","LISTEN","UNDERSTAND","SEPARATE_FACT_FROM_INFERENCE","QUESTION","CONNECT","CREATE","HUMANIZE","TEST","VERIFY","CORRECT","TEACH","SHARE_LAWFULLY","CARRY_FORWARD")
SYSTEM_SCOPE=(
"human intelligence","human culture","intergenerational memory and historical preservation",
"consent-aware private memory","child safety and age assurance","learning and knowledge gaps",
"web intelligence","self-reflection and evolution","energy-internal research","product and public QA",
"lawful public education and distribution","capability radar and engine discovery",
"universal learning across fields","emerging-field discovery","interdisciplinary knowledge graph",
"capability substitution and provider independence","verified capability self-application",
"self-application release testing",
"teaching verified capabilities to people","release/version stewardship","repository health/statistics review",
"real-user growth and retention","privacy-preserving product analytics and feedback",
"global localization and accessibility","app-store readiness and verified reputation",
"lawful growth experiments and partnership discovery","long-horizon continuity (daily/monthly/yearly/decadal)"
)

COMMANDS={
"web_intelligence":["python",".ima/web_intelligence/global_discovery.py","--once"],
"evolution":["python",".ima/evolution/EVOLUTION_CONTROLLER.py"],
"daily_summary":["python",".ima/web_intelligence/daily_summary.py"],
"community_frontier":["python","-c","from learning.learning_gap_detector import detect; from learning.conclusion_engine import conclude; from learning.teaching_artifact import create_teaching_artifact; print('IMA_LEARNING_SYSTEM=PASS')"],
"product_qa":["python","qa/daily_qa.py"],
"culture_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_culture.py","-v"],
"distribution":["python",".ima/distribution/prepare.py"],
"human_intelligence_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_intelligence_policy.py","-v"],
"unified_loop_tests":["python","-m","unittest","discover","-s","tests","-p","test_ima_loop.py","-v"],
"universal_learning_tests":["python","-m","unittest","discover","-s","tests","-p","test_universal_learning_engine.py","-v"],
"foresight_tests":["python","-m","unittest","discover","-s","tests","-p","test_long_horizon_foresight.py","-v"],
"creative_bridge_tests":["python","-m","unittest","discover","-s","tests","-p","test_creative_bridge.py","-v"],
"self_application_tests":["python","-m","unittest","discover","-s","tests","-p","test_capability_self_application.py","-v"],
"capability_radar":["python","scripts/ima_capability_radar.py"],
"engine_discovery":["python","learning/engine_discovery.py"],
"capability_contract":["npm","run","test:capabilities"],
"growth_cycle":["python","scripts/ima_growth_cycle.py"],
}

def now_local(): return datetime.now(timezone.utc).astimezone(TZ).replace(microsecond=0)

def due(now):
    tasks=["web_intelligence","foresight_tests","culture_tests","human_intelligence_tests","unified_loop_tests","universal_learning_tests","self_application_tests","creative_bridge_tests","distribution","capability_contract","growth_cycle"]
    if now.hour%6==0: tasks += ["evolution","engine_discovery"]
    if now.hour==3: tasks += ["community_frontier","product_qa"]
    if now.hour==4: tasks += ["capability_radar"]
    if now.hour==21: tasks += ["daily_summary"]
    return tasks

def run_task(name):
    command=COMMANDS[name]
    try:
        p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=900)
        return {"task":name,"command":command,"status":"PASS" if p.returncode==0 else "FAIL","returncode":p.returncode,"stdout_tail":p.stdout[-1500:],"stderr_tail":p.stderr[-1500:]}
    except Exception as exc: return {"task":name,"command":command,"status":"ERROR","error":repr(exc)}

def run_loop():
    now=now_local(); tasks=due(now); results=[run_task(t) for t in tasks]
    foresight=system_foresight(SYSTEM_SCOPE)
    foresight_actions=prioritize_actions([__import__('core.long_horizon_foresight', fromlist=['FutureCapability']).create_trajectory(__import__('core.long_horizon_foresight', fromlist=['HORIZONS']).HORIZONS[0], item['outcome'], first_actions=item['first_actions']) for packets in foresight.values() for item in packets[:1]])
    findings=[]
    for result in results:
        status=result.get("status")
        task=result.get("task","unknown")
        action="carry_forward" if status=="PASS" else ("inspect_logs_before_change" if status=="FAIL" else "inspect_runtime_evidence")
        findings.append({"task":task,"finding":status or "UNKNOWN","action":action})
    record={"schema":"IMA-UNIFIED-LOOP-1.3","timestamp":now.isoformat(),"timezone":"Asia/Jerusalem","stages":list(STAGES),"scope":list(SYSTEM_SCOPE),"tasks":results,
      "foresight":{"components":foresight,"priority_now_actions":foresight_actions},
      "diagnostics":{"summary":{"total":len(results),"passed":sum(r.get("status")=="PASS" for r in results),"failed":sum(r.get("status")=="FAIL" for r in results),"errors":sum(r.get("status") in {"ERROR","UNKNOWN",None} for r in results)},"findings":findings,"truth_rule":"Diagnostics describe this run; they do not prove live deployment without runtime evidence."},
      "single_scheduler":True,
      "universal_learning_rule":"Every newly accessible field or capability is discovered, evidenced, tested, verified, taught and evaluated for bounded self-application through this loop.",
      "creative_bridge_rule":"When a meaningful gap is detected between domains, IMA may form a bridge hypothesis; it must be tested and evidenced before being treated as verified.",
      "foresight_rule":"For every meaningful IMA component, continuously model plausible future states across near, one-year, multi-year and long horizons; treat them as hypotheses, identify signals and prerequisites, and take only safe present actions that prepare for them.",
      "self_application_rule":"A verified capability may improve IMA itself only through the same inspect -> change -> test -> verify -> carry-forward gates.",
      "provider_independence_rule":"Separate capability from provider; record alternatives, cost, license, privacy and unresolved gaps.",
      "truth_rule":"Documentation, intention, advertised availability and generated state are not runtime proof; verification must be recorded separately.",
      "lawful_distribution_rule":"Public sharing is limited to lawful, consent-respecting, non-spam channels and authorized accounts.",
      "user_change_rule":"Every explicit request to add or change the loop is reconciled into this canonical loop contract."}
    STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return record

if __name__=="__main__": print(json.dumps(run_loop(),ensure_ascii=False,indent=2))
