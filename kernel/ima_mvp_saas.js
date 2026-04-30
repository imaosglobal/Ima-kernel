require("./env_boot");

const express = require("express");
const crypto = require("crypto");
const Stripe = require("stripe");

const app = express();
app.use(express.json());

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// ===== MEMORY (MVP בלבד) =====
const users = {}; // apiKey → usage
const LIMIT = 10;

// ===== API KEY GENERATOR =====
function genKey() {
  return crypto.randomBytes(16).toString("hex");
}

// ===== SIGNUP =====
app.post("/signup", (req, res) => {
  const key = genKey();
  users[key] = { count: 0, paid: false };
  res.json({ apiKey: key });
});

// ===== RUN =====
app.post("/run", (req, res) => {
  const key = req.headers["x-api-key"];
  const user = users[key];

  if (!user) return res.json({ error: "Invalid API key" });

  if (!user.paid && user.count >= LIMIT) {
    return res.json({ error: "Limit reached", pay: "/pay" });
  }

  user.count++;

  res.json({
    ok: true,
    result: `Processed: ${req.body.task}`
  });
});

// ===== PAY =====
app.post("/pay", async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      mode: "payment",
      line_items: [{
        price_data: {
          currency: "usd",
          product_data: { name: "IMA PRO ACCESS" },
          unit_amount: 500
        },
        quantity: 1
      }],
      success_url: "http://localhost:4000/success",
      cancel_url: "http://localhost:4000/cancel"
    });

    res.json({ url: session.url });
  } catch (e) {
    res.json({ error: e.message });
  }
});

// ===== START =====
app.listen(4000, () => {
  console.log("MVP SAAS RUNNING ON 4000");
});
