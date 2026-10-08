import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".ima/contracts/n8n_agent_contract.json"
MATRIX = ROOT / "integrations/IMA_ADAPTATION_MATRIX.json"

class N8NInteroperabilityContractTests(unittest.TestCase):
    def test_contract_is_research_only_and_scope_bound(self):
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "RESEARCH_CANDIDATE")
        self.assertFalse(data["enabled"])
        self.assertEqual(data["action_authority"], "none")
        self.assertEqual(data["tool_scope"], "explicit_only")
        self.assertTrue(data["approval_required_for_sensitive_actions"])

    def test_contract_requires_evidence_before_adoption(self):
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["adoption_gate"], "implementation + tests + runtime_or_external_verification")
        self.assertTrue(data["required_evidence"]["source"])
        self.assertTrue(data["required_evidence"]["test"])
        self.assertTrue(data["required_evidence"]["verification"])

    def test_matrix_contains_n8n_candidate(self):
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(data["sources"]["n8n_agents"]["status"], "RESEARCH_CANDIDATE")
        self.assertIn("n8n_mcp_tool_boundary", data["sources"]["n8n_agents"]["tests"])

if __name__ == "__main__":
    unittest.main()
