const core = require("./ima_evolving_core");

const input = process.argv.slice(2).join(" ") || "test";

const result = core.run(input);

console.log("🧠 IMA EVOLVING CORE");
console.log(JSON.stringify(result, null, 2));

core.save();
