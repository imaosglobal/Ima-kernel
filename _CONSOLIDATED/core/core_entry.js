const http = require('http');
const mesh = require('./ima_mesh_core_v2');

const PORT = 7000;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    return res.end(JSON.stringify(mesh.health()));
  }

  if (req.url === '/enqueue' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      const task = JSON.parse(body);
      const result = mesh.enqueue(task);
      res.end(JSON.stringify(result));
    });
    return;
  }

  if (req.url === '/history') {
    return res.end(JSON.stringify(mesh.history()));
  }

  res.statusCode = 404;
  res.end();
});

server.listen(PORT, () => {
  console.log('[CORE] mesh_v2 ACTIVE :', PORT);
});


// === SAFE AUTO REGISTER ===
if (!global.__MESH_REGISTERED__) {
  global.__MESH_REGISTERED__ = true;

  const http = require('http');

  function registerSelf() {
    const payload = JSON.stringify({
      id: 'mesh_v1',
      type: 'mesh',
      host: '127.0.0.1',
      port: 7000
    });

    const req = http.request({
      hostname: '127.0.0.1',
      port: 7200,
      path: '/register',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    });

    req.on('error', e => {
      console.log('[MESH] register fail', e.message);
    });

    req.write(payload);
    req.end();
  }

  setTimeout(registerSelf, 1000);
}
