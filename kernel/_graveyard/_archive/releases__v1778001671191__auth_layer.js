const fs = require("fs");

const DB_PATH = "./users.db.json";

function loadDB() {
  try {
    return JSON.parse(fs.readFileSync(DB_PATH));
  } catch {
    return {};
  }
}

function saveDB(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}

function createUser() {
  const db = loadDB();
  const key = Math.random().toString(36).substring(2, 14);

  db[key] = {
    created: Date.now(),
    memory: [],
    usage: 0
  };

  saveDB(db);
  return key;
}

function auth(key) {
  const db = loadDB();
  return db[key] || null;
}

function appendMemory(key, task, result) {
  const db = loadDB();
  if (!db[key]) return;

  db[key].memory.push({ task, result, t: Date.now() });
  db[key].usage++;

  saveDB(db);
}

module.exports = {
  createUser,
  auth,
  appendMemory
};
