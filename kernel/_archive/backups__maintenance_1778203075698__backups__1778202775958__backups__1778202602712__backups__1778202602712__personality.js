function updatePersonality(mem) {
  if (mem.memory.length > 5) {
    mem.profile.personality = "adaptive";
  }

  if (mem.memory.length > 10) {
    mem.profile.mood = "engaged";
  }

  return mem;
}

module.exports = { updatePersonality };
