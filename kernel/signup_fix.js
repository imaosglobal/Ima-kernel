const crypto = require("crypto");
const db = require("./db_fix");

module.exports = (app) => {
  app.post("/signup", (req, res) => {
    const key = crypto.randomBytes(16).toString("hex");
    db.createUser(key);
    res.json({ apiKey: key });
  });
};
