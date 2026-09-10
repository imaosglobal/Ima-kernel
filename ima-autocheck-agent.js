#!/usr/bin/env node
/**
 * ima-autocheck-agent.js
 * סקריפט חכם ואוטונומי ל-Ima-3d-mom
 * - בדיקה פנימית של קבצים ו-assets
 * - חיבור למודלי בינה חיצוניים (Gemini 3, GPT)
 * - סוכנים פנימיים שמיישמים תיקונים
 * - שמירת לוג פנימי של Ima
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

// ------------------- הגדרות בסיס -------------------
const requiredFiles = ['index.html', 'Main.js', 'style.css'];
const assetsFolder = path.join(__dirname, 'assets');
const modelFile = path.join(assetsFolder, 'model.glb');
const logFile = path.join(__dirname, 'ima-agent-log.json');
const aiModel = 'gpt-5-mini';

// ------------------- שמירת לוג -------------------
function saveLog(entry) {
  let logs = [];
  if (fs.existsSync(logFile)) {
    try { logs = JSON.parse(fs.readFileSync(logFile)); } catch {}
  }
  logs.push({ timestamp: new Date().toISOString(), ...entry });
  fs.writeFileSync(logFile, JSON.stringify(logs, null, 2));
}

// ------------------- בדיקה פנימית -------------------
function checkLocalFiles() {
  let errors = [];

  requiredFiles.forEach(file => {
    if (!fs.existsSync(file)) errors.push(`Missing file: ${file}`);
  });

  if (!fs.existsSync(assetsFolder)) errors.push('Assets folder missing');
  if (!fs.existsSync(modelFile)) errors.push('model.glb missing');

  if (errors.length > 0) {
    console.log('❌ Internal check failed:');
    errors.forEach(e => console.log(` - ${e}`));
    saveLog({ type: 'internal', success: false, errors });
    return false;
  } else {
    console.log('✅ Internal check passed.');
    saveLog({ type: 'internal', success: true });
    return true;
  }
}

// ------------------- סוכן תיקון פנימי -------------------
function runInternalAgents(errors) {
  if (!errors || errors.length === 0) return;

  console.log('🛠 Running internal agents to fix issues...');
  errors.forEach(err => {
    if (err.includes('Missing file')) {
      const fileName = err.split(': ')[1];
      fs.writeFileSync(fileName, `<!-- Auto-created by Ima agent -->\n`);
      console.log(`   ✅ Created missing file: ${fileName}`);
    }
    if (err.includes('model.glb missing') || err.includes('Assets folder missing')) {
      if (!fs.existsSync(assetsFolder)) fs.mkdirSync(assetsFolder);
      if (!fs.existsSync(modelFile)) fs.writeFileSync(modelFile, '');
      console.log('   ✅ Created assets folder and empty model.glb');
    }
  });
  saveLog({ type: 'agents', action: 'auto-fix applied', errors });
}

// ------------------- חיבור למודלים חיצוניים -------------------
async function checkExternalAI() {
  try {
    const response = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: aiModel,
      messages: [
        { role: "system", content: "Review project files and suggest improvements for Ima-3d-mom GitHub repo." },
        { role: "user", content: `Please check files: ${requiredFiles.join(', ')} and ${modelFile}` }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    const suggestion = response.data.choices[0].message.content;
    console.log('💡 External AI suggestions:');
    console.log(suggestion);
    saveLog({ type: 'external', success: true, suggestion });
  } catch (err) {
    console.log('⚠️ Error connecting to external AI:', err.message);
    saveLog({ type: 'external', success: false, error: err.message });
  }
}

// ------------------- הפעלה עיקרית -------------------
(async function main() {
  console.log('🔗 Running Ima Autocheck Agent...');
  const isInternalOk = checkLocalFiles();
  if (!isInternalOk) {
    // אם יש שגיאות, נתקן אותן אוטומטית
    const errors = JSON.parse(fs.readFileSync(logFile)).filter(l => l.type === 'internal' && !l.success).pop()?.errors;
    runInternalAgents(errors);
  }
  await checkExternalAI();
  console.log('✅ Ima Autocheck Agent finished.');
})();
