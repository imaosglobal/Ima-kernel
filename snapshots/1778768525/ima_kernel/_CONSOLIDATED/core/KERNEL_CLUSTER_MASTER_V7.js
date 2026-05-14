const cluster = require('cluster');
const os = require('os');
const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

const WORKERS = 2;
const STATE = {
  sessions: {},
  queue: []
};

function newSession() {
  const id = Date.now().toString();
  STATE.sessions[id] = {
    graph: {},
    executed: {},
    failed: false,
    history: []
  };
  return id;
}

function runWorkerLogic() {
  cluster.on('message', (worker, msg) => {
    if (!msg || !msg.cmd) return;

    const session = STATE.sessions[msg.session];
    if (!session) return;

    const nodeId = msg.nodeId;

    try {
      const res = EXEC.execute(msg.cmd);

      session.executed[nodeId] = true;
      session.graph[nodeId].status = 'done';
      session.graph[nodeId].result = res;
      session.history.push({ id: nodeId, res });

      worker.send({ ok: true, nodeId });
    } catch (e) {
      session.graph[nodeId].status = 'failed';
      session.failed = true;

      worker.send({ ok: false, error: e.message });
    }
  });
}

function start() {
  if (cluster.isPrimary) {
    console.log('[MASTER] starting cluster:', WORKERS);

    for (let i = 0; i < WORKERS; i++) {
      cluster.fork({ WORKER_ID: i });
    }

    runWorkerLogic();
  } else {
    process.on('message', (msg) => {
      process.send(msg);
    });
  }
}

function request(cmd) {
  const sessionId = newSession();

  const nodeId = require('crypto')
    .createHash('sha256')
    .update(JSON.stringify(cmd) + Math.random())
    .digest('hex');

  STATE.sessions[sessionId].graph[nodeId] = {
    cmd,
    status: 'queued'
  };

  const workerIds = Object.keys(cluster.workers || {});
  const w = cluster.workers?.[workerIds[0]];

  if (w) {
    w.send({ cmd, nodeId, session: sessionId });
  }

  return { session: sessionId, node: nodeId };
}

function inspect(sessionId) {
  return STATE.sessions[sessionId];
}

function metrics() {
  return {
    workers: Object.keys(cluster.workers || {}).length,
    sessions: Object.keys(STATE.sessions).length
  };
}

module.exports = { start, request, inspect, metrics };
