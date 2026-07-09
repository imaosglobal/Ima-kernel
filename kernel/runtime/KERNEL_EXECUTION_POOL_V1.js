const { Worker } = require('worker_threads');
const crypto = require('crypto');
const path = require('path');

const WORKERS = 2;

const STATE = {
  sessions: {},
  workers: []
};

function newSession() {
  const id = Date.now().toString();
  STATE.sessions[id] = {
    graph: {},
    executed: {},
    history: [],
    failed: false
  };
  return id;
}

function start() {
  console.log('[POOL] starting workers:', WORKERS);

  for (let i = 0; i < WORKERS; i++) {
    const w = new Worker(path.join(__dirname, 'KERNEL_WORKER_V1.js'));

    w.on('message', (msg) => {
      const s = STATE.sessions[msg.session];
      if (!s) return;

      const node = s.graph[msg.nodeId];
      if (!node) return;

      if (msg.error) {
        node.status = 'failed';
        s.failed = true;
      } else {
        node.status = 'done';
        s.executed[msg.nodeId] = true;
        s.history.push(msg);
      }
    });

    STATE.workers.push(w);
  }
}

let rr = 0;

function request(cmd) {
  const session = newSession();

  const nodeId = crypto
    .createHash('sha256')
    .update(JSON.stringify(cmd) + Date.now())
    .digest('hex');

  STATE.sessions[session].graph[nodeId] = {
    cmd,
    status: 'queued'
  };

  const worker = STATE.workers[rr++ % STATE.workers.length];

  worker.postMessage({
    session,
    nodeId,
    cmd
  });

  return { session, node: nodeId };
}

function inspect(session) {
  return STATE.sessions[session];
}

function metrics() {
  return {
    workers: STATE.workers.length,
    sessions: Object.keys(STATE.sessions).length
  };
}

module.exports = { start, request, inspect, metrics };
