import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CanonicalLoopJournalTests(unittest.TestCase):
    def test_canonical_loop_persists_development_transitions(self):
        p = ROOT / ".ima" / "loop" / "unified_loop.py"
        text = p.read_text(encoding="utf-8")
        self.assertIn("def append_journal", text)
        self.assertIn('JOURNAL = ROOT/".ima/journal/development.jsonl"', text)
        self.assertIn('"event": "canonical_loop_task"', text)
        self.assertIn('"event": "canonical_loop_cycle"', text)
        self.assertIn('"GAPS_RECORDED"', text)

if __name__ == "__main__":
    unittest.main()
