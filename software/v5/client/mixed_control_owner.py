"""One focused A-client control suite; no old suite or genuine proof gate."""
import json
import unittest


def main(context):
    from client import test_workspace_mixed as T
    T.EVIDENCE = context.location_workspace/"mixed-controls"
    T.EVIDENCE.mkdir()
    suite = unittest.TestSuite(T.MixedWorkspaceControls(name) for name in T.SELECTED)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = result.wasSuccessful() and result.testsRun == len(T.SELECTED) and not result.skipped
    report = {"status": "PASS_SYNTHETIC_PUBLIC_A_CLIENT_CONTROLS" if ok else "FAIL",
        "tests": result.testsRun, "selected": list(T.SELECTED), "errors": len(result.errors),
        "failures": len(result.failures), "skipped": len(result.skipped),
        "native_calls": 0, "receipt_verifications": 0, "node_launches": 0, "proof_calls": 0,
        "scope": "REAL_CLIENT_STORAGE_GRANTS_BUDGET_AND_PURE_BINDINGS_WITH_SYNTHETIC_ISSUERS",
        "authority": "FABRICATED_HANDLES_NOT_GENUINE_A_OR_MATHEMATICAL_EVIDENCE",
        "semantic_import": "ONE_ROUTING_STUB_NOT_MATERIALIZATION_QUALIFICATION",
        "enclosing_job": "SEPARATELY_REPORTED_BY_PUBLIC_LAUNCHER"}
    with (T.EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True)
    return 0 if ok else 1
