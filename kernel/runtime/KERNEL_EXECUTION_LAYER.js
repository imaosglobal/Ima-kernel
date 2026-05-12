const fs = require('fs');

const G = require('./KERNEL_API_GATEWAY');

const LOG_PATH = './runtime/.execution_log.json';

function loadLog(){
  try { return JSON.parse(fs.readFileSync(LOG_PATH,'utf8')); }
  catch { return []; }
}

function saveLog(log){
  fs.writeFileSync(LOG_PATH, JSON.stringify(log,null,2));
}

function append(entry){
  const log = loadLog();
  log.push(entry);
  saveLog(log);
}

function validate(cmd){
  if(!cmd || !cmd.type) return {ok:false, reason:'missing_type'};
  return {ok:true};
}

function execute(cmd){

  const validation = validate(cmd);
  if(!validation.ok){
    return {status:'rejected', reason:validation.reason};
  }

  const entry = {
    id: Date.now(),
    cmd,
    ts: Date.now()
  };

  append(entry);

  const res = G.request(cmd);

  append({
    id: entry.id,
    result: res,
    ts: Date.now()
  });

  return res;
}

function replay(filterType){

  const log = loadLog();
  const cmds = log.filter(x => x.cmd && (!filterType || x.cmd.type === filterType));

  const results = [];

  for(const e of cmds){
    try{
      const r = G.request(e.cmd);
      results.push({cmd: e.cmd, result: r});
    }catch(err){
      results.push({cmd: e.cmd, error: err.message});
    }
  }

  return {
    replayed: results.length,
    results
  };
}

function status(){
  const log = loadLog();
  return {
    entries: log.length,
    last: log[log.length - 1] || null
  };
}

module.exports = {
  execute,
  replay,
  status
};
