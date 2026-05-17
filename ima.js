const app = require("./kernel/app");
const engine = require("./kernel/runtime/engine");
const api = require("./kernel/api");
const { startAutoSync } = require("./kernel/runtime/sync_daemon");

engine.boot();
api.register(app);

startAutoSync(); // 👈 autonomous layer

app.listen(7000, ()=>{
  console.log("[IMA AUTONOMOUS SYNC ENGINE RUNNING]");
});
