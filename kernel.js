class IMAKernel {
  constructor() {
    this.modules = {};
    this.listeners = {};
    this.state = { cycle: 0, memory: {} };
  }

  on(event, fn) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(fn);
  }

  emit(event, data) {
    (this.listeners[event] || []).forEach(fn => fn(data));
  }

  register(name, fn) {
    this.modules[name] = fn;
  }

  loadModules() {
    Object.values(this.modules).forEach(fn => fn(this));
  }

  start(args = []) {
    console.log("🧠 IMA KERNEL START");
    this.loadModules();
    this.emit("boot", { args });

    setInterval(() => {
      this.state.cycle++;
      this.emit("tick", this.state);
    }, 1000);
  }
}

module.exports = IMAKernel;
