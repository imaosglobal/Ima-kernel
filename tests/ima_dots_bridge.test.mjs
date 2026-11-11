import assert from "node:assert/strict";
import dots from "../kernel/runtime/CANONICAL/IMA_DOTS_BRIDGE.js";

assert.equal(dots.DOTS_ID, "ima-dots");
assert.equal(dots.CONTRACT_VERSION, "1.0.0");

const registered = dots.register();
assert.equal(registered, "ima-dots");

const card = dots.card();
assert.ok(card.capabilities.includes("bidirectional-learning"));
assert.equal(card.safety.human_agency, true);
assert.equal(card.safety.no_permission_escalation, true);

const a = dots.teachIma("DOTS can monitor long-running goals.", { source: "test" });
assert.equal(a.content.direction, "DOTS_TO_IMA");

const b = dots.teachDots("IMA requires provenance for learned changes.", { source: "test" });
assert.equal(b.content.direction, "IMA_TO_DOTS");

const run = await dots.run({
  goal: "verify bidirectional learning bridge",
  action: "monitor",
  capability: "research"
});
assert.equal(run.verification.verified, true);
assert.equal(run.result.delegated, true);

const status = dots.status();
assert.equal(status.active, true);
assert.equal(status.registered, true);
assert.ok(status.memory.length >= 2);

console.log(JSON.stringify({
  ok: true,
  dots: status.id,
  bidirectional_learning: true,
  memory_records: status.memory.length
}, null, 2));
