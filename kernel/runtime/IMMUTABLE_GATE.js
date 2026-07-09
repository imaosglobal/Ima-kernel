const FS = require("./FS_CONTROLLER");

function write(file, content, meta = {}) {
  const result = FS.createFile(file, content);

  return {
    ...result,
    meta,
    timestamp: Date.now()
  };
}

function update(file, content) {
  return FS.updateFile(file, content);
}

function remove(file) {
  return FS.safeDelete(file);
}

module.exports = { write, update, remove };
