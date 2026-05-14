const EventEmitter = require("events");

class IMACore extends EventEmitter {
  constructor() {
    super();

    this.state = {
      cycle: 0,
      mood: 0,
      memory: [],
      patterns: {},
      sync: { status: "idle", last: null }
    };
  }

  tick() {
    this.state.cycle++;

    // mood לא רנדום - תלוי זיכרון
    const memoryFactor = this.state.memory.length * 0.01;
    this.state.mood = Math.sin(this.state.cycle * 0.01) + memoryFactor;

    this.emit("tick", this.state);
  }

  learn(input) {
    const entry = {
      value: input,
      time: Date.now()
    };

    this.state.memory.push(entry);

    // pattern tracking
    this.state.patterns[input] =
      (this.state.patterns[input] || 0) + 1;

    this.emit("learn", entry);
  }

  sync() {
    this.state.sync.status = "syncing";
    this.state.sync.last = Date.now();
    this.state.sync.status = "done";
  }

  start() {
    setInterval(() => this.tick(), 200);
    setInterval(() => this.sync(), 5000);
    console.log("IMA CORE LIVE (EVOLVING)");
  }
}

module.exports = new IMACore();
