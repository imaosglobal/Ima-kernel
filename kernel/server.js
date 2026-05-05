
const http = require('http');
const runtime = require('./ima_runtime.js');
const heal = require('./ima_self_heal.js');

heal.heal();

const server = http.createServer((req,res)=>{
  const cmd = req.url.replace('/','') || 'run';

  if(cmd === 'health'){
    return res.end(JSON.stringify({ok:true}));
  }

  const result = runtime.loopOnce(cmd);

  res.end(JSON.stringify(result));
});

server.listen(4000,'0.0.0.0',()=>{
  console.log('[SERVER STABLE 4000]');
});
