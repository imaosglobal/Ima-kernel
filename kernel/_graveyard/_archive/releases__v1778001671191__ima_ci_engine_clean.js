
function gitSyncSafe(){
  const { execSync } = require('child_process');
  try {
    console.log('[GIT] stash');
    execSync('git stash --include-untracked || true', {stdio:'inherit'});

    console.log('[GIT] pull');
    execSync('undefined

    console.log('[GIT] restore');
    execSync('git stash pop || true', {stdio:'inherit'});
  } catch(e){
    console.log('[GIT] sync warning:', e.message);
  }
}


function npmPreflight(){
  const { execSync } = require('child_process');
  try {
    execSync('npm whoami', {stdio:'ignore'});
    console.log('[NPM] authenticated');
    return true;
  } catch(e){
    console.log('[NPM] not logged in → skipping publish');
    return false;
  }
}

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
    sh('    console.log('[NPM] published');
  } catch (e) {
    console.log('[NPM] publish failed');
  }
}

/* =========================
   DEPLOY PIPELINE
========================= */
function deploy(){ gitSyncSafe(); const npmOk = npmPreflight(); this._npmOk = npmOk;{
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
