import fs from 'node:fs';
import assert from 'node:assert/strict';

const app=fs.readFileSync(new URL('../ima-ui/src/App.jsx',import.meta.url),'utf8');
const index=fs.readFileSync(new URL('../ima-ui/index.html',import.meta.url),'utf8');
const manifest=fs.readFileSync(new URL('../ima-ui/public/manifest.webmanifest',import.meta.url),'utf8');

assert.match(app,/id="support"/,'public support section missing');
assert.match(app,/href="#support"/,'support navigation must point to an existing section');
assert.doesNotMatch(app,/app\.heygen\.com\/videos/,'public UI must not link visitors to HeyGen studio');
assert.match(app,/youtube\.com\/@imaglobal-d4g/,'public video destination must be IMA YouTube');
assert.match(app,/getStoredGoogleUser\(\)/,'Google session must be restored');
assert.match(app,/signInWithGoogleCredential/,'Google verification flow must exist');
assert.match(app,/loggedIn\?go\('chat'\):go\('login'\)/,'chat must be gated behind verified sign-in');
assert.match(app,/beforeinstallprompt/,'installable PWA flow missing');
assert.match(index,/manifest\.webmanifest/,'manifest link missing');
assert.match(manifest,/"display": "standalone"/,'PWA must be installable as standalone');
const ids=[...app.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
for(const target of [...app.matchAll(/href="#([^"]+)"/g)].map(m=>m[1])) assert.ok(ids.includes(target),`broken internal anchor #${target}`);
console.log('PUBLIC_UI_CONTRACT_OK',JSON.stringify({ids,internalAnchors:[...new Set([...app.matchAll(/href="#([^"]+)"/g)].map(m=>m[1]))]}));
