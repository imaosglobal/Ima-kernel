'use strict';

const cluster = require('cluster');
const path = require('path');
const crypto = require('crypto');

const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

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
  if (!cluster.isPrimary) return;

  const workerPath = path.join(__dirname, 'KERNEL_CLUSTER_WORKER_BOOT.js');

  cluster.setupPrimary({ exec: workerPath });

  console.log('[MASTER] starting cluster:', WORKERS);

  for (let i = 0; i < WORKERS; i++) {
    const worker = cluster.fork({ WORKER_ID: String(i) });

    worker.on('message', (msg) => {

      const session = STATE.sessions[msg.session];
      if (!session) return;

      const node = session.graph[msg.nodeId];
      if (!node) return;

      try {
        const res = EXEC.execute(msg.cmd);

        node.status = 'done';
        node.result = res;

        session.executed[msg.nodeId] = true;
        session.history.push({ id: msg.nodeId, res });

      } catch (e) {
        node.status = 'failed';
        node.error = e.message;
        session.failed = true;
      }
    });
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
    status: 'queued',
    result: null,
    error: null
  };

  const workers = Object.values(cluster.workers || {});
  const worker = workers[0];

  if (worker) {
    worker.send({
      session: sessionId,
      nodeId,
      cmd
    });
  }

  return { session: sessionId, nodeId };
}

function metrics() {
  return {
    sessions: Object.keys(STATE.sessions).length
  };
}

module.exports = { start, request, metrics };
