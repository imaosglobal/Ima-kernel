const fs = require("fs");

module.exports = {
  log: (apiKey, task) => {
    const line = {
      key: apiKey,
      task,
      time: Date.now()
    };

    fs.appendFileSync(
      "./analytics.log",
      JSON.stringify(line) + "\n"
    );
  }
};
