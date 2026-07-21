const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';
const VERSION='1.0.'+Date.now();

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

// ---------------- SCAN ----------------

function scan(){

  const hashes=new Map();
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

        if(!hashes.has(h)) hashes.set(h,[]);
        hashes.get(h).push(rel);

      }catch(e){}
    }
  }

  walk(ROOT);

  for(const v of hashes.values()){
    if(v.length>1) duplicates.push(v);
  }

  return duplicates;
}

// ---------------- HEALTH CHECK (REAL RUNTIME) ----------------

function runtimeCheck(){

  console.log('RUNNING RUNTIME CHECK...');

  const server=exec('node server.js & sleep 2');

  const res=exec('curl -s http://localhost:4000/status');

  if(!res || !res.includes('IMA')){
    console.log('RUNTIME FAIL');
    return false;
  }

  console.log('RUNTIME OK');
  return true;
}

// ---------------- SAFE PUBLISH ----------------

function publish(){

  const who=exec('npm whoami');

  if(!who){
    console.log('NO AUTH');
    return false;
  }

  const exists=exec(`npm view ${NAME}@${VERSION} version`);

  if(exists){
    console.log('VERSION EXISTS');
    return false;
  }

  for(let i=0;i<2;i++){

    console.log('PUBLISH TRY',i+1);

    const ok=exec('npm publish --access public');

    if(ok){
      console.log('PUBLISH OK');
      return true;
    }
  }

  return false;
}

// ---------------- GIT ----------------

function git(){

  exec('git add .');
  exec(`git commit -m "auto ${VERSION}" || true`);
  exec(`git push || true`);
  exec(`git push --tags || true`);

}

// ---------------- SYSTEM STATE ----------------

function saveState(data){

  write('memory/system_state.json',JSON.stringify(data,null,2));

}

// ---------------- MAIN ----------------

console.log('=== IMA FULL ENGINE ===');

const duplicates=scan();

console.log('DUPLICATES:',duplicates.length);

const runtimeOk=runtimeCheck();

const published=publish();

git();

saveState({
  version:VERSION,
  duplicates:duplicates.length,
  runtime:runtimeOk,
  published:published,
  time:Date.now()
});

console.log('=== DONE ===');
console.log({
  VERSION,
  runtimeOk,
  published
});

