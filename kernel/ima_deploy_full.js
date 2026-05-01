const { execSync } = require("child_process");

// ===== VERSION RESOLVER (TOP LEVEL SAFE) =====


function getPublishedVersions(){
  try {
    const out = execSync('npm view ima-core-saas versions --json', {encoding:'utf8'});
    return JSON.parse(out || '[]');
  } catch {
    return [];
  }
}

function nextVersion(base, used){
  let [a,b,c] = base.split('.').map(Number);
  while (used.includes(`${a}.${b}.${c}`)) c++;
  return `${a}.${b}.${c}`;
}

function resolveVersion(current){
  return nextVersion(current, getPublishedVersions());
}
// =========================================


const fs = require('fs');

function sh(cmd){
  try {
    execSync(cmd, { stdio: 'inherit' });
    return true;
  } catch(e){
    console.log('[WARN]', cmd);
    return false;
  }
}

console.log('======================');
console.log('[IMA FULL DEPLOY]');

// 0. ensure clean git BEFORE anything
try {
  require('child_process').execSync('git add -A', {stdio:'inherit'});
  require('child_process').execSync('git commit -m "pre-deploy clean" || true', {stdio:'inherit'});
} catch {}


// 1. bootstrap test
if (!sh('node ima_bootstrap.js')) {
  console.log('[STOP] bootstrap failed');
  process.exit(1);
}

// 2. read version
const pkg = JSON.parse(fs.readFileSync('package.json'));
const oldVersion = pkg.version;

// 3. bump version (patch)
const parts = oldVersion.split('.').map(Number);
parts[2]++;
const base = parts.join('.');
const newVersion = resolveVersion(base);

pkg.version = newVersion;
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));

console.log('[VERSION]', oldVersion, '→', newVersion);

if (!canPublish(newVersion)) {
  console.log('[BLOCKED] version already exists on npm');
  process.exit(0);
}

// 4. git commit
sh('git add .');
sh(`git commit -m "auto deploy v${newVersion}"`);

// 5. npm publish (safe)
const publishOk = sh('npm publish');

// אם נכשל → החזר גרסה
if (!publishOk) {
  console.log('[ROLLBACK VERSION]');
  pkg.version = oldVersion;
  fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
}

// 6. git push
sh('git push origin main');

console.log('======================');
console.log('[DEPLOY COMPLETE]');
console.log('======================');


// NPM_VERSION_CHECK
function canPublish(version){
  try {
    const res = require('child_process')
      .execSync('npm view ima-core-saas versions --json', {encoding:'utf8'});
    const versions = JSON.parse(res || '[]');
    return !versions.includes(version);
  } catch(e){
    return true; // אם אין גישה → נניח שמותר
  }
}


function resolveVersion(current){
  const used = getPublishedVersions();
  return nextVersion(current, used);
}
