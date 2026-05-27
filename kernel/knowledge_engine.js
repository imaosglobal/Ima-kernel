const memory = require("./core/memory");

function handle(input) {
  const mem = memory.load();

  if (!mem.history) mem.history = [];

  const match = mem.history.find(m =>
    JSON.stringify(m).includes(input)
  );

  if (match) {
    return {
      status: "FOUND",
      answer: match
    };
  }

  memory.add({
    query: input,
    result: "stored new knowledge",
    type: "auto"
  });

  return {
    status: "NEW",
    answer: "נוסף לזיכרון"
  };
}

module.exports = { handle };
