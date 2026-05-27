const express = require("express");
const app = express();

const { load, save, addMemory } = require("./kernel/core/memory");

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "alive", time: Date.now() });
});

app.get("/", (req, res) => {
  try {
    const mem = load();
    addMemory(mem, "ping " + Date.now(), "interaction");
    save(mem);

    res.json({
      status: "IMA LIVE",
      memorySize: mem.memory.length
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.listen(3000, () => {
  console.log("🧠 IMA KERNEL RUNNING");
});

const knowledge = require("./kernel/knowledge_engine");

app.post("/ask", (req, res) => {
  try {
    const input = req.body.input || "";
    const result = knowledge.handle(input);
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});
