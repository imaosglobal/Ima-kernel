
module.exports = {
  plan(cmd){ return {cmd, ts:Date.now()}; },
  execute(p){ console.log('[AGENT]', p.cmd); }
};
