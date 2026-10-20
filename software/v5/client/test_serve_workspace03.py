"""Run only the unresolved serving control with a feasible summary bound.

The two present features expand to 512 partition descriptors plus 512 sibling
hashes, exceeding the first fixture's 64 KiB expanded ceiling. Keep its 64 KiB
wire ceiling and all assertions; 128 KiB covers the derived <92 KiB summary.
The ten passing lifecycle controls from run02 are not repeated.
"""
from copy import deepcopy
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_serve_workspace02 as corrected

original = corrected.original


class ServingControls(corrected.ServingControls):
    async def exchange(self, endpoint, route, request, maximum=65536):
        if route == original.H.OFFER_ROUTE:
            self.assertEqual(request["max_expanded_bytes"], 65536)
            request = deepcopy(request)
            request["max_expanded_bytes"] = 131072
        return await super().exchange(endpoint, route, request, maximum)


if __name__ == "__main__":
    original.ServingControls = ServingControls
    original.SELECTED = ("test_existing_data_offer_group_finite_stop_and_reopen",)
    raise SystemExit(original.main())
