
const fs = require("fs");
const crypto = require("crypto");

const FILE = process.env.HOME + "/.bashrc";
const HASH_FILE = process.env.HOME + "/ima_core/kernel/.cli_hash";

let last = null;

function hash() {
  return crypto.createHash("sha256")
    .update(fs.readFileSync(FILE))
    .digest("hex");
}

function getSaved() {
  try {
    return fs.readFileSync(HASH_FILE, "utf8").trim();
  } catch {
    return null;
  }
}

function save(h) {
  fs.writeFileSync(HASH_FILE, h);
}

function check() {
  const current = hash();
  const saved = getSaved();

  if (!saved) {
    save(current);
    last = current;
    console.log("[DAEMON] baseline initialized");
    return;
  }

  if (current !== saved && last !== current) {
    console.log("[DAEMON] CLI MODIFIED DETECTED");
    save(current);
    last = current;
    return;
  }

  last = current;
}

console.log("[DAEMON] running...");

setInterval(check, 4000);

