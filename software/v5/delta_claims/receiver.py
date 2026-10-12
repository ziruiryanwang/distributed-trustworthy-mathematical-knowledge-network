"""Fresh exact-warrant successor: semantic ModuleID variants may coexist.

Owner-local native admission with a complete bounded uncertified closure.

Only a real ReceiptVerifier can discharge frontier premises. Neither native
stdout, a saved report nor a caller-created handle grants authority by itself.
The owner process/installation are trusted; Windows Jobs are NOT a sandbox.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import math
import os
from pathlib import Path
import time

from admission.verifier import ReceiptVerifier
from admission.bindings import journal
from modules import codec as C
from production.producer import parse as parse_local_report
from delta.packet import (MIB, Envelope, DeltaError, need, parse_packet, bind_native,
                     require_closure)


def _sha(raw): return hashlib.sha256(raw).hexdigest()


class VerifiedDelta:
    """Opaque local authority. Not a VerifiedModule and not a receipt/proof file."""
    __slots__ = ()


class DeltaVerifier:
    """Single owner, fixed finite lifetime; no automatic retries or network I/O.

    Constructor arguments are independently adopted LOCAL owner configuration,
    never a remote packet's instructions. All admission calls share one allowance.
    Any failed receive closes this instance; underlying receipt owner is separate.
    """
    def __init__(self, frontier_verifier, *, native_executable, runtime_pins,
                 output_directory, envelope=None, operations=8,
                 submitted_bytes=128*MIB, reserved_cpu_seconds=3600,
                 controller_cpu_seconds=600, wall_seconds=3600,
                 output_bytes=512*MIB, output_entries=4096):
        self._started, self._cpu_started = time.monotonic(), time.process_time()
        need(type(frontier_verifier) is ReceiptVerifier, "EXACT_REAL_FRONTIER_VERIFIER")
        frontier_verifier._active()
        self._frontier = self._origin = frontier_verifier
        self._A, self._Job = frontier_verifier._supervisor, frontier_verifier._job
        self._image = frontier_verifier._image
        self._foundation, self._policy = frontier_verifier._foundation, frontier_verifier._policy
        self._frontier_profile = frontier_verifier.report()["profile_id"]
        self._envelope = Envelope() if envelope is None else envelope
        need(type(self._envelope) is Envelope, "EXACT_OWNER_ENVELOPE")
        self._envelope.validate()
        values = (operations, submitted_bytes, reserved_cpu_seconds, controller_cpu_seconds,
                  wall_seconds, output_bytes, output_entries)
        caps = (128, 1024*MIB, 86400, 3600, 86400, 2*1024*MIB, 8192)
        need(all(type(v) is int and 0 < v <= cap for v, cap in zip(values, caps)), "OWNER_ALLOWANCE")
        self._caps = tuple(values)
        self._deadline = min(self._started+wall_seconds, frontier_verifier._deadline)
        self._closed = self._busy = False
        self._used = [0, 0, 0]
        self._observed_worker = 0.0
        self._handles, self._cache, self._history = {}, {}, []
        need(type(runtime_pins) is dict and 1 <= len(runtime_pins) <= 128, "NATIVE_PIN_MAP")
        self._pins = {}
        for name, pin in runtime_pins.items():
            C.fields(pin, {"sha256", "bytes"}); C.digest_string(pin["sha256"])
            need(0 < C.uint(pin["bytes"], 128*MIB), "NATIVE_PIN_SIZE")
            path = self._A.absolute(name)
            need(path not in self._pins, "NATIVE_DUPLICATE_PIN")
            self._pins[path] = dict(pin)
        need(sum(p["bytes"] for p in self._pins.values()) <= 512*MIB, "NATIVE_PIN_TOTAL")
        self._native = self._A.absolute(native_executable)
        root = Path(__file__).resolve().parents[1]
        required = {self._native, root/"delta_claims/receiver.py", root/"delta_claims/__init__.py",
                    root/"delta_claims/claims.py", root/"delta/receiver.py", root/"delta/packet.py",
                    root/"delta/__init__.py", root/"admission/verifier.py",
                    root/"admission/bindings.py", root/"modules/codec.py",
                    root/"production/producer.py", root/"production/__init__.py"}
        need(required <= set(self._pins), "REQUIRED_NATIVE_AND_CONTROLLER_PINS")
        self._profile_id = C.hash_value("local-native-delta-exact-warrants-profile-v1", {
            "frontier_profile":self._frontier_profile, "envelope":asdict(self._envelope),
            "native":self._pins[self._native],
            "pins":{str(k):v for k,v in self._pins.items()}})
        self._check()
        self._output = self._A.absolute(output_directory, directory=True, fresh=True)
        for protected in (self._frontier._install, self._frontier._manifest,
                          *self._frontier._pins, *self._pins):
            need(not self._A.overlap(self._output, protected), "OUTPUT_OVERLAP")
        self._output.mkdir()
        self._save(self._output/"owner.json", {"profile":self._profile_id,
            "frontier_profile":self._frontier_profile, "envelope":asdict(self._envelope),
            "allowance":list(values), "authority":"OWNER_SELECTION_NOT_MATHEMATICAL_PROOF"})
        self._owner_raw = self._A.bounded_read(self._output/"owner.json", MIB)
        self._active(); self._census()

    def _active(self, deadline=None):
        need(not self._closed and self._frontier is self._origin,
             "DELTA_CLOSED_OR_CHANGED_FRONTIER_OWNER")
        need(time.monotonic() < min(self._deadline, deadline or self._deadline),
             "DELTA_ORIGINAL_DEADLINE", "RESOURCE_INCOMPLETE")
        need(time.process_time()-self._cpu_started <= self._caps[3],
             "DELTA_CONTROLLER_CPU", "RESOURCE_INCOMPLETE")
        self._frontier._active()
        need(self._frontier.report()["profile_id"] == self._frontier_profile,
             "FRONTIER_PROFILE_CHANGED")

    def _check(self, deadline=None):
        self._active(deadline); self._frontier._check_install()
        for path, pin in self._pins.items():
            self._active(deadline)
            need(self._A.pin(path) == pin, "NATIVE_OR_CONTROLLER_PIN_CHANGED")
        if hasattr(self, "_owner_raw"):
            need(self._A.bounded_read(self._output/"owner.json", MIB) == self._owner_raw,
                 "OWNER_SELECTION_CHANGED")
        self._active(deadline)

    def _write(self, path, raw):
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())

    def _save(self, path, value):
        self._write(path, C.canonical(value))

    def _census(self, reserve=0, entries=0):
        size, count = reserve, entries
        for directory, dirs, names in os.walk(self._output, followlinks=False):
            for name in dirs+names:
                self._active(); path = Path(directory)/name; count += 1
                self._A.absolute(path, directory=name in dirs)
                if name in names: size += path.stat().st_size
                need(size <= self._caps[5] and count <= self._caps[6],
                     "DELTA_OUTPUT_ENVELOPE", "RESOURCE_INCOMPLETE")
        need(size <= self._caps[5] and count <= self._caps[6],
             "DELTA_OUTPUT_ENVELOPE", "RESOURCE_INCOMPLETE")

    def _live_frontiers(self, selected, deadline=None):
        self._active(deadline)
        for handle, receipt_digest, expected_journal, expected_summary in selected:
            live = self._frontier.describe(handle)
            need(live["profile_id"] == self._frontier_profile
                 and live["receipt_sha256"] == receipt_digest
                 and live["journal"] == expected_journal
                 and C.canonical(live["summary"]) == expected_summary,
                 "EXACT_LIVE_FRONTIER_BINDING")
        self._active(deadline)

    @staticmethod
    def _clean(report, cpu, wall):
        final = report.get("final_job")
        if (type(final) is dict and report.get("child_exit_code") not in (None, 0)
                and report.get("direct_child_reaped") is True and report.get("job_closed") is True
                and report.get("cleanup_errors") == [] and report.get("termination_requested") is False
                and final.get("active_processes") == 0 and final.get("terminated_processes") == 0):
            raise DeltaError("INVALID_OR_UNBOUND", "NATIVE_OR_FRONTIER_REJECTED")
        need(type(final) is dict and report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
             and report.get("child_exit_code") == 0 and report.get("direct_child_reaped") is True
             and report.get("job_closed") is True and report.get("cleanup_errors") == []
             and report.get("termination_requested") is False
             and final.get("active_processes") == 0 and final.get("terminated_processes") == 0,
             "NATIVE_OR_FRONTIER_REFUSED_OR_UNCLOSED", "RESOURCE_INCOMPLETE")
        cost = final.get("cpu_seconds"); elapsed = report.get("wall_seconds_through_cleanup")
        need(type(cost) in (int,float) and math.isfinite(cost) and 0 <= cost <= cpu
             and type(elapsed) in (int,float) and math.isfinite(elapsed) and 0 <= elapsed <= wall,
             "ACTUAL_WORKER_OR_WALL_EXCEEDED", "RESOURCE_INCOMPLETE")
        return cost

    def receive(self, packet, expected_summary, *, native_cpu_seconds=30,
                receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024):
        """Check a complete packet and return ONLY a distinct local delta handle.

        Frontiers are real receipts; a packet cannot supply a saved acceptance.
        The requested summary is a caller-selected goal identity, not authority.
        """
        entered = time.monotonic()
        self._active(); need(not self._busy, "DELTA_SINGLE_OWNER")
        for value, cap in ((native_cpu_seconds,600),(receipt_cpu_seconds,600),
                           (wall_seconds,600),(memory_mib,4096)):
            need(type(value) is int and 0 < value <= cap, "DELTA_CALL_LIMIT")
        need(memory_mib >= 64, "DELTA_MEMORY_LIMIT")
        need(type(packet) is bytes, "IMMUTABLE_PACKET_BYTES")
        need(self._used[0]+1 <= self._caps[0] and self._used[1]+len(packet) <= self._caps[1],
             "DELTA_AGGREGATE_INPUT_ALLOWANCE", "RESOURCE_INCOMPLETE")
        self._used[0] += 1; self._used[1] += len(packet)
        self._busy = True
        directory = None
        deadline = min(self._deadline, entered+wall_seconds)
        try:
            received, witnesses, census = parse_packet(packet, self._envelope)
            C.validate_summary(expected_summary)
            summary = C.canonical(expected_summary)
            need(expected_summary["foundation"] == self._foundation
                 and expected_summary["policy"] == self._policy, "REQUESTED_TARGET_POLICY")
            need(C.canonical(witnesses[-1][2]) == summary, "LAST_DELTA_REQUESTED_TARGET")
            reserve = len(received)*receipt_cpu_seconds+len(witnesses)*native_cpu_seconds
            need(self._used[2]+reserve <= self._caps[2],
                 "DELTA_AGGREGATE_CPU_RESERVATION", "RESOURCE_INCOMPLETE")
            self._used[2] += reserve  # Conservative reservation, retained on failure/cache hits.
            self._check(deadline)
            self._census(len(packet)+census["witness_bytes"]+census["receipt_bytes"]
                         +len(witnesses)*6*MIB+len(received)*MIB+MIB,
                         12*(len(received)+len(witnesses))+8)
            directory = self._output/str(self._used[0]); directory.mkdir()
            self._write(directory/"packet.json", packet)
            self._save(directory/"request.json", {"profile":self._profile_id,
                "packet_sha256":_sha(packet), "target":C.parse_json(summary),
                "census":census, "worker_cpu_reserved":reserve,
                "native_cpu_seconds":native_cpu_seconds, "receipt_cpu_seconds":receipt_cpu_seconds,
                "wall_seconds":wall_seconds, "memory_mib":memory_mib})
            graph, representations, selected = {}, {}, []
            for index, (receipt, encoded_summary) in enumerate(received):
                self._active(deadline)
                key = (_sha(receipt), encoded_summary)
                handle = self._cache.get(key)
                if handle is None:
                    remaining = math.floor(deadline-time.monotonic())
                    need(remaining >= 1, "FRONTIER_DEADLINE", "RESOURCE_INCOMPLETE")
                    operation = directory/("frontier-"+str(index))
                    handle = self._frontier.receive(receipt, C.parse_json(encoded_summary), operation,
                        cpu_seconds=receipt_cpu_seconds, wall_seconds=remaining, memory_mib=memory_mib)
                    # Evidence here accounts resources; only returned live handle confers authority.
                    # Local telemetry contains fractional CPU/wall values. The
                    # integer-only mathematical wire parser is inappropriate.
                    process = parse_local_report(self._A.bounded_read(operation/"process.json", MIB))
                    self._observed_worker += self._clean(process,receipt_cpu_seconds,remaining)
                    self._cache[key] = handle
                live = self._frontier.describe(handle)
                need(live["receipt_sha256"] == key[0]
                     and C.canonical(live["summary"]) == encoded_summary, "FRONTIER_RECEIPT_BINDING")
                raw_journal = live["journal"]; decoded = journal(raw_journal)
                need(raw_journal[12:44].hex() == self._image
                     and decoded["foundation"] == self._foundation and decoded["policy"] == self._policy
                     and decoded["rank"] <= self._envelope.rank, "FRONTIER_ADOPTION")
                need(raw_journal not in graph, "DUPLICATE_EXACT_FRONTIER")
                graph[raw_journal] = ()
                representations[raw_journal] = ("receipt-frontier", _sha(receipt))
                selected.append((handle,key[0],raw_journal,encoded_summary))
            target = None
            for index, (witness, parents, own_summary, rank) in enumerate(witnesses):
                self._check(deadline); self._live_frontiers(selected,deadline)
                need(all(parent in graph for parent in parents),
                     "MISSING_OR_FORWARD_PARENT", "MISSING_MATERIAL")
                need(len(set(parents)) == len(parents), "DUPLICATE_DELTA_PARENT")
                need(rank == (1+max(journal(p)["rank"] for p in parents) if parents else 0),
                     "EXACT_DELTA_RANK")
                path = directory/("delta-"+str(index)+".json")
                self._write(path,witness)
                remaining = math.floor(deadline-time.monotonic())
                need(remaining >= 1, "NATIVE_DEADLINE", "RESOURCE_INCOMPLETE")
                limits = self._A.limits_checked({"cpu_seconds":native_cpu_seconds,
                    "wall_seconds":remaining,"memory_mib":memory_mib,"active_processes":2,
                    "stdout_bytes":4*MIB,"stderr_bytes":MIB})
                command = directory/("native-"+str(index))
                process = self._A.supervise([str(self._native),"check",self._image,str(path)],
                    self._frontier._install,command,limits,self._Job)
                self._save(directory/("process-"+str(index)+".json"),process)
                self._observed_worker += self._clean(process,native_cpu_seconds,remaining)
                self._check(deadline); self._live_frontiers(selected,deadline)
                need(self._A.bounded_read(path,16*MIB) == witness, "NATIVE_INPUT_CHANGED")
                raw = self._A.bounded_read(command/"stdout.txt",4*MIB)
                target, actual_parents = bind_native(raw,witness,parents,own_summary,rank,
                    self._image,self._foundation,self._policy)
                need(target not in graph, "DUPLICATE_EXACT_DELTA")
                need(all(p in graph for p in actual_parents), "UNCHECKED_NATIVE_PREMISE")
                graph[target] = actual_parents
                representations[target] = ("native-delta", _sha(witness))
            require_closure(target,graph)
            need(C.canonical(journal(target)["summary"]) == summary, "CHECKED_TARGET_IDENTITY")
            self._check(deadline); self._live_frontiers(selected,deadline)
            need(self._A.bounded_read(directory/"packet.json",self._envelope.packet_bytes) == packet,
                 "WHOLE_PACKET_CHANGED")
            self._census()
            self._save(directory/"RESULT.json", {"status":"BOUND_DELTA_BEFORE_LIVE_PROMOTION",
                "profile":self._profile_id,"module":journal(target)["module"],
                "journal":list(target),"packet_sha256":_sha(packet),"census":census,
                "authority":"SAVED_REPORT_NOT_TRANSFERABLE_PROOF_OR_LIVE_HANDLE"})
            # Durable output and census can block; promotion is after all of them.
            self._census(); self._check(deadline); self._live_frontiers(selected,deadline)
            handle = VerifiedDelta()
            # Retain ONLY the actual established journals, not an inventory
            # claimed by packet metadata. Each graph entry passed this call's
            # induction and complete target-closure check.
            self._handles[handle] = (target,packet,tuple(selected),tuple(graph),representations)
            self._history.append({"module":journal(target)["module"],"packet_sha256":_sha(packet)})
            self._active(deadline)
            return handle
        except BaseException as error:
            self._handles.clear(); self._closed = True
            if directory is not None:
                self._save(directory/"FINALIZATION-FAILED.json", {"status":"NO_LIVE_DELTA_HANDLE",
                    "reason":type(error).__name__+": "+str(error)[:2000]})
            if isinstance(error, C.StructureError):
                raise DeltaError("INVALID_OR_UNBOUND", str(error)) from error
            raise
        finally:
            self._busy = False

    def describe(self, handle):
        self._check()
        need(type(handle) is VerifiedDelta and handle in self._handles, "FOREIGN_OR_UNKNOWN_DELTA_HANDLE")
        raw, packet, selected, _, _ = self._handles[handle]
        self._live_frontiers(selected)
        decoded = journal(raw)
        return {"module":decoded["module"],"summary":decoded["summary"],"journal":raw,
                "profile_id":self._profile_id,"packet_sha256":_sha(packet),
                "proof_form":"bounded-native-delta-not-succinct-receipt"}

    def members(self, handle):
        """Copied facts about this SAME accepted closure, not new receipt handles."""
        self.describe(handle)
        _, packet, selected, inventory, representations = self._handles[handle]
        result = []
        for raw in inventory:
            decoded = journal(raw)
            result.append({"module":decoded["module"],"summary":decoded["summary"],
                "journal":raw,"profile_id":self._profile_id,"packet_sha256":_sha(packet),
                "proof_form":representations[raw][0],"evidence_sha256":representations[raw][1]})
        self._live_frontiers(selected)
        return result

    def variants(self, handle, module):
        """Enumerate exact warrant alternatives; never choose a rank implicitly."""
        C.digest_string(module)
        return sorted((item for item in self.members(handle) if item["module"] == module),
                      key=lambda item: item["journal"])

    def describe_member(self, handle, exact_journal):
        """Exact bytes are a selector, not authority; the live closure supplies it."""
        journal(exact_journal)
        for item in self.members(handle):
            if item["journal"] == exact_journal:
                self._active()
                return item
        raise DeltaError("MISSING_MATERIAL", "EXACT_WARRANT_NOT_IN_ACCEPTED_DELTA_CLOSURE")

    def open_member_group(self, handle, exact_journal, opening):
        accepted = self.describe_member(handle,exact_journal)
        group = C.verify_group_opening(accepted["module"],opening)
        need(opening["summary"] == accepted["summary"], "DELTA_MEMBER_OPENING_SUMMARY")
        self.describe_member(handle,exact_journal)
        return group

    def open_group(self, handle, opening):
        accepted = self.describe(handle)
        group = C.verify_group_opening(accepted["module"],opening)
        need(opening["summary"] == accepted["summary"], "DELTA_OPENING_SUMMARY")
        self.describe(handle)
        return group

    def export_packet(self, handle):
        """Return complete untrusted onward-checking material, NEVER authority."""
        self.describe(handle)
        return self._handles[handle][1]

    def report(self):
        return {"attempts":self._used[0],"submitted_bytes":self._used[1],
                "reserved_worker_cpu":self._used[2],"observed_success_worker_cpu":self._observed_worker,
                "controller_cpu_seconds":time.process_time()-self._cpu_started,
                "live_handles":len(self._handles),"closed":self._closed,
                "scope":"OWNER_LIFETIME_CONTROLLER;RESERVATIONS_RETAIN_FAILED_WORK;OBSERVED_WORKER_IS_PARTIAL",
                "profile_id":self._profile_id,"mathematical_authority":False}

    def close(self):
        need(not self._busy, "DELTA_CALL_ACTIVE")
        self._closed = True; self._handles.clear(); self._cache.clear()


