import unittest
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
p=Path(__file__).resolve().parents[1]/".ima/web_intelligence/trend_to_brand.py"
s=spec_from_file_location("ttb",p); m=module_from_spec(s); s.loader.exec_module(m)
class TrendTests(unittest.TestCase):
    def test_card_is_research_only(self):
        c=m.build_card({"url":"https://example.com","source":"x","observed_at":"2026-10-12T00:00:00Z","signal_strength":.8})
        self.assertEqual(c["status"],"RESEARCH_ONLY")
        self.assertFalse(c["commercial_action_allowed"])
    def test_score_is_bounded(self):
        c=m.build_card({"url":"https://example.com","source":"x","signal_strength":1},independent_sources=3,persistence=1,purchase_intent=1,competition=0,safety=1,testability=1)
        self.assertLessEqual(c["opportunity_score"],100)
if __name__=="__main__": unittest.main()
