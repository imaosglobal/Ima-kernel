from pathlib import Path
import sys

ROOT = Path.home() / "ima_kernel"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from importlib.util import (
    spec_from_file_location,
    module_from_spec,
)

IO_PATH = (
    ROOT
    / ".ima/canonical_state_guard/canonical_io.py"
)

_spec = spec_from_file_location(
    "ima_canonical_io",
    IO_PATH
)

_module = module_from_spec(_spec)
_spec.loader.exec_module(_module)

load_memory = _module.load_memory
save_memory = _module.save_memory
