const fs = require("fs");
const FILE = "./users.json";

function load() {
  if (!fs.existsSync(FILE)) fs.writeFileSync(FILE, "{}");
  return JSON.parse(fs.readFileSync(FILE));
}

function save(data) {
  fs.writeFileSync(FILE, JSON.stringify(data, null, 2));
}

module.exports = {
  getUser: (key, cb) => {
    const db = load();
    cb(null, db[key]);
  },

  createUser: (key, cb) => {
    const db = load();
    db[key] = { usage: 0, plan: "free", createdAt: Date.now() };
    save(db);
    cb(null, db[key]);
  },

  updateUser: (key, data, cb) => {
    const db = load();
    db[key] = data;
    save(db);
    cb(null, data);
  }
};
