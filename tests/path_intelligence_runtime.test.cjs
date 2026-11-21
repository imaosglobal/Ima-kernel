const assert=require("node:assert/strict");
const runtime=require("../kernel/runtime/CANONICAL/IMA_RUNTIME.js");
const p=runtime.pathIntelligence.ingest({
  goal:"test canonical integration",
  current_state:"blocked",
  blocker:"missing bridge",
  path:["identify","prepare","cross","verify"],
  minimum_required_human_action:"approve required boundary",
  human_boundary:"APPROVAL",
  evidence:["test-evidence"],
  outcome:"crossed",
  privacy_classification:"ABSTRACTED",
  reuse_scope:"PUBLIC_PATTERN",
  confidence:"VERIFIED"
});
assert.equal(runtime.pathIntelligence.status().canonical,true);
assert.equal(p.type,"PATH_RECORD");
assert.equal(runtime.pathIntelligence.teachBack(p).ok,true);
console.log("PATH_INTELLIGENCE_RUNTIME=PASS");