const fs = require('fs');

let fc = fs.readFileSync('./runtime/FS_CONTROLLER.js','utf8');

// ensure VERSION import
if (!fc.includes("VERSION_ENGINE")) {
  fc = "const VERSION=require('./VERSION_ENGINE');\n" + fc;
}

// FULL SAFE REWRITE of updateFile (no regex traps)
const newFn =
`function updateFile(filePath, content) {
  VERSION.snapshot(filePath);
  return createFile(filePath, content);
}`;

fc = fc.replace(/function updateFile\\([^]*?\\}/, newFn);

// write back
fs.writeFileSync('./runtime/FS_CONTROLLER.js', fc);

console.log("FS_CONTROLLER FIXED OK");
