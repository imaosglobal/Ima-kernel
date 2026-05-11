const fs = require("fs");

function read(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf-8"));
  } catch {
    return fallback;
  }
}

function planExecution() {
  const state = read("ima_state.json", {});
  const product = state.product_brain || {};

  let plan = [];

  if (product.recommendation === "build_feature") {
    plan.push({
      action: "create_module",
      target: "new_feature_module",
      description: `Build feature for focus: ${product.focus}`
    });

    plan.push({
      action: "update_routes",
      target: "api_layer",
      description: "Expose new feature via API"
    });

    plan.push({
      action: "update_cli",
      target: "ima_cli",
      description: "Add CLI hook for feature"
    });
  }

  state.execution_plan = plan;

  fs.writeFileSync("ima_state.json", JSON.stringify(state, null, 2));

  return plan;
}

module.exports = { planExecution };
