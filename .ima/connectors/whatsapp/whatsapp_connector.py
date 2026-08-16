import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

CANONICAL = (
    ROOT
    / ".ima"
    / "CANONICAL_AUTHORITY"
    / "SINGLE_SNAPSHOT"
    / "CURRENT"
    / "connectors"
    / "whatsapp"
)

if str(CANONICAL) not in sys.path:
    sys.path.insert(0, str(CANONICAL))

from whatsapp_connector import WhatsAppConnector, whatsapp

__all__ = ["WhatsAppConnector", "whatsapp"]
