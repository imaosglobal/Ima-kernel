const CORE = require('./KERNEL_CORE');

function start() {
  console.log('=== KERNEL MINIMAL SYSTEM ===');

  CORE.setVersion('1.1.1');

  setInterval(() => {
    const state = CORE.read();
    console.log('[HEARTBEAT]', state.version);
  }, 2000);
}

module.exports = { start };
