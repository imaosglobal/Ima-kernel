const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SNAP_DIR = './runtime/.snapshots';
const QUAR_DIR = './runtime/.quarantine';

fs.mkdirSync(SNAP_DIR, { recursive: true });
fs.mkdirSync(QUAR_DIR, { recursive: true });

function hash(content){
  return crypto.createHash('sha256').update(content).digest('hex');
}

function snapshot(filePath, content){
  const id = path.basename(filePath) + '.' + Date.now();
  const snapPath = path.join(SNAP_DIR, id + '.bak');
  fs.writeFileSync(snapPath, content);
  return snapPath;
}

function isValidJS(code){
  try {
    new Function(code);
    return true;
  } catch (e) {
    return false;
  }
}

function read(file){
  return fs.readFileSync(file, 'utf8');
}

function writeSafe(filePath, newContent){

  const oldContent = fs.existsSync(filePath) ? read(filePath) : null;

  // 1. snapshot קודם
  if (oldContent) snapshot(filePath, oldContent);

  // 2. validate לפני כתיבה
  if (path.extname(filePath) === '.js') {
    if (!isValidJS(newContent)) {
      console.log('[HEALER] INVALID JS → quarantine:', filePath);

      const badPath = path.join(
        QUAR_DIR,
        path.basename(filePath) + '.' + Date.now() + '.broken.js'
      );

      fs.writeFileSync(badPath, newContent);
      return { status: 'rejected', reason: 'syntax_error', quarantined: badPath };
    }
  }

  // 3. write
  fs.writeFileSync(filePath, newContent);

  return { status: 'written', file: filePath };
}

function heal(filePath){
  const snaps = fs.readdirSync(SNAP_DIR)
    .filter(f => f.startsWith(path.basename(filePath)))
    .sort()
    .reverse();

  if (snaps.length === 0) {
    return { status: 'no_snapshot' };
  }

  const latest = path.join(SNAP_DIR, snaps[0]);
  const content = fs.readFileSync(latest, 'utf8');

  fs.writeFileSync(filePath, content);

  return { status: 'restored', from: latest };
}

function audit(dir){
  const results = { ok:0, broken:[], healed:0 };

  function walk(d){
    for (const f of fs.readdirSync(d)) {
      const p = path.join(d, f);
      const st = fs.statSync(p);

      if (st.isDirectory()) walk(p);
      else {
        if (!f.endsWith('.js')) continue;

        const c = read(p);
        if (isValidJS(c)) results.ok++;
        else {
          results.broken.push(p);
          heal(p);
          results.healed++;
        }
      }
    }
  }

  walk(dir);
  return results;
}

module.exports = {
  writeSafe,
  heal,
  audit
};
