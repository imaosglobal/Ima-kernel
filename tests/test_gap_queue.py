import json
import tempfile
import unittest
from pathlib import Path

from gap_queue import CapabilityGapQueue


class GapQueueTests(unittest.TestCase):
    def _queue(self, payload):
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
        try:
            json.dump(payload, handle)
            handle.close()
            return CapabilityGapQueue(Path(handle.name))
        finally:
            pass

    def test_prioritizes_critical_before_high(self):
        queue = self._queue({
            "schema": "test",
            "policy": "evidence",
            "gaps": [
                {"id": "h", "capability": "high", "priority": "high", "state": "detected"},
                {"id": "c", "capability": "critical", "priority": "critical", "state": "implemented"},
            ],
        })
        self.assertEqual(queue.next_gap()["id"], "c")

    def test_snapshot_counts_states(self):
        queue = self._queue({
            "schema": "test",
            "policy": "evidence",
            "gaps": [
                {"id": "a", "capability": "a", "priority": "low", "state": "detected"},
                {"id": "b", "capability": "b", "priority": "low", "state": "specified"},
            ],
        })
        snapshot = queue.snapshot()
        self.assertEqual(snapshot["total"], 2)
        self.assertEqual(snapshot["by_state"]["detected"], 1)
        self.assertEqual(snapshot["by_state"]["specified"], 1)


if __name__ == "__main__":
    unittest.main()
