const fs = require('fs');

function heal(){
  const required = [
    '.ima/runtime/runtime.py',
    'learning/meta_orchestrator.py',
    '.ima/governance/canonical_architecture.json'
  ];

  required.forEach(f=>{
    if(!fs.existsSync(f)){
      console.log('[HEAL] missing canonical', f);
    } else {
      console.log('[HEAL] OK', f);
    }
  });

  console.log('[CANONICAL HEAL CHECK DONE]');
}

module.exports = { heal };
