const fs = require('fs');

// load file
let fc = fs.readFileSync('./runtime/FS_CONTROLLER.js','utf8');

// ensure guard import
if (!fc.includes("KERNEL_WRITE_GUARD")) {
  fc = "const GUARD=require('./KERNEL_WRITE_GUARD');\n" + fc;
}

// replace fs.writeFileSync safely (string-based, לא regex מסוכן)
fc = fc.split("fs.writeFileSync").join("GUARD.safeWrite");

// write back safely
fs.writeFileSync('./runtime/FS_CONTROLLER.js', fc);

console.log("FS_CONTROLLER ENFORCED SAFE MODE");
