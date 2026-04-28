const fs = require("fs");
const path = require("path");

module.exports = (kernel) => {
  const dir = "./modules";

  fs.readdirSync(dir).forEach(file => {
    const mod = require(path.join(__dirname, dir, file));
    if (typeof mod === "function") mod(kernel);
  });
};
