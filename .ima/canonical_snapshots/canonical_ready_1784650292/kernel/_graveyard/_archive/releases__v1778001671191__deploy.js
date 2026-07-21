const { execSync } = require('child_process');

function run(cmd,label,soft=false){
  console.log('\n→ ' + label);
  try { execSync(cmd,{stdio:'inherit'}); return true; }
  catch(e){ if(!soft) throw e; return false; }
}

function npmPublish(){
  console.log('\n→ npm publish');
  try {
    execSync('npm publish',{stdio:'inherit'});
    return true;
  } catch(e){
    console.log('⚠ npm publish failed');
    return false;
  }
}

module.exports = function deploy(){

  run('pkill -f "ima-core-saas/runtime/server.js" || true','stop server',true);

  run('git add .','stage');
  run('git commit -m "auto deploy" || true','commit',true);
  run('git push','push',true);

  run('npm version patch','version');

  const published = npmPublish();

  return { ok: true, published };
}
