from billing.adapters.tranzila import TranzilaAdapter

ADAPTERS = {
    "tranzila": TranzilaAdapter,
}


def configured_providers():
    return [
        provider_id
        for provider_id, adapter_cls in ADAPTERS.items()
        if adapter_cls.is_configured()
    ]


def get_adapter(provider):
    adapter_cls = ADAPTERS.get(provider)

    if adapter_cls is None:
        raise RuntimeError(
            f"No billing adapter registered for provider: {provider}"
        )

    if not adapter_cls.is_configured():
        raise RuntimeError(
            f"Billing provider is not configured: {provider}"
        )

    return adapter_cls()


def available_adapters():
    return {
        provider_id: {
            "configured": adapter_cls.is_configured(),
        }
        for provider_id, adapter_cls in ADAPTERS.items()
    }
