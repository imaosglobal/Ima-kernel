"use strict";

const STATUSES = Object.freeze(["PLANNED","ATTEMPTED","EXECUTED","VERIFIED","FAILED","GAPS_RECORDED"]);

function assess(evidence = {}) {
  const hasSource = typeof evidence.source === "string" && evidence.source.length > 0;
  const hasTimestamp = Boolean(evidence.timestamp || evidence.checked_at);
  const hasReproduction = Boolean(evidence.reproducible || evidence.reproduction || evidence.test);
  const status = evidence.status || "GAPS_RECORDED";
  const verified = status === "VERIFIED" && hasSource && hasTimestamp && hasReproduction;
  return {
    verified,
    status: STATUSES.includes(status) ? status : "GAPS_RECORDED",
    source_present: hasSource,
    timestamp_present: hasTimestamp,
    reproducible_evidence_present: hasReproduction,
    claim_allowed: verified
  };
}

function assertVerified(evidence) {
  const result = assess(evidence);
  if (!result.verified) {
    throw new Error("TRUTH_GATE_REQUIRES_REPRODUCIBLE_VERIFIED_EVIDENCE");
  }
  return result;
}

module.exports = { STATUSES, assess, assertVerified };
