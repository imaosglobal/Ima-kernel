const db = require("./db_fix");

function ensureUser(key) {
  const user = db.getUser(key);
  if (!user) return null;

  if (!user.usage) user.usage = 0;
  if (!user.plan) user.plan = "free";

  db.updateUser(key, user);
  return user;
}

module.exports = { ensureUser };
