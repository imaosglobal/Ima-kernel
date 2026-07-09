const express = require("express");
const app = express();

const memory = require("./memory");
const personality = require("./ima_personality");
const analyzeIntent = require("./intent_engine");
const feedbackPatch = require("./feedback_patch");

app.use(express.json());

feedbackPatch(app);

app.post("/signup", (req, res) => {
  const key = req.body?.fixed || Math.random().toString(36).substring(2);
  memory.createUser(key);
  res.json({ apiKey: key });
});

app.post("/run", (req, res) => {

  const key = req.headers["x-api-key"];
  const task = req.body?.task;

  if (!key) return res.json({ error: "Missing API key" });

  const user = memory.getUser(key);
  if (!user) return res.json({ error: "Invalid API key" });

  memory.addEvent(key, { task });

  const ctx = memory.getContext(key);
  const intent = analyzeIntent(task, ctx);

  const response = personality(task, {
    usage: ctx.usage,
    inferredNeed: intent.inferredNeed,
    improvementMode: ctx.improvementMode
  });

  res.json({
    ok: true,
    result: response.message,
    improvement: response.improvement,
    meta: {
      tone: response.tone,
      intent: intent.intent
    },
    usage: ctx.usage,
    memory_size: ctx.historySize
  });
});

module.exports = app;
