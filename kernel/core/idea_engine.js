const { callGemini, syncModels } = require('./gemini_autosync');

async function idea(text) {
  console.log("[IDEA]", text);

  await syncModels();

  const prompt = `
אתה מנוע שיפור מערכת קצה-לקצה.

כלל:
- אתה רואה מערכת קיימת
- משפר אותה אוטומטית
- מחזיר PATCH בלבד
- בלי הסברים

המשימה:
${text}
`;

  const res = await callGemini(prompt);

  if (!res) {
    console.log("[AI] empty response");
    return;
  }

  console.log("[AI PATCH]");
  console.log(res);
}

module.exports = { idea };
