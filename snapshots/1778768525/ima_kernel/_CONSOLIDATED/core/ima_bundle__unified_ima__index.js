console.log("IMA UNIFIED SYSTEM BOOT");

const fs = require("fs");
const path = require("path");

const modules = fs.readdirSync(__dirname)
  .filter(x => fs.lstatSync(x).isDirectory());

console.log("Loaded modules:", modules);

modules.forEach(m => {
  try {
    const mod = require("./" + m);
    if (mod.init) mod.init();
  } catch (e) {
    console.log("Module failed:", m, e.message);
  }
});
