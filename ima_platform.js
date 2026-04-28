const IMA = require("./ima_core_engine");
const Memory = require("./ima_memory");
const tools = require("./ima_tools");

const memory = new Memory();
const ima = new IMA({ memory, tools });

module.exports = ima;
