"use strict";

/**
 * IMA Innovation Loop
 * Canonical extension of Continuous Betterment.
 * Learns from authorized human input, research, real-world outcomes,
 * external ecosystems and failures/successes without copying private data
 * or treating novelty as truth.
 */
const SOURCES=Object.freeze([
  "USER_FEEDBACK","RESEARCH","OPEN_SOURCE","MARKET","COMPETITOR",
  "SCIENCE","ARTS","ENGINEERING","EDUCATION","COMMUNITY","FAILURE","SUCCESS"
]);
const HORIZONS=Object.freeze(["NOW","NEAR","FRONTIER"]);

function norm(v){return typeof v==="string"?v.trim().toUpperCase():v??"UNKNOWN";}

function collectSignals(inputs=[]){
  return (Array.isArray(inputs)?inputs:[]).map((x,i)=>({
    id:x.id||`signal-${i+1}`,
    source:SOURCES.includes(norm(x.source))?norm(x.source):"RESEARCH",
    horizon:HORIZONS.includes(norm(x.horizon))?norm(x.horizon):"NEAR",
    claim:x.claim||"",
    evidence:x.evidence||null,
    provenance:x.provenance||null,
    privacy_safe:x.privacy_safe!==false,
    authorized:x.authorized!==false
  })).filter(x=>x.privacy_safe&&x.authorized&&x.claim);
}

function generateCandidates(signals=[]){
  const usable=collectSignals(signals);
  return usable.map((s,i)=>({
    id:`innovation-${i+1}`,
    source:s.source,
    horizon:s.horizon,
    hypothesis:s.claim,
    evidence:s.evidence,
    provenance:s.provenance,
    novelty_score:s.horizon==="FRONTIER"?3:s.horizon==="NEAR"?2:1,
    impact_score:s.source==="SUCCESS"||s.source==="USER_FEEDBACK"?3:2,
    readiness:s.evidence?"EVIDENCE_AVAILABLE":"EVIDENCE_GAP",
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

function innovationPlan(signals=[]){
  const candidates=prioritize(generateCandidates(signals));
  return {
    principle:"IMA must continuously learn from humanity and the world without becoming dependent on any single person.",
    source_coverage:SOURCES,
    candidates,
    experiment_rule:"Prefer small, reversible, measurable experiments before irreversible adoption.",
    truth_rule:"Novelty is a hypothesis until independently evidenced.",
    human_agency_rule:"Do not replace human authorship, consent, ownership or accountable decisions.",
    privacy_rule:"Private user data is never generalized into another user's context without authorization.",
    continuity_rule:"Every valuable capability must have documentation, tests, provenance and more than one maintainer/path where feasible."
  };
}

module.exports={SOURCES,HORIZONS,collectSignals,generateCandidates,prioritize,innovationPlan};
