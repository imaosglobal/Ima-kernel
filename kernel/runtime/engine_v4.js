const fs=require('fs');
const cp=require('child_process');
const crypto=require('crypto');
const path=require('path');

const ROOT=process.cwd();
const NAME='@mom-os1/ima-core';

// ---------------- SAFE EXEC ----------------

function run(cmd,allowFail=true){
  try{
    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:'pipe'
    }).toString().trim();
  }catch(e){
    return allowFail?null:process.exit(1);
  }
}

// ---------------- FILE SYSTEM HASH ----------------

function hashDir(){
  const hash=crypto.createHash('sha256');

  function walk(dir){
    for(const f of fs.readdirSync(dir)){
      const full=path.join(dir,f);
      if(full.includes('node_modules')||full.includes('.git')) continue;

      const stat=fs.statSync(full);
      if(stat.isDirectory()) walk(full);
      else hash.update(fs.readFileSync(full));
    }
  }

  walk(ROOT);
  return hash.digest('hex');
}

// ---------------- VERSION ENGINE ----------------

function getVersion(){
  const base = run(`npm view ${NAME} version`) || "0.0.0";
  return "1.0." + Date.now() + "-" + base.split(".").pop();
}

// ---------------- BACKUP ----------------

function backup(){
  const dir=`backups/${Date.now()}`;
  fs.mkdirSync(dir,{recursive:true});
  run(`cp -r . ${dir} || true`);
  return dir;
}

// ---------------- GIT GUARD ----------------

function gitSync(){

  run('git fetch --all');
  run('git pull --rebase || true');

  const status=run('git status --porcelain');

  return status;
}

// ---------------- TEST LAYER ----------------

function validate(){

  if(!fs.existsSync('server.js')) return false;

  const syntax=run('node --check server.js',true);
  return syntax!==null;
}

// ---------------- RELEASE PIPE ----------------

function publish(version){

  run(`git add .`);
  run(`git commit -m "AUTO RELEASE ${version}" || true`);
  run(`git tag ${version} || true`);
  run(`git push || true`);
  run(`git push --tags || true`);

  for(let i=0;i<3;i++){
    const ok=run(`npm publish --access public`,true);
    if(ok!==null) return true;
  }

  return false;
}

// ---------------- VERIFY ----------------

function verify(version){

  for(let i=0;i<8;i++){

    const v=run(`npm view ${NAME} version`)||'';

    if(v.includes(version)) return true;

    run('sleep 2',true);
  }

  return false;
}

// ---------------- ENGINE ----------------

async function loop(){

  console.log("IMA v4 RELEASE ENGINE STARTED");

  while(true){

    const backupDir=backup();

    const stateHashBefore=hashDir();

    const gitStatus=gitSync();

    const version=getVersion();

    const valid=validate();

    if(!valid){
      console.log("INVALID STATE → ROLLBACK");
      run(`cp -r ${backupDir}/* . || true`);
      continue;
    }

    const published=publish(version);

    const verified=verify(version);

    const stateHashAfter=hashDir();

    const integrityOK = stateHashBefore !== stateHashAfter ? false : true;

    console.log({
      version,
      gitStatus,
      published,
      verified,
      integrityOK
    });

    if(!published || !verified || !integrityOK){

      console.log("FAIL SAFE TRIGGER → RESTORE BACKUP");

      run(`cp -r ${backupDir}/* . || true`);

    } else {

      console.log("RELEASE SUCCESSFUL");

    }

    run('sleep 20',true);
  }
}

loop();
