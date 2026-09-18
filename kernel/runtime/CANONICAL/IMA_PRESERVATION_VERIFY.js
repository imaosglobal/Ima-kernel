"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function sha256File(file) {
  return crypto
    .createHash("sha256")
    .update(fs.readFileSync(file))
    .digest("hex");
}

function verifyArtifact(record, root) {
  if (!record || !record.content_file) {
    return {
      status: "UNAVAILABLE",
      reason: "content_file_missing"
    };
  }

  const file = path.resolve(root, record.content_file);

  if (!fs.existsSync(file)) {
    return {
      status: "UNAVAILABLE",
      reason: "content_not_found",
      file
    };
  }

  const actual = sha256File(file);
  const expected = record.sha256 || record.hash || null;

  if (!expected) {
    return {
      status: "NO_EXPECTED_HASH",
      actual
    };
  }

  return {
    status: actual === expected ? "VERIFIED" : "MISMATCH",
    expected,
    actual,
    file
  };
}

function verifyRegistry(registry, root) {
  const records = Array.isArray(registry)
    ? registry
    : registry?.artifacts || [];

  return records.map(record => ({
    artifact_id: record.artifact_id || record.id || null,
    ...verifyArtifact(record, root)
  }));
}

module.exports = {
  sha256File,
  verifyArtifact,
  verifyRegistry
};
