
const memory = require('./ima_memory_long.js');
const policy = require('./ima_policy.js');
const kernel = require('./ima_kernel.js');

function perceive(input){
  return { input, t: Date.now() };
}

function decide(state){
  // לוגיקה פשוטה — ניתן לשדרג בהמשך
  return { action: state.input, confidence: 0.8 };
}

function act(decision){
  const p = policy.allow(decision.action);
  if(!p.ok){
    return { ok:false, error:p.reason };
  }

  if(kernel[decision.action]){
    kernel[decision.action]();
    return { ok:true };
  }

  return { ok:false, error:'unknown action' };
}

function loopOnce(input){
  const state = perceive(input);
  const decision = decide(state);
  const result = act(decision);

  memory.save({ state, decision, result });
  return result;
}

module.exports = { loopOnce };
