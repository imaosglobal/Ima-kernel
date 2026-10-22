#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const required = [
  "docs/IMA_SYSTEM_TRUTH_AND_CAPABILITY_MAP.md",
  "docs/IMA_HUMAN_AGENCY_GATE.md",
  "docs/IMA_REVENUE_EVIDENCE_LOOP.md",
  "docs/IMA_DAILY_LOOP_CONTRACT.md",
  "docs/IMA_DEVELOPMENT_JOURNAL.md",
  "data/IMA_FINANCIAL_EVIDENCE_LEDGER.json",
  "kernel/runtime/CANONICAL/IMA_HUMAN_AGENCY_GATE.js",
  "kernel/runtime/CANONICAL/IMA_TRUTH_GATE.js",
  "kernel/runtime/CANONICAL/IMA_REVENUE_EVIDENCE.js"
];

const missing = required.filter(file => !fs.existsSync(path.join(root, file)));
const ledger = JSON.parse(fs.readFileSync(path.join(root, "data/IMA_FINANCIAL_EVIDENCE_LEDGER.json"), "utf8"));
const runtime = fs.readFileSync(path.join(root, "kernel/runtime/CANONICAL/IMA_RUNTIME.js"), "utf8");
const actionEngine = fs.readFileSync(path.join(root, "kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE.js"), "utf8");

const checks = {
  required_files: missing.length === 0,
  financial_ledger_valid: Array.isArray(ledger.events),
  runtime_truth_gate_wired: runtime.includes("IMA_TRUTH_GATE"),
  runtime_agency_gate_wired: runtime.includes("IMA_HUMAN_AGENCY_GATE"),
  runtime_revenue_evidence_wired: runtime.includes("IMA_REVENUE_EVIDENCE"),
  action_engine_agency_gate_wired: actionEngine.includes("IMA_HUMAN_AGENCY_GATE")
};

const result = {
  tool: "IMA Governance Audit",
  status: Object.values(checks).every(Boolean) && missing.length === 0 ? "VERIFIED" : "GAPS_RECORDED",
  checks,
  missing,
  ledger_events: ledger.events.length,
  rule: "No claim of live capability or received revenue without reproducible evidence."
};

console.log(JSON.stringify(result, null, 2));
if (result.status !== "VERIFIED") process.exitCode = 2;
