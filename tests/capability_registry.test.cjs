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
console.log('IMA capability registry contract: PASS (' + registry.capabilities.length + ' capabilities)');
