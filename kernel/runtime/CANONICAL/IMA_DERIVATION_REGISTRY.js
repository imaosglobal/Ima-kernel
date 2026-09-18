"use strict";

const crypto = require("crypto");

const records = new Map();

function hashContent(content) {
  return crypto
    .createHash("sha256")
    .update(String(content), "utf8")
    .digest("hex");
}

function validate(record) {
  return Boolean(
    record &&
    record.original_artifact_id &&
    record.derivative_artifact_id &&
    record.content !== undefined
  );
}

function registerDerivative(input) {
  if (!validate(input)) {
    throw new Error("INVALID_DERIVATION_RECORD");
  }

  const contentHash = hashContent(input.content);

  const record = {
    original_artifact_id: input.original_artifact_id,
    derivative_artifact_id: input.derivative_artifact_id,
    source_language: input.source_language || null,
    target_language: input.target_language || null,
    derivation_type: input.derivation_type || "translation",
    content_hash: contentHash,
    content: String(input.content),
    created_at: new Date().toISOString()
  };

  records.set(record.derivative_artifact_id, record);
  return { ...record };
}

function verifyRecord(id) {
  const record = records.get(id);

  if (!record) {
    return {
      valid: false,
      reason: "NOT_FOUND"
    };
  }

  const actual = hashContent(record.content);

  return {
    valid: actual === record.content_hash,
    artifact_id: id,
    expected: record.content_hash,
    actual
  };
}

function list() {
  return [...records.values()].map(record => ({
    ...record,
    content: undefined
  }));
}

// Runtime-compatible registry verification.
// Verifies every currently registered derivation record.
function verifyAll() {
  const results = [...records.keys()].map(verifyRecord);
  const invalid = results.filter(result => !result.valid);

  return {
    valid: invalid.length === 0,
    total: results.length,
    verified: results.length - invalid.length,
    invalid: invalid.length,
    results
  };
}

// Runtime-compatible build operation.
// Returns a deterministic snapshot of the active registry.
function build() {
  return {
    type: "IMA_DERIVATION_REGISTRY",
    version: "1.0",
    total: records.size,
    records: list()
  };
}

// Compatibility API:
// - verify(id) verifies one record.
// - verify() verifies the complete registry.
function verify(id) {
  if (id !== undefined && id !== null) {
    return verifyRecord(id);
  }
  return verifyAll();
}

module.exports = {
  hashContent,
  validate,
  registerDerivative,
  verify,
  verifyAll,
  build,
  list
};
