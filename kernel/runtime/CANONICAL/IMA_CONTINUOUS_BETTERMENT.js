"use strict";

/**
 * IMA Continuous Betterment Matrix
 * A bounded, evidence-first way to decide what "better" means.
 */
const DIMENSIONS=Object.freeze([
  "TRUTH","SAFETY","HUMAN_AGENCY","HEALTH_AND_WELLBEING","ACCESSIBILITY",
  "PRIVACY","SECURITY","CAPABILITY","USEFULNESS","CLARITY","UX",
  "RELIABILITY","PERFORMANCE","INTEROPERABILITY","PRESERVATION",
  "LEARNING","GOVERNANCE","ECONOMIC_SUSTAINABILITY","COMMUNITY_BENEFIT",
  "ENVIRONMENTAL_RESPONSIBILITY"
]);
const PRIORITIES=Object.freeze(["CRITICAL","HIGH","NORMAL","LOW"]);
function normalize(v){return typeof v==="string"?v.trim().toUpperCase():v??"UNKNOWN";}
function evaluate(change={}){
  const evidence=normalize(change.evidence);
  const risk=normalize(change.risk);
  const reversibility=normalize(change.reversibility);
  const humanImpact=normalize(change.human_impact);
  let priority="NORMAL";
  if(["UNKNOWN","WEAK"].includes(evidence)) priority="LOW";
  if(["HIGH","CRITICAL"].includes(risk)) priority="CRITICAL";
  else if(["HIGH"].includes(humanImpact)) priority=priority==="CRITICAL"?"CRITICAL":"HIGH";
  const allowed = !["CRITICAL","HIGH"].includes(risk) || change.human_authorized===true;
  return {
    allowed,
    priority,
    dimensions:Array.isArray(change.dimensions)&&change.dimensions.length?change.dimensions.filter(d=>DIMENSIONS.includes(normalize(d))).map(normalize):["USEFULNESS"],
    evidence,
    risk,
    reversibility,
    human_impact:humanImpact,
    reason:allowed?"CHANGE_CAN_BE_CONSIDERED":"HUMAN_AUTHORIZATION_REQUIRED_FOR_HIGH_IMPACT_RISK",
    rule:"Improve what can be evidenced; preserve what cannot yet be safely improved; never trade away truth, safety, agency, privacy or human authorization for convenience."
  };
}
function selfAssessment(signals={}){
  return evaluate({
    evidence:signals.evidence||"UNKNOWN",
    risk:signals.risk||"UNKNOWN",
    reversibility:signals.reversibility||"UNKNOWN",
    human_impact:signals.human_impact||"UNKNOWN",
    dimensions:DIMENSIONS,
    human_authorized:false
  });
}
module.exports={DIMENSIONS,PRIORITIES,evaluate,selfAssessment};
