#!/usr/bin/env node

class IMA {
  constructor() {
    this.version = "1.0.0";
    this.plugins = {};
    this.memory = { logs: [] };
  }

  log(event) {
    this.memory.logs.push(event);
  }

  register(name, fn) {
    this.plugins[name] = fn;
  }

  runPlugin(name, input) {
    if (this.plugins[name]) {
      return this.plugins[name](input);
    }
    return "Plugin not found";
  }

  ask(query) {
    this.log(query);

    if (query.includes("finance")) {
      return this.runPlugin("finance", query);
    }

    if (query.includes("learn")) {
      return this.runPlugin("learning", query);
    }

    return "IMA: " + query;
  }

  cli() {
    const input = process.argv.slice(2).join(" ");

    if (!input) {
      console.log("IMA READY");
      return;
    }

    console.log(this.ask(input));
  }
}

const ima = new IMA();

ima.register("finance", (x) => "📊 finance: " + x);
ima.register("learning", (x) => "📚 learning: " + x);

ima.cli();
