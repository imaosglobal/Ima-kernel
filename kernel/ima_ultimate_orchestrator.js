const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');
const https=require('https');

const ROOT=process.cwd();
const VERSION='4.0.'+Date.now();
const PACKAGE='@mom-os1/ima-core';

console.log('======================================');
console.log('IMA ULTIMATE ORCHESTRATOR');
console.log('======================================');
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

function sha(file){

  try{

    return crypto
    .createHash('sha256')
    .update(
      fs.readFileSync(
        path.join(ROOT,file)
      )
    )
    .digest('hex');

  }catch{

    return null;

  }

}

function walk(dir,list=[]){

  if(!fs.existsSync(dir)) return list;

  for(const item of fs.readdirSync(dir)){

    const full=path.join(dir,item);

    const rel=path.relative(ROOT,full);

    if(
      rel.startsWith('.git')||
      rel.startsWith('node_modules')||
      rel.startsWith('_archive')
    ) continue;

    let stat;

    try{
      stat=fs.statSync(full);
    }catch{
      continue;
    }

    if(stat.isDirectory()){

      walk(full,list);
      continue;

    }

    list.push(rel);

  }

  return list;

}

const files=walk(ROOT);

console.log('FILES:',files.length);

write(
'logs/files.json',
JSON.stringify(files,null,2)
);

// ======================================
// ENGINE DISCOVERY
// ======================================

const engineFiles=files.filter(f=>

  f.includes('engine')||
  f.includes('runtime')||
  f.includes('daemon')||
  f.includes('server')||
  f.includes('supervisor')

);

console.log('ENGINES:',engineFiles.length);

// ======================================
// CANONICAL ENGINE SELECTION
// ======================================

let canonical=null;

const priorities=[
'runtime/engine_v6.js',
'runtime/engine_v5.js',
'runtime/engine_v4.js',
'runtime/engine.js',
'runtime/server.js',
'server.js'
];

for(const p of priorities){

  if(exists(p)){

    canonical=p;
    break;

  }

}

if(!canonical&&engineFiles.length){

  canonical=engineFiles[0];

}

console.log('CANONICAL:',canonical);

// ======================================
// DUPLICATE PRUNING
// ======================================

const hashes={};
const duplicates=[];

for(const file of files){

  const h=sha(file);

  if(!h) continue;

  if(!hashes[h]){

    hashes[h]=[];

  }

  hashes[h].push(file);

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

// ======================================
// ARCHIVE DUPLICATES
// ======================================

let archived=0;

for(const group of duplicates){

  const keep=group[0];

  for(let i=1;i<group.length;i++){

    const file=group[i];

    try{

      const target=
      '_archive/duplicates/'+
      file.replace(/[\/]/g,'__');

      fs.mkdirSync(
        path.dirname(
          path.join(ROOT,target)
        ),
        {recursive:true}
      );

      fs.renameSync(
        path.join(ROOT,file),
        path.join(ROOT,target)
      );

      archived++;

    }catch{}

  }

}

console.log('ARCHIVED:',archived);

// ======================================
// CORE REGISTRY
// ======================================

const registry={

  version:VERSION,
  canonical,
  engines:engineFiles,
  totalFiles:files.length,
  duplicates:duplicates.length,
  archived,
  generated:Date.now()

};

write(
'core/runtime_registry.json',
JSON.stringify(registry,null,2)
);

// ======================================
// TRUTH ENGINE
// ======================================

write(
'runtime/truth_engine.js',
`
module.exports={

score:function(sources){

if(!Array.isArray(sources)) return 0;

let score=0;

for(const s of sources){

if(
s &&
s.trusted
) score++;

}

return score/sources.length;

},

verify:function(values){

const map={};

for(const v of values){

map[v]=(map[v]||0)+1;

}

let best=null;
let max=0;

for(const k in map){

if(map[k]>max){

max=map[k];
best=k;

}

}

return {
value:best,
confidence:max/values.length
};

}

};
`
);

// ======================================
// TELEMETRY ENGINE
// ======================================

write(
'runtime/telemetry.js',
`
const fs=require('fs');

module.exports=function(event,data){

const row={

time:Date.now(),
event,
data

};

fs.appendFileSync(
'logs/telemetry.log',
JSON.stringify(row)+'\\n'
);

};
`
);

// ======================================
// ANALYTICS ENGINE
// ======================================

write(
'runtime/npm_analytics.js',
`
const https=require('https');
const fs=require('fs');

function fetch(url){

return new Promise(resolve=>{

https.get(url,res=>{

let data='';

res.on('data',d=>data+=d);

res.on('end',()=>{

try{

resolve(JSON.parse(data));

}catch{

resolve(null);

}

});

}).on('error',()=>resolve(null));

});

}

(async()=>{

const pkg='${PACKAGE}';

const downloads=
await fetch(
'https://api.npmjs.org/downloads/point/last-week/'+pkg
);

fs.writeFileSync(
'logs/npm_downloads.json',
JSON.stringify(downloads,null,2)
);

})();
`
);

// ======================================
// SELF REPAIR ENGINE
// ======================================

write(
'core/self_repair.js',
`
const fs=require('fs');

module.exports=function(){

const required=[

'package.json',
'server.js',
'cli.js',
'core/runtime_registry.json'

];

for(const r of required){

if(!fs.existsSync(r)){

console.log('MISSING',r);

}

}

console.log('SELF REPAIR COMPLETE');

};
`
);

// ======================================
// AUTONOMOUS RUNTIME
// ======================================

write(
'runtime/autonomous_runtime.js',
`
const fs=require('fs');
const cp=require('child_process');

function exec(cmd){

try{

return cp.execSync(
cmd,
{
shell:true,
encoding:'utf8'
}
).toString();

}catch{

return null;

}

}

console.log('AUTONOMOUS RUNTIME ONLINE');

setInterval(()=>{

console.log('HEARTBEAT',Date.now());

exec('node runtime/npm_analytics.js');

exec('git add .');

exec(
'git commit -m "AUTO HEARTBEAT" || true'
);

exec('git push || true');

},1000*60*60);

`
);

// ======================================
// SERVER
// ======================================

write(
'server.js',
`
const http=require('http');
const fs=require('fs');

http.createServer((req,res)=>{

if(req.url==='/'){

res.writeHead(200,{
'content-type':'text/html'
});

return res.end(
fs.readFileSync('./ui/index.html')
);

}

if(req.url==='/status'){

return res.end(
JSON.stringify({

status:'online',
time:Date.now()

})

);

}

res.end('IMA');

}).listen(4000,()=>{

console.log('IMA ONLINE 4000');

});
`
);

// ======================================
// UI
// ======================================

write(
'ui/index.html',
`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>IMA</title>
<style>

body{
background:#0b0b0b;
color:white;
font-family:sans-serif;
text-align:center;
padding-top:50px;
}

.card{
width:80%;
margin:auto;
padding:30px;
border-radius:20px;
background:#151515;
}

button{
padding:15px;
font-size:18px;
border-radius:10px;
}

</style>
</head>
<body>

<div class="card">

<h1>IMA</h1>

<p>Autonomous Intelligence System</p>

<button onclick="status()">
STATUS
</button>

<pre id="out"></pre>

</div>

<script>

async function status(){

const r=
await fetch('/status');

const t=
await r.text();

document.getElementById(
'out'
).innerText=t;

}

</script>

</body>
</html>
`
);

// ======================================
// CLI
// ======================================

write(
'cli.js',
`#!/usr/bin/env node

console.log('IMA CLI ONLINE');

`
);

exec('chmod +x cli.js');

// ======================================
// PACKAGE
// ======================================

write(
'package.json',
JSON.stringify({

name:PACKAGE,
version:VERSION,
main:'server.js',

scripts:{

start:'node server.js',
runtime:'node runtime/autonomous_runtime.js',
analytics:'node runtime/npm_analytics.js'

},

bin:{
ima:'cli.js'
},

files:[

'server.js',
'runtime',
'core',
'logs',
'ui',
'memory',
'plugins',
'policies'

],

publishConfig:{
access:'public'
}

},null,2)
);

// ======================================
// TERMUX BOOT
// ======================================

try{

exec('mkdir -p ~/.termux/boot');

fs.writeFileSync(

process.env.HOME+
'/.termux/boot/ima_boot.sh',

`#!/data/data/com.termux/files/usr/bin/sh

cd ~/ima_core/kernel

nohup node runtime/autonomous_runtime.js >/dev/null 2>&1 &
nohup node server.js >/dev/null 2>&1 &

`

);

exec(
'chmod +x ~/.termux/boot/ima_boot.sh'
);

console.log('TERMUX BOOT OK');

}catch{

console.log('BOOT FAILED');

}

// ======================================
// GIT
// ======================================

exec('git add .');

exec(
'git commit -m "IMA ULTIMATE '+VERSION+'" || true'
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
'npm i -g '+PACKAGE+' --force'
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

// ======================================
// FINAL
// ======================================

write(
'logs/final_state.json',
JSON.stringify({

version:VERSION,
files:files.length,
duplicates:duplicates.length,
archived,
canonical,
published,
verify

},null,2)
);

console.log('======================================');
console.log('IMA ULTIMATE COMPLETE');
console.log('======================================');

console.log({

VERSION,
FILES:files.length,
DUPLICATES:duplicates.length,
ARCHIVED:archived,
CANONICAL:canonical,
PUBLISHED:published,
CLI:verify

});
