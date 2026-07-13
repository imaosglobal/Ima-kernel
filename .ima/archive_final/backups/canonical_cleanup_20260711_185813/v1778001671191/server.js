
const http = require('http');
const kernel = require('./ima_kernel.js');
const loop = require('./ima_loop.js');

http.createServer((req,res)=>{
  const cmd = req.url.slice(1) || 'run';

  loop.tick(cmd);

  if(kernel[cmd]) kernel[cmd]();

  res.end(JSON.stringify({ ok:true, cmd }));
}).listen(4000,'0.0.0.0',()=>{
  console.log('[WORLD ACTIVE]');
});
