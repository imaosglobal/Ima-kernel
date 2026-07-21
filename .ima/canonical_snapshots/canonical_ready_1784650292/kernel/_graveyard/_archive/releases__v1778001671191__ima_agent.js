
module.exports = {
  plan(cmd){
    return { cmd, ts:Date.now(), safe:true };
  },
  execute(plan){
    console.log('[AGENT]', plan.cmd);
  }
};
