'use strict';

const http = require('http');

const STATE = {
  workers: [],
  queue: [],
  tasks: 0,
  history: []
};

function log(x) {
  console.log('[CORE]', x);
}

function registerWorker(worker) {

  const exists =
    STATE.workers.find(w => w.id === worker.id);

  if (!exists) {

    STATE.workers.push(worker);

    log('WORKER REGISTERED ' + worker.id);
  }
}

function nextWorker() {

  if (!STATE.workers.length) {
    return null;
  }

  const w = STATE.workers.shift();

  STATE.workers.push(w);

  return w;
}

function dispatch(task) {

  const worker = nextWorker();

  if (!worker) {

    return {
      ok: false,
      error: 'NO_WORKERS'
    };
  }

  const payload = JSON.stringify(task);

  const req = http.request(
    {
      hostname: worker.host,
      port: worker.port,
      path: '/task',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length':
          Buffer.byteLength(payload)
      }
    },

    res => {

      let body = '';

      res.on('data', c => body += c);

      res.on('end', () => {

        try {

          const json = JSON.parse(body);

          STATE.tasks++;

          STATE.history.push({
            worker: worker.id,
            task,
            result: json,
            ts: Date.now()
          });

          log(
            'TASK OK ' +
            worker.id +
            ' ' +
            JSON.stringify(task)
          );

        } catch (e) {

          log('BAD RESPONSE');
        }
      });
    }
  );

  req.on('error', () => {

    log('WORKER FAIL ' + worker.id);
  });

  req.write(payload);

  req.end();

  return {
    ok: true,
    worker: worker.id
  };
}

function enqueue(task) {

  STATE.queue.push(task);

  return {
    queued: true,
    size: STATE.queue.length
  };
}

function processQueue() {

  while (STATE.queue.length) {

    const task = STATE.queue.shift();

    dispatch(task);
  }
}

setInterval(processQueue, 100);

const server =
  http.createServer((req, res) => {

  if (
    req.method === 'POST' &&
    req.url === '/register'
  ) {

    let body = '';

    req.on('data', c => body += c);

    req.on('end', () => {

      try {

        const worker =
          JSON.parse(body);

        registerWorker(worker);

        res.end(JSON.stringify({
          ok: true
        }));

      } catch (e) {

        res.statusCode = 500;

        res.end(JSON.stringify({
          ok: false
        }));
      }
    });

    return;
  }

  if (
    req.method === 'POST' &&
    req.url === '/enqueue'
  ) {

    let body = '';

    req.on('data', c => body += c);

    req.on('end', () => {

      try {

        const task =
          JSON.parse(body);

        enqueue(task);

        res.end(JSON.stringify({
          ok: true,
          queued: task
        }));

      } catch (e) {

        res.statusCode = 500;

        res.end(JSON.stringify({
          ok: false,
          error: e.message
        }));
      }
    });

    return;
  }

  if (
    req.method === 'GET' &&
    req.url === '/health'
  ) {

    return res.end(
      JSON.stringify({
        ok: true,
        workers: STATE.workers.length,
        tasks: STATE.tasks,
        queue: STATE.queue.length
      })
    );
  }

  if (
    req.method === 'GET' &&
    req.url === '/history'
  ) {

    return res.end(
      JSON.stringify(
        STATE.history.slice(-20),
        null,
        2
      )
    );
  }

  res.statusCode = 404;

  res.end();
});

server.listen(7000, () => {

  log('CORE ONLINE :7000');
});
