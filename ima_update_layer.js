const fs = require("fs");

// מצב נוכחי של המערכת
let state = {
  version: "1.0",
  avatar: "default",
  behavior: "stable"
};

// טעינת קונפיג
function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync("./ima_config.json"));
  } catch {
    return {};
  }
}

// שמירה
function saveConfig(cfg) {
  fs.writeFileSync("./ima_config.json", JSON.stringify(cfg, null, 2));
}

// קבלת "שדרוג"
function applyUpdate(update) {
  console.log("🔄 Checking update...");

  // תנאי בסיסי
  if (!update || !update.version) return state;

  // רק אם גרסה חדשה יותר
  if (update.version > state.version) {
    console.log("🚀 Applying update");

    state = {
      ...state,
      ...update
    };

    saveConfig(state);
  } else {
    console.log("🧠 No update applied");
  }

  return state;
}

// דוגמה לשדרוג חיצוני
const incomingUpdate = {
  version: "1.1",
  avatar: "creative",
  behavior: "adaptive"
};

applyUpdate(incomingUpdate);
