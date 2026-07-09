const store = require('./store');

module.exports = {
  set: store.set,
  get: store.get,
  dump: store.dump
};
