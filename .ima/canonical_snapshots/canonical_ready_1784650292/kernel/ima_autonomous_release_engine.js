const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';

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

// ---------------- DUPLICATES ENGINE ----------------

function scanDuplicates(){

  const map=new Map();
  const duplicates=[];

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

      try{
        const h=crypto.createHash('sha256')
        .update(fs.readFileSync(full))
        .digest('hex');

        if(!map.has(h)) map.set(h,[]);
        map.get(h).push(rel);

      }catch(e){}
    }
  }

  walk(ROOT);

  for(const v of map.values()){
    if(v.length>1) duplicates.push(v);
  }

  return duplicates;
}

// ---------------- VERSION FIXER ----------------

function safeVersion(){

  const base='1.0.'+Date.now();

  const exists=exec(`npm view ${NAME}@${base} version`);

  if(exists){
    return '1.0.'+(Date.now()+Math.floor(Math.random()*1000));
  }

  return base;
}

// ---------------- RUNTIME CHECK ----------------

function runtimeCheck(){

  exec('node server.js & sleep 2');

  const res=exec('curl -s http://localhost:4000/status');

  return res && res.includes('IMA');
}

// ---------------- GIT SYNC ----------------

function gitSync(){

  exec('git fetch --all');
  exec('git pull --rebase || true');

  exec('git add .');
  exec(`git commit -m "auto release" || true`);
  exec('git push || true');
  exec('git push --tags || true');
}

// ---------------- PUBLISH ENGINE ----------------

function publish(version){

  const who=exec('npm whoami');

  if(!who){
    return {ok:false,reason:'NO_AUTH'};
  }

  for(let i=0;i<3;i++){

    const out=exec('npm publish --access public 2>&1');

    if(out && !out.includes('ERR') && !out.includes('error')){
      return {ok:true};
    }

    if(out){

      if(out.includes('OTP')){
        return {ok:false,reason:'OTP_REQUIRED'};
      }

      if(out.includes('already exists')){
        return {ok:false,reason:'VERSION_EXISTS'};
      }

    }

  }

  return {ok:false,reason:'UNKNOWN_FAILURE'};
}

// ---------------- MAIN ----------------

console.log('=== IMA AUTONOMOUS RELEASE ENGINE ===');

// 1. duplicates
const duplicates=scanDuplicates();
console.log('DUPLICATES:',duplicates.length);

// 2. version
const VERSION=safeVersion();
console.log('VERSION:',VERSION);

// 3. runtime
const runtimeOk=runtimeCheck();
console.log('RUNTIME:',runtimeOk);

// 4. package rebuild
write('package.json',JSON.stringify({
  name:NAME,
  version:VERSION,
  main:'server.js',
  files:['server.js','cli.js','core','ui','memory','policies','runtime','plugins','system']
},null,2));

// 5. git sync
gitSync();

// 6. publish
const result=publish(VERSION);

// 7. decision engine
if(result.ok){

  console.log('========================');
  console.log('PUBLISH SUCCESS');
  console.log(NAME);
  console.log(VERSION);
  console.log('========================');

}else{

  console.log('========================');
  console.log('PUBLISH FAILED');
  console.log('REASON:',result.reason);
  console.log('========================');

}

// 8. state log
write('logs/last_run.json',JSON.stringify({
  version:VERSION,
  duplicates:duplicates.length,
  runtime:runtimeOk,
  publish:result
},null,2));

