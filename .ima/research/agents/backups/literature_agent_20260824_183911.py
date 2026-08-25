
class LiteratureAgent:

    name = "LITERATURE"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "CAPABILITY_PENDING",
            "question": question,
            "requires": [
                "literature/search provider"
            ],
            "contract": (
                "Return scientific papers, evidence, "
                "contradictions and source metadata."
            )
        }
