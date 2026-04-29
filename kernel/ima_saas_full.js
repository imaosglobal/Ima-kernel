require('dotenv').config();

const express = require("express");
const app = express();

app.use(express.json());

/**
 * =========================
 * CONFIG BOOTSTRAP
 * =========================
 */

const STRIPE_KEY = process.env.STRIPE_SECRET_KEY;

if (!STRIPE_KEY) {
  console.error("Missing Stripe Key");
  process.exit(1);
}

/**
 * =========================
 * STRIPE INIT (SINGLE SOURCE)
 * =========================
 */
const Stripe = require("stripe");
const stripe = new Stripe(STRIPE_KEY);

/**
 * =========================
 * SIMPLE API KEY STORE (TEMP)
 * =========================
 */

const validKeys = {
  demo: { plan: "free", usage: 0 }
};

function checkKey(apiKey) {
  if (!validKeys[apiKey]) return false;

  const limit = validKeys[apiKey].plan === "free" ? 2 : 100000;

  if (validKeys[apiKey].usage >= limit) {
    return "PAY";
  }

  validKeys[apiKey].usage++;
  return true;
}

/**
 * =========================
 * ROUTES
 * =========================
 */

app.post("/run", (req, res) => {
  const key = req.headers["x-api-key"];

  const ok = checkKey(key);

  if (!ok) {
    return res.json({ ok: false, error: "INVALID KEY" });
  }

  if (ok === "PAY") {
    return res.json({ ok: false, error: "PAYMENT REQUIRED" });
  }

  res.json({
    ok: true,
    result: "hello from stable kernel"
  });
});

/**
 * =========================
 * STRIPE TEST ROUTE
 * =========================
 */

app.post("/pay", async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      mode: "payment",
      line_items: [
        {
          price_data: {
            currency: "usd",
            product_data: { name: "Kernel Access" },
            unit_amount: 100
          },
          quantity: 1
        }
      ],
      success_url: "http://localhost:4000/success",
      cancel_url: "http://localhost:4000/cancel"
    });

    res.json({ ok: true, url: session.url });
  } catch (e) {
    res.json({ ok: false, error: e.message });
  }
});

/**
 * =========================
 * START SERVER
 * =========================
 */

const PORT = process.env.PORT || 4000;

app.listen(PORT, () => {
  console.log("KERNEL SAAS RUNNING ON PORT", PORT);
});
