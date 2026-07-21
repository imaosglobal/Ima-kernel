const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';
const VERSION='1.0.'+Date.now();

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

console.log('');
console.log('====================================');
console.log('IMA FINAL AUTONOMOUS PIPELINE');
console.log('====================================');
console.log('');

const who=exec('npm whoami');

if(!who){

  console.log('LOGIN REQUIRED');
  console.log('RUN: npm login --auth-type=web');
  process.exit(1);

}

console.log('AUTH OK:',who);

// -----------------------------------
// GIT SYNC
// -----------------------------------

console.log('');
console.log('SYNC GIT');
console.log('');

exec('git fetch --all',true);
exec('git pull --rebase || true',true);

// -----------------------------------
// REMOVE OLD GLOBAL CLI CONFLICT
// -----------------------------------

console.log('');
console.log('FIX GLOBAL CLI');
console.log('');

exec('rm -f /data/data/com.termux/files/usr/bin/ima',true);

// -----------------------------------
// DUPLICATE SCAN
// -----------------------------------

console.log('');
console.log('SCAN DUPLICATES');
console.log('');

const skip=[
'.git',
'node_modules',
'backups',
'releases'
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

write(
'logs/duplicates.json',
JSON.stringify(duplicates,null,2)
);

console.log('DUPLICATES:',duplicates.length);

// -----------------------------------
// PACKAGE
// -----------------------------------

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
    release:'node system/final_autonomous_pipeline.js'
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
    'system',
    'logs'
  ],

  bin:{
    ima:'cli.js'
  }

},null,2));

// -----------------------------------
// CLI
// -----------------------------------

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

// -----------------------------------
// SELF HEAL
// -----------------------------------

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

// -----------------------------------
// UI
// -----------------------------------

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
padding-top:50px;
}
textarea{
width:80%;
height:120px;
}
button{
padding:15px;
font-size:18px;
}
</style>
</head>
<body>

<h1>IMA</h1>

<p>Autonomous Intelligence</p>

<button onclick="status()">
STATUS
</button>

<br/><br/>

<textarea placeholder="Talk to IMA"></textarea>

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

// -----------------------------------
// SERVER
// -----------------------------------

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

// -----------------------------------
// TESTS
// -----------------------------------

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

console.log('TESTS PASSED');

// -----------------------------------
// GIT
// -----------------------------------

console.log('');
console.log('GIT PUSH');
console.log('');

exec('git add .',true);
exec('git commit -m "IMA FINAL '+VERSION+'" || true',true);
exec('git tag '+VERSION+' || true',true);
exec('git push || true',true);
exec('git push --tags || true',true);

// -----------------------------------
// PUBLISH
// -----------------------------------

console.log('');
console.log('NPM PUBLISH');
console.log('');

const pub=exec(
'npm publish --access public',
true
);

if(!pub){

  console.log('PUBLISH FAILED');
  process.exit(1);

}

// -----------------------------------
// VERIFY REAL
// -----------------------------------

console.log('');
console.log('VERIFY');
console.log('');

let verified=false;

for(let i=0;i<10;i++){

  const v=exec(
    'npm view '+NAME+' version'
  )||'';

  if(v.includes(VERSION)){

    verified=true;
    break;

  }

  exec('sleep 2',true);

}

if(!verified){

  console.log('VERIFY FAILED');
  process.exit(1);

}

console.log('');
console.log('======================');
console.log('IMA SUCCESS VERIFIED');
console.log('======================');
console.log('');
console.log(NAME);
console.log(VERSION);
console.log('');
console.log('INSTALLING GLOBAL...');
console.log('');

exec('npm i -g '+NAME+' --force',true);

console.log('');
console.log('RUNNING HEALTH TEST');
console.log('');

exec('ima',true);

console.log('');
console.log('================================');
console.log('IMA FULL PIPELINE COMPLETE');
console.log('================================');
console.log('');

