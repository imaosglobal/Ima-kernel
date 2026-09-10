from .model_selector import current
from .executor import execute
from .identity_guard import wrap_response


def ask(message):
    selection = current()

    selected = selection.get("selected", {})
    provider = selected.get("provider")
    model = selected.get("model")

    if not provider:
        return {
            "identity": "IMA",
            "status": "no_provider",
        }

    result = execute(
        model=model,
        prompt=message,
        provider=provider,
    )

    return wrap_response(result, "IMA")
