const { execSync } = require('child_process');

function run(cmd, label, soft=false){
  console.log('\n→ ' + label);
  try {
    execSync(cmd, { stdio: 'inherit' });
    return true;
  } catch (e) {
    if (!soft) throw e;
    console.log('[WARN]', e.message);
    return false;
  }
}

function gitSync(){
  console.log('\n[Git Sync]');
  try {
    const status = execSync('git status --porcelain',{encoding:'utf8'});

    if(status.trim()){
      console.log('[GIT] dirty → auto commit');
      run('git add .','stage',true);
      run('git commit -m "auto sync" || true','commit',true);
    }

    run('git pull --rebase','pull',true);
    run('git push','push',true);

  } catch(e){
    console.log('[GIT WARN]', e.message);
  }
}

function npmStep(){
  console.log('\n[NPM]');
  try {
    execSync('npm whoami',{stdio:'ignore'});
  } catch {
    console.log('[NPM] login required');
    execSync('npm login',{stdio:'inherit'});
  }

  run('npm version patch','version');

  try {
    execSync('npm publish',{stdio:'inherit'});
    console.log('[NPM] published');
  } catch(e){
    console.log('[NPM WARN]', e.message);
  }
}

function freePort(){
  console.log('\n[PORT CLEAN]');
  try {
    execSync('lsof -ti:4000 | xargs kill -9',{stdio:'ignore'});
    console.log('[PORT] cleared');
  } catch {}
}

function runtime(){
  console.log('\n[Runtime]');
  try {
    execSync('node server.js',{stdio:'inherit'});
  } catch(e){
    console.log('[RUNTIME STOP]');
  }
}

function deploy(){
  console.log('======================');
  console.log('[IMA FINAL ENGINE]');
  console.log('======================');

  console.log('[1] git');
  gitSync();

  console.log('[2] npm');
  npmStep();

  console.log('[3] port');
  freePort();

  console.log('[4] runtime');
  runtime();

  console.log('======================');
  console.log('[DONE]');
  console.log('======================');
}

module.exports = { deploy };
