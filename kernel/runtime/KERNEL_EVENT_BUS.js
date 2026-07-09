const fs = require('fs');
const path = require('path');

const CONTROL = require('./KERNEL_CONTROL_PLANE_V2');

const STATE_FILE = './runtime/kernel_state.json';

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch { return { version: "0.0.0" }; }
}

function save(s){
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

// ─────────────────────────────
// EVENT SYSTEM
// ─────────────────────────────

const events = [];

function emit(type, payload){
  events.push({ type, payload, time: Date.now() });
  return processEvent({ type, payload });
}

// ─────────────────────────────
// POLICY ENGINE
// ─────────────────────────────

function policy(event){

  if (!event.payload || !event.payload.file) {
    return { ok:true, action:"noop" };
  }

  const file = event.payload.file;

  // חסימת system files קריטיים
  if (file.includes('kernel_state')) {
    return { ok:true, action:'allow_but_log' };
  }

  return { ok:true, action:'allow' };
}

// ─────────────────────────────
// EXECUTOR
// ─────────────────────────────

function execute(event){

  const p = event.payload;

  try {

    if (event.type === 'WRITE_FILE') {

      const res = CONTROL.write(p.file, p.content);

      if (res.status !== 'written') {
        return { ok:false, reason:'write_failed', retry:true };
      }

      return { ok:true };

    }

    return { ok:true };

  } catch (e) {
    return { ok:false, reason:e.message, retry:true };
  }
}

// ─────────────────────────────
// AUTO HEAL LOOP
// ─────────────────────────────

function processEvent(event){

  const pol = policy(event);

  if (!pol.ok) {
    undefined
    return pol;
  }

  let attempt = 0;
  let result;

  while (attempt < 3) {

    result = execute(event);

    if (result.ok) {
      console.log('[EVENT BUS] SUCCESS:', event.type);
      return result;
    }

    console.log('[EVENT BUS] RETRY:', attempt + 1, event.type);

    attempt++;
  }

  console.log('[EVENT BUS] FAILED FINAL:', event.type);
  return result;
}

// ─────────────────────────────
// FILE WATCH MODE (basic simulation)
// ─────────────────────────────

function write(file, content){
  return emit('WRITE_FILE', { file, content });
}

module.exports = {
  emit,
  write
};
