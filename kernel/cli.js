#!/usr/bin/env node
const http = require('http');
const cmd = process.argv[2] || 'run';
const host = process.env.IMA_HOST || 'localhost';

http.get('http://' + host + ':4000/' + cmd, res => {
  res.pipe(process.stdout);
}).on('error', () => {
  console.log('server not reachable');
});
