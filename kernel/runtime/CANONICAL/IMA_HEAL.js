const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../..");

const REQUIRED = [
    "IMA_RUNTIME.js",
    "IMA_STATE.js",
    "IMA_EVENTS.js",
    "IMA_HEAL.js",
    "IMA_POLICY.js",
    "IMA_SUPERVISOR.py",
    "IMA_WATCHDOG.py",
    "python_bridge.py"
];

function check() {
    const missing = [];
    const invalid = [];

    for (const name of REQUIRED) {
        const file = path.join(__dirname, name);

        if (!fs.existsSync(file)) {
            missing.push(name);
            continue;
        }

        try {
            if (fs.statSync(file).size === 0) {
                invalid.push(name);
            }
        } catch (error) {
            invalid.push(name);
        }
    }

    return {
        healthy: missing.length === 0 && invalid.length === 0,
        missing,
        invalid,
        time: Date.now()
    };
}

module.exports = {check};
