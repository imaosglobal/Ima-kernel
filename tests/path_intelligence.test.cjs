const assert=require("node:assert/strict");
(async()=>{
  const m=await import("../kernel/runtime/CANONICAL/IMA_INNOVATION_LOOP.js");
  const p=m.buildPathRecord({
    goal:"cross a blocker", current_state:"stuck", blocker:"missing access",
    prerequisites:["identity"], path:["discover","prepare","handoff","verify"],
    minimum_required_human_action:"approve identity step",
    evidence:["verified-result"], outcome:"completed",
    recovery_branches:["retry with alternate provider"], accessibility:["keyboard"],
    privacy_classification:"ABSTRACTED", reuse_scope:"PUBLIC_PATTERN",
    confidence:"VERIFIED", last_verification:"2026-11-21"
  });
  assert.equal(p.type,"PATH_RECORD");
  assert.equal(p.minimum_required_human_action,"approve identity step");
  assert.match(p.transfer_rule,/VERIFIED_ABSTRACT_PRINCIPLE/);
  const paths=m.pathFromSignals([{id:"s1",source:"SUCCESS",claim:"reach a verified outcome",cause:"missing access",evidence:"receipt",outcome:"done",authorized:true,privacy_safe:true}]);
  assert.equal(paths.length,1);
  assert.equal(paths[0].privacy_classification,"ABSTRACTED");
  console.log("PATH_INTELLIGENCE_TEST_PASS");
})();