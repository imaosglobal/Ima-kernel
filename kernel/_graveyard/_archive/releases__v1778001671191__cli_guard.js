
const fs = require("fs");
const crypto = require("crypto");

const FILE = process.env.HOME + "/.bashrc";
const HASH_FILE = process.env.HOME + "/ima_core/kernel/.cli_hash";

function hash() {
  return crypto.createHash("sha256")
    .update(fs.readFileSync(FILE))
    .digest("hex");
}

function check() {
  if (!fs.existsSync(HASH_FILE)) return true;

  const old = fs.readFileSync(HASH_FILE, "utf8").trim();
  const now = hash();

  if (old !== now) {
    console.log("[CLI GUARD] MODIFIED");
    return false;
  }

  return true;
}

module.exports = { check };

