const OpenAI = require("openai");

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// ---------------- GPT REAL ----------------
async function gpt(input) {
  const res = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You are IMA, a learning system." },
      { role: "user", content: input }
    ]
  });

  return res.choices[0].message.content;
}

// ---------------- PLACEHOLDERS ----------------
async function claude(input) {
  return `Claude (not connected yet): ${input}`;
}

async function gemini(input) {
  return `Gemini (not connected yet): ${input}`;
}

module.exports = { gpt, claude, gemini };
