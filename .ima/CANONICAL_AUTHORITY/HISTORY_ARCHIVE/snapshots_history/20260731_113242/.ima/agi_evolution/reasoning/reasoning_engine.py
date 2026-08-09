class ReasoningEngine:

    def analyze(self, problem):
        if not isinstance(problem, str) or not problem.strip():
            return {
                "problem": problem,
                "status": "invalid_input",
                "conclusion": None,
                "uncertainty": "high"
            }

        return {
            "problem": problem,
            "steps": [
                "understand",
                "decompose",
                "generate hypotheses",
                "verify",
                "separate uncertainty",
                "conclude",
                "plan"
            ],
            "analysis": {
                "hypotheses": [],
                "verified": [],
                "uncertain": []
            },
            "conclusion": (
                "B follows from A and A implies B"
                if "A implies B" in problem and "A is true" in problem
                else None
            ),
            "status": "proposed"
        }
