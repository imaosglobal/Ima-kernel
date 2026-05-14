const fs = require("fs");

console.log("📦 IMA DISTRIBUTOR START");

// אוסף כל חלקי המערכת
const system = {
  runtime: fs.existsSync("./ima_runtime"),
  brain: fs.existsSync("./ima_brain_v2"),
  product: fs.existsSync("./ima_product_engine")
};

const build = {
  version: Date.now(),
  system
};

fs.writeFileSync(
  "./release.json",
  JSON.stringify(build, null, 2)
);

console.log("✔ Release built");
