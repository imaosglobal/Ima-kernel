const fs = require("fs");
const { execSync } = require("child_process");
const { runTest } = require("./ima_benchmark");

function backup() {
  fs.copyFileSync("server.js", "server.js.bak");
}

function restore() {
  fs.copyFileSync("server.js.bak", "server.js");
}

function evolve() {
  console.log("🧠 EVOLUTION START");

  const before = runTest();

  // הרץ שיפור
  execSync("node ima_smart_patch.js");

  const after = runTest();

  console.log("📊 BEFORE:", before);
  console.log("📊 AFTER:", after);

  if (after > before) {
    console.log("🛑 WORSE → ROLLBACK");
    restore();
  } else {
    console.log("🚀 IMPROVED → KEEP");
    execSync("git add server.js");
    execSync(`git commit -m "evolution success ${Date.now()}"`);
    execSync("git push");
  }

  console.log("✅ EVOLUTION DONE");
}

evolve();
