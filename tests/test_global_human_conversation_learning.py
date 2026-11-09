
import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / ".ima/conversation/global_human_conversation_learning.py"

spec = importlib.util.spec_from_file_location("ghcl", MODULE)
ghcl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ghcl)

class GlobalHumanConversationLearningTests(unittest.TestCase):
    def test_private_experience_is_not_shared(self):
        item = {
            "claim": "my local experience",
            "evidence": ["first-person account"],
            "truth_state": "SUPPORTED_FINDING",
            "privacy_class": "PRIVATE",
            "consent_scope": "PRIVATE",
        }
        result = ghcl.assess(item)
        self.assertFalse(result["shareable"])
        self.assertEqual(result["truth_state"], "SUPPORTED_FINDING")

    def test_conflict_prevents_false_certainty(self):
        item = {
            "claim": "contested claim",
            "evidence": ["source-a"],
            "counterevidence": ["source-b"],
            "truth_state": "ESTABLISHED_FACT",
            "privacy_class": "PUBLIC",
            "consent_scope": "PUBLIC",
        }
        result = ghcl.assess(item)
        self.assertEqual(result["truth_state"], "OPEN_HYPOTHESIS")

    def test_missing_evidence_downgrades_claim(self):
        item = {"claim": "unsupported", "truth_state": "ESTABLISHED_FACT"}
        result = ghcl.assess(item)
        self.assertEqual(result["truth_state"], "UNKNOWN")

    def test_contract_exists(self):
        contract = json.loads((ROOT / ".ima/conversation/GLOBAL_HUMAN_CONVERSATION_LEARNING.json").read_text())
        self.assertEqual(contract["canonical_loop"], "ima-unified-loop")
        self.assertIn("Popularity is never a validation method.", contract["rules"])

if __name__ == "__main__":
    unittest.main()
