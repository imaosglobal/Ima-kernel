const express = require("express");
const Distribution = require("./ima_distribution");

const app = express();
app.use(express.json());

const dist = new Distribution();

/* Register user */
app.post("/register", (req, res) => {
  const { id, source } = req.body;
  const user = dist.registerUser(id, source);
  res.json(user);
});

/* Track usage */
app.post("/track", (req, res) => {
  const { userId, event } = req.body;
  dist.trackUsage(userId, event);
  res.json({ status: "ok" });
});

/* Referral */
app.post("/referral", (req, res) => {
  const { referrer, newUser } = req.body;
  dist.addReferral(referrer, newUser);
  res.json({ status: "linked" });
});

/* Stats */
app.get("/stats", (req, res) => {
  res.json(dist.getStats());
});

app.listen(3000, () => {
  console.log("🚀 IMA Distribution API running on port 3000");
});
