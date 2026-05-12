const express = require("express");
const router = express.Router();

router.post("/task", (req, res) => {
  res.json({ ok: true, task: req.body.task });
});

router.get("/queue", (req, res) => {
  res.json({ queue: [] });
});

module.exports = router;
