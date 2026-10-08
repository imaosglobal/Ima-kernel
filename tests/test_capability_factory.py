import unittest
from datetime import datetime, timezone
from pathlib import Path

import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / ".ima" / "plugins" / "capability_factory.py"
spec = importlib.util.spec_from_file_location("ima_capability_factory_test", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CapabilityAdapter = module.CapabilityAdapter
CapabilityEvidence = module.CapabilityEvidence
CapabilityGap = module.CapabilityGap
verify_adapter = module.verify_adapter
GAP_STATES = module.GAP_STATES


class CapabilityFactoryTests:undefined