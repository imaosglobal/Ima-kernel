module.exports = (app, db) => {

  app.post("/run", (req, res, next) => {

    const task = req.body?.task;

    if (!task) return next();

    // זה מה שמייצר את התוצאה בפועל
    req.ctx.result = {
      ok: true,
      result: "Processed: " + task
    };

    next();
  });

};
