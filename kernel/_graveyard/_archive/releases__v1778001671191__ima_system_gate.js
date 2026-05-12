const cp = require('child_process');

function run(cmd){
  try {
    return { ok: true, out: cp.execSync(cmd, {encoding:'utf8'}).toString() };
  } catch (e){
    return { ok: false, err: e.message };
  }
}

function checkModule(name){
  try {
    require.resolve(name);
    return true;
  } catch {
    return false;
  }
}

function runGate(){

  console.log('[GATE] START');

  // 1. modules
  const modules = [
    './ima_identity',
    './ima_unified_sync',
    './ima_network_layer',
    './ima_platform_bridge',
    './ima_unified_runtime'
  ];

  for (const m of modules){
    if(!checkModule(m)){
      console.log('[FAIL] missing module:', m);
      process.exit(1);
    }
  }

  console.log('[OK] modules');

  // 2. runtime test
  try {
    const rt = require('./ima_unified_runtime');
    const b = rt.boot('google',{email:'gate@test.ai'},'watch');
    if(!b || !b.user) throw new Error('boot failed');

    const m = rt.move('gate@test.ai','mobile');
    if(!m) throw new Error('move failed');

    console.log('[OK] runtime');
  } catch (e){
    console.log('[FAIL] runtime', e.message);
    process.exit(1);
  }

  // 3. sync test
  try {
    const s = require('./ima_unified_sync');
    s.set('gate','test','ok');
    const snap = s.snapshot('gate');
    if(!snap) throw new Error('sync broken');
    console.log('[OK] sync');
  } catch (e){
    console.log('[FAIL] sync', e.message);
    process.exit(1);
  }

  // 4. git clean check
  const git = run('git status --porcelain');
  if(git.out.trim().length > 0){
    console.log('[FAIL] git not clean');
    process.exit(1);
  }

  console.log('[OK] git clean');

  // 5. final success
  console.log('======================');
  console.log('[GATE PASSED]');
  console.log('======================');

  return true;
}

module.exports = { runGate };
