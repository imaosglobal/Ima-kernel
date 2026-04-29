const express = require("express");
const app = express();

const { load, save, addMemory } = require("./kernel/memory_engine");
const stability = require("./kernel/stability");

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
