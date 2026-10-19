import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class HumanAgencyIntelligibilityTests(unittest.TestCase):
    def test_charter(self):
        x=(ROOT/"docs/IMA_HUMAN_AGENCY_AND_INTELLIGIBILITY_CHARTER.md").read_text(encoding="utf-8")
        for q in ("Intelligibility","Contestability","Human override","Independent verification","Reversibility","Concentration monitoring","Safe degradation","Anti-dependency test","PLANNED -> IMPLEMENTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE"):
            self.assertIn(q,x)
    def test_loop(self):
        x=(ROOT/".ima/loop/unified_loop.py").read_text(encoding="utf-8")
        for q in ("human agency and intelligibility","human_agency_tests","human_agency_rule","critical_ai_dependency_rule"):
            self.assertIn(q,x)
