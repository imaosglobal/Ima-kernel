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