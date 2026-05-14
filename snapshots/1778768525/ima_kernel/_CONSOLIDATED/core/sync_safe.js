const fs = require("fs");
const { execSync } = require("child_process");

console.log("📡 IMA SAFE SYNC ENGINE");

function run(cmd) {
  return execSync(cmd).toString().trim();
}

// 1. init git אם צריך
if (!fs.existsSync(".git")) {
  console.log("🧱 Initializing git repo...");
  run("git init");
}

// 2. add
console.log("📦 Staging files...");
run("git add .");

// 3. commit
try {
  run('git commit -m "IMA sync commit"');
  console.log("✔ Commit created");
} catch (e) {
  console.log("⚠️ Nothing to commit or already up to date");
}

// 4. check remote
try {
  const remote = run("git remote -v");
  console.log("🔗 Remote:", remote);
} catch {
  console.log("⚠️ No remote configured yet");
  console.log("👉 You must add:");
  console.log("git remote add origin <YOUR_REPO_URL>");
}

console.log("✔ SYNC READY (not pushed automatically)");
