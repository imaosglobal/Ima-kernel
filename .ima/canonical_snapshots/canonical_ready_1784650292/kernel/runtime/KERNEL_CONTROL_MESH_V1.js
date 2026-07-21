const ORCH = require('./KERNEL_ORCHESTRATOR_V2');
const TX = require('./KERNEL_TRANSACTION_LAYER');

function request(cmd){

  // 1. create session
  const state = TX.load();
  const sid = TX.newSession(state);

  const session = state.sessions[sid];

  // 2. wrap command into graph node
  const nodeId = ORCH.add(cmd);

  // 3. execute orchestrator
  ORCH.run();

  // 4. transaction layer sync
  TX.runNode(session, {
    id: nodeId,
    cmd
  });

  TX.save(state);

  // 5. return unified response
  return {
    session: sid,
    node: nodeId,
    status: 'processed'
  };
}

module.exports = { request };
