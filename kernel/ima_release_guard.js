const gate = require('./ima_system_gate');

function release(){
  gate.runGate();
  console.log('[RELEASE SAFE] continuing release flow...');
}

module.exports = { release };


);
  console.log('[AUTO PUSH DONE]');
} catch(e) {
  console.log('[AUTO PUSH SKIPPED]');
}


// AUTO_PUSH_FINAL
function autoPush(){
  try {
    require('child_process').execSync('git push origin main', { stdio: 'inherit' });
    console.log('[AUTO PUSH DONE]');
  } catch(e){
    console.log('[AUTO PUSH SKIPPED]');
  }
}

// HOOK
setTimeout(autoPush, 0);
