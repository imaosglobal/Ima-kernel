const TX = require('./KERNEL_TRANSACTION_LAYER');
const ORCH = require('./KERNEL_ORCHESTRATOR_V2');

const EVENT_BUS = {
  queue: [],
  subscribers: {},

  emit(type, payload){
    if(!this.subscribers[type]) return;
    for(const fn of this.subscribers[type]){
      try { fn(payload); } catch(e){}
    }
  },

  on(type, fn){
    if(!this.subscribers[type]) this.subscribers[type] = [];
    this.subscribers[type].push(fn);
  }
};

// --------------------
// Scheduler loop
// --------------------

let running = false;

async function loop(){

  if(running) return;
  running = true;

  const state = TX.load();

  for(const sid of Object.keys(state.sessions || {})){

    const session = state.sessions[sid];

    for(const id of Object.keys(session.graph || {})){

      const node = session.graph[id];

      if(node.status === 'done') continue;

      // retry policy
      if(node.retries === undefined) node.retries = 0;

      try {

        const res = TX.runNode(session, {
          id,
          cmd: node.cmd
        });

        if(res && res.ok){
          node.status = 'done';
          EVENT_BUS.emit('node_done', {sid, id});
        } else {
          throw new Error(res?.error || 'execution_failed');
        }

      } catch(e){

        node.retries++;

        node.error = e.message;

        node.status = node.retries > 2 ? 'failed' : 'retry';

        EVENT_BUS.emit('node_failed', {sid, id, error:e.message});

      }
    }
  }

  TX.save(state);

  running = false;
}

// --------------------
// Public API
// --------------------

function request(cmd){

  const state = TX.load();
  const sid = TX.newSession(state);
  const session = state.sessions[sid];

  const nodeId = ORCH.add(cmd);

  session.graph[nodeId] = {
    cmd,
    status:'pending',
    retries:0
  };

  TX.save(state);

  loop(); // async trigger

  return { session: sid, node: nodeId, status:'queued' };
}

// --------------------
// Healing (manual + automatic retry)
// --------------------

function heal(sessionId){

  const state = TX.load();
  const session = state.sessions?.[sessionId];

  if(!session) return {error:'no_session'};

  let fixed = 0;

  for(const id of Object.keys(session.graph)){

    const node = session.graph[id];

    if(node.status !== 'failed') continue;

    node.status = 'pending';
    node.retries = 0;

    fixed++;
  }

  TX.save(state);

  loop();

  return { healed: fixed };
}

// --------------------

function inspect(sessionId){
  const state = TX.load();
  return state.sessions?.[sessionId] || null;
}

// --------------------

module.exports = {
  request,
  inspect,
  heal,
  EVENT_BUS
};
