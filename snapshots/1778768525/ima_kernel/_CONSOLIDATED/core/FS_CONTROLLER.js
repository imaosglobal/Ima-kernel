const GUARD=require('./KERNEL_WRITE_GUARD');
const VERSION=require('./VERSION_ENGINE');
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function hash(content) {
  return crypto.createHash("sha256").update(content).digest("hex");
}

function loadRegistry(dir) {
  const regPath = path.join(dir, "file_registry.log");
  if (!fs.existsSync(regPath)) return {};
  
  const lines = fs.readFileSync(regPath, "utf8").trim().split("\n");
  const map = {};
  
  for (const line of lines) {
    const [file, h] = line.split(" ");
    if (file && h) map[file] = h;
  }
  
  return map;
}

function writeRegistry(dir, file, h) {
  fs.appendFileSync(path.join(dir, "file_registry.log"), `${file} ${h}\n`);
}

function createFile(filePath, content) {
  const dir = path.dirname(filePath);
  const registry = loadRegistry(dir);

  const newHash = hash(content);

  // 1. אם אותו hash כבר קיים → דילוג
  if (Object.values(registry).includes(newHash)) {
    return { status: "duplicate_hash", filePath };
  }

  // 2. אם קובץ קיים עם אותו שם
  if (fs.existsSync(filePath)) {
    const existingHash = hash(fs.readFileSync(filePath));
    if (existingHash === newHash) {
      return { status: "duplicate_file", filePath };
    }
  }

  // 3. כתיבה
  GUARD.safeWrite(filePath, content);
  writeRegistry(dir, filePath, newHash);

  return { status: "created", filePath };
}

function updateFile(filePath, content) {
  if (typeof VERSION !== 'undefined') {
    VERSION.snapshot(filePath);
  }
  return createFile(filePath, content);
}

function safeDelete(filePath) {
  if (!fs.existsSync(filePath)) return { status: "not_found" };

  fs.unlinkSync(filePath);
  return { status: "deleted", filePath };
}

module.exports = {
  createFile,
  updateFile,
  safeDelete
};
