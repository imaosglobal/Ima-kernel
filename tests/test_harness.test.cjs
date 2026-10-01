"use strict";

const assert = require("assert");
const fs = require("fs");

const health = fs.readFileSync(".github/workflows/ima-continuous-health.yml", "utf8");
const pages = fs.readFileSync(".github/workflows/ima-ui-pages.yml", "utf8");
const verify = fs.readFileSync("scripts/verify-ima.mjs", "utf8");
const coreTest = fs.readFileSync("tests/ima_core.test.cjs", "utf8");
const portableIdentity = fs.readFileSync("kernel/runtime/CANONICAL/IMA_PORTABLE_IDENTITY.js", "utf8");
const selfHealingDoc = fs.readFileSync("docs/IMA_SELF_HEALING_AND_AUTOMATED_REPAIR.md", "utf8");

assert.ok(health.includes("npm run ima:verify"), "continuous health must invoke the canonical verification runner");
for (const required of [
  '["core", ["npm", "test"]]',
  '["integrity", ["npm", "run", "ima:integrity"]]',
  '["runtime", ["npm", "run", "ima:runtime"]]',
  '["public-runtime", ["python", "-c"',
  '["contract-harness", ["node", "tests/test_harness.test.cjs"]]'
]) {
  assert.ok(verify.includes(required), `verification runner missing required test: ${required}`);
}

for (const required of ["npm ci", "npm run lint", "npm run build"]) {
  assert.ok(health.includes(required), `continuous health missing frontend step: ${required}`);
}

assert.ok(health.includes("schedule:"), "continuous health must remain scheduled");
assert.ok(health.includes("IMA_LIVE_DEPLOYMENT_SMOKE=PASS"), "live deployment smoke test must remain enabled");
assert.ok(health.includes('cron: "17 */6 * * *"'), "continuous health cadence changed unexpectedly");
assert.ok(pages.includes("VITE_IMA_API_BASE"), "Pages must publish the runtime API base");
assert.ok(pages.includes("artifact_name: github-pages-"), "Pages artifact must remain uniquely named");
assert.ok(coreTest.includes("IMA_CORE_TEST=PASS"), "core test must have a deterministic success marker");

for (const required of [
  "function ensureContinuityDirectory()",
  "function writeEmptyContinuityState()",
  "CONTINUITY_SEEDS_NOT_FOUND",
  "CONTENT_OBJECT_NOT_FOUND",
  "bootstrapped"
]) {
  assert.ok(portableIdentity.includes(required), `self-healing runtime missing: ${required}`);
}

for (const required of [
  "DETECT -> DIAGNOSE -> CLASSIFY -> REPAIR -> TEST -> VERIFY -> REPORT -> OBSERVE",
  "never fabricate facts or content",
  "hash mismatch remains an integrity error"
]) {
  assert.ok(selfHealingDoc.includes(required), `self-healing contract missing: ${required}`);
}

console.log("IMA_TEST_HARNESS=PASS");
