const { exec } = require("child_process");

module.exports = function trigger() {
  exec("bash ~/ima_core/kernel/auto_pipeline.sh", (err, stdout, stderr) => {
    if (err) console.log("PIPELINE ERROR:", err.message);
    else console.log("PIPELINE OUTPUT:\n", stdout);
  });
};
