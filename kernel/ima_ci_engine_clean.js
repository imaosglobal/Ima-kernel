const { execSync } = require('child_process');

function sh(cmd){
  return execSync(cmd, { stdio: 'inherit' });
}

function safe(cmd){
  try {
    return execSync(cmd, { encoding: 'utf8' });
  } catch {
    return null;
  }
}

/* =========================
   GIT LAYER
========================= */
function gitOk(){
  const out = safe('git status --porcelain');
  return !out || out.trim().length === 0;
}

function gitSync(){
  if (!gitOk()) {
    console.log('[GIT] committing changes...');
    sh('git add -A');
    sh('git commit -m "auto deploy sync" || true');
  }
  sh('git push origin main');
}

/* =========================
   VERSION LAYER
========================= */
function bumpVersion(){
  const pkg = require('./package.json');
  const parts = pkg.version.split('.').map(Number);
  parts[2]++;

  const next = parts.join('.');
  pkg.version = next;

  const fs = require('fs');
  fs.writeFileSync('./package.json', JSON.stringify(pkg, null, 2));

  console.log('[VERSION]', next);
  return next;
}

/* =========================
   NPM LAYER (SAFE)
========================= */
function npmReady(){
  try {
    safe('npm whoami');
    return true;
  } catch {
    return false;
  }
}

function npmPublish(){
  if (process.env.IMA_SKIP_NPM === '1') {
    console.log('[NPM] skipped by env');
    return;
  }

  if (!npmReady()) {
    console.log('[NPM] not authenticated → skipping');
    return;
  }

  try {
    sh('npm publish');
    console.log('[NPM] published');
  } catch (e) {
    console.log('[NPM] publish failed');
  }
}

/* =========================
   DEPLOY PIPELINE
========================= */
function deploy(){
  console.log('======================');
  console.log('[IMA CI CLEAN DEPLOY]');
  console.log('======================');

  const v = bumpVersion();

  gitSync();

  npmPublish();

  console.log('======================');
  console.log('[DEPLOY COMPLETE]', v);
  console.log('======================');
}

module.exports = { deploy };
