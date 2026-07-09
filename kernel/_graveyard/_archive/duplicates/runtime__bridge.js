const device = require('./ima_device_layer');
const reactive = require('./ima_reactive');
const events = require('./ima_events');
const identity = require('./ima_identity');
const sync = require('./ima_sync');
const devices = require('./ima_devices');

module.exports = { events, reactive, device,
  identity,
  sync,
  devices
};
