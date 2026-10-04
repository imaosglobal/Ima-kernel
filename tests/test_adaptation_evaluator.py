import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"integrations/IMA_ADAPTATION_MATRIX.json"
ENGINE=ROOT/".ima/web_intelligence/adaptation_evaluator.py"

class AdaptationTests(unittest.TestCase):
    def test_matrix_is_broad_and_has_acceptance_rules(self):
        data=json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["dimensions"]),10)
        self.assertGreaterEqual(len(data["acceptance"]),5)

    def test_engine_compiles(self):
        subprocess.run([sys.executable,"-m","py_compile",str(ENGINE)],check=True)

if __name__=="__main__":
    unittest.main()
