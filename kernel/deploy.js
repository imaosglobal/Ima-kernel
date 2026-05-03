#!/usr/bin/env node
const { execSync } = require('child_process');

function run(cmd,label,allowFail=false){
  console.log('\n→ ' + label);
  try{
    return execSync(cmd,{stdio:'inherit'});
  }catch(e){
    if(!allowFail) throw e;
  }
}

function npmAuthCheck(){
  try{
    execSync('npm whoami',{stdio:'pipe'});
    return true;
  }catch(e){
    return false;
  }
}

try{
  run('pkill -f "ima-core-saas/runtime/server.js"','stop server',true);

  run('git status','check git');
  run('git add .','stage');
  run('git commit -m "auto deploy" || true','commit',true);
  run('git push','push',true);

  run('npm version patch','version',true);

  if(npmAuthCheck()){
    run('npm publish','publish');
  } else {
    console.log('\n⚠ npm not authenticated → skipping publish');
  }

  run('node node_modules/ima-core-saas/runtime/server.js','start');

  console.log('\n✔ DEPLOY COMPLETE');
}catch(e){
  console.log('\n✖ FAILED');
  console.error(e.message);
}
