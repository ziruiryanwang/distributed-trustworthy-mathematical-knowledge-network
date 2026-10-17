"""Single native-free atomic-import control suite under the retained launcher."""
import json
from pathlib import Path
import sys
import unittest


def main(context):
    # Exercise the actual product import closure before legacy comparison helpers
    # load the old mixed imports module and could mask a missing eager dependency.
    from client import workspace_atomic
    from mixed_claims import imports_atomic
    from aggregate_claims.aggregate_admission_controls import fake_owner
    if "mixed_claims.imports" in sys.modules:
        raise ValueError("CONTROL_COLD_IMPORT_PRECONDITION")
    owner, *unused = fake_owner()
    owner._pins = {Path(module.__file__).resolve(): {"bytes": 1, "sha256": "00"*32}
                   for module in tuple(sys.modules.values())
                   if type(getattr(module, "__file__", None)) is str}
    session = None
    try:
        session = imports_atomic.MixedImportSession(aggregate_verifier=owner)
    finally:
        if session is not None: session.close()
        owner.close()
    from mixed_claims.test_atomic import AtomicImportControls
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AtomicImportControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = result.wasSuccessful() and result.testsRun == 13 and not result.skipped
    report = {"status": "PASS_ATOMIC_IMPORT_CONTROLS" if ok else "FAIL",
        "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
        "native_calls": 0, "receipt_verifications": 0, "proof_calls": 0,
        "cold_product_import_closure": "PASS_WITH_SYNTHETIC_OWNER_BEFORE_LEGACY_HELPER_IMPORTS",
        "owner_authority": "EXPLICITLY_FABRICATED_TEST_ONLY_NOT_MATHEMATICAL_EVIDENCE",
        "scope": "CHANGED_BOUNDARY_SEMANTICS_AND_LOGICAL_SCAN_COUNTS_NOT_RUNTIME_SPEEDUP"}
    with (context.location_workspace/"atomic-control-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True)
    return 0 if ok else 1
