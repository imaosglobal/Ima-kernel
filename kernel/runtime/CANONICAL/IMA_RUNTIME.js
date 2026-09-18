const state = require("./IMA_STATE");
const events = require("./IMA_EVENTS");
const heal = require("./IMA_HEAL");
const policy = require("./IMA_POLICY");
const arbitrage = require("../../opportunity/IMA_ARBITRAGE");
const continuity = require("./IMA_CONTINUITY");
const preservation = require("./IMA_PRESERVATION_REGISTRY");
const preservationVerify = require("./IMA_PRESERVATION_VERIFY");
const vaultManifest = require("./IMA_VAULT_MANIFEST");
const contentAddress = require("./IMA_CONTENT_ADDRESS");
const portableIdentity = require("./IMA_PORTABLE_IDENTITY");
const derivationRegistry = require("./IMA_DERIVATION_REGISTRY");

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

      const preservationStatus = preservation.status();
      const preservationIntegrity = preservationVerify.verify();
      const vaultManifestBuild = vaultManifest.build();
      const vaultManifestIntegrity = vaultManifest.verify();
      const contentAddressBuild = contentAddress.build();
      const contentAddressIntegrity = contentAddress.verify();
      const portableIdentityBuild = portableIdentity.build();
      const portableIdentityIntegrity = portableIdentity.verify();
      const derivationRegistryBuild = derivationRegistry.build();
      const derivationRegistryIntegrity = derivationRegistry.verify();

      events.emit("CONTINUITY_READY", continuity.status());
      events.emit("PRESERVATION_REGISTRY_READY", preservationStatus);
      events.emit("PRESERVATION_INTEGRITY", preservationIntegrity);
      events.emit("VAULT_MANIFEST_INTEGRITY", vaultManifestIntegrity);
      events.emit("CONTENT_ADDRESS_INTEGRITY", contentAddressIntegrity);
      events.emit("PORTABLE_IDENTITY_INTEGRITY", portableIdentityIntegrity);
      events.emit("DERIVATION_REGISTRY_INTEGRITY", derivationRegistryIntegrity);

        return {
            status: state.get("status"),
            health,
            policy: {
                safe_actions: policy.SAFE_ACTIONS,
                approval_required: policy.APPROVAL_REQUIRED
            },
            state: state.dump(),
        continuity: continuity.status(),
      preservation: preservation.status(),
      preservation_integrity: preservationIntegrity,
      vault_manifest: {
        build: vaultManifestBuild,
        integrity: vaultManifestIntegrity
      },
      content_addressing: {
        build: contentAddressBuild,
        integrity: contentAddressIntegrity
      },
      portable_identity: {
        build: portableIdentityBuild,
        integrity: portableIdentityIntegrity
      },
      derivation_registry: {
        build: derivationRegistryBuild,
        integrity: derivationRegistryIntegrity
      }
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
