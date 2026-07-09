const fs = require('fs');

const STATE = './runtime/kernel_state.json';

let queue = [];
let running = false;

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE));
  } catch {
    return {
      version: '0.0.0',
      sourceOfTruth: 'PIPELINE',
      locked: false
    };
  }
}

function commit(s) {
  s.sourceOfTruth = 'PIPELINE';
  s.locked = true;
  fs.writeFileSync(STATE, JSON.stringify(s, null, 2));
}

function blockExternalWrites(state) {
  // אם מישהו אחר נגע → דריסה חזרה ל-pipeline
  if (state.sourceOfTruth !== 'PIPELINE') {
    state.sourceOfTruth = 'PIPELINE';
    state.locked = true;
  }
  return state;
}

function apply(event, state) {
  if (event.type === 'SET_VERSION') {
    state.version = event.version;
    state.activeVersion = event.version;
    state.lastWrite = Date.now();
  }

  return state;
}

async function run() {
  if (running) return;
  running = true;

  while (queue.length) {
    const event = queue.shift();
    let state = load();

    state = blockExternalWrites(state);
    state = apply(event, state);

    commit(state);
  }

  running = false;
}

function dispatch(event) {
  queue.push(event);
  run();
}

// 🔒 מנגנון “single writer enforcement”
function assertSingleWriter() {
  const state = load();

  if (state.sourceOfTruth !== 'PIPELINE') {
    state.sourceOfTruth = 'PIPELINE';
    commit(state);
  }

  return true;
}

module.exports = {
  dispatch,
  assertSingleWriter
};
