const express = require("express");
const cors = require("cors");
const kernel = require("./kernel/runtime");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/ask", (req, res) => {
  const msg = req.body?.message || "";
  const reply = kernel.run(msg);

  res.json({ reply });
});

app.listen(3000, () => {
  console.log("🧠 IMA KERNEL RUNNING");
});
