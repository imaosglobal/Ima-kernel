"use strict";

const assert = require("assert");
const fs = require("fs");

const health = fs.readFileSync(".github/workflows/ima-continuous-health.yml", "utf8");
const pages = fs.readFileSync(".github/workflows/ima-ui-pages.yml", "utf8");
const canonicalPages = fs.readFileSync(".github/workflows/deploy-ima-pages.yml", "utf8");
const publicMonitor = fs.readFileSync(".github/workflows/ima-critical-public-monitor.yml", "utf8");
const unifiedWorkflow = fs.readFileSync(".github/workflows/ima-unified-loop.yml", "utf8");
const verify = fs.readFileSync("scripts/verify-ima.mjs", "utf8");
const coreTest = fs.readFileSync("tests/ima_core.test.cjs", "utf8");
const portableIdentity = fs.readFileSync("kernel/runtime/CANONICAL/IMA_PORTABLE_IDENTITY.js", "utf8");
const selfHealingDoc = fs.readFileSync("docs/IMA_SELF_HEALING_AND_AUTOMATED_REPAIR.md", "utf8");
const unifiedLoop = fs.readFileSync(".ima/loop/unified_loop.py", "utf8");

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

assert.ok(health.includes("IMA_LIVE_DEPLOYMENT_SMOKE=PASS"), "live deployment smoke test must remain enabled");
assert.ok(unifiedLoop.includes("IMA-UNIFIED-LOOP-1.4"), "canonical unified loop must be current");
assert.ok(unifiedLoop.includes("single_scheduler"), "canonical unified loop must remain the single scheduler");
assert.ok(pages.includes("VITE_IMA_API_BASE"), "Pages must publish the runtime API base");
assert.ok(pages.includes("name: github-pages-${{ github.run_id }}-${{ github.run_attempt }}"), "Pages artifact builder must use a unique run-attempt name");
assert.ok(canonicalPages.includes("name: ima-pages-${{ github.run_id }}-${{ github.run_attempt }}"), "canonical Pages upload must use a unique run-attempt name");
assert.ok(canonicalPages.includes("artifact_name: ima-pages-${{ github.run_id }}-${{ github.run_attempt }}"), "canonical Pages deploy must consume the unique run-attempt artifact");
assert.ok(canonicalPages.includes("types: [ima-canonical-deploy]"), "canonical Pages deploy must accept the unified-loop dispatch");
assert.ok(canonicalPages.includes("source_sha: ${{ steps.source.outputs.sha }}"), "canonical Pages artifact must be stamped from the checked-out canonical source SHA");
assert.ok(unifiedWorkflow.includes("ima-canonical-deploy"), "unified loop must request a canonical deployment after persisting state");
assert.ok(!publicMonitor.includes("raw.githubusercontent.com/imaosglobal/Ima-kernel/gh-pages/version.json"), "public monitor must never substitute branch metadata for public runtime evidence");
assert.ok(publicMonitor.includes("IMA_PUBLIC_INDEX_NORMAL_AND_CACHE_BUSTED=VERIFIED"), "public monitor must compare normal and cache-busted HTML paths");
assert.ok(!/^\\s*push:/m.test(publicMonitor), "public monitor must not run on pushes and race canonical deployment");
assert.ok(publicMonitor.includes('cron: "*/5 * * * *"'), "public monitor must retain its periodic schedule");
assert.ok(publicMonitor.includes("workflow_dispatch:"), "public monitor must remain manually runnable");
assert.ok(publicMonitor.includes("if: github.ref == 'refs/heads/main'"), "public runtime monitor must not compare a feature branch to production");
assert.ok(unifiedWorkflow.includes("branches: [main]"), "canonical unified orchestrator must run on main pushes only");
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
