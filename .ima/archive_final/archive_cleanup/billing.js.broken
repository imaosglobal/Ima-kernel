const Stripe = require("stripe");
const stripe = new Stripe(process.env.STRIPE_KEY);

module.exports = {
  checkout: async (userId) => {
    return stripe.checkout.sessions.create({
      mode: "payment",
      success_url: "http://localhost:4000/success",
      cancel_url: "http://localhost:4000/cancel"
    });
  }
};
