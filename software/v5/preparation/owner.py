"""Bounded owner preparation over the existing native frontend and module host.

The controller never creates verification handles, runs a proof, or fetches data.
Owner code/files/OS are trusted. Jobs supervise resources, not hostile code.
"""
from __future__ import annotations

from copy import deepcopy
import math
import os
from pathlib import Path
import re
import struct
import time

from authoring.source import SourceOperation
from modules import codec as C
from modules.receipt.witness import decode_journal
from production.producer import (Producer, MIB, fields, uint, number, digest,
    encoded, parse, file_pin, pin_fields, hash_bytes, require, clean, closure_known)

SCHEMA = "DMKN_V5_PREPARATION_PROFILE_V1"
REQUIRED_SOURCES = (
    "preparation/owner.py", "preparation/__init__.py", "authoring/worker.py",
    "authoring/source.py", "authoring/context.py", "authoring/imports.py",
    "modules/codec.py", "modules/model.py", "modules/source_rows.py",
    "modules/native_rows.py", "modules/receipt/witness.py",
)
CHILD_FIELDS = ("status", "input", "parent_receipts", "source_sha256", "roots",
    "local_module", "local_groups", "parent_selection_binding", "mathematical_acceptance")


class OwnerPreparation:
    """One serialized owner, fresh evidence root, and nonrenewable allowance.

    Constructor and lifetime owner-process CPU are observed inclusively. Thus
    unrelated owner work while this object lives is conservatively included.
    Across restart no authority or allowance is reconstructed from saved JSON.
    Any failed operation closes this instance; demands are ordinary nonfailures.
    """
    def __init__(self, profile, allowance, output_directory):
        self._started, self._cpu_started = time.monotonic(), time.process_time()
        self._closed = self._busy = False
        self._calls, self._worker_charge = 0, 0.0
        self._unknown = False
        self._history, self._last_failure = [], None
        fields(allowance, ("allowance_id", "operations", "worker_cpu_seconds",
            "controller_cpu_seconds", "wall_seconds", "output_bytes", "output_entries"))
        digest(allowance["allowance_id"])
        for name, cap, low in (("operations", 16, 1), ("worker_cpu_seconds", 3600, 1),
                ("controller_cpu_seconds", 600, 1), ("wall_seconds", 3600, 1),
                ("output_bytes", 1024*MIB, 128*MIB), ("output_entries", 4096, 32)):
            uint(allowance[name], cap, low)
        self._allowance = parse(encoded(allowance))
        self._deadline = self._started + allowance["wall_seconds"]
        fields(profile, ("schema", "producer", "image", "worker", "native_executable",
            "lean_root", "lean_runtime_pins", "source_pins"))
        require(profile["schema"] == SCHEMA, "PREPARATION_PROFILE_SCHEMA")
        self._profile = parse(encoded(profile))
        self._profile_raw = encoded(self._profile)
        require(len(self._profile_raw) <= MIB, "PREPARATION_PROFILE_BYTES")
        # Reuse only this adopted loader/pinning/supervision implementation.
        # Producer.run is never called, and no producer allowance is created.
        self._P = Producer(self._profile["producer"])
        self._A, self._Job = self._P._A, self._P._Job
        self._pins = deepcopy(self._P._pins)
        p = self._profile
        self._lean_root = self._A.absolute(p["lean_root"], directory=True)
        require((self._lean_root/"bin").is_dir() and (self._lean_root/"lib/lean").is_dir(),
                "PREPARATION_LEAN_RUNTIME_LAYOUT")
        require(type(p["lean_runtime_pins"]) is list and 1 <= len(p["lean_runtime_pins"]) <= 128,
                "PREPARATION_LEAN_PIN_COUNT")
        for row in p["lean_runtime_pins"]:
            path = pin_fields(row)
            require(path.is_relative_to(self._lean_root), "PREPARATION_LEAN_PIN_ROOT")
        lean_paths = [pin_fields(row) for row in p["lean_runtime_pins"]]
        required_dlls = {"libInit_shared.dll", "libleanshared.dll", "libleanshared_1.dll",
                         "libleanshared_2.dll", "libc++.dll"}
        require(len(lean_paths) == len(set(lean_paths))
                and {self._lean_root/"bin"/name for name in required_dlls} <= set(lean_paths),
                "PREPARATION_LEAN_REQUIRED_PINS")
        sources = p["source_pins"]
        require(type(sources) is list and 1 <= len(sources) <= 128, "PREPARATION_SOURCE_PIN_COUNT")
        base = Path(__file__).resolve().parents[1]
        require({base / name for name in REQUIRED_SOURCES} <= {pin_fields(row) for row in sources},
                "PREPARATION_REQUIRED_SOURCE_PINS")
        require(pin_fields(p["worker"]) == base / "authoring/worker.py", "PREPARATION_WORKER_ORIGIN")
        pin_fields(p["worker"], 2*MIB); pin_fields(p["image"], 64*MIB)
        require(pin_fields(p["native_executable"], 64*MIB).suffix.lower() == ".exe",
                "PREPARATION_NATIVE_EXECUTABLE")
        for row in (p["image"], p["worker"], p["native_executable"], *sources, *p["lean_runtime_pins"]):
            self._P._add_pin(self._pins, row)
        require(sum(row["bytes"] for row in self._pins.values()) <= 512*MIB,
                "PREPARATION_TOTAL_PIN_BYTES")
        self._controls = {}
        self._check()
        self._output = self._A.absolute(output_directory, directory=True, fresh=True)
        for protected in (self._P._install, self._lean_root, *map(Path, self._pins)):
            require(not self._A.overlap(self._output, protected), "PREPARATION_OUTPUT_OVERLAP")
        self._output.mkdir()
        self._save(self._output/"profile.json", p)
        self._save(self._output/"allowance.json", self._allowance)
        self._controls = {str(path): file_pin(path) for path in
                          (self._output/"profile.json", self._output/"allowance.json")}
        self._active()
        self._census()

    def _active(self):
        require(not self._closed and not self._unknown, "PREPARATION_CLOSED_OR_UNCERTAIN")
        require(time.monotonic() < self._deadline, "PREPARATION_ORIGINAL_DEADLINE")
        require(time.process_time()-self._cpu_started <= self._allowance["controller_cpu_seconds"],
                "PREPARATION_CONTROLLER_CPU")

    def _check(self, extra=None):
        self._active()
        require(encoded(self._profile) == self._profile_raw, "PREPARATION_PROFILE_CHANGED")
        self._P._check(self._pins)
        self._P._check(self._controls)
        if extra:
            self._P._check(extra)
        self._active()

    def _save(self, path, value):
        raw = encoded(value)
        require(len(raw) <= MIB, "PREPARATION_REPORT_BYTES")
        self._write(path, raw)

    @staticmethod
    def _write(path, raw):
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def _census(self):
        total, entries = 0, 0
        for path in self._output.rglob("*"):
            entries += 1
            require(entries <= self._allowance["output_entries"], "PREPARATION_OUTPUT_ENTRIES")
            self._A.absolute(path, directory=path.is_dir())
            if path.is_file():
                total += path.stat().st_size
                require(total <= self._allowance["output_bytes"], "PREPARATION_OUTPUT_BYTES")
        return total, entries

    def _space(self, extra_bytes, extra_entries):
        self._active()
        total, entries = self._census()
        require(total+extra_bytes <= self._allowance["output_bytes"]
                and entries+extra_entries <= self._allowance["output_entries"],
                "PREPARATION_OUTPUT_RESERVATION")

    def report(self):
        return {"allowance_id": self._allowance["allowance_id"], "calls": self._calls,
            "worker_cpu_charge": self._worker_charge, "unknown_worker_accounting": self._unknown,
            "controller_cpu_seconds": time.process_time()-self._cpu_started,
            "wall_seconds": time.monotonic()-self._started, "closed": self._closed,
            "history": deepcopy(self._history), "last_failure": deepcopy(self._last_failure),
            "scope": "OWNER_LIFETIME_CPU_INCLUSIVE_AND_PRE_REPORT_WALL;FINAL_WRITE_EXIT_TAILS_EXCLUDED",
            "mathematical_acceptance": False}

    def _limits(self, cpu_seconds, wall_seconds, memory_mib, deadline):
        uint(cpu_seconds, 1200, 1); uint(wall_seconds, 600, 1); uint(memory_mib, 4096, 64)
        effective = min(self._deadline, deadline, time.monotonic()+wall_seconds)
        remaining = math.floor(effective-time.monotonic())
        require(remaining >= 1, "PREPARATION_STAGE_DEADLINE")
        limits = self._A.limits_checked({"cpu_seconds": cpu_seconds, "wall_seconds": remaining,
            "memory_mib": memory_mib, "active_processes": 2,
            "stdout_bytes": MIB, "stderr_bytes": MIB})
        return limits, effective

    def _stage(self, directory, name, argv, limits, deadline, pins, storage):
        self._check(pins)
        self._space(*storage)
        require(time.monotonic() < deadline, "PREPARATION_STAGE_DEADLINE")
        remaining = math.floor(min(self._deadline, deadline)-time.monotonic())
        require(remaining >= 1, "PREPARATION_STAGE_DEADLINE")
        limits = {**limits, "wall_seconds": min(limits["wall_seconds"], remaining)}
        reserved = limits["cpu_seconds"]
        require(self._worker_charge+reserved <= self._allowance["worker_cpu_seconds"],
                "PREPARATION_WORKER_RESERVATION")
        self._save(directory/(name+"-reservation.json"), {"allowance_id": self._allowance["allowance_id"],
            "stage": name, "argv": argv, "limits": limits, "deadline_monotonic": deadline,
            "worker_cpu_reserved": reserved, "worker_charge_before": self._worker_charge,
            "output_reserved_bytes": storage[0], "output_reserved_entries": storage[1]})
        # Reservation is durable before ANY process can start. Unknown outcome
        # retains it; it is bookkeeping, not a proved total-CPU upper bound.
        self._worker_charge += reserved
        try:
            self._active()
            result = self._A.supervise(argv, self._P._install, directory/(name+"-command"),
                                       limits, self._Job)
        except BaseException:
            self._unknown = self._closed = True
            raise
        reliable = closure_known(result)
        try:
            actual = number(result["final_job"]["cpu_seconds"]) if reliable else None
        except (ValueError, KeyError, TypeError):
            reliable, actual = False, None
        if reliable:
            self._worker_charge += actual-reserved
        else:
            self._unknown = self._closed = True
        self._history.append({"operation": directory.name, "stage": name,
            "reserved_cpu": reserved, "charged_cpu": actual if reliable else reserved,
            "closure_accounting_known": reliable})
        self._save(directory/(name+"-process.json"), result)
        self._save(directory/(name+"-settlement.json"), self._history[-1])
        require(reliable, "PREPARATION_UNKNOWN_CLOSURE_OR_ACCOUNTING")
        require(clean(result), "PREPARATION_COMMAND_FAILED_OR_DIRTY")
        require(actual <= reserved and self._worker_charge <= self._allowance["worker_cpu_seconds"],
                "PREPARATION_WORKER_OVERSHOOT")
        self._check(pins)
        self._census()
        require(time.monotonic() < deadline, "PREPARATION_STAGE_DEADLINE")
        return result

    def _call(self, kind, name, work):
        require(not self._busy, "PREPARATION_SINGLE_OWNER")
        directory = None
        self._busy = True
        try:
            self._active()
            require(self._calls < self._allowance["operations"], "PREPARATION_OPERATION_LIMIT")
            self._calls += 1
            require(type(name) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name),
                    "PREPARATION_OPERATION_NAME")
            directory = self._A.absolute(self._output/name, directory=True, fresh=True)
            self._space(MIB, 4)
            directory.mkdir()
            self._save(directory/"operation.json", {"kind": kind, "name": name,
                "allowance_id": self._allowance["allowance_id"], "original_deadline_monotonic": self._deadline})
            result = work(directory)
            completion = result.pop("_completion", None)
            self._check()
            if completion is not None: completion()
            self._save(directory/"RESULT.json", {"status": result["status"], "kind": kind,
                "accounting": self.report(), "mathematical_acceptance": False})
            self._active(); self._census()
            public = {**result, "evidence": str(directory), "accounting": self.report()}
            if completion is not None: completion()
            self._active()
            return public
        except BaseException as error:
            self._closed = True
            self._last_failure = {"kind": kind, "error_type": type(error).__name__,
                "message": str(error)[:2000], "accounting_unknown": self._unknown}
            failure = {"status": "FAIL_OWNER_RECOVERY_REQUIRED", **self._last_failure,
                       "accounting": self.report(), "mathematical_acceptance": False}
            try:
                if directory is not None and directory.is_dir():
                    target = directory/("FINALIZATION-FAILED.json" if (directory/"RESULT.json").exists() else "RESULT.json")
                else:
                    target = self._output/("failure-"+str(self._calls)+".json")
                self._save(target, failure)
            except BaseException:
                self._last_failure["durable_failure_report_written"] = False
            raise
        finally:
            self._busy = False

    def author(self, operation, name, *, cpu_seconds, wall_seconds, memory_mib=2048):
        """Run exactly one owner-selected source, keeping its live origin intact."""
        entered = time.monotonic()
        def work(directory):
            uint(cpu_seconds, 1200, 1); uint(wall_seconds, 600, 1); uint(memory_mib, 4096, 64)
            call_deadline = min(self._deadline, entered+wall_seconds)
            require(time.monotonic() < call_deadline, "PREPARATION_AUTHOR_TOTAL_WALL")
            require(type(operation) is SourceOperation, "PREPARATION_EXACT_SOURCE_OPERATION")
            operation._active()
            original_session, original_verifier = operation._origin_session, operation._origin_verifier
            original_deadline = operation._deadline
            def source_live():
                require(operation._origin_session is original_session
                    and operation._origin_verifier is original_verifier and operation._deadline == original_deadline,
                    "PREPARATION_SOURCE_ORIGIN_CHANGED")
                operation._active()
                require(time.monotonic() < min(call_deadline, original_deadline), "PREPARATION_AUTHOR_TOTAL_WALL")
            p = self._profile["producer"]
            require((original_verifier._image, original_verifier._foundation, original_verifier._policy)
                    == (p["image_id"], p["foundation"], p["policy"]), "PREPARATION_SOURCE_PROFILE")
            ready = operation.prepare()
            if ready["status"] == "NEED_AUTHORING_CONTEXT_DATA":
                return {**deepcopy(ready), "_completion": source_live}
            require(ready["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION"
                    and ready["mathematical_acceptance"] is False, "PREPARATION_SOURCE_READY")
            raw = ready["request"]
            require(type(raw) is bytes and 0 < len(raw) <= 16*MIB
                    and hash_bytes(raw) == ready["request_sha256"], "PREPARATION_SOURCE_REQUEST")
            limits, deadline = self._limits(cpu_seconds, wall_seconds, memory_mib, min(call_deadline, original_deadline))
            # Native frontend may write64MiB NDJSON AND16MiB EXPORT plus logs.
            self._space(len(raw)+96*MIB, 16)
            request = directory/"source-request.json"
            self._write(request, raw)
            config = {"schema": "DMKN_OWNER_LEAN_WORKER_V1", "worker": self._profile["worker"],
                "executable": self._profile["native_executable"], "lean_root": str(self._lean_root),
                "runtime_pins": deepcopy(self._profile["lean_runtime_pins"]), "request": file_pin(request),
                "output_directory": str(directory/"frontend"), "report_path": str(directory/"worker-result.json"),
                "deadline_monotonic": deadline}
            control = directory/"worker-config.json"
            require(len(encoded(config)) <= 128*1024, "PREPARATION_WORKER_CONFIG_BYTES")
            self._save(control, config)
            config_pin = file_pin(control)
            pins = {str(request): file_pin(request), str(control): config_pin}
            argv = [p["python"]["path"], "-I", "-S", "-B", self._profile["worker"]["path"],
                    "--config", str(control), "--config-sha256", config_pin["sha256"]]
            self._stage(directory, "author", argv, limits, deadline, pins, (96*MIB, 16))
            source_live()
            report = parse(self._A.bounded_read(directory/"worker-result.json", MIB))
            export = self._A.bounded_read(directory/"frontend/EXPORT.json", 16*MIB)
            require(report.get("schema") == "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
                and report.get("status") == "PASS_NATIVE_EXPORT_ONLY"
                and report.get("request_sha256") == pins[str(request)]["sha256"]
                and report.get("executable_sha256") == self._profile["native_executable"]["sha256"]
                and report.get("config_sha256") == config_pin["sha256"]
                and report.get("worker_sha256") == self._profile["worker"]["sha256"]
                and report.get("export_sha256") == hash_bytes(export) and report.get("export_bytes") == len(export)
                and report.get("deadline_monotonic") == deadline and report.get("mathematical_acceptance") is False
                and report.get("native_return_code") == 0 and report.get("native_timed_out") is False
                and report.get("direct_child_reaped") is True and report.get("outer_job_closure_required") is True,
                "PREPARATION_WORKER_RETURN_BINDING")
            child = operation.finish(export)
            self._check(pins)
            operation._active()
            require(time.monotonic() < deadline, "PREPARATION_AUTHOR_TOTAL_WALL")
            return {"status": "UNTRUSTED_CHILD_REQUEST_PREPARED", "child": child,
                "export": file_pin(directory/"frontend/EXPORT.json"), "mathematical_acceptance": False,
                "_completion": source_live}
        return self._call("author", name, work)

    def _child(self, child):
        """Structural handoff only. The host rechecks genuine parent receipts."""
        child = deepcopy(child)
        fields(child, CHILD_FIELDS)
        require(child["status"] == "UNTRUSTED_PROVER_REQUEST_NOT_CHILD_ADMISSION"
                and child["mathematical_acceptance"] is False, "PREPARATION_UNTRUSTED_CHILD_REQUIRED")
        digest(child["source_sha256"]); digest(child["parent_selection_binding"])
        require(type(child["roots"]) is list and 1 <= len(child["roots"]) <= 64, "PREPARATION_CHILD_ROOTS")
        for root in child["roots"]: C.validate_name(root)
        value = child["input"]
        fields(value, ("schema", "image", "rank", "local_spec", "rows", "parents", "bodies"))
        p = self._profile["producer"]
        image_bytes = bytes.fromhex(p["image_id"])
        words = [int.from_bytes(image_bytes[i:i+4], "little") for i in range(0, 32, 4)]
        require(value["schema"] == "DMKN_CERTIFIED_MODULES_V2" and value["image"] == words,
                "PREPARATION_CHILD_PROFILE2_IMAGE")
        summary = C.summarize(value["local_spec"])
        module = C.summary_id(summary)
        require(summary["foundation"] == p["foundation"] and summary["policy"] == p["policy"]
                and child["local_module"] == module and child["local_groups"] == summary["group_count"],
                "PREPARATION_CHILD_SUMMARY")
        parents, receipts = value["parents"], child["parent_receipts"]
        require(type(parents) is list and type(receipts) is list and len(parents) == len(receipts) <= 8,
                "PREPARATION_EXACT_PARENT_COUNT")
        owners, ranks, total = [], [], 0
        for parent, receipt in zip(parents, receipts):
            fields(parent, ("journal", "openings")); fields(receipt, ("module", "journal", "receipt"))
            require(type(parent["journal"]) is list and len(parent["journal"]) == 184,
                    "PREPARATION_PARENT_JOURNAL")
            for byte in parent["journal"]: uint(byte, 255)
            raw = bytes(parent["journal"])
            parsed = decode_journal(raw)
            require(type(receipt["journal"]) is bytes and receipt["journal"] == raw
                    and receipt["module"] == parsed["module"] and parsed["module"] != module
                    and parsed["image"] == words and parsed["foundation"] == p["foundation"]
                    and parsed["policy"] == p["policy"], "PREPARATION_PARENT_BINDING")
            require(type(receipt["receipt"]) is bytes and 0 < len(receipt["receipt"]) <= 64*MIB,
                    "PREPARATION_PARENT_RECEIPT_BYTES")
            total += len(receipt["receipt"])
            require(type(parent["openings"]) is list and 1 <= len(parent["openings"]) <= 4096,
                    "PREPARATION_PARENT_OPENINGS")
            indices = []
            for opening in parent["openings"]:
                C.verify_group_opening(parsed["module"], opening)
                require(opening["summary"] == parsed["summary"], "PREPARATION_PARENT_SUMMARY")
                indices.append(opening["index"])
            require(len(indices) == len(set(indices)), "PREPARATION_DUPLICATE_PARENT_GROUP")
            owners.append(parsed["module"]); ranks.append(parsed["rank"])
        require(owners == sorted(set(owners)), "PREPARATION_EXACT_ORDERED_DISTINCT_PARENTS")
        uint(value["rank"], 2**64-1)
        require(value["rank"] == (max(ranks)+1 if ranks else 0), "PREPARATION_EXACT_CHILD_RANK")
        raw = C.canonical(value)
        require(0 < len(raw) <= 16*MIB and total+len(raw)+4+self._profile["image"]["bytes"]+184 <= 512*MIB,
                "PREPARATION_HOST_INPUT_BYTES")
        return child, raw, summary, words, total

    def snapshot(self, child, name, *, cycles, po2, prepare_cpu_seconds=30,
                 prepare_wall_seconds=60, cpu_seconds=240, wall_seconds=300, memory_mib=2048):
        """One actual parent-aware execution; returns an untrusted Producer session."""
        entered = time.monotonic()
        def work(directory):
            uint(cycles, 2**28, 1); uint(po2, 20, 12)
            uint(cpu_seconds, 1200, 1); uint(wall_seconds, 600, 1)
            deadline = min(self._deadline, entered+wall_seconds)
            def completed_in_time():
                require(time.monotonic() < deadline, "PREPARATION_SNAPSHOT_TOTAL_WALL")
            completed_in_time()
            selected, raw, summary, words, parent_bytes = self._child(child)
            first, deadline1 = self._limits(prepare_cpu_seconds, prepare_wall_seconds, memory_mib, self._deadline)
            uint(prepare_cpu_seconds, 60, 1)
            # The complete two-command snapshot operation shares one wall cap.
            uint(wall_seconds, 600, 1)
            deadline1 = min(deadline1, deadline)
            self._space(parent_bytes+2*len(raw)+72*MIB, 30+len(selected["parent_receipts"]))
            input_path = directory/"child-input.json"
            self._write(input_path, raw)
            pins = {str(input_path): file_pin(input_path)}
            parent_pins = []
            for i, parent in enumerate(selected["parent_receipts"]):
                path = directory/("parent-"+str(i)+".receipt")
                self._write(path, parent["receipt"])
                row = file_pin(path); parent_pins.append(row); pins[str(path)] = row
            frame, expected = directory/"child.frame", directory/"child.expected-journal"
            p = self._profile
            host, image = p["producer"]["host"]["path"], p["image"]["path"]
            self._stage(directory, "prepare", [host, "prepare", image, str(input_path), str(frame), str(expected)],
                first, deadline1, pins, (len(raw)+8*MIB, 12))
            framed = self._A.bounded_read(frame, 16*MIB+4)
            require(framed == struct.pack("<I", len(raw))+raw, "PREPARATION_EXACT_FRAME")
            journal = self._A.bounded_read(expected, 184)
            parsed = decode_journal(journal)
            require(parsed["summary"] == summary and parsed["image"] == words
                    and parsed["module"] == selected["local_module"]
                    and parsed["rank"] == selected["input"]["rank"], "PREPARATION_EXACT_EXPECTED_JOURNAL")
            prepared = parse(self._A.bounded_read(directory/"prepare-command/stdout.txt", MIB))
            require(prepared == {"status": "PREPARED_ONLY_NOT_CERTIFIED", "image": words,
                "module": selected["local_module"], "rank": selected["input"]["rank"],
                "mathematical_admission": False}, "PREPARATION_HOST_PREPARE_REPLY")
            pins[str(frame)] = file_pin(frame); pins[str(expected)] = file_pin(expected)
            second, effective = self._limits(cpu_seconds, wall_seconds, memory_mib, deadline)
            capsule = directory/"child.snapshot"
            argv = [host, "stage", image, str(frame), str(expected), str(cycles), str(po2), "snapshot", "0",
                    str(capsule), str(len(parent_pins)), *[row["path"] for row in parent_pins]]
            self._stage(directory, "snapshot", argv, second, effective, pins, (72*MIB, 12))
            text = self._A.bounded_read(directory/"snapshot-command/stdout.txt", MIB).decode("utf-8").strip()
            match = re.fullmatch(r"REAL_EXECUTION_SNAPSHOT_NOT_APPLICATION_CERTIFICATE schema=(\d+) snapshot_bytes=(\d+) "
                r"segments=(\d+) assumptions=(\d+) binding=([0-9a-f]{64})", text)
            require(match is not None, "PREPARATION_SNAPSHOT_REPLY")
            schema, size, segments, assumptions = map(int, match.groups()[:4])
            require(schema == 3 and 0 < size <= 64*MIB and 1 <= segments <= 128
                    and assumptions == len(parent_pins), "PREPARATION_SNAPSHOT_CENSUS")
            capsule_pin = file_pin(capsule)
            require(capsule_pin["bytes"] == size, "PREPARATION_CAPSULE_SIZE")
            with capsule.open("rb") as stream:
                require(stream.read(4) == struct.pack("<I", 3), "PREPARATION_CAPSULE_SCHEMA")
            self._check(pins)
            session = {"image": deepcopy(p["image"]), "frame": pins[str(frame)], "expected": pins[str(expected)],
                "capsule": capsule_pin, "parents": parent_pins, "binding": match[5], "cycles": cycles,
                "po2": po2, "segments": segments, "assumptions": assumptions}
            self._save(directory/"producer-session.json", session)
            return {"status": "UNTRUSTED_PROVER_CAPSULE_PREPARED", "session": session,
                "local_module": selected["local_module"], "mathematical_acceptance": False,
                "_completion": completed_in_time}
        return self._call("snapshot", name, work)

    def close(self):
        require(not self._busy, "PREPARATION_ACTIVE_CALL")
        self._closed = True
        self._P.close()
        target = self._output/"CLOSED.json"
        if not target.exists():
            self._save(target, {"status": "CLOSED_NO_HANDLE_AUTHORITY", "accounting": self.report()})
