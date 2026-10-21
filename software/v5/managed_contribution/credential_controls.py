"""Four network-free private-credential boundary groups; not actual issuance.

Synthetic tokens/files are parser inputs, never issued grants or secret custody.
No fabricated PlacementService is accepted and no publish-after-issue fault is
claimed. Root separately selects any execution; all fixture files are retained.
"""
import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import shutil
import socket
import subprocess
import sys
import time
import traceback
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALLATION = PROJECT / "product-local/v5-distribution-managed-owner-01/Mathematical Commons v5"
RELEASE_SHA = "8fcf2c971029c8ad0787ec8da0891be178a95b80999f8bccc262e077009701a2"
SOURCE = Path(__file__).resolve().parent
HELPER_BYTES = 12374
HELPER_SHA = "7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0"
MIB = 1024**2
# Publicly specified deterministic parser fixture, never an authentic grant.
SYNTHETIC_TOKEN = "a7" * 32
C = N = OUTPUT = None
SOURCES = {}
OBSERVED = {}
FORBIDDEN = []


def need(value, code):
    if not value:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def ordinary(path, directory=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve() == path and all(
        not p.is_symlink() and not p.is_junction() for p in (path, *path.parents)), "CONTROL_ORDINARY")
    need(path.is_dir() if directory else path.is_file(), "CONTROL_PATH_KIND")
    return path


def pin(path, size, digest):
    path = ordinary(path)
    need(0 < size <= 8*MIB and path.stat().st_size == size, "CONTROL_PIN_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(8*MIB+1)
    need(len(raw) == size and sha(raw) == digest, "CONTROL_PIN")
    return raw


def forbidden(*unused, **ignored):
    FORBIDDEN.append("FORBIDDEN_NETWORK_PROCESS_ISSUANCE_OR_DELETE")
    raise AssertionError(FORBIDDEN[-1])


def adopt(release_sha):
    """Same installed-map plus explicit snapshotted-overlay pattern as prior controls."""
    global C, N
    need(release_sha == RELEASE_SHA, "CONTROL_ADOPTED_126_RELEASE")
    path = ordinary(INSTALLATION / "V5-RELEASE.json")
    release = json.loads(pin(path, path.stat().st_size, release_sha))
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3" and
         len(release["sdk_sources"]) == 126, "CONTROL_EXACT_INSTALLED_RELEASE")
    need(Path(sys.executable).resolve() == INSTALLATION / "base/receiver/runtime/python/python.exe",
         "CONTROL_INSTALLED_PYTHON")
    for logical, relative in release["sdk_sources"].items():
        parts = PurePosixPath(logical).parts
        need(len(parts) >= 2 and parts[0] in ("v5", "portable") and relative == "sdk/" + logical
             and ".." not in parts and "\\" not in logical, "CONTROL_SOURCE_PATH")
        row = release["files"][relative]
        target = INSTALLATION / relative
        pin(target, row["bytes"], row["sha256"])
        SOURCES[logical] = dict(path=str(target), bytes=row["bytes"], sha256=row["sha256"])
    prefixes = {PurePosixPath(name).parts[1] for name in SOURCES}
    need(not any(name.split(".")[0] in prefixes for name in sys.modules), "CONTROL_EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(INSTALLATION / "sdk/v5"), str(INSTALLATION / "sdk/portable")]
    name = "client.private_credentials"
    target = SOURCE / "client/private_credentials.py"
    pin(target, HELPER_BYTES, HELPER_SHA)
    parent = __import__("client")
    spec = importlib.util.spec_from_file_location(name, target)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(parent, "private_credentials", module)
    SOURCES["v5/client/private_credentials.py"] = dict(path=str(target), bytes=HELPER_BYTES, sha256=HELPER_SHA)
    C, N = module, sys.modules["placement.network"]


def rebind(release_sha):
    path = INSTALLATION / "V5-RELEASE.json"
    pin(path, path.stat().st_size, release_sha)
    selected = {Path(row["path"]) for row in SOURCES.values()}
    prefixes = {PurePosixPath(name).parts[1] for name in SOURCES}
    origins = {}
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in prefixes:
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            paths = getattr(module, "__path__", ())
            need(paths and all(Path(p).is_relative_to(INSTALLATION / "sdk") for p in paths), "CONTROL_NAMESPACE")
        else:
            path = ordinary(origin)
            need(path in selected, "CONTROL_PRODUCT_ORIGIN")
            origins[name] = str(path)
    for row in SOURCES.values():
        pin(row["path"], row["bytes"], row["sha256"])
    need(len(SOURCES) == 127, "CONTROL_126_PLUS_HELPER")
    return origins


def endpoint(port):
    return dict(host="127.0.0.1", port=port, tls=False, server_name=None)


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT / ("c%02d" % (SELECTED.index(self._testMethodName)+1))
        self.root.mkdir()
        self.private = self.root / "synthetic-credential-fixtures"
        self.private.mkdir()
        self.public = self.root / "public"
        self.public.mkdir()
        (self.public / "control").mkdir()
        self.clients = []
        self.events = {"synthetic_nonissued_credentials": True}
        self.serial = 0
        self.metadata = dict(schema=C.METADATA_SCHEMA, scope=C.SCOPE,
            grant_id=sha(SYNTHETIC_TOKEN.encode("ascii")),
            bindings=dict(service_epoch="11"*32, generation="12"*32,
                          namespace="13"*32, wire_profile_id="14"*32),
            read_endpoint=endpoint(45101), intake_endpoint=endpoint(45102), source=endpoint(45103),
            write_until_ms=2000000000000, retention_until_ms=2000000001000,
            limits={key: 1 for key in C.P.RESOURCES}, release_sha256=RELEASE_SHA,
            profile_sha256="21"*32,
            operation=dict(name="control", run=str(self.public / "control"),
                           workspace_root=str(self.public), plan_sha256="22"*32),
            session=dict(number=1, nonce="23"*32, worker=dict(pid=1, created=1)),
            issuing_runtime="24"*32, service_until_ns=time.monotonic_ns()+120*10**9)
        self.egress = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                           test_endpoints=[dict(host="127.0.0.1", port=p) for p in (45101, 45102, 45103)])

    def tearDown(self):
        for client in self.clients:
            self.assertFalse(client._busy)
            client.close()
            self.assertTrue(client.closed)
        OBSERVED[self._testMethodName] = self.events

    def specification(self, path):
        return dict(source=deepcopy(self.metadata["source"]), write_until_ms=2000000000000,
            retention_until_ms=2000000001000, limits=deepcopy(self.metadata["limits"]),
            credential_path=str(path), confidentiality=C.CONFIDENTIALITY)

    def envelope(self):
        return dict(schema=C.SCHEMA, token=SYNTHETIC_TOKEN, metadata=deepcopy(self.metadata))

    def fixture(self, raw):
        self.serial += 1
        path = self.private / ("fixture-%02d.json" % self.serial)
        with path.open("xb") as stream:
            self.assertEqual(stream.write(raw), len(raw))
        return dict(path=str(path), bytes=len(raw), sha256=sha(raw))

    def reader(self, selected, expected=None, **changes):
        options = dict(egress=deepcopy(self.egress), contact=deepcopy(self.metadata["intake_endpoint"]),
            deadline=time.monotonic()+30, requests=2, incoming_bytes=2*N.OUT_RESERVE,
            outgoing_bytes=2*N.IN_RESERVE, operation_ms=1000)
        options.update(changes)
        client, metadata = C.read_client(selected, deepcopy(self.metadata if expected is None else expected), **options)
        self.clients.append(client)
        return client, metadata

    def refused(self, code, stage, call):
        try:
            call()
        except C.CredentialError as error:
            self.assertEqual(str(error), code)
            self.assertEqual(error.code, code)
            self.assertEqual(error.stage, stage)
            self.assertTrue(error.__suppress_context__)
            observation = error.observation()
            self.assertFalse(observation["charge_refunded"])
            self.assertFalse(observation["mathematical_acceptance"])
            self.assertNotIn(SYNTHETIC_TOKEN, encode(observation).decode())
            self.assertNotIn(SYNTHETIC_TOKEN, "".join(traceback.format_exception(error)))
            return observation
        self.fail("CONTROL_EXPECTED_FIXED_CREDENTIAL_REFUSAL")

    def test_preflight_disjoint_fresh_nonmutating(self):
        fresh = self.private / "fresh.json"
        spec = self.specification(fresh)
        before = deepcopy(spec)
        self.assertIsNone(C.preflight(spec, [str(self.public), str(INSTALLATION)]))
        self.assertEqual(spec, before)
        self.assertFalse(fresh.exists())
        cases = [
            (self.specification(self.public / "inside.json"), [str(self.public)]),
            (self.specification(self.root / "ancestor"), [str(self.root / "ancestor/descendant")]),
            (spec, [str(fresh)]),
            (self.specification(Path("relative.json")), [str(self.public)]),
            (spec, []),
            ({**spec, "confidentiality": "UNADOPTED"}, [str(self.public)]),
        ]
        for selected, protected in cases:
            self.refused("PRIVATE_CREDENTIAL_PREFLIGHT_REFUSED", "PREFLIGHT",
                         lambda selected=selected, protected=protected: C.preflight(selected, protected))
        existing = self.private / "existing.json"
        with existing.open("xb") as stream:
            stream.write(b"CONTROL_EXISTING_SENTINEL")
        self.refused("PRIVATE_CREDENTIAL_PREFLIGHT_REFUSED", "PREFLIGHT",
                     lambda: C.preflight(self.specification(existing), [str(self.public)]))
        self.assertTrue(existing.read_bytes() == b"CONTROL_EXISTING_SENTINEL")
        self.assertFalse(fresh.exists())
        self.events.update(refusals=7, positive_preflight_created_nothing=True,
                           overlap_both_directions=True, existing_bytes_preserved=True)

    def test_reader_pin_canonical_metadata_and_token_identifier(self):
        baseline = encode(self.envelope())
        selected = self.fixture(baseline)
        cases = [({**selected, "sha256": "00"*32}, self.metadata),
                 ({**selected, "bytes": selected["bytes"]-1}, self.metadata)]
        variants = [baseline+b"\n", b'{"token":"'+SYNTHETIC_TOKEN.encode()+b'",'+baseline[1:],
                    baseline[:41], b"x"*(C.MAX_BYTES+1)]
        altered = self.envelope(); altered["token"] = "a8"*32
        variants.append(encode(altered))
        altered = self.envelope(); altered["metadata"]["scope"] = "CROSS_HOST_UNADOPTED"
        variants.append(encode(altered))
        altered = self.envelope(); altered["metadata"]["unexpected"] = SYNTHETIC_TOKEN
        variants.append(encode(altered))
        for value in variants:
            row = self.fixture(value)
            if len(value) > C.MAX_BYTES:
                row["bytes"] = C.MAX_BYTES  # Reach the actual file-size guard, not only pin syntax.
            cases.append((row, self.metadata))
        for field in ("profile_sha256", "release_sha256", "issuing_runtime"):
            expected = deepcopy(self.metadata); expected[field] = "31"*32
            cases.append((selected, expected))
        expected = deepcopy(self.metadata); expected["session"]["nonce"] = "32"*32
        cases.append((selected, expected))
        expected = deepcopy(self.metadata); expected["operation"]["plan_sha256"] = "33"*32
        cases.append((selected, expected))
        expected = deepcopy(self.metadata); expected["bindings"]["generation"] = "34"*32
        cases.append((selected, expected))
        for row, expected in cases:
            before = Path(row["path"]).read_bytes()
            self.refused("PRIVATE_CREDENTIAL_READER_REFUSED", "READ",
                         lambda row=row, expected=expected: self.reader(row, expected))
            self.assertTrue(Path(row["path"]).read_bytes() == before)
        self.assertFalse(self.clients)
        self.events.update(refusals=len(cases), malformed_and_partial_files_preserved=True,
                           canonical_pin_metadata_token_identifier_checked=True)

    def test_reader_independent_authority_and_original_cutoff(self):
        self.metadata["service_until_ns"] = time.monotonic_ns()+60*10**9
        selected = self.fixture(encode(self.envelope()))
        earlier = time.monotonic()+20
        client, returned = self.reader(selected, deadline=earlier)
        self.assertIs(type(client), N.PlacementClient)
        self.assertEqual(returned, self.metadata)
        self.assertIsNot(returned, self.metadata)
        self.assertEqual(client._deadline, earlier)
        self.assertEqual(client._caps, (2, 2*N.OUT_RESERVE, 2*N.IN_RESERVE, 1000))
        self.assertNotIn(SYNTHETIC_TOKEN, encode(client.report()).decode())
        later, unused = self.reader(selected, deadline=time.monotonic()+90, requests=1,
                                    incoming_bytes=N.OUT_RESERVE, outgoing_bytes=N.IN_RESERVE, operation_ms=500)
        cutoff = math.nextafter(self.metadata["service_until_ns"]/10**9, -math.inf)
        self.assertEqual(later._deadline, cutoff)
        self.assertEqual(later._caps, (1, N.OUT_RESERVE, N.IN_RESERVE, 500))
        denied = deepcopy(self.egress)
        denied["test_endpoints"] = [dict(host="127.0.0.1", port=45103)]
        cases = [dict(contact=endpoint(45103)), dict(egress=denied), dict(requests=0),
                 dict(incoming_bytes=N.OUT_RESERVE-1), dict(outgoing_bytes=N.IN_RESERVE-1),
                 dict(operation_ms=0), dict(deadline=1), dict(deadline=float("inf"))]
        for changes in cases:
            self.refused("PRIVATE_CREDENTIAL_READER_REFUSED", "READ",
                         lambda changes=changes: self.reader(selected, **changes))
        expired = deepcopy(self.metadata); expired["service_until_ns"] = 1
        self.refused("PRIVATE_CREDENTIAL_READER_REFUSED", "READ", lambda: self.reader(selected, expired))
        # Simulated clock advance AFTER genuine client construction. No sleep,
        # renewed deadline, network or fabricated PlacementClient is involved.
        made = []
        original_client = C.PlacementClient
        def observing_client(*args, **kwargs):
            actual = original_client(*args, **kwargs)
            made.append(actual)
            return actual
        ticks = iter([self.metadata["service_until_ns"]-1,
                      self.metadata["service_until_ns"]-1, self.metadata["service_until_ns"]])
        simulated_time = SimpleNamespace(monotonic=time.monotonic, monotonic_ns=lambda: next(ticks))
        with patch.object(C, "time", simulated_time), patch.object(C, "PlacementClient", observing_client):
            self.refused("PRIVATE_CREDENTIAL_READER_REFUSED", "READ", lambda: self.reader(selected))
        self.assertEqual(len(made), 1)
        self.assertIs(type(made[0]), N.PlacementClient)
        self.assertTrue(made[0].closed)
        self.assertFalse(made[0]._busy)
        self.events.update(refusals=10, genuine_clients_created=3, no_client_request_sent=True,
            original_cutoff_and_caller_caps_preserved=True, simulated_postconstruct_expiry_closed_client=True)

    def test_fixed_error_diagnostics_and_preissuance_publish_refusal(self):
        malformed = C.CredentialError(SYNTHETIC_TOKEN, SYNTHETIC_TOKEN, SYNTHETIC_TOKEN)
        self.assertEqual(str(malformed), "PRIVATE_CREDENTIAL_HANDOFF_FAILED")
        self.assertEqual(malformed.stage, "PREFLIGHT")
        self.assertIsNone(malformed.grant_id)
        self.assertNotIn(SYNTHETIC_TOKEN, encode(malformed.observation()).decode())
        selected = self.fixture(encode(self.envelope()))
        # Explicit synthetic secret-bearing I/O exception: production facade
        # must hide its text/context from ordinary formatted diagnostics.
        with patch.object(C, "_file", side_effect=OSError(SYNTHETIC_TOKEN)):
            observed = self.refused("PRIVATE_CREDENTIAL_READER_REFUSED", "READ", lambda: self.reader(selected))
        self.assertIsNone(observed["grant_id"])
        fresh = self.private / "publish-refused.json"
        observation = self.refused("PRIVATE_CREDENTIAL_HANDOFF_FAILED", "PREFLIGHT", lambda: C.publish(
            object(), self.specification(fresh), release_sha256=RELEASE_SHA, profile_sha256="21"*32,
            operation=self.metadata["operation"], session=self.metadata["session"],
            service_until_ns=self.metadata["service_until_ns"], protected=[str(self.public)]))
        self.assertIsNone(observation["grant_id"])
        self.assertFalse(fresh.exists())
        self.events.update(refusals=2, arbitrary_service_refused_before_issuance=True,
            fixed_diagnostics_hide_simulated_io_payload=True, credential_error_invalid_fields_sanitized=True,
            issuance_attempts=0, authentic_grant_charge_tested=False, partial_issued_output_tested=False)


SELECTED = (
    "test_preflight_disjoint_fresh_nonmutating",
    "test_reader_pin_canonical_metadata_and_token_identifier",
    "test_reader_independent_authority_and_original_cutoff",
    "test_fixed_error_diagnostics_and_preissuance_publish_refusal",
)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--release-sha", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_ISOLATED_CANONICAL_OWNER")
    OUTPUT = ordinary(args.output, directory=True)
    need(OUTPUT.parent == PROJECT / "experiments/v5-local-checks" and
         SOURCE == OUTPUT / "sources/software/v5/managed_contribution", "CONTROL_SELECTED_SNAPSHOT")
    with ExitStack() as guards:
        for owner, name in ((subprocess, "Popen"), (os, "system"), (socket, "socket"),
                            (asyncio, "open_connection"), (asyncio, "start_server"),
                            (os, "remove"), (os, "unlink"), (os, "rmdir"), (shutil, "rmtree")):
            guards.enter_context(patch.object(owner, name, forbidden))
        adopt(args.release_sha)
        for name in ("start", "issue_token"):
            guards.enter_context(patch.object(C.PlacementService, name, forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
        origins = rebind(args.release_sha)
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_PRIVATE_CREDENTIAL_BOUNDARY_CONTROLS_V1", status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), observations=OBSERVED, forbidden_calls=FORBIDDEN,
        sources=SOURCES, origins=origins, release_sha256=args.release_sha,
        synthetic_nonissued_fixture_files=True, simulated_faults=["secret-bearing-read-error", "postconstruct-clock-expiry"],
        actual_grant_issuance=False, authentic_grant_charge_tested=False, partial_issued_output_tested=False,
        actual_processes_started=0, actual_network_calls=0, actual_native_calls=0, actual_proof_calls=0,
        actual_verifier_calls=0, old_suites_imported=False, managed_deletions=0, old_data_deleted=False,
        windows_acl_confidentiality_proved=False, mathematical_acceptance=False)
    raw = encode(report)+b"\n"
    need(len(raw) <= MIB and SYNTHETIC_TOKEN.encode() not in raw, "CONTROL_NONSECRET_REPORT_BOUND")
    with (OUTPUT / "credential-controls-result.json").open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_SHORT_WRITE")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
