"""Owner-adopted, same-call bounded receipt verification (Windows adapter).

The owner-controlled Python process/installation/filesystem are trusted. This
is resource supervision, not a hostile-code security sandbox. Remote callers
may supply receipt bytes and expected mathematical identities, NOT this class's
constructor configuration. There is no API to load a saved acceptance report.
"""
from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys
import time

from modules import codec as C
from .bindings import JOURNAL_PROFILE, bind_output
from . import pin_phase as PP
from . import trust as T


def _sha(raw): return hashlib.sha256(raw).hexdigest()


class VerifiedModule:
    """An opaque local handle; only its originating live verifier can use it."""
    __slots__ = ()


class ReceiptVerifier:
    """One owner-thread instance with an aggregate finite operation budget.

    Imported trusted supervisor implementation is unchanged from its adopted
    release. Supply absolute owner paths and exact pins. No external service,
    proof ancestry or network request is made here. close() revokes all handles.
    """
    def __init__(self, *, supervisor_manifest, supervisor_manifest_sha256,
                 executable, runtime_pins, image_id, foundation, policy,
                 operations, submitted_bytes, reserved_cpu_seconds, wall_seconds, trust_binding):
        C.require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
                  and sys.dont_write_bytecode and not sys.flags.optimize, "ADMISSION_WINDOWS_ISOLATED_OWNER")
        for value in (supervisor_manifest_sha256, image_id, foundation, policy): C.digest_string(value)
        for value, cap in ((operations, 4096), (submitted_bytes, 1024**3),
                           (reserved_cpu_seconds, 86400), (wall_seconds, 86400)):
            C.require(0 < C.uint(value, cap), "ADMISSION_AGGREGATE_LIMIT")
        self._deadline = time.monotonic()+wall_seconds
        self._closed = False; self._busy = False; self._handles = {}
        self._trust_binding = self._trust_original_binding = trust_binding
        self._trust_module = T
        self._trust_origin = Path(__file__).resolve().parent / "trust.py"
        C.require(T is sys.modules.get("admission.trust")
            and type(getattr(T, "__file__", None)) is str
            and Path(T.__file__).resolve() == self._trust_origin,
            "ADMISSION_TRUST_SOURCE_ORIGIN")
        self._trust_identity = T.check_binding(trust_binding)
        self._trust_domain = trust_binding._domain
        self._caps = (operations, submitted_bytes, reserved_cpu_seconds)
        self._used = [0, 0, 0]
        self._image, self._foundation, self._policy = image_id, foundation, policy
        manifest = Path(supervisor_manifest)
        C.require(manifest.is_absolute() and manifest.is_file() and manifest.stat().st_size <= 8*1024**2,
                  "ADMISSION_SUPERVISOR_MANIFEST_PATH")
        raw = manifest.read_bytes()
        C.require(len(raw) <= 8*1024**2 and _sha(raw) == supervisor_manifest_sha256,
                  "ADMISSION_SUPERVISOR_MANIFEST_PIN")
        held = C.parse_json(raw, C.Limits(max_bytes=8*1024**2))
        C.require(type(held) is dict and type(held.get("files")) is dict, "ADMISSION_SUPERVISOR_MANIFEST")
        self._install = manifest.parent
        self._manifest, self._manifest_raw = manifest, raw
        self._loaded_pins = {}

        def load(name, relative):
            path = self._install / relative
            expected = held["files"].get(relative)
            C.fields(expected, {"sha256", "bytes"})
            C.digest_string(expected["sha256"]); C.uint(expected["bytes"], 4*1024**2)
            C.require(path.is_file() and path.stat().st_size == expected["bytes"], "ADMISSION_SUPERVISOR_SIZE")
            source = path.read_bytes()
            C.require(len(source) == expected["bytes"] and _sha(source) == expected["sha256"],
                      "ADMISSION_SUPERVISOR_SOURCE_PIN")
            self._loaded_pins[path] = dict(expected)
            if name in sys.modules:
                existing = sys.modules[name]
                C.require(getattr(existing, "_dmkn_admission_source_pin", None) == expected["sha256"]
                          and Path(getattr(existing, "__file__", "")) == path,
                          "ADMISSION_MODULE_NAME_COLLISION")
                return existing
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            try: exec(compile(source, str(path), "exec"), module.__dict__)
            except BaseException:
                del sys.modules[name]; raise
            module._dmkn_admission_source_pin = expected["sha256"]
            return module

        self._supervisor = load("_dmkn_v5_admission_supervisor", "operator/commons.py")
        load("domains", "receiver/helpers/domains.py")
        self._job = load("_dmkn_v5_admission_job", "receiver/helpers/run_stage.py").Job
        self._supervisor.absolute(manifest)
        self._supervisor.absolute(self._install, directory=True)
        C.require(type(runtime_pins) is dict and 1 <= len(runtime_pins) <= 128, "ADMISSION_RUNTIME_PINS")
        self._pins = {}
        for name, pin in runtime_pins.items():
            C.require(type(name) is str, "ADMISSION_RUNTIME_PATH")
            C.fields(pin, {"sha256", "bytes"}); C.digest_string(pin["sha256"])
            C.uint(pin["bytes"], 128*1024**2)
            path = self._supervisor.absolute(name)
            self._pins[path] = dict(pin)
        C.require(sum(pin["bytes"] for pin in self._pins.values()) <= 512*1024**2,
                  "ADMISSION_RUNTIME_TOTAL_BOUND")
        self._executable = self._supervisor.absolute(executable)
        C.require(self._executable in self._pins, "ADMISSION_UNPINNED_VERIFIER")
        self._pin_phase_origin = Path(__file__).resolve().parent / "pin_phase.py"
        C.require(self._pin_phase_origin in self._pins, "ADMISSION_UNPINNED_PIN_PHASE")
        C.require(self._trust_origin in self._pins, "ADMISSION_UNPINNED_TRUST_GUARD")
        # Do not infer that this pin map proves a hermetic OS/DLL closure.
        self._profile_id = C.hash_value("local-admission-profile", {
            "journal_profile": JOURNAL_PROFILE, "trust": self._trust_identity,
            "image": image_id, "foundation": foundation, "policy": policy,
            "verifier": self._pins[self._executable],
            "supervisor_manifest": supervisor_manifest_sha256,
            "runtime_pins": {str(k): v for k, v in self._pins.items()}})
        self._check_install()

    def _revoke(self):
        # Internal denial must also work during receive(); public close refuses
        # that busy state and would mask the original withdrawal exception.
        self._closed = True
        self._handles.clear()

    def _active(self):
        try:
            C.require(not self._closed and time.monotonic() < self._deadline,
                      "ADMISSION_CLOSED_OR_EXPIRED")
            C.require(self._trust_module is T and T is sys.modules.get("admission.trust")
                and type(getattr(T, "__file__", None)) is str
                and Path(T.__file__).resolve() == self._trust_origin,
                "ADMISSION_TRUST_SOURCE_ORIGIN")
            C.require(self._trust_binding is self._trust_original_binding
                and type(self._trust_binding) is T.TrustBinding
                and self._trust_binding._domain is self._trust_domain,
                "ADMISSION_ORIGINAL_TRUST_BINDING")
            C.require(T.check_binding(self._trust_binding) == self._trust_identity,
                      "ADMISSION_TRUST_IDENTITY_CHANGED")
        except BaseException:
            self._revoke()
            raise

    def _check_install(self):
        self._active()
        C.require(PP is sys.modules.get("admission.pin_phase")
                  and type(getattr(PP, "__file__", None)) is str
                  and Path(PP.__file__).resolve() == self._pin_phase_origin,
                  "ADMISSION_PIN_PHASE_SOURCE_ORIGIN")
        C.require(self._supervisor.bounded_read(self._manifest, 8*1024**2) == self._manifest_raw,
                  "ADMISSION_MANIFEST_CHANGED")
        for path, expected in {**self._loaded_pins, **self._pins}.items():
            self._active()
            C.require(PP.check_pin(self._supervisor.pin, path, expected), "ADMISSION_RUNTIME_CHANGED")
        self._active()

    def receive(self, receipt, expected_summary, operation_directory, *, cpu_seconds=30,
                wall_seconds=60, memory_mib=1024):
        """Verify module validity, not the provenance of separately supplied proofs.

        No test-success, submitted-witness or saved-report parameter exists.
        """
        self._active(); C.require(not self._busy, "ADMISSION_SINGLE_OWNER")
        C.require(type(receipt) is bytes and 0 < len(receipt) <= 64*1024**2, "ADMISSION_RECEIPT_BOUND")
        module = C.summary_id(expected_summary)
        C.require(expected_summary["foundation"] == self._foundation
                  and expected_summary["policy"] == self._policy, "ADMISSION_EXPECTED_POLICY")
        summary_bytes = C.canonical(expected_summary)
        limits = self._supervisor.limits_checked({"cpu_seconds": cpu_seconds,
            "wall_seconds": wall_seconds, "memory_mib": memory_mib, "active_processes": 2,
            "stdout_bytes": 16384, "stderr_bytes": 16384})
        C.require(cpu_seconds <= 600 and wall_seconds <= 600 and memory_mib <= 4096,
                  "ADMISSION_PER_CALL_LIMIT")
        charged = (1, len(receipt), cpu_seconds)
        C.require(all(a+b <= cap for a, b, cap in zip(self._used, charged, self._caps)),
                  "ADMISSION_AGGREGATE_BUDGET")
        output = self._supervisor.absolute(operation_directory, directory=True, fresh=True)
        for protected in [self._install, *self._pins]:
            C.require(not self._supervisor.overlap(output, protected), "ADMISSION_OUTPUT_OVERLAP")
        self._busy = True
        # Full reservation remains charged on ALL later exits, including preflight.
        self._used = [a+b for a, b in zip(self._used, charged)]
        started = time.monotonic(); controller_started = time.process_time()
        try:
            self._check_install()
            limits["wall_seconds"] = min(limits["wall_seconds"], math.floor(self._deadline-started))
            C.require(limits["wall_seconds"] >= 1, "ADMISSION_DEADLINE")
            output.mkdir()
            received = output / "receipt.bin"
            with received.open("xb") as stream:
                stream.write(receipt); stream.flush(); os.fsync(stream.fileno())
            self._supervisor.save_new(output / "request.json", {"profile_id": self._profile_id,
                "module": module, "summary": C.parse_json(summary_bytes),
                "receipt_sha256": _sha(receipt), "receipt_bytes": len(receipt), "limits": limits})
            report = self._supervisor.supervise([str(self._executable), "receive", self._image,
                str(received), module], self._install, output / "command", limits, self._job, started=started)
            # Save operational evidence even if clean closure or binding later fails.
            self._supervisor.save_new(output / "process.json", report)
            C.require(report["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
                and report["child_exit_code"] == 0 and report["direct_child_reaped"] is True
                and report["job_closed"] is True and report["cleanup_errors"] == []
                and report["termination_requested"] is False
                and report["final_job"]["active_processes"] == 0
                and report["final_job"]["terminated_processes"] == 0, "ADMISSION_VERIFIER_REFUSED")
            self._check_install()
            C.require(self._supervisor.bounded_read(received, 64*1024**2) == receipt,
                      "ADMISSION_RECEIPT_CHANGED")
            bound = bind_output(self._supervisor.bounded_read(output / "command/stdout.txt", 16384),
                receipt, C.parse_json(summary_bytes), image_id=self._image,
                foundation=self._foundation, policy=self._policy)
            self._active()
            C.require(time.monotonic()-started <= limits["wall_seconds"], "ADMISSION_TOTAL_WALL_LIMIT")
            self._supervisor.save_new(output / "binding.json", {"status": "SAME_CALL_BINDINGS_VALIDATED_BEFORE_HANDLE",
                "profile_id": self._profile_id, "module": module, "receipt_sha256": _sha(receipt),
                "controller_cpu_seconds": time.process_time()-controller_started,
                "wall_seconds": time.monotonic()-started,
                "authority": "LOCAL_EVIDENCE_NOT_TRANSFERABLE_PROOF"})
            # Evidence I/O can block too; never mint authority after its deadline.
            self._active()
            C.require(time.monotonic()-started <= limits["wall_seconds"], "ADMISSION_TOTAL_WALL_LIMIT")
            handle = VerifiedModule()
            self._handles[handle] = (bound["module"], summary_bytes, bound["journal"], bound["receipt_sha256"])
            return handle
        finally:
            self._busy = False

    def describe(self, handle):
        self._active()
        C.require(type(handle) is VerifiedModule and handle in self._handles, "ADMISSION_FOREIGN_OR_UNKNOWN_HANDLE")
        module, summary, raw_journal, receipt_sha256 = self._handles[handle]
        fact = {"module": module, "summary": C.parse_json(summary), "journal": raw_journal,
                "receipt_sha256": receipt_sha256, "profile_id": self._profile_id}
        self._active()
        return fact

    def open_group(self, handle, opening):
        accepted = self.describe(handle)
        group = C.verify_group_opening(accepted["module"], opening)
        C.require(opening["summary"] == accepted["summary"], "ADMISSION_OPENING_SUMMARY")
        copied = C.parse_json(C.canonical(group))
        self._active()
        return copied

    def report(self):
        return {"attempts": self._used[0], "submitted_bytes": self._used[1],
                "reserved_cpu_seconds": self._used[2], "live_handles": len(self._handles),
                "closed": self._closed, "profile_id": self._profile_id,
                "authority": "LOCAL_RESOURCE_ACCOUNTING_NOT_PROOF"}

    def close(self):
        C.require(not self._busy, "ADMISSION_CALL_ACTIVE")
        self._revoke()
