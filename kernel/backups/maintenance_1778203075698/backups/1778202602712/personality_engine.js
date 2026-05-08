function update(mem) {
  const prefs = mem.memory.filter(m => m.type === "preference");

  const music = prefs.filter(p => p.value.includes("מוזיקה")).length;

  if (music >= 2) {
    mem.profile.personality = "creative";
    mem.profile.mood = "inspired";
  } else if (prefs.length > 3) {
    mem.profile.personality = "curious";
    mem.profile.mood = "active";
  } else {
    mem.profile.personality = "neutral";
    mem.profile.mood = "calm";
  }

  return mem;
}

module.exports = { update };
