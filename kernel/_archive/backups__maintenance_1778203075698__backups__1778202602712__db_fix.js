const fs = require("fs");
const path = require("path");

const DB_PATH = path.join(__dirname, "ima_db.json");

function load() {
  if (!fs.existsSync(DB_PATH)) {
    fs.writeFileSync(DB_PATH, JSON.stringify({ users: {} }, null, 2));
  }
  return JSON.parse(fs.readFileSync(DB_PATH));
}

function save(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}

module.exports = {
  createUser: (key) => {
    const db = load();
    db.users[key] = { count: 0, paid: 0 };
    save(db);
  },

  getUser: (key) => {
    const db = load();
    return db.users[key] || null;
  },

  updateUser: (key, data) => {
    const db = load();
    db.users[key] = {
      ...(db.users[key] || {}),
      ...data
    };
    save(db);
  }
};
