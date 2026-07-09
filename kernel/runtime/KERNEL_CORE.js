const fs = require('fs');

const STATE_PATH = './runtime/kernel_state.json';

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return {
      version: '0.0.0',
      sourceOfTruth: 'PIPELINE',
      locked: true
    };
  }
}

function commit(state) {
  state.sourceOfTruth = 'PIPELINE';
  state.locked = true;
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function setVersion(version) {
  const state = load();
  state.version = version;
  state.activeVersion = version;
  state.lastUpdate = Date.now();
  commit(state);
  return state;
}

function read() {
  return load();
}

module.exports = {
  setVersion,
  read
};
