"""One trusted local owner strategy for the changed client/portable path controls.

Runs through the NEW public launcher, inside its actual enclosing Job. Synthetic
unit helpers never perform native/cryptographic verification. This is not a
mathematical workload, network service or proof-production operation.
"""
import json
import unittest


def main(context):
    from client import test_paths, test_workspace
    root = context.location_workspace/"controls"
    root.mkdir()
    test_paths.EVIDENCE = root/"paths"; test_paths.EVIDENCE.mkdir()
    test_paths.EXPECTED_OVERLAY = context.sources_portable
    test_workspace.EVIDENCE = root/"workspace"; test_workspace.EVIDENCE.mkdir()
    suite = unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(test_paths.PortablePathControls),
        unittest.defaultTestLoader.loadTestsFromTestCase(test_workspace.WorkspaceControls)))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = result.wasSuccessful() and result.testsRun == 14 and not result.skipped
    report = {"status": "PASS_CLIENT_PORTABLE_CONTROLS" if ok else "FAIL",
              "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
              "native_calls": 0, "receipt_verifications": 0, "node_launches": 0,
              "mathematical_authority": False, "enclosing_job": "REPORTED_BY_PUBLIC_LAUNCHER"}
    with (root/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    return 0 if ok else 1
