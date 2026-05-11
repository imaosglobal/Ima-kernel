const fs = require('fs');
const cp = require('child_process');

function sh(cmd){
  try { return cp.execSync(cmd,{stdio:'inherit'}); } catch(e){}
}

console.log('==============================');
console.log('IMA FULL SYSTEM BOOTSTRAP');
console.log('==============================');

// =====================
// 1. KERNEL CORE
// =====================
fs.writeFileSync('./ima_kernel.js', `
module.exports = {
  run(){ console.log('[KERNEL RUN]'); },
  update(){ console.log('[KERNEL UPDATE]'); },
  deploy(){ console.log('[KERNEL DEPLOY]'); },
  restart(){ console.log('[KERNEL RESTART]'); }
};
`);

// =====================
// 2. AGENT LAYER
// =====================
fs.writeFileSync('./ima_agent.js', `
module.exports = {
  plan(cmd){
    return { cmd, ts:Date.now(), safe:true };
  },
  execute(plan){
    console.log('[AGENT]', plan.cmd);
  }
};
`);

// =====================
// 3. SELF HEALING ENGINE
// =====================
fs.writeFileSync('./ima_self_heal.js', `
const fs = require('fs');

module.exports = {
  analyze(){
    const issues = [];
    const files = fs.readdirSync('.');
    if(!files.includes('ima_kernel.js')) issues.push('missing kernel');
    return issues;
  },

  fix(issues){
    if(issues.length){
      console.log('[HEAL] fixing:', issues);
    } else {
      console.log('[HEAL] system clean');
    }
  }
};
`);

// =====================
// 4. LOOP ENGINE (AGENT BRAIN)
// =====================
fs.writeFileSync('./ima_loop.js', `
const agent = require('./ima_agent.js');
const heal = require('./ima_self_heal.js');

function tick(cmd){
  const plan = agent.plan(cmd);
  agent.execute(plan);

  const issues = heal.analyze();
  heal.fix(issues);
}

module.exports = { tick };
`);

// =====================
// 5. WORLD SERVER
// =====================
fs.writeFileSync('./server.js', `
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
`);

// =====================
// 6. MEMORY
// =====================
fs.writeFileSync('./ima_memory.json','[]');

// =====================
// 7. CLI
// =====================
const cli = (process.env.PREFIX||'') + '/bin/ima';

fs.writeFileSync(cli, `
#!/usr/bin/env node
const kernel = require(process.env.HOME + '/ima_core/kernel/ima_kernel.js');
const loop = require(process.env.HOME + '/ima_core/kernel/ima_loop.js');

const cmd = process.argv[2] || 'run';

loop.tick(cmd);

if(kernel[cmd]) kernel[cmd]();
`);

sh('chmod +x ' + cli);

// =====================
// 8. VERIFY SYSTEM
// =====================
console.log('--- VERIFY ---');

try {
  const k = require('./ima_kernel.js');
  const a = require('./ima_agent.js');
  const l = require('./ima_loop.js');

  console.log('[OK] kernel:', Object.keys(k));
  console.log('[OK] agent ready');
  console.log('[OK] loop ready');
} catch(e){
  console.log('[FAIL]', e.message);
}

// =====================
// 9. START SERVER
// =====================
try {
  require('./server.js');
} catch(e){
  console.log('[SERVER FAIL]', e.message);
}

console.log('==============================');
console.log('BOOT COMPLETE');
console.log('==============================');
