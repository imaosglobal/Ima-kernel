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
const selfHosted = require("./IMA_SELF_HOSTED");
const relationalCare = require("./IMA_RELATIONAL_CARE");
const truthGate = require("./IMA_TRUTH_GATE");
const agencyGate = require("./IMA_HUMAN_AGENCY_GATE");
const revenueEvidence = require("./IMA_REVENUE_EVIDENCE");
const healthyEmpowerment = require("./IMA_HEALTHY_EMPOWERMENT");
const continuousBetterment = require("./IMA_CONTINUOUS_BETTERMENT");
const dots = require("./IMA_DOTS_BRIDGE");
const continuousLearning = require("./IMA_CONTINUOUS_LEARNING.cjs");
const innovationLoop = require("./IMA_INNOVATION_LOOP.js");
const pathIntelligence = require("./IMA_PATH_INTELLIGENCE");
const prPathRegistry = require("../../../core/PR_PATH_INTEGRATION_REGISTRY.json");
const roleContext = require("./IMA_ROLE_CONTEXT");

const runtime = {
    boot() {
        const health = heal.check();

        state.set("status", health.healthy ? "ONLINE" : "DEGRADED");
        state.set("role_context", roleContext.status());
        state.set("runtime", "CANONICAL");
        state.set("last_boot", Date.now());
        state.set("health", health);
        state.set("relational_care", relationalCare.contract());
        state.set("governance", { truth_gate: "CANONICAL", human_agency_gate: "CANONICAL", revenue_evidence: "CANONICAL", healthy_empowerment: "CANONICAL" });
        const empowerment = healthyEmpowerment.selfAssessment({ safety: "UNKNOWN", capacity: "UNKNOWN", energy: "UNKNOWN", overload: "UNKNOWN", agency: "HIGH" });
        state.set("healthy_empowerment", empowerment);
        continuousLearning.seed();
        const pathStatus = pathIntelligence.status();
        const prIntegration = pathIntelligence.ingestCapabilityMap(prPathRegistry);
        state.set("path_intelligence", pathStatus);
        state.set("pr_path_integration", prIntegration);
        events.emit("PATH_INTELLIGENCE_READY", pathStatus);
        events.emit("PR_PATH_INTEGRATION_READY", prIntegration);
        state.set("continuous_learning", continuousLearning.status());
        dots.register();
        state.set("dots", dots.status());
        events.emit("DOTS_READY", dots.card());

        const betterment = continuousBetterment.selfAssessment({ evidence: "UNKNOWN", risk: "UNKNOWN", reversibility: "UNKNOWN", human_impact: "UNKNOWN" });
        state.set("continuous_betterment", betterment);

        events.emit("ROLE_CONTEXT_READY", roleContext.status());

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
      const learningStatus = continuousLearning.status();
      const runtimePathSnapshot = pathIntelligence.ingestRuntimeSnapshot({
        health,
        relational_care: relationalCare.contract(),
        continuous_learning: learningStatus,
        path_intelligence: pathIntelligence.status(),
        pr_path_integration: state.get("pr_path_integration"),
        preservation: preservationStatus,
        preservation_integrity: preservationIntegrity,
        content_addressing: contentAddressIntegrity,
        portable_identity: portableIdentityIntegrity,
        derivation_registry: derivationRegistryIntegrity,
        dots: dots.status()
      });
      state.set("path_runtime_snapshot", runtimePathSnapshot.id);
      events.emit("PATH_RUNTIME_SNAPSHOT", runtimePathSnapshot.id);
      events.emit("CONTINUOUS_LEARNING_READY", learningStatus);

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
            governance: {
                truth_gate: truthGate.STATUSES,
                human_agency_gate: agencyGate.ACTION_CLASSES,
                revenue_evidence: { received_only: true },
                healthy_empowerment: empowerment,
                continuous_betterment: betterment
            },
            policy: {
                safe_actions: policy.SAFE_ACTIONS,
                approval_required: policy.APPROVAL_REQUIRED,
                relational_care: relationalCare.contract()
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
      dots: dots.status(),
      continuous_learning: learningStatus,
      path_intelligence: pathIntelligence.status(),
      pr_path_integration: state.get("pr_path_integration"),
      derivation_registry: {
        build: derivationRegistryBuild,
        integrity: derivationRegistryIntegrity
      },
      self_hosted: selfHosted.capabilityReport()
        };
    },

    state,
    events,
    heal,
    policy,
    arbitrage,
    relationalCare,
    innovationLoop,
    pathIntelligence
};

if (require.main === module) {
    console.log(JSON.stringify(runtime.boot(), null, 2));
}

module.exports = runtime;
