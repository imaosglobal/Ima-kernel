const fs = require('fs');

const ACTIVE = require('./KERNEL_CONSOLIDATION_ENGINE_V1').inspect();

function safeRequire(path){
  try { return require(path); }
  catch(e){ return { __error: e.message }; }
}

function validateModule(name, path){
  const mod = safeRequire(path);

  const result = {
    name,
    path,
    ok: true,
    errors: []
  };

  // 1. must not fail loading
  if(mod.__error){
    result.ok = false;
    result.errors.push('LOAD_FAIL: ' + mod.__error);
    return result;
  }

  // 2. must expose expected interface (soft contract)
  const expected = {
    eventBus: ['all'],
    tx: ['load', 'save'],
    orchestrator: ['add', 'run'],
    execution: ['execute'],
    cluster: ['start', 'request']
  };

  const role = Object.keys(ACTIVE.active).find(k =>
    ACTIVE.active[k] && ACTIVE.active[k].includes(path)
  );

  if(role && expected[role]){
    for(const fn of expected[role]){
      if(typeof mod[fn] !== 'function'){
        result.ok = false;
        result.errors.push(`MISSING_METHOD: ${fn}`);
      }
    }
  }

  return result;
}

function run(){
  const modules = ACTIVE.active;

  const report = Object.entries(modules).map(([role,path]) =>
    validateModule(role, path)
  );

  const failed = report.filter(r => !r.ok);

  return {
    ok: failed.length === 0,
    failed,
    total: report.length
  };
}

module.exports = { run };
