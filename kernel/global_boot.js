const express = require("express");
const app = express();

const db = require("./db_memory");

// core parsing
app.use(express.json());

// global layers
require("./api_layer")(app, db);
require("./usage_layer")(app, db);
require("./rate_layer")(app, db);

// RUN endpoint (single contract)
app.post("/run", (req, res) => {

  const key = req.apiKey;
  const task = req.body?.task;

  if (!key) return res.json({ error: "Missing API key" });
  if (!task) return res.json({ error: "Missing task" });

  db.getUser(key, (err, user) => {
    if (!user) return res.json({ error: "Invalid API key" });

    res.json({
      ok: true,
      result: "Processed: " + task,
      usage: user.usage || 0,
      plan: user.plan
    });
  });

});

// signup
app.post("/signup", (req, res) => {
  const key = Math.random().toString(36).substring(2);

  db.createUser(key, () => {
    res.json({ apiKey: key });
  });
});

app.listen(4000, () => {
  console.log("GLOBAL API PRODUCT RUNNING ON 4000");
});
