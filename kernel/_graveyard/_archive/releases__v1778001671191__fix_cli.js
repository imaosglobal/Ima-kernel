const fs=require('fs');

const cli='/data/data/com.termux/files/usr/bin/ima';

let f=fs.readFileSync(cli,'utf8');

f = f.replace(
  /const engine = require\\(.+\\);/,
  `const engine = require('/data/data/com.termux/files/home/ima_core/kernel/ima_engine_final.js');`
);

fs.writeFileSync(cli,f);
console.log('[CLI HARD FIX APPLIED]');
