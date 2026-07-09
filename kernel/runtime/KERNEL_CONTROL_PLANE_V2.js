const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const STATE_FILE = './runtime/kernel_state.json';
const SNAP_DIR = './runtime/.control_snapshots';

fs.mkdirSync(SNAP_DIR, { recursive: true });

// ─────────────────────────────
// KEEP ORIGINAL FS (CRITICAL FIX)
// ─────────────────────────────
const nativeWrite = fs.writeFileSync;
const nativeRead = fs.readFileSync;

function loadState(){
  try { return JSON.parse(nativeRead(STATE_FILE,'utf8')); }
  catch { return { version: "0.0.0" }; }
}

function saveState(s){
  nativeWrite(STATE_FILE, JSON.stringify(s,null,2));
}

function hash(c){
  return crypto.createHash('sha256').update(c).digest('hex');
}

function snapshot(file, content){
  const id = path.basename(file) + '.' + Date.now() + '.bak';
  const p = path.join(SNAP_DIR, id);
  nativeWrite(p, content);
  return p;
}

function validate(file, content){
  if (file.endsWith('.js')) {
    try { new Function(content); }
    catch (e) {
      return { ok:false, reason:'syntax_error', error:e.message };
    }
  }
  return { ok:true };
}

// ─────────────────────────────
// SAFE WRITE PIPELINE
// ─────────────────────────────
function write(filePath, content){

  const state = loadState();

  if (fs.existsSync(filePath)) {
    snapshot(filePath, nativeRead(filePath,'utf8'));
  }

  const result = validate(filePath, content);

  if (!result.ok) {
    console.log('[CONTROL PLANE] BLOCKED:', filePath, result.reason);

    return { status:'rejected', reason:result.reason };
  }

  // IMPORTANT: use native write ONLY
  nativeWrite(filePath, content);

  state.lastWrite = {
    file: filePath,
    time: Date.now(),
    hash: hash(content)
  };

  saveState(state);

  console.log('[CONTROL PLANE] WROTE:', filePath);

  return { status:'written', file:filePath };
}

// ─────────────────────────────
// GLOBAL HOOK (SAFE NOW)
// ─────────────────────────────
function installGlobalHook(){

  fs.writeFileSync = function(file, data, ...args){
    return write(file, data);
  };

  console.log('[CONTROL PLANE] GLOBAL HOOK INSTALLED');
}

module.exports = {
  write,
  installGlobalHook
};
