"use strict";
const assert=require("node:assert/strict");
const m=require("../kernel/runtime/CANONICAL/IMA_INNOVATION_LOOP");

const signals=[
 {source:"SUCCESS",horizon:"NOW",entity_type:"COMPANY",claim:"A successful workflow should become a reusable capability.",outcome:"faster delivery",evidence:"verified outcome",authorized:true},
 {source:"FAILURE",horizon:"PAST",entity_type:"ORGANIZATION",claim:"A recurring failure pattern should become a prevention control.",cause:"single point of failure",evidence:"incident record",authorized:true},
 {source:"SCIENCE",horizon:"FRONTIER",entity_type:"SYSTEM",claim:"Explore a new human-computer interaction hypothesis.",evidence:null,authorized:true},
 {source:"USER_FEEDBACK",horizon:"NEAR",entity_type:"PERSON",claim:"Users need fewer steps to recover from failure.",evidence:"feedback",authorized:true},
 {source:"USER_FEEDBACK",claim:"private secret",privacy_safe:false,authorized:true}
];
const collected=m.collectSignals(signals);
assert.equal(collected.length,4);
const plan=m.buildUniversalLearningPlan(signals);
assert.equal(plan.candidates.length,4);
assert.ok(plan.candidates.some(x=>x.readiness==="EVIDENCE_GAP"));
assert.ok(plan.candidates.some(x=>x.learning_mode==="PREVENT"));
assert.ok(plan.coverage.sources.includes("SUCCESS"));
assert.ok(plan.coverage.sources.includes("FAILURE"));
assert.ok(plan.coverage.entities.includes("PERSON"));
assert.ok(plan.coverage.horizons.includes("FRONTIER"));
assert.equal(plan.privacy_rule.includes("never"),true);
assert.equal(plan.preemption_rule.includes("failure"),true);
console.log("IMA universal innovation/resilience learning loop: PASS");
