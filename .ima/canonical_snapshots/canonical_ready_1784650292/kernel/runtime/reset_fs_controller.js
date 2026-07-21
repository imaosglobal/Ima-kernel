const fs = require('fs');

let fc = fs.readFileSync('./runtime/FS_CONTROLLER.js','utf8');

// ensure import exists
if (!fc.includes("VERSION=require")) {
  fc = "const VERSION=require('./VERSION_ENGINE');\n" + fc;
}

// hard reset function (no patching, full overwrite)
fc = fc.replace(
  /function updateFile[\s\S]*?}/,
  `function updateFile(filePath, content) {
  if (typeof VERSION !== 'undefined') {
    VERSION.snapshot(filePath);
  }
  return createFile(filePath, content);
}`
);

fs.writeFileSync('./runtime/FS_CONTROLLER.js', fc);

console.log("RESET COMPLETE");
