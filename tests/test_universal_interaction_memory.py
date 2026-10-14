import tempfile, unittest
from pathlib import Path
import public_memory
from importlib.util import spec_from_file_location, module_from_spec

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/".ima/memory/universal_interaction_memory.py"
s=spec_from_file_location("uim",p); m=module_from_spec(s); s.loader.exec_module(m)

class UniversalMemoryTests(unittest.TestCase):
    def test_consent_blocks_learning_without_grant(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                with self.assertRaises(ValueError):
                    m.capture(user_id="u",source="chat",content="x",consent="UNKNOWN",authorized_learning=True)
            finally: public_memory._DB=old
    def test_missing_consent_blocks_capture(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                with self.assertRaises(ValueError):
                    m.capture(user_id="u",source="chat",content="hello",consent="UNKNOWN")
            finally: public_memory._DB=old

    def test_capture_requires_stored_grant(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                with self.assertRaises(ValueError):
                    m.capture(user_id="u",source="chat",content="hello",consent="GRANTED")
                m.set_consent("u","GRANTED")
                row=m.capture(user_id="u",source="chat",content="hello",consent="GRANTED")
                self.assertEqual(row["status"],"EXECUTED")
            finally: public_memory._DB=old

    def test_denied_consent_blocks_capture(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                m.set_consent("u","DENIED")
                with self.assertRaises(ValueError):
                    m.capture(user_id="u",source="chat",content="hello",consent="DENIED")
            finally: public_memory._DB=old

    def test_consent_and_audit(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                m.set_consent("u","GRANTED")
                self.assertEqual(m.get_consent("u")["status"],"GRANTED")
                self.assertEqual(m.audit_events("u")[0]["action"],"CONSENT_UPDATE")
            finally: public_memory._DB=old

    def test_secret_like_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                with self.assertRaises(ValueError):
                    m.capture(user_id="u",source="chat",content="Authorization: Bearer abc",consent="GRANTED")
            finally: public_memory._DB=old

    def test_roundtrip_and_delete(self):
        with tempfile.TemporaryDirectory() as td:
            old=public_memory._DB; public_memory._DB=Path(td)/"m.sqlite3"
            try:
                m.set_consent("u","GRANTED")
                m.capture(user_id="u",source="chat",content="hello",consent="GRANTED",authorized_learning=True)
                rows=m.export_user_memory("u")
                self.assertEqual(len(rows),1)
                self.assertEqual(len(m.learning_records()),1)
                self.assertEqual(m.delete_user_memory("u"),1)
                self.assertEqual(m.export_user_memory("u"),[])
                self.assertEqual([x["action"] for x in m.audit_events("u")],["CONSENT_UPDATE","CAPTURE","DELETE"])
            finally: public_memory._DB=old

if __name__=="__main__": unittest.main()
