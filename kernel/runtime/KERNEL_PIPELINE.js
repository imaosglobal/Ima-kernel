const fs = require('fs');

const STATE_PATH = './runtime/kernel_state.json';

const queue = [];
let running = false;

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return { version: '0.0.0', sourceOfTruth: 'PIPELINE' };
  }
}

function commit(state) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function validate(event, state) {
  if (!event || !event.type) return { ok: false };
  if (state.sourceOfTruth !== 'PIPELINE') return { ok: false };
  return { ok: true };
}

function apply(event, state) {
  if (event.type === 'SET_VERSION') {
    state.version = event.version;
    state.activeVersion = event.version;
  }
  return state;
}

async function run() {
  if (running) return;
  running = true;

  while (queue.length) {
    const event = queue.shift();
    let state = load();

    const v = validate(event, state);
    if (!v.ok) continue;

    state = apply(event, state);
    commit(state);
  }

  running = false;
}

function dispatch(event) {
  queue.push(event);
  run();
}

module.exports = { dispatch };
