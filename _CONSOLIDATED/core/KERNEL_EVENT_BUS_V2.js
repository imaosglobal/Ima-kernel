const fs = require('fs');
const crypto = require('crypto');

const LOG_PATH = './runtime/.event_log.json';

function load(){
  try { return JSON.parse(fs.readFileSync(LOG_PATH,'utf8')); }
  catch { return []; }
}

function save(log){
  fs.writeFileSync(LOG_PATH, JSON.stringify(log,null,2));
}

function emit(type, payload){
  const log = load();

  const id = crypto.createHash('sha256')
    .update(JSON.stringify(payload))
    .digest('hex');

  const exists = log.find(e => e.id === id);
  if(exists) return exists;

  const event = {
    id,
    type,
    payload,
    ts: Date.now()
  };

  log.push(event);
  save(log);

  return event;
}

function all(){
  return load();
}

module.exports = { emit, all };
