const kernel = require("./kernel");

module.exports = (app) => {

  app.get("/", (req, res) => {
    res.json({
      status: "IMA WORLD API RUNNING"
    });
  });

};
