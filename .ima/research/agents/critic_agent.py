
class CriticAgent:

    name = "CRITIC"

    def investigate(self, question, evidence=None):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Search for contradictions, hidden assumptions, "
                "alternative explanations, and falsification tests."
            ),
            "evidence_received": bool(evidence)
        }
