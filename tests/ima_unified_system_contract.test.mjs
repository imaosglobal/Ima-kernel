import assert from 'node:assert/strict';
import fs from 'node:fs';

const app = fs.readFileSync('ima-ui/src/App.jsx', 'utf8');
const chat = fs.readFileSync('ima-ui/src/services/imaChat.js', 'utf8');
const bus = fs.readFileSync('ima-ui/src/services/imaLearningBus.js', 'utf8');

assert.match(app, /imaLearningBus/);
assert.match(app, /observeIma/);
assert.match(app, /recordImaPreference/);
assert.match(app, /deriveImaAdaptations/);
assert.match(chat, /imaLearningBus/);
assert.match(chat, /observeIma/);
assert.match(bus, /BUS_KEY = 'ima-unified-learning-bus-v1'/);
assert.match(bus, /MAX_EVENTS = 120/);
assert.doesNotMatch(bus, /deploy|publish|spend|contact/i);

console.log('IMA_UNIFIED_SYSTEM_CONTRACT=PASS');
const contract = JSON.parse(fs.readFileSync('IMA_SYSTEM_UNIFIED_CONTRACT.json', 'utf8'));
assert.deepEqual(contract.priority_order.map(x => x.id), [
  'human_agency_truth_safety',
  'production_reliability',
  'canonical_unification',
  'memory_learning_feedback',
  'universal_action_core',
  'continuity_interoperability_preservation',
  'sustainable_growth_and_revenue',
  'frontier_research_and_creation'
]);
assert.match(fs.readFileSync('scripts/ima-next-action.mjs', 'utf8'), /priorityOrder/);
