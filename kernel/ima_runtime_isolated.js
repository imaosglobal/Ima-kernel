const { spawn } = require('child_process');

console.log('[IMA RUNTIME] isolated start');

// מריצים את השרת כתהליך נפרד
const child = spawn('node', ['global_boot.js'], {
  stdio: 'inherit'
});

// כיבוי אחרי 2 שניות בכל מקרה
setTimeout(() => {
  console.log('[IMA RUNTIME] force shutdown');

  child.kill('SIGTERM');

  setTimeout(() => {
    try {
      child.kill('SIGKILL');
    } catch (e) {}

    console.log('[IMA RUNTIME] closed');
    process.exit(0);
  }, 1000);

}, 2000);

// אם התהליך נופל
child.on('exit', () => {
  console.log('[IMA RUNTIME] exited naturally');
  process.exit(0);
});
