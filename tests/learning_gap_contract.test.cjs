const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root=process.cwd();
const protocol=fs.readFileSync(path.join(root,"docs/IMA_ETERNAL_LEARNING_PROTOCOL.md"),"utf8");
for (const marker of [
  "FIND GAPS","DISCOVER","LEARN","INFER","TEST","VERIFY","APPLY","TEACH","REVISE",
  "generations","private","provenance"
]) assert.ok(protocol.includes(marker),marker);

const registry=JSON.parse(fs.readFileSync(path.join(root,"integrations/IMA_LEARNING_GAPS.json"),"utf8"));
assert.equal(registry.schema,"IMA-LEARNING-GAPS-1.0");
assert.ok(registry.gap_types.includes("unknown"));
assert.ok(registry.gap_types.includes("technology_upgrade"));

const detector=fs.readFileSync(path.join(root,"learning/learning_gap_detector.py"),"utf8");
assert.ok(detector.includes("def detect"));
assert.ok(detector.includes("RESEARCHING"));
assert.ok(detector.includes("VERIFIED"));
assert.ok(detector.includes("TAUGHT"));

console.log("IMA_LEARNING_GAP_CONTRACT=PASS");
