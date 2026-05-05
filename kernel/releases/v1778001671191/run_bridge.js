
module.exports = (app) => {
  app.post("/run", (req, res) => {
    res.json({
      ok: true,
      migrated: true,
      source: "prod_server",
      route: "legacy-compat",
      v2: ["/v2/health", "/v2/queue", "/v2/brain"]
    });
  });
};

