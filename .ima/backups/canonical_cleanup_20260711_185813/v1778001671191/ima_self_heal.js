
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
