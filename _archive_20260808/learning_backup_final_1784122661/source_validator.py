
def validate(source):

    if not source:
        return {
            "verified":False,
            "confidence":0
        }

    confidence=source.get("confidence",0)

    return {
        "verified": confidence >= 0.7,
        "confidence": confidence,
        "checks":[
            "source_exists",
            "confidence_score"
        ]
    }
