const EventEmitter = require("events")

const bus = new EventEmitter()

global.IMA_EVENT_BUS = bus

console.log("[EVENT BUS] online")

module.exports = bus
