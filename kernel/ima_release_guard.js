const gate = require('./ima_system_gate');

function release(){
  gate.runGate();
  console.log('[RELEASE SAFE] continuing release flow...');
}

module.exports = { release };
