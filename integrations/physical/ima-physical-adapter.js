/**
 * IMA Physical World Adapter — vendor-neutral reference interface.
 * This file intentionally contains no vendor credentials and performs no
 * physical actuation by itself.
 */

export const IMA_PHYSICAL_STANDARD = "0.1";

export class ImaPhysicalAdapter {
  constructor(device) {
    this.device = device;
    this.authorityLevel = 0;
  }

  discover() {
    return {
      standard: IMA_PHYSICAL_STANDARD,
      device: this.device,
      authorityLevel: this.authorityLevel
    };
  }

  describe() {
    return this.device;
  }

  observe(payload = {}) {
    return { ok: true, mode: "observe", payload };
  }

  propose(action) {
    return {
      ok: true,
      mode: "propose",
      action,
      requiresAuthorization: true
    };
  }

  authorize(level) {
    if (!Number.isInteger(level) || level < 0 || level > 5) {
      throw new Error("IMA authority level must be 0..5");
    }
    this.authorityLevel = level;
    return { ok: true, authorityLevel: level };
  }

  act(action, { explicitAuthorization = false } = {}) {
    if (this.authorityLevel < 3 || !explicitAuthorization) {
      return {
        ok: false,
        blocked: true,
        reason: "physical_action_requires_explicit_authorization"
      };
    }
    throw new Error("Vendor adapter must implement physical actuation");
  }

  stop() {
    return { ok: true, mode: "stop_requested" };
  }

  audit(event) {
    return {
      timestamp: new Date().toISOString(),
      standard: IMA_PHYSICAL_STANDARD,
      event
    };
  }
}
