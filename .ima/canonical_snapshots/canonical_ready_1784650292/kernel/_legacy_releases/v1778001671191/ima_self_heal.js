const fs = require('fs');

function heal(){

const required=[
'.ima/runtime/runtime.py',
'learning/meta_orchestrator.py',
'.ima/governance/canonical_architecture.json'
];

required.forEach(f=>{
 if(fs.existsSync(f)){
  console.log('[HEAL OK]',f);
 }else{
  console.log('[HEAL MISSING]',f);
 }
});

console.log('[CANONICAL RELEASE HEAL CHECK]');
}

module.exports={heal};
