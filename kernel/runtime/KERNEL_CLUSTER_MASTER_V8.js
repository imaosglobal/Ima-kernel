const cluster = require('cluster');
const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');
const crypto = require('crypto');

const WORKERS = 2;

const STATE = {
  sessions: {}
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
  if (cluster.isPrimary) {
    console.log('[MASTER] starting cluster:', WORKERS);

    const workerFile = require('path').join(__dirname, 'KERNEL_CLUSTER_WORKER_BOOT.js');

    for (let i = 0; i < WORKERS; i++) {
      cluster.fork({
        WORKER_ID: String(i),
        WORKER_BOOT: workerFile
      });
    }

    cluster.on('message', (worker, msg) => {
      const session = STATE.sessions[msg.session];
      if (!session) return;

      const nodeId = msg.nodeId;

      try {
        const res = EXEC.execute(msg.cmd);

        session.graph[nodeId].status = 'done';
        session.executed[nodeId] = true;
        session.history.push({ id: nodeId, res });

        worker.send({ ok: true, nodeId });
      } catch (e) {
        session.graph[nodeId].status = 'failed';
        session.failed = true;

        worker.send({ ok: false, error: e.message });
      }
    });

  } else {
    // fallback worker mode (לא אמור לקרות אם boot נכון)
    require(process.env.WORKER_BOOT);
  }
}

function request(cmd) {
  const sessionId = newSession();

  const nodeId = crypto
    .createHash('sha256')
    .update(JSON.stringify(cmd) + Date.now())
    .digest('hex');

  STATE.sessions[sessionId].graph[nodeId] = {
    cmd,
    status: 'queued'
  };

  const worker = Object.values(cluster.workers || {})[0];
  if (worker) {
    worker.send({ cmd, nodeId, session: sessionId });
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
