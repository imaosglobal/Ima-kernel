import unittest

from learning.collaboration_value_engine import (
    CollaborationOpportunity,
    CollaborationStatus,
    qualify,
    value_types,
)
from learning.ip_provenance_vault import IPAssetRecord, record_asset
from learning.ima_personality_system import personality_contract
from learning.universal_device_interoperability import register_adapter


class CollaborationIPPersonalityDeviceTests(unittest.TestCase):
    def test_collaboration_becomes_outreach_ready_but_stays_approved(self):
        row = qualify(CollaborationOpportunity(
            "Example", "robotics", "embodied interaction",
            "integration research", "new device surface",
        ))
        self.assertEqual(row["status"], CollaborationStatus.OUTREACH_READY)
        self.assertTrue(row["requires_human_approval"])

    def test_value_types_include_material_and_nonmaterial_value(self):
        self.assertIn("revenue", value_types())
        self.assertIn("knowledge", value_types())
        self.assertIn("social_impact", value_types())

    def test_ip_requires_provenance(self):
        row = record_asset(IPAssetRecord(
            "ip-1", "Example", "copyright", "source repository",
            ("human contributor",), "steward", "global",
            "license pending", "commit:abc",
        ))
        self.assertEqual(row["status"], "PROVENANCE_RECORDED")

    def test_personality_is_explicit(self):
        p = personality_contract()
        self.assertIn("truth before announcement", p["behavior"])

    def test_device_adapter_has_one_memory_authority(self):
        row = register_adapter("smart_mirror", ("camera", "voice", "display"), "secure_adapter")
        self.assertEqual(row["memory_authority"], "canonical_ima_only")


if __name__ == "__main__":
    unittest.main()
