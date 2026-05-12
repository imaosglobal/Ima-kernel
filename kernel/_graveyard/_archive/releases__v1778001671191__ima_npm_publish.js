
const { execSync } = require('child_process');

function npmPublish(){
  try {
    execSync('npm whoami', { stdio: 'ignore' });
  } catch {
    console.log('[NPM] not logged in');
    return { ok:false };
  }

  try {
    execSync('npm publish', { stdio: 'inherit' });
    return { ok:true };
  } catch (e) {
    console.log('[NPM ERROR]', e.message);
    return { ok:false };
  }
}

module.exports = { npmPublish };
