"use strict";

const assert = require("assert");
const fs = require("fs");

const app = fs.readFileSync("ima-ui/src/App.jsx", "utf8");
const css = fs.readFileSync("ima-ui/src/index.css", "utf8");

assert.ok(app.includes('dir="rtl"'), "UI must declare RTL direction");
assert.ok(app.includes('aria-label="נוכחות תלת ממדית"'), "3D presence must have an accessible label");
assert.ok(app.includes('aria-label="כתוב לאמא"'), "chat input must have an accessible label");
assert.ok(app.includes("disabled={busy}"), "busy state must disable the composer");
assert.ok(app.includes("onKeyDown={e => e.key === 'Enter' && send()}"), "chat must support Enter submission");
assert.ok(css.includes(".chat-shell"), "chat shell styling must remain present");

console.log("IMA_ACCESSIBILITY_CONTRACT=PASS");
