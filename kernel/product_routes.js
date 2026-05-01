const express = require("express");
const router = express.Router();

router.get("/products", (req, res) => {
  res.json({ ok: true, products: [] });
});

module.exports = router;
