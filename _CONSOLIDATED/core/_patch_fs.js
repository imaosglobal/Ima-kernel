const fs = require('fs');

let fc = fs.readFileSync('./runtime/FS_CONTROLLER.js','utf8');

// ensure VERSION import
if (!fc.includes("VERSION_ENGINE")) {
  fc = "const VERSION=require('./VERSION_ENGINE');\n" + fc;
}

// patch updateFile safely
if (fc.includes("function updateFile") && !fc.includes("snapshot(filePath)")) {
  fc = fc.replace(
    "function updateFile(filePath, content)",
    "function updateFile(filePath, content) {\n  VERSION.snapshot(filePath);"
  );
}

// fix broken brace if injected incorrectly
fc = fc.replace(
  "function updateFile(filePath, content) {\n  VERSION.snapshot(filePath);",
  "function updateFile(filePath, content) {\n  VERSION.snapshot(filePath);\n"
);

fs.writeFileSync('./runtime/FS_CONTROLLER.js', fc);

console.log("FS_CONTROLLER PATCHED OK");
