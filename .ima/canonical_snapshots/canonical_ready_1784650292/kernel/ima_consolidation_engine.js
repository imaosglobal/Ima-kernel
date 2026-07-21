const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';
const VERSION='2.0.'+Date.now();

console.log('====================================');
console.log('IMA CONSOLIDATION ENGINE');
console.log('====================================');
console.log('ROOT:',ROOT);
console.log('VERSION:',VERSION);

// =====================================
// SAFE EXEC
// =====================================

function exec(cmd,inherit=false){

  try{

    const out=cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      encoding:'utf8',
      stdio:inherit?'inherit':['ignore','pipe','pipe']
    });

    return inherit?true:out.toString().trim();

  }catch(e){

    return null;

  }

}

// =====================================
// WRITE
// =====================================

function write(file,data){

  const full=path.join(ROOT,file);

  fs.mkdirSync(
    path.dirname(full),
    {recursive:true}
  );

  fs.writeFileSync(full,data);

  console.log('WRITE:',file);

}

// =====================================
// EXISTS
// =====================================

function exists(file){

  return fs.existsSync(
    path.join(ROOT,file)
  );

}

// =====================================
// PROJECT SCAN
// =====================================

console.log('');
console.log('SCAN PROJECT...');
console.log('');

const SKIP=[
'.git',
'node_modules'
];

const FILES=[];

function walk(dir){

  if(!fs.existsSync(dir)) return;

  for(const item of fs.readdirSync(dir)){

    const full=path.join(dir,item);

    const rel=path.relative(ROOT,full);

    if(
      SKIP.some(s=>rel.startsWith(s))
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

    FILES.push(rel);

  }

}

walk(ROOT);

console.log('FILES:',FILES.length);

// =====================================
// DUPLICATE SCAN
// =====================================

console.log('');
console.log('SCAN DUPLICATES...');
console.log('');

const HASHES={};
const DUPS=[];

for(const file of FILES){

  try{

    const hash=crypto
      .createHash('sha256')
      .update(
        fs.readFileSync(
          path.join(ROOT,file)
        )
      )
      .digest('hex');

    if(!HASHES[hash]){
      HASHES[hash]=[];
    }

    HASHES[hash].push(file);

  }catch{}

}

for(const h in HASHES){

  if(HASHES[h].length>1){

    DUPS.push(HASHES[h]);

  }

}

console.log('DUPLICATES:',DUPS.length);

write(
'logs/duplicates_before_cleanup.json',
JSON.stringify(DUPS,null,2)
);

// =====================================
// CLEAN DUPLICATES
// =====================================

console.log('');
console.log('CLEAN DUPLICATES...');
console.log('');

fs.mkdirSync('_archive',{
  recursive:true
});

let removed=0;

for(const group of DUPS){

  const keep=group[0];

  for(let i=1;i<group.length;i++){

    const file=group[i];

    if(
      file.includes('release')||
      file.includes('backup')||
      file.includes('snapshot')||
      file.includes('_archive')
    ){

      const src=path.join(ROOT,file);

      const dest=path.join(
        ROOT,
        '_archive',
        file.replace(/[\/]/g,'__')
      );

      try{

        fs.mkdirSync(
          path.dirname(dest),
          {recursive:true}
        );

        fs.renameSync(src,dest);

        removed++;

      }catch{}

    }

  }

}

console.log('ARCHIVED:',removed);

// =====================================
// CORE REGISTRY
// =====================================

console.log('');
console.log('BUILD CORE REGISTRY...');
console.log('');

const REGISTRY={

  runtime:null,
  daemon:null,
  ui:null,
  memory:null,
  brain:null

};

const runtimePriority=[
'ima_unified_runtime.js',
'runtime/server.js',
'runtime.js'
];

const daemonPriority=[
'control_daemon.js',
'watchdog.js',
'supervisor.js'
];

const memoryPriority=[
'memory_engine.js',
'ima_memory.js',
'memory.js'
];

const uiPriority=[
'ima_ui_core.js',
'ui/index.html'
];

const brainPriority=[
'ima_agi_core.js',
'brain.js',
'decision_engine.js'
];

function select(priority){

  for(const p of priority){

    if(exists(p)){

      return p;

    }

  }

  return null;

}

REGISTRY.runtime=select(runtimePriority);
REGISTRY.daemon=select(daemonPriority);
REGISTRY.memory=select(memoryPriority);
REGISTRY.ui=select(uiPriority);
REGISTRY.brain=select(brainPriority);

write(
'core_registry.json',
JSON.stringify(REGISTRY,null,2)
);

console.log(REGISTRY);

// =====================================
// PACKAGE CLEAN
// =====================================

console.log('');
console.log('BUILD PACKAGE...');
console.log('');

write(
'package.json',
JSON.stringify({

  name:NAME,
  version:VERSION,
  main:'server.js',

  scripts:{
    start:'node server.js',
    daemon:REGISTRY.daemon?
      'node '+REGISTRY.daemon:
      'node server.js'
  },

  files:[
    'server.js',
    'core',
    'runtime',
    'memory',
    'plugins',
    'ui',
    'policies',
    'logs',
    'core_registry.json'
  ],

  publishConfig:{
    access:'public'
  },

  bin:{
    ima:'cli.js'
  }

},null,2)
);

// =====================================
// CLI
// =====================================

write(
'cli.js',
`#!/usr/bin/env node

console.log('IMA CLI ONLINE');

`
);

exec('chmod +x cli.js');

// =====================================
// VERIFY NPM AUTH
// =====================================

console.log('');
console.log('VERIFY NPM...');
console.log('');

let who=exec('npm whoami');

if(!who){

  console.log('');
  console.log('OPENING LOGIN...');
  console.log('');

  exec(
    'npm login --auth-type=web',
    true
  );

  who=exec('npm whoami');

}

const npmReady=!!who;

console.log('NPM USER:',who||'NONE');

if(!npmReady){

  console.log('NPM AUTH FAILED');
  process.exit(1);

}

// =====================================
// GIT SYNC
// =====================================

console.log('');
console.log('SYNC GIT...');
console.log('');

exec('git fetch --all',true);
exec('git pull --rebase || true',true);

exec('git add .',true);

exec(
'git commit -m "IMA CONSOLIDATED '+VERSION+'" || true',
true
);

exec(
'git tag '+VERSION+' || true',
true
);

exec('git push || true',true);
exec('git push --tags || true',true);

// =====================================
// PUBLISH VERIFIED
// =====================================

console.log('');
console.log('PUBLISH...');
console.log('');

let published=false;

for(let i=1;i<=5;i++){

  console.log('TRY:',i);

  exec(
    'npm publish --access public',
    true
  );

  const check=exec(
    'npm view '+NAME+' version'
  );

  if(
    check &&
    check.includes(VERSION)
  ){

    published=true;
    break;

  }

  exec('sleep 3',true);

}

if(!published){

  console.log('');
  console.log('PUBLISH FAILED');
  console.log('');
  process.exit(1);

}

// =====================================
// GLOBAL INSTALL
// =====================================

console.log('');
console.log('INSTALL GLOBAL...');
console.log('');

exec(
'rm -f /data/data/com.termux/files/usr/bin/ima',
true
);

exec(
'npm i -g '+NAME+' --force',
true
);

// =====================================
// START DAEMON
// =====================================

console.log('');
console.log('START DAEMON...');
console.log('');

if(REGISTRY.daemon){

  exec(
    'nohup node '+REGISTRY.daemon+' >/dev/null 2>&1 &',
    true
  );

}

// =====================================
// VERIFY CLI
// =====================================

console.log('');
console.log('VERIFY CLI...');
console.log('');

exec('ima',true);

// =====================================
// FINAL STATE
// =====================================

write(
'logs/final_state.json',
JSON.stringify({

  version:VERSION,
  files:FILES.length,
  duplicatesBefore:DUPS.length,
  archived:removed,
  registry:REGISTRY,
  npmUser:who,
  published

},null,2)
);

console.log('');
console.log('====================================');
console.log('IMA CONSOLIDATION COMPLETE');
console.log('====================================');

console.log({
  VERSION,
  FILES:FILES.length,
  DUPLICATES_BEFORE:DUPS.length,
  ARCHIVED:removed,
  PUBLISHED:published
});
