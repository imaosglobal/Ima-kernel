import fs from "node:fs";

const registryPath = "docs/IMA_GLOBAL_INTEGRATION_REGISTRY.json";
const ledgerPath = "data/IMA_INTEGRATION_CONNECTION_LEDGER.json";

const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
const ledger = JSON.parse(fs.readFileSync(ledgerPath, "utf8"));

if (!Array.isArray(registry.priority_targets)) throw new Error("registry.priority_targets must be an array");
if (!Array.isArray(ledger.connections)) throw new Error("ledger.connections must be an array");

const allowed = new Set([
  "DISCOVERED","ELIGIBLE_PATH_FOUND","PREPARED","AUTHORIZED",
  "CONNECTED","VERIFIED","BLOCKED"
]);

for (const item of registry.priority_targets) {
  if (!item.name || !item.domain) throw new Error("priority target missing name/domain");
  if (item.status && !allowed.has(item.status)) throw new Error(`invalid status for ${item.name}`);
}

for (const c of ledger.connections) {
  if (!c.id || !c.target || !allowed.has(c.status)) throw new Error("invalid connection ledger record");
  if ((c.status === "CONNECTED" || c.status === "VERIFIED") && !c.evidence) {
    throw new Error(`connection ${c.id} lacks evidence`);
  }
}

console.log(JSON.stringify({
  ok: true,
  priority_targets: registry.priority_targets.length,
  recorded_connections: ledger.connections.length,
  verified_connections: ledger.connections.filter(x => x.status === "VERIFIED").length
}, null, 2));
