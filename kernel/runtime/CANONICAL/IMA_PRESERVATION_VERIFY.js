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

// Backward-compatible runtime API.
// IMA_RUNTIME calls preservationVerify.verify() during boot.
//
// The canonical preservation registry is the source of artifact records.
// Verification recomputes SHA-256 from the actual content bytes and
// compares it with each recorded expected hash.
function verify() {
  const root = path.resolve(__dirname, "../../../..");
  const registryModule = require("./IMA_PRESERVATION_REGISTRY");

  let registry = [];

  if (typeof registryModule.get === "function") {
    registry = registryModule.get();
  } else if (typeof registryModule.list === "function") {
    registry = registryModule.list();
  } else if (typeof registryModule.status === "function") {
    const status = registryModule.status();
    registry = status?.artifacts || status?.records || [];
  } else if (Array.isArray(registryModule)) {
    registry = registryModule;
  } else if (Array.isArray(registryModule.artifacts)) {
    registry = registryModule.artifacts;
  } else if (Array.isArray(registryModule.records)) {
    registry = registryModule.records;
  }

  const results = verifyRegistry(registry, root);
  const verified = results.filter(r => r.status === "VERIFIED").length;
  const mismatched = results.filter(r => r.status === "MISMATCH").length;
  const unavailable = results.filter(r => r.status === "UNAVAILABLE").length;
  const noExpectedHash = results.filter(r => r.status === "NO_EXPECTED_HASH").length;

  return {
    valid: mismatched === 0 && unavailable === 0 && noExpectedHash === 0,
    total: results.length,
    verified,
    mismatched,
    unavailable,
    no_expected_hash: noExpectedHash,
    results
  };
}

module.exports = {
  sha256File,
  verifyArtifact,
  verifyRegistry,
  verify
};
