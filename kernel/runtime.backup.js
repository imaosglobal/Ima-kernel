
const { load, save, addMemory } = require('./kernel/memory_engine');
console.log('🧠 IMA RUNTIME BOOTED');
setInterval(() => {
  try {
    const report = stability.healthCheck();
    console.log('🛡 health:', report);
    const recovery = stability.smartRecover();
  } catch (e) {
    console.log('⚠️ stability error:', e.message);
  }
}, 15000);
