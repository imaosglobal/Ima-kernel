const kernel = require("./ima_kernel_os");

console.log("🚀 IMA OS BOOT SEQUENCE START");

kernel.boot({
  mode: "production",
  debug: false
});
