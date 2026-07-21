module.exports = (app, db) => {
  const fs = require("fs");
  const path = require("path");

  const pluginsPath = path.join(__dirname, "plugins");
  const files = fs.readdirSync(pluginsPath);

  files.forEach(file => {
    if (file.endsWith(".js")) {
      const plugin = require(path.join(pluginsPath, file));
      plugin(app, db);
    }
  });
};
