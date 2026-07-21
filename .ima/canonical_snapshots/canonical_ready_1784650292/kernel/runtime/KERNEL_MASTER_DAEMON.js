const fs = require('fs');
const path = require('path');

const BUS = require('./KERNEL_EVENT_BUS');
const HEAL = require('./SELF_HEALING_COMPILER_V2');
const E2E = require('./KERNEL_E2E_LOCK');

// ─────────────────────────────
// STATE
// ─────────────────────────────

const STATE_FILE = './runtime/kernel_state.json';

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch { return {}; }
}

function save(s){
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

// ─────────────────────────────
// CORE LOOP
// ─────────────────────────────

function cycle(){

  const state = load();

  console.log('=== KERNEL CYCLE START ===');

  // 1. E2E CHECK
  const e2e = E2E.run();

  if (!e2e || e2e.status !== 'locked') {
    console.log('[DAEMON] SYSTEM NOT STABLE - HEALING PHASE');

    // ניסיון heal על runtime
    HEAL.audit('./runtime');

    return;
  }

  // 2. EVENT HEARTBEAT
  BUS.emit('HEARTBEAT', { time: Date.now() });

  // 3. SAFE SYNC MARK
  state.lastCycle = Date.now();
  state.status = 'healthy';

  save(state);

  console.log('=== KERNEL CYCLE OK ===');
}

// ─────────────────────────────
// DAEMON LOOP (persistent)
// ─────────────────────────────

function start(){

  console.log('[DAEMON] BOOTING MASTER KERNEL');

  setInterval(() => {
    try {
      cycle();
    } catch (e) {
      console.log('[DAEMON] CRASH RECOVER:', e.message);
    }
  }, 3000); // כל 3 שניות

}

module.exports = { start };
