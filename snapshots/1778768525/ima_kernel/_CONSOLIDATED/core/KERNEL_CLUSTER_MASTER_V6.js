const cluster = require('cluster');
const os = require('os');
const TX = require('./KERNEL_TRANSACTION_LAYER');

const WORKERS = Math.max(2, os.cpus().length - 1);

const QUEUE = [];

function enqueue(job){ QUEUE.push(job); }
function dequeue(){ return QUEUE.shift(); }

function dispatch(job){

  const state = TX.load();
  const session = state.sessions?.[job.sessionId];
  if(!session) return;

  const node = session.graph[job.nodeId];
  if(!node) return;

  try {
    const res = TX.runNode(session, {
      id: job.nodeId,
      cmd: job.cmd
    });

    node.status = res?.ok ? 'done' : 'failed';
    node.result = res;

  } catch(e){
    node.status = 'failed';
    node.error = e.message;

    if(!job.retry){
      job.retry = true;
      enqueue(job);
    }
  }

  TX.save(state);
}

// --------------------
// MASTER LOOP
// --------------------

function masterLoop(){

  setInterval(() => {

    const job = dequeue();
    if(job) dispatch(job);

  }, 80);
}

// --------------------
// WORKER
// --------------------

function worker(){

  process.on('message', (msg) => {

    if(msg.type === 'JOB'){
      const TX = require('./KERNEL_TRANSACTION_LAYER');

      const state = TX.load();
      const session = state.sessions?.[msg.job.sessionId];

      if(!session) return;

      const res = TX.runNode(session, {
        id: msg.job.nodeId,
        cmd: msg.job.cmd
      });

      session.graph[msg.job.nodeId].status = res?.ok ? 'done' : 'failed';

      TX.save(state);

      process.send({ type:'DONE' });
    }
  });
}

// --------------------
// START (FIXED)
// --------------------

function start(){

  if(cluster.isPrimary){

    console.log('[MASTER] starting cluster:', WORKERS);

    cluster.setupPrimary({
      exec: __filename   // 🔥 FIX: חשוב מאוד
    });

    for(let i=0;i<WORKERS;i++){
      const w = cluster.fork();

      w.on('message', (msg) => {
        if(msg.type === 'DONE'){
          // ok
        }
      });
    }

    masterLoop();

  } else {
    worker();
  }
}

// --------------------
// API
// --------------------

const ORCH = require('./KERNEL_ORCHESTRATOR_V2');

function request(cmd){

  const state = TX.load();
  const sid = TX.newSession(state);
  const session = state.sessions[sid];

  const nodeId = ORCH.add(cmd);

  session.graph[nodeId] = {
    cmd,
    status:'queued'
  };

  const job = { sessionId: sid, nodeId, cmd };

  enqueue(job);
  TX.save(state);

  return { session: sid, node: nodeId, status:'queued' };
}

function inspect(id){
  const state = TX.load();
  return state.sessions?.[id] || null;
}

module.exports = { start, request, inspect };
