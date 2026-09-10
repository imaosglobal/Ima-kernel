const state = require("./IMA_STATE");
const events = require("./IMA_EVENTS");
const heal = require("./IMA_HEAL");
const policy = require("./IMA_POLICY");
const arbitrage = require("../../opportunity/IMA_ARBITRAGE");

const runtime = {
    boot() {
        const health = heal.check();

        state.set("status", health.healthy ? "ONLINE" : "DEGRADED");
        state.set("runtime", "CANONICAL");
        state.set("last_boot", Date.now());
        state.set("health", health);

        events.emit("BOOT", {
            status: state.get("status"),
            health
        });

        return {
            status: state.get("status"),
            health,
            policy: {
                safe_actions: policy.SAFE_ACTIONS,
                approval_required: policy.APPROVAL_REQUIRED
            },
            state: state.dump()
        };
    },

    state,
    events,
    heal,
    policy,
    arbitrage
};

if (require.main === module) {
    console.log(JSON.stringify(runtime.boot(), null, 2));
}

module.exports = runtime;
