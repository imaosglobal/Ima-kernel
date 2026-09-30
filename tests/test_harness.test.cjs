"use strict";

const assert = require("assert");
const fs = require("fs");

const health = fs.readFileSync(".github/workflows/ima-continuous-health.yml", "utf8");
const pages = fs.readFileSync(".github/workflows/ima-ui-pages.yml", "utf8");
const coreTest = fs.readFileSync("tests/ima_core.test.cjs", "utf8");

for (const required of [
  "npm test",
  "ima:integrity",
  "ima:runtime",
  "python -m unittest tests/public_runtime.test.py",
  "npm run lint",
  "npm run build"
]) {
  assert.ok(health.includes(required), `continuous health missing: ${required}`);
}

assert.ok(health.includes("schedule:"), "continuous health must remain scheduled");
assert.ok(health.includes("IMA_LIVE_DEPLOYMENT_SMOKE=PASS"), "live deployment smoke test must remain enabled");
assert.ok(health.includes('cron: "17 */6 * * *"'), "continuous health cadence changed unexpectedly");
assert.ok(pages.includes("VITE_IMA_API_BASE"), "Pages must publish the runtime API base");
assert.ok(pages.includes("artifact_name: github-pages-"), "Pages artifact must remain uniquely named");
assert.ok(coreTest.includes("IMA_CORE_TEST=PASS"), "core test must have a deterministic success marker");

console.log("IMA_TEST_HARNESS=PASS");
