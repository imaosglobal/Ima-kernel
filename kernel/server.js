
const http = require('http');
const k = require('./ima_kernel.js');
const a = require('./ima_agent.js');

http.createServer((req,res)=>{
  const cmd = req.url.slice(1) || 'run';
  const plan = a.plan(cmd);
  a.execute(plan);

  if(k[cmd]) k[cmd]();
  res.end(JSON.stringify({ok:true,cmd}));
}).listen(4000,'0.0.0.0',()=>{
  console.log('[WORLD ON :4000]');
});
