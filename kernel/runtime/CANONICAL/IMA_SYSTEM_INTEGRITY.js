"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../..");

const required = [
  "IMA_CORE_CONTRACT.js",
  "IMA_POLICY.js",
  "IMA_RUNTIME.js",
  "IMA_CONTINUITY.js",
  "IMA_PRESERVATION_VERIFY.js",
  "IMA_DERIVATION_REGISTRY.js",
  "memory/IMA_MEMORY.js",
  "gateway/IMA_MODEL_GATEWAY.js",
  "gateway/IMA_TOOL_GATEWAY.js",
  "gateway/IMA_AGENT_GATEWAY.js",
  "orchestration/IMA_ACTION_ENGINE.js"
];

const missing = required.filter(file =>
  !fs.existsSync(path.join(__dirname, file))
);

const result = {
  valid: missing.length === 0,
  canonical_root: __dirname,
  missing
};

console.log(JSON.stringify(result, null, 2));

if (!result.valid) process.exit(1);
