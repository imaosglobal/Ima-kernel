const rt = require('./ima_unified_runtime');

const memory = {};

function boot(provider, user, device){
  const id = user.email || user;
  const res = rt.boot(provider, user, device);

  memory[id] = {
    session: res.state,
    devices: res.devices,
    updated: Date.now()
  };

  return memory[id];
}

function move(userId, device){
  const res = rt.move(userId, device);

  memory[userId] = {
    session: res.state,
    devices: res.devices,
    updated: Date.now()
  };

  return memory[userId];
}

function get(userId){
  return memory[userId] || null;
}

module.exports = { boot, move, get };
