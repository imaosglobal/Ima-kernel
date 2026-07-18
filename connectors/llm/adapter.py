import time

def normalize(provider, response):
    return {
        "provider": provider,
        "response": response,
        "time": time.time(),
        "source": "external_model"
    }


def choose(results):
    if not results:
        return {
            "provider": "none",
            "response": "",
            "status": "no_models"
        }

    # עדיפות עתידית: דירוג לפי איכות/מהירות
    first = next(iter(results))

    return normalize(
        first,
        results[first]
    )
