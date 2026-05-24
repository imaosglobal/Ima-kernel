const os = require("os")

function installer(){

  const platform = os.platform()

  let mode = "unknown"

  if(platform === "android") mode = "termux"
  if(platform === "linux") mode = "linux"
  if(platform === "darwin") mode = "mac"
  if(platform === "win32") mode = "windows"

  console.log("[INSTALLER]",mode)

}

installer()
