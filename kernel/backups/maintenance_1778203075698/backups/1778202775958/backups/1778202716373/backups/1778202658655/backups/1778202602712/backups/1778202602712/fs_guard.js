const fs = require("fs");

const VERSION_DIR = "./versions";
const MAIN_FILE = "./server.js";

function backup() {
  const stamp = Date.now();
  fs.copyFileSync(MAIN_FILE, `${VERSION_DIR}/server_${stamp}.js`);
  return stamp;
}

function rollback() {
  const files = fs.readdirSync(VERSION_DIR)
    .filter(f => f.startsWith("server_"))
    .sort()
    .reverse();

  if (files.length === 0) return false;

  const last = files[0];
  fs.copyFileSync(`${VERSION_DIR}/${last}`, MAIN_FILE);
  return true;
}

function safeWrite(file, content) {
  fs.writeFileSync(file, content);

  try {
    require("child_process").execSync(`node -c ${file}`);
    return true;
  } catch (e) {
    console.log("❌ Syntax broken → rollback");
    rollback();
    return false;
  }
}

module.exports = { backup, rollback, safeWrite };
