console.log("🚀 IMA BOOTSTRAP START");

const Kernel = require("./kernel");

const ima = new Kernel();

ima.start(process.argv.slice(2));
