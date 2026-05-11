module.exports = (app, db) => {

  app.post("/run", (req, res) => {

    const key = req.headers["x-api-key"];
    const task = req.body?.task;

    if (!task) return res.json({ error: "Missing task" });

    const user = db.getUser(key);
    if (!user) return res.json({ error: "Invalid API key" });

    if (user.plan === "free" && user.usage > 50) {
      return res.json({
        error: "Upgrade required",
        reason: "usage limit reached"
      });
    }

    user.usage++;
    db.updateUser(key, user);

    return res.json({
      ok: true,
      result: "Processed: " + task,
      usage: user.usage
    });
  });

};
