const fs = require('fs');

const STATE_FILE = './runtime/kernel_state.json';

function load() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch { return {}; }
}

function save(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

function isStable() {
  const s = load();
  return s.e2e_locked === true && s.stability === 'stable';
}

function lockStable() {
  const s = load();
  s.e2e_locked = true;
  s.stability = 'stable';
  s.last_lock = Date.now();
  save(s);
  return s;
}

module.exports = { isStable, lockStable };
