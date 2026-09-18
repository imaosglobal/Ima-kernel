"use strict";

const providers = new Map();

function register(provider) {
  if (!provider || !provider.id || typeof provider.generate !== "function") {
    throw new Error("Invalid model provider");
  }

  providers.set(provider.id, provider);
  return provider.id;
}

function list() {
  return [...providers.values()].map(provider => ({
    id: provider.id,
    capabilities: provider.capabilities || []
  }));
}

async function generate(providerId, request) {
  const provider = providers.get(providerId);

  if (!provider) {
    throw new Error(`Unknown model provider: ${providerId}`);
  }

  return provider.generate(request);
}

module.exports = {
  register,
  list,
  generate
};
