const fs = require('fs');

let f = fs.readFileSync('ima_engine_final.js','utf8');

if (!f.includes('IMA_POLICY_LAYER')) {

const patch = `
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
`;

  const i = f.indexOf('\n') + 1;
  f = f.slice(0, i) + patch + '\n' + f.slice(i);

  fs.writeFileSync('ima_engine_final.js', f);
  console.log('[POLICY ADDED]');
} else {
  console.log('[POLICY EXISTS]');
}
