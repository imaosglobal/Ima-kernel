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

function append(event){
  const log = load();
  log.push(event);
  save(log);
}

function emit(type, payload){
  const event = {
    id: crypto.randomUUID(),
    type,
    payload,
    ts: Date.now()
  };

  append(event);
  return event;
}

function all(){
  return load();
}

module.exports = {
  emit,
  all
};
