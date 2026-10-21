"""Same-call native extension over exact typed I/A receipt frontiers.

This is NOT a new mathematical checker. The retained native relation is invoked
with I even when an A-only owner supplies supervision. Exact configured local
owners discharge typed premises; copied facts/saved reports never suffice.
"""
from dataclasses import asdict
import hashlib
import math
import os
from pathlib import Path
import sys
import time

from admission.verifier import ReceiptVerifier, VerifiedModule
from admission.bindings import journal
from admission import pin_phase as PP
from aggregate_claims.aggregate_admission import (
    AggregateReceiptVerifier, VerifiedAggregate, VerifiedAggregateMember)
from aggregate_claims import bindings as B
from modules import codec as C
from production.producer import parse as parse_local_report
from delta.packet import bind_native, require_closure
from delta_claims.receiver import DeltaVerifier as RetainedDeltaVerifier
from . import packet as P

MIB,need,DeltaError = P.MIB,P.need,P.DeltaError


def _sha(raw): return hashlib.sha256(raw).hexdigest()


class VerifiedMixedDelta:
    """Distinct owner-local warrant closure, neither I nor A receipt authority."""
    __slots__ = ()


class MixedDeltaVerifier:
    """Trusted single-owner controller; finite lifetime, no network or retries.

    All configured owners bound the lifetime, even when a call uses a subset.
    Failed entered receive or detected live-origin/pin failure revokes this owner,
    not independently owned I/A authorities. Windows Jobs are not a sandbox.
    """
    def __init__(self, *, legacy_verifier=None, aggregate_verifier=None,
                 native_executable, runtime_pins, output_directory, envelope=None,
                 operations=8,submitted_bytes=128*MIB,reserved_cpu_seconds=3600,
                 controller_cpu_seconds=600,wall_seconds=3600,
                 output_bytes=512*MIB,output_entries=4096):
        self._started,self._cpu_started = time.monotonic(),time.process_time()
        need(legacy_verifier is None or type(legacy_verifier) is ReceiptVerifier,"MIXED_EXACT_I_OWNER")
        need(aggregate_verifier is None or type(aggregate_verifier) is AggregateReceiptVerifier,
             "MIXED_EXACT_A_OWNER")
        need(legacy_verifier is not None or aggregate_verifier is not None,"MIXED_OWNER_REQUIRED")
        self._owners = self._origins = legacy_verifier,aggregate_verifier
        self._profiles = tuple(None if owner is None else owner.report()["profile_id"] for owner in self._owners)
        # These are relation constants, NOT the image of the supervision donor.
        self._image,self._foundation,self._policy = B.RELATION_IMAGE,B.FOUNDATION,B.POLICY
        if legacy_verifier is not None:
            need((legacy_verifier._image,legacy_verifier._foundation,legacy_verifier._policy)
                 == (self._image,self._foundation,self._policy),"MIXED_I_ADOPTION")
        if aggregate_verifier is not None:
            aggregate_verifier._check_live()
            need((aggregate_verifier._foundation,aggregate_verifier._policy) == (self._foundation,self._policy),
                 "MIXED_A_ADOPTION")
        self._aggregate_image = None if aggregate_verifier is None else aggregate_verifier._image
        donor = aggregate_verifier if aggregate_verifier is not None else legacy_verifier
        self._donor,self._A,self._Job = donor,donor._supervisor,donor._job
        self._envelope = P.Envelope() if envelope is None else envelope
        need(type(self._envelope) is P.Envelope,"MIXED_EXACT_ENVELOPE"); self._envelope.validate()
        values = operations,submitted_bytes,reserved_cpu_seconds,controller_cpu_seconds,wall_seconds,output_bytes,output_entries
        caps = 128,1024*MIB,86400,3600,86400,2*1024*MIB,8192
        need(all(type(v) is int and 0 < v <= cap for v,cap in zip(values,caps)),"MIXED_OWNER_ALLOWANCE")
        self._caps = values
        self._deadline = min(self._started+wall_seconds,*[owner._deadline for owner in self._owners if owner is not None])
        self._closed = self._busy = False
        self._used,self._observed_worker = [0,0,0],0.0
        self._handles,self._cache = {},{}
        # Exact conditional observations from only the last fully admitted
        # packet. These never discharge a current packet's parent obligations.
        self._native_memo = {}
        self._native_checks,self._native_reuses = 0,0
        need(type(runtime_pins) is dict and 1 <= len(runtime_pins) <= 128,"MIXED_NATIVE_PIN_MAP")
        self._pins = {}
        for name,pin in runtime_pins.items():
            C.fields(pin,{"sha256","bytes"}); C.digest_string(pin["sha256"])
            need(0 < C.uint(pin["bytes"],128*MIB),"MIXED_NATIVE_PIN_SIZE")
            path = self._A.absolute(name)
            need(path not in self._pins,"MIXED_DUPLICATE_PIN"); self._pins[path] = dict(pin)
        need(sum(pin["bytes"] for pin in self._pins.values()) <= 512*MIB,"MIXED_PIN_TOTAL")
        self._native = self._A.absolute(native_executable)
        root = Path(__file__).resolve().parents[1]
        names = ("mixed_claims","mixed_claims.packet","mixed_claims.receiver",
            "admission","admission.verifier","admission.bindings","admission.pin_phase",
            "aggregate_claims","aggregate_claims.aggregate_admission","aggregate_claims.admission_binding",
            "aggregate_claims.bindings","modules","modules.codec","delta","delta.packet","delta.receiver",
            "delta_claims","delta_claims.receiver","delta_claims.claims","production","production.producer")
        self._required_origins = {name:root/(name.replace(".","/")+("/__init__.py" if "." not in name else ".py"))
                                  for name in names}
        need({self._native,*self._required_origins.values()} <= set(self._pins),"MIXED_REQUIRED_SOURCE_PINS")
        self._profile_id = C.hash_value("local-mixed-exact-warrants-v1",{
            "owners":list(self._profiles),"relation_image":self._image,"aggregate_image":self._aggregate_image,
            "foundation":self._foundation,"policy":self._policy,"schema":P.SCHEMA,
            "envelope":asdict(self._envelope),"pins":{str(k):v for k,v in self._pins.items()}})
        self._origin_profile = self._profile_id
        self._check()
        self._output = self._A.absolute(output_directory,directory=True,fresh=True)
        protected = list(self._pins)
        for owner in self._owners:
            if owner is not None: protected.extend((owner._install,owner._manifest,*owner._pins))
        for path in protected: need(not self._A.overlap(self._output,path),"MIXED_OUTPUT_OVERLAP")
        self._output.mkdir()
        self._save(self._output/"owner.json",{"profile":self._profile_id,"owners":list(self._profiles),
            "envelope":asdict(self._envelope),"allowance":list(values),"authority":"LOCAL_OWNER_SELECTION_NOT_PROOF"})
        self._owner_raw = self._A.bounded_read(self._output/"owner.json",MIB)
        self._check(); self._census()

    def _revoke(self):
        self._closed = True; self._handles.clear(); self._cache.clear(); self._native_memo.clear()

    def _active(self,deadline=None):
        try:
            need(not self._closed and len(self._owners) == 2
                 and all(owner is origin for owner,origin in zip(self._owners,self._origins)),
                 "MIXED_CLOSED_OR_CHANGED_ORIGIN")
            need(time.monotonic() < min(self._deadline,self._deadline if deadline is None else deadline),
                 "MIXED_ORIGINAL_DEADLINE","RESOURCE_INCOMPLETE")
            need(time.process_time()-self._cpu_started <= self._caps[3],"MIXED_CONTROLLER_CPU","RESOURCE_INCOMPLETE")
            need(self._profile_id == self._origin_profile
                 and (self._image,self._foundation,self._policy) == (B.RELATION_IMAGE,B.FOUNDATION,B.POLICY),
                 "MIXED_PROFILE_CHANGED")
            donor = self._owners[1] if self._owners[1] is not None else self._owners[0]
            need(self._donor is donor and self._A is donor._supervisor and self._Job is donor._job,
                 "MIXED_SUPERVISION_ORIGIN_CHANGED")
            for tag,owner in enumerate(self._owners):
                if owner is None: continue
                need(type(owner) is (ReceiptVerifier if tag == 0 else AggregateReceiptVerifier),"MIXED_OWNER_TYPE_CHANGED")
                owner._active()
                need(owner.report()["profile_id"] == self._profiles[tag],"MIXED_ORIGIN_PROFILE_CHANGED")
                need(owner._image == (self._image if tag == 0 else self._aggregate_image)
                     and (owner._foundation,owner._policy) == (self._foundation,self._policy),"MIXED_ORIGIN_ADOPTION_CHANGED")
        except BaseException:
            self._revoke(); raise

    def _check(self,deadline=None):
        try:
            # Synchronous installation validation only; never enclose receive
            # work, subprocesses or result promotion. Import _live may explicitly
            # register this original owner and own the sole final sweep.
            with PP.borrow_or_phase(lambda: self._active(deadline), owner=self):
                self._check_phase(deadline)
        except BaseException:
            self._revoke(); raise

    def _check_phase(self,deadline=None):
        try:
            self._active(deadline)
            for name,path in self._required_origins.items():
                module = sys.modules.get(name)
                need(module is not None and type(getattr(module,"__file__",None)) is str
                     and Path(module.__file__).resolve() == path,"MIXED_LOADED_SOURCE_ORIGIN:"+name)
            need(ReceiptVerifier is sys.modules["admission.verifier"].ReceiptVerifier
                 and PP is sys.modules["admission.pin_phase"]
                 and AggregateReceiptVerifier is sys.modules["aggregate_claims.aggregate_admission"].AggregateReceiptVerifier
                 and P is sys.modules["mixed_claims.packet"] and C is sys.modules["modules.codec"]
                 and B is sys.modules["aggregate_claims.bindings"]
                 and bind_native is sys.modules["delta.packet"].bind_native
                 and require_closure is sys.modules["delta.packet"].require_closure
                 and RetainedDeltaVerifier is sys.modules["delta_claims.receiver"].DeltaVerifier
                 and journal is sys.modules["admission.bindings"].journal
                 and B.journal is journal and VerifiedModule is sys.modules["admission.verifier"].VerifiedModule
                 and VerifiedAggregate is sys.modules["aggregate_claims.aggregate_admission"].VerifiedAggregate
                 and VerifiedAggregateMember is sys.modules["aggregate_claims.aggregate_admission"].VerifiedAggregateMember
                 and parse_local_report is sys.modules["production.producer"].parse,
                 "MIXED_IMPORTED_SYMBOL_ORIGIN")
            for tag,owner in enumerate(self._owners):
                if owner is not None:
                    if tag == 0: owner._check_install()
                    else: owner._check_live()
            for path,pin in self._pins.items():
                self._active(deadline); need(PP.check_pin(self._A.pin,path,pin),"MIXED_INSTALL_PIN_CHANGED")
            if hasattr(self,"_owner_raw"):
                need(self._A.bounded_read(self._output/"owner.json",MIB) == self._owner_raw,"MIXED_OWNER_SELECTION_CHANGED")
            self._active(deadline)
        except BaseException:
            self._revoke(); raise

    @staticmethod
    def _write(path,raw):
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())

    def _save(self,path,value): self._write(path,C.canonical(value))

    @staticmethod
    def _retain_native(records,byte_count,witness,record,entry_cap,byte_cap):
        """Bound inert pending records only; this never promotes live authority."""
        if witness not in records and len(records) < min(entry_cap,16) \
                and byte_count+len(witness) <= min(byte_cap,16*MIB):
            records[witness] = record
            return byte_count+len(witness)
        return byte_count

    def _census(self,reserve=0,entries=0):
        size,count = reserve,entries
        for directory,dirs,names in os.walk(self._output,followlinks=False):
            for name in dirs+names:
                self._active(); path = Path(directory)/name; count += 1
                self._A.absolute(path,directory=name in dirs)
                if name in names: size += path.stat().st_size
                need(size <= self._caps[5] and count <= self._caps[6],"MIXED_OUTPUT_CAP","RESOURCE_INCOMPLETE")
        need(size <= self._caps[5] and count <= self._caps[6],"MIXED_OUTPUT_CAP","RESOURCE_INCOMPLETE")

    def _claim_live(self,tag,handle,digest,receipt_bytes,statement,deadline=None):
        self._active(deadline); owner = self._owners[tag]
        need(owner is not None,"MIXED_MISSING_ORIGIN","UNSUPPORTED_PROOF_FORM")
        need(type(handle) is (VerifiedModule if tag == 0 else VerifiedAggregate),"MIXED_EXACT_CLAIM_HANDLE")
        fact = owner.describe(handle)
        need(fact["profile_id"] == self._profiles[tag] and fact["receipt_sha256"] == digest,
             "MIXED_LIVE_CLAIM_BINDING")
        if tag == 0:
            need(fact["journal"] == statement and fact["summary"] == journal(statement)["summary"],
                 "MIXED_EXACT_I_JOURNAL")
        else:
            need(fact["header"] == statement and fact["receipt_bytes"] == receipt_bytes,"MIXED_EXACT_A_HEADER")
        self._active(deadline); return fact

    def _live_frontiers(self,selected,deadline=None):
        self._active(deadline)
        for tag,claim_handle,member_handle,digest,count,statement,exact,index,siblings in selected:
            self._claim_live(tag,claim_handle,digest,count,statement,deadline)
            if tag == 1:
                need(type(member_handle) is VerifiedAggregateMember,"MIXED_EXACT_MEMBER_HANDLE")
                live = self._owners[1].describe_member(member_handle)
                need(live["profile_id"] == self._profiles[1] and live["aggregate_image"] == self._aggregate_image
                     and live["aggregate_header"] == statement and live["journal"] == exact
                     and live["summary"] == journal(exact)["summary"] and live["receipt_sha256"] == digest
                     and live["receipt_bytes"] == count and live["member_index"] == index
                     and tuple(live["siblings"]) == siblings,"MIXED_LIVE_A_MEMBER_BINDING")
            else: need(exact == statement and member_handle is None,"MIXED_LIVE_I_FRONTIER")
        self._active(deadline)

    def receive(self,packet,expected_summary,*,native_cpu_seconds=30,receipt_cpu_seconds=30,
                wall_seconds=600,memory_mib=1024):
        entered = time.monotonic(); self._active(); need(not self._busy,"MIXED_SINGLE_OWNER")
        for value,cap in ((native_cpu_seconds,600),(receipt_cpu_seconds,600),(wall_seconds,600),(memory_mib,4096)):
            need(type(value) is int and 0 < value <= cap,"MIXED_CALL_LIMIT")
        need(memory_mib >= 64 and type(packet) is bytes,"MIXED_IMMUTABLE_INPUT_OR_MEMORY")
        need(self._used[0]+1 <= self._caps[0] and self._used[1]+len(packet) <= self._caps[1],
             "MIXED_INPUT_ALLOWANCE","RESOURCE_INCOMPLETE")
        self._used[0] += 1; self._used[1] += len(packet); self._busy = True
        deadline,directory = min(self._deadline,entered+wall_seconds),None
        try:
            claims,frontiers,witnesses,census = P.parse_packet(packet,self._envelope,aggregate_image=self._aggregate_image)
            need(all(self._owners[tag] is not None for tag,unused,receipt in claims),
                 "MIXED_REQUIRED_PROOF_OWNER_ABSENT","UNSUPPORTED_PROOF_FORM")
            C.validate_summary(expected_summary); summary = C.canonical(expected_summary)
            need((expected_summary["foundation"],expected_summary["policy"]) == (self._foundation,self._policy),
                 "MIXED_REQUESTED_POLICY")
            need(C.canonical(witnesses[-1][2]) == summary,"MIXED_LAST_DELTA_REQUESTED_TARGET")
            reserve = len(claims)*receipt_cpu_seconds+len(witnesses)*native_cpu_seconds
            need(self._used[2]+reserve <= self._caps[2],"MIXED_CPU_ALLOWANCE","RESOURCE_INCOMPLETE")
            self._used[2] += reserve # Includes cache hits; never refunded on failure.
            self._check(deadline)
            self._census(len(packet)+census["witness_bytes"]+census["receipt_bytes"]
                         +len(witnesses)*6*MIB+len(claims)*MIB+MIB,12*(len(claims)+len(witnesses))+8)
            directory = self._output/str(self._used[0]); directory.mkdir()
            self._write(directory/"packet.json",packet)
            self._save(directory/"request.json",{"profile":self._profile_id,"packet_sha256":_sha(packet),
                "summary":expected_summary,"census":census,"worker_cpu_reserved":reserve,
                "native_cpu_seconds":native_cpu_seconds,"receipt_cpu_seconds":receipt_cpu_seconds,
                "wall_seconds":wall_seconds,"memory_mib":memory_mib})
            claim_handles = []
            for claim_index,(tag,statement,receipt) in enumerate(claims):
                self._check(deadline); owner = self._owners[tag]
                key = tag,self._profiles[tag],statement,_sha(receipt),len(receipt)
                handle = self._cache.get(key)
                if handle is None:
                    remaining = math.floor(deadline-time.monotonic())
                    need(remaining >= 1,"MIXED_CLAIM_DEADLINE","RESOURCE_INCOMPLETE")
                    operation = directory/("claim-"+str(claim_index))
                    expected = journal(statement)["summary"] if tag == 0 else statement
                    handle = owner.receive(receipt,expected,operation,cpu_seconds=receipt_cpu_seconds,
                                           wall_seconds=remaining,memory_mib=memory_mib)
                    process = parse_local_report(self._A.bounded_read(operation/"process.json",MIB))
                    self._observed_worker += RetainedDeltaVerifier._clean(process,receipt_cpu_seconds,remaining)
                    self._claim_live(tag,handle,key[3],len(receipt),statement,deadline)
                    self._cache[key] = handle
                self._claim_live(tag,handle,key[3],len(receipt),statement,deadline)
                claim_handles.append(handle)
            graph,representations,selected = {},{},[]
            for frontier in frontiers:
                claim_index,exact,index,siblings = frontier
                tag,statement,receipt = claims[claim_index]; handle = claim_handles[claim_index]
                member = None
                if tag == 1: member = self._owners[1].select_member(handle,exact,index,list(siblings))
                selected.append((tag,handle,member,_sha(receipt),len(receipt),statement,exact,index,siblings))
                graph[exact] = ()
                representations[exact] = ("i-receipt-frontier" if tag == 0 else "a-member-frontier",
                                          _sha(P.frontier_evidence(claims[claim_index],frontier)))
            self._live_frontiers(selected,deadline)
            target = None
            pending_native,native_observations,pending_bytes = {},[],0
            for index,(witness,parents,own_summary,rank) in enumerate(witnesses):
                self._check(deadline); self._live_frontiers(selected,deadline)
                need(all(parent in graph for parent in parents),"MIXED_UNESTABLISHED_PARENT")
                need(len(set(parents)) == len(parents) and rank ==
                     (1+max(journal(p)["rank"] for p in parents) if parents else 0),"MIXED_ACTUAL_EXACT_RANK")
                # A bytes key uses complete equality, not digest equality. The
                # record is private to this exact live owner, not a saved PASS.
                cached = self._native_memo.get(witness)
                if cached is None:
                    path = directory/("delta-"+str(index)+".json"); self._write(path,witness)
                    remaining = math.floor(deadline-time.monotonic())
                    need(remaining >= 1,"MIXED_NATIVE_DEADLINE","RESOURCE_INCOMPLETE")
                    limits = self._A.limits_checked({"cpu_seconds":native_cpu_seconds,"wall_seconds":remaining,
                        "memory_mib":memory_mib,"active_processes":2,"stdout_bytes":4*MIB,"stderr_bytes":MIB})
                    command = directory/("native-"+str(index))
                    self._native_checks += 1
                    process = self._A.supervise([str(self._native),"check",self._image,str(path)],
                                                self._donor._install,command,limits,self._Job)
                    self._save(directory/("process-"+str(index)+".json"),process)
                    self._observed_worker += RetainedDeltaVerifier._clean(process,native_cpu_seconds,remaining)
                    self._check(deadline); self._live_frontiers(selected,deadline)
                    need(self._A.bounded_read(path,16*MIB) == witness,"MIXED_NATIVE_INPUT_CHANGED")
                    target,actual_parents = bind_native(self._A.bounded_read(command/"stdout.txt",4*MIB),
                        witness,parents,own_summary,rank,self._image,self._foundation,self._policy)
                    observation = "NATIVE_EXECUTED_CONDITIONAL_CHECK"
                else:
                    origin,profile,image,foundation,policy,actual_parents,actual_rank,target = cached
                    need(origin is self and (profile,image,foundation,policy,actual_parents,actual_rank) ==
                         (self._profile_id,self._image,self._foundation,self._policy,parents,rank),
                         "MIXED_NATIVE_MEMO_BINDING")
                    self._check(deadline); self._live_frontiers(selected,deadline)
                    decoded = journal(target)
                    need(target[12:44].hex() == self._image and decoded["foundation"] == self._foundation
                         and decoded["policy"] == self._policy and decoded["summary"] == own_summary
                         and decoded["rank"] == rank,"MIXED_NATIVE_MEMO_CONCLUSION")
                    self._native_reuses += 1
                    observation = "SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION"
                need(target not in graph and all(p in graph for p in actual_parents),"MIXED_ACTUAL_GRAPH_BINDING")
                graph[target] = actual_parents; representations[target] = "native-delta",_sha(witness)
                native_observations.append({"index":index,"observation":observation,
                    "witness_sha256":_sha(witness),"witness_bytes":len(witness),"journal":list(target)})
                # Pending records have no authority until complete final
                # admission. Overflow only loses an optional future hit.
                pending_bytes = self._retain_native(pending_native,pending_bytes,witness,
                    (self,self._profile_id,self._image,self._foundation,self._policy,actual_parents,rank,target),
                    self._envelope.deltas,self._envelope.witness_bytes)
            require_closure(target,graph)
            need(C.canonical(journal(target)["summary"]) == summary,"MIXED_CHECKED_TARGET_IDENTITY")
            self._check(deadline); self._live_frontiers(selected,deadline)
            need(self._A.bounded_read(directory/"packet.json",self._envelope.packet_bytes) == packet,"MIXED_PACKET_CHANGED")
            self._census()
            self._save(directory/"RESULT.json",{"status":"MIXED_BOUND_BEFORE_LIVE_PROMOTION",
                "profile":self._profile_id,"journal":list(target),"packet_sha256":_sha(packet),
                "census":census,"native_observations":native_observations,
                "authority":"SAVED_REPORT_NOT_TRANSFERABLE_PROOF"})
            self._census(); self._check(deadline); self._live_frontiers(selected,deadline); self._active(deadline)
            handle = VerifiedMixedDelta()
            self._handles[handle] = target,packet,tuple(selected),tuple(graph),representations
            self._native_memo = pending_native
            return handle
        except BaseException as error:
            self._revoke()
            if directory is not None:
                self._save(directory/"FINALIZATION-FAILED.json",{"status":"NO_LIVE_MIXED_HANDLE",
                    "reason":type(error).__name__+": "+str(error)[:2000]})
            if isinstance(error,C.StructureError): raise DeltaError("INVALID_OR_UNBOUND",str(error)) from error
            raise
        finally: self._busy = False

    def describe(self,handle):
        try:
            self._check()
            need(type(handle) is VerifiedMixedDelta and handle in self._handles,"MIXED_FOREIGN_HANDLE")
            exact,packet,selected,unused,representations = self._handles[handle]
            self._live_frontiers(selected); decoded = journal(exact)
            return {"module":decoded["module"],"summary":decoded["summary"],"journal":exact,
                "profile_id":self._profile_id,"packet_sha256":_sha(packet),
                "proof_form":"mixed-bounded-native-delta-not-receipt"}
        except BaseException:
            self._revoke(); raise

    def members(self,handle):
        self.describe(handle)
        unused,packet,selected,inventory,representations = self._handles[handle]
        result = []
        for exact in inventory:
            decoded = journal(exact)
            result.append({"module":decoded["module"],"summary":decoded["summary"],"journal":exact,
                "profile_id":self._profile_id,"packet_sha256":_sha(packet),
                "proof_form":representations[exact][0],"evidence_sha256":representations[exact][1]})
        self.describe(handle); return result

    def describe_member(self,handle,exact_journal):
        journal(exact_journal)
        for item in self.members(handle):
            if item["journal"] == exact_journal: return item
        raise DeltaError("MISSING_MATERIAL","MIXED_EXACT_WARRANT_NOT_IN_CLOSURE")

    def variants(self,handle,module):
        C.digest_string(module)
        return sorted((item for item in self.members(handle) if item["module"] == module),key=lambda item:item["journal"])

    def open_member_group(self,handle,exact_journal,opening):
        accepted = self.describe_member(handle,exact_journal)
        # Detached result prevents a caller mutating an authenticated stored fact.
        copied = C.parse_json(C.canonical(opening))
        group = C.verify_group_opening(accepted["module"],copied)
        need(copied["summary"] == accepted["summary"],"MIXED_MEMBER_GROUP_SUMMARY")
        self.describe_member(handle,exact_journal); return group

    def open_group(self,handle,opening):
        accepted = self.describe(handle)
        return self.open_member_group(handle,accepted["journal"],opening)

    def export_packet(self,handle):
        self.describe(handle); return self._handles[handle][1]

    def report(self):
        return {"attempts":self._used[0],"submitted_bytes":self._used[1],"reserved_worker_cpu":self._used[2],
            "observed_success_worker_cpu":self._observed_worker,"live_handles":len(self._handles),
            "native_check_attempts":self._native_checks,"native_reuse_observations":self._native_reuses,
            "retained_native_records":len(self._native_memo),
            "retained_native_witness_bytes":sum(len(witness) for witness in self._native_memo),
            "closed":self._closed,"profile_id":self._profile_id,"mathematical_authority":False,
            "scope":"RESERVATIONS_RETAIN_FAILURES;WORKER_OBSERVATION_PARTIAL;CONTROLLER_INSTALL_TRUSTED"}

    def close(self):
        need(not self._busy,"MIXED_CALL_ACTIVE"); self._revoke()
