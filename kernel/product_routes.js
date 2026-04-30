const { createUser, auth, appendMemory } = require("./auth_layer");

module.exports = function(app) {

  // signup
  app.post("/v1/signup", (req, res) => {
    const key = createUser();
    res.json({ apiKey: key });
  });

  // run (product API)
  app.post("/v1/run", (req, res) => {
    const key = req.headers["x-api-key"];
    const user = auth(key);

    if (!user) {
      return res.status(401).json({ error: "Invalid API key" });
    }

    const task = req.body?.task || "";

    const result = {
      ok: true,
      result: "Processed: " + task,
      meta: {
        personalized: true,
        memorySize: user.memory.length
      }
    };

    appendMemory(key, task, result.result);

    res.json(result);
  });

};
