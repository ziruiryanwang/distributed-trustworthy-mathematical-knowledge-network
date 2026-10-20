"""One-shot, owner-local complete-DAG native acceptance; no receipt authority.

Configuration/code/OS are trusted. Windows Jobs supervise resources, not hostile
code. A parent must reserve this suballocation once before constructing the
owner, pass its original remaining monotonic deadline, and account for all spent
work. No client-grant or semantic-authoring integration is implied by this API.
"""
from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys
import threading
import time

from aggregate_claims import bindings as B
from aggregate_claims import input as AI
from modules import codec as C
from . import binding as NB

MIB = 1024**2
NATIVE_PIN = (1801216, "2306e9f32292bdee6e6638a5f9c9cc9f1f9bc288c967a6443ec8862886e942c9")
SOURCE_NAMES = ("native_closure", "native_closure.binding", "native_closure.owner",
                "aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
                "admission", "admission.bindings", "modules", "modules.codec")


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def _load_supervision(manifest, raw):
    """Load adopted resource helpers only; never an old mathematical verifier."""
    held = C.parse_json(raw, C.Limits(max_bytes=8*MIB))
    C.require(type(held) is dict and type(held.get("files")) is dict, "NATIVE_OWNER_MANIFEST")
    pins = {}

    def load(name, relative):
        path = manifest.parent / relative
        pin = held["files"].get(relative)
        C.fields(pin, {"sha256", "bytes"}); C.digest_string(pin["sha256"])
        C.require(0 < C.uint(pin["bytes"], 4*MIB), "NATIVE_OWNER_HELPER_SIZE")
        C.require(path.is_file() and path.resolve() == path
                  and path.stat().st_size == pin["bytes"], "NATIVE_OWNER_HELPER_PATH")
        with path.open("rb") as stream:
            source = stream.read(pin["bytes"]+1)
        C.require(len(source) == pin["bytes"] and _sha(source) == pin["sha256"],
                  "NATIVE_OWNER_HELPER_PIN")
        pins[path] = dict(pin)
        if name in sys.modules:
            module = sys.modules[name]
            C.require(getattr(module, "_dmkn_admission_source_pin", None) == pin["sha256"]
                      and Path(getattr(module, "__file__", "")) == path, "NATIVE_OWNER_HELPER_COLLISION")
            return module
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            exec(compile(source, str(path), "exec"), module.__dict__)
        except BaseException:
            del sys.modules[name]
            raise
        module._dmkn_admission_source_pin = pin["sha256"]
        return module

    supervisor = load("_dmkn_v5_admission_supervisor", "operator/commons.py")
    load("domains", "receiver/helpers/domains.py")
    job = load("_dmkn_v5_admission_job", "receiver/helpers/run_stage.py").Job
    return supervisor, job, pins


class VerifiedNativeMember:
    """Opaque same-owner token; neither an I/A receipt nor a mixed-import token."""
    __slots__ = ()


class NativeClosureOwner:
    """One finite check, then bounded live member inspection; no retries/network."""
    def __init__(self, *, supervisor_manifest, supervisor_manifest_sha256,
                 executable, runtime_pins, adopted_image, deadline,
                 submitted_bytes, reserved_cpu_seconds, controller_cpu_seconds=30):
        C.require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
                  and sys.dont_write_bytecode and not sys.flags.optimize, "NATIVE_OWNER_ISOLATED_WINDOWS")
        self._started, self._cpu_started = time.monotonic(), time.process_time()
        C.require(_finite(deadline) and 0 < deadline-self._started <= 86400, "NATIVE_OWNER_ORIGINAL_DEADLINE")
        values = submitted_bytes, reserved_cpu_seconds, controller_cpu_seconds
        for value, cap in zip(values, (AI.MAX_BYTES, 600, 600)):
            C.require(0 < C.uint(value, cap), "NATIVE_OWNER_ALLOWANCE")
        B._adopted_image(adopted_image); C.digest_string(supervisor_manifest_sha256)
        self._deadline, self._caps, self._image = deadline, values, adopted_image
        self._thread = threading.current_thread()
        self._closed = self._busy = False
        self._used = [0, 0, 0]; self._observed_worker = 0.0; self._calls = 0
        self._handles, self._members, self._wire, self._bound = {}, (), None, None
        self._authority = None
        manifest = Path(supervisor_manifest)
        C.require(manifest.is_absolute() and manifest.is_file() and manifest.resolve() == manifest
                  and 0 < manifest.stat().st_size <= 8*MIB, "NATIVE_OWNER_MANIFEST_PATH")
        with manifest.open("rb") as stream:
            raw = stream.read(8*MIB+1)
        C.require(len(raw) <= 8*MIB and _sha(raw) == supervisor_manifest_sha256, "NATIVE_OWNER_MANIFEST_PIN")
        self._A, self._Job, loaded_pins = _load_supervision(manifest, raw)
        self._manifest = self._A.absolute(manifest)
        self._install = self._A.absolute(manifest.parent, directory=True)
        self._manifest_raw = raw
        C.require(type(runtime_pins) is dict and 1 <= len(runtime_pins) <= 128, "NATIVE_OWNER_RUNTIME_MAP")
        pins = dict(loaded_pins)
        for name, pin in runtime_pins.items():
            C.require(type(name) is str, "NATIVE_OWNER_RUNTIME_PATH")
            C.fields(pin, {"sha256", "bytes"}); C.digest_string(pin["sha256"])
            C.require(0 < C.uint(pin["bytes"], 128*MIB), "NATIVE_OWNER_RUNTIME_SIZE")
            path = self._A.absolute(name)
            C.require(path not in pins or pins[path] == pin, "NATIVE_OWNER_CONFLICTING_PIN")
            pins[path] = dict(pin)
        self._executable = self._A.absolute(executable)
        C.require(pins.get(self._executable) == {"bytes": NATIVE_PIN[0], "sha256": NATIVE_PIN[1]},
                  "NATIVE_OWNER_ADOPTED_EXECUTABLE")
        root = Path(__file__).resolve().parents[1]
        self._origins = tuple((name, root / (name.replace(".", "/") +
                              ("/__init__.py" if "." not in name else ".py"))) for name in SOURCE_NAMES)
        C.require({path for _, path in self._origins} <= set(pins), "NATIVE_OWNER_REQUIRED_SOURCE_PINS")
        C.require(sum(pin["bytes"] for pin in pins.values()) <= 512*MIB, "NATIVE_OWNER_PIN_TOTAL")
        self._pins = tuple(sorted((path, pin["bytes"], pin["sha256"]) for path, pin in pins.items()))
        self._profile_id = C.hash_value("native-complete-closure-owner-v1", {
            "manifest": supervisor_manifest_sha256, "native": NATIVE_PIN[1],
            "image": adopted_image, "foundation": B.FOUNDATION, "policy": B.POLICY,
            "pins": [[str(path), size, digest] for path, size, digest in self._pins],
            "limits": list(values)})
        self._origin_config = self._configuration()
        self._symbols = (NB.bind_output, AI.encode, B.member_journal, VerifiedNativeMember)
        self._check()

    def _configuration(self):
        return (self._A, self._Job, self._manifest, self._manifest_raw, self._install,
                self._pins, self._origins, self._executable, self._image, self._caps,
                self._deadline, self._profile_id, self._thread)

    def _revoke(self):
        self._closed = True; self._handles.clear(); self._members = ()
        self._wire = self._bound = None
        self._authority = None

    def _active(self):
        C.require(not self._closed and time.monotonic() < self._deadline, "NATIVE_OWNER_CLOSED_OR_EXPIRED")
        C.require(threading.current_thread() is self._thread, "NATIVE_OWNER_THREAD")
        C.require(time.process_time()-self._cpu_started <= self._caps[2], "NATIVE_OWNER_CONTROLLER_CPU")
        C.require(self._configuration() == self._origin_config, "NATIVE_OWNER_CONFIG_CHANGED")
        if self._authority is None:
            C.require(not self._handles and not self._members and self._wire is None and self._bound is None,
                      "NATIVE_OWNER_UNISSUED_STATE")
        else:
            wire, bound, members, handles = self._authority
            C.require(self._wire is wire and self._bound is bound and self._members is members
                      and tuple(self._handles.items()) == handles, "NATIVE_OWNER_MEMBERSHIP_CHANGED")

    def _check(self):
        try:
            self._active()
            for name, path in self._origins:
                module = sys.modules.get(name)
                C.require(module is not None and type(getattr(module, "__file__", None)) is str
                          and Path(module.__file__).resolve() == path, "NATIVE_OWNER_SOURCE_ORIGIN:"+name)
            C.require(NB is sys.modules["native_closure.binding"]
                      and AI is sys.modules["aggregate_claims.input"]
                      and B is sys.modules["aggregate_claims.bindings"] and C is sys.modules["modules.codec"]
                      and NB.B is B and NB.AI is AI and NB.C is C and AI.B is B and AI.C is C
                      and B.C is C and B.journal is sys.modules["admission.bindings"].journal
                      and NativeClosureOwner is sys.modules["native_closure.owner"].NativeClosureOwner
                      and all(a is b for a, b in zip(self._symbols,
                          (NB.bind_output, AI.encode, B.member_journal, VerifiedNativeMember))),
                      "NATIVE_OWNER_SYMBOL_ORIGIN")
            C.require(self._A is sys.modules.get("_dmkn_v5_admission_supervisor")
                      and self._Job is getattr(sys.modules.get("_dmkn_v5_admission_job"), "Job", None),
                      "NATIVE_OWNER_SUPERVISOR_ORIGIN")
            C.require(self._A.bounded_read(self._manifest, 8*MIB) == self._manifest_raw, "NATIVE_OWNER_MANIFEST_CHANGED")
            for path, size, digest in self._pins:
                self._active()
                C.require(self._A.pin(path) == {"bytes": size, "sha256": digest}, "NATIVE_OWNER_PIN_CHANGED")
            self._active()
        except BaseException:
            self._revoke()
            raise

    def _inspect(self):
        self._check()
        C.require(self._calls < 128, "NATIVE_OWNER_INSPECTION_LIMIT")
        self._calls += 1

    def _census(self, output):
        size = count = 0
        for directory, dirs, names in os.walk(output, followlinks=False):
            for name in dirs+names:
                self._active(); path = Path(directory)/name; count += 1
                self._A.absolute(path, directory=name in dirs)
                if name in names:
                    size += path.stat().st_size
                C.require(size <= 32*MIB and count <= 32, "NATIVE_OWNER_OUTPUT_LIMIT")

    @staticmethod
    def _clean(report, limits):
        C.require(type(report) is dict and type(report.get("final_job")) is dict, "NATIVE_OWNER_PROCESS_REPORT")
        final = report["final_job"]
        C.require(report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
                  and type(report.get("child_exit_code")) is int and report["child_exit_code"] == 0
                  and report.get("direct_child_reaped") is True and report.get("job_closed") is True
                  and report.get("cleanup_errors") == [] and report.get("termination_requested") is False
                  and type(final.get("active_processes")) is int and final["active_processes"] == 0
                  and type(final.get("terminated_processes")) is int and final["terminated_processes"] == 0,
                  "NATIVE_OWNER_UNCLEAN_OR_REFUSED")
        cost, wall = final.get("cpu_seconds"), report.get("wall_seconds_through_cleanup")
        C.require(_finite(cost) and 0 <= cost <= limits["cpu_seconds"]
                  and _finite(wall) and 0 <= wall <= limits["wall_seconds"], "NATIVE_OWNER_ACTUAL_LIMIT")
        return cost

    def check(self, witnesses, targets, operation_directory, *, cpu_seconds=30,
              wall_seconds=60, memory_mib=512):
        """Run once, then return same-owner tokens for every exact checked J."""
        started = time.monotonic()
        try:
            self._check()
            C.require(not self._busy and self._used[0] == 0, "NATIVE_OWNER_ONE_SHOT")
            for value, cap in ((cpu_seconds, 600), (wall_seconds, 600), (memory_mib, 4096)):
                C.require(0 < C.uint(value, cap), "NATIVE_OWNER_CALL_LIMIT")
            C.require(memory_mib >= 64, "NATIVE_OWNER_MEMORY_MINIMUM")
            C.require(cpu_seconds <= self._caps[1], "NATIVE_OWNER_RESERVED_BUDGET")
            # One owner thread; entry is consumed before any encoding or callback.
            self._busy = True
            self._used = [1, 0, cpu_seconds]
            C.require(type(witnesses) is list and 1 <= len(witnesses) <= AI.MAX_DELTAS
                      and all(type(raw) is bytes for raw in witnesses)
                      and type(targets) is list and 1 <= len(targets) <= len(witnesses),
                      "NATIVE_OWNER_INPUT_LISTS")
            submitted = 60+184*len(targets)+sum(4+len(raw) for raw in witnesses)
            self._used[1] = submitted
            C.require(submitted <= self._caps[0], "NATIVE_OWNER_RESERVED_BUDGET")
            # Encoding establishes no truth; it only prepares immutable exact input.
            wire = AI.encode(adopted_image=self._image, claims=[], frontiers=[],
                             witnesses=witnesses, targets=targets)
            targets = list(targets)
            C.require(len(wire) == submitted, "NATIVE_OWNER_ENCODED_LENGTH")
            limits = self._A.limits_checked({"cpu_seconds": cpu_seconds,
                "wall_seconds": min(wall_seconds, math.floor(self._deadline-started)),
                "memory_mib": memory_mib, "active_processes": 2,
                "stdout_bytes": NB.OUTPUT_BYTES, "stderr_bytes": 16384})
            output = self._A.absolute(operation_directory, directory=True, fresh=True)
            for protected in (self._install, self._manifest, *(row[0] for row in self._pins)):
                C.require(not self._A.overlap(output, protected), "NATIVE_OWNER_OUTPUT_OVERLAP")
            output.mkdir()
            received = output / "closure.bin"
            with received.open("xb") as stream:
                stream.write(wire); stream.flush(); os.fsync(stream.fileno())
            self._A.save_new(output / "request.json", {"profile_id": self._profile_id,
                "input_sha256": _sha(wire), "input_bytes": len(wire), "targets": [list(j) for j in targets],
                "limits": limits, "authority": "LOCAL_OPERATION_REQUEST_NOT_PROOF"})
            self._check()
            self._observed_worker = None  # An attempted launch without a usable report is unknown.
            process = self._A.supervise([str(self._executable), "check", str(received)],
                self._install, output / "command", limits, self._Job, started=started)
            final = process.get("final_job") if type(process) is dict else None
            cost = final.get("cpu_seconds") if type(final) is dict else None
            if _finite(cost) and cost >= 0:
                self._observed_worker = cost
            self._A.save_new(output / "process.json", process)
            self._clean(process, limits)
            self._check()
            C.require(self._A.bounded_read(received, AI.MAX_BYTES) == wire, "NATIVE_OWNER_INPUT_CHANGED")
            bound = NB.bind_output(self._A.bounded_read(output / "command/stdout.txt", NB.OUTPUT_BYTES),
                                   wire, targets, adopted_image=self._image)
            # Allocate all returned objects before the final pin/deadline checks.
            tokens = tuple(VerifiedNativeMember() for _ in bound["members"])
            handles = dict(zip(tokens, bound["members"]))
            self._A.save_new(output / "binding.json", {"status": "SAME_CALL_NATIVE_CLOSURE_BOUND",
                "profile_id": self._profile_id, "input_sha256": bound["input_sha256"],
                "members": len(tokens), "authority": "LOCAL_EVIDENCE_NOT_RECEIPT_OR_TRANSFERABLE_PROOF"})
            self._census(output); self._check()
            C.require(time.monotonic()-started <= limits["wall_seconds"], "NATIVE_OWNER_TOTAL_WALL_LIMIT")
            self._handles, self._members, self._wire = handles, tokens, wire
            self._bound = (bound["input_sha256"], bound["header"])
            self._authority = (wire, self._bound, tokens, tuple(handles.items()))
            return tokens
        except BaseException:
            self._revoke()
            raise
        finally:
            self._busy = False

    def describe(self, member):
        try:
            self._inspect()
            C.require(type(member) is VerifiedNativeMember and member in self._handles, "NATIVE_OWNER_FOREIGN_MEMBER")
            raw = self._handles[member]; decoded = B.member_journal(raw)
            result = {"journal": raw, "module": decoded["module"], "summary": decoded["summary"],
                "profile_id": self._profile_id, "input_sha256": self._bound[0],
                "proof_form": "NATIVE_COMPLETE_CLOSURE"}
            self._check()
            return result
        except BaseException:
            self._revoke()
            raise

    def members(self):
        try:
            self._inspect()
            C.require(self._wire is not None, "NATIVE_OWNER_NOT_CHECKED")
            result = self._members
            self._check()
            return result
        except BaseException:
            self._revoke()
            raise

    def report(self):
        """Operational data only; reading this can never establish/reopen authority."""
        return {"attempts": self._used[0], "submitted_bytes": self._used[1],
            "reserved_cpu_seconds": self._used[2], "observed_worker_cpu_seconds": self._observed_worker,
            "controller_cpu_seconds": time.process_time()-self._cpu_started,
            "live_handles": len(self._handles), "closed": self._closed, "profile_id": self._profile_id,
            "authority": "LOCAL_RESOURCE_ACCOUNTING_NOT_PROOF"}

    def close(self):
        C.require(not self._busy, "NATIVE_OWNER_CALL_ACTIVE")
        self._revoke()
