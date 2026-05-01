const app = require('./global_boot.js');

console.log('[IMA UPDATE] runtime dry mode start');

// אם זה Express / server
let server = null;

try {
  if (typeof app === 'function') {
    server = app.listen(4000);
  } else if (app && app.listen) {
    server = app.listen(4000);
  }

  console.log('[RUNTIME OK] started');

  setTimeout(() => {
    try {
      if (server && server.close) {
        server.close();
        console.log('[RUNTIME CLOSED]');
      }
    } catch (e) {}

    process.exit(0);
  }, 800);

} catch (e) {
  console.log('[RUNTIME SAFE FAIL]', e.message);
  process.exit(0);
}
