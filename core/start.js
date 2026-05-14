'use strict';

const path = require('path');

const mode = process.argv[2];

if (mode === 'core') {
  require('./mesh/core.js');
}

if (mode === 'worker') {
  require('./workers/worker_http.js');
}

if (!mode) {
  console.log('usage: node index.js [core|worker]');
}
