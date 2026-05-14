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
