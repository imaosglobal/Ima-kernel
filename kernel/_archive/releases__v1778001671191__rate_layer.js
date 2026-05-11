module.exports = (app, db) => {

  app.use((req, res, next) => {
    const key = req.apiKey;
    if (!key) return next();

    db.getUser(key, (err, user) => {
      if (!user) return next();

      if (user.plan !== "paid" && user.usage > 100) {
        return res.json({ error: "Upgrade required (limit reached)" });
      }

      next();
    });
  });

};
