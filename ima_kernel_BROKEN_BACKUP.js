class IMAKernel {
  constructor() {
    this.events = {};
    this.events = {};
    this.version = "2.0.0";
    this.plugins = {};
    this.memory = {
      logs: [],
      state: {
        cycle: 0,
        alive: false,
        lastTick: null
      }
    };

    this.loopHandle = null;
  }

  /* -------------------------
     CORE EVENTS
  ------------------------- */

  log(event) {
    this.memory.logs.push({
      time: Date.now(),
      ...event
    });
  }

  register(name, fn) {
    this.plugins[name] = fn;
    this.log({ type: "plugin_registered", name });
  }

  runPlugin(name, input) {
    if (!this.plugins[name]) {
      return `PLUGIN NOT FOUND: ${name}`;
    }
    return this.plugins[name](input);
  }

  ask(query) {
    this.log({ type: "query", query });

    if (query.includes("finance")) {
      return this.runPlugin("finance", query);
    }

    if (query.includes("learn")) {
      return this.runPlugin("learning", query);
    }

    return `IMA RESPONSE → ${query}`;
  }

  /* -------------------------
     RUNTIME LOOP (החלק החשוב)
  ------------------------- */

  
  on(event, fn) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(fn);
  }

  emit(event, data) {
    const list = this.events[event] || [];
    for (const fn of list) fn(data);
  }

  tick() {
    this.memory.state.cycle++; this.emit('tick', this.memory.state);
    this.memory.state.lastTick = Date.now();

    this.log({
      type: "tick",
      cycle: this.memory.state.cycle
    });

    // כאן בעתיד ייכנס: learning / sync / evolution
  }

  startLoop() {
    if (this.loopHandle) return;

    this.memory.state.alive = true;

    this.loopHandle = setInterval(() => {
      this.
  on(event, fn) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(fn);
  }

  emit(event, data) {
    const list = this.events[event] || [];
    for (const fn of list) fn(data);
  }

  tick();
    }, 1000);

    console.log("🔁 IMA LOOP STARTED");
  }

  stopLoop() {
    clearInterval(this.loopHandle);
    this.loopHandle = null;
    this.memory.state.alive = false;

    console.log("⛔ IMA LOOP STOPPED");
  }

  /* -------------------------
     BOOT
  ------------------------- */

  boot() {
    console.log("🚀 IMA KERNEL BOOTING...");

    this.startLoop();

    this.register("finance", (input) => {
      return "📊 FINANCE MODULE → " + input;
    });

    this.register("learning", (input) => {
      return "📚 LEARNING MODULE → " + input;
    });

    console.log("✅ IMA KERNEL READY");
  }

  /* -------------------------
     CLI
  ------------------------- */

  cli(args) {
    const input = args.slice(2).join(" ");

    if (!input) {
      console.log("IMA READY");
      return;
    }

    console.log(this.ask(input));
  }

  /* -------------------------
     DEBUG INFO
  ------------------------- */

  info() {
    return {
      version: this.version,
      plugins: Object.keys(this.plugins),
      cycles: this.memory.state.cycle,
      alive: this.memory.state.alive
    };
  }
}

/* -------------------------
   BOOTSTRAP
------------------------- */


/* =========================
   CLEAN BOOTSTRAP (FIXED)
========================= */

const ima = new IMAKernel();

ima.boot();
ima.cli(process.argv);

module.exports = ima;
