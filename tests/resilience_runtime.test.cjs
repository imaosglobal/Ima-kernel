const assert = require("node:assert/strict");

(async () => {
  const { classifyIncident, buildResiliencePlan, gateAction, buildEvidenceRecord } =
    await import("../core/resilience-runtime.js");

  const incident = classifyIncident({
    category: "REPUTATION",
    severity: "HIGH",
    confidence: "HIGH",
    verified: true,
    source: "test",
    unknowns: ["scope"]
  });

  assert.equal(incident.category, "REPUTATION");
  assert.equal(incident.severity, "HIGH");
  assert.equal(incident.verified, true);
  assert.deepEqual(incident.unknowns, ["scope"]);

  const plan = buildResiliencePlan(incident);
  assert.equal(plan.protocol, "GLOBAL_RESILIENCE_AND_CRISIS_PROTOCOL");
  assert.equal(plan.human_boundary, "REVIEW");
  assert.equal(plan.communication.verified_only, true);
  assert.equal(plan.communication.include_unknowns, true);
  assert.ok(plan.actions.includes("PRESERVE_EVIDENCE"));

  assert.deepEqual(gateAction({}).boundary, "NONE");
  assert.equal(gateAction({requiresIdentity:true}).must_stop, true);
  assert.equal(gateAction({requiresSignature:true}).must_stop, true);
  assert.equal(gateAction({requiresBanking:true}).must_stop, true);
  assert.equal(gateAction({requiresAccountableDecision:true}).must_stop, true);
  assert.equal(gateAction({requiresHuman:true, irreversible:true, authorized:false}).boundary, "APPROVAL");

  const evidence = buildEvidenceRecord({
    incident,
    action: {type:"contain"},
    result: {status:"verified"}
  });
  assert.equal(evidence.provenance_required, true);
  assert.deepEqual(evidence.unresolved_unknowns, ["scope"]);

  console.log("resilience-runtime: PASS");
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
