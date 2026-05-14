const fs = require("fs");

/* ---------- CORE ---------- */
class IMA {
  constructor(){
    this.plugins = {};
    this.memory = [];
  }

  register(plugin){
    this.plugins[plugin.name] = plugin;
  }

  ask(input){
    const domain = this.detectDomain(input);

    if(this.plugins[domain]){
      return this.plugins[domain].run(input);
    }

    return this.fallback(input);
  }

  detectDomain(input){
    if(input.includes("כסף")) return "finance";
    if(input.includes("רגש")) return "psychology";
    if(input.includes("קוד")) return "dev";
    return "general";
  }

  fallback(input){
    return {
      answer: `IMA GENERAL RESPONSE: ${input}`
    };
  }

  learn(input, output){
    this.memory.push({ input, output, time: Date.now() });
  }
}

/* ---------- EXPORT (SDK READY) ---------- */
module.exports = { IMA };
