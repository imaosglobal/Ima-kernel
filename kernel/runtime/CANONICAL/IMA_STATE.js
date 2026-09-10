const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../..");
const FILE = path.join(ROOT, ".ima/runtime/canonical_state.json");

class IMAState {
    constructor() {
        this.data = {};
        this.load();
    }

    load() {
        try {
            if (fs.existsSync(FILE)) {
                this.data = JSON.parse(fs.readFileSync(FILE, "utf8"));
            }
        } catch (error) {
            this.data = {};
        }
    }

    set(key, value) {
        this.data[key] = value;
        this.persist();
        return value;
    }

    get(key) {
        return this.data[key];
    }

    dump() {
        return {...this.data};
    }

    persist() {
        try {
            fs.mkdirSync(path.dirname(FILE), {recursive: true});
            fs.writeFileSync(
                FILE,
                JSON.stringify(this.data, null, 2),
                "utf8"
            );
        } catch (error) {
            // Runtime state must never crash the boot process.
        }
    }
}

module.exports = new IMAState();
