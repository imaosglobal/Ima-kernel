import unittest

from core.ima_loop import LOOP_STAGES, loop_context, loop_contract


class UnifiedLoopTests(unittest.TestCase):
    def test_single_scheduler_contract(self):
        contract = loop_contract()
        self.assertTrue(contract["single_scheduler"])
        self.assertTrue(contract["requires_explicit_learning_authorization"])
        self.assertTrue(contract["requires_runtime_verification"])
        self.assertTrue(contract["lawful_distribution_only"])

    def test_all_required_stages_exist(self):
        required = {
            "REMEMBER", "PRESERVE", "OBSERVE", "DISCOVER", "LISTEN",
            "UNDERSTAND", "SEPARATE_FACT_FROM_INFERENCE", "QUESTION",
            "CONNECT", "CREATE", "HUMANIZE", "TEST", "VERIFY",
            "CORRECT", "TEACH", "SHARE_LAWFULLY", "CARRY_FORWARD",
        }
        self.assertTrue(required.issubset(set(LOOP_STAGES)))
        self.assertIn("single canonical improvement, learning, preservation", loop_context())
        self.assertIn("add this to the loop", loop_context())

if __name__ == "__main__":
    unittest.main()
