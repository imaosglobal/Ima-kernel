const kernel = require("./ima_kernel_os");

const cmd = process.argv[2];

if(cmd === "boot"){
  kernel.boot({ mode: "cli" });

} else if(cmd === "health"){
  console.log(kernel.health());

} else {
  console.log("IMA OS COMMANDS:");
  console.log("boot | health");
}
