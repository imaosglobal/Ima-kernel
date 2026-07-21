const fs = require('fs');
const TX = require('./KERNEL_TRANSACTION_LAYER');
const ORCH = require('./KERNEL_ORCHESTRATOR_V2');

const QUEUE_PATH = './runtime/.mesh_queue.json';
const DLQ_PATH = './runtime/.mesh_dlq.json';

// --------------------
// persistence
// --------------------

function load(file, fallback){
  try { return JSON.parse(fs.readFileSync(file,'utf8')); }
  catch { return fallback; }
}

function save(file, data){
  fs.writeFileSync(file, JSON.stringify(data,null,2));
}

// --------------------
// queues
// --------------------

function enqueue(job){
  const q = load(QUEUE_PATH, []);
  q.push(job);
  save(QUEUE_PATH, q);
}

function dequeue(){
  const q = load(QUEUE_PATH, []);
  const job = q.shift();
  save(QUEUE_PATH, q);
  return job;
}

function pushDLQ(job){
  const d = load(DLQ_PATH, []);
  d.push(job);
  save(DLQ_PATH, d);
}

// --------------------
// policy layer
// --------------------

function policy(cmd){
  if(!cmd || !cmd.type) return {ok:false, reason:'invalid_cmd'};

  // simple guardrails
  if(cmd.type === 'DELETE_FS') {
    return {ok:false, reason:'forbidden_operation'};
  }

  return {ok:true};
}

// --------------------
// worker engine
// --------------------

function worker(){

  const job = dequeue();
  if(!job) return;

  const {sessionId, nodeId, cmd} = job;

  const state = TX.load();
  const session = state.sessions?.[sessionId];

  if(!session) return;

  const node = session.graph[nodeId];
  if(!node) return;

  const p = policy(cmd);
  if(!p.ok){
    node.status = 'rejected';
    node.error = p.reason;
    pushDLQ(job);
    TX.save(state);
    return;
  }

  try {

    const res = TX.runNode(session, {
      id: nodeId,
      cmd
    });

    if(res && res.ok){
      node.status = 'done';
    } else {
      throw new Error(res?.error || 'execution_failed');
    }

  } catch(e){

    node.retries = (node.retries || 0) + 1;
    node.error = e.message;

    if(node.retries > 2){
      node.status = 'dead';
      pushDLQ(job);
    } else {
      node.status = 'retry';
      enqueue(job);
    }
  }

  TX.save(state);
}

// --------------------
// scheduler loop
// --------------------

let running = false;

function start(){

  if(running) return;
  running = true;

  setInterval(worker, 100); // distributed-like tick

}

// --------------------
// API
// --------------------

function request(cmd){

  const state = TX.load();
  const sid = TX.newSession(state);
  const session = state.sessions[sid];

  const nodeId = ORCH.add(cmd);

  session.graph[nodeId] = {
    cmd,
    status:'queued',
    retries:0
  };

  enqueue({sessionId:sid, nodeId, cmd});

  TX.save(state);

  return {
    session: sid,
    node: nodeId,
    status:'queued'
  };
}

function inspect(sessionId){
  const state = TX.load();
  return state.sessions?.[sessionId] || null;
}

function dlq(){
  return load(DLQ_PATH, []);
}

module.exports = {
  request,
  inspect,
  start,
  dlq
};
