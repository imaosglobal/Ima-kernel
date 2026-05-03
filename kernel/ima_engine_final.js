const { execSync } = require('child_process');

function run(cmd,label,soft=false){
  console.log('→',label);
  try { execSync(cmd,{stdio:'inherit'}); return true; }
  catch(e){ if(!soft) throw e; return false; }
}

/* ===================== */
/* COMMANDS */
/* ===================== */

function gitPull(){
  console.log('\n[GIT PULL]');
  run('git pull --rebase','pull',true);
}

function gitPush(){
  console.log('\n[GIT PUSH]');
  run('git add .','stage',true);
  run('git commit -m "auto deploy" || true','commit',true);
  run('git push','push',true);
}

function npmPublish(){
  console.log('\n[NPM]');
  try { execSync('npm whoami',{stdio:'ignore'}); }
  catch { execSync('npm login',{stdio:'inherit'}); }

  run('npm version patch','version');
  run('npm publish','publish',true);
}

function freePort(){
  console.log('\n[PORT]');
  try { execSync('lsof -ti:4000 | xargs kill -9',{stdio:'ignore'}); }
  catch {}
}

function startServer(){
  console.log('\n[RUN]');
  execSync('node server.js',{stdio:'inherit'});
}

/* ===================== */
/* PUBLIC API */
/* ===================== */

function runCmd(){
  startServer();
}

function deploy(){
  gitPush();
  npmPublish();
}

function update(){
  gitPull();
}

function restart(){
  freePort();
  startServer();
}

module.exports = {
  run: runCmd,
  deploy,
  update,
  restart
};
