console.log("[IMA OS] boot sequence start")

try {

  require("../runtime/ima_orchestrator")

  console.log("[IMA OS] orchestrator loaded")

} catch(e){

  console.log("[IMA OS ERROR]", e.message)

}

console.log("[IMA OS] runtime active")
