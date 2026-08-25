
class DeepResearchAgent:

    name = "DEEP_RESEARCH"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "CAPABILITY_PENDING",
            "question": question,
            "requires": [
                "connected deep-research provider"
            ],
            "contract": (
                "Return sourced research, competing evidence, "
                "uncertainty and citations."
            )
        }
