const stability = require("./stability");

console.log("🧠 IMA RUNTIME BOOTED");

setInterval(() => {
  try {
    const report = stability.healthCheck();
    console.log("🛡 health:", report);

    const recovery = stability.smartRecover();
    if (!recovery.skipped) {
      console.log("🔄 recovery:", recovery);
    }
  } catch (e) {
    console.log("⚠️ stability error:", e.message);
  }
}, 15000);
