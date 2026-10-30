import unittest
from unittest.mock import patch

import ima_master_runtime


class MasterRuntimeResilienceTests(unittest.TestCase):
    def test_public_runtime_does_not_expose_internal_shape_errors(self):
        with patch.object(ima_master_runtime, "ima_llm_answer", return_value={"status": "error", "error": "provider unavailable"}),              patch.object(ima_master_runtime, "search_concept", return_value=[{"id": "demo"}]),              patch.object(
                 ima_master_runtime,
                 "build_answer",
                 side_effect=TypeError("list indices must be integers or slices, not str"),
             ),              patch.object(ima_master_runtime.ima_mom, "generate_answer", return_value="תשובת IMA בטוחה"):
            result = ima_master_runtime.ask(
                "שאלה לבדיקה",
                user_id="public:test",
                public=True,
                public_memory=[],
            )

        self.assertEqual(result.get("response"), "תשובת IMA בטוחה")
        self.assertNotIn("list indices must be integers or slices, not str", result.get("response", ""))
        self.assertNotIn("IMA runtime fallback:", result.get("response", ""))
        self.assertIn("knowledge_error", result)


if __name__ == "__main__":
    unittest.main()
