"use strict";

const assert = require("assert");
const fs = require("fs");

const app = fs.readFileSync("ima-ui/src/App.jsx", "utf8");
const css = fs.readFileSync("ima-ui/src/index.css", "utf8");

// Direction is applied from the resolved locale at runtime, not hard-coded in JSX.
assert.ok(app.includes("document.documentElement.dir=locale.dir"), "UI must apply locale-aware RTL/LTR direction");
assert.ok(app.includes('alt="IMA avatar"'), "avatar image must have meaningful alternative text");
assert.ok(app.includes('aria-label="IMA Google campaign destination"'), "avatar campaign link must have an accessible name");
assert.ok(app.includes('htmlFor="ima-composer"') && app.includes('id="ima-composer"'), "chat composer must have a programmatic label");
assert.ok(app.includes("disabled={busy}"), "busy state must disable the composer");
assert.ok(/onKeyDown=\{e=>e\.key===['"]Enter['"]&&send\(\)\}/.test(app), "chat must support Enter submission");
assert.ok(css.includes(".chat-layout"), "chat layout styling must remain present");

console.log("IMA_ACCESSIBILITY_CONTRACT=PASS");
