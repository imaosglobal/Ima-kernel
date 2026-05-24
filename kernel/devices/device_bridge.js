const os = require("os")

function scan(){

  const devices = {
    platform: os.platform(),
    arch: os.arch(),
    hostname: os.hostname(),
    cpus: os.cpus().length
  }

  console.log("[DEVICE BRIDGE]",JSON.stringify(devices))
}

setInterval(scan,30000)

scan()
