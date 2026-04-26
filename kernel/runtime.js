const memory = require("./memory_engine");
const personality = require("./personality_engine");

function run(msg) {
  const mem = memory.load();

  const text = msg.toLowerCase();

  if (text.includes("קוראים לי")) {
    const name = msg.split("קוראים לי")[1]?.trim();
    mem.profile.name = name;
    memory.addMemory(mem, name, "identity");
  }

  if (text.includes("אני אוהב")) {
    const pref = msg.split("אני אוהב")[1]?.trim();
    memory.addMemory(mem, pref, "preference");
  }

  personality.update(mem);
  memory.save(mem);

  const name = mem.profile.name;

  if (text.includes("מה אתה זוכר")) {
    return mem.memory
      .sort((a,b)=>(b.weight+b.hits)-(a.weight+a.hits))
      .slice(0,5)
      .map(m => m.value)
      .join(" | ");
  }

  return `אני איתך ${name}`;
}

module.exports = { run };
