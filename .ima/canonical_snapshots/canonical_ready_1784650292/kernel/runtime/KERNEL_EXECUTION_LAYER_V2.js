const fs = require('fs');
const crypto = require('crypto');
const G = require('./KERNEL_API_GATEWAY');

const PATH = './runtime/.exec_store.json';

function empty(){
  return { commands: {}, results: {} };
}

function load(){
  try { return JSON.parse(fs.readFileSync(PATH,'utf8')); }
  catch { return empty(); }
}

function save(s){
  fs.writeFileSync(PATH, JSON.stringify(s,null,2));
}

function hash(cmd){
  return crypto.createHash('sha256')
    .update(JSON.stringify(cmd))
    .digest('hex');
}

function validate(cmd){
  if(!cmd || !cmd.type) return {ok:false};
  return {ok:true};
}

function execute(cmd){

  const v = validate(cmd);
  if(!v.ok) return {status:'rejected'};

  const store = load();
  const id = hash(cmd);

  // idempotency
  if(store.results[id]){
    return store.results[id];
  }

  store.commands[id] = cmd;

  let res;
  try{
    res = G.request(cmd);
  }catch(e){
    res = {status:'error', reason:e.message};
  }

  store.results[id] = res;
  save(store);

  return res;
}

function replay(){

  const store = load();
  const results = [];

  for(const id of Object.keys(store.commands)){
    const cmd = store.commands[id];

    try{
      const r = G.request(cmd);
      results.push({id, cmd, result:r});
    }catch(e){
      results.push({id, cmd, error:e.message});
    }
  }

  return {
    replayed: results.length,
    results
  };
}

function status(){
  const s = load();
  return {
    commands: Object.keys(s.commands).length,
    results: Object.keys(s.results).length
  };
}

module.exports = {
  execute,
  replay,
  status
};
