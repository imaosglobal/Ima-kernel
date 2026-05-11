process.chdir(__dirname);

const fs = require('fs');

const CORE = {
  control: './ima_control_plane_v5',
  update: './ima_update_guard',
  release: './ima_release_guard',
  dep: './ima_dependency_guard',
  runtime: './ima_unified_runtime',
  sync: './ima_unified_sync',
  network: './ima_network_layer',
  events: './ima_events',
  reactive: './ima_reactive',
  ui: './ima_ui_core',
  brain: './ima_brain_hub',
  lock: './ima_brain_lock'
};

// ---------- SAFE LOAD ----------
function load(name, path) {
  try {
    const mod = require(path);
    return { ok: true, mod };
  } catch (e) {
    return { ok: false, mod: null, err: e.message };
  }
}

// ---------- ENGINE ----------
function doctor() {
  console.log('======================');
  console.log('[IMA CORE DOCTOR]');
  console.log('======================');

  const report = {};

  for (const [k, path] of Object.entries(CORE)) {
    const res = load(k, path);
    report[k] = res.ok;

    console.log(res.ok ? `[OK] ${k}` : `[MISSING] ${k}`);
  }

  const failed = Object.entries(report).filter(([_, v]) => !v);

  console.log('======================');
  console.log('STATUS:', failed.length ? 'DEGRADED' : 'CLEAN');
  console.log('MISSING:', failed.map(f => f[0]));
  console.log('======================');

  return report;
}

function run() {
  console.log('======================');
  console.log('[IMA CORE ENGINE RUN]');
  console.log('======================');

  const user = 'test@ima.ai';

  const runtime = load('runtime', CORE.runtime).mod;
  const sync = load('sync', CORE.sync).mod;
  const brain = load('brain', CORE.brain).mod;
  const ui = load('ui', CORE.ui).mod;
  const lock = load('lock', CORE.lock).mod;

  // DEP
  const dep = load('dep', CORE.dep).mod;
  if (dep?.assert) dep.assert();

  // UPDATE / RELEASE (safe)
  const update = load('update', CORE.update).mod;
  const release = load('release', CORE.release).mod;

  update?.update?.();

  // BRAIN
  const boot = brain?.boot?.('google', { email: user }, 'watch');

  // UI
  if (ui?.login) ui.login('google', { email: user }, 'watch');
  if (ui?.subscribe) ui.subscribe(user, s => console.log('[UI]', s?.device));
  if (ui?.move) ui.move(user, 'mobile');

  // LOCK
  const l = lock?.lock?.(user);
  const v = lock?.verify?.(user);

  // RELEASE
  release?.release?.();

  console.log('======================');
  console.log('[FINAL SNAPSHOT]');
  console.log({
    brain: boot || null,
    ui: ui?.snapshot?.(user),
    sync: sync?.snapshot?.(user),
    lock: { ok: v?.ok, ts: l?.ts }
  });

  console.log('======================');
  console.log('[ENGINE DONE]');
  console.log('======================');
}

module.exports = { run, doctor };
