try { require("../brain/brain_engine") } catch(e) { console.log("[GUARD] brain_engine missing") }
require("../agents/self_heal_agent")
require("../memory/memory_writer")
require("../registry/runtime_registry")

console.log("[IMA ORCHESTRATOR] online")

require("./live_api")
require("./device_mesh")
require("./patch_queue")
require("./ui_server")

console.log("[IMA FULL STACK] active")
