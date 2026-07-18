import time

def wrap_response(model_result, identity="IMA"):

    return {
        "time": time.time(),
        "identity": identity,
        "engine": model_result.get("model","unknown"),
        "response": model_result.get("response",""),
        "processed_by": "IMA_identity_layer"
    }
