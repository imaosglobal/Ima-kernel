const core = require("./ima_unified_runtime");

function ask(input){

  const result = core.boot(input);

  return {
    user_view: format(result),
    internal: result
  };
}

function format(result){
  return `
🧠 IMA RESPONSE

💡 Output:
${result.result.output}

📊 Insight:
${JSON.stringify(result.result.analysis, null, 2)}

🔧 Suggestions:
${result.result.suggestions.suggestions.join("\n- ") || "No suggestions"}

`;
}

module.exports = { ask };
