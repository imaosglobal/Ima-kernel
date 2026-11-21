"use strict";

/**
 * IMA Innovation + Resilience Learning Loop
 * Canonical extension of Continuous Learning / Betterment.
 *
 * Core formula:
 * success + failure + change signals
 * -> understand cause -> extract transferable principle
 * -> preempt risk / generate opportunity
 * -> bounded experiment -> evidence
 * -> capability -> deployment -> measurement -> learning.
 *
 * Applies across people, teams, organizations, products, communities and
 * other authorized entities, across past/present/future time horizons.
 * It must not depend on one founder, leader, researcher, model or source.
 */
const SOURCES=Object.freeze([
  "USER_FEEDBACK","RESEARCH","OPEN_SOURCE","MARKET","COMPETITOR",
  "SCIENCE","ARTS","ENGINEERING","EDUCATION","COMMUNITY","FAILURE","SUCCESS"
]);
const HORIZONS=Object.freeze(["PAST","NOW","NEAR","FRONTIER"]);
const ENTITY_TYPES=Object.freeze([
  "PERSON","TEAM","COMPANY","ORGANIZATION","COMMUNITY","PRODUCT",
  "SERVICE","SYSTEM","INSTITUTION","OTHER"
]);
const LEARNING_MODES=Object.freeze([
  "PREVENT","ADAPT","INNOVATE","RECOVER","SCALE","REPLICATE","RETIRE"
]);
const COMPASSION_STEPS=Object.freeze([
  "NOTICE","UNDERSTAND","CHECK_TRUTH_AND_CONTEXT","ASSESS_HARM_AND_NEED",
  "RESPOND_WITH_DIGNITY","SET_BOUNDARIES_WHEN_NEEDED","CHECK_EFFECT","LEARN","ADJUST"
]);

function norm(v){return typeof v==="string"?v.trim().toUpperCase():v??"UNKNOWN";}

function collectSignals(inputs=[]){
  return (Array.isArray(inputs)?inputs:[]).map((x,i)=>({
    id:x.id||`signal-${i+1}`,
    source:SOURCES.includes(norm(x.source))?norm(x.source):"RESEARCH",
    horizon:HORIZONS.includes(norm(x.horizon))?norm(x.horizon):"NOW",
    entity_type:ENTITY_TYPES.includes(norm(x.entity_type))?norm(x.entity_type):"OTHER",
    entity_id:x.entity_id||null,
    claim:x.claim||"",
    outcome:x.outcome||null,
    cause:x.cause||null,
    evidence:x.evidence||null,
    provenance:x.provenance||null,
    privacy_safe:x.privacy_safe!==false,
    authorized:x.authorized!==false,
    suffering_or_need:x.suffering_or_need||null,
    affected_parties:Array.isArray(x.affected_parties)?x.affected_parties:[],
    boundaries:Array.isArray(x.boundaries)?x.boundaries:[]
  })).filter(x=>x.privacy_safe&&x.authorized&&x.claim);
}

function extractPrinciple(signal){
  if(signal.cause) return `Transfer the evidenced causal lesson: ${signal.cause}`;
  if(signal.outcome) return `Study the mechanism behind the observed outcome: ${signal.outcome}`;
  return "Identify the smallest transferable principle before copying the observed result.";
}

function compassionAssessment(signal){
  const need=signal.suffering_or_need||null;
  return {
    detected:!!need,
    need,
    action:need
      ?"Understand context, reduce avoidable harm, preserve dignity, and measure whether the response helped."
      :"No suffering/need signal supplied; do not invent one.",
    boundaries:["truth","safety","consent","rights","privacy","law","fairness","human_agency","long_term_well_being"],
    cycle:[...COMPASSION_STEPS]
  };
}
function chooseBoundedResponse(signal){
  const c=compassionAssessment(signal);
  return {
    compassion:c,
    response_mode:c.detected?"COMPASSIONATE_WITH_BOUNDARIES":"STANDARD_LEARNING",
    boundary_rule:"Compassion is not agreement or emotional performance; refuse, pause, redirect or escalate when compliance would create greater harm."
  };
}
function generateCandidates(signals=[]){
  const usable=collectSignals(signals);
  return usable.map((s,i)=>({
    id:`innovation-${i+1}`,
    source:s.source,
    horizon:s.horizon,
    entity_type:s.entity_type,
    entity_id:s.entity_id,
    hypothesis:s.claim,
    transferable_principle:extractPrinciple(s),
    outcome:s.outcome,
    evidence:s.evidence,
    provenance:s.provenance,
    novelty_score:s.horizon==="FRONTIER"?3:s.horizon==="NEAR"?2:1,
    impact_score:s.source==="SUCCESS"||s.source==="USER_FEEDBACK"||s.source==="FAILURE"?3:2,
    readiness:s.evidence?"EVIDENCE_AVAILABLE":"EVIDENCE_GAP",
    learning_mode:s.source==="FAILURE"?"PREVENT":s.source==="SUCCESS"?"REPLICATE":"INNOVATE",
    compassionate_response:chooseBoundedResponse(s),
    next_step:s.evidence
      ?"Run a bounded, reversible experiment and measure outcome."
      :"Seek independent evidence before treating this as a product direction."
  }));
}

function prioritize(candidates=[]){
  return [...candidates].sort((a,b)=>
    (b.impact_score+b.novelty_score)-(a.impact_score+a.novelty_score)
  );
}

function buildUniversalLearningPlan(signals=[]){
  const candidates=prioritize(generateCandidates(signals));
  return {
    principle:"IMA continuously learns from humanity and the world; no single person, organization, model or source is a permanent bottleneck.",
    formula:[
      "OBSERVE",
      "VERIFY",
      "UNDERSTAND_CAUSE",
      "EXTRACT_PRINCIPLE",
      "RECOGNIZE_SUFFERING_AND_NEED",
      "PREEMPT_OR_CREATE",
      "CHOOSE_COMPASSIONATE_RESPONSE_WITH_BOUNDARIES",
      "EXPERIMENT",
      "MEASURE",
      "ADOPT_OR_REJECT",
      "DOCUMENT",
      "TEACH_BACK",
      "REPEAT"
    ],
    coverage:{
      entities:ENTITY_TYPES,
      horizons:HORIZONS,
      sources:SOURCES
    },
    candidates,
    preemption_rule:"Every material failure pattern should generate a prevention hypothesis before it becomes an IMA failure, when evidence permits.",
    success_rule:"Every material success should be analyzed for mechanism, transferable principle, boundary conditions and replication potential—not merely recorded as a win.",
    crisis_rule:"When an external person or organization enters a crisis, learn the preventable causes and controls without exploiting private information or importing unverified claims.",
    accumulation_rule:"New capability should build on prior verified capabilities; retire or replace only when evidence shows the old layer is inferior or unsafe.",
    experiment_rule:"Prefer small, reversible, measurable experiments before irreversible adoption.",
    truth_rule:"Observation, hypothesis, metaphor and verified fact remain explicitly distinct.",
    privacy_rule:"Private data is never generalized into another person's or organization's context without authorization and lawful basis.",
    agency_rule:"Do not replace human authorship, consent, ownership or accountable decisions.",
    resilience_rule:"Design for graceful degradation, succession, redundancy, recovery and learning before crisis.",
    continuity_rule:"Every valuable capability should have documentation, tests, provenance and more than one maintainer/path where feasible.",
    compassion_cycle:[...COMPASSION_STEPS],
    compassion_rule:"Treat suffering, vulnerability, exclusion, fear, loss and legitimate unmet need as signals; compassion is action bounded by truth, safety, consent, rights, privacy, law, fairness, agency and long-term well-being.",
    balance_rule:"Balance immediate relief vs long-term capability, individual vs others affected, autonomy vs safety, speed vs verification, innovation vs stability, privacy vs legitimate evidence, and compassion vs harmful enabling.",
    agency_rule_expanded:"Prefer outcomes that increase human capability and reduce unnecessary dependence on IMA."
  };
}

function innovationPlan(signals=[]){
  return buildUniversalLearningPlan(signals);
}

function buildPathRecord(input={}){
  const x=input||{};
  const required=(v)=>Array.isArray(v)?v.filter(Boolean):[];
  return {
    type:"PATH_RECORD", version:"1.0",
    goal:x.goal||"", current_state:x.current_state||"UNKNOWN",
    blocker:x.blocker||null, prerequisites:required(x.prerequisites),
    constraints:required(x.constraints), decision_points:required(x.decision_points),
    verified_options:required(x.verified_options), path:required(x.path),
    minimum_required_human_action:x.minimum_required_human_action||null,
    human_boundary:x.human_boundary||null, execution:required(x.execution),
    evidence:required(x.evidence), outcome:x.outcome||null,
    failure_modes:required(x.failure_modes), recovery_branches:required(x.recovery_branches),
    accessibility:required(x.accessibility), cost_time_effort:x.cost_time_effort||null,
    privacy_classification:x.privacy_classification||"PRIVATE",
    reuse_scope:x.reuse_scope||"AUTHORIZED_ABSTRACT_LESSONS_ONLY",
    confidence:x.confidence??"UNKNOWN", last_verification:x.last_verification||null,
    provenance:x.provenance||null,
    transfer_rule:"PRIVATE_EXPERIENCE -> VERIFIED_ABSTRACT_PRINCIPLE -> REUSABLE_PATTERN -> INDEPENDENTLY_TESTED_PATH",
    agency_rule:"Remove unnecessary friction without removing the person's authority over decisions that belong to them."
  };
}
function pathFromSignals(signals=[]){
  return collectSignals(signals).map((s,i)=>buildPathRecord({
    goal:s.claim, current_state:s.horizon, blocker:s.cause,
    path:[extractPrinciple(s)], evidence:s.evidence?[s.evidence]:[],
    outcome:s.outcome, provenance:s.provenance,
    privacy_classification:"ABSTRACTED",
    confidence:s.evidence?"EVIDENCE_AVAILABLE":"UNKNOWN"
  })).map((p,i)=>Object.assign(p,{id:"path-"+(i+1)}));
}

module.exports={
  SOURCES,HORIZONS,ENTITY_TYPES,LEARNING_MODES,COMPASSION_STEPS,
  collectSignals,extractPrinciple,generateCandidates,prioritize,
  buildUniversalLearningPlan,innovationPlan,buildPathRecord,pathFromSignals
};
