"""Finite owner-local route observations, separate from immutable placement receipts."""
import asyncio
from copy import deepcopy
import sqlite3
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.transport import CompositeProvider
from location.controller_services import ServiceLocationProcess
from . import codec as P
from .controller import PlacementController

ROUTE_BYTES = 16384


def _now_ms(): return int(time.time()*1000)


class PlacementAdvertisement:
    """One exact controller/read provider/locator and bounded durable dispatches."""
    @classmethod
    def open(cls, controller, service, location, provider, endpoint, *,
             health_cap, journal_pages=256, create=False):
        F.need(type(controller) is PlacementController, "PLACEMENT_ROUTE_CONTROLLER")
        controller._active(service)
        F.need(type(location) is ServiceLocationProcess and type(provider) is CompositeProvider,
               "PLACEMENT_ROUTE_ACTUAL_ROLES")
        cfg = controller.ledger.config
        F.uint(health_cap, 2, 58); F.uint(journal_pages, 256, 65536)
        F.need(type(create) is bool, "PLACEMENT_ROUTE_CREATE")
        F.need(location.config["schema"] == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1"
               and location.config["role"] == "index-provider"
               and location.config["namespace"] == cfg["namespace"]
               and location.config["endpoints"] == [endpoint]
               and location.sequence == 0 and location.process is None,
               "PLACEMENT_ROUTE_FRESH_V1_PROVIDER")
        commands = health_cap+2*cfg["max_cells"]+1
        F.need(commands <= min(location.config["limits"]["commands"], 60)
               and cfg["max_cells"] <= location.config["limits"]["advertised_keys"],
               "PLACEMENT_ROUTE_ORIGINAL_COMMAND_RESERVATION")
        w = controller.workspace
        previous = getattr(w, "_placement_advertisement", None)
        F.need(previous is None or previous.closed, "PLACEMENT_ROUTE_ALREADY_OPEN")
        self = cls.__new__(cls)
        self.controller, self.service, self.location, self.provider = controller, service, location, provider
        self._origin = controller, service, location, provider, w
        self.endpoint = deepcopy(endpoint); self._endpoint_raw = F.compact(endpoint)
        self._location_raw = F.compact(location.config)
        self._runtime, self._deadline = service.run_id, service.deadline
        self.health_cap, self.health_checks = health_cap, 0
        self._health_cap, self._busy, self.closed = health_cap, False, False
        self.db = None; self.run = None
        self._config = {"schema":"DMKN_V5_PLACEMENT_ROUTE_JOURNAL_V1",
            **{name:cfg[name] for name in ("service_epoch","generation","namespace","wire_profile_id",
                                          "max_cells","max_runs")},
            "read_endpoint":deepcopy(endpoint), "journal_pages":journal_pages}
        self._config_raw = F.compact(self._config)
        self._path = ordinary(w.root/"placement-routes.sqlite", fresh=create, directory=False)
        w._placement_advertisement = self
        try:
            self.db = sqlite3.connect(self._path, timeout=1, isolation_level=None)
            for pragma in ("journal_mode=DELETE", "synchronous=FULL", "foreign_keys=ON",
                           "temp_store=MEMORY", "mmap_size=0", "cache_size=-1024"):
                self.db.execute("PRAGMA "+pragma)
            F.need(self.db.execute("PRAGMA max_page_count="+str(journal_pages)).fetchone()[0]
                   == journal_pages, "PLACEMENT_ROUTE_PAGE_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1),config BLOB NOT NULL);
                    CREATE TABLE runs(n INTEGER PRIMARY KEY,runtime TEXT UNIQUE NOT NULL,
                        allocation BLOB NOT NULL);
                    CREATE TABLE routes(cell TEXT NOT NULL,run INTEGER NOT NULL,
                        request_id TEXT NOT NULL,feature TEXT NOT NULL,phase TEXT NOT NULL,
                        observed_ms INTEGER NOT NULL,observation BLOB,
                        PRIMARY KEY(cell,run),FOREIGN KEY(run) REFERENCES runs(n)) WITHOUT ROWID;
                    COMMIT;
                """)
                self._transaction(lambda:self.db.execute("INSERT INTO meta VALUES(1,?)",
                                  (self._config_raw,)), check_meta=False)
            self._active()
            def reserve():
                number = self.db.execute("SELECT COALESCE(MAX(n),0)+1 FROM runs").fetchone()[0]
                F.need(number <= cfg["max_runs"], "PLACEMENT_ROUTE_RUN_CAP")
                allocation = {"cells":cfg["max_cells"],"health":health_cap,
                    "publish":cfg["max_cells"],"withdraw":cfg["max_cells"],"stop":1,
                    "commands":commands,"funding":"NONREFUNDABLE_ORIGINAL_RUN_AUTHORIZATION"}
                self.db.execute("INSERT INTO runs VALUES(?,?,?)",
                                (number,service.run_id,F.compact(allocation)))
                return number
            self.run = self._transaction(reserve)
            return self
        except BaseException:
            self.close(); raise

    def _active(self, until=None, *, network=False, check_meta=True):
        c,s,n,p,w = self._origin
        F.need(not self.closed and self.db is not None and self.controller is c
               and self.service is s and self.location is n and self.provider is p
               and c.workspace is w and getattr(w,"_placement_advertisement",None) is self,
               "PLACEMENT_ROUTE_ORIGIN")
        c._active(s)
        F.need((s.run_id,s.deadline) == (self._runtime,self._deadline)
               and F.compact(n.config) == self._location_raw
               and F.compact(self.endpoint) == self._endpoint_raw
               and self.health_cap == self._health_cap
               and p.index is w.index and p.custody is w.modules and p.packets is w.packets,
               "PLACEMENT_ROUTE_ROLE_BINDING")
        F.need(until is None or time.monotonic() < min(until,self._deadline),
               "PLACEMENT_ROUTE_OPERATION_EXPIRED")
        if check_meta:
            row = self.db.execute("SELECT config FROM meta WHERE id=1").fetchone()
            F.need(row is not None and bytes(row[0]) == self._config_raw,
                   "PLACEMENT_ROUTE_CONFIG_CHANGED")
        if network:
            F.need(p.server is not None and p.server.is_serving()
                   and not n.closed and not n.channel_failed and n.process is not None
                   and n.process.returncode is None, "PLACEMENT_ROUTE_SERVICE_NOT_LIVE")

    def _transaction(self, function, until=None, *, check_meta=True, extra_guard=None):
        def guard():
            self._active(until, check_meta=check_meta)
            if extra_guard is not None: extra_guard()
        guard(); self.db.execute("BEGIN IMMEDIATE")
        try:
            value = function(); guard(); self.db.execute("COMMIT"); return value
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def _facet(self, value):
        cell,feature = P.cell(self.controller.workspace.adapter,value["fingerprint"])
        F.need(cell == value["cell"], "PLACEMENT_ROUTE_CELL_BINDING")
        row = self.db.execute("SELECT r.run,r.request_id,r.feature,r.phase,r.observed_ms,r.observation,u.runtime "
            "FROM routes r JOIN runs u ON u.n=r.run WHERE r.cell=? ORDER BY r.run DESC LIMIT 1",(cell,)).fetchone()
        result = {"status":"NOT_ATTEMPTED","cell":cell,"features":[feature],"stripe":0,
            "run_id":None,"request_id":None,"observed_at_ms":None,
            "add_provider_write":0,"error_code":None}
        if row is None: return result
        F.need(row[2] == feature, "PLACEMENT_ROUTE_JOURNAL_FEATURE")
        phase = row[3]
        F.need(phase in ("DISPATCH_ATTEMPTED","INCOMPLETE","HINT_DISPATCHED_UNACKNOWLEDGED"),
               "PLACEMENT_ROUTE_JOURNAL_PHASE")
        observed = None if row[5] is None else F.strict(bytes(row[5]),ROUTE_BYTES)
        writes = 0 if observed is None else observed["census"]["add_provider_write"]
        F.uint(writes,0,2**53-1,"PLACEMENT_ROUTE_WRITE_COUNT")
        # Attempt persisted before the call; a missing returned observation
        # cannot distinguish not-yet-sent from sent-but-unrecorded.
        status = "DISPATCH_UNCERTAIN" if phase == "DISPATCH_ATTEMPTED" else phase
        result.update(status=status,run_id=F.hexid(row[6]),request_id=F.hexid(row[1]),
            observed_at_ms=F.uint(row[4],1,2**53-1),add_provider_write=writes,
            error_code=None if phase == "HINT_DISPATCHED_UNACKNOWLEDGED" else
                ("ROUTE_UNCERTAIN" if phase == "DISPATCH_ATTEMPTED" else "ROUTE_INCOMPLETE"))
        return result

    def _joined(self, placement, value):
        public = deepcopy(placement)
        if public["phase"] != "RECEIPT_COMMITTED" and public["outcome"] is not None:
            public["outcome"] = {"status":"INCOMPLETE","code":"PLACEMENT_INCOMPLETE"}
        return {"placement":public,"route":self._facet(value)}

    async def submit(self, token, raw, *, until):
        self._active(until)
        F.need(not self._busy, "PLACEMENT_NETWORK_BUSY")
        self._busy = True
        try:
            c = self.controller; cfg = c.ledger.config
            value = P.manifest(raw,cfg)
            auth = c.ledger.authenticate(token)
            rid = P.request_id(raw,auth[0],cfg["generation"])
            old = c.ledger.db.execute("SELECT manifest FROM requests WHERE id=?",(rid,)).fetchone()
            if old is not None:
                F.need(bytes(old[0]) == raw, "PLACEMENT_REQUEST_ID_CONFLICT")
            else:
                self._active(until,network=True)
            async with asyncio.timeout_at(min(until,self._deadline)):
                placement = await c.submit(self.service,token,raw)
                self._active(until)
                if old is None:
                    F.need(placement["phase"] == "RECEIPT_COMMITTED"
                           and placement["request_id"] == rid, "PLACEMENT_ROUTE_COMMITTED_RECEIPT")
                    await self._publish(value,auth[2],rid,placement["outcome"],until)
                return self._joined(placement,value)
        finally:
            self._busy = False

    def status(self, token, request_id, *, until):
        self._active(until)
        F.need(not self._busy, "PLACEMENT_NETWORK_BUSY")
        placement = self.controller.status(self.service,token,request_id)
        row = self.controller.ledger.request(request_id)
        value = P.manifest(row["manifest"],self.controller.ledger.config)
        self._active(until)
        return self._joined(placement,value)

    async def _publish(self, value, policy, rid, outcome, until):
        c = self.controller
        cell,feature = P.cell(c.workspace.adapter,value["fingerprint"])
        F.need(outcome["route"] == {"status":"INTENT_ONLY","cell":cell,"features":[feature],"stripe":0},
               "PLACEMENT_ROUTE_RECEIPT_BINDING")
        def guard():
            self._active(until,network=True)
            c._window(value,policy,False)
        guard()
        old = self.db.execute("SELECT 1 FROM routes WHERE cell=? AND run=?",(cell,self.run)).fetchone()
        if old is not None: return  # One opportunity per cell/run, even after uncertainty.
        def attempt():
            F.need(self.db.execute("SELECT count(*) FROM routes WHERE run=?",(self.run,)).fetchone()[0]
                   < self._config["max_cells"], "PLACEMENT_ROUTE_CELL_CAP")
            self.db.execute("INSERT INTO routes VALUES(?,?,?,?,'DISPATCH_ATTEMPTED',?,NULL)",
                            (cell,self.run,rid,feature,_now_ms()))
        self._transaction(attempt,until,extra_guard=guard)
        response = await self.location.command("publish",{"features":[feature],"stripe":0},until=until)
        guard()
        encoded = F.compact(response)
        F.need(len(encoded) <= ROUTE_BYTES and type(response) is dict
               and response.get("route_key") == cell
               and response.get("remote_placement_confirmed") is False
               and response.get("global_complete") is False
               and response.get("mathematical_acceptance") is False,
               "PLACEMENT_ROUTE_RESPONSE_BINDING")
        census = response.get("census")
        F.need(type(census) is dict, "PLACEMENT_ROUTE_RESPONSE_CENSUS")
        writes = F.uint(census.get("add_provider_write"),0,2**53-1,"PLACEMENT_ROUTE_WRITE_COUNT")
        phase = response.get("status")
        F.need(phase in ("INCOMPLETE","HINT_DISPATCHED_UNACKNOWLEDGED")
               and (phase != "HINT_DISPATCHED_UNACKNOWLEDGED" or
                    (response.get("error") is None and writes > 0)), "PLACEMENT_ROUTE_RESPONSE_STATUS")
        self._transaction(lambda:self.db.execute("UPDATE routes SET phase=?,observed_ms=?,observation=? "
            "WHERE cell=? AND run=?",(phase,_now_ms(),encoded,cell,self.run)),until,extra_guard=guard)

    async def health(self, *, until):
        self._active(until,network=True)
        F.need(self.health_checks < self.health_cap, "PLACEMENT_ROUTE_HEALTH_CAP")
        self.health_checks += 1
        value = await self.location.command("status",{},until=until)
        self._active(until,network=True)
        F.need(type(value) is dict and value.get("status") == "RUNNING"
               and value.get("namespace") == self._config["namespace"]
               and value.get("role") == "index-provider"
               and value.get("global_complete") is False
               and value.get("mathematical_acceptance") is False, "PLACEMENT_ROUTE_HEALTH_FAILED")
        return {"status":"RUNNING","health_checks":self.health_checks,
                "scope":"BOUNDED_OBSERVATION_NOT_CONTINUOUS_READINESS"}

    def report(self):
        return {"runtime":self._runtime,"run":self.run,"health_checks":self.health_checks,
            "health_cap":self.health_cap,"max_cells":self._config["max_cells"],
            "closed":self.closed,"mathematical_acceptance":False}

    def close(self):
        self.closed = True
        try:
            if self.db is not None: self.db.close(); self.db = None
        finally:
            w = self._origin[4]
            if getattr(w,"_placement_advertisement",None) is self:
                w._placement_advertisement = None
