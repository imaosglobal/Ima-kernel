const { exec } = require('child_process');

console.log('[KILL SWITCH] waiting 2s then stopping runtime...');

setTimeout(() => {
  try {
    // הורג כל מה שקשור ל-4000 או node של הפרויקט
    exec("lsof -ti:4000 | xargs kill -9 2>/dev/null || true");
    exec("pkill -f global_boot || true");
    exec("pkill -f ima-core || true");

    console.log('[KILLED] runtime stopped safely');
  } catch (e) {
    console.log('[KILL ERROR]', e.message);
  }

  process.exit(0);
}, 2000);
