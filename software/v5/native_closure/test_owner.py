"""Focused native-closure binder/owner controls with INERT native execution.

Synthetic witnesses are deliberately not mathematical proofs. The supervisor
fixture never starts a process; its output exercises the same-call wrapper,
not the retained native checker or graph relation. Any resulting test tokens
belong only to these inert fixtures and are never exported as real authority.
Only a separately selected finite root runner may execute this file.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from aggregate_claims import bindings as B
from aggregate_claims import input as I
from modules import codec as C
from native_closure import binding as N
from native_closure import owner as O

MIB = 1024**2
IMAGE = "81"*32
OUTPUT = None
OBSERVED = {"inert_supervisor_calls": 0}
FIXTURE_COUNT = 0


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def journal(name, rank):
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"name": [["s", name]],
            "kind": "theorem", "universes": 0, "type": ["sort", ["zero"]],
            "value_hash": None, "meta": {}}]}]}
    summary = C.summarize(spec)
    return (b"DMKNM002"+(2).to_bytes(4, "little")+bytes.fromhex(B.RELATION_IMAGE)
        +bytes.fromhex(B.FOUNDATION+B.POLICY+C.summary_id(summary)+summary["group_root"])
        +(1).to_bytes(4, "little")+rank.to_bytes(8, "little"))


def sample():
    members = sorted([journal("SyntheticBaseNotChecked", 0), journal("SyntheticTargetNotChecked", 1)])
    target = journal("SyntheticTargetNotChecked", 1)
    witnesses = [b"SYNTHETIC_NOT_A_NATIVE_WITNESS_BASE", b"SYNTHETIC_NOT_A_NATIVE_WITNESS_TARGET"]
    wire = I.encode(adopted_image=IMAGE, claims=[], frontiers=[],
                    witnesses=witnesses, targets=[target])
    return witnesses, [target], members, wire


def reply(wire, members):
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")+bytes.fromhex(IMAGE+B.RELATION_IMAGE
        +B.FOUNDATION+B.POLICY)+B.commitment(members)+len(members).to_bytes(4, "little")
        +max(B.member_journal(j)["rank"] for j in members).to_bytes(8, "little")
        +(1).to_bytes(8, "little"))
    return {"schema": "DMKN_NATIVE_AGGREGATE_CONCLUSION_V1",
        "status": "CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION", "mathematical_admission": False,
        "input_sha256": sha(wire), "input_bytes": len(wire), "wire_bytes": len(wire),
        "header": list(header), "assumptions": [],
        "members": [{"index": index, "journal": list(raw),
            "siblings": [list(item) for item in B.opening(members, index)]}
            for index, raw in enumerate(members)], "edges": 1,
        "census": {"rows": 2, "bodies": 1, "openings": 2, "nodes": 3,
                   "maximum_depth": 2, "parent_edges": 1}}


class BindingControls(unittest.TestCase):
    def setUp(self):
        self.witnesses, self.targets, self.members, self.wire = sample()
        self.value = reply(self.wire, self.members)

    def bind(self, value=None, *, wire=None, targets=None, image=IMAGE):
        return N.bind_output(C.canonical(self.value if value is None else value),
            self.wire if wire is None else wire, self.targets if targets is None else targets,
            adopted_image=image)

    def test_pure_output_binding_is_not_admission(self):
        result = self.bind()
        self.assertIs(type(result), dict)
        self.assertEqual(tuple(result["members"]), tuple(self.members))
        self.assertEqual(result["input_sha256"], sha(self.wire))
        self.assertNotIsInstance(result, O.VerifiedNativeMember)

    def test_zero_input_and_output_assumptions_are_independent(self):
        for offset in (44, 48):
            changed = self.wire[:offset]+(1).to_bytes(4, "little")+self.wire[offset+4:]
            value = reply(changed, self.members)
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                self.bind(value, wire=changed)
        for assumptions in ([{"image": IMAGE, "journal": list(self.targets[0])}], {}, None):
            value = deepcopy(self.value); value["assumptions"] = assumptions
            with self.subTest(assumptions=assumptions), self.assertRaises(ValueError):
                self.bind(value)

    def test_same_call_input_and_complete_wire_are_bound(self):
        for field, value in (("input_sha256", "02"*32), ("input_bytes", len(self.wire)+1),
                             ("wire_bytes", len(self.wire)-1)):
            changed = deepcopy(self.value); changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.bind(changed)
        for changed in (self.wire+b"TAIL", self.wire[:-1]):
            with self.subTest(length=len(changed)), self.assertRaises(ValueError):
                self.bind(reply(changed, self.members), wire=changed)

    def test_exact_target_variant_cannot_be_replaced_by_module_id(self):
        variant = journal("SyntheticTargetNotChecked", 2)
        self.assertEqual(B.member_journal(variant)["module"],
                         B.member_journal(self.targets[0])["module"])
        self.assertNotEqual(variant, self.targets[0])
        with self.assertRaises(ValueError): self.bind(targets=[variant])
        changed = I.encode(adopted_image=IMAGE, claims=[], frontiers=[],
                           witnesses=self.witnesses, targets=[variant])
        with self.assertRaises(ValueError):
            self.bind(reply(changed, self.members), wire=changed, targets=[variant])

    def test_exact_header_members_and_order_are_bound(self):
        for offset in (12, 140, 172, 176, 184):
            value = deepcopy(self.value); value["header"][offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError): self.bind(value)
        # Positive but inflated rank/height must not pass merely because the
        # generic aggregate header permits them for different workflows.
        for offset in (176, 184):
            value = deepcopy(self.value); value["header"][offset] = 2
            with self.subTest(inflated_offset=offset), self.assertRaises(ValueError): self.bind(value)
        for mode in ("reverse", "duplicate", "missing", "index", "sibling"):
            value = deepcopy(self.value)
            if mode == "reverse": value["members"].reverse()
            elif mode == "duplicate": value["members"][1] = deepcopy(value["members"][0])
            elif mode == "missing": value["members"].pop()
            elif mode == "index": value["members"][0]["index"] = 1
            else: value["members"][0]["siblings"][0][0] ^= 1
            with self.subTest(mode=mode), self.assertRaises(ValueError): self.bind(value)
        with self.assertRaises(ValueError): self.bind(image="82"*32)

    def test_strict_fields_numbers_and_untrusted_stdout(self):
        mutations = []
        for field in ("input_bytes", "wire_bytes", "edges"):
            value = deepcopy(self.value); value[field] = True; mutations.append(value)
        for field in self.value["census"]:
            value = deepcopy(self.value); value["census"][field] = True; mutations.append(value)
        for location in ("index", "journal", "header", "sibling"):
            value = deepcopy(self.value)
            if location == "index": value["members"][0]["index"] = False
            elif location == "journal": value["members"][0]["journal"][0] = True
            elif location == "header": value["header"][0] = True
            else: value["members"][0]["siblings"][0][0] = False
            mutations.append(value)
        for field, wrong in (("mathematical_admission", 0), ("mathematical_admission", True),
                             ("schema", "OTHER"), ("status", "VERIFIED"), ("unexpected", True)):
            value = deepcopy(self.value); value[field] = wrong; mutations.append(value)
        for value in mutations:
            with self.subTest(value=value), self.assertRaises(ValueError): self.bind(value)
        raw = C.canonical(self.value)
        for value in (b"", raw+b"{}", raw[:-1]+b',"edges":1}',
                      raw.replace(b'"edges":1', b'"edges":1.0')):
            with self.subTest(raw=value[:40]), self.assertRaises(ValueError):
                N.bind_output(value, self.wire, self.targets, adopted_image=IMAGE)

    def test_distinct_exact_journals_sharing_module_remain_distinct(self):
        members = sorted([journal("SameModuleNotChecked", 0), journal("SameModuleNotChecked", 1)])
        self.assertEqual(B.member_journal(members[0])["module"],
                         B.member_journal(members[1])["module"])
        wire = I.encode(adopted_image=IMAGE, claims=[], frontiers=[],
                        witnesses=self.witnesses, targets=members)
        bound = N.bind_output(C.canonical(reply(wire, members)), wire, members, adopted_image=IMAGE)
        self.assertEqual(bound["members"], tuple(members))
        self.assertEqual(len(set(bound["members"])), 2)


class InertSupervisor:
    """Test double, not an OS supervisor, pin implementation, or native checker.

    The placeholder executable is deliberately NOT the adopted executable. Its
    reported pin and native response are injected only at this private fixture
    seam, so successful controls cannot be evidence of mathematical admission.
    """
    def __init__(self, root, members):
        self.root, self.members = root, members
        self.install = root / "inert-install"; self.install.mkdir(parents=True)
        self.manifest = self.install / "manifest.json"
        self.manifest.write_bytes(b'{"fixture":"INERT_NOT_INSTALLED"}')
        self.executable = self.install / "INERT_NOT_EXECUTABLE.bin"
        self.executable.write_bytes(b"NOT_NATIVE_NEVER_EXECUTE")
        self.pins = {}
        for name in O.SOURCE_NAMES:
            path = Path(sys.modules[name].__file__).resolve()
            raw = path.read_bytes()
            self.pins[str(path)] = {"bytes": len(raw), "sha256": sha(raw)}
        self.pins[str(self.executable)] = {"bytes": O.NATIVE_PIN[0], "sha256": O.NATIVE_PIN[1]}
        self.calls, self.break_pin = 0, False
        self.output_edit = self.process_edit = self.after_call = self.after_binding = None
        self.last_limits, self.last_command = None, None

    @staticmethod
    def absolute(value, *, directory=False, fresh=False):
        path = Path(value)
        if not path.is_absolute() or path.resolve() != path:
            raise ValueError("INERT_PATH")
        if fresh:
            if path.exists() or not path.parent.is_dir(): raise ValueError("INERT_NOT_FRESH")
        elif directory:
            if not path.is_dir(): raise ValueError("INERT_NOT_DIRECTORY")
        elif not path.is_file(): raise ValueError("INERT_NOT_FILE")
        return path

    @staticmethod
    def bounded_read(path, cap):
        with Path(path).open("rb") as stream: raw = stream.read(cap+1)
        if len(raw) > cap: raise ValueError("INERT_READ_LIMIT")
        return raw

    def pin(self, path):
        pin = dict(self.pins[str(path)])
        if self.break_pin and Path(path) == self.executable: pin["sha256"] = "01"*32
        return pin

    @staticmethod
    def overlap(left, right):
        return left == right or left in right.parents or right in left.parents

    @staticmethod
    def limits_checked(limits):
        if any(type(value) is not int or value <= 0 for value in limits.values()):
            raise ValueError("INERT_LIMIT")
        return dict(limits)

    def save_new(self, path, value):
        with Path(path).open("xb") as stream: stream.write(C.canonical(value))
        if Path(path).name == "binding.json" and self.after_binding:
            self.after_binding()

    def supervise(self, command, cwd, output, limits, Job, *, started):
        self.calls += 1; OBSERVED["inert_supervisor_calls"] += 1
        self.last_command, self.last_limits = list(command), dict(limits)
        if command[:2] != [str(self.executable), "check"] or cwd != self.install:
            raise ValueError("INERT_WRONG_COMMAND")
        if Job is not InertJob: raise ValueError("INERT_WRONG_JOB")
        wire = Path(command[2]).read_bytes()
        value = reply(wire, self.members)
        if self.output_edit: self.output_edit(value)
        output.mkdir()
        (output / "stdout.txt").write_bytes(C.canonical(value))
        (output / "stderr.txt").write_bytes(b"")
        result = {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
            "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
            "termination_requested": False, "wall_seconds_through_cleanup": 0.01,
            "final_job": {"active_processes": 0, "terminated_processes": 0, "cpu_seconds": 0.01}}
        if self.process_edit: self.process_edit(result)
        if self.after_call: self.after_call(Path(command[2]))
        return result


class InertJob:
    def __init__(self, *args, **kwargs):
        raise AssertionError("No real Job may be constructed by these controls")


class OwnerControls(unittest.TestCase):
    def fixture(self, *, members=None, **overrides):
        global FIXTURE_COUNT
        FIXTURE_COUNT += 1
        root = OUTPUT / ("fixture-%03d" % FIXTURE_COUNT)
        root.mkdir()
        witnesses, targets, ordinary, wire = sample()
        supervisor = InertSupervisor(root, ordinary if members is None else members)
        modules = patch.dict(sys.modules, {"_dmkn_v5_admission_supervisor": supervisor,
            "_dmkn_v5_admission_job": SimpleNamespace(Job=InertJob)})
        modules.start(); self.addCleanup(modules.stop)
        loader = patch.object(O, "_load_supervision", return_value=(supervisor, InertJob, {}))
        loader.start(); self.addCleanup(loader.stop)
        options = {"supervisor_manifest": supervisor.manifest,
            "supervisor_manifest_sha256": sha(supervisor.manifest.read_bytes()),
            "executable": supervisor.executable, "runtime_pins": supervisor.pins,
            "adopted_image": IMAGE, "deadline": time.monotonic()+45,
            "submitted_bytes": 4096, "reserved_cpu_seconds": 3, "controller_cpu_seconds": 10}
        options.update(overrides)
        owner = O.NativeClosureOwner(**options)
        self.addCleanup(owner.close)
        return owner, supervisor, root / "operation", witnesses, targets, wire

    @staticmethod
    def call(owner, output, witnesses, targets):
        return owner.check(witnesses, targets, output,
                           cpu_seconds=3, wall_seconds=30, memory_mib=64)

    def assert_revoked(self, owner):
        self.assertTrue(owner.report()["closed"])
        self.assertEqual(owner.report()["live_handles"], 0)
        with self.assertRaises(ValueError): owner.members()

    def test_same_call_success_and_copied_descriptions(self):
        owner, supervisor, output, witnesses, targets, wire = self.fixture()
        deadline = owner._deadline
        tokens = self.call(owner, output, witnesses, targets)
        self.assertEqual(len(tokens), 2); self.assertIsNot(tokens[0], tokens[1])
        self.assertTrue(all(type(token) is O.VerifiedNativeMember for token in tokens))
        self.assertEqual(tokens, owner.members()); self.assertEqual(supervisor.calls, 1)
        self.assertEqual(owner._deadline, deadline)
        rows = [owner.describe(token) for token in tokens]
        self.assertEqual([row["journal"] for row in rows], sorted(sample()[2]))
        self.assertTrue(all(row["proof_form"] == "NATIVE_COMPLETE_CLOSURE" for row in rows))
        rows[0]["journal"] = b"changed returned copy"
        self.assertNotEqual(owner.describe(tokens[0])["journal"], rows[0]["journal"])
        report = owner.report()
        self.assertEqual((report["attempts"], report["submitted_bytes"], report["reserved_cpu_seconds"]),
                         (1, len(wire), 3))
        self.assertEqual(report["authority"], "LOCAL_RESOURCE_ACCOUNTING_NOT_PROOF")
        self.assertEqual(supervisor.last_limits["active_processes"], 2)
        self.assertLessEqual(supervisor.last_limits["wall_seconds"], 30)
        owner.close()
        with self.assertRaises(ValueError): owner.describe(tokens[0])
        self.assert_revoked(owner)

    def test_owner_keeps_same_module_exact_variants(self):
        members = sorted([journal("SameModuleNotChecked", 0), journal("SameModuleNotChecked", 1)])
        owner, _, output, witnesses, _, _ = self.fixture(members=members)
        tokens = self.call(owner, output, witnesses, members)
        descriptions = [owner.describe(token) for token in tokens]
        self.assertEqual([row["journal"] for row in descriptions], members)
        self.assertEqual(descriptions[0]["module"], descriptions[1]["module"])
        self.assertNotEqual(tokens[0], tokens[1])

    def test_fabricated_saved_and_foreign_tokens_revoke(self):
        foreign = None
        for mode in ("fabricated", "saved", "foreign"):
            owner, _, output, witnesses, targets, _ = self.fixture()
            tokens = self.call(owner, output, witnesses, targets)
            if mode == "fabricated": bad = O.VerifiedNativeMember(); foreign = tokens[0]
            elif mode == "saved": bad = owner.describe(tokens[0])
            else: bad = foreign
            with self.subTest(mode=mode), self.assertRaises(ValueError): owner.describe(bad)
            self.assert_revoked(owner)

    def test_no_live_members_before_check_and_no_repeated_check(self):
        owner, supervisor, _, _, _, _ = self.fixture()
        with self.assertRaises(ValueError): owner.members()
        self.assert_revoked(owner); self.assertEqual(supervisor.calls, 0)
        owner, supervisor, output, witnesses, targets, _ = self.fixture()
        tokens = self.call(owner, output, witnesses, targets)
        with self.assertRaises(ValueError): self.call(owner, output, witnesses, targets)
        self.assertEqual(supervisor.calls, 1)
        with self.assertRaises(ValueError): owner.describe(tokens[0])
        self.assert_revoked(owner)

    def test_expiry_and_controller_exhaustion_revoke_tokens(self):
        for clock in ("monotonic", "process_time"):
            owner, _, output, witnesses, targets, _ = self.fixture()
            token = self.call(owner, output, witnesses, targets)[0]
            value = owner._deadline+1 if clock == "monotonic" else owner._cpu_started+owner._caps[2]+1
            with self.subTest(clock=clock), patch.object(O.time, clock, return_value=value):
                with self.assertRaises(ValueError): owner.describe(token)
            self.assert_revoked(owner)

    def test_changed_pins_before_after_and_final_binding_refuse(self):
        for phase in ("before", "after_call", "after_binding", "inspection"):
            owner, supervisor, output, witnesses, targets, _ = self.fixture()
            if phase == "before": supervisor.break_pin = True
            elif phase == "after_call":
                supervisor.after_call = lambda path: setattr(supervisor, "break_pin", True)
            elif phase == "after_binding":
                supervisor.after_binding = lambda: setattr(supervisor, "break_pin", True)
            if phase == "inspection":
                token = self.call(owner, output, witnesses, targets)[0]
                supervisor.break_pin = True
                with self.assertRaises(ValueError): owner.describe(token)
            else:
                with self.subTest(phase=phase), self.assertRaises(ValueError):
                    self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner)
            self.assertEqual(supervisor.calls, 0 if phase == "before" else 1)

    def test_input_output_substitution_and_symbol_replacement_refuse(self):
        for mode in ("input", "digest", "assumption", "symbol"):
            owner, supervisor, output, witnesses, targets, _ = self.fixture()
            if mode == "input": supervisor.after_call = lambda path: path.write_bytes(b"SWAPPED")
            elif mode == "digest": supervisor.output_edit = lambda value: value.update(input_sha256="00"*32)
            elif mode == "assumption": supervisor.output_edit = lambda value: value.update(assumptions=[{}])
            if mode == "symbol":
                with patch.object(N, "bind_output", return_value={}), self.assertRaises(ValueError):
                    self.call(owner, output, witnesses, targets)
            else:
                with self.subTest(mode=mode), self.assertRaises(ValueError):
                    self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner)
            self.assertEqual(supervisor.calls, 0 if mode == "symbol" else 1)

    def test_unclean_or_over_budget_supervision_never_mints(self):
        mutations = [("status", "FAILED"), ("child_exit_code", 1), ("child_exit_code", False),
            ("job_closed", False), ("direct_child_reaped", False), ("cleanup_errors", ["cleanup"]),
            ("termination_requested", True), ("wall_seconds_through_cleanup", 31),
            ("wall_seconds_through_cleanup", True)]
        for field, value in mutations:
            owner, supervisor, output, witnesses, targets, wire = self.fixture()
            supervisor.process_edit = lambda row, k=field, v=value: row.update({k: v})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner)
            report = owner.report()
            self.assertEqual((report["attempts"], report["submitted_bytes"], report["reserved_cpu_seconds"]),
                             (1, len(wire), 3))
            self.assertEqual(report["observed_worker_cpu_seconds"], 0.01)
            self.assertEqual(supervisor.calls, 1)
        for field, value in (("active_processes", 1), ("terminated_processes", 1),
                              ("active_processes", False), ("cpu_seconds", 4),
                              ("cpu_seconds", True), ("cpu_seconds", -1)):
            owner, supervisor, output, witnesses, targets, _ = self.fixture()
            supervisor.process_edit = lambda row, k=field, v=value: row["final_job"].update({k: v})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner); self.assertEqual(supervisor.calls, 1)
            expected = (value if type(value) in (int, float) and value >= 0 else None) \
                       if field == "cpu_seconds" else 0.01
            self.assertEqual(owner.report()["observed_worker_cpu_seconds"], expected)

    def test_insufficient_allowance_refuses_without_child_or_retry(self):
        for caps in ({"submitted_bytes": 100}, {"reserved_cpu_seconds": 2}):
            owner, supervisor, output, witnesses, targets, _ = self.fixture(**caps)
            with self.subTest(caps=caps), self.assertRaises(ValueError):
                self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner); self.assertEqual(supervisor.calls, 0)
            self.assertEqual(owner.report()["attempts"], 1 if "submitted_bytes" in caps else 0)
            with self.assertRaises(ValueError): self.call(owner, output, witnesses, targets)
            self.assertEqual(supervisor.calls, 0)

    def test_reentrant_encoder_entry_cannot_reuse_reservation(self):
        original, held, nested = I.encode, {}, []

        def reentrant_encode(**kwargs):
            if "owner" in held:
                nested.append("entered")
                with self.assertRaises(ValueError):
                    self.call(held["owner"], held["output"], kwargs["witnesses"], kwargs["targets"])
            return original(**kwargs)

        # Adopt the test-only hook before construction, so this tests the entry
        # guard rather than the separate symbol-replacement control above.
        with patch.object(I, "encode", side_effect=reentrant_encode):
            owner, supervisor, output, witnesses, targets, wire = self.fixture()
            held.update(owner=owner, output=output)
            with self.assertRaises(ValueError): self.call(owner, output, witnesses, targets)
            self.assert_revoked(owner)
            self.assertEqual(nested, ["entered"]); self.assertEqual(supervisor.calls, 0)
            report = owner.report()
            self.assertEqual((report["attempts"], report["submitted_bytes"], report["reserved_cpu_seconds"]),
                             (1, len(wire), 3))

    def test_thread_identity_and_membership_changes_revoke(self):
        for mode in ("thread", "membership"):
            owner, _, output, witnesses, targets, _ = self.fixture()
            token = self.call(owner, output, witnesses, targets)[0]
            if mode == "thread":
                with patch.object(O.threading, "current_thread", return_value=object()), \
                     self.assertRaises(ValueError): owner.describe(token)
            else:
                owner._handles[token] = journal("TamperedMembership", 0)
                with self.assertRaises(ValueError): owner.describe(token)
            self.assert_revoked(owner)

    def test_unknown_failed_launch_cost_is_not_zero(self):
        owner, supervisor, output, witnesses, targets, wire = self.fixture()

        def failed_launch(path):
            raise RuntimeError("INERT_SUPERVISOR_FAILED_WITHOUT_REPORT")

        supervisor.after_call = failed_launch
        with self.assertRaises(RuntimeError): self.call(owner, output, witnesses, targets)
        self.assert_revoked(owner)
        self.assertEqual(supervisor.calls, 1)
        self.assertIsNone(owner.report()["observed_worker_cpu_seconds"])
        self.assertEqual((owner.report()["attempts"], owner.report()["submitted_bytes"],
                          owner.report()["reserved_cpu_seconds"]), (1, len(wire), 3))


def main():
    """Finite inert controls only. Root must select/supervise this entry point."""
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise SystemExit("usage: test_owner.py --output ABSOLUTE_SELECTED_DIRECTORY")
    selected_output = Path(sys.argv[2])
    if not selected_output.is_absolute() or selected_output.resolve() != selected_output \
       or not selected_output.is_dir() or (selected_output / "controls-result.json").exists():
        raise SystemExit("control output must be a selected absolute directory without a prior result")
    OUTPUT = selected_output / "controls"
    if OUTPUT.exists(): raise SystemExit("control fixture directory must be fresh")
    OUTPUT.mkdir()
    source_paths = sorted({Path(__file__).resolve(), *[
        Path(sys.modules[name].__file__).resolve() for name in O.SOURCE_NAMES]})
    identities = {str(path): {"bytes": path.stat().st_size, "sha256": sha(path.read_bytes())}
                  for path in source_paths}
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(BindingControls),
                               unittest.defaultTestLoader.loadTestsFromTestCase(OwnerControls)])
    selected = [test.id() for group in suite for test in group]
    started = time.monotonic()
    with patch.object(subprocess, "Popen", side_effect=AssertionError("real child forbidden")), \
         patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
         patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged = all(path.stat().st_size == identities[str(path)]["bytes"] and
                    sha(path.read_bytes()) == identities[str(path)]["sha256"] for path in source_paths)
    report = {"schema": "DMKN_NATIVE_CLOSURE_INERT_CONTROLS_V1",
        "status": "PASS" if result.wasSuccessful() and unchanged else "FAIL",
        "selected": selected, "tests_run": result.testsRun,
        "failures": [[test.id(), detail] for test, detail in result.failures],
        "errors": [[test.id(), detail] for test, detail in result.errors],
        "skipped": [[test.id(), reason] for test, reason in result.skipped],
        "source_identities": identities, "sources_unchanged": unchanged,
        "inert_supervisor_calls": OBSERVED["inert_supervisor_calls"],
        "real_native_calls": 0, "real_network_calls": 0, "real_proof_calls": 0,
        "wall_seconds": time.monotonic()-started,
        "scope": "SYNTHETIC_WRAPPER_CONTROLS_NOT_MATHEMATICAL_ADMISSION"}
    with (selected_output / "controls-result.json").open("xb") as stream: stream.write(C.canonical(report))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
