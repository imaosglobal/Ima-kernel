const fs = require("fs");
const path = require("path");
const EventEmitter = require("events");

class IMAEngine extends EventEmitter {
  constructor() {
    super();

    this.version = "2.0.0";
    this.root = process.cwd();

    this.state = {
      plugins: {},
      memory: this.loadMemory(),
      startedAt: Date.now()
    };
  }

  memoryFile() {
    return path.join(this.root, "ima_memory.json");
  }

  loadMemory() {
    try {
      if (fs.existsSync(this.memoryFile())) {
        return JSON.parse(fs.readFileSync(this.memoryFile(), "utf8"));
      }
    } catch (e) {}

    return { events: [] };
  }

  saveMemory() {
    fs.writeFileSync(
      this.memoryFile(),
      JSON.stringify(this.state.memory, null, 2)
    );
  }

  remember(type, data) {
    this.state.memory.events.push({
      type,
      data,
      time: new Date().toISOString()
    });

    this.saveMemory();
  }

  registerPlugin(name, fn) {
    this.state.plugins[name] = fn;
  }

  runPlugin(name, input) {
    if (!this.state.plugins[name]) return `Plugin not found: ${name}`;
    return this.state.plugins[name](input, this);
  }

  ask(input) {
    this.remember("query", input);

    if (input.includes("finance")) {
      return this.runPlugin("finance", input);
    }

    if (input.includes("learn")) {
      return this.runPlugin("learning", input);
    }

    return `IMA_ENGINE_RESPONSE: ${input}`;
  }

  cli(argv) {
    const input = argv.slice(2).join(" ");

    if (!input) {
      console.log("IMA ENGINE READY");
      console.log(this.info());
      return;
    }

    console.log(this.ask(input));
  }

  info() {
    return {
      version: this.version,
      plugins: Object.keys(this.state.plugins),
      events: this.state.memory.events.length
    };
  }

  boot() {
    this.emit("boot");
  }
}

/* ---------------- BOOTSTRAP ---------------- */

const engine = new IMAEngine();

engine.boot();

engine.registerPlugin("finance", (input) =>
  `📊 FINANCE ENGINE ACTIVE → ${input}`
);

engine.registerPlugin("learning", (input) =>
  `📚 LEARNING ENGINE ACTIVE → ${input}`
);

engine.cli(process.argv);

module.exports = engine;
