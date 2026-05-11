const api = require('./node_modules/ima-core-saas/api_layer');
const db = require('./node_modules/ima-core-saas/db_memory');

module.exports = {
  handle: (req, cb) => {
    if (req === 'health') return cb(null, api.health());
    if (req.startsWith('user:get:')) {
      const key = req.split(':')[2];
      return db.getUser(key, cb);
    }
    if (req.startsWith('user:create:')) {
      const key = req.split(':')[2];
      return db.createUser(key, cb);
    }
    return cb(null, { error: 'unknown command' });
  }
};
