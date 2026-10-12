"""Same-call aggregate receipt admission and exact member authority.

Source-only candidate. Requires an independently adopted actual A host/image;
structural bindings or a synthetic A never replace that verification. The local
controller/install are trusted; inherited Windows Jobs are not a security sandbox.
"""
from __future__ import annotations

import hashlib
import math
import os
from pathlib import Path
import sys
import time

from admission.verifier import ReceiptVerifier
from modules import codec as C
from . import bindings as B
from .admission_binding import bind_output

MIB = 1024**2


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


class VerifiedAggregate:
    """Opaque owner-local (A,H) authority, never a VerifiedModule/I receipt."""
    __slots__ = ()


class VerifiedAggregateMember:
    """Opaque selected exact J, borrowing its SAME live aggregate owner."""
    __slots__ = ()


class AggregateReceiptVerifier(ReceiptVerifier):
    """Reuse only frozen owner supervision/install machinery, not I statements.

    All statement-facing methods/profile/handle registries are overridden. The
    base initializer runs no mathematical verifier. Exact old ReceiptVerifier
    gates reject this subclass. One owner, finite lifetime, no retries/network.
    """
    def __init__(self, *, supervisor_manifest, supervisor_manifest_sha256,
                 executable, runtime_pins, aggregate_image, operations,
                 submitted_bytes, reserved_cpu_seconds, wall_seconds,
                 member_calls=4096, member_storage=4096, member_bytes=64*MIB,
                 controller_cpu_seconds=600, output_bytes=512*MIB, output_entries=8192):
        # Base __init__ calls self._check_install -> self._active. Initialize all
        # fields read by our override first; final profile binding starts later.
        self._aggregate_initialized = False
        self._members, self._member_cache = {}, {}
        self._member_used = [0,0]
        self._output_reserved = [0,0]
        self._controller_started = time.process_time()
        for value,maximum in ((member_calls,65536),(member_storage,16384),
                              (member_bytes,256*MIB),(controller_cpu_seconds,3600),
                              (output_bytes,2*1024*MIB),(output_entries,65536)):
            C.require(0 < C.uint(value,maximum),"AGGREGATE_OWNER_LIMIT")
        self._member_caps = member_calls,member_storage,member_bytes
        self._controller_cpu_cap = controller_cpu_seconds
        self._output_caps = output_bytes,output_entries
        B._adopted_image(aggregate_image)
        self._adopted_aggregate_image = aggregate_image
        super().__init__(supervisor_manifest=supervisor_manifest,
            supervisor_manifest_sha256=supervisor_manifest_sha256,
            executable=executable,runtime_pins=runtime_pins,image_id=aggregate_image,
            foundation=B.FOUNDATION,policy=B.POLICY,operations=operations,
            submitted_bytes=submitted_bytes,reserved_cpu_seconds=reserved_cpu_seconds,
            wall_seconds=wall_seconds)
        root = Path(__file__).resolve().parents[1]
        self._required_origins = {name:root/relative for name,relative in (
            ("aggregate_claims.aggregate_admission","aggregate_claims/aggregate_admission.py"),
            ("aggregate_claims","aggregate_claims/__init__.py"),
            ("aggregate_claims.admission_binding","aggregate_claims/admission_binding.py"),
            ("aggregate_claims.bindings","aggregate_claims/bindings.py"),
            ("admission","admission/__init__.py"),
            ("admission.verifier","admission/verifier.py"),
            ("admission.bindings","admission/bindings.py"),
            ("modules","modules/__init__.py"),("modules.codec","modules/codec.py"))}
        C.require(set(self._required_origins.values()) <= set(self._pins),
                  "AGGREGATE_OWNER_REQUIRED_SOURCE_PINS")
        self._profile_id = C.hash_value("local-aggregate-admission-exact-warrants-v2",{
            "aggregate_image":aggregate_image,"relation_image":B.RELATION_IMAGE,
            "foundation":B.FOUNDATION,"policy":B.POLICY,"header_magic":B.MAGIC.hex(),
            "header_version":B.VERSION,"header_bytes":B.HEADER_BYTES,
            "receipt_scheme":"resolved-succinct-poseidon2",
            "verifier":self._pins[self._executable],
            "supervisor_manifest":supervisor_manifest_sha256,
            "runtime_pins":{str(k):v for k,v in self._pins.items()}})
        self._origin_profile = self._profile_id
        self._aggregate_initialized = True
        self._check_live()

    def _revoke(self):
        self._closed = True
        if hasattr(self,"_handles"): self._handles.clear()
        self._members.clear(); self._member_cache.clear()

    def _active(self):
        try:
            ReceiptVerifier._active(self)
            C.require(time.process_time()-self._controller_started <= self._controller_cpu_cap,
                      "AGGREGATE_CONTROLLER_CPU")
            if self._aggregate_initialized:
                C.require(self._profile_id == self._origin_profile
                    and self._image == self._adopted_aggregate_image
                    and self._foundation == B.FOUNDATION and self._policy == B.POLICY,
                    "AGGREGATE_OWNER_PROFILE_CHANGED")
        except BaseException:
            self._revoke(); raise

    def _check_live(self):
        try:
            self._check_loaded_sources()
            self._check_install()
        except BaseException:
            self._revoke(); raise

    def _check_loaded_sources(self):
        # Actual imported code must come from these pinned files, not merely
        # coexist with them on disk in a second installation.
        for name,path in self._required_origins.items():
            module = sys.modules.get(name)
            C.require(module is not None and type(getattr(module,"__file__",None)) is str
                and Path(module.__file__).resolve() == path,"AGGREGATE_LOADED_SOURCE_ORIGIN:"+name)
        C.require(ReceiptVerifier is sys.modules["admission.verifier"].ReceiptVerifier
            and C is sys.modules["modules.codec"] and B is sys.modules["aggregate_claims.bindings"]
            and bind_output is sys.modules["aggregate_claims.admission_binding"].bind_output
            and B.journal is sys.modules["admission.bindings"].journal,
            "AGGREGATE_IMPORTED_SYMBOL_ORIGIN")

    def _member_begin(self):
        self._active()
        C.require(not self._busy,"AGGREGATE_SINGLE_OWNER")
        C.require(self._member_used[0] < self._member_caps[0],"AGGREGATE_MEMBER_CALL_ALLOWANCE")
        self._member_used[0] += 1
        self._check_live()

    def _charge_member_bytes(self, count):
        self._member_used[1] += count
        C.require(self._member_used[1] <= self._member_caps[2],"AGGREGATE_MEMBER_BYTE_ALLOWANCE")

    def _aggregate_record(self, handle):
        C.require(type(handle) is VerifiedAggregate and handle in self._handles,
                  "AGGREGATE_FOREIGN_OR_UNKNOWN_HANDLE")
        return self._handles[handle]

    def _member_record(self, handle):
        C.require(type(handle) is VerifiedAggregateMember and handle in self._members,
                  "AGGREGATE_FOREIGN_OR_UNKNOWN_MEMBER")
        aggregate,exact,index,siblings = self._members[handle]
        header,receipt_digest,receipt_bytes = self._aggregate_record(aggregate)
        member = B.bind_member(header,exact,index,list(siblings),adopted_image=self._image)
        return aggregate,header,receipt_digest,receipt_bytes,exact,index,siblings,member

    @staticmethod
    def _write(path, raw):
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())

    def _census(self, directory, byte_cap, entry_cap):
        count = size = 0
        for parent,dirs,names in os.walk(directory,followlinks=False):
            for name in dirs+names:
                self._active(); path = Path(parent)/name
                self._supervisor.absolute(path,directory=name in dirs)
                count += 1
                if name in names: size += path.stat().st_size
                C.require(count <= entry_cap and size <= byte_cap,"AGGREGATE_OPERATION_OUTPUT_BOUND")

    def receive(self, receipt, expected_header, operation_directory, *, cpu_seconds=30,
                wall_seconds=60, memory_mib=1024):
        """Fully verify exact (A,H) in this call; saved stdout cannot enter."""
        self._active(); C.require(not self._busy,"AGGREGATE_SINGLE_OWNER")
        C.require(type(receipt) is bytes and 0 < len(receipt) <= 64*MIB,
                  "AGGREGATE_RECEIPT_BOUND")
        C.require(type(expected_header) is bytes and len(expected_header) == B.HEADER_BYTES,
                  "AGGREGATE_EXPECTED_HEADER_BYTES")
        for value,maximum,minimum in ((cpu_seconds,600,1),(wall_seconds,600,1),(memory_mib,4096,64)):
            C.require(minimum <= C.uint(value,maximum),"AGGREGATE_PER_CALL_LIMIT")
        charged = 1,len(receipt),cpu_seconds
        C.require(all(a+b <= cap for a,b,cap in zip(self._used,charged,self._caps)),
                  "AGGREGATE_ADMISSION_ALLOWANCE")
        output_charge = len(receipt)+B.HEADER_BYTES+MIB,32
        C.require(all(a+b <= cap for a,b,cap in zip(self._output_reserved,output_charge,self._output_caps)),
                  "AGGREGATE_OUTPUT_RESERVATION")
        self._used = [a+b for a,b in zip(self._used,charged)]
        self._output_reserved = [a+b for a,b in zip(self._output_reserved,output_charge)]
        started = time.monotonic(); self._busy = True
        try:
            B.decode_header(expected_header,adopted_image=self._image)
            self._check_live()
            deadline = min(self._deadline,started+wall_seconds)
            # supervise(started=started) measures from the original call start.
            # Its allowance must not subtract preflight time a second time.
            total_wall = math.floor(deadline-started)
            C.require(total_wall >= 1 and time.monotonic() < deadline,"AGGREGATE_ADMISSION_DEADLINE")
            limits = self._supervisor.limits_checked({"cpu_seconds":cpu_seconds,
                "wall_seconds":total_wall,"memory_mib":memory_mib,"active_processes":2,
                "stdout_bytes":16384,"stderr_bytes":16384})
            output = self._supervisor.absolute(operation_directory,directory=True,fresh=True)
            for protected in (self._install,self._manifest,*self._pins):
                C.require(not self._supervisor.overlap(output,protected),"AGGREGATE_OUTPUT_OVERLAP")
            output.mkdir()
            receipt_path,header_path = output/"receipt.bin",output/"header.bin"
            self._write(receipt_path,receipt); self._write(header_path,expected_header)
            self._supervisor.save_new(output/"request.json",{"profile_id":self._profile_id,
                "aggregate_image":self._image,"header":list(expected_header),
                "receipt_sha256":_sha(receipt),"receipt_bytes":len(receipt),"limits":limits,
                "authority":"OWNER_EXPECTED_STATEMENT_NOT_PROOF"})
            self._active(); C.require(time.monotonic() < deadline,"AGGREGATE_ADMISSION_DEADLINE")
            process = self._supervisor.supervise([str(self._executable),"verify",self._image,
                str(receipt_path),str(header_path)],self._install,output/"command",limits,
                self._job,started=started)
            self._supervisor.save_new(output/"process.json",process)
            final = process.get("final_job")
            C.require(type(final) is dict and process.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
                and process.get("child_exit_code") == 0 and process.get("direct_child_reaped") is True
                and process.get("job_closed") is True and process.get("cleanup_errors") == []
                and process.get("termination_requested") is False
                and final.get("active_processes") == 0 and final.get("terminated_processes") == 0,
                "AGGREGATE_VERIFIER_REFUSED_OR_UNCLOSED")
            observed_cpu,observed_wall = final.get("cpu_seconds"),process.get("wall_seconds_through_cleanup")
            C.require(type(observed_cpu) in (int,float) and math.isfinite(observed_cpu)
                and 0 <= observed_cpu <= cpu_seconds and type(observed_wall) in (int,float)
                and math.isfinite(observed_wall) and 0 <= observed_wall <= wall_seconds,
                "AGGREGATE_ACTUAL_CPU_OR_WALL")
            self._check_live()
            C.require(self._supervisor.bounded_read(receipt_path,64*MIB) == receipt
                and self._supervisor.bounded_read(header_path,B.HEADER_BYTES) == expected_header,
                "AGGREGATE_EXACT_INPUT_CHANGED")
            bound = bind_output(self._supervisor.bounded_read(output/"command/stdout.txt",16384),
                receipt,expected_header,adopted_image=self._image)
            self._census(output,*output_charge)
            self._supervisor.save_new(output/"binding.json",{"status":"SAME_CALL_AGGREGATE_BOUND_BEFORE_HANDLE",
                "profile_id":self._profile_id,"header":list(expected_header),
                "receipt_sha256":bound["receipt_sha256"],
                "authority":"LOCAL_EVIDENCE_NOT_TRANSFERABLE_PROOF"})
            self._census(output,*output_charge); self._check_live()
            C.require(time.monotonic() < deadline,"AGGREGATE_TOTAL_WALL")
            handle = VerifiedAggregate()
            self._handles[handle] = expected_header,bound["receipt_sha256"],len(receipt)
            return handle
        except BaseException:
            self._revoke(); raise
        finally:
            self._busy = False

    def describe(self, handle):
        """Explicit override: describes only A/H, never returns an I module fact."""
        return self.describe_aggregate(handle)

    def describe_aggregate(self, handle):
        self._member_begin()
        header,digest,count = self._aggregate_record(handle)
        fact = {"header":header,"statement":B.decode_header(header,adopted_image=self._image),
            "receipt_sha256":digest,"receipt_bytes":count,"profile_id":self._profile_id,
            "proof_form":"resolved-aggregate-v2"}
        self._check_live(); return fact

    def select_member(self, handle, exact_journal, index, siblings):
        self._member_begin()
        C.require(type(exact_journal) is bytes and len(exact_journal) == 184
            and type(siblings) is list and len(siblings) <= B.MAX_SIBLINGS
            and all(type(sibling) is bytes and len(sibling) == 32 for sibling in siblings),
            "AGGREGATE_MEMBER_IMMUTABLE_INPUT")
        self._charge_member_bytes(len(exact_journal)+32*len(siblings))
        header,_,_ = self._aggregate_record(handle)
        B.bind_member(header,exact_journal,index,siblings,adopted_image=self._image)
        record = handle,exact_journal,index,tuple(siblings)
        existing = self._member_cache.get(record)
        if existing is not None:
            self._member_record(existing); self._check_live(); return existing
        C.require(len(self._members) < self._member_caps[1],"AGGREGATE_MEMBER_STORAGE")
        self._check_live()
        member = VerifiedAggregateMember()
        self._members[member] = record; self._member_cache[record] = member
        return member

    def describe_member(self, handle):
        self._member_begin()
        _,header,digest,count,exact,index,siblings,member = self._member_record(handle)
        fact = {"module":member["module"],"summary":member["summary"],"journal":exact,
            "aggregate_header":header,"aggregate_image":self._image,"receipt_sha256":digest,
            "receipt_bytes":count,"member_index":index,"siblings":list(siblings),
            "profile_id":self._profile_id,"proof_form":"aggregate-member-not-legacy-receipt"}
        self._check_live(); return fact

    def open_group(self, handle, opening):
        self._member_begin()
        # Caller data is already inside the trusted bounded controller. Encoding
        # allocates before this byte charge; process/decoder bounds still apply.
        raw = C.canonical(opening); self._charge_member_bytes(len(raw))
        _,_,_,_,_,_,_,member = self._member_record(handle)
        copied = C.parse_json(raw)
        group = C.verify_group_opening(member["module"],copied)
        C.require(copied["summary"] == member["summary"],"AGGREGATE_MEMBER_GROUP_SUMMARY")
        result = C.parse_json(C.canonical(group))
        self._check_live(); return result

    def report(self):
        return {"attempts":self._used[0],"submitted_receipt_bytes":self._used[1],
            "reserved_cpu_seconds":self._used[2],"member_calls":self._member_used[0],
            "submitted_member_bytes":self._member_used[1],"live_aggregates":len(self._handles),
            "live_members":len(self._members),"reserved_output_bytes":self._output_reserved[0],
            "reserved_output_entries":self._output_reserved[1],"closed":self._closed,
            "profile_id":self._profile_id,"authority":"LOCAL_ACCOUNTING_NOT_PROOF"}

    def close(self):
        C.require(not self._busy,"AGGREGATE_ADMISSION_CALL_ACTIVE")
        self._revoke()
