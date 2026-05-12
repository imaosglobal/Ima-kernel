const fs = require('fs');
const path = require('path');

const BUS = require('./KERNEL_EVENT_BUS');
const HEAL = require('./SELF_HEALING_COMPILER_V2');
const CONTROL = require('./KERNEL_CONTROL_PLANE_V2');

const STATE_FILE = './runtime/kernel_state.json';

// ─────────────────────────────
// LOAD STATE
// ─────────────────────────────

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch { return {}; }
}

function save(s){
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

// ─────────────────────────────
// INBOUND TEST
// ─────────────────────────────

function inboundTest(){

  const files = fs.readdirSync('./runtime');

  for (const f of files) {
    if (!f.endsWith('.js')) continue;

    const c = fs.readFileSync('./runtime/' + f, 'utf8');

    try {
      new Function(c);
    } catch (e) {
      console.log('[E2E] INBOUND FAIL:', f);
      return false;
    }
  }

  console.log('[E2E] INBOUND OK');
  return true;
}

// ─────────────────────────────
// OUTBOUND TEST
// ─────────────────────────────

function outboundTest(){

  const res = BUS.write('./runtime/e2e_test.js','console.log("e2e ok")');

  if (!res || res.status === 'failed_unrecoverable') {
    console.log('[E2E] OUTBOUND FAIL');
    return false;
  }

  console.log('[E2E] OUTBOUND OK');
  return true;
}

// ─────────────────────────────
// ROUNDTRIP TEST
// ─────────────────────────────

function roundTrip(){

  const file = './runtime/e2e_roundtrip.js';

  BUS.write(file,'console.log("roundtrip")');

  const c = fs.readFileSync(file,'utf8');

  try {
    new Function(c);
  } catch {
    console.log('[E2E] ROUNDTRIP FAIL');
    return false;
  }

  console.log('[E2E] ROUNDTRIP OK');
  return true;
}

// ─────────────────────────────
// FINAL LOCK
// ─────────────────────────────

function lockSystem(){

  const state = load();

  state.locked = true;
  state.lockedAt = Date.now();

  state.policy = {
    writeGuard: true,
    e2eRequired: true,
    autoHeal: true
  };

  save(state);

  console.log('========================');
  console.log('[E2E] SYSTEM LOCKED');
  console.log('========================');
}

// ─────────────────────────────
// RUN FULL PIPELINE
// ─────────────────────────────

function run(){

  console.log('=== E2E VERIFY START ===');

  const a = inboundTest();
  const b = outboundTest();
  const c = roundTrip();

  if (a && b && c) {
    lockSystem();
    return { status:'locked' };
  }

  console.log('[E2E] NOT READY');
  return { status:'failed' };
}

module.exports = {
  run
};
