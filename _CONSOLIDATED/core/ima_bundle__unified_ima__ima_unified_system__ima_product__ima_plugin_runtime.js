const fs = require("fs");
const path = require("path");

/* ---------- STATE ---------- */
const PLUGIN_DIR = "./ima_plugins";
const STATE_FILE = "./ima_plugin_state.json";

function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- STATE ---------- */
let state = load(STATE_FILE, {
  plugins: {},
  logs: []
});

/* ---------- LOAD PLUGIN ---------- */
function loadPlugin(file){
  try {
    const plugin = require(path.resolve(PLUGIN_DIR, file));

    if(!plugin || !plugin.name || !plugin.run){
      return console.log("⚠ invalid plugin:", file);
    }

    state.plugins[plugin.name] = file;

    console.log("📦 Loaded plugin:", plugin.name);
    return plugin;

  } catch (e) {
    console.log("⚠ failed plugin:", file);
  }
}

/* ---------- RELOAD ALL ---------- */
function reload(){
  if(!fs.existsSync(PLUGIN_DIR)){
    fs.mkdirSync(PLUGIN_DIR);
  }

  const files = fs.readdirSync(PLUGIN_DIR);

  const loaded = [];

  for(const f of files){
    const p = loadPlugin(f);
    if(p) loaded.push(p);
  }

  return loaded;
}

/* ---------- EXEC ENGINE ---------- */
function run(input, plugins){
  let results = [];

  for(const p of plugins){
    try {
      results.push({
        plugin: p.name,
        output: p.run(input)
      });
    } catch (e) {
      results.push({
        plugin: p.name,
        error: true
      });
    }
  }

  return results;
}

/* ---------- MAIN ---------- */
function main(){
  console.log("🧠 IMA PLUGIN RUNTIME STARTED");

  const input = process.argv.slice(2).join(" ") || "test input";

  const plugins = reload();

  const result = run(input, plugins);

  state.logs.push({
    input,
    result,
    time: Date.now()
  });

  if(state.logs.length > 300){
    state.logs.shift();
  }

  save(STATE_FILE, state);

  console.log("📡 INPUT:", input);
  console.log("📦 PLUGINS:", Object.keys(state.plugins));
  console.log("💬 RESULT:", result);
}

main();
