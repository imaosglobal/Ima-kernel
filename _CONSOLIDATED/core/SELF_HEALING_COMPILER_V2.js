const fs = require('fs');
const acorn = require('acorn');
const escodegen = require('escodegen');

const CONTROL = require('./KERNEL_CONTROL_PLANE_V2');

// ─────────────────────────────
// PARSE SAFELY
// ─────────────────────────────

function parse(code){
  try {
    return acorn.parse(code, { ecmaVersion: 2022 });
  } catch (e) {
    return { error: e.message };
  }
}

// ─────────────────────────────
// SIMPLE AUTO FIX ENGINE
// ─────────────────────────────

function attemptFix(code){

  // תיקון בסיסי: סוגריים חסרים / חיתוך קוד שבור
  let fixed = code;

  // אם אין אפשרות parse בכלל → fallback
  const ast = parse(code);
  if (ast.error) {

    // ניסיון 1: חיתוך שורה אחרונה (common corruption)
    const lines = code.split('\n');
    lines.pop();
    fixed = lines.join('\n');

    const retry = parse(fixed);
    if (!retry.error) return fixed;

    return null;
  }

  return code;
}

// ─────────────────────────────
// WRITE SAFE WITH HEAL
// ─────────────────────────────

function writeSafe(file, content){

  const ast = parse(content);

  if (!ast.error) {
    return CONTROL.write(file, content);
  }

  console.log('[HEAL] DETECTED BROKEN CODE:', file);

  const fixed = attemptFix(content);

  if (!fixed) {
    console.log('[HEAL] UNRECOVERABLE:', file);
    return { status:'failed_unrecoverable' };
  }

  console.log('[HEAL] FIXED AND RETRYING:', file);

  return CONTROL.write(file, fixed);
}

// ─────────────────────────────
// AUDIT + HEAL LOOP
// ─────────────────────────────

function audit(dir){

  const files = walk(dir);
  let healed = 0;
  let broken = [];

  for (const f of files) {
    if (!f.endsWith('.js')) continue;

    const c = fs.readFileSync(f,'utf8');
    const ast = parse(c);

    if (ast.error) {
      const res = writeSafe(f, c);
      healed++;
      broken.push({ file:f, result:res });
    }
  }

  return {
    ok: files.length - broken.length,
    broken: broken.length,
    healed
  };
}

// ─────────────────────────────
// helper
// ─────────────────────────────

function walk(dir){
  let out=[];
  for (const f of fs.readdirSync(dir)) {
    const p = require('path').join(dir,f);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

module.exports = {
  writeSafe,
  audit
};
