import fs from 'node:fs';
import assert from 'node:assert/strict';

const app=fs.readFileSync(new URL('../ima-ui/src/App.jsx',import.meta.url),'utf8');
const index=fs.readFileSync(new URL('../ima-ui/index.html',import.meta.url),'utf8');
const manifest=fs.readFileSync(new URL('../ima-ui/public/manifest.json',import.meta.url),'utf8');
const support=fs.readFileSync(new URL('../ima-ui/public/support.html',import.meta.url),'utf8');

assert.match(app,/id="support"/,'public support section missing');
assert.match(app,/SUPPORT_URL/,'public support destination must be defined');
assert.match(app,/href=\{SUPPORT_URL\}/,'footer support link must use the canonical support page');
assert.match(support,/href="\/Ima-kernel\/#support"/,'support page must return to the in-page feedback section');
assert.doesNotMatch(app,/app\.heygen\.com\/videos/,'public UI must not link visitors to HeyGen studio');
assert.match(app,/youtube\.com\/@imaglobal-d4g/,'public video destination must be IMA YouTube');
assert.match(app,/getStoredGoogleUser\(\)/,'Google session must be restored');
assert.match(app,/signInWithGoogleCredential/,'Google verification flow must exist');
assert.match(app,/getStoredGoogleUser\(\)/,'chat must use persisted Google session state');
assert.match(app,/beforeinstallprompt/,'installable PWA flow missing');
assert.match(index,/manifest\.json/,'canonical manifest link missing');
assert.match(manifest,/"display": "standalone"/,'PWA must be installable as standalone');
const ids=[...app.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
for(const target of [...app.matchAll(/href="#([^"]+)"/g)].map(m=>m[1])) assert.ok(ids.includes(target),`broken internal anchor #${target}`);
console.log('PUBLIC_UI_CONTRACT_OK',JSON.stringify({ids,internalAnchors:[...new Set([...app.matchAll(/href="#([^"]+)"/g)].map(m=>m[1]))]}));

assert.doesNotMatch(app,/PersonalizationPanel|personalization-panel|applyChatPersonalization|recordImaPreference/,'the broken public personalization engine must not be shown or run');
assert.doesNotMatch(app,/AvatarScene|mother_character\.glb|hero-avatar canvas/,'the public hero must not show the old character render');
assert.match(app,/wordmark-mark/,'the canonical IMA wordmark must be present');
assert.match(app,/heroTitle/,'the current IMA hero headline must be present');
