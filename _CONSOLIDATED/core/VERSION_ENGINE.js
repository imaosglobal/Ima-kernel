const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function hash(c) {
  return crypto.createHash("sha256").update(c).digest("hex");
}

function snapshot(filePath) {
  if (!fs.existsSync(filePath)) return null;

  const content = fs.readFileSync(filePath, "utf8");
  const dir = path.dirname(filePath);

  const snapDir = path.join(dir, ".snapshots");
  fs.mkdirSync(snapDir, { recursive: true });

  const version = Date.now();
  const snapPath = path.join(snapDir, `${path.basename(filePath)}.${version}.bak`);

  fs.writeFileSync(snapPath, content);

  return { filePath, snapshot: snapPath, hash: hash(content) };
}

module.exports = { snapshot };
