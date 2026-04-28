class IMAKernel {
  constructor() {
    this.modules = {};
    this.booted = false;
  }

  register(name, mod) {
    this.modules[name] = mod;
  }

  start(args = []) {
    if (this.booted) return;
    this.booted = true;

    console.log("🧠 IMA KERNEL STARTED");

    if (this.modules.boot) {
      this.modules.boot(args);
    }
  }
}

module.exports = IMAKernel;
