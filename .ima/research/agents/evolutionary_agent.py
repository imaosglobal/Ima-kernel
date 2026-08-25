
class EvolutionaryAgent:

    name = "EVOLUTIONARY_SEARCH"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Search candidate explanations or models "
                "algorithmically."
            )
        }
