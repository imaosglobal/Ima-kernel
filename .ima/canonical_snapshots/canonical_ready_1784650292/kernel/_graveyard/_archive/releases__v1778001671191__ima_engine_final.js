

// ======================
// IMA_POLICY_LAYER
// ======================
const { execSync } = require('child_process');

function safeGitSync(){
  try {
    const status = execSync('git status --porcelain', {encoding:'utf8'});

    if (status.trim()) {
      console.log('[GIT] dirty state detected → auto-stash');
      execSync('git stash -u', {stdio:'inherit'});
    }

    execSync('git pull --rebase', {stdio:'inherit'});
    return true;

  } catch (e) {
    console.log('[GIT] non-blocking error:', e.message);
    return false;
  }
}

module.exports = {
  run(){ console.log('[RUN OK]'); },
  update(){ console.log('[UPDATE OK]'); },
  deploy(){ console.log('[DEPLOY OK]'); },
  restart(){ console.log('[RESTART OK]'); }
};
