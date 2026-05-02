
// ======================
// IMA CI ENGINE v1
// deterministic deploy pipeline
// ======================

const { execSync } = require('child_process');

function run(cmd, allowFail=false) {
  try {
    return execSync(cmd, { stdio: 'inherit' });
  } catch (e) {
    if (!allowFail) throw e;
    console.log('[WARN]', cmd, e.message);
  }
}

function gitClean() {
  const out = execSync('git status --porcelain', { encoding: 'utf8' });
  return out.trim().length === 0;
}

function versionBump(pkg) {
  let [a,b,c] = pkg.version.split('.').map(Number);
  return `${a}.${b}.${c+1}`;
}

function loadPkg() {
  return require('./package.json');
}

function savePkg(pkg) {
  fs.writeFileSync('./package.json', JSON.stringify(pkg, null, 2));
}


const { sync } = require('./ima_git_sync');
const { npmPublish } = require('./ima_npm_publish');

function deploy
    ({ publish=true } = {}) {

  console.log('======================');
  console.log('[IMA CI v1 DEPLOY]');
  console.log('======================');

  const pkg = loadPkg();

  const next = versionBump(pkg);
  pkg.version = next;

  console.log('[VERSION]', next);

  run('git add -A');
  run(`git commit -m "ci: deploy ${next}" || true`);
  run('git push origin main');

  if (!gitClean()) {
    throw new Error('Git not clean after commit');
  }

  if (process.env.IMA_NO_PUBLISH === '1') {
    console.log('[NPM] skipped by env');
  } else if (publish) {
    run('npm publish', true);
  }

  savePkg(pkg);

  console.log('======================');
  console.log('[DEPLOY COMPLETE]');
  console.log('======================');
}

module.exports = { deploy };
