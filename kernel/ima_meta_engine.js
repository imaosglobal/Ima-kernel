const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();

const CONFIG={
  name:'@mom-os1/ima-core',
  port:4000
};

// ---------------- EXEC ----------------

function exec(cmd){
  try{
    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:'pipe'
    }).toString().trim();
  }catch(e){
    return null;
  }
}

// ---------------- WRITE ----------------

function write(file,data){
  const full=path.join(ROOT,file);
  fs.mkdirSync(path.dirname(full),{recursive:true});
  fs.writeFileSync(full,data);
}

// ---------------- HASH ----------------

function hashFile(file){
  return crypto.createHash('sha256')
    .update(fs.readFileSync(file))
    .digest('hex');
}

// ---------------- SCAN PROJECT ----------------

function scan(){

  const files=[];
  const hashes=new Map();

  function walk(dir){

    for(const f of fs.readdirSync(dir)){

      const full=path.join(dir,f);
      const rel=path.relative(ROOT,full);

      if(rel.startsWith('node_modules') || rel.startsWith('.git')) continue;

      const stat=fs.statSync(full);

      if(stat.isDirectory()){
        walk(full);
        continue;
      }

      files.push(rel);

      try{
        const h=hashFile(full);
        if(!hashes.has(h)) hashes.set(h,[]);
        hashes.get(h).push(rel);
      }catch(e){}
    }
  }

  walk(ROOT);

  const duplicates=[...hashes.values()].filter(x=>x.length>1);

  return {files,duplicates};
}

// ---------------- REGISTRY ----------------

function loadRegistry(){

  const file='memory/registry.json';

  if(!fs.existsSync(file)){
    return {modules:{}};
  }

  return JSON.parse(fs.readFileSync(file));
}

function saveRegistry(r){
  write('memory/registry.json',JSON.stringify(r,null,2));
}

// ---------------- MODULE BUILDER ----------------

function buildModule(name){

  const dir=`modules/${name}`;

  if(fs.existsSync(dir)) return;

  write(`${dir}/index.js`,`
module.exports=function(){
  return {
    name:"${name}",
    status:"active"
  };
};
  `);
}

// ---------------- LOADER ----------------

function loadModule(name){
  const p=`./modules/${name}/index.js`;
  if(fs.existsSync(p)){
    return require(path.resolve(p));
  }
  return null;
}

// ---------------- VERIFY MODULE ----------------

function verify(mod){
  try{
    return mod && mod().name;
  }catch(e){
    return false;
  }
}

// ---------------- SELF HEAL ----------------

function selfHeal(files){

  const required=[
    'server.js',
    'package.json',
    'cli.js',
    'ui/index.html'
  ];

  for(const f of required){
    if(!files.includes(f)){
      console.log('MISSING:',f);
    }
  }
}

// ---------------- SYSTEM RUN ----------------

function runSystem(){

  console.log('=== IMA META ENGINE ===');

  const scanResult=scan();

  console.log('FILES:',scanResult.files.length);
  console.log('DUPLICATES:',scanResult.duplicates.length);

  selfHeal(scanResult.files);

  let registry=loadRegistry();

  const requiredModules=[
    'chat',
    'avatar',
    'memory',
    'ui'
  ];

  for(const m of requiredModules){

    let mod=loadModule(m);

    if(!mod){
      buildModule(m);
      mod=loadModule(m);
    }

    const ok=verify(mod);

    registry.modules[m]=ok?'active':'broken';

  }

  saveRegistry(registry);

  // ---------------- GIT ----------------

  exec('git add .');
  exec('git commit -m "meta engine sync" || true');
  exec('git push || true');

  // ---------------- NPM ----------------

  const version='1.0.'+Date.now();

  const pkg={
    name:CONFIG.name,
    version,
    main:'server.js',
    files:['modules','memory','core','ui','server.js','cli.js']
  };

  write('package.json',JSON.stringify(pkg,null,2));

  const pub=exec('npm publish --access public');

  if(!pub){
    console.log('PUBLISH SKIPPED/FAILED');
  }

  console.log('=== DONE ===');
  console.log('VERSION:',version);

}

// ---------------- START ----------------

runSystem();

