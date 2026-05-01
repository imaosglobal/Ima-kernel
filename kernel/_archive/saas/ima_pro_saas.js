const app = require("./bootstrap_fix");
const db = require("./db_fix");

const crypto = require("crypto");

/* ======================
   SIGNUP
====================== */
app.post("/signup", (req, res) => {
  const key = crypto.randomBytes(16).toString("hex");
  db.createUser(key);
  res.json({ apiKey: key });
});

/* ======================
   RUN
====================== */
app.post("/run", (req, res) => {
console.log("BODY:", req.body);
  const body = req.body || {};
  const task = body.task;
  const key = req.headers["x-api-key"];

  if (!task) return res.json({ error: "Missing task" });

  const user = db.getUser(key);
  if (!user) return res.json({ error: "Invalid API key" });

  if (!user.paid && user.count >= 10) {
    return res.json({ error: "Limit reached", pay: "/pay" });
  }

  db.updateUser(key, { count: user.count + 1 });

  res.json({
    ok: true,
    result: "Processed: " + task
  });
});

/* ======================
   PAY (stub)
====================== */
app.post("/pay", (req, res) => {
  res.json({ url: "https://checkout.stripe.com/..." });
});

/* ======================
   START
====================== */
app.listen(4000, () => {
  console.log("KERNEL SAAS RUNNING ON PORT 4000");
});
require("./signup_fix")(app);
const { ensureUser } = require("./db_extend");
require("./run_patch")(app, require("./db_fix"));
require("./plugin_loader")(app, require("./db_fix"));
require("./plugins/default_processor")(app, require("./db_fix"));
