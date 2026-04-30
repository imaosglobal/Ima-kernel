const { addTask, getQueue } = require("./task_engine");

module.exports = function(app) {

  app.post("/v2/task", (req, res) => {
    const task = req.body?.task;
    if (!task) return res.status(400).json({ error: "missing task" });

    addTask(task);

    res.json({ ok: true, status: "queued" });
  });

  app.get("/v2/queue", (req, res) => {
    res.json({ queue: getQueue() });
  });

};
