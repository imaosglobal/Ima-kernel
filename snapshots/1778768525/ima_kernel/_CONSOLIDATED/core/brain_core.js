const memory = require("./memory_engine");

function decide(input, mem) {
  const text = input.toLowerCase();

  const state = {
    intent: "chat",
    actions: []
  };

  // זיכרון בסיסי משפיע
  if (mem.memory && mem.memory.length > 20) {
    state.context = "experienced_user";
  }

  // החלטות פשוטות (שלב 1 בלבד)
  if (text.includes("קנה") || text.includes("מוצר")) {
    state.intent = "commerce";
    state.actions.push("open_store");
  }

  if (text.includes("למד")) {
    state.intent = "learning";
    state.actions.push("activate_learning");
  }

  if (text.includes("זכור")) {
    state.actions.push("store_memory");
  }

  return state;
}

module.exports = { decide };
