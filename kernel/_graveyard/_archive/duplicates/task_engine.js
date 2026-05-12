const fs = require("fs");

const DB = "./tasks.db.json";

function load() {
  try { return JSON.parse(fs.readFileSync(DB)); }
  catch { return { queue: [], done: [] }; }
}

function save(d) {
  fs.writeFileSync(DB, JSON.stringify(d, null, 2));
}

function addTask(task) {
  const db = load();
  db.queue.push({
    id: Date.now().toString(),
    task,
    status: "pending",
    created: Date.now()
  });
  save(db);
}

function getQueue() {
  return load().queue;
}

function completeTask(id, result) {
  const db = load();

  const task = db.queue.find(t => t.id === id);
  if (!task) return;

  db.queue = db.queue.filter(t => t.id !== id);

  db.done.push({
    ...task,
    result,
    finished: Date.now()
  });

  save(db);
}

module.exports = {
  addTask,
  getQueue,
  completeTask
};
