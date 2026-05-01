const update = require('./ima_update_guard');
const release = require('./ima_release_guard');

function run(){
  console.log('======================');
  console.log('[IMA AUTOPILOT START]');
  console.log('======================');

  // UPDATE PHASE
  update.update();

  console.log('[PHASE 1 DONE: UPDATE]');

  // RELEASE PHASE
  release.release();

  console.log('[PHASE 2 DONE: RELEASE]');

  console.log('======================');
  console.log('[AUTOPILOT COMPLETE]');
  console.log('======================');
}

module.exports = { run };
