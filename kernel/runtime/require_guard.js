const Module = require("module")

const oldRequire =
Module.prototype.require

Module.prototype.require =
function(request){

  try{

    return oldRequire.apply(this,arguments)

  } catch(e){

    console.log(
      "[GUARD]",
      request,
      e.message
    )

    return {}

  }

}
