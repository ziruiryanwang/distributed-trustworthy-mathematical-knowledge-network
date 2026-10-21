"""Five pure diagnostic-helper groups; execution requires root's selection.

Only the pinned owner's three constants and four helper definitions are AST
extracted. The complete pinned formal_features module supplies real compact/need.
No owner import, PlacementService construction, lifecycle, network or proof runs.
Inputs and secrets below are synthetic. Only the selected result file is written.
"""
import argparse
import ast
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch


PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUTPUT = PROJECT / "experiments/v5-local-checks/managed-observed-controls-01"
RELATIVE = Path("software/v5/managed_observed/observation_controls.py")
OWNER_RELATIVE = Path("software/v5/managed_observed/client/managed_owner.py")
FEATURE_RELATIVE = Path("software/v5/instantiation_discovery/discovery/formal_features.py")
OWNER_BYTES = 31626
OWNER_SHA = "1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503"
FEATURE_BYTES = 10826
FEATURE_SHA = "8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c"
EXTRACTED = ("_CLOSE_FLAGS", "_CLOSE_COMPONENTS", "_CLOSE_FAILURES", "_close_enum",
             "_close_scalars", "_project_service_close", "_service_close_observation")
SCHEMA = "DMKN_V5_MANAGED_SERVICE_CLOSE_OBSERVATION_V1"
FINAL = "DMKN_V5_PLACEMENT_SERVICE_RESULT_V1"
PARTIAL = "DMKN_V5_PLACEMENT_SERVICE_STATUS_V1"
SECRET = "SYNTHETIC_ONLY_NOT_A_CREDENTIAL_7a29d6"
FLAGS = ("intake_closed", "retained_closed", "location_closed", "read_closed",
         "journal_closed", "controller_closed", "workspace_closed")
LOCATION_FLAGS = ("closed", "channel_failed", "forced_termination")
LOCATION_COUNTS = ("sent_bytes", "received_bytes", "commands", "reply_frames",
                   "stderr_bytes", "cleanup_allowance_seconds")
INTAKE_FLAGS = ("active_intake", "accepting", "stopped")
INTAKE_COUNTS = ("active_connections", "retained_closing_connections")
USED = ("requests", "incoming_reserved", "outgoing_reserved", "observed_incoming",
        "attempted_outgoing", "busy", "refused", "completed_actions", "cancelled",
        "cleanup_errors", "handler_errors")
F = H = None


def need(ok, code):
    if not ok:
        raise ValueError(code)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction() for item in (path, *path.parents)),
        "CONTROL_ORDINARY_PATH")
    return path


def pin(path, size, digest):
    ordinary(path)
    need(path.is_file() and path.stat().st_size == size, "CONTROL_SOURCE_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(size + 1)
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "CONTROL_SOURCE_PIN")
    return raw


def adopt(sources):
    global F, H
    feature_path = sources / FEATURE_RELATIVE
    feature_raw = pin(feature_path, FEATURE_BYTES, FEATURE_SHA)
    F = ModuleType("_managed_observation_actual_formal_features")
    F.__file__ = str(feature_path)
    # Execute exact authenticated bytes, not an unpinned second loader read.
    # This module imports only hashlib/json/re and writes no product state.
    exec(compile(feature_raw, str(feature_path), "exec", dont_inherit=True), F.__dict__)
    owner_path = sources / OWNER_RELATIVE
    tree = ast.parse(pin(owner_path, OWNER_BYTES, OWNER_SHA), filename=str(owner_path))
    nodes, names = [], []
    for node in tree.body:
        name = node.name if isinstance(node, ast.FunctionDef) else None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        if name in EXTRACTED:
            names.append(name)
            nodes.append(node)
    need(tuple(names) == EXTRACTED, "CONTROL_EXACT_HELPER_EXTRACTION")
    H = {"F": F, "__name__": "_managed_observation_extracted_helpers"}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(owner_path), "exec",
                 dont_inherit=True), H)


def minimal(status):
    return dict(schema=SCHEMA, observation_status=status,
                closure_authority=False, mathematical_acceptance=False)


def failed_snapshot():
    return dict(schema=FINAL, status="FAILED", failure_code="PLACEMENT_SERVICE_HEALTH_FAILED",
        started=True, closing=True, closed=False, retained_active=False,
        cleanup={**{key: True for key in FLAGS}, "location_closed": False,
                 "errors": [{"component": "location_close", "code": "CLEANUP_UNCERTAIN"}]},
        observed=dict(location={**{key: index for index, key in enumerate(LOCATION_COUNTS)},
                               "closed": False, "channel_failed": True,
                               "forced_termination": False, "returncode": 7},
                      intake={**{key: index for index, key in enumerate(INTAKE_COUNTS)},
                              "active_intake": False, "accepting": False, "stopped": True,
                              "used": {key: index for index, key in enumerate(USED)}}))


class SyntheticReportOnly:
    """A callback fixture only, never represented as a real service instance."""
    def __init__(self, raw=None, error=None):
        self.raw, self.error, self.calls = raw, error, 0

    def report(self):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.raw


class SecretError(BaseException):
    rendered = 0

    def __str__(self):
        type(self).rendered += 1
        return SECRET

    def __repr__(self):
        type(self).rendered += 1
        return SECRET


class Controls(unittest.TestCase):
    def project(self, raw):
        result = H["_project_service_close"](raw)
        self.assertEqual(result["schema"], SCHEMA)
        self.assertIs(result["closure_authority"], False)
        self.assertIs(result["mathematical_acceptance"], False)
        self.assertLessEqual(len(F.compact(result)), 8192)
        return result

    def test_01_failed_snapshot_exact_whitelist(self):
        raw = failed_snapshot()
        before = deepcopy(raw)
        callback = SyntheticReportOnly(raw)
        result = H["_service_close_observation"](callback)
        expected = {**minimal("FINAL_SNAPSHOT"),
            "service": dict(started=True, closing=True, closed=False, retained_active=False,
                            status="FAILED", failure_code="PLACEMENT_SERVICE_HEALTH_FAILED"),
            "cleanup": {**before["cleanup"], "errors_available": True, "errors_truncated": False},
            "location": {**before["observed"]["location"], "available": True},
            "intake": {**before["observed"]["intake"], "available": True}}
        self.assertEqual(result, expected)
        self.assertEqual(callback.calls, 1)
        self.assertEqual(raw, before)
        self.assertEqual(self.project(raw), expected)
        for failure in ("PLACEMENT_SERVICE_START_FAILED", None):
            raw["failure_code"] = failure
            self.assertEqual(self.project(raw)["service"]["failure_code"], failure)
        raw.update(status="CLOSED", failure_code=None)
        self.assertEqual(self.project(raw)["service"]["status"], "CLOSED")

    def test_02_partial_missing_and_unrecognized(self):
        raw = dict(schema=PARTIAL, started=True)
        result = self.project(raw)
        self.assertEqual(result["observation_status"], "PARTIAL_SNAPSHOT")
        self.assertIs(result["service"]["started"], True)
        self.assertIsNone(result["service"]["closed"])
        self.assertIsNone(result["service"]["status"])
        self.assertFalse(result["cleanup"]["errors_available"])
        self.assertFalse(result["cleanup"]["errors_truncated"])
        self.assertEqual(result["cleanup"]["errors"], [])
        self.assertFalse(result["location"]["available"])
        self.assertFalse(result["intake"]["available"])
        self.assertTrue(all(value is None for value in result["intake"]["used"].values()))
        for malformed in (None, [], SECRET, {}, {"schema": SECRET}, {"schema": 1}):
            self.assertEqual(self.project(malformed), minimal("UNRECOGNIZED_REPORT"))
        class DictSubclass(dict):
            pass
        self.assertEqual(self.project(DictSubclass(schema=FINAL)), minimal("UNRECOGNIZED_REPORT"))
        for bad in (None, [], SECRET, DictSubclass(errors=[])):
            result = self.project(dict(schema=FINAL, cleanup=bad, observed=bad))
            self.assertFalse(result["cleanup"]["errors_available"])
            self.assertFalse(result["location"]["available"])
            self.assertFalse(result["intake"]["available"])

    def test_03_exact_scalars_bounds_and_32_rows(self):
        class IntSubclass(int):
            pass
        for value in (0, 1, "true", [], {}, None):
            raw = failed_snapshot()
            raw.update({key: value for key in ("started", "closing", "closed", "retained_active")})
            raw["cleanup"].update({key: value for key in FLAGS})
            raw["observed"]["location"].update({key: value for key in LOCATION_FLAGS})
            raw["observed"]["intake"].update({key: value for key in INTAKE_FLAGS})
            result = self.project(raw)
            for section, keys in (("service", ("started", "closing", "closed", "retained_active")),
                                  ("cleanup", FLAGS), ("location", LOCATION_FLAGS), ("intake", INTAKE_FLAGS)):
                self.assertTrue(all(result[section][key] is None for key in keys))
        for value in (True, False, -1, 2**53, 1.0, "1", IntSubclass(1), 0, 2**53-1):
            raw = failed_snapshot()
            raw["observed"]["location"].update({key: value for key in LOCATION_COUNTS})
            raw["observed"]["intake"].update({key: value for key in INTAKE_COUNTS})
            raw["observed"]["intake"]["used"] = {key: value for key in USED}
            result = self.project(raw)
            expected = value if type(value) is int and 0 <= value <= 2**53-1 else None
            self.assertEqual({result["location"][key] for key in LOCATION_COUNTS}, {expected})
            self.assertEqual({result["intake"][key] for key in INTAKE_COUNTS}, {expected})
            self.assertEqual(set(result["intake"]["used"].values()), {expected})
        for value in (True, 1.0, IntSubclass(1), -2**31-1, 2**32, -2**31, 2**32-1):
            raw = failed_snapshot()
            raw["observed"]["location"]["returncode"] = value
            expected = value if type(value) is int and -2**31 <= value <= 2**32-1 else None
            self.assertEqual(self.project(raw)["location"]["returncode"], expected)
        row = dict(component="live_actor_prevents_store_close", code="CLEANUP_UNCERTAIN")
        for count in (32, 33):
            raw = failed_snapshot()
            raw["cleanup"]["errors"] = [dict(row) for unused in range(count)]
            result = self.project(raw)["cleanup"]
            self.assertEqual(result["errors"], [row] * 32)
            self.assertEqual(result["errors_truncated"], count > 32)
        raw["cleanup"]["errors"] = [None, SECRET, {}]
        self.assertEqual(self.project(raw)["cleanup"]["errors"],
                         [dict(component=None, code=None)] * 3)
        raw["cleanup"]["errors"] = (row,)
        self.assertFalse(self.project(raw)["cleanup"]["errors_available"])

    def test_04_synthetic_secret_redaction(self):
        SecretError.rendered = 0
        raw = failed_snapshot()
        raw.update(status=SECRET, failure_code=SecretError(SECRET),
                   token=SECRET, credential={SECRET: SECRET}, route={SECRET: SECRET},
                   bindings={SECRET: SECRET}, stderr=SECRET, traceback=SECRET)
        raw["cleanup"].update(message=SECRET, errors=[dict(component=SECRET, code=SecretError(SECRET),
                                                        message=SECRET, exception=SecretError(SECRET))])
        raw["observed"]["location"].update(stderr=SECRET, source_map={SECRET: SECRET}, token=SECRET)
        raw["observed"]["intake"].update(token=SECRET, credential={SECRET: SECRET}, limits={SECRET: SECRET})
        raw["observed"]["intake"]["used"][SECRET] = SECRET
        raw["observed"]["read"] = {SECRET: SECRET}
        result = self.project(raw)
        self.assertNotIn(SECRET.encode("ascii"), F.compact(result))
        self.assertEqual(SecretError.rendered, 0)
        self.assertEqual(result["service"]["status"], "UNRECOGNIZED_REDACTED")
        self.assertEqual(result["service"]["failure_code"], "UNRECOGNIZED_REDACTED")
        self.assertEqual(result["cleanup"]["errors"],
                         [dict(component="UNRECOGNIZED_REDACTED", code="UNRECOGNIZED_REDACTED")])
        class StringSubclass(str):
            pass
        for value in (StringSubclass("FAILED"), "x" * 65):
            raw["status"] = value
            self.assertEqual(self.project(raw)["service"]["status"], "UNRECOGNIZED_REDACTED")

    def test_05_missing_throwing_and_projection_failure_fallback(self):
        self.assertEqual(H["_service_close_observation"](None), minimal("NO_OWNED_SERVICE"))
        SecretError.rendered = 0
        for error in (RuntimeError(SECRET), SecretError(SECRET), KeyboardInterrupt(SECRET)):
            callback = SyntheticReportOnly(error=error)
            self.assertEqual(H["_service_close_observation"](callback), minimal("OBSERVATION_UNAVAILABLE"))
            self.assertEqual(callback.calls, 1)
        callback = SyntheticReportOnly(failed_snapshot())
        original_compact = F.compact
        # Fault injection in the real serializer; restored before output/pin checks.
        with patch.object(F, "compact", side_effect=SecretError(SECRET)):
            result = H["_service_close_observation"](callback)
        self.assertIs(F.compact, original_compact)
        self.assertEqual(result, minimal("OBSERVATION_UNAVAILABLE"))
        self.assertEqual(callback.calls, 1)
        self.assertNotIn(SECRET.encode("ascii"), F.compact(result))
        self.assertEqual(SecretError.rendered, 0)


SELECTED = ("test_01_failed_snapshot_exact_whitelist", "test_02_partial_missing_and_unrecognized",
            "test_03_exact_scalars_bounds_and_32_rows", "test_04_synthetic_secret_redaction",
            "test_05_missing_throwing_and_projection_failure_fallback")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = ordinary(Path(args.output))
    need(output == OUTPUT and output.is_dir(), "CONTROL_SELECTED_OUTPUT")
    sources = output / "sources"
    need(Path(__file__).resolve() == sources / RELATIVE, "CONTROL_SNAPSHOT_EXECUTION_REQUIRED")
    result_path = output / "observed-controls-result.json"
    need(not result_path.exists(), "CONTROL_FRESH_RESULT_REQUIRED")
    adopt(sources)
    suite = unittest.TestSuite(Controls(name) for name in SELECTED)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    pin(sources / OWNER_RELATIVE, OWNER_BYTES, OWNER_SHA)
    pin(sources / FEATURE_RELATIVE, FEATURE_BYTES, FEATURE_SHA)
    summary = dict(schema="DMKN_V5_MANAGED_OBSERVATION_CONTROLS_V1",
        status="PASS" if result.wasSuccessful() else "FAIL", tests_run=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(SELECTED), owner_sha256=OWNER_SHA, formal_features_sha256=FEATURE_SHA,
        extracted=list(EXTRACTED), extraction_only=True, full_owner_imported=False,
        actual_service_used=False, synthetic_secret_inputs=True,
        closure_authority=False, mathematical_acceptance=False)
    raw = F.compact(summary)
    need(len(raw) <= 8192, "CONTROL_RESULT_BOUND")
    with result_path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_RESULT_WRITE")
    print(raw.decode("utf-8"))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
