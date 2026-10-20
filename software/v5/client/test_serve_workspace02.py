"""Test-only path correction; preserve all original serving assertions.

The small local-check snapshot selects the Python location package at
v5/location, not the boot launcher's separate portable/location tree.
Serving never executes location code, but correctly requires this contextual
source root to exist. The first failed run remains unchanged.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_serve_workspace as original


class ServingControls(original.ServingControls):
    def context(self, *args, **kwargs):
        value = super().context(*args, **kwargs)
        value.sources_portable = original.SOURCE/"location"
        return value


if __name__ == "__main__":
    original.ServingControls = ServingControls
    raise SystemExit(original.main())
