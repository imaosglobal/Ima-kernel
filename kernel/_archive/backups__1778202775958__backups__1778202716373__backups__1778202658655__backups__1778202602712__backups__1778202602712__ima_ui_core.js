const brain = require('./ima_brain_hub');

const listeners = {};

function subscribe(user, cb){
  if(!listeners[user]) listeners[user] = [];
  listeners[user].push(cb);
}

function emit(user){
  const state = snapshot(user);
  (listeners[user] || []).forEach(cb => {
    try { cb(state); } catch {}
  });
}

function login(provider, user, device){
  const res = brain.boot(provider, user, device);
  emit(user.email || user);
  return res;
}

function move(user, device){
  const res = brain.move(user, device);
  emit(user);
  return res;
}

function snapshot(user){
  return brain.get(user);
}

module.exports = { subscribe, login, move, snapshot };
