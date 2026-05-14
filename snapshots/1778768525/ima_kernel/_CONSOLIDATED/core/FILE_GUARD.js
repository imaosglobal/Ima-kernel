const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

function hash(content) {
  return crypto.createHash("sha256").update(content).digest("hex");
}

function existsDuplicate(dir, newHash) {
  const files = fs.existsSync(dir) ? fs.readdirSync(dir) : [];

  for (const f of files) {
    const full = path.join(dir, f);
    if (fs.statSync(full).isFile()) {
      const h = hash(fs.readFileSync(full));
      if (h === newHash) return true;
    }
  }
  return false;
}

function createUnique(filePath, content) {
  const dir = path.dirname(filePath);

  const newHash = hash(content);

  if (existsDuplicate(dir, newHash)) {
    return { status: "duplicate", filePath };
  }

  fs.writeFileSync(filePath, content);
  fs.appendFileSync(
    path.join(dir, "file_registry.log"),
    `${filePath} ${newHash}\n`
  );

  return { status: "created", filePath };
}

module.exports = { createUnique };
