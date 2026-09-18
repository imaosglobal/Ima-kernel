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

function verify(id) {
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

module.exports = {
  hashContent,
  validate,
  registerDerivative,
  verify,
  list
};
