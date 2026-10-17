import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

class GlobalGrowthContractTests(unittest.TestCase):
    def test_growth_contract_files_exist(self):
        for path in (
            "docs/IMA_GLOBAL_GROWTH_AND_USER_TRUTH.md",
            "docs/IMA_USER_FEEDBACK_AND_REPUTATION.md",
            "docs/IMA_APP_STORE_LAUNCH_CHECKLIST.md",
            "docs/IMA_GLOBAL_GROWTH_EXPERIMENTS.md",
            "feedback.html",
            "scripts/ima_growth_cycle.py",
        ):
            self.assertTrue((ROOT / path).exists(), path)

    def test_growth_cycle_does_not_claim_users(self):
        spec = importlib.util.spec_from_file_location("growth", ROOT / "scripts/ima_growth_cycle.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        state = module.run()
        self.assertEqual(state["principle"], "real_users_only")
        self.assertFalse(state["distribution"]["store_listing_verified"])
        self.assertIn("UNKNOWN", state["truth_rule"])

    def test_public_feedback_is_present(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("./feedback.html", html)
        self.assertNotIn("\\ntrack('page_view'", html)

if __name__ == "__main__":
    unittest.main()
