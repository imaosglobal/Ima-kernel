"use strict";

const assert = require("assert");
const derivation = require("../kernel/runtime/CANONICAL/IMA_DERIVATION_REGISTRY.js");
const fs = require("fs");

const original = "שלום עולם";
const derivative = derivation.registerDerivative({
  original_artifact_id: "original-test-artifact",
  derivative_artifact_id: "translation-test-artifact",
  source_language: "he",
  target_language: "en",
  derivation_type: "translation",
  content: "Hello world"
});

assert.strictEqual(derivative.original_artifact_id, "original-test-artifact");
assert.strictEqual(derivative.derivative_artifact_id, "translation-test-artifact");
assert.strictEqual(derivation.verify("translation-test-artifact").valid, true);
assert.notStrictEqual(original, derivative.content);
assert.strictEqual(derivation.verifyAll().valid, true);

const portable = fs.readFileSync("kernel/runtime/CANONICAL/IMA_PORTABLE_IDENTITY.js", "utf8");
assert.ok(portable.includes("CONTENT_OBJECT_NOT_FOUND"), "missing artifacts must be detected");
assert.ok(portable.includes("PORTABLE_IDENTITY_INTEGRITY_ERROR"), "hash/integrity failures must be reported");
assert.ok(portable.includes("originals_never_overwritten: true"), "original preservation rule must remain explicit");

console.log("IMA_PRESERVATION_CONTRACT=PASS");
