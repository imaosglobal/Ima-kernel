module.exports = (app, db) => {

  // attach context
  app.use((req, res, next) => {
    req.ctx = {};
    next();
  });

  // auth middleware
  app.use((req, res, next) => {
    const key = req.headers["x-api-key"];
    req.apiKey = key;
    next();
  });

};
