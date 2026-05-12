const { execSync } = require("child_process");
const { analyzeChanges } = require("./decision_engine");

function run() {
  const d = analyzeChanges();

  if (d.shouldRestart) {
    console.log("[AUTO] restart");
    safeExec("ima restart", { stdio: "inherit" });
  }

  if (d.shouldPush) {
    console.log("[AUTO] git push");
    safeExec("git add . && git commit -m 'auto sync' && git push", {
      stdio: "inherit"
    });
  }

  if (d.shouldRelease) {
    console.log("[AUTO] version bump");
    safeExec("npm version patch --no-git-tag-version", { stdio: "inherit" });
  }

  return d;
}

module.exports = { run };

const { decideProductDirection } = require("./product_brain");

function productLayer() {
  const d = decideProductDirection();

  console.log("[PRODUCT BRAIN]", d);

  if (d.recommendation === "build_feature") {
    console.log("[PRODUCT] HIGH PRIORITY FEATURE DETECTED");
  }
}

module.exports.productLayer = productLayer;

const { planExecution } = require("./execution_brain");

function executionLayer() {
  const plan = planExecution();

  if (plan.length > 0) {
    console.log("[EXECUTION PLAN]");
    plan.forEach(p => console.log("-", p.action, "→", p.target));
  }
}

module.exports.executionLayer = executionLayer;

const { generateCodeFromPlan } = require("./code_writer");

function codeLayer() {
  const files = generateCodeFromPlan();

  if (files.length > 0) {
    console.log("[CODE WRITER]");
    files.forEach(f => console.log("generated:", f));
  }
}

module.exports.codeLayer = codeLayer;

const { safetyCheck } = require("./safety_brain");

function safetyLayer() {
  const results = safetyCheck();

  const failed = results.filter(r => !r.ok);

  if (failed.length > 0) {
    console.log("[SAFETY] issues detected:", failed.length);
    console.log("[SAFETY] blocking auto release");
    return { blocked: true };
  }

  console.log("[SAFETY] all checks passed");
  return { blocked: false };
}

module.exports.safetyLayer = safetyLayer;

// FIX: safer shell execution for Termux
const { execSync } = require("child_process");

function safeExec(cmd) {
  try {
    return safeExec(cmd, {
      shell: "/data/data/com.termux/files/usr/bin/bash",
      encoding: "utf-8",
      stdio: "pipe"
    });
  } catch (e) {
    console.log("[SAFE EXEC ERROR]", e.message);
    return null;
  }
}

module.exports.safeExec = safeExec;
