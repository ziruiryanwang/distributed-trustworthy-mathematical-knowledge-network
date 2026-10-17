"""One selected two-form control run; no earlier suite or real proof launch."""
import json
import unittest


def main(context):
    from client import test_workspace_evidence as T
    T.EVIDENCE = context.location_workspace/"evidence-controls"
    T.EVIDENCE.mkdir()
    suite = unittest.TestSuite(T.EvidenceControls(name) for name in T.SELECTED)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = result.wasSuccessful() and result.testsRun == len(T.SELECTED) and not result.skipped
    report = {"status": "PASS_SYNTHETIC_TWO_FORM_CONTROLS" if ok else "FAIL",
        "tests": result.testsRun, "selected": list(T.SELECTED), "errors": len(result.errors),
        "failures": len(result.failures), "skipped": len(result.skipped),
        "native_calls": 0, "receipt_verifications": 0, "node_launches": 0, "proof_calls": 0,
        "socket_calls": 0, "scope": "REAL_TWO_FORM_STORAGE_DISPATCH_BUDGET_WITH_SYNTHETIC_ISSUERS",
        "transport": "REAL_PROVIDER_DISPATCH_AND_CLIENT_REQUESTS_WITH_INERT_EXCHANGE_AND_SEARCH",
        "authority": "FABRICATED_HANDLES_NOT_GENUINE_A_OR_MATHEMATICAL_EVIDENCE",
        "enclosing_job": "SEPARATELY_REPORTED_BY_PUBLIC_LAUNCHER"}
    with (T.EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True)
    return 0 if ok else 1
