import unittest
from core.creative_bridge import BridgeStatus, build_bridge

class CreativeBridgeTests(unittest.TestCase):
    def test_bridge_needs_tests_and_evidence(self):
        b=build_bridge('music','technology','shared creative structure','prototype')
        b.connect(); b.add_test('prototype test'); b.mark_tested(True)
        with self.assertRaises(ValueError): b.verify([])
        b.verify(['passing prototype evidence'])
        self.assertEqual(b.status, BridgeStatus.VERIFIED)

    def test_failed_bridge_is_not_verified(self):
        b=build_bridge('humanity','software','missing bridge','prototype')
        b.connect(); b.add_test('test'); b.mark_tested(False)
        self.assertNotEqual(b.status, BridgeStatus.VERIFIED)

if __name__ == '__main__': unittest.main()
