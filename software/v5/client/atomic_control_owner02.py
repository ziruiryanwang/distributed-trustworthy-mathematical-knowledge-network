"""Only the three controls not reached because of controls01's fixture error."""
import json
import unittest


def main(context):
    from mixed_claims.test_atomic02 import AtomicImportControls
    selected = (
        "test_call_data_and_submitted_caps_are_not_bypassed",
        "test_context_selection_and_onward_equal_incremental_semantics",
        "test_need_is_extendable_then_ready_seals")
    suite = unittest.TestSuite(AtomicImportControls(name) for name in selected)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = result.wasSuccessful() and result.testsRun == 3 and not result.skipped
    report = {"status": "PASS_ATOMIC_IMPORT_REMAINING_CONTROLS" if ok else "FAIL",
        "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
        "selected": list(selected), "native_calls": 0, "receipt_verifications": 0, "proof_calls": 0,
        "prior": "atomic-import-controls-01_RETAINED_FAIL_WITH_TEN_PASSES_AND_COLD_GATE",
        "scope": "THREE_UNREACHED_CONTROLS_AFTER_TEST_FIXTURE_METADATA_REPAIR",
        "owner_authority": "EXPLICITLY_FABRICATED_TEST_ONLY_NOT_MATHEMATICAL_EVIDENCE"}
    with (context.location_workspace/"atomic-control-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True)
    return 0 if ok else 1
