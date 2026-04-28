const { syncAll } = require("./ima_master_control");

console.log("🧠 IMA KERNEL START");

// boot
syncAll();

console.log("✅ IMA KERNEL MASTER ACTIVE");

// loop בסיסי
setInterval(() => {
  syncAll();
}, 5000);
