const IMAKernel = require("./kernel");

const kernel = new IMAKernel();

kernel.register("learning", (k) => {
  k.on("boot", () => {
    console.log("📚 learning module booted");
  });

  k.on("tick", (state) => {
    console.log("tick:", state.cycle);
  });
});

kernel.start(process.argv.slice(2));
