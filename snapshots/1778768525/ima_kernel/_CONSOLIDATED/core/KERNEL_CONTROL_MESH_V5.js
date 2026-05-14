const fs = require('fs');
const TX = require('./KERNEL_TRANSACTION_LAYER');
const ORCH = require('./KERNEL_ORCHESTRATOR_V2');

const QUEUE_PATH = './runtime/.mesh_v5_queue.json';

// --------------------
// persistence queue
// --------------------

function load(){
  try { return JSON.parse(fs.readFileSync(QUEUE_PATH,'utf8')); }
  catch { return {queue:[], locked:false}; }
}

function save(s){
  fs.writeFileSync(QUEUE_PATH, JSON.stringify(s,null,2));
}

// --------------------
// worker pool
// --------------------

const WORKERS = 3;
let running = false;

// --------------------
// lock safe dequeue
// --------------------

function takeJob(state){
  if(state.locked) return null;

  state.locked = true;
  save(state);

  const job = state.queue.shift();

  state.locked = false;
  save(state);

  return job;
}

// --------------------
// execution core
// --------------------

function execute(job){

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
    node.traceId = job.traceId;
    node.result = res;

  } catch(e){

    node.status = 'failed';
    node.error = e.message;

  }

  TX.save(state);
}

// --------------------
// worker loop
// --------------------

function workerLoop(workerId){

  const state = load();

  const job = takeJob(state);
  if(!job) return;

  job.workerId = workerId;
  job.ts = Date.now();

  execute(job);
}

// --------------------
// scheduler
// --------------------

function start(){

  if(running) return;
  running = true;

  setInterval(() => {

    for(let i=0;i<WORKERS;i++){
      workerLoop(i);
    }

  }, 50);
}

// --------------------
// API
// --------------------

function request(cmd){

  const state = TX.load();
  const sid = TX.newSession(state);
  const session = state.sessions[sid];

  const nodeId = ORCH.add(cmd);

  const job = {
    sessionId: sid,
    nodeId,
    cmd,
    traceId: 'tr_' + Date.now() + '_' + Math.random().toString(16).slice(2)
  };

  session.graph[nodeId] = {
    cmd,
    status:'queued',
    traceId: job.traceId
  };

  const q = load();
  q.queue.push(job);
  save(q);

  TX.save(state);

  return {
    session: sid,
    node: nodeId,
    traceId: job.traceId,
    status:'queued'
  };
}

function inspect(sessionId){
  const state = TX.load();
  return state.sessions?.[sessionId] || null;
}

function metrics(){

  const q = load();
  return {
    queueLength: q.queue.length,
    workers: WORKERS,
    locked: q.locked
  };
}

module.exports = {
  request,
  inspect,
  start,
  metrics
};
