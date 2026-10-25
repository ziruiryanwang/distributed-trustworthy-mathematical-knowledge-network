"""Selected grounded-cut support and one actual conditional kernel event.

Source-only integration. No package is built/adopted by this module. A caller
must first load the existing exact ordinary profile and these exact new files
through its approved bootstrap. A conditional output is not local admission;
the separate protected controller owns grounding, freshness and atomic commit.
"""
from pathlib import Path
import hashlib
import math
import os
import time

import ordinary_evidence as E
import ordinary_semantics as S
import ordinary_admission as A
import local_catalog as C
import source_anchor as H


MIB = 1024 * 1024
SCHEMA = "DMKN_GROUNDED_CUT_BASIS_SUPPORT_V1"
DOMAIN = b"DMKN-GROUNDED-CUT-BASIS-SUPPORT-V1\0"
SOURCES = {"GroundedCut.lean", "GroundedCutDriver.lean", "cut_worker.py",
           "cut_runtime.py", "cut_controller.py", "source_anchor.py",
           "cut_map.py", "cut_summary.py", "cut_catalog.py", "cut_bootstrap.py"}
SUFFIXES = {".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig"}
OBJECTS = {"lean-lib/GroundedCut" + suffix for suffix in SUFFIXES}


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_RUNTIME_" + code)


class UncertainWorker(ValueError):
    """Child-tree cleanup was not confirmed; controller must quarantine its store."""


class CutRuntime:
    @classmethod
    def open(cls, addition_root, expected_manifest_sha256, base, *, check):
        need(callable(check) and type(base.installation) is A.NativeInstallation,
             "APPROVED_ORDINARY_BASE_REQUIRED")
        check()
        root = C.ordinary(addition_root, directory=True)
        raw = C.read_bounded(root / "CUT-SUPPORT.json", 2 * MIB)
        need(hashlib.sha256(raw).hexdigest() == C.hexid(expected_manifest_sha256), "SUPPORT_PIN")
        doc = E.strict_json(raw, E.Limits(max_bytes=2 * MIB))
        need(type(doc) is dict and set(doc) == {"schema", "base_profile_sha256", "files"}
             and doc["schema"] == SCHEMA, "SUPPORT_FIELDS")
        files = doc["files"]
        need(type(files) is dict and SOURCES | {"lean-lib/GroundedCut.olean"} <= set(files)
             <= SOURCES | OBJECTS, "PAYLOAD_CENSUS")
        for name, pin in files.items():
            need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
                 type(pin["bytes"]) is int and 0 < pin["bytes"] <= 64 * MIB, "PAYLOAD_PIN")
            C.hexid(pin["sha256"])
        base_raw = C.read_bounded(base.root / "PROFILE.json", 2 * MIB)
        need(hashlib.sha256(base_raw).hexdigest() == C.hexid(doc["base_profile_sha256"]), "BASE_PROFILE_PIN")
        need(Path(__file__).resolve() == root / "cut_runtime.py", "RUNNING_RUNTIME_SOURCE")
        for left, right in [(root, base.root)] + [
                (root, path) for path in base.installation.runtime_roots.values()]:
            need(not left.is_relative_to(right) and not right.is_relative_to(left), "SUPPORT_OVERLAP")
        self = cls.__new__(cls)
        self.root, self.base, self.manifest_raw, self.manifest_sha = root, base, raw, expected_manifest_sha256
        self.files, self.support_id = files, hashlib.sha256(DOMAIN + raw).hexdigest()
        self.semantic_id, self.foundation_id = S.semantic_id(), S.foundation_id()
        self.verify(check)
        return self

    def verify(self, check):
        check()
        need(C.read_bounded(self.root / "CUT-SUPPORT.json", 2 * MIB) == self.manifest_raw,
             "SUPPORT_CHANGED")
        self.base.profile.verify(check)
        need(self.base.installation.semantic_id == self.semantic_id, "BASE_SEMANTICS")
        # Fixed local support cost, independent of theorem-history size.
        for name, pin in self.files.items():
            check()
            raw = C.read_bounded(self.root / name, 64 * MIB)
            need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
                 "PAYLOAD_CHANGED:" + name)
        library = C.ordinary(self.root / "lean-lib", directory=True)
        expected = {Path(name).name for name in self.files if name.startswith("lean-lib/")}
        actual = set()
        for path in library.iterdir():
            check()
            C.ordinary(path)
            actual.add(path.name)
            need(len(actual) <= len(expected), "NATIVE_OBJECT_CENSUS")
        need(actual == expected, "NATIVE_OBJECT_CENSUS")
        check()

    def check_packet(self, packet_raw, call_directory, budget, *, anchor):
        """One clean fixed worker event, still conditional on caller grounding.

        `budget` is the original claimed OperationBudget. No re-claim, retry or
        fallback occurs here. Files must be in a fresh disjoint local call folder.
        The caller packet has no snapshot field: the held authenticated anchor
        alone supplies it. Return the actual augmented request bytes for commit
        identity. A conditional report is never a protected local warrant.
        """
        need(type(budget) is A.OperationBudget and type(anchor) is H.SourceAnchor,
             "BUDGET_AND_SOURCE_ANCHOR_TYPES")
        anchor.check()
        need(anchor._doc["implementation_id"] == self.base.installation.implementation_id,
             "BASIS_IMPLEMENTATION")
        budget.check()
        self.verify(budget.check)
        packet = E.strict_json(packet_raw, E.Limits(max_bytes=64 * MIB))
        need(len(packet_raw) + 18 * MIB + 2 * budget.log_bytes + 128 * 1024 <=
             budget.output_bytes, "COMPLETE_CALL_SPOOL_BOUND")
        need(type(packet) is dict and set(packet) == {"schema", "request_id", "concrete_units",
             "signature_rows", "new_unit"} and packet["schema"] == "DMKN_GROUNDED_CUT_BASIS_REQUEST_V1",
             "REQUEST_FIELDS")
        C.hexid(packet["request_id"])
        # No caller snapshot field is accepted. Authenticate once, under the
        # controller's held source/cut locks, before any native deserialization.
        snapshot = anchor.basis_snapshot()
        need(len(E.canonical_json(snapshot)) + 32 <= 256 * 1024,
             "SNAPSHOT_DESCRIPTOR_BOUND")
        packet["basis_snapshot"] = snapshot
        packet_raw = E.canonical_json(packet)
        need(len(packet_raw) <= 64 * MIB and
             len(packet_raw) + 18 * MIB + 2 * budget.log_bytes + 128 * 1024 <=
             budget.output_bytes, "AUTHENTICATED_PACKET_BOUND")
        call = C.ordinary(call_directory, directory=True, fresh=True)
        for support in (self.root, self.base.root, *self.base.installation.runtime_roots.values()):
            need(not call.is_relative_to(support) and not support.is_relative_to(call), "CALL_SUPPORT_OVERLAP")
        call.mkdir()
        request, report_path = call / "request.json", call / "report.json"
        self.base.A.P.PortableCatalog._write_fresh(request, packet_raw)
        installation = self.base.installation
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(self.root / "cut_worker.py"),
                str(self.root), str(self.base.root), str(installation.runtime_roots["python_runtime"]),
                str(installation.runtime_roots["lean_runtime"]), self.manifest_sha, str(request), str(report_path)]
        supervisor, job = installation._supervisor, installation._job_module
        remaining = math.floor(budget.deadline - time.monotonic())
        need(remaining > 0, "DEADLINE")
        allowance = supervisor.limits_checked(budget.allowance(budget.deadline))
        observation = None
        anchor.check()  # A pre-launch refusal does not imply an uncertain child.
        try:
            observation = supervisor.supervise(argv, call, call / "supervision", allowance, job.Job)
        finally:
            # A report cannot make an uncertain live child safe to ignore.
            closed = type(observation) is dict and observation.get("job_closed") is True and \
                observation.get("direct_child_reaped") is True and observation.get("cleanup_errors") == [] and \
                type(observation.get("final_job")) is dict and observation["final_job"].get("active_processes") == 0
            if not closed:
                raise UncertainWorker("GROUNDED_RUNTIME_CLEANUP_UNCERTAIN")
        supervisor.save_new(call / "observation.json", observation)
        final = observation["final_job"]
        if type(final.get("cpu_seconds")) in (int, float):
            budget.worker_cpu += final["cpu_seconds"]
        need(A._clean_worker(observation), "CONDITIONAL_CHECK_NOT_CLEAN")
        need(C.ordinary(call / "supervision/stderr.txt").stat().st_size == 0, "WORKER_STDERR")
        anchor.check()
        budget.check()
        need(C.read_bounded(request, 64 * MIB) == packet_raw, "REQUEST_CHANGED")
        report_raw = C.read_bounded(report_path, 16 * MIB)
        report = A._writer_json(report_raw, 16 * MIB)
        need(type(report) is dict and set(report) == {"schema", "assurance", "request_id",
             "theorem_name", "theorem_inventory", "signature_labels", "counts"}, "REPORT_FIELDS")
        need(report["schema"] == "DMKN_GROUNDED_CUT_BASIS_CONDITIONAL_OUTPUT_V1" and
             report["assurance"] == "CONDITIONAL_KERNEL_JUDGMENT_NOT_LOCAL_WARRANT" and
             report["request_id"] == packet["request_id"], "REPORT_BINDING")
        unit = packet["new_unit"]
        need(len(unit[2]) == 1 and report["theorem_name"] == unit[2][0][0] and
             report["theorem_inventory"] == unit[2][0] and
             report["signature_labels"] == [[row[0], row[2]] for row in packet["signature_rows"]],
             "ACTUAL_INVENTORY_BINDING")
        counts = report["counts"]
        expected_counts = {"concrete_units", "concrete_names", "signatures", "scratch_names",
                           "input_bytes", "basis_artifact_bytes", "encoded_nodes",
                           "scan_nodes", "kernel_calls"}
        need(type(counts) is dict and set(counts) == expected_counts and
             all(type(value) is int and 0 <= value <= (1 << 64) - 1
                 for value in counts.values()) and
             counts["basis_artifact_bytes"] == snapshot["artifact_bytes"] and
             counts["concrete_units"] == len(packet["concrete_units"]) and
             counts["signatures"] == len(packet["signature_rows"]) and
             counts["kernel_calls"] == len(packet["concrete_units"]) +
                 2 * len(packet["signature_rows"]) + 2, "ACTUAL_COST_BINDING")
        self.verify(budget.check)
        anchor.check()
        budget.check()
        # Observation is returned from THIS live call, never reread as permission.
        return report_raw, observation, packet_raw
