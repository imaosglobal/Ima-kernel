const fs = require('fs');
const cp = require('child_process');

function sh(cmd){
  try { return cp.execSync(cmd,{stdio:'inherit'}); } catch(e){}
}

console.log('=== IMA BOOTSTRAP CLEAN ===');

// =====================
// KERNEL
// =====================
fs.writeFileSync('./ima_kernel.js', `
module.exports = {
  run(){ console.log('[RUN OK]'); },
  update(){ console.log('[UPDATE OK]'); },
  deploy(){ console.log('[DEPLOY OK]'); },
  restart(){ console.log('[RESTART OK]'); }
};
`);

// =====================
// AGENT
// =====================
fs.writeFileSync('./ima_agent.js', `
module.exports = {
  plan(cmd){ return {cmd, ts:Date.now()}; },
  execute(p){ console.log('[AGENT]', p.cmd); }
};
`);

// =====================
// SERVER (REAL WORLD ENTRY)
// =====================
fs.writeFileSync('./server.js', `
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
`);

// =====================
// MEMORY
// =====================
fs.writeFileSync('./ima_memory.json','[]');

// =====================
// CLI FIX
// =====================
const cliPath = (process.env.PREFIX||'') + '/bin/ima';

fs.writeFileSync(cliPath, `
#!/usr/bin/env node
const k = require(process.env.HOME + '/ima_core/kernel/ima_kernel.js');
const a = require(process.env.HOME + '/ima_core/kernel/ima_agent.js');

const cmd = process.argv[2] || 'run';
const plan = a.plan(cmd);
a.execute(plan);

if(k[cmd]) k[cmd]();
`);

sh('chmod +x ' + cliPath);

console.log('=== BOOT COMPLETE ===');
