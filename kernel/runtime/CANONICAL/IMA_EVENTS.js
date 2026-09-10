const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../..");
const LOG = path.join(ROOT, ".ima/runtime/canonical_events.jsonl");

class IMAEvents {
    constructor() {
        this.listeners = {};
    }

    on(name, fn) {
        if (!this.listeners[name]) {
            this.listeners[name] = [];
        }
        this.listeners[name].push(fn);
    }

    emit(name, data = {}) {
        const event = {
            time: Date.now(),
            name,
            data
        };

        try {
            fs.mkdirSync(path.dirname(LOG), {recursive: true});
            fs.appendFileSync(
                LOG,
                JSON.stringify(event) + "\n",
                "utf8"
            );
        } catch (error) {
            // Event logging must not stop runtime execution.
        }

        for (const fn of this.listeners[name] || []) {
            try {
                fn(data);
            } catch (error) {
                // One listener must never kill the event bus.
            }
        }

        return event;
    }
}

module.exports = new IMAEvents();
