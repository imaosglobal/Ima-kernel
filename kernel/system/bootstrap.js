const fs=require('fs');
const cp=require('child_process');
const path=require('path');

const ROOT=process.cwd();

const CONFIG={
  NAME:'@mom-os1/ima-core',
  VERSION:'1.0.'+Date.now(),
  PORT:4000
};

function run(cmd,inherit=false){
  try{
    const out=cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:inherit?'inherit':'pipe'
    });

    return inherit?true:out.toString().trim();

  }catch(e){
    return inherit?false:null;
  }
}

function write(file,data){
  const full=path.join(ROOT,file);
  fs.mkdirSync(path.dirname(full),{recursive:true});
  fs.writeFileSync(full,data);
  console.log('CREATED:',file);
}

console.log('========================');
console.log('IMA AUTONOMOUS SYSTEM');
console.log('========================');

// AUTH
const who=run('npm whoami');

if(!who){
  console.log('');
  console.log('LOGIN REQUIRED');
  console.log('RUN: npm login --auth-type=web');
  console.log('');
  process.exit(1);
}

console.log('AUTH:',who);

// PACKAGE
write('package.json',JSON.stringify({
  name:CONFIG.NAME,
  version:CONFIG.VERSION,
  main:'server.js',
  license:'MIT',
  publishConfig:{
    access:'public'
  },
  files:[
    'server.js',
    'cli.js',
    'core',
    'api',
    'memory',
    'policies',
    'runtime',
    'ui'
  ],
  bin:{
    ima:'cli.js'
  }
},null,2));

// CLI
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

run('chmod +x cli.js',true);

// MEMORY
write('memory/long_memory.json',JSON.stringify({
  goals:[],
  users:[],
  learning:[],
  upgrades:[]
},null,2));

// POLICY
write('policies/safety_policy.json',JSON.stringify({
  forbid:[
    'violence',
    'terror',
    'malware',
    'fraud',
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

// API
write('api/server_api.js',`
module.exports=function(req,res){
  res.end(JSON.stringify({
    status:'online',
    system:'IMA'
  }));
};
`);

// CORE
write('core/self_heal.js',`
const fs=require('fs');

module.exports=function(){

  const required=[
    'server.js',
    'package.json',
    'cli.js'
  ];

  for(const f of required){

    if(!fs.existsSync(f)){
      console.log('MISSING',f);
    }

  }

};
`);

// UI
write('ui/index.html',`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>IMA</title>
<style>
body{
background:#111;
color:#fff;
font-family:sans-serif;
text-align:center;
padding-top:100px;
}
</style>
</head>
<body>
<h1>IMA ONLINE</h1>
<p>Autonomous Intelligence System</p>
</body>
</html>
`);

// SERVER
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

// RELEASE SYSTEM
write('scripts/release.js',`
const cp=require('child_process');

function ok(cmd){
  try{
    cp.execSync(cmd,{stdio:'inherit',shell:true});
    return true;
  }catch(e){
    return false;
  }
}

ok('git add .');
ok('git commit -m "auto release" || true');
ok('git push || true');

ok('npm publish --access public');
`);

// START
run('git add .',true);
run('git commit -m "IMA autonomous bootstrap" || true',true);
run('git push || true',true);

console.log('');
console.log('========================');
console.log('IMA READY');
console.log('========================');
console.log('');
console.log('START: node server.js');
console.log('RELEASE: node scripts/release.js');
console.log('CLI: ima');
console.log('');
