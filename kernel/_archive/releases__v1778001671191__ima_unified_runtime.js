const guard = require('./ima_dependency_guard');
guard.assert();
const identity = require('./ima_identity');
const sync = require('./ima_unified_sync');
const network = require('./ima_network_layer');

function boot(provider, user, device){

  const id = user.email || user.name;

  const login = identity.login(provider, user);

  network.register(id, device);

  sync.set(id, 'identity', login);
  sync.set(id, 'device', device);
  sync.set(id, 'session', {
    active: true,
    ts: Date.now()
  });

  return {
    user: id,
    device,
    state: sync.snapshot(id),
    devices: network.list(id)
  };
}

function move(userId, newDevice){

  network.switchDevice(userId, newDevice);

  sync.set(userId, 'device', newDevice);
  sync.set(userId, 'session', {
    ...sync.snapshot(userId).session,
    movedTo: newDevice,
    ts: Date.now()
  });

  return {
    state: sync.snapshot(userId),
    devices: network.list(userId)
  };
}

function snapshot(userId){
  return {
    state: sync.snapshot(userId),
    devices: network.list(userId)
  };
}

module.exports = { boot, move, snapshot };
