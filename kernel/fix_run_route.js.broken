module.exports = function(app, db) {

  app.post("/run", (req, res) => {
    const key = req.headers["x-api-key"];
    const task = req.body?.task;

    if (!key) {
      return res.json({ error: "Missing API key" });
    }

    if (!task) {
      return res.json({ error: "Missing task" });
    }

    db.getUser(key, (err, user) => {
      if (err || !user) {
        return res.json({ error: "Invalid API key" });
      }

      user.usage = (user.usage || 0) + 1;

      db.updateUser(key, user, () => {
        return res.json({
          ok: true,
          result: "Processed: " + task,
          usage: user.usage,
          plan: user.plan || "free"
        });
      });
    });

  });

};
EOFgrep -q "IMA_LOG" ~/ima_core/kernel/apply_fix.js || cat >> ~/ima_core/kernel/apply_fix.js << 'EOF'

app.use((req, res, next) => {
  console.log("[IMA_LOG]", req.method, req.url);
  next();
});
EOFgrep -q "IMA_LOG" ~/ima_core/kernel/apply_fix.js || cat >> ~/ima_core/kernel/apply_fix.js << 'EOF'

app.use((req, res, next) => {
  console.log("[IMA_LOG]", req.method, req.url);
  next();
});
