import unittest

from core.ima_loop import IMA_IDENTITY_CONTEXT, LOOP_STAGES, loop_context, loop_contract


class UnifiedLoopTests(unittest.TestCase):
    def test_single_scheduler_contract(self):
        contract = loop_contract()
        self.assertTrue(contract["single_scheduler"])
        self.assertTrue(contract["requires_explicit_learning_authorization"])
        self.assertTrue(contract["requires_runtime_verification"])
        self.assertTrue(contract["lawful_distribution_only"])\n        self.assertTrue(contract["universal_learning"])\n        self.assertTrue(contract["capability_self_application"])\n        self.assertTrue(contract["capability_teaching"])\n        self.assertTrue(contract["provider_independence"])

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

    def test_ima_knows_self_world_and_user_boundaries(self):
        contract = loop_contract()
        self.assertTrue(contract["identity"]["one_global_ima"])
        self.assertTrue(contract["identity"]["human_centered"])
        self.assertTrue(contract["identity"]["world_model_is_uncertain_and_updateable"])
        self.assertTrue(contract["identity"]["user_context_is_private_by_default"])
        self.assertIn("one global human-centered intelligence identity", IMA_IDENTITY_CONTEXT)
        self.assertIn("Private user context is isolated", IMA_IDENTITY_CONTEXT)
        self.assertIn("current user is the immediate human context", IMA_IDENTITY_CONTEXT)\n        self.assertIn("Every verified capability belongs to two paths", IMA_IDENTITY_CONTEXT)

if __name__ == "__main__":
    unittest.main()
