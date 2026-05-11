const gate = require('./ima_system_gate');

function update(){
  gate.runGate();
  console.log('[UPDATE SAFE] continuing update flow...');
}

module.exports = { update };
