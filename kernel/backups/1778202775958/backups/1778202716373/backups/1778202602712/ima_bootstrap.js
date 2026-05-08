process.chdir(__dirname);

function req(name, path){
  try {
    const m = require(path);
    console.log('[OK]', name);
    return m;
  } catch(e){
    console.log('[FATAL]', name, '->', e.message);
    process.exit(1);
  }
}

console.log('======================');
console.log('[IMA BOOTSTRAP]');
console.log('======================');

// חובה
const dep = req('dep','./ima_dependency_guard');
const runtime = req('runtime','./ima_unified_runtime');
const sync = req('sync','./ima_unified_sync');
const network = req('network','./ima_network_layer');
const events = req('events','./ima_events');
const reactive = req('reactive','./ima_reactive');

// שכבת אפליקציה (חובה לנעילה מלאה)
const ui = req('ui','./ima_ui_core');
const brain = req('brain','./ima_brain_hub');
const lock = req('lock','./ima_brain_lock');

// אופציונלי (לא מפיל)
let control = null;
try {
  control = require('./ima_control_plane_v5');
  console.log('[OK] control');
} catch {
  console.log('[WARN] control missing (ignored)');
}

// שלב 1 – dependency
dep.assert();

// שלב 2 – update (אם קיים)
try { require('./ima_update_guard').update(); } catch {}

// שלב 3 – boot
const user = 'test@ima.ai';

const boot = brain.boot('google',{email:user},'watch');

ui.login('google',{email:user},'watch');
ui.subscribe(user, s => console.log('[UI]', s?.device));
ui.move(user,'mobile');

// שלב 4 – lock
const l = lock.lock(user);
const v = lock.verify(user);

// שלב 5 – control (אם קיים)
if (control?.runAll) control.runAll();

// שלב 6 – release (אם קיים)
try { require('./ima_release_guard').release(); } catch {}

// final
console.log('======================');
console.log('[SYSTEM READY]');
console.log({
  brain: boot,
  ui: ui.snapshot(user),
  sync: sync.snapshot(user),
  lock: { ok: v.ok, ts: l.ts }
});
console.log('======================');
