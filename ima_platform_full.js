const fs = require("fs");
const { execSync } = require("child_process");

/* CORE */
class IMA {
  constructor(){
    this.memory = [];
    this.mode = "stable";
  }

  ask(q){
    const result = `IMA: ${q}`;

    this.memory.push({q, result, t:Date.now()});
    if(this.memory.length > 200) this.memory.shift();

    this.adapt();
    return result;
  }

  adapt(){
    if(this.memory.length > 50) this.mode = "adaptive";
    if(this.memory.length > 120) this.mode = "creative";
  }
}

/* RUN */
const ima = new IMA();

const input = process.argv.slice(2).join(" ") || "test";

const out = ima.ask(input);

try {
  execSync("git add .");
  execSync(`git commit -m "IMA update ${Date.now()}"`);
  execSync("git push origin main");
} catch(e){}

console.log("🧠 MODE:", ima.mode);
console.log("💬", out);
