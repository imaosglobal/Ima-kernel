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
    def test_single_source_cannot_support_significant_conclusion(self):
        c=m.build_card({"url":"https://example.com","source":"x","signal_strength":.8},independent_sources=1)
        self.assertFalse(c["significant_conclusion_allowed"])
        self.assertEqual(c["evidence_state"],"SINGLE_SOURCE_PENDING")

    def test_multiple_sources_unlock_evidence_gate(self):
        c=m.build_card({"url":"https://example.com","source":"x","signal_strength":.8},independent_sources=2)
        self.assertTrue(c["significant_conclusion_allowed"])
        self.assertEqual(c["evidence_state"],"MULTI_SOURCE")

    def test_score_includes_business_risk_dimensions(self):
        item={"url":"https://example.com","source":"x","signal_strength":1,
              "audience_size":1,"unmet_need":1,"price_fit":1,
              "gross_margin_estimate":1,"production_complexity":0,
              "regulatory_burden":0,"logistics_complexity":0,
              "sustainability_fit":1,"inventory_risk":0,"cultural_fit":1}
        c=m.build_card(item,independent_sources=3,persistence=1,
                       purchase_intent=1,competition=0,safety=1,testability=1)
        self.assertGreater(c["opportunity_score"],0)
        safe = m.build_card(item,independent_sources=3,persistence=1,purchase_intent=1,competition=0,safety=1,testability=1)["opportunity_score"]
        unsafe = m.build_card(item,independent_sources=3,persistence=1,purchase_intent=1,competition=0,safety=0,testability=1)["opportunity_score"]
        self.assertGreater(safe, unsafe)
        self.assertIn("creator_rights_status",c)
        self.assertEqual(c["commerce_channel_status"],"UNVERIFIED")

    def test_multiple_public_sources_are_preserved(self):
        item={"url":"https://a.example","source":"a","signal_strength":.8,
              "sources":[{"url":"https://b.example","observed_at":"2026-10-14T00:00:00Z"}],
              "independent_sources":2}
        c=m.build_card(item)
        self.assertEqual(len(c["demand_evidence"]),2)
        self.assertTrue(c["significant_conclusion_allowed"])

    def test_score_is_bounded(self):
        c=m.build_card({"url":"https://example.com","source":"x","signal_strength":1},independent_sources=3,persistence=1,purchase_intent=1,competition=0,safety=1,testability=1)
        self.assertLessEqual(c["opportunity_score"],100)
if __name__=="__main__": unittest.main()
