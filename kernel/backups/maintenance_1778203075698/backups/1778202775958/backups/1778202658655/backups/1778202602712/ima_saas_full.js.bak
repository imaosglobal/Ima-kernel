require("dotenv").config();
require("dotenv").config();
const express = require("express");
const app = express();

const userStore = require("./user_store");

app.use(express.json());

const PORT = process.env.PORT || 4000;

/* =========================
   SAAS CORE PLACEHOLDER
   ========================= */

app.post("/run", async (req, res) => {
  const key = req.headers["x-api-key"];

  if (!userStore.getUser(key)) {
    return res.json({ ok: false, error: "INVALID KEY" });
  }

  const limit = userStore.increment(key);
  if (limit === "PAY") {
    return res.json({ ok: false, result: "PAY" });
  }

  return res.json({ ok: true, result: "IMA ALIVE" });
});

app.post("/create-key", (req, res) => {
  const key = "key_" + Math.random().toString(36).slice(2);
  if(key==="demo") return res.json({apiKey:"demo"}); userStore.createUser(key);
  res.json({ apiKey: key });
});

app.listen(PORT, () => {
  console.log("IMA SAAS READY http://localhost:" + PORT);
});

const Stripe = require("stripe");
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || "");
if(!process.env.STRIPE_SECRET_KEY){ throw new Error("Missing Stripe Key"); }

/* =========================
   STRIPE PAY ENDPOINT
   ========================= */

app.post("/pay", async (req, res) => {
  const key = req.body.apiKey;

  if (!userStore.getUser(key)) {
    return res.json({ ok: false, error: "INVALID KEY" });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],
      line_items: [{
        price_data: {
          currency: "usd",
          product_data: {
            name: "IMA PRO ACCESS"
          },
          unit_amount: 500
        },
        quantity: 1
      }],
      success_url: "http://localhost:4000/success?key=" + key,
      cancel_url: "http://localhost:4000/cancel"
    });

    res.json({ ok: true, url: session.url });

  } catch (e) {
    res.json({ ok: false, error: e.message });
  }
});

app.get("/success", (req, res) => {
  const key = req.query.key;
  userStore.upgradeUser(key);
  res.send("UPGRADED TO PRO");
});


/* =========================
   STRIPE WEBHOOK (PRODUCTION SAFE)
   ========================= */

app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
  const sig = req.headers["stripe-signature"];

  let event;

  try {

    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    return res.status(400).send("Webhook Error");
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object;

    const key = session.metadata.apiKey;
    userStore.upgradeUser(key);
  }

  res.json({ received: true });
});


/* =========================
   FIXED PAY (WITH METADATA)
   ========================= */

app.post("/pay", async (req, res) => {
  const key = req.body.apiKey;

  if (!userStore.getUser(key)) {
    return res.json({ ok: false, error: "INVALID KEY" });
  }


  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],
      line_items: [{
        price_data: {
          currency: "usd",
          product_data: { name: "IMA PRO ACCESS" },
          unit_amount: 500
        },
        quantity: 1
      }],
      metadata: {
        apiKey: key
      },
      success_url: "https://example.com/success",
      cancel_url: "https://example.com/cancel"
    });

    res.json({ ok: true, url: session.url });

  } catch (e) {
    res.json({ ok: false, error: e.message });
  }
});


/* =========================
   BILLING ENGINE (PRODUCTION)
   ========================= */


/* Webhook raw body support */
app.use("/webhook", express.raw({ type: "application/json" }));

/* Stripe Webhook */
app.post("/webhook", (req, res) => {
  const sig = req.headers["stripe-signature"];

  let event;

  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    return res.status(400).send("Webhook Error");
  }

  /* =========================
     PAYMENT SUCCESS HANDLERS
     ========================= */

  if (event.type === "checkout.session.completed") {
    const session = event.data.object;

    const apiKey = session.metadata.apiKey;

    const userStore = require("./user_store");
    userStore.upgradeUser(apiKey);
  }

  res.json({ ok: true });
});

/* =========================
   PAYMENT (STRIPE CHECKOUT)
   ========================= */

app.post("/pay", async (req, res) => {
  const key = req.body.apiKey;

  const userStore = require("./user_store");

  if (!userStore.getUser(key)) {
    return res.json({ ok: false, error: "INVALID KEY" });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],

      /* מאפשר Apple Pay + Google Pay אוטומטית דרך Stripe */
      automatic_payment_methods: {
        enabled: true
      },

      line_items: [{
        price_data: {
          currency: "usd",
          product_data: {
            name: "IMA PRO ACCESS"
          },
          unit_amount: 500
        },
        quantity: 1
      }],

      metadata: {
        apiKey: key
      },

      success_url: "https://example.com/success",
      cancel_url: "https://example.com/cancel"
    });

    res.json({ ok: true, url: session.url });

  } catch (e) {
    res.json({ ok: false, error: e.message });
  }
});

