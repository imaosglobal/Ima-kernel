const ima = require("./ima_platform");

const userId = "user_" + process.env.USER || "guest";
const input = process.argv.slice(2).join(" ");

ima.ask(userId, input).then(res => {
  console.log("\n🧠 IMA RESPONSE\n");
  console.log(res);
});
