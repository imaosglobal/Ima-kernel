const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();
app.use(cors());
app.use(express.json());

const FILE = "./memory.json";

// ---------- load ----------
function loadMemory() {
  try {
    return JSON.parse(fs.readFileSync(FILE));
  } catch {
    return {
      profile: { name: "אורי", mood: "calm", personality: "neutral" },
      memory: []
    };
  }
}

// ---------- save ----------
function saveMemory(m) {
  fs.writeFileSync(FILE, JSON.stringify(m, null, 2));
}

// ---------- decay system ----------
function decay(mem) {
  mem.memory.forEach(m => {
    m.weight = Math.max(0.1, (m.weight || 0.5) * 0.98);
  });
}

// ---------- memory update ----------
function remember(text, mem) {
  const msg = text.trim();

  let value = msg;
  let type = "fact";

  if (msg.includes("קוראים לי")) {
    value = msg.split("קוראים לי")[1]?.trim();
    type = "identity";
    mem.profile.name = value;
  }

  if (msg.includes("אני אוהב")) {
    value = msg.split("אני אוהב")[1]?.trim();
    type = "preference";
  }

  let found = mem.memory.find(m => m.value === value);

  if (found) {
    found.hits = (found.hits || 0) + 1;
    found.weight = Math.min(1, (found.weight || 0.5) + 0.15);
    found.lastUsed = Date.now();
  } else {
    mem.memory.push({
      value,
      type,
      weight: 0.5,
      hits: 1,
      created: Date.now(),
      lastUsed: Date.now()
    });
  }

  decay(mem);
  updatePersonality(mem);
  saveMemory(mem);
}

// ---------- personality engine ----------
function updatePersonality(mem) {
  const prefs = mem.memory.filter(m => m.type === "preference");

  const music = prefs.filter(p => p.value.includes("מוזיקה")).length;
  const social = prefs.length;

  if (music >= 2) {
    mem.profile.personality = "creative";
    mem.profile.mood = "inspired";
  } else if (social >= 4) {
    mem.profile.personality = "expressive";
    mem.profile.mood = "active";
  } else if (social === 0) {
    mem.profile.personality = "neutral";
    mem.profile.mood = "calm";
  } else {
    mem.profile.personality = "curious";
  }
}

// ---------- intent ----------
function detectIntent(msg) {
  const t = (msg || "").replace(/s/g, "");

  if (t.includes("מהאתזוכר")) return "memory";
  if (t.includes("מההאישיותשלך") || t.includes("איזהאישיות")) return "personality";
  if (t.includes("איךקוראיםלי")) return "identity";
  if (t.startsWith("imaremember")) return "remember";

  return "chat";
}

// ---------- respond ----------
function respond(intent, msg, mem) {
  const name = mem.profile?.name || "אורי";

  if (intent === "memory") {
    const list = mem.memory
      .filter(m => m && m.value)
      .sort((a,b)=>(b.weight + b.hits) - (a.weight + a.hits));

    return list.length
      ? list.map(m => `${m.value}(${(m.weight||0).toFixed(2)})`).join(" | ")
      : "אין זיכרון";
  }

  if (intent === "personality") {
    return `אני ${mem.profile.personality} (מצב: ${mem.profile.mood})`;
  }

  if (intent === "identity") {
    return `קוראים לך ${name}`;
  }

  return `אני איתך ${name}`;
}

// ---------- API ----------
app.post("/ask", (req, res) => {
  const msg = (req.body?.message || "").trim();
  const mem = loadMemory();

  const intent = detectIntent(msg);

  if (intent === "remember") {
    remember(msg.replace(/ima remember/i, ""), mem);
    return res.json({ reply: "נשמר ✔" });
  }

  const reply = respond(intent, msg, mem);

  saveMemory(mem);

  res.json({
    reply,
    intent,
    mood: mem.profile.mood,
    personality: mem.profile.personality
  });
});

app.listen(3000, () => {
  console.log("IMA LIVE PERSONALITY SYSTEM RUNNING");
});
