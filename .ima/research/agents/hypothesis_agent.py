
class HypothesisAgent:

    name = "HYPOTHESIS"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Generate multiple competing hypotheses "
                "without selecting one prematurely."
            )
        }
