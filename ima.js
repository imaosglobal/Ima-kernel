const app = require("./kernel/app");

app.get("/health",(req,res)=>{
  res.json({ ok:true, system:"IMA_CORE_SERVER" });
});

app.listen(7000, ()=>{
  console.log("[IMA CORE SERVER RUNNING]");
});
require("./kernel/os/bootstrap")

const { loadPlugins } = require("./kernel/runtime/plugin_loader")
loadPlugins()



require("./kernel/os/bootstrap")



require("./kernel/shell/adaptive_shell")


require("./kernel/network/discovery_mesh")


require("./kernel/installer/universal_installer")


require("./kernel/ai/local_brain")


require("./kernel/events/event_bus")


require("./kernel/identity/identity")


require("./kernel/devices/device_bridge")


require("./kernel/skills/skill_runtime")


require("./kernel/tasks/task_manager")


require("./kernel/decisions/decision_engine")


require("./kernel/security/permission_layer")


require("./kernel/update/update_graph")


require("./kernel/users/user_manager")


require("./kernel/api/live_api")


require("./kernel/sync/cloud_sync")


require("./kernel/os/singleton_lock")


require("./kernel/memory/stability_engine")


require("./kernel/stability/stability_core")

require('./kernel/runtime/require_guard')

require("./kernel/stability/freeze_layer")

require("./kernel/vibe/termux_gateway")
require("./kernel/sync/sync_engine")
