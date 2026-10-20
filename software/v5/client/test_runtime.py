"""Finite constructor-boundary controls; all mathematical owners are INERT.

Real pin validation, runtime rebasing, workspaces and grants are exercised.
Only owner constructors and final ownership-transfer calls are replaced by
explicit recording doubles. No receipt/native/proof/Lean operation is run.
"""
import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from aggregate_claims import bindings as B
from client import runtime as R
from client import workspace_atomic as W
from discovery import formal_features as F
from evidence_network.custody import public_profile as evidence_profile
from frontier_network.custody import public_profile as atomic_profile
from mixed_claims.packet import Envelope

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
IMAGE = "81"*32
FOUNDATION = b"SYNTHETIC-FOUNDATION-NO-MATHEMATICAL-USE"
OUTPUT = None
OBSERVED = {"inert_owner_constructions": 0, "inert_ownership_transfers": 0}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    return pin(path)


def configuration(*, evidence=False):
    value = {
        "schema": "DMKN_V5_CLIENT_WORKSPACE_V1",
        "wire_profile": atomic_profile(),
        "module_limits": dict(modules=8, groups=16, declarations=32, bodies=8,
                              logical_bytes=MIB, db_pages=256),
        "packet_limits": dict(packets=8, offers=16, offers_per_module=4,
                             packet_bytes=65536, logical_bytes=MIB, db_pages=256),
        "index_limits": dict(max_objects=8, max_postings=1024, max_features=128,
                            max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        "packet_envelope": asdict(Envelope()),
        "max_operations": 8, "max_report_bytes": MIB, "ledger_pages": 256,
    }
    if evidence:
        from client import workspace_evidence as E
        value.update(schema=E.SCHEMA, wire_profile=evidence_profile(IMAGE),
                     terminal_receipt_bytes=65536)
    return value


def limits(*, author_cpu=40):
    return dict(
        wall_seconds=60, controller_cpu_seconds=30, calls=128,
        input_bytes=4*MIB, worker_cpu_seconds=70+author_cpu,
        output_bytes=128*MIB, output_entries=512,
        acquisition=dict(requests=8, reply_bytes=MIB, verify_attempts=3,
                         verification_input_bytes=65536, worker_cpu_seconds=70),
        imports=dict(max_sources=8, max_members=16, max_receipts=8,
                     max_calls=4096, submitted_bytes=MIB, data_bytes=MIB),
    )


class InertOwner:
    def __init__(self, tag, args, kwargs, *, close_error=None):
        self.tag, self.args, self.kwargs = tag, args, kwargs
        self.close_error, self.closed = close_error, 0

    def close(self):
        self.closed += 1
        if self.close_error is not None:
            raise self.close_error


class RuntimeControls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.workspaces = []

    def tearDown(self):
        for workspace in reversed(self.workspaces):
            if not workspace._closed:
                workspace.close()

    def fixture(self, *, aggregate=False, receipt=True, suffix="profile"):
        """Tiny fake runtime bytes, pinned data only; never load or execute them."""
        root = self.root/suffix
        old, install, sources = root/"old-install", root/"new-install", SOURCE
        install.mkdir(parents=True)
        source_names = {
            "client/runtime.py",
            "production/__init__.py", "production/producer.py", "authoring/worker.py",
        }
        # These four files are actual runner-selected immutable snapshot bytes.
        # This small map tests the factory's own minimum closure, not the deeper
        # owner constructors whose installation checks are replaced below.
        selected = {}
        for name in sorted(source_names):
            row = pin(sources/name)
            selected["v5/"+name] = row["sha256"]
        runtime_names = ("receiver/runtime/python/python.exe",
                         "receiver/runtime/python/python314.dll",
                         "receiver/runtime/python/Lib/encodings/__init__.py")
        rows = [write(install/name, ("inert-runtime:"+name).encode()) for name in runtime_names]
        files = {name: {key: row[key] for key in ("bytes", "sha256")}
                 for name, row in zip(runtime_names, rows)}
        manifest = write(install/"RELEASE-MANIFEST.json", encoded({"files": files}))
        def old_row(row):
            return {**row, "path": str(old/Path(row["path"]).relative_to(install))}
        host = write(root/"producer-host.exe", b"inert-producer-host")
        image = write(root/"guest-image.bin", b"inert-image")
        frontend = write(root/"frontend.exe", b"inert-frontend")
        lean_runtime = write(root/"lean/bin/runtime.dll", b"inert-lean-runtime")
        producer = {
            "schema": "DMKN_V5_PRODUCER_PROFILE_V1",
            "image_id": B.RELATION_IMAGE, "foundation": B.FOUNDATION, "policy": B.POLICY,
            "supervisor_manifest": {**manifest, "path": str(old/"RELEASE-MANIFEST.json")},
            "host": host, "python": old_row(rows[0]), "python_dll": old_row(rows[1]),
            "runtime_pins": [old_row(rows[2])], "source_pins": [],
        }
        template = {
            "schema": "DMKN_V5_PREPARATION_PROFILE_V1", "producer": producer,
            "image": image, "worker": pin(sources/"authoring/worker.py"),
            "native_executable": frontend, "lean_root": str(root/"lean"),
            "lean_runtime_pins": [lean_runtime], "source_pins": [],
        }
        adoption = {
            "schema": "DMKN_V5_CLIENT_RUNTIME_V1",
            "preparation_profile": write(root/"preparation.json", encoded(template)),
            "native": write(root/"native.exe", b"inert-native"),
            "receipt": write(root/"receipt.exe", b"inert-receipt") if receipt else None,
            "aggregate": {"executable": write(root/"aggregate.exe", b"inert-aggregate"),
                          "image": IMAGE} if aggregate else None,
        }
        context = SimpleNamespace(
            installation=install, sources_v5=sources, source_sha256=selected,
            deadline=time.monotonic()+120, remaining_seconds=lambda: 100)
        return context, adoption, template, manifest, files

    def open_workspace(self, *, evidence=False, author_cpu=40):
        if evidence:
            from client import workspace_evidence as E
            cls = E.Workspace
        else:
            cls = W.Workspace
        workspace = cls.open(self.root/("workspace"+str(len(self.workspaces))),
                             configuration(evidence=evidence), create=True)
        self.workspaces.append(workspace)
        grant = workspace.reserve(limits(author_cpu=author_cpu))
        return workspace, grant

    def record_owners(self, *, fail=None, close_failure=None):
        made, calls = {}, []
        stack = ExitStack()
        self.addCleanup(stack.close)
        for symbol, tag in (
            ("ReceiptVerifier", "I"), ("AggregateReceiptVerifier", "A"),
            ("MixedDeltaVerifier", "delta"), ("MixedOwnerPreparation", "preparation"),
        ):
            def constructor(*args, _tag=tag, **kwargs):
                calls.append((_tag, args, kwargs))
                OBSERVED["inert_owner_constructions"] += 1
                if _tag == fail:
                    raise ValueError("INERT_CONSTRUCTION_"+_tag)
                owner = InertOwner(_tag, args, kwargs,
                    close_error=RuntimeError("INERT_CLEANUP_"+_tag)
                    if _tag == close_failure else None)
                made[_tag] = owner
                return owner
            stack.enter_context(patch.object(R, symbol, side_effect=constructor))
        return made, calls

    def transfer(self, workspace, *, error=None):
        observed, token = {}, object()
        def operation(grant, **owners):
            OBSERVED["inert_ownership_transfers"] += 1
            observed.update(grant=grant, **owners)
            if error is not None:
                raise error
            return token
        self.enterContext(patch.object(workspace, "operation", side_effect=operation))
        return observed, token

    def invoke(self, profile, workspace, grant, *, mode="atomic", authoring=False):
        return profile.open_operation(workspace, grant, mode=mode, authoring=authoring,
            foundation_bytes=FOUNDATION, foundation_sha256=sha(FOUNDATION))

    def test_relocation_uses_selected_pins_and_copies_configuration(self):
        context, adoption, template, manifest, files = self.fixture()
        before = deepcopy(adoption)
        profile = R.RuntimeProfile.from_context(context, adoption)
        view = profile.describe()
        self.assertEqual(adoption, before)
        rebased = view["preparation"]["producer"]
        self.assertEqual(rebased["supervisor_manifest"], manifest)
        for name in ("python", "python_dll"):
            self.assertTrue(Path(rebased[name]["path"]).is_relative_to(context.installation))
        self.assertEqual(rebased["host"], template["producer"]["host"])
        self.assertEqual(view["preparation"]["image"], template["image"])
        self.assertEqual(view["preparation"]["native_executable"], template["native_executable"])
        self.assertEqual(view["preparation"]["lean_root"], template["lean_root"])
        self.assertEqual(set(view["sources"]), {name[3:] for name in context.source_sha256})
        self.assertEqual(view["sources"]["client/runtime.py"]["sha256"],
                         context.source_sha256["v5/client/runtime.py"])
        self.assertIsNone(view["aggregate_runtime"])
        view["preparation"]["producer"]["image_id"] = "00"*32
        adoption["native"]["sha256"] = "00"*32
        self.assertEqual(profile.describe()["adoption"], before)
        self.assertEqual(profile.describe()["preparation"]["producer"]["image_id"], B.RELATION_IMAGE)

    def test_wrong_selected_source_and_manifest_pin_are_rejected(self):
        context, adoption, template, manifest, files = self.fixture()
        context.source_sha256["v5/client/runtime.py"] = "00"*32
        with self.assertRaises(ValueError):
            R.RuntimeProfile.from_context(context, adoption)
        context.source_sha256["v5/client/runtime.py"] = pin(context.sources_v5/"client/runtime.py")["sha256"]
        damaged = deepcopy(adoption)
        damaged["preparation_profile"]["sha256"] = "00"*32
        with self.assertRaises(ValueError):
            R.RuntimeProfile.from_context(context, damaged)
        template["producer"]["python"]["sha256"] = "00"*32
        damaged["preparation_profile"] = write(self.root/"mismatched-runtime.json", encoded(template))
        with self.assertRaises(ValueError):
            R.RuntimeProfile.from_context(context, damaged)

    def test_source_origin_and_minimum_source_closure_are_required(self):
        context, adoption, template, manifest, files = self.fixture()
        missing = context.source_sha256.pop("v5/client/runtime.py")
        with self.assertRaises(ValueError):
            R.RuntimeProfile.from_context(context, adoption)
        context.source_sha256["v5/client/runtime.py"] = missing
        with patch.object(R, "__file__", str(context.sources_v5/"different.py")):
            with self.assertRaises(ValueError):
                R.RuntimeProfile.from_context(context, adoption)
        context.source_sha256.pop("v5/authoring/worker.py")
        with self.assertRaises(ValueError):
            R.RuntimeProfile.from_context(context, adoption)

    def test_rebound_manifest_cannot_escape_profile_integrity_check(self):
        context, adoption, template, manifest, files = self.fixture()
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace()
        made, calls = self.record_owners()
        profile._manifest = {**profile._manifest, "sha256": "00"*32}
        with self.assertRaisesRegex(ValueError, "RUNTIME_PROFILE_CHANGED"):
            self.invoke(profile, workspace, grant)
        self.assertEqual(calls, [])

    def test_atomic_owner_pairing_and_disjoint_author_allowance(self):
        context, adoption, template, manifest, files = self.fixture()
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace()
        made, calls = self.record_owners()
        observed, token = self.transfer(workspace)
        actual = self.invoke(profile, workspace, grant, authoring=True)
        self.assertIs(actual, token)
        self.assertEqual([tag for tag, _, _ in calls], ["I", "delta", "preparation"])
        self.assertIs(made["delta"].kwargs["legacy_verifier"], made["I"])
        self.assertIsNone(made["delta"].kwargs["aggregate_verifier"])
        self.assertIs(observed["receipt_owner"], made["I"])
        self.assertIs(observed["delta_owner"], made["delta"])
        self.assertIs(observed["preparation_owner"], made["preparation"])
        self.assertEqual(observed["foundation_bytes"], FOUNDATION)
        self.assertEqual(observed["foundation_sha256"], sha(FOUNDATION))
        self.assertEqual(grant.limits["acquisition"]["verify_attempts"], 3)
        self.assertEqual(workspace.config["packet_envelope"]["claims"], 8)
        self.assertEqual(made["I"].kwargs["operations"], 24)
        self.assertEqual(made["delta"].kwargs["operations"], 3)
        self.assertEqual(made["I"].kwargs["reserved_cpu_seconds"], 70)
        self.assertEqual(made["I"].kwargs["submitted_bytes"], 65536)
        self.assertEqual(made["delta"].kwargs["reserved_cpu_seconds"], 70)
        self.assertEqual(made["delta"].kwargs["submitted_bytes"], 65536)
        allowance = made["preparation"].args[1]
        self.assertEqual(allowance["worker_cpu_seconds"], 40)
        self.assertLessEqual(allowance["worker_cpu_seconds"]+
                             made["delta"].kwargs["reserved_cpu_seconds"], grant.limits["worker_cpu_seconds"])
        self.assertTrue(all(owner.closed == 0 for owner in made.values()))

    def test_evidence_mode_pairs_optional_I_and_exact_A_owner(self):
        context, adoption, template, manifest, files = self.fixture(aggregate=True, receipt=False)
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace(evidence=True)
        made, calls = self.record_owners()
        observed, token = self.transfer(workspace)
        self.assertIs(self.invoke(profile, workspace, grant, mode="evidence"), token)
        self.assertEqual([tag for tag, _, _ in calls], ["A", "delta"])
        self.assertIsNone(made["delta"].kwargs["legacy_verifier"])
        self.assertIs(made["delta"].kwargs["aggregate_verifier"], made["A"])
        self.assertEqual(made["A"].kwargs["aggregate_image"], IMAGE)
        self.assertEqual(made["A"].kwargs["operations"], 24)
        self.assertEqual(made["delta"].kwargs["operations"], 3)
        self.assertEqual(made["A"].kwargs["reserved_cpu_seconds"], 70)
        self.assertEqual(made["A"].kwargs["submitted_bytes"], 65536)
        self.assertEqual(made["delta"].kwargs["reserved_cpu_seconds"], 70)
        self.assertEqual(made["delta"].kwargs["submitted_bytes"], 65536)
        self.assertIs(observed["aggregate_owner"], made["A"])
        self.assertIsNone(observed["receipt_owner"])

    def test_wrong_mode_missing_A_and_zero_author_budget_precede_owners(self):
        context, adoption, template, manifest, files = self.fixture()
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace(author_cpu=0)
        made, calls = self.record_owners()
        for mode, authoring in (("unadopted", False), ("evidence", False), ("atomic", True)):
            with self.subTest(mode=mode, authoring=authoring), self.assertRaises(ValueError):
                self.invoke(profile, workspace, grant, mode=mode, authoring=authoring)
        evidence_workspace, evidence_grant = self.open_workspace(evidence=True)
        with self.assertRaisesRegex(ValueError, "CLIENT_GRANT_CHANGED_OR_EXPIRED"):
            self.invoke(profile, workspace, evidence_grant)
        with self.assertRaisesRegex(ValueError, "RUNTIME_NO_ISSUER_DOWNGRADE"):
            self.invoke(profile, evidence_workspace, evidence_grant, mode="evidence")
        a_context, a_adoption, _, _, _ = self.fixture(aggregate=True, suffix="A-profile")
        a_profile = R.RuntimeProfile.from_context(a_context, a_adoption)
        with self.assertRaisesRegex(ValueError, "RUNTIME_NO_ISSUER_DOWNGRADE"):
            self.invoke(a_profile, workspace, grant, mode="atomic")
        self.assertEqual(calls, [])

    def test_original_deadline_recomputed_for_each_owner_and_context_bound(self):
        context, adoption, template, manifest, files = self.fixture()
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace()
        made, calls = self.record_owners()
        self.transfer(workspace)
        remaining = iter((50, 40, 30, 20, 10, 5, 2, 1))
        with patch.object(W.OperationGrant, "remaining_seconds", side_effect=lambda: next(remaining)):
            self.invoke(profile, workspace, grant, authoring=True)
        walls = [made["I"].kwargs["wall_seconds"], made["delta"].kwargs["wall_seconds"],
                 made["preparation"].args[1]["wall_seconds"]]
        self.assertTrue(all(0 < value <= 60 for value in walls))
        self.assertTrue(walls[0] > walls[1] > walls[2])
        self.assertEqual(grant.limits["wall_seconds"], 60)
        context.deadline = grant.started+1
        before = len(calls)
        with self.assertRaises(ValueError):
            self.invoke(profile, workspace, grant)
        self.assertEqual(len(calls), before)

    def test_construction_failure_closes_all_prior_owners(self):
        context, adoption, template, manifest, files = self.fixture(aggregate=True)
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace(evidence=True)
        made, calls = self.record_owners(fail="preparation")
        with self.assertRaisesRegex(ValueError, "INERT_CONSTRUCTION_preparation"):
            self.invoke(profile, workspace, grant, mode="evidence", authoring=True)
        self.assertEqual(set(made), {"I", "A", "delta"})
        self.assertTrue(all(owner.closed == 1 for owner in made.values()))
        self.assertFalse(grant._used)

    def test_deadline_expiry_during_construction_closes_existing_owner(self):
        context, adoption, template, manifest, files = self.fixture()
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace()
        made, calls = self.record_owners()
        with patch.object(W.OperationGrant, "remaining_seconds",
                          side_effect=(30, ValueError("INERT_EXPIRED_DEADLINE"))):
            with self.assertRaisesRegex(ValueError, "INERT_EXPIRED_DEADLINE"):
                self.invoke(profile, workspace, grant)
        self.assertEqual([tag for tag, _, _ in calls], ["I"])
        self.assertEqual(made["I"].closed, 1)
        self.assertFalse(grant._used)

    def test_failed_cleanup_preserves_primary_error_and_closes_remaining_owners(self):
        context, adoption, template, manifest, files = self.fixture(aggregate=True)
        profile = R.RuntimeProfile.from_context(context, adoption)
        workspace, grant = self.open_workspace(evidence=True)
        made, calls = self.record_owners(close_failure="delta")
        primary = ValueError("INERT_TRANSFER_FAILURE")
        self.transfer(workspace, error=primary)
        with self.assertRaises(BaseExceptionGroup) as caught:
            self.invoke(profile, workspace, grant, mode="evidence", authoring=True)
        self.assertIs(caught.exception.exceptions[0], primary)
        self.assertTrue(any("INERT_CLEANUP_delta" in str(error) for error in caught.exception.exceptions))
        self.assertTrue(all(owner.closed == 1 for owner in made.values()))
        self.assertTrue(workspace._poisoned)
        with self.assertRaises(ValueError):
            workspace.reserve(limits())


SELECTED = (
    "test_relocation_uses_selected_pins_and_copies_configuration",
    "test_wrong_selected_source_and_manifest_pin_are_rejected",
    "test_source_origin_and_minimum_source_closure_are_required",
    "test_rebound_manifest_cannot_escape_profile_integrity_check",
    "test_atomic_owner_pairing_and_disjoint_author_allowance",
    "test_evidence_mode_pairs_optional_I_and_exact_A_owner",
    "test_wrong_mode_missing_A_and_zero_author_budget_precede_owners",
    "test_original_deadline_recomputed_for_each_owner_and_context_bound",
    "test_construction_failure_closes_all_prior_owners",
    "test_deadline_expiry_during_construction_closes_existing_owner",
    "test_failed_cleanup_preserves_primary_error_and_closes_remaining_owners",
)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize,
           "CANONICAL_ISOLATED_RUNTIME_CONTROLS")
    OUTPUT = Path(args.output)
    F.need(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT
           and OUTPUT.is_relative_to(PROJECT/"experiments") and not OUTPUT.exists()
           and OUTPUT.parent.is_dir(), "FRESH_RUNTIME_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.TestSuite(RuntimeControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = [{"name": name, **pin(Path(module.__file__))}
               for name, module in sorted(sys.modules.items())
               if getattr(module, "__file__", None) and Path(module.__file__).is_relative_to(SOURCE)]
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "selected": list(SELECTED), "imports": imports,
        "scope": "REAL_PIN_REBASE_WORKSPACE_GRANT_WITH_EXPLICITLY_INERT_OWNER_CONSTRUCTORS",
        "mathematical_acceptance": False, "real_aggregate_checks": 0, "real_native_checks": 0,
        "proof_calls": 0, "network_calls": 0, "subprocess_calls": 0,
        "fixture_observations": dict(OBSERVED),
    }
    with (OUTPUT/"RESULT.json").open("xb") as stream:
        stream.write(encoded(report))
    print(encoded(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
