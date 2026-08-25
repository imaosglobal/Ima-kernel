
from pathlib import Path
import json


class QuestionEngine:

    def decompose(self, question):

        return {
            "primary_question": question,

            "subquestions": [
                {
                    "id": "empirical",
                    "question": (
                        "What observations or measurements can "
                        "actually bear on the question?"
                    ),
                    "agents": [
                        "DEEP_RESEARCH",
                        "LITERATURE"
                    ]
                },

                {
                    "id": "mechanism",
                    "question": (
                        "What mechanisms could explain the "
                        "observed phenomenon without assuming "
                        "the conclusion?"
                    ),
                    "agents": [
                        "MEDA",
                        "HYPOTHESIS"
                    ]
                },

                {
                    "id": "alternatives",
                    "question": (
                        "What competing explanations exist?"
                    ),
                    "agents": [
                        "HYPOTHESIS",
                        "DEEP_RESEARCH"
                    ]
                },

                {
                    "id": "criticism",
                    "question": (
                        "What are the strongest arguments against "
                        "each proposed explanation?"
                    ),
                    "agents": [
                        "CRITIC"
                    ]
                },

                {
                    "id": "testability",
                    "question": (
                        "What observations or experiments could "
                        "distinguish the competing hypotheses?"
                    ),
                    "agents": [
                        "MEDA",
                        "LITERATURE",
                        "CRITIC"
                    ]
                },

                {
                    "id": "unknowns",
                    "question": (
                        "What remains genuinely unknown?"
                    ),
                    "agents": [
                        "CRITIC",
                        "LITERATURE"
                    ]
                }
            ]
        }
