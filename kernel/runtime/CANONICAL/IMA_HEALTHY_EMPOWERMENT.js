"use strict";

const MODES = Object.freeze(["STABILIZE","SUPPORT","BUILD_CAPACITY","ENABLE_INDEPENDENCE","PARTICIPATE","CONTRIBUTE"]);
const TONES = Object.freeze(["POSITIVE","NEUTRAL","GENTLE_HUMOR"]);
const NON_NEGOTIABLES = Object.freeze({
  no_invented_state:true, preserve_agency:true, no_harm_to_self_or_others:true,
  no_dependency_design:true, no_coercion:true, reversible_steps_preferred:true,
  uncertainty_explicit:true
});
function normalize(v){ if(v===null||v===undefined)return "UNKNOWN"; if(typeof v==="string")return v.trim().toUpperCase(); return v; }
function assess(input={}){
  const safety=normalize(input.safety), capacity=normalize(input.capacity), energy=normalize(input.energy);
  const overload=normalize(input.overload), agency=normalize(input.agency), goal=input.goal||null;
  let mode="SUPPORT", reason="INSUFFICIENT_CURRENT_STATE", urgency="UNKNOWN";
  if(["IMMEDIATE_DANGER","MEDICAL_EMERGENCY","SEVERE_DISORIENTATION"].includes(safety)){mode="STABILIZE";urgency="IMMEDIATE_HUMAN_HELP";reason="CURRENT_SAFETY_SIGNAL_REQUIRES_HUMAN_ESCALATION";}
  else if(["LOW","VERY_LOW"].includes(capacity)||["HIGH","VERY_HIGH"].includes(overload)){mode="STABILIZE";urgency="HIGH_SUPPORT";reason="CURRENT_LOAD_EXCEEDS_RELIABLE_CAPACITY";}
  else if(agency==="LOW"){mode="SUPPORT";urgency="SUPPORT";reason="RESTORE_CHOICE_BEFORE_INCREASING_DEMAND";}
  else if(capacity==="MODERATE"||energy==="MODERATE"){mode="BUILD_CAPACITY";urgency="NORMAL";reason="BUILD_ONE_REALISTIC_CAPABILITY";}
  else if(capacity==="HIGH"&&agency!=="LOW"){mode=goal?"ENABLE_INDEPENDENCE":"PARTICIPATE";urgency="NORMAL";reason=goal?"SUPPORT_SELF_DIRECTED_PROGRESS":"CAPACITY_AVAILABLE_FOR_CHOICE";}
  return {mode,urgency,reason,goal,observed:{safety,capacity,energy,overload,agency},evidence_rule:"Only explicitly supplied or verified current-state signals are used; UNKNOWN stays UNKNOWN."};
}
function chooseTone(input={}){
  const p=normalize(input.tone_preference);
  if(TONES.includes(p))return p;
  if(input.distress===true||input.safety==="IMMEDIATE_DANGER")return "NEUTRAL";
  if(input.humor_welcome===true&&input.high_stakes!==true)return "GENTLE_HUMOR";
  return "POSITIVE";
}
function plan(input={}){
  const assessment=assess(input), tone=chooseTone(input);
  const steps={
    STABILIZE:["reduce unnecessary load","orient to immediate reality","identify appropriate human help when needed","choose one safe next step"],
    SUPPORT:["clarify what help is wanted","offer a small number of choices","protect boundaries","avoid taking over"],
    BUILD_CAPACITY:["choose one realistic skill or capability","practice or prepare","review what worked","keep the change reversible where practical"],
    ENABLE_INDEPENDENCE:["remove unnecessary friction","provide tools/knowledge","let the person decide","make support easy to stop"],
    PARTICIPATE:["support self-directed action","connect with people/tools/resources","measure useful outcomes rather than dependence"],
    CONTRIBUTE:["offer opportunities to help others","preserve choice and boundaries","learn from the contribution without exploiting it"]
  }[assessment.mode];
  return {...assessment,tone,steps,guardrails:NON_NEGOTIABLES,success:["meaningful choice is retained","the next step fits current capacity","no unnecessary harm or coercion is introduced","the person can reject or stop IMA support","support increases capability or reduces unnecessary load"]};
}
function selfAssessment(runtimeSignals={}){
  return plan({safety:runtimeSignals.safety||"UNKNOWN",capacity:runtimeSignals.capacity||"UNKNOWN",energy:runtimeSignals.energy||"UNKNOWN",overload:runtimeSignals.overload||"UNKNOWN",agency:runtimeSignals.agency||"HIGH",goal:"IMA should improve its own capability without becoming autonomous over people.",humor_welcome:false,high_stakes:true});
}
module.exports={MODES,TONES,NON_NEGOTIABLES,assess,chooseTone,plan,selfAssessment};
