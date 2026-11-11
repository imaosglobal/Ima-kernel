"use strict";

const assert = require("assert");
const fs = require("fs");

const app = fs.readFileSync("ima-ui/src/App.jsx", "utf8");
const css = fs.readFileSync("ima-ui/src/index.css", "utf8");

// Direction is applied from the resolved locale at runtime, not hard-coded in JSX.
assert.ok(app.includes("document.documentElement.dir = lang === 'he' ? 'rtl' : 'ltr'"), "UI must apply locale-aware RTL/LTR direction");
assert.ok(app.includes('aria-label="אמא"'), "Mama figure must have an accessible name");
assert.ok(app.includes('aria-label="IMA public campaign"'), "campaign destination must have an accessible name");
assert.ok(app.includes('aria-label={t.write}'), "chat composer must have a programmatic label");
assert.ok(app.includes("disabled={busy || !message.trim()}"), "busy/empty state must disable the composer");
assert.ok(/onKeyDown=\{e=>e\.key===['"]Enter['"]&&send\(\)\}/.test(app), "chat must support Enter submission");
assert.ok(css.includes(".chat-panel") && css.includes(".chat-composer"), "chat layout styling must remain present");

console.log("IMA_ACCESSIBILITY_CONTRACT=PASS");
