const runtime = require("./autonomous_runtime");

console.log("SUPERVISOR ONLINE");

if (runtime && runtime.start) {
  runtime.start();
}
