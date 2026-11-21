"use strict";
const assert=require("node:assert/strict");
const m=require("../kernel/runtime/CANONICAL/IMA_INNOVATION_LOOP");

const signals=[
 {source:"SUCCESS",horizon:"NOW",claim:"A successful user workflow should become a reusable capability.",evidence:"verified outcome",authorized:true},
 {source:"SCIENCE",horizon:"FRONTIER",claim:"Explore a new human-computer interaction hypothesis.",evidence:null,authorized:true},
 {source:"USER_FEEDBACK",horizon:"NEAR",claim:"Users need fewer steps to recover from failure.",evidence:"feedback",authorized:true},
 {source:"USER_FEEDBACK",claim:"private secret",privacy_safe:false,authorized:true}
];
const collected=m.collectSignals(signals);
assert.equal(collected.length,3);
const plan=m.innovationPlan(signals);
assert.equal(plan.candidates.length,3);
assert.ok(plan.candidates.some(x=>x.readiness==="EVIDENCE_GAP"));
assert.ok(plan.source_coverage.includes("FAILURE"));
assert.equal(plan.privacy_rule.includes("never"),true);
console.log("IMA innovation loop: PASS");
