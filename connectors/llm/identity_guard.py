import time


def wrap_response(model_result, identity="IMA"):
    return {
        "time": time.time(),
        "identity": identity,
        "provider": model_result.get("provider"),
        "model": model_result.get("model"),
        "engine": model_result.get("model", "unknown"),
        "response": model_result.get("response", ""),
        "status": model_result.get("status"),
        "error": model_result.get("error"),
        "latency": model_result.get("latency"),
        "processed_by": "IMA_identity_layer",
    }
