"""Canonical single IMA loop with universal learning and self-application."""
# first-priority provenance: provenance precedes promotion; cross-domain reconciliation and global user benefit are canonical requirements.
# human agency and intelligibility are mandatory checks in the same canonical loop.
from __future__ import annotations
import json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from core.long_horizon_foresight import HORIZONS, create_trajectory, prioritize_actions, system_foresight

ROOT=Path(__file__).resolve().parents[2]
TZ=ZoneInfo("Asia/Jerusalem")
STATE=ROOT/".ima/loop/UNIFIED_LOOP_STATE.json"
JOURNAL=ROOT/".ima/journal/development.jsonl"

STAGES=("REMEMBER","PRESERVE","OBSERVE","DISCOVER","LISTEN","UNDERSTAND","SEPARATE_FACT_FROM_INFERENCE","QUESTION","CONNECT","CREATE","HUMANIZE","TEST","VERIFY","CORRECT","TEACH","SHARE_LAWFULLY","CARRY_FORWARD")
SYSTEM_SCOPE=(
"human intelligence","human culture","human-centered interactive world-models","intergenerational memory and historical preservation",
"consent-aware private memory","child safety and age assurance","learning and knowledge gaps",
"web intelligence","self-reflection and evolution","energy-internal research","product and public QA",
"lawful public education and distribution","capability radar and engine discovery",
"universal learning across fields","emerging-field discovery","interdisciplinary knowledge graph",
"capability substitution and provider independence","verified capability self-application",
"self-application release testing",
"teaching verified capabilities to people","release/version stewardship","repository health/statistics review",
"real-user growth and retention","privacy-preserving product analytics and feedback",
"global localization and accessibility","app-store readiness and verified reputation",
"lawful growth experiments and partnership discovery","creator-to-commerce and revenue evidence","nonprofit finance, expenses and creator succession governance","long-horizon continuity (daily/monthly/yearly/decadal)","multi-perspective whole-system review (user/customer/executive/operator/technical/community/future)"
)

COMMANDS={
"web_intelligence":["python",".ima/web_intelligence/global_discovery.py","--once"],
"scientific_open_research":["python","scripts/scientific_open_research_health.py"],
"scientific_open_research_tests":["python","-m","unittest","discover","-s","tests","-p","test_scientific_open_research_health.py","-v"],
"evolution":["python",".ima/evolution/EVOLUTION_CONTROLLER.py"],
"daily_summary":["python",".ima/web_intelligence/daily_summary.py"],
"community_frontier":["python","-c","from learning.learning_gap_detector import detect; from learning.conclusion_engine import conclude; from learning.teaching_artifact import create_teaching_artifact; print('IMA_LEARNING_SYSTEM=PASS')"],
"product_qa":["python","qa/daily_qa.py"],
"culture_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_culture.py","-v"],
"distribution":["python",".ima/distribution/prepare.py"],
"human_intelligence_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_intelligence_policy.py","-v"],
"world_model_tests":["python","-m","unittest","discover","-s","tests","-p","test_world_model_humanization.py","-v"],
"world_model_availability":["python","scripts/ima_world_model_availability_check.py"],
"unified_loop_tests":["python","-m","unittest","discover","-s","tests","-p","test_ima_loop.py","-v"],
"universal_learning_tests":["python","-m","unittest","discover","-s","tests","-p","test_universal_learning_engine.py","-v"],
"foresight_tests":["python","-m","unittest","discover","-s","tests","-p","test_long_horizon_foresight.py","-v"],
"creative_bridge_tests":["python","-m","unittest","discover","-s","tests","-p","test_creative_bridge.py","-v"],
"self_application_tests":["python","-m","unittest","discover","-s","tests","-p","test_capability_self_application.py","-v"],
"capability_radar":["python","scripts/ima_capability_radar.py"],
"engine_discovery":["python","learning/engine_discovery.py"],
"capability_contract":["npm","run","test:capabilities"],
"growth_cycle":["python","scripts/ima_growth_cycle.py"],
"monetization_readiness":["python","scripts/ima_monetization_readiness.py"],
"finance_governance_audit":["node","scripts/ima-finance-governance-audit.mjs"],
"provenance_tests":["python","-m","unittest","discover","-s","tests","-p","test_provenance.py","-v"],
"human_agency_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_agency_intelligibility.py","-v"],
"global_integration_intake":["node","scripts/ima-daily-loop-intake.mjs"],
"public_reconciliation":["python","scripts/ima_public_reconciliation.py"],
}

def now_local(): return datetime.now(timezone.utc).astimezone(TZ).replace(microsecond=0)

def due(now):
    tasks=["web_intelligence","scientific_open_research_tests","foresight_tests","culture_tests","human_intelligence_tests","unified_loop_tests","universal_learning_tests","self_application_tests","creative_bridge_tests","human_agency_tests","world_model_tests","world_model_availability","global_integration_intake","public_reconciliation","finance_governance_audit","distribution","capability_contract","growth_cycle","monetization_readiness"]
    if now.hour%6==0: tasks += ["evolution","engine_discovery"]
    if now.hour==2: tasks += ["scientific_open_research"]
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
    foresight_actions=prioritize_actions([create_trajectory(HORIZONS[0], item["outcome"], first_actions=item["first_actions"]) for packets in foresight.values() for item in packets[:1]])
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
      "user_change_rule":"Every explicit request to add or change the loop is reconciled into this canonical loop contract.",
      "provenance_rule":"Every present and future IMA capability is lineage-tracked from imagination/proposal through implementation, testing, deployment and verified-live evidence; provenance, limitations and contributors are preserved.",
      "cross_domain_reconciliation_rule":"All IMA domains, interfaces, memories, research, creative work, integrations, governance and future capabilities must reconcile into one canonical identity, capability lineage and single improvement loop; duplicate parallel systems are not permitted without explicit justification.",
      "multi_perspective_rule":"Review meaningful changes through relevant user, customer, executive, operator, technical, accessibility, privacy, finance, distribution, community and future lenses at micro/product/macro/system-of-systems scales and now-to-intergenerational horizons; evidence gates remain mandatory.",
      "global_integration_rule":"Every newly verified external integration is automatically ingested through the canonical daily intake, deduplicated, evidence-checked and carried into the next improvement cycle; no second daily orchestrator is created.",
      "global_user_benefit_rule":"Verified capabilities are evaluated for safe, lawful, consent-respecting reuse across IMA users without exposing private memory or private identity data.","world_model_rule":"Interactive world models are simulations, not reality. Use them for bounded exploration, education and hypothesis testing; preserve provenance, human control and reversible actions, and require real-world validation for high-impact decisions. Do not claim a live world-model provider integration unless independently verified.",
      "human_agency_rule":"IMA must preserve meaningful human agency: people should be able to understand consequential AI behavior at an appropriate level, question it, challenge it, obtain human review, and know who is accountable.","finance_truth_rule":"Revenue and expenses require evidence; estimates, views, followers, eligibility and projections are never income; no autonomous spending or financial commitment is permitted.",
      "finance_governance_spec":"Use docs/IMA_GLOBAL_NONPROFIT_CHARTER.md, docs/IMA_FINANCIAL_LEDGER_SCHEMA.json, docs/IMA_CREATOR_SUCCESSION_AND_ESTATE.md and data/IMA_FINANCIAL_EVIDENCE_LEDGER.json as canonical specifications. Keep personal creator property, creator compensation, nonprofit operating costs, restricted funds and humanitarian/community benefit separate. No legal nonprofit status is claimed without registration evidence. No fixed surplus percentages are inferred.",
      "nonprofit_creator_separation_rule":"Public-benefit mission assets remain separate from Ori Cohen personal property, creator compensation, royalties and estate rights; legal nonprofit status is never inferred from repository governance.",
      "surplus_allocation_rule":"refunds/chargebacks/required_taxes -> verified_transaction_and_platform_fees -> authorized_operating_expenses -> documented_creator_compensation_or_license_royalty -> required_reserve -> nonprofit_mission_reinvestment -> authorized_humanitarian_or_community_benefit; no fixed percentages without explicit approval.",
      "critical_ai_dependency_rule":"For high-impact systems, IMA continuously checks intelligibility, contestability, human override, traceability, independent verification, reversibility, provider plurality, rights visibility, failure behavior and concentration of power; when verification fails, autonomy must not silently increase."}
    STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return record

if __name__=="__main__": print(json.dumps(run_loop(),ensure_ascii=False,indent=2))
