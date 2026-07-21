const fs = require('fs');

const file = './ima_unified_runtime.js';
let f = fs.readFileSync(file, 'utf8');

if (!f.includes('ima_dependency_guard')) {
  f = `const guard = require('./ima_dependency_guard');\nguard.assert();\n` + f;
}

fs.writeFileSync(file, f);

console.log('[GUARD ATTACHED SAFE]');
