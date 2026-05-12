const fs = require('fs');
const crypto = require('crypto');

const STATE_PATH = './runtime/.tx_engine_state.json';

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_PATH,'utf8')); }
  catch {
    return {
      transactions: {},
      committed: [],
      failed: []
    };
  }
}

function save(s){
  fs.writeFileSync(STATE_PATH, JSON.stringify(s,null,2));
}

function newTx(cmd){
  return {
    id: crypto.randomUUID(),
    cmd,
    status: 'pending',
    createdAt: Date.now()
  };
}

function begin(state, cmd){
  const tx = newTx(cmd);
  state.transactions[tx.id] = tx;
  return tx;
}

function markCommitted(state, txId, result){
  const tx = state.transactions[txId];
  if (!tx) return;

  tx.status = 'committed';
  tx.result = result;

  state.committed.push(tx);
}

function markFailed(state, txId, error){
  const tx = state.transactions[txId];
  if (!tx) return;

  tx.status = 'failed';
  tx.error = error;

  state.failed.push(tx);
}

module.exports = {
  load,
  save,
  begin,
  markCommitted,
  markFailed
};
