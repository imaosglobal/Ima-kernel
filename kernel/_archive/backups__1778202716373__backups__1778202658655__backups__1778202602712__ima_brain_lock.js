const brain = require('./ima_brain_hub');

const store = {};

function lock(userId){
  const state = brain.get(userId);
  const entry = {
    ts: Date.now(),
    userId,
    state
  };
  store[userId] = entry;
  return entry;
}

function verify(userId){
  const saved = store[userId];
  const current = brain.get(userId);

  const ok = JSON.stringify(saved?.state) === JSON.stringify(current);

  return {
    ok,
    saved,
    current
  };
}

module.exports = { lock, verify };
