import fs from 'node:fs';
import assert from 'node:assert/strict';

const app=fs.readFileSync(new URL('../ima-ui/src/PublicApp.jsx',import.meta.url),'utf8');
const css=fs.readFileSync(new URL('../ima-ui/src/PublicApp.css',import.meta.url),'utf8');
const main=fs.readFileSync(new URL('../ima-ui/src/main.jsx',import.meta.url),'utf8');
const index=fs.readFileSync(new URL('../ima-ui/index.html',import.meta.url),'utf8');
const manifest=fs.readFileSync(new URL('../ima-ui/public/manifest.json',import.meta.url),'utf8');

assert.match(main,/PublicApp/,'canonical public entry must use PublicApp');
assert.match(app,/askIma\(/,'public UI must call the real IMA chat runtime');
assert.match(app,/authenticated:true/,'public chat must run with an authenticated account context');
assert.match(app,/signInWithGoogleCredential/,'public entry must retain Google account sign-in');
assert.match(app,/getStoredGoogleUser/,'public entry must restore the signed-in Google account');
assert.match(app,/submitFeedback/,'public feedback must enter the canonical learning path');
assert.match(css,/\.public-chat/,'public chat styling missing');
assert.match(css,/\.public-hero/,'public hero styling missing');
assert.match(index,/manifest\.json/,'canonical manifest link missing');
assert.match(manifest,/standalone/,'PWA must remain installable as standalone');

for(const internal of ['Impact Window','Window capabilities','IMA Store','LIVE-001','PersonalizationPanel','AvatarScene']){
  assert.equal(app.includes(internal),false,'internal system detail must not appear in public UI: '+internal);
}

assert.match(app,/מה קורה אצלך עכשיו\?|What is happening for you right now\?/,'direct human-facing product headline missing');
console.log('PUBLIC_UI_CONTRACT_OK',JSON.stringify({entry:'PublicApp',internalSurfacesHidden:true,directChat:true,pwa:true}));
