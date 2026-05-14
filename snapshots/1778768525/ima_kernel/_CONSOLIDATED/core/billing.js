module.exports = (app, db) => {

  app.use((req, res, next) => {
    req.userKey = req.headers["x-api-key"];
    next();
  });

  app.post("/run", (req, res, next) => {
    const key = req.headers["x-api-key"];
    const task = req.body?.task;

    if (!key) return res.json({ error: "Missing API key" });
    if (!task) return res.json({ error: "Missing task" });

    const user = db.getUser(key);
    if (!user) return res.json({ error: "Invalid API key" });

    if (!user.usage) user.usage = 0;
    if (!user.plan) user.plan = "free";

    if (user.plan !== "paid" && user.usage >= 100) {
      return res.json({ error: "Upgrade required" });
    }

    user.usage++;
    db.updateUser(key, user);

    // attach for next layer
    req._processed = {
      ok: true,
      result: "Processed: " + task,
      usage: user.usage,
      plan: user.plan
    };

    next();
  });

};
