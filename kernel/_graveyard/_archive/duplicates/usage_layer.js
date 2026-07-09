module.exports = (app, db) => {

  app.use((req, res, next) => {
    const key = req.apiKey;
    const task = req.body?.task;

    if (!key || !task) return next();

    db.getUser(key, (err, user) => {
      if (user) {
        user.usage = (user.usage || 0) + 1;
        db.updateUser(key, user, () => {});
      }
      next();
    });
  });

};
