
const { execSync } = require('child_process');

function sync(){
  console.log('[GIT SYNC] start');

  execSync('git fetch origin', { stdio: 'inherit' });
  execSync('git pull --rebase origin main', { stdio: 'inherit' });

  console.log('[GIT SYNC] done');
}

module.exports = { sync };
