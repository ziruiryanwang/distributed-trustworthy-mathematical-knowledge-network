"""Ten new lifecycle controls: synthetic mathematics/owners, zero native calls.

Real new profile/configuration/staging/adoption and inherited request plumbing;
only retained installation/build adoption and process execution are synthetic.
This suite does not run predecessor suites or claim a genuine I/A proof.
"""
from copy import deepcopy
from dataclasses import asdict, replace
import argparse
from pathlib import Path
import struct
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from aggregate_lifecycle import producer as L, snapshot as N
from aggregate_small import producer as S
from production import producer as P
from aggregate_claims import bindings as B
from admission.bindings import journal
from delta_claims.claims import expected_journal
from mixed_claims.packet import Envelope, SCHEMA
from modules import codec as C

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
IMAGE = "a5"*32
OUTPUT = None
DISPATCHES = []


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
    return P.file_pin(path)


def spec(name):
    return {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
        "name": [["s", name]], "universes": 0, "type": ["sort", ["zero"]],
        "value_hash": None, "meta": {}}]}]}


def exact(name, rank=0):
    return expected_journal(C.summarize(spec(name)), rank, B.RELATION_IMAGE)


def witness(name, rank, parents):
    return {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": journal(exact(name, rank))["image"],
        "rank": rank, "local_spec": spec(name), "rows": [], "bodies": [],
        "parents": [{"journal": list(j), "openings": []} for j in parents]}


def packet(previous=None):
    if previous is None:
        parents = [exact("Base0"), exact("Base1")]
        claims = [{"tag": 0, "statement": list(j),
                   "receipt_hex": (b"SYNTHETIC-I-NOT-A-PROOF-"+bytes([i])).hex()}
                  for i,j in enumerate(parents)]
        frontiers = [{"claim_index": i, "journal": list(j), "member_index": 0, "siblings": []}
                     for i,j in enumerate(parents)]
        name, rank = "First", 1
    else:
        parents = [previous.target_journal]
        claims = [{"tag": 1, "statement": list(previous.expected_header),
                   "receipt_hex": b"SYNTHETIC-A-NOT-A-PROOF".hex()}]
        frontiers = [{"claim_index": 0, "journal": list(previous.target_journal),
            "member_index": previous.target_index, "siblings": [list(s) for s in previous.target_siblings]}]
        name, rank = "Second", 2
    return C.canonical({"schema": SCHEMA, "claims": claims, "frontiers": frontiers,
                        "deltas": [witness(name, rank, parents)]}), exact(name, rank)


def clean(argv, cwd, limits, cpu=0.125):
    return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
        "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
        "termination_requested": False, "argv": argv, "cwd": str(cwd), "limits": limits,
        "final_job": {"active_processes": 0, "terminated_processes": 0, "cpu_seconds": cpu}}


class InertSupervisor:
    CEILINGS = {"memory_mib": 8192}

    def __init__(self):
        self.mode = "complete"

    def absolute(self, value, *, directory=False, fresh=False):
        path = Path(value)
        P.require(path.is_absolute() and path.resolve() == path and not path.is_symlink(),
                  "SYNTHETIC_ORDINARY_PATH")
        P.require(not path.exists() if fresh else path.is_dir() if directory else path.is_file(),
                  "SYNTHETIC_PATH_STATE")
        return path

    def overlap(self, a, b):
        return a.is_relative_to(b) or b.is_relative_to(a)

    def bounded_read(self, path, maximum):
        with self.absolute(path).open("rb") as stream:
            raw = stream.read(maximum+1)
        P.require(len(raw) <= maximum, "SYNTHETIC_READ_BOUND")
        return raw

    def save_new(self, path, value):
        save(Path(path), P.encoded(value))

    def supervise(self, argv, cwd, evidence, limits, job):
        P.require(argv[1] == "snapshot" and argv[0].endswith("snapshot.fake")
                  and job is object, "ONLY_EXPLICIT_SYNTHETIC_SNAPSHOT_DISPATCH")
        output = Path(argv[9]).parent
        command = P.parse((output/"COMMAND.json").read_bytes())
        manifest = P.parse((output/"staging.json").read_bytes())
        P.require(command["argv"] == argv and command["limits"] == limits
                  and command["cwd"] == str(cwd), "SYNTHETIC_DURABLE_COMMAND")
        P.require(argv[12:] == [p["file"]["path"] for p in manifest["parents"]],
                  "SYNTHETIC_ORDERED_STAGED_PARENTS")
        for pin in [manifest["wire"], manifest["expected"], *[p["file"] for p in manifest["parents"]]]:
            P.require(P.file_pin(Path(pin["path"])) == pin, "SYNTHETIC_ACTUAL_STAGED_PIN")
        evidence.mkdir()
        save(evidence/"command.json", P.encoded({"argv": argv, "cwd": str(cwd), "limits": limits}))
        binding = P.hash_bytes(b"SYNTHETIC-SESSION\0"+Path(argv[4]).read_bytes())
        capsule = b"DMKNAS01"+struct.pack("<I", 1)+bytes.fromhex(binding)+b"NOT-A-REAL-CAPSULE"
        if self.mode != "missing-capsule":
            save(Path(argv[9]), capsule)
        actual = {"schema": "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1",
            "status": "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED", "aggregate_image": IMAGE,
            "header": list(Path(argv[5]).read_bytes()), "capsule_path": argv[9],
            "capsule_bytes": len(capsule), "capsule_sha256": P.hash_bytes(capsule),
            "capsule_binding": P.hash_bytes(b"SYNTHETIC-CAPSULE\0"+capsule), "session_binding": binding,
            "segments": 1, "assumptions": len(manifest["parents"]),
            "mathematical_admission": False, "proof_calls": 0, "guest_execute_calls": 1}
        save(evidence/"stdout.txt", P.encoded(actual))
        save(evidence/"stderr.txt", b"SYNTHETIC; NO PROCESS WAS EXECUTED\n")
        save(Path(argv[10]), P.encoded({"scope": "SYNTHETIC_NOT_GUEST_EXECUTION"}))
        DISPATCHES.append({"argv": argv, "mode": self.mode, "authority": "INERT_NO_NATIVE_OR_PROOF"})
        return clean(argv, cwd, limits, limits["cpu_seconds"]+1 if self.mode == "cpu-overshoot" else 0.125)


class SyntheticSupport:
    def __init__(self, install, host):
        self._A, self._Job, self._install = InertSupervisor(), object, install
        self._pins = {host["path"]: host}

    def _check(self, pins):
        for path,pin in pins.items():
            self._A.absolute(path)
            P.require(P.file_pin(Path(path)) == pin, "SYNTHETIC_INPUT_PIN_CHANGED")

    def _read(self, pin, maximum):
        P.pin_fields(pin, maximum); self._check({pin["path"]: pin})
        return self._A.bounded_read(pin["path"], maximum)

    def close(self):
        pass


class Fixture:
    def __init__(self, name):
        self.path = OUTPUT/name; self.path.mkdir()
        self.install = self.path/"inputs"; self.install.mkdir()
        stage = save(self.install/"stage.fake", b"NOT-AN-EXECUTABLE")
        self.snapshot_host = save(self.install/"snapshot.fake", b"NOT-AN-EXECUTABLE-EITHER")
        self.image = save(self.install/"image.fake", b"NOT-A-REAL-IMAGE")
        builds = {name: save(self.install/(name+".json"), P.encoded({"synthetic_role": name}))
                  for name in ("result", "attempt", "selection", "source_map", "command")}
        base = {"schema": S.PREFIX+"PROFILE_V1", "support_profile": {
            "schema": "SYNTHETIC_SUPPORT_NOT_BUILD_ADOPTION", "host": stage,
            "image_id": IMAGE, "foundation": B.FOUNDATION, "policy": B.POLICY},
            "source_pins": [P.file_pin(Path(S.__file__).resolve().parent/n) for n in S.SOURCE_NAMES],
            "relation_image": B.RELATION_IMAGE, "host_build": {}, "image_adoption": {},
            "stage_memory_ceiling_mib": 4096}
        self.profile = {"schema": L.PROFILE_SCHEMA, "base_profile": base,
            "source_pins": [P.file_pin(path) for path in L.source_paths()], "snapshot_host_build": builds}

    def owner(self, profile=None):
        def image(owner):
            owner._image = self.image; owner._add(owner._pins, self.image)
        def build(owner, pins, table, role):
            P.require(role == "snapshot", "ONLY_SYNTHETIC_SNAPSHOT_BUILD_ADOPTION")
            for pin in pins.values(): owner._add(table, pin)
            owner._add(table, self.snapshot_host)
            return self.snapshot_host
        with patch.object(P, "Producer", lambda p: SyntheticSupport(self.install, p["host"])), \
             patch.object(S.AggregateProducer, "_adopt_build", lambda o: None), \
             patch.object(S.AggregateProducer, "_adopt_image", image), \
             patch.object(S.AggregateProducer, "_adopt_host_build", build):
            return L.LifecycleProducer(deepcopy(self.profile if profile is None else profile))

    def configuration(self, owner, name, *, previous=None, change=None):
        raw, target = packet(previous)
        packet_pin = save(self.install/(name+"-packet.json"), raw)
        profile_pin = save(self.install/(name+"-profile.json"), P.encoded(owner.profile_document()))
        cfg = {"schema": N.CONFIG_SCHEMA, "profile_id": owner.profile_id, "profile_document": profile_pin,
            "packet": packet_pin, "target_journal": target.hex(), "envelope": asdict(Envelope()),
            "cycles": 1 << 26, "po2": 18, "diagnostic_mode": "stats", "limits": dict(N.CEILINGS),
            "output_directory": str(self.path/(name+"-layout"))}
        if change: change(cfg)
        config_pin = save(self.install/(name+"-configuration.json"), P.encoded(cfg))
        runtime = {p["path"]: p["sha256"] for p in owner._pins.values()}
        runtime.update({p["path"]: p["sha256"] for p in (config_pin, profile_pin, packet_pin)})
        selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name, "sources": {},
            "runtime_pins": runtime, "argv": ["SYNTHETIC-NOT-EXECUTED", config_pin["path"], config_pin["sha256"]],
            "limits": {"cpu_seconds": 210, "wall_seconds": 300, "memory_mib": 3072,
                       "active_processes": 3, "stdout_bytes": P.MIB, "stderr_bytes": P.MIB}}
        selection_pin = save(self.install/(name+"-selection.json"), P.encoded(selection))
        prepared = owner.prepare(raw, target, envelope=Envelope())
        return cfg, config_pin, selection_pin, selection, prepared

    def complete(self, owner, name, *, previous=None, mode="complete"):
        cfg, config_pin, selection_pin, selection, prepared = self.configuration(owner, name, previous=previous)
        owner._A.mode = mode
        report = owner.snapshot(prepared, configuration=config_pin, selection=selection_pin)
        outer = {"schema": "DMKN_V5_LOCAL_CHECK_RESULT_V1", "selection_sha256": selection_pin["sha256"],
            "result": clean(selection["argv"], PROJECT, selection["limits"]), "wrapper_cpu_seconds": 0,
            "wall_seconds": 1, "authority": "SYNTHETIC_OUTER_NOT_A_REAL_JOB",
            "runtime_scope": "NO_NATIVE_NO_BUILD_NO_PROOF"}
        outer_pin = save(self.path/(name+"-outer.json"), P.encoded(outer))
        evidence = {"result": P.file_pin(Path(cfg["output_directory"])/"RESULT.json"),
            "outer": outer_pin, "selection": selection_pin, "configuration": config_pin,
            "command": report["command"]}
        return report, evidence, prepared

    def request(self, owner, name, evidence, *, prior=()):
        stage = {"cpu_seconds": 1, "wall_seconds": 20, "memory_mib": 64, "active_processes": 1,
                 "stdout_bytes": 4096, "stderr_bytes": 4096, "output_bytes": 4096}
        return owner.production_request(evidence, allowance_id="ab"*32,
            budget={"worker_cpu_seconds": 50, "controller_cpu_seconds": 30, "wall_seconds": 120,
                "output_bytes": 64*P.MIB, "output_entries": 100,
                "stages": {kind: dict(stage) for kind in P.KINDS}}, checkpoints=[],
            prior_attempts=list(prior), output_directory=self.path/(name+"-production"), stage_limit=1,
            carried_external_costs={"worker_cpu_seconds": 0, "controller_cpu_seconds": 0,
                "wall_seconds": 0, "scope": "EXPLICIT_SYNTHETIC_NO_PRODUCTION_COST"})


class LifecycleControls(unittest.TestCase):
    def opened(self, name):
        fixture = Fixture(name); owner = fixture.owner()
        self.addCleanup(owner.close)
        return fixture, owner

    def test_stable_profile_source_mutation_and_closed_entry(self):
        f, owner = self.opened("profile")
        self.assertEqual(P.encoded(owner.profile), P.encoded(f.profile["base_profile"]))
        self.assertEqual(owner.profile_id, P.hash_bytes(L.PROFILE_DOMAIN+P.encoded(f.profile)))
        copy = owner.profile_document(); copy["schema"] = "changed"
        self.assertEqual(owner.profile_document(), f.profile)
        owner._lifecycle_profile["source_pins"][0]["sha256"] = "00"*32
        with self.assertRaisesRegex(ValueError, "LIFECYCLE_PROFILE_MUTATED"):
            owner.profile_document()
        owner.close()
        with patch.object(owner, "_read", side_effect=AssertionError("CLOSED_OWNER_READ")):
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_CLOSED_OR_BUSY"):
                f.request(owner, "closed", {})

    def test_synthetic_I_to_A_renewal_and_no_host_preflight(self):
        f, owner = self.opened("renewal"); before = len(DISPATCHES)
        first, e1, prepared1 = f.complete(owner, "first")
        req1 = f.request(owner, "first", e1)
        q1 = owner.preflight(req1)
        self.assertEqual(first["status"], N.PASS)
        self.assertEqual(tuple(p.tag for p in prepared1.parents), (0, 0))
        self.assertEqual(req1["session"]["assumptions"], 2)
        second, e2, prepared2 = f.complete(owner, "second", previous=prepared1)
        req2 = f.request(owner, "second", e2); q2 = owner.preflight(req2)
        self.assertEqual(second["status"], N.PASS)
        self.assertEqual(tuple(p.tag for p in prepared2.parents), (1,))
        self.assertEqual(prepared2.parents[0].statement, prepared1.expected_header)
        self.assertEqual(B.decode_header(prepared2.expected_header, adopted_image=IMAGE)["seal_height"], 2)
        self.assertEqual(len(DISPATCHES)-before, 2)
        self.assertNotEqual(q1["session_id"], q2["session_id"])
        self.assertEqual(q1["profile_id"], q2["profile_id"])
        self.assertFalse(Path(req1["output_directory"]).exists())
        self.assertFalse(Path(req2["output_directory"]).exists())
        self.assertFalse(first["mathematical_admission"] or second["mathematical_admission"])

    def test_forged_preparation_wire_or_parent_order_never_dispatches(self):
        f, owner = self.opened("forged-plan"); before = len(DISPATCHES)
        cfg, c, s, unused, prepared = f.configuration(owner, "selected")
        for invalid in (replace(prepared, wire=prepared.wire+b"x"),
                        replace(prepared, parents=tuple(reversed(prepared.parents)))):
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_EXACT_PREPARATION"):
                owner.snapshot(invalid, configuration=c, selection=s)
        self.assertFalse(Path(cfg["output_directory"]).exists())
        self.assertEqual(len(DISPATCHES), before)

    def test_wrong_target_or_changed_original_pin_never_dispatches(self):
        f, owner = self.opened("target-pin"); before = len(DISPATCHES)
        cfg, c, s, unused, prepared = f.configuration(owner, "wrong-target",
            change=lambda v: v.update(target_journal=exact("NotPresent").hex()))
        with self.assertRaises(ValueError): owner.snapshot(prepared, configuration=c, selection=s)
        cfg2, c2, s2, unused, p2 = f.configuration(owner, "wrong-pin")
        c2 = {**c2, "sha256": "00"*32}
        with self.assertRaisesRegex(ValueError, "SYNTHETIC_INPUT_PIN_CHANGED"):
            owner.snapshot(p2, configuration=c2, selection=s2)
        self.assertFalse(Path(cfg["output_directory"]).exists())
        self.assertFalse(Path(cfg2["output_directory"]).exists())
        self.assertEqual(len(DISPATCHES), before)

    def test_reordered_generated_manifest_refused_at_adoption(self):
        f, owner = self.opened("manifest-order")
        report, evidence, unused = f.complete(owner, "selected")
        original = N._doc
        def reordered(o, pin, maximum=P.MIB):
            value = original(o, pin, maximum)
            if pin == report["staging"]:
                value["parents"] = list(reversed(value["parents"]))
            return value
        # Inject a decoded-record mutation; preserve all actual saved evidence.
        with patch.object(N, "_doc", reordered):
            with self.assertRaisesRegex(ValueError, "LIFECYCLE_EXACT_STAGING_MANIFEST"):
                f.request(owner, "bad", evidence)
        self.assertEqual(N._doc(owner, report["staging"])["parents"][0]["tag"], 0)

    def test_geometry_and_output_limits_refuse_before_layout(self):
        f, owner = self.opened("limits"); before = len(DISPATCHES)
        changes = (lambda v: v.update(po2=19), lambda v: v.update(cycles=(1 << 26)+1),
                   lambda v: v["limits"].update(output_bytes=1))
        for index, change in enumerate(changes):
            cfg, c, s, unused, prepared = f.configuration(owner, "bad-"+str(index), change=change)
            with self.assertRaises(ValueError): owner.snapshot(prepared, configuration=c, selection=s)
            self.assertFalse(Path(cfg["output_directory"]).exists())
        self.assertEqual(len(DISPATCHES), before)

    def test_missing_capsule_is_preserved_failure_not_adoptable(self):
        f, owner = self.opened("partial")
        report, evidence, unused = f.complete(owner, "selected", mode="missing-capsule")
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["host_calls_attempted"], 1)
        self.assertEqual(report["worker_cpu_charge"], 0.125)
        self.assertIsNone(report["session"])
        with self.assertRaisesRegex(ValueError, "LIFECYCLE_COMPLETED_SNAPSHOT_ONLY"):
            f.request(owner, "forbidden", evidence)

    def test_clean_cpu_overshoot_cannot_report_success(self):
        f, owner = self.opened("overshoot")
        report, evidence, unused = f.complete(owner, "selected", mode="cpu-overshoot")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(report["closure_accounting_known"])
        self.assertEqual(report["worker_cpu_charge"], N.CEILINGS["worker_cpu_seconds"]+1)
        self.assertIn("LIFECYCLE_SNAPSHOT_WORKER_CPU", report["error"])
        with self.assertRaises(ValueError): f.request(owner, "forbidden", evidence)

    def test_finalization_sentinel_overrides_snapshot(self):
        f, owner = self.opened("sentinel")
        report, evidence, unused = f.complete(owner, "selected")
        save(Path(evidence["result"]["path"]).parent/"FINALIZATION-FAILED.json",
             P.encoded({"status": "SYNTHETIC_FINALIZATION_FAILURE"}))
        with self.assertRaisesRegex(ValueError, "FINALIZATION_OVERRIDE"):
            f.request(owner, "forbidden", evidence)

    def test_prior_profile_lineage_cannot_be_relabelled(self):
        f, owner = self.opened("lineage")
        unused, evidence, unused_plan = f.complete(owner, "selected")
        request = f.request(owner, "valid", evidence); quote = owner.preflight(request)
        prior = {key: None for key in S.ATTEMPT_FIELDS}
        prior.update(schema=S.PREFIX+"ATTEMPT_V1", status="PASS_SELECTED_PREFIX_ONLY",
            profile_id="00"*32, session_id=quote["session_id"], allowance_id=request["allowance_id"],
            prior_attempts=[], budget=request["budget"], carried_external_costs=request["carried_external_costs"])
        pin = save(f.path/"wrong-profile-attempt.json", P.encoded(prior))
        with self.assertRaisesRegex(ValueError, "COMPLETE_SAME_ALLOWANCE_LINEAGE"):
            f.request(owner, "forbidden", evidence, prior=[pin])


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    OUTPUT = Path(parser.parse_args().output)
    P.require(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
              and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_CONTROLS")
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and not OUTPUT.exists()
              and OUTPUT.parent.is_dir(), "FRESH_CONTROL_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LifecycleControls)
    P.require(suite.countTestCases() == 10, "EXACT_TEN_LIFECYCLE_CONTROLS")
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = []
    for name,module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if location and Path(location).is_relative_to(SOURCE):
            imports.append({"name": name, **P.file_pin(Path(location))})
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "scope": "SYNTHETIC_LIFECYCLE_ONLY_NO_NATIVE_BUILD_GUEST_PROOF_OR_NETWORK",
        "synthetic_dispatches": DISPATCHES, "native_process_calls": 0, "imports": imports}
    save(OUTPUT/"RESULT.json", P.encoded(report)); print(P.encoded(report).decode(), end="", flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
