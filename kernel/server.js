const express = require("express");
const app = express();
const db = require("./db_memory");

app.use(express.json());

app.post("/signup", (req, res) => {
  const key = Math.random().toString(36).substring(2);

  db.createUser(key, () => {
    res.json({ apiKey: key });
  });
});

app.post("/run", (req, res) => {
  const key = req.headers["x-api-key"];
  const task = req.body?.task;

  if (!key) return res.json({ error: "Missing API key" });
  if (!task) return res.json({ error: "Missing task" });

  db.getUser(key, (err, user) => {
    if (!user) return res.json({ error: "Invalid API key" });

    if (user.plan !== "paid" && user.usage >= 100) {
      return res.json({ error: "Limit reached (upgrade required)" });
    }

    user.usage++;

    db.updateUser(key, user, () => {
      res.json({
        ok: true,
        result: "Processed: " + task,
        usage: user.usage,
        plan: user.plan
      });
    });
  });
});

require("./run_bridge")(app);
require("./run_bridge")(app);
app.listen(4000, () => {
  console.log("SAAS RUNNING ON 4000");
});
