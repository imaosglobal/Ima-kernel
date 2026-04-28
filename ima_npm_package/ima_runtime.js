const engine = require("./ima_engine");

class IMARuntime {
  constructor(engine) {
    this.engine = engine;
    this.queue = [];
  }

  start() {
    console.log("🚀 IMA RUNTIME STARTED");

    setInterval(() => {
      this.tick();
    }, 2000);
  }

  tick() {
    const event = {
      type: "tick",
      time: Date.now()
    };

    this.engine.remember("system_tick", event);

    console.log(this.engine.ask("learn system evolution"));
  }

  send(input) {
    this.queue.push(input);
    console.log(this.engine.ask(input));
  }
}

/* BOOT */

const runtime = new IMARuntime(engine);
runtime.start();

module.exports = runtime;