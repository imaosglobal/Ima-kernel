const memory = require("./memory_engine");

async function dispatch(action, context = {}) {
  switch (action) {

    case "open_store":
      return {
        type: "store",
        result: "חנות הופעלה",
        data: ["product_1", "product_2"]
      };

    case "activate_learning":
      return {
        type: "learning",
        result: "למידה הופעלה"
      };

    case "store_memory":
      const mem = memory.loadMemory();
      memory.addMemory(mem, context.message || "unknown", "action_memory");
      memory.saveMemory(mem);
      return {
        type: "memory",
        result: "נשמר בזיכרון"
      };

    default:
      return {
        type: "unknown",
        result: "אין פעולה מוגדרת"
      };
  }
}

module.exports = { dispatch };
