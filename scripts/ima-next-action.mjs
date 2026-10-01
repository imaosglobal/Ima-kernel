#!/usr/bin/env node
/**
 * IMA Next Action Tool
 * Read-only, deterministic capability audit. It never performs external actions.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const registryPath = path.join(root, 'docs/IMA_CAPABILITY_REGISTRY.json');
const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const rank = { NOT_VERIFIED: 0, PLANNED: 1, IMPLEMENTED: 2, TESTED: 3, VERIFIED: 4, LIVE: 5, DISABLED: 6 };
const unresolved = registry.capabilities
  .filter(x => ['NOT_VERIFIED', 'PLANNED', 'IMPLEMENTED'].includes(x.status))
  .sort((a, b) => rank[a.status] - rank[b.status] || a.id.localeCompare(b.id));
const rows = unresolved.map((x, i) => ({
  priority: i + 1,
  id: x.id,
  status: x.status,
  next_step: x.status === 'IMPLEMENTED'
    ? 'Run reproducible test and verify deployed surface before changing status.'
    : x.status === 'PLANNED'
      ? 'Implement the smallest safe slice, add a reproducible test, then verify deployment.'
      : 'Inspect the current implementation; define a bounded test and deployment evidence before claiming availability.',
  boundary: x.boundary
}));
const report = {
  tool: 'IMA Next Action',
  mode: 'read-only; no purchases, messages, account changes, or deployments',
  generated_at: new Date().toISOString(),
  registry_version: registry.schema_version,
  unresolved_count: rows.length,
  next_actions: rows
};
console.log(JSON.stringify(report, null, 2));
if (process.argv.includes('--strict') && unresolved.length) process.exitCode = 2;
