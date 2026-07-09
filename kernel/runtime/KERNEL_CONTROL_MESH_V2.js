const ORCH = require('./KERNEL_ORCHESTRATOR_V2');
const TX = require('./KERNEL_TRANSACTION_LAYER');

function request(cmd){

  // 1. load global state (single source of truth)
  const state = TX.load();

  const sid = TX.newSession(state);
  const session = state.sessions[sid];

  // 2. create node in orchestrator BUT bind to session
  const nodeId = ORCH.add(cmd);

  // attach execution context into session graph
  session.graph[nodeId] = {
    cmd,
    status: 'pending'
  };

  // 3. run orchestrator (still global, but now session-aware)
  ORCH.run();

  // 4. execute only within session boundary
  const node = session.graph[nodeId];

  const result = TX.runNode(session, {
    id: nodeId,
    cmd
  });

  // update session state
  if(result && result.ok) {
    node.status = 'done';
    session.executed[nodeId] = true;
  } else {
    node.status = 'failed';
    session.failed = true;
  }

  // 5. persist single truth
  TX.save(state);

  return {
    session: sid,
    node: nodeId,
    status: result?.ok ? 'success' : 'failed',
    result
  };
}

function inspect(sessionId){
  const state = TX.load();
  return state.sessions?.[sessionId] || null;
}

function replay(sessionId){
  const state = TX.load();
  const session = state.sessions?.[sessionId];

  if(!session) return {error:'no_session'};

  const results = [];

  for(const id of Object.keys(session.graph)){
    const node = session.graph[id];
    const r = TX.runNode(session, { id, cmd: node.cmd });
    results.push({id, r});
  }

  TX.save(state);

  return {replayed: results.length, results};
}

module.exports = { request, inspect, replay };
