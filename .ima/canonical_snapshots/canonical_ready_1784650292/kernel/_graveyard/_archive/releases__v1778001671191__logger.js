const fs = require("fs");

module.exports = {
  log: (type, data) => {
    fs.appendFileSync(
      "./usage.log",
      JSON.stringify({ type, data, time: Date.now() }) + "\n"
    );
  }
};
