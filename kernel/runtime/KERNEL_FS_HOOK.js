const fs = require('fs');
const GUARD = require('./KERNEL_WRITE_GUARD');

// backup original
const rawWrite = fs.writeFileSync;

// override global write
fs.writeFileSync = function(path, content, ...args) {
  return GUARD.safeWrite(path, content);
};

console.log("FS HOOK ACTIVE");
module.exports = {};
