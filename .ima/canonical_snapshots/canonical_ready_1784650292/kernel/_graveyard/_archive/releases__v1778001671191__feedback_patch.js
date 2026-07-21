const memory = require("./memory");

module.exports = function(app) {

  // feedback endpoint
  app.post("/feedback", (req, res) => {
    const key = req.headers["x-api-key"];
    const score = req.body?.score;
    const note = req.body?.note;

    memory.addFeedback(key, { score, note });

    res.json({ ok: true });
  });

  // toggle improvement mode
  app.post("/improve-mode", (req, res) => {
    const key = req.headers["x-api-key"];
    const enabled = req.body?.enabled;

    memory.setImprovementMode(key, !!enabled);

    res.json({ ok: true, improvementMode: enabled });
  });

};
