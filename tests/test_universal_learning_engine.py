import unittest
from core.universal_learning_engine import Capability, CapabilityState, Domain, EvidenceLevel, Source, connect_domains, propose_field, knowledge_packet
from core.capability_substitution import CapabilityRegistry

class UniversalLearningEngineTests(unittest.TestCase):
    def test_evidence_and_unknowns_are_preserved(self):
        source=Source("Example","urn:test",EvidenceLevel.HYPOTHESIS)
        packet=knowledge_packet(Domain("Test","A test domain",sources=[source],open_questions=["unknown"]))
        self.assertEqual(packet["sources"][0]["evidence"],EvidenceLevel.HYPOTHESIS)
        self.assertIn("unknown",packet["open_questions"])
    def test_emerging_field_is_only_a_proposal(self):
        self.assertEqual(propose_field("X","candidate",["A"],[],["Q"]).status,"PROPOSAL")
    def test_domains_connect_both_ways(self):
        a,b=Domain("A","a"),Domain("B","b"); connect_domains(a,b)
        self.assertIn("B",a.connections); self.assertIn("A",b.connections)
    def test_capability_requires_verified_state(self):
        r=CapabilityRegistry(); r.register(Capability("web_building","build sites",CapabilityState.DISCOVERED))
        self.assertEqual(len(r.unresolved()),1)
        for state in (CapabilityState.CONNECTED,CapabilityState.TESTED,CapabilityState.DEPLOYED,CapabilityState.VERIFIED_LIVE): r.promote("web_building",state)
        self.assertEqual(r.unresolved(),[])
if __name__=="__main__": unittest.main()
