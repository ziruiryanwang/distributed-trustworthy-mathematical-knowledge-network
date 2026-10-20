"""Focused persisted/live withdrawal controls; inert owner authority only.

Real trust records and guard methods are exercised. Issuer/runtime fixture shells
do not adopt executables, verify receipts or mint mathematical authority. No old
suite is imported; no subprocess, network, native check or proof may run.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / "portable_runtime"), str(SOURCE)]


def overlay(name, relative):
    parent = importlib.import_module(name.rsplit(".", 1)[0])
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(parent, name.rsplit(".", 1)[1], module)
    return module


overlay("admission.pin_phase", "runtime_efficient/admission/pin_phase.py")
T = overlay("admission.trust", "trust_withdrawal/admission/trust.py")
I = overlay("admission.verifier", "trust_withdrawal/admission/verifier.py")
A = overlay("aggregate_claims.aggregate_admission", "trust_withdrawal/aggregate_claims/aggregate_admission.py")
overlay("mixed_claims.receiver", "runtime_efficient/mixed_claims/receiver.py")
overlay("mixed_claims.imports_atomic", "interface_views/imports_atomic.py")
overlay("mixed_claims.interface_projection", "interface_views/projection.py")
overlay("mixed_claims.authoring_atomic", "interface_views/authoring_atomic.py")
overlay("transport.semantic_staging", "interface_views/semantic_staging.py")
overlay("client.workspace_evidence", "interface_views/workspace_evidence.py")
overlay("client.workspace_staged", "interface_views/workspace_staged.py")
overlay("client.semantic_reader", "interface_views/semantic_reader.py")
R = overlay("client.runtime", "trust_withdrawal/client/runtime.py")
from aggregate_claims import bindings as B
from modules import codec as C

OUTPUT = None
OBSERVED = {}


def support():
    # Syntactically valid policy record, explicitly NOT an adopted math runtime.
    return {"schema": "DMKN_LOCAL_TRUST_SUPPORT_V1", "identities": {
        "relation_image": B.RELATION_IMAGE, "aggregate_image": None,
        "foundation": B.FOUNDATION, "policy": B.POLICY,
        "receipt_scheme": "resolved-succinct-poseidon2"}, "roles": {
            "inert/control.py": {"bytes": 1, "sha256": hashlib.sha256(b"x").hexdigest()}}}


class WithdrawalControls(unittest.TestCase):
    def setUp(self):
        self.serial = 0

    def fresh(self, label="domain"):
        self.serial += 1
        return OUTPUT / (self._testMethodName + "-" + str(self.serial) + "-" + label)

    def domain(self):
        path = self.fresh()
        identifier = hashlib.sha256(str(path).encode()).hexdigest()
        domain = T.TrustDomain.create(path, identifier, support())
        return domain, path, identifier

    def issuer(self, domain, *, aggregate=False):
        # No constructor, adopted executable or successful receipt. Only actual
        # liveness methods are tested; registry values are opaque sentinels.
        cls = A.AggregateReceiptVerifier if aggregate else I.ReceiptVerifier
        owner = cls.__new__(cls)
        binding = domain.bind()
        owner._trust_binding = owner._trust_original_binding = binding
        owner._trust_domain, owner._trust_module = domain, T
        owner._trust_origin = Path(T.__file__).resolve()
        owner._trust_identity = T.check_binding(binding)
        owner._closed, owner._busy = False, False
        owner._handles = {object(): object()}
        owner._deadline = time.monotonic() + 30
        owner._used, owner._caps = [0, 0, 0], (2, 1024, 5)
        if aggregate:
            owner._members, owner._member_cache = {object(): object()}, {object(): object()}
            owner._aggregate_initialized = False
            owner._controller_started, owner._controller_cpu_cap = time.process_time(), 30
        return owner

    def runtime(self, domain):
        runtime = R.RuntimeProfile.__new__(R.RuntimeProfile)
        runtime._trust_domain, runtime._trust_binding = domain, domain.bind()
        runtime._trust_original = (runtime._trust_domain, runtime._trust_binding)
        runtime._trust_identity, runtime._support = domain.identity(), support()
        runtime._sources = {"admission/trust.py": {"path": str(Path(T.__file__).resolve())}}
        runtime._manifest = {"path": "inert", "sha256": "11"*32}
        runtime._preparation = {}
        runtime._receipt_runtime = runtime._aggregate_runtime = runtime._native_runtime = {}
        runtime._adoption = {"receipt": {"path": "inert-I"}, "native": {"path": "inert-N"},
            "aggregate": {"executable": {"path": "inert-A"}, "image": "44"*32}}
        runtime._context = SimpleNamespace(deadline=time.monotonic()+30,
                                           remaining_seconds=lambda: 25)
        runtime._selection = C.canonical(runtime.describe())
        return runtime

    def test_exact_binding_and_existing_domain_reopen(self):
        domain, path, identifier = self.domain()
        binding = domain.bind()
        original = domain.identity()
        self.assertEqual(T.check_binding(binding), original)
        reopened = T.TrustDomain.open(path, identifier, T.support_id(support()))
        self.assertEqual(reopened.identity(), original)
        self.assertEqual(T.check_binding(reopened.bind()), original)
        reordered = deepcopy(support())
        reordered = dict(reversed(list(reordered.items())))
        self.assertEqual(T.support_id(reordered), T.support_id(support()))
        with self.assertRaises(FileExistsError):
            T.TrustDomain.create(path, identifier, support())
        OBSERVED["ordinary_reopen_same_adoption"] = True

    def test_missing_mismatched_or_foreign_binding_refuses(self):
        domain, path, identifier = self.domain()
        with self.assertRaises(FileNotFoundError):
            T.TrustDomain.open(self.fresh("missing"), identifier, T.support_id(support()))
        with self.assertRaisesRegex(C.StructureError, "TRUST_ADOPTION_MISMATCH"):
            T.TrustDomain.open(path, "22"*32, T.support_id(support()))
        with self.assertRaisesRegex(C.StructureError, "TRUST_ADOPTION_MISMATCH"):
            T.TrustDomain.open(path, identifier, "33"*32)
        with self.assertRaisesRegex(C.StructureError, "TRUST_EXACT_REGISTERED_BINDING"):
            T.check_binding(None)
        with self.assertRaisesRegex(C.StructureError, "TRUST_EXACT_REGISTERED_BINDING"):
            T.check_binding(T.TrustBinding.__new__(T.TrustBinding))
        unregistered = T.TrustBinding.__new__(T.TrustBinding)
        unregistered._domain = domain
        with self.assertRaisesRegex(C.StructureError, "TRUST_UNREGISTERED_BINDING"):
            T.check_binding(unregistered)
        other, unused_path, unused_id = self.domain()
        with self.assertRaisesRegex(C.StructureError, "TRUST_UNREGISTERED_BINDING"):
            other.check(domain.bind())

    def test_withdrawal_persists_and_never_reinstates_observed_domain(self):
        domain, path, identifier = self.domain()
        binding = domain.bind()
        domain.withdraw("local checking stack withdrawn by fixture owner")
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding)
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            T.TrustDomain.open(path, identifier, T.support_id(support()))
        self.assertTrue((path/"WITHDRAWN").is_file())
        # Controlled test-fixture tampering only, never a supported reset action.
        (path/"WITHDRAWN").unlink()
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding)
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            domain.bind()
        self.assertFalse(hasattr(T.TrustDomain, "clear"))
        self.assertFalse(hasattr(T.TrustDomain, "reinstate"))
        OBSERVED["sticky_after_fixture_marker_removal"] = True

    def test_partial_marker_and_failed_sync_deny(self):
        domain, path, identifier = self.domain()
        binding = domain.bind()
        with (path/"WITHDRAWN").open("xb") as stream:
            stream.write(b"")
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            T.check_binding(binding)
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            T.TrustDomain.open(path, identifier, T.support_id(support()))
        domain2, path2, identifier2 = self.domain()
        binding2 = domain2.bind()
        with patch.object(T.os, "fsync", side_effect=OSError("INERT_SYNC_FAILURE")):
            with self.assertRaisesRegex(OSError, "INERT_SYNC_FAILURE"):
                domain2.withdraw("sync failure must not acknowledge success")
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding2)
        with self.assertRaisesRegex(C.StructureError, "TRUST_WITHDRAWN"):
            T.TrustDomain.open(path2, identifier2, T.support_id(support()))
        OBSERVED["failed_sync_denies"] = True

    def test_missing_and_malformed_adoption_refuse_and_latch(self):
        domain, path, identifier = self.domain()
        binding = domain.bind()
        record = path/"ADOPTION.json"
        raw = record.read_bytes()
        # Tampering only with this test's freshly provisioned inert record.
        record.unlink()
        with self.assertRaises(FileNotFoundError):
            T.check_binding(binding)
        with record.open("xb") as stream:
            stream.write(raw)
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding)
        malformed = self.fresh("partial")
        malformed.mkdir()
        with (malformed/"ADOPTION.json").open("xb") as stream:
            stream.write(b'{"schema":')
        with self.assertRaisesRegex(C.StructureError, "JSON_DECODE"):
            T.TrustDomain.open(malformed, identifier, T.support_id(support()))
        with self.assertRaises(FileExistsError):
            T.TrustDomain.create(malformed, identifier, support())

    def test_failed_marker_create_latches_without_false_persistence(self):
        domain, path, identifier = self.domain()
        binding = domain.bind()
        original_open = Path.open

        def fail_marker(file, *args, **kwargs):
            if file == path/"WITHDRAWN":
                raise PermissionError("INERT_MARKER_CREATE_FAILURE")
            return original_open(file, *args, **kwargs)

        with patch.object(Path, "open", fail_marker):
            with self.assertRaisesRegex(PermissionError, "INERT_MARKER_CREATE_FAILURE"):
                domain.withdraw("cannot acknowledge a marker that was not written")
        self.assertFalse((path/"WITHDRAWN").exists())
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            T.check_binding(binding)
        # The failure above never acknowledged persistence. This is not hardware
        # antirollback; fresh open cannot infer an unwritten owner action.
        self.assertEqual(T.TrustDomain.open(path, identifier, T.support_id(support())).identity(),
                         domain._identity)
        OBSERVED["failed_create_not_reported_persistent"] = True

    def test_issuer_live_and_aggregate_cache_revocation(self):
        domain, unused_path, unused_id = self.domain()
        individual = self.issuer(domain)
        aggregate = self.issuer(domain, aggregate=True)
        individual._active()
        aggregate._active()
        individual._busy = aggregate._busy = True
        domain.withdraw("must revoke without public close while busy")
        for owner in (individual, aggregate):
            with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
                owner._active()
            self.assertTrue(owner._closed)
            self.assertEqual(owner._handles, {})
            self.assertTrue(owner._busy)
        self.assertEqual(aggregate._members, {})
        self.assertEqual(aggregate._member_cache, {})
        OBSERVED["busy_safe_I_A_registry_revocation"] = True

    def test_individual_postworker_denial_precedes_binding_and_minting(self):
        domain, unused_path, unused_id = self.domain()
        owner = self.issuer(domain)
        owner._image, owner._foundation, owner._policy = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
        owner._install, owner._pins, owner._executable = OUTPUT, {}, Path("inert-verifier")
        owner._profile_id, owner._job = "55"*32, object()
        owner._check_install = owner._active  # Bypass installation only, not trust.
        calls = []

        def save(path, value):
            with path.open("x", encoding="utf-8") as target:
                json.dump(value, target)

        def supervise(*args, **kwargs):
            calls.append("inert-operational-closure")
            domain.withdraw("applied during inert worker")
            return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
                "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
                "termination_requested": False,
                "final_job": {"active_processes": 0, "terminated_processes": 0}}

        owner._supervisor = SimpleNamespace(limits_checked=lambda value: dict(value),
            absolute=lambda value, **kwargs: Path(value), overlap=lambda a, b: False,
            save_new=save, supervise=supervise)
        summary = {"schema": C.SUMMARY_SCHEMA, "foundation": B.FOUNDATION,
                   "policy": B.POLICY, "group_count": 1, "group_root": "66"*32}
        receipt = b"INERT_NOT_A_CRYPTOGRAPHIC_RECEIPT"
        with patch.object(I, "bind_output", side_effect=AssertionError("MUST_NOT_BIND")) as bind:
            with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
                owner.receive(receipt, summary, self.fresh("worker"),
                              cpu_seconds=1, wall_seconds=5, memory_mib=64)
            bind.assert_not_called()
        self.assertEqual(calls, ["inert-operational-closure"])
        self.assertEqual(owner._used, [1, len(receipt), 1])
        self.assertEqual(owner._handles, {})
        self.assertFalse(owner._busy)
        self.assertTrue(owner._closed)
        OBSERVED["postworker_no_binding_no_mint_no_refund"] = True

    def test_runtime_original_binding_and_new_operation_denial(self):
        domain, unused_path, unused_id = self.domain()
        runtime = self.runtime(domain)
        runtime._check_trust()
        original = runtime._trust_binding
        runtime._trust_binding = domain.bind()
        with self.assertRaisesRegex(ValueError, "RUNTIME_ORIGINAL_TRUST_BINDING"):
            runtime._check_trust()
        runtime._trust_binding = original
        domain.withdraw("operation guard must run before workspace access")
        with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
            runtime.open_operation(object(), object(), mode="validated",
                foundation_bytes=b"x", foundation_sha256=hashlib.sha256(b"x").hexdigest())

    def test_runtime_forwards_same_binding_and_cleans_before_transfer(self):
        domain, unused_path, unused_id = self.domain()
        runtime = self.runtime(domain)
        events, owners = [], []

        class Workspace:
            _client, _poisoned = None, False
            config = {"wire_profile": {"aggregate_image": "44"*32}, "packet_envelope": {}}
            def _active(self): pass
            def _grant_active(self, grant): pass
            def operation(self, *args, **kwargs):
                raise AssertionError("TRANSFER_AFTER_WITHDRAWAL")

        class Owner:
            def __init__(self, label): self.label, self.closed = label, False
            def close(self): self.closed = True; events.append("close:"+self.label)

        def issuer(label):
            def construct(**kwargs):
                self.assertIs(kwargs["trust_binding"], runtime._trust_binding)
                value = Owner(label)
                owners.append(value)
                events.append("construct:"+label)
                return value
            return construct

        def delta(**kwargs):
            value = Owner("delta")
            owners.append(value)
            events.append("construct:delta")
            domain.withdraw("after constructors, before ownership transfer")
            return value

        workspace = Workspace()
        grant = R.OperationGrant.__new__(R.OperationGrant)
        grant._workspace, grant._used = workspace, False
        grant._deadline, grant._directory = runtime._context.deadline-1, self.fresh("grant")
        grant._limits = {"acquisition": {"verify_attempts": 1, "verification_input_bytes": 1024,
            "worker_cpu_seconds": 1}, "worker_cpu_seconds": 2, "input_bytes": 1024,
            "imports": {"max_calls": 1, "max_members": 1}, "controller_cpu_seconds": 1,
            "output_bytes": 1024, "output_entries": 32}
        with patch.object(R, "_workspace_type", return_value=Workspace), \
             patch.object(R, "ReceiptVerifier", issuer("I")), \
             patch.object(R, "AggregateReceiptVerifier", issuer("A")), \
             patch.object(R, "MixedDeltaVerifier", delta):
            with self.assertRaisesRegex(C.StructureError, "TRUST_DENIAL_LATCHED"):
                runtime.open_operation(workspace, grant, mode="validated",
                    foundation_bytes=b"x", foundation_sha256=hashlib.sha256(b"x").hexdigest())
        self.assertEqual(events, ["construct:I", "construct:A", "construct:delta",
                                  "close:delta", "close:A", "close:I"])
        self.assertTrue(all(owner.closed for owner in owners))
        self.assertFalse(grant._used)
        self.assertFalse(workspace._poisoned)
        OBSERVED["same_binding_final_gate_cleanup_no_transfer"] = True

    def test_required_constructor_bindings_have_no_default(self):
        for cls in (I.ReceiptVerifier, A.AggregateReceiptVerifier):
            parameter = inspect.signature(cls).parameters["trust_binding"]
            self.assertIs(parameter.default, inspect.Parameter.empty)
        parameter = inspect.signature(R.RuntimeProfile.from_context).parameters["trust_domain"]
        self.assertIs(parameter.default, inspect.Parameter.empty)


SELECTED = (
    "test_exact_binding_and_existing_domain_reopen",
    "test_missing_mismatched_or_foreign_binding_refuses",
    "test_withdrawal_persists_and_never_reinstates_observed_domain",
    "test_partial_marker_and_failed_sync_deny",
    "test_required_constructor_bindings_have_no_default",
    "test_missing_and_malformed_adoption_refuse_and_latch",
    "test_failed_marker_create_latches_without_false_persistence",
    "test_issuer_live_and_aggregate_cache_revocation",
    "test_individual_postworker_denial_precedes_binding_and_minting",
    "test_runtime_original_binding_and_new_operation_denial",
    "test_runtime_forwards_same_binding_and_cleans_before_transfer",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output:
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output / "trust-fixtures"
    OUTPUT.mkdir()
    suite = unittest.TestSuite(WithdrawalControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "scope": "PERSISTENT_GUARDS_WITH_INERT_ISSUER_RUNTIME_SHELLS",
        "selected": list(SELECTED), "observed": OBSERVED, "native_calls": 0, "proof_calls": 0,
        "mathematical_acceptance": False}
    with (output / "controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
