import unittest
from core.universal_learning_engine import Capability, CapabilityState
from core.capability_self_application import propose_self_application, can_apply

class SelfApplicationTests(unittest.TestCase):
    def test_unverified_capability_cannot_self_apply(self):
        with self.assertRaises(ValueError):
            propose_self_application(Capability("x","x",CapabilityState.TESTED),"site","improve")
    def test_verified_capability_creates_bounded_plan(self):
        c=Capability("x","x",CapabilityState.VERIFIED_LIVE)
        p=propose_self_application(c,"site","improve")
        self.assertEqual(p.gates,("INSPECT","PLAN","CHANGE","TEST","VERIFY","CARRY_FORWARD"))
        self.assertFalse(can_apply(p,False))

if __name__=="__main__": unittest.main()
