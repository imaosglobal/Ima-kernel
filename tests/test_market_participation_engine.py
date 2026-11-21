import unittest
from learning.market_participation_engine import (
    MarketOpportunity, MarketParticipationStatus, validate_opportunity,
    participation_paths,
)


class MarketParticipationTests(unittest.TestCase):
    def test_validates_real_market_offer(self):
        x = MarketOpportunity(
            "device integration", "same IMA across devices",
            "universal_device_interoperability",
            "IMA device adapter and SDK",
            "hardware pilot",
            "integration value plus distribution",
            "successful authenticated device session",
            status=MarketParticipationStatus.OFFER_READY,
        )
        self.assertEqual(validate_opportunity(x)["status"], MarketParticipationStatus.OFFER_READY)

    def test_rejects_empty_market_offer(self):
        x = MarketOpportunity("", "problem", "capability", "offer", "path", "value", "metric")
        with self.assertRaises(ValueError):
            validate_opportunity(x)

    def test_has_multiple_market_paths(self):
        self.assertIn("direct_product", participation_paths())
        self.assertIn("device_integration", participation_paths())
        self.assertIn("licensing", participation_paths())


if __name__ == "__main__":
    unittest.main()
