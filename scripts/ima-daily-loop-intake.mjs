import fs from "node:fs";

const inputs = [
  "docs/IMA_DAILY_LOOP_INTEGRATION_PROTOCOL.md",
  "docs/IMA_GLOBAL_INTEGRATION_REGISTRY.json",
  "data/IMA_INTEGRATION_CONNECTION_LEDGER.json"
];
for (const p of inputs) if (!fs.existsSync(p)) throw new Error("Missing canonical input: " + p);

const registry = JSON.parse(fs.readFileSync(inputs[1], "utf8"));
const ledger = JSON.parse(fs.readFileSync(inputs[2], "utf8"));
const active = ledger.connections.filter(x => ["AUTHORIZED","CONNECTED","VERIFIED"].includes(x.status));

const report = {
  generated_at: new Date().toISOString(),
  canonical_loop: "IMA Global Health Loop — לולאת התפתחות מאוחדת",
  integration_targets: registry.priority_targets.length,
  authorized_or_connected_records: active.length,
  next_cycle_inputs: [
    "new_verified_integrations",
    "new_verified_capabilities",
    "new_verified_revenue_evidence",
    "new_verified_safety_or_governance_changes",
    "new_verified_research_and_learning"
  ],
  second_daily_orchestrator: false
};

fs.mkdirSync(".ima/loop", { recursive: true });
fs.writeFileSync(".ima/loop/daily_intake.json", JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify(report, null, 2));
