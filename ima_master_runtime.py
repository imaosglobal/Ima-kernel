"""
IMA Master Runtime compatibility adapter.

Keeps the historical API expected by api.server.py while
delegating actual reasoning to the current canonical ima_system layer.
"""

import ima_system


class IMAMaster:
    def __init__(self):
        self.name = "IMA MASTER"

    def ask(self, message):
        result = ima_system.ask(message)

        if isinstance(result, dict):
            return {
                **result,
                "response": result.get("text", ""),
            }

        return {
            "response": str(result),
        }


IMA = IMAMaster()


def ask(message):
    return IMA.ask(message)
