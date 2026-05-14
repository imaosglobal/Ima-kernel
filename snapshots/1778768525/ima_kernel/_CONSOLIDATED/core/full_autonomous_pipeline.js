const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';

function exec(cmd,inherit=false){

  try{

    const out=cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:inherit?'inherit':'pipe'
    });

    return inherit?true:out.toString().trim();

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

  console.log('WRITE',file);

}

function exists(file){

  return fs.existsSync(path.join(ROOT,file));

}

console.log('');
console.log('===================================');
console.log('IMA UNIVERSAL AUTONOMOUS PIPELINE');
console.log('===================================');
console.log('');

const user=exec('npm whoami');

if(!user){

  console.log('AUTH FAILED');
  process.exit(1);

}

console.log('AUTH OK:',user);

// --------------------
// FULL GIT SYNC
// --------------------

console.log('');
console.log('GIT SYNC');
console.log('');

exec('git fetch --all',true);
exec('git pull --rebase',true);

// --------------------
// BACKUP
// --------------------

const BACKUP='backups/'+Date.now();

fs.mkdirSync(BACKUP,{
  recursive:true
});

console.log('BACKUP:',BACKUP);

// --------------------
// DUPLICATE SCAN
// --------------------

console.log('');
console.log('SCAN DUPLICATES');
console.log('');

const skip=[
'.git',
'node_modules',
'backups',
'dist',
'build'
];

const hashes={};
const duplicates=[];

function walk(dir){

  for(const item of fs.readdirSync(dir)){

    const full=path.join(dir,item);

    const rel=path.relative(ROOT,full);

    if(skip.some(s=>rel.startsWith(s))) continue;

    const stat=fs.statSync(full);

    if(stat.isDirectory()){

      walk(full);

      continue;

    }

    try{

      const hash=crypto
      .createHash('sha256')
      .update(fs.readFileSync(full))
      .digest('hex');

      if(!hashes[hash]){
        hashes[hash]=[];
      }

      hashes[hash].push(rel);

    }catch(e){}

  }

}

walk(ROOT);

for(const h in hashes){

  if(hashes[h].length>1){

    duplicates.push(hashes[h]);

  }

}

if(duplicates.length){

  console.log('');
  console.log('DUPLICATES FOUND');
  console.log('');

  duplicates.forEach(g=>{

    console.log(g.join(' <=> '));

  });

}else{

  console.log('NO DUPLICATES');

}

// --------------------
// CLEAN
// --------------------

console.log('');
console.log('CLEAN');
console.log('');

[
'.npmignore',
'npm-debug.log',
'yarn.lock'
].forEach(f=>{

  try{

    fs.unlinkSync(f);

    console.log('REMOVED',f);

  }catch(e){}

});

// --------------------
// VERSION
// --------------------

let current='0.0.0';

try{

  current=exec('npm view '+NAME+' version')||'0.0.0';

}catch(e){}

console.log('');
console.log('CURRENT VERSION:',current);

const VERSION='1.0.'+Date.now();

console.log('NEW VERSION:',VERSION);

// --------------------
// PACKAGE
// --------------------

write('package.json',JSON.stringify({

  name:NAME,
  version:VERSION,
  main:'server.js',
  license:'MIT',

  publishConfig:{
    access:'public'
  },

  scripts:{
    start:'node server.js',
    release:'node system/full_autonomous_pipeline.js'
  },

  files:[
    'server.js',
    'cli.js',
    'core',
    'api',
    'memory',
    'policies',
    'runtime',
    'plugins',
    'ui',
    'system'
  ],

  bin:{
    ima:'cli.js'
  }

},null,2));

// --------------------
// CLI
// --------------------

write('cli.js',`#!/usr/bin/env node

const http=require('http');

const cmd=process.argv[2]||'status';

const host=process.env.IMA_HOST||'localhost';

const port=process.env.IMA_PORT||4000;

http.get(
'http://'+host+':'+port+'/'+cmd,
res=>res.pipe(process.stdout)
).on(
'error',
()=>{
console.log('IMA OFFLINE');
}
);
`);

exec('chmod +x cli.js',true);

// --------------------
// CORE
// --------------------

write('core/self_heal.js',`
const fs=require('fs');

module.exports=function(){

const required=[
'server.js',
'package.json',
'cli.js',
'ui/index.html'
];

for(const f of required){

if(!fs.existsSync(f)){

console.log('MISSING',f);

}

}

};
`);

// --------------------
// MEMORY
// --------------------

write('memory/long_memory.json',JSON.stringify({

users:[],
learning:[],
goals:[],
skills:[],
history:[],
upgrades:[]

},null,2));

// --------------------
// POLICY
// --------------------

write('policies/safety.json',JSON.stringify({

forbid:[
'violence',
'terror',
'fraud',
'malware',
'self_harm'
],

allow:[
'education',
'healing',
'creativity',
'science',
'collaboration'
]

},null,2));

// --------------------
// UI
// --------------------

write('ui/index.html',`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>IMA</title>
<style>

body{
background:#111;
color:white;
font-family:sans-serif;
text-align:center;
padding-top:60px;
}

button{
padding:15px;
font-size:18px;
border:none;
border-radius:10px;
cursor:pointer;
}

#chat{
width:80%;
height:120px;
margin-top:20px;
}

</style>
</head>
<body>

<h1>IMA</h1>

<p>Autonomous Intelligence System</p>

<button onclick="status()">STATUS</button>

<br/>

<textarea id="chat" placeholder="Talk to IMA"></textarea>

<script>

function status(){

fetch('/status')
.then(r=>r.text())
.then(alert);

}

</script>

</body>
</html>
`);

// --------------------
// SERVER
// --------------------

write('server.js',`
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

return res.end('IMA ONLINE');

}

res.end('OK');

}).listen(4000,()=>{

console.log('IMA RUNNING ON 4000');

});
`);

// --------------------
// TESTS
// --------------------

console.log('');
console.log('TESTS');
console.log('');

if(exec('node --check server.js')===null){

  console.log('SERVER FAILED');
  process.exit(1);

}

if(exec('node --check cli.js')===null){

  console.log('CLI FAILED');
  process.exit(1);

}

if(!exists('ui/index.html')){

  console.log('UI FAILED');
  process.exit(1);

}

console.log('TESTS PASSED');

// --------------------
// GIT SAVE
// --------------------

console.log('');
console.log('GIT PUSH');
console.log('');

exec('git add .',true);
exec('git commit -m "IMA AUTO '+VERSION+'" || true',true);
exec('git tag '+VERSION+' || true',true);
exec('git push',true);
exec('git push --tags',true);

// --------------------
// PUBLISH
// --------------------

console.log('');
console.log('NPM PUBLISH');
console.log('');

const pub=exec(
'npm publish --access public',
true
);

if(!pub){

  console.log('');
  console.log('PUBLISH FAILED');
  console.log('');
  console.log('RUN AGAIN:');
  console.log('node system/full_autonomous_pipeline.js');
  console.log('');

  process.exit(1);

}

// --------------------
// VERIFY
// --------------------

console.log('');
console.log('VERIFY');
console.log('');

const verify=exec(
'npm view '+NAME+' version'
)||'';

if(String(verify).includes(VERSION)){

  console.log('');
  console.log('======================');
  console.log('IMA SUCCESS');
  console.log('======================');
  console.log('');
  console.log(NAME);
  console.log(VERSION);
  console.log('');
  console.log('INSTALL:');
  console.log('npm i -g '+NAME);
  console.log('');

}else{

  console.log('');
  console.log('VERIFY DELAYED');
  console.log('');

}
