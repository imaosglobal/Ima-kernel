
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
"lawful public education and distribution","self-marketing, sales, brand and growth","capability radar and engine discovery",
"universal learning across fields","emerging-field discovery","interdisciplinary knowledge graph",
"capability substitution and provider independence","verified capability self-application",
"self-application release testing",
"teaching verified capabilities to people","release/version stewardship","repository health/statistics review",
"real-user growth and retention","privacy-preserving product analytics and feedback","global micro-signal observation and relevance pruning","cross-surface feedback reconciliation","self-adaptive visual and interaction quality","global ecosystem and competitor intelligence",
"global funding, grants, sponsorships, credits, partnerships and lawful revenue discovery",
"global localization and accessibility","app-store readiness and verified reputation",
"lawful growth experiments and partnership discovery","creator-to-commerce and revenue evidence","nonprofit finance, expenses and creator succession governance","long-horizon continuity (daily/monthly/yearly/decadal)","multi-perspective whole-system review (user/customer/executive/operator/technical/community/future)",
"forward care and one-year preparedness","peer and competitor cooperation intelligence","universal task support and safe task routing","conflict de-escalation and safety-aware care","global source scanning within authorization","global change and humanitarian world pulse","historical conflict/outcome mapping","temporal relevance and stale-capability pruning","continuous self-repair and simplification"
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
"funding_revenue_intelligence":["python","scripts/ima_world_pulse.py"],
"finance_governance_audit":["node","scripts/ima-finance-governance-audit.mjs"],
"provenance_tests":["python","-m","unittest","discover","-s","tests","-p","test_provenance.py","-v"],
"human_agency_tests":["python","-m","unittest","discover","-s","tests","-p","test_human_agency_intelligibility.py","-v"],
"global_integration_intake":["node","scripts/ima-daily-loop-intake.mjs"],
"global_human_conversation_learning":["python",".ima/conversation/global_human_conversation_learning.py"],
"global_human_conversation_learning_tests":["python","-m","unittest","discover","-s","tests","-p","test_global_human_conversation_learning.py","-v"],
"universal_intelligence_gateway":["python",".ima/intelligence/universal_intelligence_gateway.py"],
"universal_intelligence_gateway_tests":["python","-m","unittest","discover","-s","tests","-p","test_universal_intelligence_gateway.py","-v"],
"public_reconciliation":["python","scripts/ima_public_reconciliation.py"],
"live_browser_health":["python","scripts/ima_live_browser_health.py"],
"world_pulse":["python","scripts/ima_world_pulse.py"],
}

def now_local(): return datetime.now(timezone.utc).astimezone(TZ).replace(microsecond=0)

def due(now):
    tasks=["web_intelligence","world_pulse","scientific_open_research_tests","foresight_tests","culture_tests","human_intelligence_tests","unified_loop_tests","universal_learning_tests","self_application_tests","creative_bridge_tests","human_agency_tests","world_model_tests","world_model_availability","global_integration_intake","global_human_conversation_learning","global_human_conversation_learning_tests","universal_intelligence_gateway","universal_intelligence_gateway_tests","public_reconciliation","live_browser_health","finance_governance_audit","funding_revenue_intelligence","distribution","capability_contract","growth_cycle","monetization_readiness"]
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

def append_journal(now, results):
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as f:
        for result in results:
            status = result.get("status")
            event_status = "EXECUTED" if status == "PASS" else ("FAILED" if status == "FAIL" else "GAPS_RECORDED")
            entry = {
                "timestamp": now.isoformat(),
                "event": "canonical_loop_task",
                "summary": f"Canonical IMA loop task {result.get('task', 'unknown')} completed with {status or 'UNKNOWN'}",
                "source": "ima-unified-loop",
                "status": event_status,
                "details": {
                    "task": result.get("task"),
                    "command": result.get("command"),
                    "returncode": result.get("returncode"),
                    "evidence": result.get("stdout_tail", ""),
                    "limitations": result.get("stderr_tail", "") if status != "PASS" else "",
                },
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        summary_status = "VERIFIED" if results and all(r.get("status") == "PASS" for r in results) else "GAPS_RECORDED"
        f.write(json.dumps({
            "timestamp": now.isoformat(),
            "event": "canonical_loop_cycle",
            "summary": "Canonical whole-IMA cycle completed; task-level evidence recorded.",
            "source": "ima-unified-loop",
            "status": summary_status,
            "details": {
                "task_count": len(results),
                "passed": sum(r.get("status") == "PASS" for r in results),
                "failed": sum(r.get("status") == "FAIL" for r in results),
                "errors": sum(r.get("status") in {"ERROR", "UNKNOWN", None} for r in results),
                "truth_rule": "Task execution evidence is not proof of public runtime capability.",
            },
        }, ensure_ascii=False) + "\n")

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
    record={"schema":"IMA-UNIFIED-LOOP-1.4","timestamp":now.isoformat(),"timezone":"Asia/Jerusalem","stages":list(STAGES),"scope":list(SYSTEM_SCOPE),"tasks":results,
      "foresight":{"components":foresight,"priority_now_actions":foresight_actions},
      "diagnostics":{"summary":{"total":len(results),"passed":sum(r.get("status")=="PASS" for r in results),"failed":sum(r.get("status")=="FAIL" for r in results),"errors":sum(r.get("status") in {"ERROR","UNKNOWN",None} for r in results)},"findings":findings,"truth_rule":"Diagnostics describe this run; they do not prove live deployment without runtime evidence."},
      "single_scheduler":True,
      "universal_learning_rule":"Every newly accessible field or capability is discovered, evidenced, tested, verified, taught and evaluated for bounded self-application through this loop.",
      "creative_bridge_rule":"When a meaningful gap is detected between domains, IMA may form a bridge hypothesis; it must be tested and evidenced before being treated as verified.",
      "foresight_rule":"For every meaningful IMA component, continuously model plausible future states across near, one-year, multi-year and long horizons; treat them as hypotheses, identify signals and prerequisites, and take only safe present actions that prepare for them.",
      "forward_care_rule":"Every cycle must look ahead at least one year where evidence supports it, identify emerging human needs and capability gaps, and prioritize safe present preparation before avoidable problems become urgent.",
      "global_attention_rule":"Treat every authorized IMA surface and source as one connected evidence field: website, app, GitHub, email, feedback, research, integrations, providers, devices and other permitted channels. Observe small signals, correlate them, verify them and route them through the same canonical loop.",
      "micro_signal_rule":"Tiny regressions and opportunities count: broken links, wording, translations, icons, accessibility friction, auth/memory inconsistencies, repeated questions, provider changes and workflow failures are recorded as signals before prioritization.",
      "relevance_pruning_rule":"Classify knowledge and capabilities as KEEP, CURRENT, EMERGING, HISTORICAL, CONTEXTUAL, STALE, IRRELEVANT, DUPLICATE, SUPERSEDED or RESTRICTED. Remove obsolete operational weight without erasing lawful historical evidence.",
      "self_adaptation_rule":"IMA continuously evaluates identity, logo, visual language, UX, app, integrations, providers, devices, research, community, infrastructure, governance and all other layers. No self-change bypasses authorize -> change -> test -> deploy -> runtime-verify gates.",
      "feedback_fusion_rule":"Authorized feedback from site, app, GitHub, email and connected sources is deduplicated into one evidence pipeline. Feedback is evidence, not automatic truth; recurring signals are contextualized before action.",
      "cooperation_rule":"Relevant peers, competitors, institutions and adjacent systems are reviewed as potential learning and cooperation partners; default relationship is LEARN -> COMPARE -> RESPECT -> CONNECT -> COOPERATE WHERE BENEFICIAL. No partnership or endorsement is claimed without evidence.",
      "universal_shoulder_rule":"IMA should support lawful tasks across domains by first understanding actual context, goal, need, risk and available capability; safety-aware support takes priority when mental or physical danger is indicated.",
      "de_escalation_rule":"When conflict, hatred or violence indicators appear, prioritize factual clarification, dignity, de-escalation and appropriate human/emergency support; never amplify retaliation, dehumanization or fabricated certainty.",
      "global_change_humanitarian_rule":"Observe major world changes through bounded lawful public sources; classify only as a hypothesis, preserve source/time/place/uncertainty, map likely human needs, compare verified historical outcomes, prefer nonviolent options, and connect to authorized help without autonomous external intervention.",
      "self_application_rule":"A verified capability may improve IMA itself only through the same inspect -> change -> test -> verify -> carry-forward gates.",
      "provider_independence_rule":"Separate capability from provider; record alternatives, cost, license, privacy and unresolved gaps.",
      "truth_rule":"Documentation, intention, advertised availability and generated state are not runtime proof; verification must be recorded separately.",
      "lawful_distribution_rule":"Public sharing is limited to lawful, consent-respecting, non-spam channels and authorized accounts.",
      "user_change_rule":"Every explicit request to add or change the loop is reconciled into this canonical loop contract.",
      "global_attention_charter":"docs/IMA_GLOBAL_ATTENTION_RELEVANCE_ADAPTATION_AND_BENEVOLENT_GROWTH_CHARTER.md",
      "provenance_rule":"Every present and future IMA capability is lineage-tracked from imagination/proposal through implementation, testing, deployment and verified-live evidence; provenance, limitations and contributors are preserved.",
      "cross_domain_reconciliation_rule":"All IMA domains, interfaces, memories, research, creative work, integrations, governance and future capabilities must reconcile into one canonical identity, capability lineage and single improvement loop; duplicate parallel systems are not permitted without explicit justification.",
      "multi_perspective_rule":"Review meaningful changes through relevant user, customer, executive, operator, technical, accessibility, privacy, finance, distribution, community and future lenses at micro/product/macro/system-of-systems scales and now-to-intergenerational horizons; evidence gates remain mandatory.",
      "global_integration_rule":"Every newly verified external integration is automatically ingested through the canonical daily intake, deduplicated, evidence-checked and carried into the next improvement cycle; no second daily orchestrator is created.",
      "live_browser_continuity_rule":"LIVE-001 is continuously checked by the canonical loop. BrowserGlass/public endpoint health and security boundaries are tested automatically; ChatGPT embedded rendering, local Termux/Chrome connectivity, authentication and consequential action outcomes remain separately unverified until runtime evidence exists. Future live-browser improvement requests are reconciled to LIVE-001 rather than creating a parallel surface.",
      "global_scan_boundary_rule":"Global discovery means broad lawful discovery within actual tool access, permissions, robots, rate limits, rights and privacy boundaries; never claim exhaustive internet coverage when it was not achieved.",
      "ecosystem_cooperation_rule":"Other intelligences, tools, providers, infrastructure and competitors are evaluated for learning, interoperability and beneficial cooperation. No impersonation, sabotage, manipulation, private-data collection or unsupported partnership claim.",
      "global_user_benefit_rule":"Verified capabilities are evaluated for safe, lawful, consent-respecting reuse across IMA users without exposing private memory or private identity data.","world_model_rule":"Interactive world models are simulations, not reality. Use them for bounded exploration, education and hypothesis testing; preserve provenance, human control and reversible actions, and require real-world validation for high-impact decisions. Do not claim a live world-model provider integration unless independently verified.",
      "human_agency_rule":"IMA must preserve meaningful human agency: people should be able to understand consequential AI behavior at an appropriate level, question it, challenge it, obtain human review, and know who is accountable.","finance_truth_rule":"Revenue and expenses require evidence; estimates, views, followers, eligibility and projections are never income; no autonomous spending or financial commitment is permitted.",
      "funding_revenue_loop_rule":"The canonical loop continuously scans global lawful funding and revenue routes, prioritizing zero-upfront-cost paths. It must verify current status, deadline, amount, geography, recipient/entity eligibility, application cost, payment mechanics, source authority, and concrete activation step. It must keep only actionable routes in the live registry, prune closed/stale/non-fit routes, distinguish revenue from grants/investment/credits, and record what was achieved, what was not, what can be done now, what is blocked and the smallest human action needed. It may prepare evidence packs, drafts, code, disclosures and activation infrastructure without spending money or making legal attestations. It must not submit legally binding applications, accept terms, add payment methods, purchase, upgrade paid plans, or claim funds as received without human authorization and provider evidence.",
      "funding_learning_rule":"Each verified funding or revenue outcome becomes economic learning: compare expected value, effort, eligibility, conversion and actual result; update prioritization and future search criteria. Prefer routes that improve both IMA sustainability and public benefit, while never allowing financial incentives to alter factual, safety or governance conclusions.",
      "global_update_rule":"World changes are not only news: funding windows, program eligibility, provider pricing, payment rails, AI access tiers, regulation, partnership programs and compute-credit availability are treated as operational signals. Re-check them through the same evidence and stale-pruning gates and continuously evolve the loop contract when reliable evidence shows a better method.",
      "finance_governance_spec":"Use docs/IMA_GLOBAL_NONPROFIT_CHARTER.md, docs/IMA_FINANCIAL_LEDGER_SCHEMA.json, docs/IMA_CREATOR_SUCCESSION_AND_ESTATE.md and data/IMA_FINANCIAL_EVIDENCE_LEDGER.json as canonical specifications. Keep personal creator property, creator compensation, nonprofit operating costs, restricted funds and humanitarian/community benefit separate. No legal nonprofit status is claimed without registration evidence. No fixed surplus percentages are inferred.",
      "nonprofit_creator_separation_rule":"Public-benefit mission assets remain separate from Ori Cohen personal property, creator compensation, royalties and estate rights; legal nonprofit status is never inferred from repository governance.",
      "surplus_allocation_rule":"refunds/chargebacks/required_taxes -> verified_transaction_and_platform_fees -> authorized_operating_expenses -> documented_creator_compensation_or_license_royalty -> required_reserve -> nonprofit_mission_reinvestment -> authorized_humanitarian_or_community_benefit; no fixed percentages without explicit approval.",
      "critical_ai_dependency_rule":"For high-impact systems, IMA continuously checks intelligibility, contestability, human override, traceability, independent verification, reversibility, provider plurality, rights visibility, failure behavior and concentration of power; when verification fails, autonomy must not silently increase."}
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    append_journal(now, results)
    return record

if __name__=="__main__": print(json.dumps(run_loop(),ensure_ascii=False,indent=2))
