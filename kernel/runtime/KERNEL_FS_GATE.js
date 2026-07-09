const FS = require("./FS_CONTROLLER");

function write(file, content) {
  return FS.createFile(file, content);
}

module.exports = { write };
