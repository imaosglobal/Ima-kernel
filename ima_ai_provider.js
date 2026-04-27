/**
 * IMA AI Provider Layer
 * מחליף בין מודלים בלי תלות בהתקנה כבדה
 */

function localFallback(input) {
  return `LOCAL IMA: ${input}`;
}

// כרגע רק fallback — אבל הארכיטקטורה מוכנה ל:
 // - OpenAI
 // - Claude
 // - Gemini
 // - Local future models

async function ask(input) {
  try {
    // בעתיד כאן נכנס API אמיתי
    return localFallback(input);
  } catch (e) {
    return localFallback(input);
  }
}

module.exports = { ask };
