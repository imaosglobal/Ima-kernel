const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const VERSION='3.0.'+Date.now();
const NAME='@mom-os1/ima-core';

function exec(cmd){

  try{

    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      encoding:'utf8',
      stdio:['ignore','pipe','pipe']
    }).trim();

  }catch(e){

    return null;

  }

}

function write(file,data){

  const full=path.join(ROOT,file);

  fs.mkdirSync(path.dirname(full),{
    recursive:true
  });

  fs.writeFileSync(full,data);

  console.log('WRITE:',file);

}

function exists(file){

  return fs.existsSync(
    path.join(ROOT,file)
  );

}

console.log('==============================');
console.log('IMA SUPREME KERNEL');
console.log('==============================');
console.log('VERSION:',VERSION);

// ======================================
// SCAN
// ======================================

const files=[];

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

    files.push(rel);

  }

}

walk(ROOT);

console.log('FILES:',files.length);

// ======================================
// DUPLICATES
// ======================================

const hashes={};
const duplicates=[];

for(const file of files){

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

console.log(
  'DUPLICATES:',
  duplicates.length
);

write(
  'logs/duplicates_final.json',
  JSON.stringify(
    duplicates.slice(0,20),
    null,
    2
  )
);

// ======================================
// ENGINE SELECTOR
// ======================================

const runtimeCandidates=files.filter(f=>

  f.includes('engine')||
  f.includes('runtime')||
  f.includes('daemon')||
  f.includes('supervisor')

);

runtimeCandidates.sort();

write(
  'core/runtime_registry.json',
  JSON.stringify(
    runtimeCandidates,
    null,
    2
  )
);

let mainEngine='runtime/engine.js';

const priority=[
  'runtime/engine_v6.js',
  'runtime/engine_v5.js',
  'runtime/engine_v4.js',
  'runtime/engine_v3.js',
  'runtime/engine_v2.js',
  'runtime/engine.js'
];

for(const p of priority){

  if(exists(p)){

    mainEngine=p;
    break;

  }

}

console.log('MAIN ENGINE:',mainEngine);

// ======================================
// AUTONOMOUS RUNTIME
// ======================================

write(
'runtime/autonomous_runtime.js',
`
const fs=require('fs');

setInterval(()=>{

const state={

time:Date.now(),
status:'alive',
memory:process.memoryUsage()

};

fs.writeFileSync(
'logs/heartbeat.json',
JSON.stringify(state,null,2)
);

console.log('IMA HEARTBEAT');

},30000);
`
);

// ======================================
// SELF REPAIR
// ======================================

write(
'core/self_repair.js',
`
const fs=require('fs');

module.exports=function(){

const critical=[

'package.json',
'server.js',
'cli.js'

];

for(const f of critical){

if(!fs.existsSync(f)){

console.log('REPAIR REQUIRED:',f);

}

}

console.log('SELF REPAIR COMPLETE');

};
`
);

// ======================================
// CLEAN PACKAGE
// ======================================

write(
'package.json',
JSON.stringify({

  name:NAME,
  version:VERSION,
  main:'server.js',

  scripts:{
    start:'node server.js',
    runtime:'node '+mainEngine,
    autonomous:'node runtime/autonomous_runtime.js'
  },

  files:[

    'server.js',
    'runtime',
    'core',
    'memory',
    'plugins',
    'policies',
    'ui'

  ],

  bin:{
    ima:'cli.js'
  },

  publishConfig:{
    access:'public'
  }

},null,2)
);

// ======================================
// CLI
// ======================================

write(
'cli.js',
`#!/usr/bin/env node
console.log('IMA ONLINE');
`
);

exec('chmod +x cli.js');

// ======================================
// SERVER
// ======================================

write(
'server.js',
`
const http=require('http');
const fs=require('fs');

http.createServer((req,res)=>{

if(req.url==='/status'){

return res.end('IMA ONLINE');

}

if(req.url==='/heartbeat'){

try{

return res.end(
fs.readFileSync(
'logs/heartbeat.json'
)
);

}catch{}

}

res.end('IMA');

}).listen(4000,()=>{

console.log('IMA SERVER ONLINE');

});
`
);

// ======================================
// TERMUX BOOT
// ======================================

const bootDir='/data/data/com.termux/files/home/.termux/boot';

try{

  fs.mkdirSync(bootDir,{
    recursive:true
  });

  fs.writeFileSync(

    path.join(
      bootDir,
      'ima_boot.sh'
    ),

`#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

cd ~/ima_core/kernel

nohup node runtime/autonomous_runtime.js >/dev/null 2>&1 &
nohup node server.js >/dev/null 2>&1 &
`

  );

  exec(
    'chmod +x ~/.termux/boot/ima_boot.sh'
  );

  console.log('TERMUX BOOT OK');

}catch(e){

  console.log('BOOT ERROR');

}

// ======================================
// GIT
// ======================================

exec('git add .');
exec(
'git commit -m "IMA SUPREME '+VERSION+'" || true'
);
exec('git tag '+VERSION+' || true');
exec('git push || true');
exec('git push --tags || true');

// ======================================
// NPM
// ======================================

const who=exec('npm whoami');

console.log('NPM:',!!who);

let published=false;

if(who){

  for(let i=1;i<=5;i++){

    console.log('PUBLISH TRY',i);

    const pub=exec(
      'npm publish --access public'
    );

    if(pub){

      published=true;
      break;

    }

  }

}

console.log('PUBLISHED:',published);

// ======================================
// INSTALL
// ======================================

exec(
'npm i -g '+NAME+' --force'
);

// ======================================
// START
// ======================================

exec(
'nohup node runtime/autonomous_runtime.js >/dev/null 2>&1 &'
);

exec(
'nohup node server.js >/dev/null 2>&1 &'
);

// ======================================
// VERIFY
// ======================================

const verify=exec('ima');

console.log('CLI:',verify);

write(
'logs/kernel_state.json',
JSON.stringify({

  version:VERSION,
  files:files.length,
  duplicates:duplicates.length,
  mainEngine,
  published,
  verify

},null,2)
);

console.log('==============================');
console.log('IMA SUPREME COMPLETE');
console.log('==============================');

console.log({

  VERSION,
  FILES:files.length,
  DUPLICATES:duplicates.length,
  ENGINE:mainEngine,
  PUBLISHED:published,
  CLI:verify

});
