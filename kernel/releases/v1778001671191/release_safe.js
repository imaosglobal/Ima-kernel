const fs = require('fs');
const cp = require('child_process');

function sh(cmd){
  try { return cp.execSync(cmd,{stdio:'inherit'}); }
  catch(e){ console.log('[SKIP]', cmd); }
}

console.log('=== IMA SAFE RELEASE SYSTEM ===');

// 1. ensure directories exist (FIX CRITICAL BUG)
if(!fs.existsSync('./releases')){
  fs.mkdirSync('./releases');
}

const version = 'v' + Date.now();
const snapshotPath = './releases/' + version;

fs.mkdirSync(snapshotPath);

// 2. snapshot files
fs.readdirSync('.')
  .filter(f => f.endsWith('.js') || f.endsWith('.json'))
  .forEach(f => {
    try {
      fs.copyFileSync(f, snapshotPath + '/' + f);
    } catch(e){}
  });

// 3. manifest
const manifest = {
  version,
  time: Date.now(),
  files: fs.readdirSync('.'),
  snapshot: snapshotPath
};

fs.writeFileSync(snapshotPath + '/manifest.json', JSON.stringify(manifest,null,2));

// 4. git safe sync
sh('git add .');
sh('git commit -m "IMA SAFE RELEASE ' + version + '" || true');
sh('git tag ' + version + ' || true');
sh('git push || true');

// 5. npm safe bump only
sh('npm version patch --no-git-tag-version || true');

// 6. kernel validation
let ok = false;

try {
  const k = require('./ima_kernel.js');
  ok =
    k &&
    typeof k.run === 'function' &&
    typeof k.update === 'function';
} catch(e){
  ok = false;
}

console.log('--- RESULT ---');
console.log('VERSION:', version);
console.log('STABLE:', ok);

if(ok){
  console.log('[OK] RELEASE STORED');
} else {
  console.log('[WARN] RELEASE STORED BUT CHECK KERNEL');
}

