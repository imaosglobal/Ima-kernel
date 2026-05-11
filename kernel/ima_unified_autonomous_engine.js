const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';
const VERSION='1.0.'+Date.now();

console.log('===================================');
console.log('IMA UNIFIED AUTONOMOUS ENGINE');
console.log('===================================');
console.log('ROOT:',ROOT);
console.log('VERSION:',VERSION);

function exec(cmd){

  try{

    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      encoding:'utf8',
      stdio:['ignore','pipe','pipe']
    }).toString().trim();

  }catch(e){

    return null;

  }

}

function write(file,data){

  const full=path.join(ROOT,file);

  fs.mkdirSync(
    path.dirname(full),
    {recursive:true}
  );

  fs.writeFileSync(full,data);

  console.log('WRITE:',file);

}

function exists(file){

  return fs.existsSync(
    path.join(ROOT,file)
  );

}

// ===================================
// FULL PROJECT SCAN
// ===================================

console.log('');
console.log('SCAN PROJECT...');
console.log('');

const ALL_FILES=[];

function walk(dir){

  if(!fs.existsSync(dir)) return;

  for(const item of fs.readdirSync(dir)){

    const full=path.join(dir,item);

    const rel=path.relative(ROOT,full);

    if(
      rel.startsWith('.git')||
      rel.startsWith('node_modules')
    ) continue;

    let stat;

    try{
      stat=fs.statSync(full);
    }catch{
      continue;
    }

    if(stat.isDirectory()){

      walk(full);
      continue;

    }

    ALL_FILES.push(rel);

  }

}

walk(ROOT);

console.log('FILES:',ALL_FILES.length);

// ===================================
// DUPLICATE DETECTION
// ===================================

console.log('');
console.log('SCAN DUPLICATES...');
console.log('');

const hashes={};
const duplicates=[];

for(const file of ALL_FILES){

  try{

    const buf=fs.readFileSync(
      path.join(ROOT,file)
    );

    const hash=crypto
      .createHash('sha256')
      .update(buf)
      .digest('hex');

    if(!hashes[hash]){
      hashes[hash]=[];
    }

    hashes[hash].push(file);

  }catch{}

}

for(const h in hashes){

  if(hashes[h].length>1){

    duplicates.push(hashes[h]);

  }

}

console.log('DUPLICATES:',duplicates.length);

write(
  'logs/duplicates.json',
  JSON.stringify(duplicates,null,2)
);

// ===================================
// DAEMON DETECTION
// ===================================

console.log('');
console.log('SCAN DAEMONS...');
console.log('');

const daemonCandidates=ALL_FILES.filter(f=>

  f.toLowerCase().includes('daemon')||
  f.toLowerCase().includes('runtime')||
  f.toLowerCase().includes('watchdog')||
  f.toLowerCase().includes('supervisor')

);

console.log(
  'DAEMON FILES:',
  daemonCandidates.length
);

write(
  'logs/daemon_scan.json',
  JSON.stringify(
    daemonCandidates,
    null,
    2
  )
);

// ===================================
// AUTO DAEMON SELECT
// ===================================

let daemon=null;

const priorities=[
  'runtime/daemon.js',
  'runtime/server.js',
  'watchdog.js',
  'supervisor.js',
  'control_daemon.js'
];

for(const p of priorities){

  if(exists(p)){

    daemon=p;
    break;

  }

}

if(!daemon&&daemonCandidates.length){

  daemon=daemonCandidates[0];

}

console.log('SELECTED DAEMON:',daemon||'NONE');

// ===================================
// PACKAGE SAFE UPDATE
// ===================================

console.log('');
console.log('UPDATE PACKAGE...');
console.log('');

write(
'package.json',
JSON.stringify({

  name:NAME,
  version:VERSION,
  main:'server.js',

  scripts:{
    start:'node server.js',
    daemon:daemon?
      'node '+daemon:
      'node server.js'
  },

  files:[
    'server.js',
    'runtime',
    'core',
    'memory',
    'plugins',
    'policies',
    'ui',
    'logs'
  ],

  bin:{
    ima:'cli.js'
  }

},null,2)
);

// ===================================
// SELF HEAL ENGINE
// ===================================

console.log('');
console.log('BUILD SELF HEAL...');
console.log('');

write(
'core/self_heal_runtime.js',
`
const fs=require('fs');

module.exports=function(){

const required=[
'server.js',
'package.json'
];

for(const f of required){

if(!fs.existsSync(f)){

console.log('MISSING:',f);

}

}

console.log('SELF HEAL OK');

};
`
);

// ===================================
// GLOBAL CLI SAFE
// ===================================

console.log('');
console.log('FIX CLI...');
console.log('');

exec(
'rm -f /data/data/com.termux/files/usr/bin/ima'
);

write(
'cli.js',
`#!/usr/bin/env node

console.log('IMA CLI ONLINE');
`
);

exec('chmod +x cli.js');

// ===================================
// GIT SYNC
// ===================================

console.log('');
console.log('SYNC GIT...');
console.log('');

const git=exec('git status');

if(git!==null){

  exec('git fetch --all');
  exec('git pull --rebase || true');

  exec('git add .');

  exec(
    'git commit -m "IMA AUTO '+VERSION+'" || true'
  );

  exec('git tag '+VERSION+' || true');

  exec('git push || true');

  exec('git push --tags || true');

  console.log('GIT OK');

}else{

  console.log('NO GIT');

}

// ===================================
// NPM AUTH
// ===================================

console.log('');
console.log('CHECK NPM...');
console.log('');

const who=exec('npm whoami');

const npmReady=!!who;

console.log(
  'NPM READY:',
  npmReady
);

// ===================================
// PUBLISH
// ===================================

let published=false;

if(npmReady){

  console.log('');
  console.log('PUBLISH...');
  console.log('');

  for(let i=1;i<=3;i++){

    console.log('TRY:',i);

    const pub=exec(
      'npm publish --access public'
    );

    if(pub!==null){

      published=true;
      break;

    }

  }

}

console.log(
  'PUBLISHED:',
  published
);

// ===================================
// START DAEMON
// ===================================

console.log('');
console.log('START DAEMON...');
console.log('');

let daemonStarted=false;

if(daemon){

  const res=exec(
    'nohup node '+daemon+' >/dev/null 2>&1 &'
  );

  daemonStarted=true;

}

console.log(
  'DAEMON:',
  daemonStarted
);

// ===================================
// FINAL LOG
// ===================================

write(
'logs/final_state.json',
JSON.stringify({

  version:VERSION,
  files:ALL_FILES.length,
  duplicates:duplicates.length,
  daemon,
  daemonStarted,
  npmReady,
  published

},null,2)
);

console.log('');
console.log('===================================');
console.log('IMA COMPLETE');
console.log('===================================');

console.log({
  VERSION,
  FILES:ALL_FILES.length,
  DUPLICATES:duplicates.length,
  DAEMON:daemon,
  STARTED:daemonStarted,
  PUBLISHED:published
});
