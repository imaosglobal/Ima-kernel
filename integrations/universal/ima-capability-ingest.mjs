#!/usr/bin/env node
/**
 * IMA Universal Capability Ingestor
 *
 * Imports a capability descriptor into an evidence-preserving record.
 * This intentionally does not execute third-party code or grant permissions.
 *
 * Usage:
 * node integrations/universal/ima-capability-ingest.mjs descriptor.json
 */
import fs from "node:fs";

const input = process.argv[2];
if (!input) {
  console.error("Usage: node integrations/universal/ima-capability-ingest.mjs <descriptor.json>");
  process.exit(2);
}

const raw = fs.readFileSync(input, "utf8");
const descriptor = JSON.parse(raw);

const required = ["identity", "interface", "authority", "safety"];
const missing = required.filter((key) => descriptor[key] === undefined);
if (missing.length) {
  console.error(JSON.stringify({ ok:false, error:"missing_required_sections", missing }, null, 2));
  process.exit(1);
}

const record = {
  ima_record_type: "capability_evidence",
  recorded_at: new Date().toISOString(),
  source: descriptor.source ?? null,
  identity: descriptor.identity,
  interface: descriptor.interface,
  authority: descriptor.authority,
  safety: descriptor.safety,
  evidence: descriptor.evidence ?? [],
  validation: descriptor.validation ?? { status:"unverified" },
  limitations: descriptor.limitations ?? [],
  privacy: descriptor.privacy ?? { data_minimization:true },
  rule: "Imported knowledge never grants authority to act."
};

console.log(JSON.stringify({ ok:true, record }, null, 2));
