'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const file = path.join(__dirname, '..', 'docs', 'IMA_CAPABILITY_REGISTRY.json');
const registry = JSON.parse(fs.readFileSync(file, 'utf8'));
const allowed = new Set(['LIVE','VERIFIED','TESTED','IMPLEMENTED','PLANNED','NOT_VERIFIED','DISABLED']);
assert.equal(registry.product, 'IMA');
assert.ok(Array.isArray(registry.capabilities) && registry.capabilities.length > 0);
const ids = new Set();
for (const item of registry.capabilities) {
  assert.ok(item.id && !ids.has(item.id), 'capability IDs must be unique');
  ids.add(item.id);
  assert.ok(allowed.has(item.status), 'unknown status: ' + item.status);
  assert.ok(item.label && item.boundary, 'each capability needs a clear boundary');
  if (item.status === 'LIVE' || item.status === 'VERIFIED') {
    assert.ok(item.evidence?.length, item.id + ' requires evidence');
    assert.ok(item.deployment_verified === true, item.id + ' requires deployment verification');
    assert.ok(item.test_verified === true, item.id + ' requires test verification');
  }
}
assert.equal(registry.capabilities.find(x => x.id === 'store_payments').status, 'DISABLED');
assert.equal(registry.policy.consequential_actions_require_explicit_user_confirmation, true);

const ui = fs.readFileSync(path.join(__dirname, '..', 'ima-ui', 'src', 'App.jsx'), 'utf8');
assert.match(ui, /import capabilityRegistry from '\.\.\/\.\.\/docs\/IMA_CAPABILITY_REGISTRY\.json'/, 'UI must consume the canonical registry');
assert.match(ui, /capabilityRegistry\.capabilities\.map/, 'UI must render registry capabilities');
assert.match(ui, /לא אומת/, 'UI must communicate verification boundaries in Hebrew');

const { spawnSync } = require('node:child_process');
const audit = spawnSync(process.execPath, [path.join(__dirname, '..', 'scripts', 'ima-next-action.mjs')], { encoding: 'utf8' });
assert.equal(audit.status, 0, 'IMA Next Action CLI must exit successfully: ' + audit.stderr);
const report = JSON.parse(audit.stdout);
assert.equal(report.tool, 'IMA Next Action');
assert.ok(Array.isArray(report.next_actions));
assert.equal(report.unresolved_count, report.next_actions.length);
assert.ok(report.next_actions.every((x, i) => x.priority === i + 1 && x.id && x.next_step && x.boundary));
console.log('IMA capability registry + Next Action CLI: PASS (' + registry.capabilities.length + ' capabilities; ' + report.unresolved_count + ' queued actions; UI wired)');
