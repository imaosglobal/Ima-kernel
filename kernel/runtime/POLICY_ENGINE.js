function allowWrite(filePath, content) {
  if (!filePath || !content) return false;

  // מניעת קבצים כפולים/ריקים
  if (content.length < 1) return false;

  // חסימת system core override
  if (filePath.includes("runtime/ENTRYPOINT")) return false;

  return true;
}

module.exports = { allowWrite };
