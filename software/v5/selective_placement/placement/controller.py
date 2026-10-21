"""One owner-local structural placement transaction; no HTTP/DHT or verifier."""
from copy import deepcopy
import secrets
import time

from discovery import formal_features as F
from evidence_network.transport import EvidenceAcquisition
from location.protocol import OwnerEgressPolicy
from modules import codec as C
from transport.receipt_client import AcquisitionBudget
from . import codec as P
from .ledger import PlacementLedger

_ISSUE = object()


def _now_ms(): return int(time.time()*1000)


class PlacementServiceGrant:
    """Exact controller-issued object, never reconstructed from saved JSON."""
    __slots__ = ("owner","run_id","deadline","started_cpu","cpu_limit","call_cap","calls","closed")
    def __init__(self,key,owner,wall_seconds,cpu_seconds,calls):
        F.need(key is _ISSUE,"PLACEMENT_LOCAL_ISSUER_ONLY")
        self.owner,self.run_id = owner,secrets.token_hex(32)
        self.deadline,self.started_cpu = time.monotonic()+wall_seconds,time.process_time()
        self.cpu_limit,self.call_cap,self.calls,self.closed = cpu_seconds,calls,0,False


class PlacementCleanupError(RuntimeError):
    """Cleanup is uncertain; any committed placement remains historical state."""
    def __init__(self,request_id,receipt_committed,original_error):
        super().__init__("PLACEMENT_ACQUISITION_CLEANUP_FAILED:"+request_id+";DURABLE_STATE_NOT_ROLLED_BACK")
        self.request_id,self.receipt_committed = request_id,receipt_committed
        self.original_error = original_error


class _Contact:
    """Exact locally selected endpoint with the owner guard on every dial."""
    def __init__(self,owner,endpoint):
        self._owner,self._endpoint,self._original = owner,endpoint,endpoint
    def __getattr__(self,name): return getattr(self._endpoint,name)
    def validate(self):
        self._owner._active()
        F.need(self._endpoint is self._original,"PLACEMENT_CONTACT_CHANGED")
        selected = self._owner.policy.endpoint({name:getattr(self._endpoint,name)
                         for name in ("host","port","tls","server_name")})
        F.need(selected == self._endpoint,"PLACEMENT_CONTACT_POLICY")
        self._endpoint.validate(); return self


class _OwnedAcquisition(EvidenceAcquisition):
    """Compose CPU/grant checks with inherited nested before-COMMIT hooks."""
    def __init__(self,owner,*args,**kwargs):
        self._placement_owner = owner
        super().__init__(*args,**kwargs)
    def _active(self):
        self._placement_owner._active()
        super()._active()


class PlacementController:
    def __init__(self,ledger,egress):
        F.need(type(ledger) is PlacementLedger,"PLACEMENT_EXACT_LEDGER")
        ledger.active()
        previous = getattr(ledger,"_controller",None)
        F.need(previous is None or previous.closed,"PLACEMENT_CONTROLLER_ALREADY_OPEN")
        self.ledger,self._ledger = ledger,ledger
        self.workspace,self._workspace = ledger.workspace,ledger.workspace
        self.policy = OwnerEgressPolicy(egress); self._egress = F.compact(egress)
        self._service,self._service_binding = None,None
        self._busy,self.closed,self._current = False,False,None
        ledger._controller = self

    def _active(self,service=None):
        grant = self._service if service is None else service
        F.need(not self.closed and self.ledger is self._ledger and self.workspace is self._workspace
               and getattr(self.ledger,"_controller",None) is self,"PLACEMENT_CONTROLLER_ORIGIN")
        self.ledger.active()
        F.need(type(grant) is PlacementServiceGrant and grant is self._service and grant.owner is self
               and not grant.closed,"PLACEMENT_EXACT_LIVE_SERVICE_GRANT")
        F.need((grant.run_id,grant.deadline,grant.started_cpu,grant.cpu_limit,grant.call_cap)
               == self._service_binding,"PLACEMENT_SERVICE_GRANT_CHANGED")
        F.need(time.monotonic() < grant.deadline and time.process_time()-grant.started_cpu <= grant.cpu_limit,
               "PLACEMENT_SERVICE_RESOURCE_LIMIT")
        F.need(F.compact(self.policy._config) == self._egress,"PLACEMENT_EGRESS_CHANGED")
        if self._current is not None:
            value,policy,recovery,unused = self._current
            self._window(value,policy,recovery)

    def _window(self,value,policy,recovery):
        now = _now_ms()
        F.need(now < value["retention_end_ms"] <= self.ledger.config["retention_not_after_ms"],
               "PLACEMENT_RETENTION_WINDOW")
        if not recovery:
            F.need(now < policy["write_until_ms"] and now < self.ledger.config["admission_close_ms"],
                   "PLACEMENT_WRITE_OR_ADMISSION_EXPIRED")

    def _call(self,service,*,idle=True):
        self._active(service)
        F.need(service.calls < service.call_cap,"PLACEMENT_SERVICE_CALL_CAP")
        service.calls += 1
        if idle: F.need(not self._busy,"PLACEMENT_BUSY")

    def start_service(self,*,wall_seconds=600,controller_cpu_seconds=120,calls=128):
        F.need(not self.closed and self._service is None,"PLACEMENT_SERVICE_ALREADY_STARTED")
        for value,cap in ((wall_seconds,3600),(controller_cpu_seconds,3600),(calls,8192)):
            F.uint(value,1,cap,"PLACEMENT_SERVICE_LIMIT")
        grant = PlacementServiceGrant(_ISSUE,self,wall_seconds,controller_cpu_seconds,calls)
        self._service = grant
        self._service_binding = grant.run_id,grant.deadline,grant.started_cpu,grant.cpu_limit,grant.call_cap
        try: self.ledger.start_run(grant.run_id,lambda:self._active(grant))
        except BaseException:
            grant.closed = True
            raise
        return grant

    def issue_token(self,service,source,*,write_until_ms,retention_until_ms,limits):
        self._call(service)
        selected = self.policy.endpoint(source)
        now = _now_ms(); cfg = self.ledger.config
        F.uint(write_until_ms,1,2**53-1); F.uint(retention_until_ms,1,2**53-1)
        F.need(now < write_until_ms <= cfg["admission_close_ms"]
               and now < retention_until_ms <= cfg["retention_not_after_ms"],"PLACEMENT_TOKEN_HORIZON")
        allowance = P.limits(limits)
        F.need(all(allowance[key] <= cfg["limits"][key] for key in P.RESOURCES),"PLACEMENT_TOKEN_SUBLIMIT")
        policy = {"source":{key:getattr(selected,key) for key in ("host","port","tls","server_name")},
                  "write_until_ms":write_until_ms,"retention_until_ms":retention_until_ms,"limits":allowance}
        def guard():
            self._active(service)
            F.need(_now_ms() < min(write_until_ms,cfg["admission_close_ms"]),"PLACEMENT_TOKEN_ISSUE_EXPIRED")
        token,identifier = self.ledger.issue(policy,guard)
        return {"token":token,"grant_id":identifier,"generation":cfg["generation"],
                "write_until_ms":write_until_ms,"retention_until_ms":retention_until_ms,**P.FLAGS}

    def status(self,service,token,request_id):
        self._call(service,idle=False)
        auth = self.ledger.authenticate(token)
        return self.ledger.public(self.ledger.request(request_id,auth[0]))

    def _bytes(self,count):
        self._active(); F.uint(count,0,2**40,"PLACEMENT_STRUCTURAL_INPUT_COUNT")
        self._structural_bytes += count
        # The original reservation funds two finite passes. Even an uncertain
        # first pass consumes its half; recovery cannot reset that allowance.
        F.need(self._structural_bytes <= self._current[3]["structural_bytes"]//2,
               "PLACEMENT_STRUCTURAL_BYTE_CAP")

    def _local_group(self,value):
        store = self.workspace.modules
        row = store.db.execute("SELECT n.idx,length(g.opening) FROM names n LEFT JOIN groups g "
            "ON g.module=n.module AND g.idx=n.idx WHERE n.module=? AND n.name=?",
            (value["module_id"],C.name_key(value["relative_name"]))).fetchone()
        if row is None: return None
        F.need(type(row[1]) is int and 0 < row[1] <= value["opening_max_bytes"],"PLACEMENT_LOCAL_GROUP_SIZE")
        self._bytes(row[1])
        return store.get_group(value["module_id"],value["relative_name"],row[0])

    def _local_packet(self,value):
        store = self.workspace.packets
        row = store.db.execute("SELECT size,length(blob) FROM packets WHERE digest=?",(value["packet_sha256"],)).fetchone()
        if row is None: return None
        F.need(row == (value["packet_bytes"],value["packet_bytes"]),"PLACEMENT_LOCAL_PACKET_SIZE")
        self._bytes(value["packet_bytes"])
        return store.get(value["packet_sha256"],value["packet_bytes"])

    def _local_body(self,value,descriptor,row):
        store = self.workspace.modules
        found = store.db.execute("SELECT length(expression) FROM bodies WHERE module=? AND universes=? AND hash=?",
            (value["module_id"],descriptor["universes"],row["body_hash"])).fetchone()
        if found is None: return None
        F.need(type(found[0]) is int and 0 < found[0] <= row["max_bytes"],"PLACEMENT_LOCAL_BODY_SIZE")
        self._bytes(found[0])
        body = store.get_body(value["module_id"],value["relative_name"],descriptor["universes"],row["body_hash"])
        F.need(len(C.canonical(body)) <= row["max_bytes"],"PLACEMENT_BODY_RESPONSE_BOUND")
        return body

    def _store_counts(self):
        self._active()
        return {"modules":self.workspace.modules.status()["counts"],
                "packets":self.workspace.packets.status()["counts"],"index":self.workspace.index.status()}

    async def submit(self,service,token,raw):
        self._call(service)
        value = P.manifest(raw,self.ledger.config)
        F.need(P.cell(self.workspace.adapter,value["fingerprint"])[0] == value["cell"],"PLACEMENT_PROPOSED_CELL")
        auth = self.ledger.authenticate(token); policy = auth[2]
        def reserve_guard():
            self._active(service); self._window(value,policy,False)
        row,fresh = self.ledger.reserve(auth,raw,value,_now_ms(),
            self.workspace.index.limits["max_logical_bytes"],reserve_guard)
        if not fresh: return self.ledger.public(row)
        return await self._run(service,row,value,policy,recovery=False)

    async def reconcile(self,service,request_id):
        self._call(service)
        row = self.ledger.request(request_id)
        if row["phase"] == "RECEIPT_COMMITTED": return self.ledger.public(row)
        value = P.manifest(row["manifest"],self.ledger.config)
        def recovery_guard():
            self._active(service); self._window(value,None,True)
        # Commit consumption first; a crash cannot restore the prepaid pass.
        row = self.ledger.recovery(request_id,recovery_guard)
        return await self._run(service,row,value,None,recovery=True)

    async def _run(self,service,row,value,policy,*,recovery):
        self._busy = True
        self._current = value,policy,recovery,row["reservation"]
        self._structural_bytes = 0
        acquisition = None
        rid = row["request_id"]
        original_error,receipt_committed = None,False
        try:
            self._active(service); before = self._store_counts()
            if not recovery:
                self.ledger.phase(rid,"PULLING",self._active)
                endpoint = self.policy.endpoint(policy["source"])
                budget = AcquisitionBudget(service.deadline,{
                    "requests":row["reservation"]["requests"],"reply_bytes":row["reservation"]["reply_bytes"],
                    "verify_attempts":1,"verification_input_bytes":1,"worker_cpu_seconds":1})
                acquisition = _OwnedAcquisition(self,self.workspace.adapter,{"source":_Contact(self,endpoint)},
                    self.workspace.packets.profile,budget,self.workspace.modules,self.workspace.packets,verifier=None)
            group = self._local_group(value)
            if group is None:
                F.need(not recovery,"PLACEMENT_RECOVERY_GROUP_NOT_RETAINED")
                await acquisition.declaration("source",value["module_id"],value["relative_name"],value["opening_max_bytes"])
                group = self._local_group(value)
            F.need(group is not None,"PLACEMENT_GROUP_READBACK")
            opening,descriptor = group
            self._bytes(value["export_object_bytes"])
            raw,described,feature = P.checked_export(self.workspace.adapter,value,opening)
            self._active()
            packet = self._local_packet(value)
            if packet is None:
                F.need(not recovery,"PLACEMENT_RECOVERY_PACKET_NOT_RETAINED")
                offers = await acquisition.offers("source",value["module_id"],max_offers=4,max_bytes=4096)
                wanted = {"packet_sha256":value["packet_sha256"],"packet_bytes":value["packet_bytes"]}
                F.need(wanted in offers["packets"],"PLACEMENT_PACKET_NOT_OFFERED")
                await acquisition.packet("source",value["module_id"],wanted)
                packet = self._local_packet(value)
            F.need(packet is not None,"PLACEMENT_PACKET_READBACK")
            self._bytes(len(packet))
            target,census = self.workspace.packets.inspect(value["module_id"],packet)
            F.need(target == opening["summary"],"PLACEMENT_PACKET_OPENING_SUMMARY")
            resolved = self.workspace.adapter.resolve(described["record"],raw)
            body_commitments = []
            for requested in value["bodies"]:
                body = self._local_body(value,descriptor,requested)
                if body is None:
                    F.need(not recovery,"PLACEMENT_RECOVERY_BODY_NOT_RETAINED")
                    await acquisition.body("source",resolved,requested["body_hash"],requested["max_bytes"])
                    body = self._local_body(value,descriptor,requested)
                F.need(body is not None,"PLACEMENT_BODY_READBACK")
                body_commitments.append({"body_hash":requested["body_hash"],
                    "response_sha256":P.digest(C.canonical(body)),"response_bytes":len(C.canonical(body))})
            self._active(); self.ledger.phase(rid,"CUSTODIED",self._active)
            self._bytes(len(raw))
            admitted = self.workspace.index.admit(raw,value["export_id"],before_commit=self._active)
            F.need(admitted["record"] == described["record"],"PLACEMENT_INDEX_RECORD_BINDING")
            snapshot = self.workspace.index.snapshot(admitted["snapshot_id"])
            held = self.workspace.index._record(admitted["record_id"])
            F.need(held == admitted["record"],"PLACEMENT_INDEX_READBACK")
            self._active(); self.ledger.phase(rid,"INDEXED",self._active)
            after = self._store_counts()
            new_logical = {name:after[name]["logical_bytes"]-before[name]["logical_bytes"]
                           for name in ("modules","packets")}
            new_logical["index"] = after["index"]["logical"]-before["index"]["logical"]
            outcome = {"status":"INDEXED_UNADVERTISED","request_id":rid,
                "service_epoch":self.ledger.config["service_epoch"],"generation":self.ledger.config["generation"],
                "namespace":value["namespace"],"wire_profile_id":value["wire_profile_id"],
                "export_id":value["export_id"],"record":admitted["record"],"record_id":admitted["record_id"],
                "snapshot_id":admitted["snapshot_id"],"snapshot":snapshot,
                "route":{"status":"INTENT_ONLY","cell":value["cell"],"features":[feature],"stripe":0},
                "export_object_sha256":value["export_object_sha256"],"export_object_bytes":len(raw),
                "packet_sha256":value["packet_sha256"],"packet_bytes":len(packet),"bodies":body_commitments,
                "retention_end_ms":value["retention_end_ms"],
                "service_not_after_ms":_now_ms()+max(0,int((service.deadline-time.monotonic())*1000)),
                "reservation":row["reservation"],"recovery":recovery,
                "reservation_semantics":"CUMULATIVE_NONREFUNDABLE_AUTHORIZATION_NOT_PHYSICAL_FREE_SPACE",
                "observed":{"structural_input_bytes":self._structural_bytes,"store_counts_before":before,
                    "store_counts_after":after,"new_store_logical_bytes":new_logical,
                    "index_work":admitted["charged"],"packet_census":census,
                    "acquisition":None if acquisition is None else acquisition.report()},
                "assurance":"OWNER_LOCAL_STRUCTURAL_CUSTODY_AND_INDEX_READBACK_NOT_REMOTE_ACK",**P.FLAGS}
            self.ledger.finish(rid,outcome,self._active)
            receipt_committed = True
            return self.ledger.public(self.ledger.request(rid))
        except BaseException as error:
            original_error = error
            # Expired owner authority cannot be revived merely to save a report.
            # Earlier durable phase/reservation remains a valid uncertain state.
            try:
                self.ledger.phase(rid,"RECOVERY_INCOMPLETE" if recovery else "INCOMPLETE",self._active,
                    {"status":"INCOMPLETE","error_type":type(error).__name__,
                     "reason":str(error)[:1000],"recovery":recovery,**P.FLAGS})
            except BaseException: pass
            raise
        finally:
            cleanup_error = None
            if acquisition is not None:
                try: acquisition.close()
                except BaseException as error:
                    service.closed = True; cleanup_error = error
            self._current = None; self._busy = False
            if cleanup_error is not None:
                # Never let a pending return imply clean completion. The exact
                # saved receipt/custody survives; callers may inspect historical
                # status through a later explicit owner, not this closed grant.
                # Keep both failure contexts, including a preceding body error.
                raise PlacementCleanupError(rid,receipt_committed,original_error) from cleanup_error

    def seal(self,service):
        self._call(service); self.ledger.seal(lambda:self._active(service))

    def close(self):
        F.need(not self._busy,"PLACEMENT_BUSY")
        if self._service is not None: self._service.closed = True
        self.closed = True; self.ledger.close()
