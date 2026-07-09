
// ======================
// IMA DEPLOY ENGINE v3 (STABLE)
// ======================

const { execSync } = require('child_process');

function safe(cmd) {
  try {
    return execSync(cmd, { stdio: 'inherit' });
  } catch (e) {
    console.log('[SAFE FAIL]', cmd, e.message);
    return null;
  }
}

function getVersion() {
  const pkg = require('./package.json');
  return pkg.version;
}

function bumpVersion(v) {
  let [a,b,c] = v.split('.').map(Number);
  c++;
  return `${a}.${b}.${c}`;
}

function publishGuard() {
  if (process.env.IMA_NO_PUBLISH === '1') {
    console.log('[NPM] publish blocked by env');
    return false;
  }
  return true;
}

function deploy() {
  console.log('======================');
  console.log('[IMA DEPLOY ENGINE v3]');
  console.log('======================');

  const version = getVersion();
  const next = bumpVersion(version);

  console.log('[VERSION]', version, '→', next);

  safe('git status --porcelain');

  safe('git add -A');
  safe(`git commit -m "auto deploy ${next}" || true`);

  safe('git push origin main');

  if (publishGuard()) {
    safe('npm publish');
  }

  console.log('======================');
  console.log('[DEPLOY COMPLETE]');
  console.log('======================');
}

module.exports = { deploy };
