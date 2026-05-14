const fs = require("fs");
const path = require("path");

const PLUGIN_DIR = "./ima_plugins";
const REGISTRY_FILE = "./ima_registry.json";

function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- INIT ---------- */
let registry = load(REGISTRY_FILE, { installed: {} });

if(!fs.existsSync(PLUGIN_DIR)){
  fs.mkdirSync(PLUGIN_DIR);
}

/* ---------- INSTALL ---------- */
function install(name){
  // סימולציה של התקנה (בעתיד: npm / git / remote)
  const pluginPath = path.join(PLUGIN_DIR, name + ".js");

  const template = `
module.exports = {
  name: "${name}",
  version: "1.0.0",
  run: (input) => {
    return "[${name}] processed: " + input;
  }
};
`;

  fs.writeFileSync(pluginPath, template);

  registry.installed[name] = {
    version: "1.0.0",
    installedAt: Date.now()
  };

  save(REGISTRY_FILE, registry);

  console.log("📦 Installed plugin:", name);
}

/* ---------- LOAD PLUGINS ---------- */
function loadPlugins(){
  const plugins = [];

  const files = fs.readdirSync(PLUGIN_DIR);

  for(const f of files){
    const p = require(path.resolve(PLUGIN_DIR, f));
    plugins.push(p);
  }

  return plugins;
}

/* ---------- RUN ---------- */
function run(input){
  const plugins = loadPlugins();

  let results = [];

  for(const p of plugins){
    try {
      results.push(p.run(input));
    } catch {}
  }

  console.log("🌍 IMA ECOSYSTEM");
  console.log("💬 INPUT:", input);
  console.log("📦 PLUGINS:", plugins.map(p=>p.name));
  console.log("📊 OUTPUT:", results);
}

/* ---------- EXPORT ---------- */
module.exports = {
  install,
  run
};
