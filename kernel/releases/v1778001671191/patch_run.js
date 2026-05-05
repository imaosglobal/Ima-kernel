const personality = require("./ima_personality");

module.exports = function(app, db) {

  app.post("/run", (req, res) => {
    const key = req.headers["x-api-key"];
    const task = req.body?.task;

    if (!key) return res.json({ error: "Missing API key" });
    if (!task) return res.json({ error: "Missing task" });

    db.getUser(key, (err, user) => {
      if (!user) return res.json({ error: "Invalid API key" });

      const response = personality(task, { key });

      user.usage = (user.usage || 0) + 1;

      db.updateUser(key, user, () => {
        res.json({
          ok: true,
          result: response.message,
          meta: {
            tone: response.tone
          }
        });
      });
    });

  });

};
