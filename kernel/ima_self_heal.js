
const fs = require('fs');

function heal(){
  const required = ['ima_kernel.js','ima_runtime.js','ima_policy.js'];

  required.forEach(f=>{
    if(!fs.existsSync(f)){
      console.log('[HEAL] missing',f);
    }
  });

  console.log('[HEAL CHECK DONE]');
}

module.exports = { heal };
