const fs = require('fs');

function isBalanced(code) {
  let stack = [];
  for (let c of code) {
    if (c === '{') stack.push(c);
    if (c === '}') {
      if (!stack.length) return false;
      stack.pop();
    }
  }
  return stack.length === 0;
}

function safeWrite(filePath, content) {
  // basic validation
  if (!content || content.length < 1) {
    throw new Error("EMPTY CONTENT BLOCKED");
  }

  if (!isBalanced(content)) {
    throw new Error("UNBALANCED CODE BLOCKED");
  }

  // duplicate prevention (simple hash)
  const crypto = require('crypto');
  const hash = crypto.createHash('sha256').update(content).digest('hex');

  const registryPath = './runtime/file_registry.log';
  if (fs.existsSync(registryPath)) {
    const log = fs.readFileSync(registryPath, 'utf8');
    if (log.includes(hash)) {
      throw new Error("DUPLICATE CONTENT BLOCKED");
    }
  }

  fs.writeFileSync(filePath, content);
  fs.appendFileSync(registryPath, `${filePath} ${hash}\n`);

  return { ok: true, filePath, hash };
}

module.exports = { safeWrite };
