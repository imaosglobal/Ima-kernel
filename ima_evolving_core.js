const fs = require("fs");

/* ================= MEMORY LAYER ================= */
const memory = {
  events: [],
  metrics: {},
  feedback: []
};

/* ================= EVENT LOGGER ================= */
function logEvent(type, data){
  memory.events.push({
    type,
    data,
    ts: Date.now()
  });
}

/* ================= LEARNING ENGINE ================= */
function analyze(){
  const summary = {
    totalEvents: memory.events.length,
    eventTypes: {}
  };

  for(const e of memory.events){
    summary.eventTypes[e.type] = (summary.eventTypes[e.type] || 0) + 1;
  }

  return summary;
}

/* ================= SELF IMPROVEMENT SUGGESTION ================= */
function suggestImprovement(){
  const analysis = analyze();

  const suggestions = [];

  if(analysis.totalEvents > 10){
    suggestions.push("Add event compression layer");
  }

  if(Object.keys(analysis.eventTypes).length > 5){
    suggestions.push("Introduce event categorization model");
  }

  return {
    analysis,
    suggestions
  };
}

/* ================= CORE RUN ================= */
function run(input){

  logEvent("input", input);

  const result = {
    output: "IMA CORE PROCESSED: " + input,
    analysis: analyze(),
    suggestions: suggestImprovement()
  };

  logEvent("output", result.output);

  return result;
}

/* ================= SAFE PERSIST ================= */
function save(){
  fs.writeFileSync(
    "./ima_memory.json",
    JSON.stringify(memory, null, 2)
  );
}

/* ================= EXPORT ================= */
module.exports = {
  run,
  logEvent,
  analyze,
  suggestImprovement,
  save,
  memory
};
