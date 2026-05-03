const { execSync } = require('child_process');

const ROOT = process.env.HOME + '/ima_core/kernel';

function goRoot(){
  process.chdir(ROOT);
}

function run(cmd,label,soft=false){
  console.log('→',label);
  try { execSync(cmd,{stdio:'inherit'}); return true; }
  catch(e){ if(!soft) throw e; return false; }
}

/* ===================== */
/* SAFE HELPERS */
/* ===================== */

function safe(fn,label){
  try {
    return fn();
  } catch(e){
    console.log(`[SAFE FAIL] ${label}:`, e.message);
    return null;
  }
}

/* ===================== */
/* GIT */
/* ===================== */

function gitPull(){
  console.log('\n[GIT PULL]');
  safe(()=>{
    const status = execSync('git status --porcelain',{encoding:'utf8'});

    if(status.trim()){
      console.log('[GIT] dirty → auto stash');
      execSync('git stash -u',{stdio:'inherit'});
    }

    run('git pull --rebase','pull');
  },'gitPull');
}

function gitPush(){
  console.log('\n[GIT PUSH]');
  run('git add .','stage',true);
  run('git commit -m "auto deploy" || true','commit',true);
  run('git push','push',true);
}

/* ===================== */
/* NPM SAFE VERSION */
/* ===================== */

function getLocalVersion(){
  return require(ROOT + '/package.json').version;
}

function getRemoteVersions(){
  try {
    const out = execSync('npm view ima-core-saas versions --json',{encoding:'utf8'});
    return JSON.parse(out);
  } catch {
    return [];
  }
}

function bumpVersionSafe(){
  let version = getLocalVersion();
  const remote = getRemoteVersions();

  while(remote.includes(version)){
    console.log('[NPM] version exists → bumping');
    execSync('npm version patch',{stdio:'inherit'});
    version = getLocalVersion();
  }

  return version;
}

function npmPublish(){
  console.log('\n[NPM]');
  safe(()=>{
    try { execSync('npm whoami',{stdio:'ignore'}); }
    catch { execSync('npm login',{stdio:'inherit'}); }

    const v = bumpVersionSafe();

    console.log('[NPM] publishing', v);
    execSync('npm publish',{stdio:'inherit'});

    console.log('[NPM DONE]');
  },'npmPublish');
}

/* ===================== */
/* RUNTIME */
/* ===================== */

function freePort(){
  console.log('\n[PORT]');
  safe(()=>{
    execSync('lsof -ti:4000 | xargs kill -9',{stdio:'ignore'});
  },'port');
}

function startServer(){
  console.log('\n[RUN]');
  execSync('node server.js',{stdio:'inherit'});
}

/* ===================== */
/* COMMANDS */
/* ===================== */

function runCmd(){
  goRoot();
  startServer();
}

function deploy(){
  goRoot();
  gitPush();
  npmPublish();
  console.log('\n[DONE DEPLOY]');
}

function update(){
  goRoot();
  gitPull();
  console.log('\n[DONE UPDATE]');
}

function restart(){
  goRoot();
  freePort();
  startServer();
}

/* ===================== */

module.exports = {
  run: runCmd,
  deploy,
  update,
  restart
};
