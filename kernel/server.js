
const http = require('http');
const runtime = require('./ima_runtime.js');
const memory = require('./ima_memory_long.js');

http.createServer((req,res)=>{
  const cmd = req.url.replace('/','') || 'run';

  if(cmd === 'memory'){
    return res.end(JSON.stringify(memory.last(20)));
  }

  const out = runtime.loopOnce(cmd);
  res.end(JSON.stringify(out));
}).listen(4000,'0.0.0.0',()=>console.log('[API LIVE :4000]'));
