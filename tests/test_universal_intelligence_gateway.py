
import json, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class UniversalIntelligenceGatewayContractTests(unittest.TestCase):
    def test_contract_and_registry(self):
        c=json.loads((ROOT/".ima/intelligence/UNIVERSAL_INTELLIGENCE_GATEWAY.json").read_text(encoding="utf-8"))
        r=json.loads((ROOT/".ima/intelligence/PROVIDER_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertTrue(c["identity"]["provider_neutral"])
        self.assertTrue(c["truth"]["disagreement_is_preserved"])
        self.assertIn("future_provider",[p["id"] for p in r["providers"]])
    def test_no_secret_material(self):
        t=(ROOT/".ima/intelligence/PROVIDER_REGISTRY.json").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?i)(sk-[A-Za-z0-9]|AIza[A-Za-z0-9_-]{20,})",t))
    def test_gateway_contract(self):
        t=(ROOT/".ima/intelligence/universal_intelligence_gateway.py").read_text(encoding="utf-8")
        self.assertIn("def route(",t); self.assertIn("verification_required",t); self.assertIn("private",t)
if __name__=="__main__": unittest.main()
