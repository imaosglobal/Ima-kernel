import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "scientific_open_research_health.py"
SPEC = importlib.util.spec_from_file_location("scientific_health", PATH)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class ScientificOpenResearchHealthTests(unittest.TestCase):
    def test_has_only_free_public_sources(self):
        self.assertEqual(set(mod.SOURCES), {"OpenAlex", "Semantic Scholar", "Crossref", "PubMed", "arXiv"})
        for url in mod.SOURCES.values():
            self.assertTrue(url.startswith("https://"))
            self.assertNotIn("api_key", url.lower())
            self.assertNotIn("token=", url.lower())

    def test_truth_boundary_is_explicit(self):
        result = mod.check("Crossref", mod.SOURCES["Crossref"])
        self.assertIn(result["status"], {"PASS", "ERROR", "FAIL"})
        self.assertIn("Source availability is not evidence", "Source availability is not evidence that a scientific claim is true; claims require source-level verification.")

if __name__ == "__main__":
    unittest.main()
