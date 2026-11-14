"use strict";

const assert = require("assert");
const learning = require("../kernel/runtime/CANONICAL/IMA_CONTINUOUS_LEARNING");

const seeded = learning.seed();
assert.ok(seeded.count >= 7);

const result = learning.ingest({
  title: "test evidence",
  source: "https://example.org/test",
  status: "VERIFIED",
  reproducible: true,
  domain: "AGENCY",
  pattern: "A user can retain meaningful control over the system.",
  action: "Test an explicit control surface."
});

assert.strictEqual(result.rejected.length, 0);
assert.ok(result.accepted.length === 1 || learning.evidence().some(x => x.title === "test evidence"));

const synthesis = learning.synthesize();
assert.ok(synthesis.total_evidence >= 8);
assert.ok(synthesis.domains.some(x => x.domain === "AGENCY"));

const actions = learning.nextActions();
assert.ok(actions.some(x => x.approval_required === true));

console.log("IMA continuous learning loop: PASS");
