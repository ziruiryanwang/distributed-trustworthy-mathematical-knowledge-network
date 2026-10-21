"""Two charged owner-local generation slots; no deletion or remote authority.

Trusted-owner Windows composition. Logical census bounds are enforced; the
supported SQLite/VFS physical envelope remains a separate adoption obligation.
Unknown crashed actors remain held: neither a lock nor saved JSON proves close.
"""
from copy import deepcopy
import ipaddress
import math
import os
from pathlib import Path
import sqlite3
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from . import codec as P

SCHEMA = "DMKN_V5_TWO_GENERATION_MANAGER_V1"
MAX_SEQUENCE = 2**63-1
MAX_RECORD = 131072
_ISSUE = object()
_CLEANUP = ("intake_closed", "retained_closed", "location_closed", "read_closed",
            "journal_closed", "controller_closed", "workspace_closed")


def _disjoint(a, b):
    return not a.is_relative_to(b) and not b.is_relative_to(a)


def _deadline(value, maximum):
    F.need(type(value) in (int, float) and math.isfinite(value)
           and time.monotonic() < value <= maximum, "GENERATIONS_DEADLINE")
    return value


def _read(path, maximum=MAX_RECORD):
    path = ordinary(path, directory=False)
    F.need(path.stat().st_size <= maximum, "GENERATIONS_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    F.need(len(raw) <= maximum, "GENERATIONS_FILE_BOUND")
    return raw


def _write_new(path, raw):
    ordinary(path, fresh=True, directory=False)
    F.need(len(raw) <= MAX_RECORD, "GENERATIONS_RECORD_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def _endpoint(value):
    F.fields(value, ("host", "port", "tls", "server_name"))
    F.need(type(value["host"]) is str and 0 < len(value["host"]) <= 253
           and type(value["tls"]) is bool
           and (value["server_name"] is None or
                type(value["server_name"]) is str and len(value["server_name"]) <= 253),
           "GENERATIONS_ENDPOINT")
    return F.uint(value["port"], 1, 65535, "GENERATIONS_ENDPOINT_PORT")


def _config(value):
    F.fields(value, ("schema", "epoch", "clock_model_id", "registry_pages",
        "owner_reserved_bytes", "registry_reserved_bytes", "cleanup_reserved_bytes",
        "protected_roots", "slots"))
    F.need(value["schema"] == SCHEMA, "GENERATIONS_SCHEMA")
    F.hexid(value["epoch"]); F.hexid(value["clock_model_id"])
    F.uint(value["registry_pages"], 64, 4096)
    for key in ("owner_reserved_bytes", "registry_reserved_bytes", "cleanup_reserved_bytes"):
        F.uint(value[key], 1, 2**50)
    F.need(type(value["protected_roots"]) is list
           and 1 <= len(value["protected_roots"]) <= 64, "GENERATIONS_PROTECTED_ROOTS")
    for root in value["protected_roots"]: ordinary(root)
    F.need(type(value["slots"]) is list and len(value["slots"]) == 2,
           "GENERATIONS_EXACTLY_TWO_SLOTS")
    ports = []
    for slot in value["slots"]:
        F.fields(slot, ("reserved_bytes", "max_cells", "max_runs", "read_endpoint",
                        "intake_endpoint", "listen"))
        F.uint(slot["reserved_bytes"], 1, 2**50)
        F.uint(slot["max_cells"], 1, 4096); F.uint(slot["max_runs"], 1, 4096)
        ports.extend((_endpoint(slot["read_endpoint"]), _endpoint(slot["intake_endpoint"])))
        F.need(type(slot["listen"]) is list and len(slot["listen"]) == 1
               and type(slot["listen"][0]) is str, "GENERATIONS_ONE_LISTEN_ADDRESS")
        parts = slot["listen"][0].split("/")
        F.need(len(parts) == 5 and parts[0] == "" and parts[1] in ("ip4", "ip6")
               and parts[3] == "tcp" and parts[4].isdigit(), "GENERATIONS_LISTEN_SHAPE")
        address = ipaddress.ip_address(parts[2])
        F.need(address.version == (4 if parts[1] == "ip4" else 6), "GENERATIONS_LISTEN_FAMILY")
        ports.append(F.uint(int(parts[4]), 1, 65535))
    # Conservative separation also avoids hostname/wildcard aliases between roles.
    F.need(len(set(ports)) == 6, "GENERATIONS_DISTINCT_ROLE_PORTS")
    total = (sum(slot["reserved_bytes"] for slot in value["slots"])
             + value["registry_reserved_bytes"] + value["cleanup_reserved_bytes"])
    F.need(total <= value["owner_reserved_bytes"], "GENERATIONS_OWNER_ALLOCATION")
    raw = F.compact(value); F.need(len(raw) <= MAX_RECORD, "GENERATIONS_CONFIG_BOUND")
    return deepcopy(value)


class ConservativeClock:
    """Fresh local adoption of a UTC lower-bound model, never a network oracle.

    The owner asserts L <= actual UTC at this call and a monotonic-clock rate
    error <= rho until expiry. Correctness is conditional on that assertion.
    No persisted observation, system wall clock or prior-session token is used.
    """
    def __init__(self, key, manager, lower_utc_ms, valid_for_ms, rate_error_ppm, model_id):
        F.need(key is _ISSUE, "GENERATIONS_CLOCK_ISSUER")
        F.uint(lower_utc_ms, 1, 2**53-1); F.uint(valid_for_ms, 1, 3600000)
        F.uint(rate_error_ppm, 0, 999999); F.hexid(model_id)
        F.need(model_id == manager.config["clock_model_id"], "GENERATIONS_CLOCK_MODEL")
        self._manager = manager
        self._anchor = time.monotonic_ns()
        self._binding = (lower_utc_ms, valid_for_ms, rate_error_ppm, model_id)

    def lower_bound_ms(self):
        self._manager._active()
        elapsed = time.monotonic_ns()-self._anchor
        lower, validity, ppm, unused = self._binding
        F.need(0 <= elapsed <= validity*1000000, "GENERATIONS_CLOCK_EXPIRED_OR_BACKWARDS")
        result = lower+(elapsed*(1000000-ppm))//1000000000000
        F.need(result <= 2**53-1, "GENERATIONS_CLOCK_RANGE")
        return result


class ManagedRun:
    """Current process's exact owned actor handle, not a serializable warrant."""
    def __init__(self, key, manager, record, outer_deadline):
        F.need(key is _ISSUE, "GENERATIONS_RUN_ISSUER")
        self._manager = manager
        self._binding = (record["slot"], record["generation"], record["runs"])
        self.outer_deadline = outer_deadline
        self.path = manager.generation_path(record)/("run-%04d" % record["runs"])
        self._outer, self._path = outer_deadline, self.path
        self.service = self.location = None
        self._roles = None
        self.closed = False


class ManagedGenerations:
    @classmethod
    def open(cls, root, config, *, create=False, deadline, calls=128, cpu_seconds=30):
        F.need(os.name == "nt", "GENERATIONS_WINDOWS_OWNER_REQUIRED")
        F.need(type(create) is bool, "GENERATIONS_CREATE_FLAG")
        cfg = _config(config)
        _deadline(deadline, time.monotonic()+3600)
        F.uint(calls, 1, 8192); F.uint(cpu_seconds, 1, 3600)
        path = ordinary(root, fresh=create)
        F.need(all(_disjoint(path, Path(p)) for p in cfg["protected_roots"]),
               "GENERATIONS_PROTECTED_PATH_OVERLAP")
        self = cls.__new__(cls)
        self.root, self._root, self.config = path, path, cfg
        self._raw = F.compact(cfg)
        self._marker = F.compact({"schema": SCHEMA, "root": str(path),
                                 "config_sha256": P.digest(self._raw)})
        self.deadline = deadline
        self._deadline, self._cpu_start, self._cpu_cap = deadline, time.process_time(), cpu_seconds
        self._calls, self._call_cap = 0, calls
        self._lock = self.db = None
        self._closed, self._poisoned = False, False
        self._handles = {}
        if create: path.mkdir()
        try:
            import msvcrt
            lock = path/"owner.lock"
            if lock.exists(): ordinary(lock, directory=False)
            self._lock = lock.open("a+b")
            if lock.stat().st_size == 0:
                self._lock.write(b"\0"); self._lock.flush(); os.fsync(self._lock.fileno())
            self._lock.seek(0); msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            dbpath = ordinary(path/"generations.sqlite", fresh=create, directory=False)
            self.db = sqlite3.connect(dbpath, timeout=1, isolation_level=None)
            if create: self.db.execute("PRAGMA page_size=4096")
            F.need(self.db.execute("PRAGMA page_size").fetchone()[0] == 4096,
                   "GENERATIONS_REGISTRY_PAGE_SIZE")
            F.need(self.db.execute("PRAGMA journal_mode=DELETE").fetchone()[0] == "delete",
                   "GENERATIONS_REGISTRY_JOURNAL")
            self.db.execute("PRAGMA synchronous=FULL"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-256")
            F.need(self.db.execute("PRAGMA synchronous").fetchone()[0] == 2
                   and self.db.execute("PRAGMA temp_store").fetchone()[0] == 2
                   and self.db.execute("PRAGMA auto_vacuum").fetchone()[0] == 0,
                   "GENERATIONS_REGISTRY_PROFILE")
            F.need(self.db.execute("PRAGMA max_page_count="+str(cfg["registry_pages"])).fetchone()[0]
                   == cfg["registry_pages"], "GENERATIONS_REGISTRY_PAGE_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), config BLOB NOT NULL,
                        sequence INTEGER NOT NULL, retired_floor INTEGER NOT NULL,
                        last_horizon INTEGER NOT NULL);
                    CREATE TABLE slots(id INTEGER PRIMARY KEY CHECK(id IN (0,1)), record BLOB);
                    INSERT INTO slots VALUES(0,NULL); INSERT INTO slots VALUES(1,NULL);
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,0,0,0)", (self._raw,))
                _write_new(path/"manager.json", self._marker)
                for index in range(2): (path/("slot-%d" % index)).mkdir()
            F.need(_read(path/"manager.json") == self._marker, "GENERATIONS_MANAGER_MARKER")
            for index in range(2): ordinary(path/("slot-%d" % index))
            self._active()
            F.need(self.db.execute("SELECT count(*) FROM meta").fetchone()[0] == 1
                   and self.db.execute("SELECT id FROM slots ORDER BY id").fetchall() == [(0,), (1,)],
                   "GENERATIONS_REGISTRY_CENSUS")
            # Saved LIVE/RESERVED/CLOSING is not a surviving current authority.
            def recover():
                for record in self._records():
                    if record is not None and record["run_state"] in ("RESERVED", "LIVE", "CLOSING"):
                        record["run_state"] = "UNKNOWN"
                        record["failure"] = "PRIOR_SESSION_CLOSURE_UNPROVEN"
                        self._save(record)
            self._transaction(recover)
            return self
        except BaseException as primary:
            try: self._release()
            except BaseException:
                primary.add_note("GENERATIONS_PARTIAL_OPEN_CLEANUP_UNCERTAIN")
            raise

    def _active(self):
        F.need(not self._closed and not self._poisoned and self.db is not None
               and self._lock is not None and not self._lock.closed,
               "GENERATIONS_CLOSED_OR_UNCERTAIN")
        F.need(self.root == self._root and self.deadline == self._deadline and time.monotonic() < self._deadline
               and time.process_time()-self._cpu_start <= self._cpu_cap,
               "GENERATIONS_OWNER_AUTHORITY_EXPIRED")
        F.need(F.compact(self.config) == self._raw, "GENERATIONS_CONFIG_CHANGED")
        row = self.db.execute("SELECT config FROM meta WHERE id=1").fetchone()
        F.need(row is not None and bytes(row[0]) == self._raw, "GENERATIONS_DURABLE_CONFIG_CHANGED")

    def _call(self):
        self._active(); F.need(self._calls < self._call_cap, "GENERATIONS_OWNER_CALL_CAP")
        self._calls += 1

    def _transaction(self, operation):
        self._active(); self.db.execute("BEGIN IMMEDIATE")
        try:
            result = operation(); self._active()
            try: self.db.execute("COMMIT")
            except BaseException:
                self._poisoned = True; raise
            return result
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def _records(self):
        sequence, floor, horizon = self.db.execute(
            "SELECT sequence,retired_floor,last_horizon FROM meta WHERE id=1").fetchone()
        F.uint(sequence, 0, MAX_SEQUENCE); F.uint(floor, 0, sequence); F.uint(horizon, 0, 2**53-1)
        records, seen = [], set()
        for slot, raw in self.db.execute("SELECT id,record FROM slots ORDER BY id"):
            if raw is None:
                records.append(None); continue
            record = F.strict(bytes(raw), MAX_RECORD)
            required = {"slot", "sequence", "generation", "phase", "runs", "run_state",
                        "failure", "retirement_lower_ms", "config"}
            F.need(type(record) is dict and required <= set(record)
                   and set(record) <= required | {"closure_sha256"}, "GENERATIONS_STORED_RECORD_FIELDS")
            F.need(record["slot"] == slot and record["sequence"] not in seen,
                   "GENERATIONS_STORED_SLOT_SEQUENCE")
            F.uint(record["sequence"], 1, sequence); seen.add(record["sequence"])
            F.need(record["phase"] in ("PROVISIONING", "OPEN", "SEALING", "SEALED_SERVING",
                                       "INCOMPLETE", "RETIRING", "RETIRED")
                   and record["run_state"] in ("NONE", "RESERVED", "LIVE", "CLOSING", "CLOSED", "UNKNOWN"),
                   "GENERATIONS_STORED_PHASE")
            cfg = record["config"]; selected = P.config(cfg["placement"])
            spec = self.config["slots"][slot]
            F.need(selected["service_epoch"] == self.config["epoch"]
                   and selected["max_runs"] <= spec["max_runs"]
                   and selected["max_cells"] <= spec["max_cells"]
                   and selected["retention_not_after_ms"] <= horizon,
                   "GENERATIONS_STORED_ALLOCATION")
            F.uint(record["runs"], 0, selected["max_runs"])
            F.need((record["run_state"] == "NONE") == (record["runs"] == 0),
                   "GENERATIONS_STORED_RUN_CENSUS")
            if record["run_state"] == "CLOSED": F.hexid(record.get("closure_sha256"))
            if record["phase"] != "RETIRED":
                F.need(record["sequence"] > floor, "GENERATIONS_STORED_RETIRED_FLOOR")
            seed = deepcopy(cfg); del seed["placement"]["generation"]
            expected = F.digest("DMKN-V5-TWO-SLOT-GENERATION-V1", {
                "manager": P.digest(self._marker), "sequence": record["sequence"], "slot": slot, "config": seed})
            F.need(record["generation"] == selected["generation"] == expected,
                   "GENERATIONS_STORED_IDENTITY")
            records.append(record)
        F.need(len(records) == 2, "GENERATIONS_STORED_SLOT_CENSUS")
        return records

    def _save(self, record):
        raw = F.compact(record); F.need(len(raw) <= MAX_RECORD, "GENERATIONS_RECORD_BOUND")
        self.db.execute("UPDATE slots SET record=? WHERE id=?", (raw, record["slot"]))

    def _find(self, generation, *, retired=False):
        self._active(); F.hexid(generation)
        for record in self._records():
            if record is not None and record["generation"] == generation:
                floor = self.db.execute("SELECT retired_floor FROM meta WHERE id=1").fetchone()[0]
                F.need(retired or record["phase"] != "RETIRED" and record["sequence"] > floor,
                       "GENERATIONS_RETIRED_IDENTITY")
                return record
        raise ValueError("GENERATIONS_NOT_CURRENTLY_REGISTERED")

    def generation_path(self, record):
        return self.root/("slot-%d" % record["slot"])/("g%020d" % record["sequence"])

    def _generation_marker(self, record):
        return F.compact({"schema": "DMKN_V5_MANAGED_GENERATION_V1", "epoch": self.config["epoch"],
            "slot": record["slot"], "sequence": record["sequence"], "generation": record["generation"],
            "config_sha256": P.digest(F.compact(record["config"]))})

    def _check_marker(self, record):
        root = ordinary(self.generation_path(record))
        F.need(_read(root/"generation.json") == self._generation_marker(record),
               "GENERATIONS_GENERATION_MARKER")
        return root

    def allocate(self, slot, generation_config):
        self._call(); F.uint(slot, 0, 1)
        F.fields(generation_config, ("workspace", "placement", "service_limits", "egress", "location"))
        cfg = deepcopy(generation_config); spec = self.config["slots"][slot]
        F.need(type(cfg["placement"]) is dict and "generation" not in cfg["placement"],
               "GENERATIONS_DERIVED_ID_REQUIRED")
        selected = P.config({**cfg["placement"], "generation": "00"*32})
        F.need(selected["service_epoch"] == self.config["epoch"]
               and selected["max_cells"] <= spec["max_cells"]
               and selected["max_runs"] <= spec["max_runs"], "GENERATIONS_SLOT_ALLOCATION")
        F.fields(cfg["location"], ("schema", "role", "namespace", "egress", "listen", "announce",
                                  "bootstrap", "endpoints", "limits"))
        location = cfg["location"]
        F.need(location["schema"] == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1"
               and location["role"] == "index-provider"
               and location["namespace"] == selected["namespace"]
               and location["listen"] == spec["listen"]
               and location["endpoints"] == [spec["read_endpoint"]]
               and location["egress"] == cfg["egress"], "GENERATIONS_LOCATION_BINDING")
        F.need(len(F.compact(cfg)) <= MAX_RECORD//2, "GENERATIONS_GENERATION_CONFIG_BOUND")
        def reserve():
            F.need(self._records()[slot] is None, "GENERATIONS_SLOT_OCCUPIED")
            sequence, unused, horizon = self.db.execute(
                "SELECT sequence,retired_floor,last_horizon FROM meta WHERE id=1").fetchone()
            F.need(sequence < MAX_SEQUENCE, "GENERATIONS_SEQUENCE_EXHAUSTED")
            F.need(selected["retention_not_after_ms"] >= horizon, "GENERATIONS_HORIZON_REGRESSION")
            sequence += 1
            generation = F.digest("DMKN-V5-TWO-SLOT-GENERATION-V1", {
                "manager": P.digest(self._marker), "sequence": sequence, "slot": slot, "config": cfg})
            bound = deepcopy(cfg); bound["placement"]["generation"] = generation
            record = {"slot": slot, "sequence": sequence, "generation": generation,
                "phase": "PROVISIONING", "runs": 0, "run_state": "NONE", "failure": None,
                "retirement_lower_ms": None, "config": bound}
            self._save(record)
            self.db.execute("UPDATE meta SET sequence=?,last_horizon=? WHERE id=1",
                            (sequence, selected["retention_not_after_ms"]))
            return record
        record = self._transaction(reserve)
        # All failures below leave the committed slot/sequence and budget charged.
        path = ordinary(self.generation_path(record), fresh=True)
        path.mkdir(); _write_new(path/"generation.json", self._generation_marker(record))
        return deepcopy(record)

    def reserve_run(self, generation, *, outer_deadline):
        self._call(); _deadline(outer_deadline, self._deadline)
        record = self._find(generation)
        F.need(record["phase"] in ("PROVISIONING", "OPEN", "SEALING", "SEALED_SERVING")
               and record["run_state"] in ("NONE", "CLOSED"), "GENERATIONS_RUN_PHASE_OR_UNKNOWN")
        F.need(record["slot"] not in self._handles, "GENERATIONS_CURRENT_ACTOR")
        root = self._check_marker(record)
        if record["phase"] == "PROVISIONING":
            F.need(record["runs"] == 0 and not os.path.lexists(root/"workspace"),
                   "GENERATIONS_NO_PROVISIONING_RECREATE")
        else: ordinary(root/"workspace")
        F.need(record["runs"] < record["config"]["placement"]["max_runs"], "GENERATIONS_RUN_CAP")
        record["runs"] += 1; record["run_state"] = "RESERVED"
        record.pop("closure_sha256", None)
        self._transaction(lambda: self._save(record))
        handle = ManagedRun(_ISSUE, self, record, outer_deadline)
        self._handles[record["slot"]] = handle
        return handle

    def _owned(self, handle):
        F.need(type(handle) is ManagedRun and handle._manager is self
               and self._handles.get(handle._binding[0]) is handle, "GENERATIONS_EXACT_RUN_OWNER")
        record = self._find(handle._binding[1], retired=True)
        F.need((record["slot"], record["generation"], record["runs"]) == handle._binding,
               "GENERATIONS_CURRENT_RUN_BINDING")
        F.need(handle.path == handle._path == self.generation_path(record)/("run-%04d" % record["runs"])
               and handle.outer_deadline == handle._outer <= self._deadline,
               "GENERATIONS_RUN_PATH_OR_AUTHORITY_CHANGED")
        if handle._roles is not None:
            F.need(handle.service is handle._roles[0] and handle.location is handle._roles[1],
                   "GENERATIONS_RUN_ROLES_CHANGED")
        return record

    def _attach(self, handle, service):
        from client.serve_placement import PlacementService
        from location.controller_services import ServiceLocationProcess
        record = self._owned(handle)
        F.need(handle._roles is None and handle.service is None
               and type(service) is PlacementService and type(handle.location) is ServiceLocationProcess
               and service.location is handle.location
               and not service._started and not service.closed and not service._closing
               and handle.location.process is None and handle.location._start_task is None
               and service.workspace.root == self.generation_path(record)/"workspace"
               and F.compact(service.ledger.config) == F.compact(record["config"]["placement"]),
               "GENERATIONS_EXACT_SERVICE_ATTACHMENT")
        service._active()
        F.need(service.ledger.db.execute("SELECT runs FROM meta WHERE id=1").fetchone()[0]
               == record["runs"], "GENERATIONS_ATTACHED_RUN_CENSUS")
        handle.service = service; handle._roles = service, handle.location

    def _started(self, handle):
        record = self._owned(handle)
        F.need(record["run_state"] == "RESERVED" and record["phase"] in
               ("PROVISIONING", "OPEN", "SEALING", "SEALED_SERVING"),
               "GENERATIONS_START_PHASE")
        service = handle.service
        F.need(service is not None and service._started and not service.closed,
               "GENERATIONS_SERVICE_NOT_STARTED")
        service._active()
        state, runs = service.ledger.db.execute("SELECT state,runs FROM meta WHERE id=1").fetchone()
        F.need(runs == record["runs"] and state in ("OPEN", "SEALED_SERVING"),
               "GENERATIONS_SERVICE_CENSUS")
        F.need(record["phase"] not in ("SEALING", "SEALED_SERVING") or state == "SEALED_SERVING",
               "GENERATIONS_SEAL_INTENT_MUST_COMPLETE")
        record["phase"] = state; record["run_state"] = "LIVE"
        self._transaction(lambda: self._save(record))

    def _live(self, generation):
        record = self._find(generation)
        handle = self._handles.get(record["slot"])
        F.need(handle is not None and handle.service is not None, "GENERATIONS_NO_CURRENT_SERVICE")
        self._owned(handle)
        F.need(record["run_state"] == "LIVE" and not handle.closed, "GENERATIONS_SERVICE_NOT_LIVE")
        return record, handle

    def seal(self, generation):
        self._call(); record, handle = self._live(generation); service = handle.service
        F.need(record["phase"] in ("OPEN", "SEALING", "SEALED_SERVING"), "GENERATIONS_SEAL_PHASE")
        service._active()
        F.need(not service.controller._busy and not service.advertisement._busy
               and (service._retained_task is None or service._retained_task.done())
               and (service.intake_provider is None or not service.intake_provider.tasks),
               "GENERATIONS_SEAL_BUSY")
        # Synchronous same-event-loop intent/seal/commit, with no intervening await.
        record["phase"] = "SEALING"; self._transaction(lambda: self._save(record))
        service.controller.seal(service.grant)
        record["phase"] = "SEALED_SERVING"; self._transaction(lambda: self._save(record))
        return deepcopy(record)

    def _closing(self, handle):
        record = self._owned(handle)
        F.need(record["run_state"] in ("LIVE", "RESERVED", "CLOSING"), "GENERATIONS_CLOSE_PHASE")
        record["run_state"] = "CLOSING"; self._transaction(lambda: self._save(record))

    def _closed_run(self, handle):
        """Accept actual same-owner closed roles only; no caller closure boolean."""
        record = self._owned(handle); service = handle.service
        F.need(service is not None and service.location is handle.location, "GENERATIONS_CLOSE_ROLES")
        result = service.report()
        F.need(all(actual is original for actual, original in zip(
            (service.workspace, service.ledger, service.controller, service.grant,
             service.advertisement, service.location, service.read_provider), service._roles)),
            "GENERATIONS_CLOSED_ROLE_IDENTITY_CHANGED")
        F.need(result.get("status") == "CLOSED" and not result["cleanup"]["errors"]
               and all(result["cleanup"][key] for key in _CLEANUP), "GENERATIONS_CLOSE_UNPROVEN")
        location = handle.location
        F.need(service.closed and service.grant.closed and service.controller.closed
               and service.workspace._closed and service.advertisement.closed
               and not service.controller._busy and not service.advertisement._busy
               and service.read_provider.server is None and not service.read_provider.tasks
               and (service.intake_provider is None or service.intake_provider.server is None
                    and not service.intake_provider.tasks), "GENERATIONS_LIVE_ROLE_REMAINS")
        F.need(location.closed and (location.process is None or location.process.returncode is not None)
               and all(task is None or task.done() for task in
                       (location._spawn_task, location._start_task, location._close_task,
                        location.stderr_task, service._start_task, service._close_task,
                        service._monitor_task, service._retained_task)), "GENERATIONS_LIVE_TASK_REMAINS")
        record["run_state"] = "CLOSED"
        record["closure_sha256"] = P.digest(F.compact(result))
        if record["phase"] == "PROVISIONING":
            record["phase"] = "INCOMPLETE"; record["failure"] = "PROVISIONING_DID_NOT_COMPLETE"
        self._transaction(lambda: self._save(record))
        handle.closed = True; del self._handles[record["slot"]]
        return deepcopy(result)

    def _unknown(self, handle):
        record = self._owned(handle)
        record["run_state"] = "UNKNOWN"; record["failure"] = "CURRENT_RUN_CLOSURE_UNPROVEN"
        if record["phase"] == "PROVISIONING": record["phase"] = "INCOMPLETE"
        self._transaction(lambda: self._save(record))

    def adopt_clock(self, *, lower_utc_ms, valid_for_ms, rate_error_ppm, model_id):
        self._call()
        return ConservativeClock(_ISSUE, self, lower_utc_ms, valid_for_ms, rate_error_ppm, model_id)

    def _time(self, record, clock):
        F.need(type(clock) is ConservativeClock and clock._manager is self, "GENERATIONS_CURRENT_CLOCK")
        lower = clock.lower_bound_ms()
        F.need(lower >= record["config"]["placement"]["retention_not_after_ms"],
               "GENERATIONS_RETENTION_STILL_PROMISED")
        return lower

    def begin_retire(self, generation, clock):
        self._call(); record = self._find(generation)
        F.need(record["phase"] in ("OPEN", "SEALING", "SEALED_SERVING", "INCOMPLETE",
                                   "PROVISIONING", "RETIRING"), "GENERATIONS_RETIRE_PHASE")
        record["retirement_lower_ms"] = self._time(record, clock)
        record["phase"] = "RETIRING"; self._transaction(lambda: self._save(record))
        handle = self._handles.get(record["slot"])
        if handle is not None and handle.service is not None:
            # Prevent late token/restore/custody work before async drain begins.
            handle.service.grant.closed = True
            # Leave _closing to the existing tracked close task. Setting it
            # here would suppress the monitor's finally-triggered auto-close.
            handle.service._wake.set()
        return deepcopy(record)

    def commit_retired(self, generation, clock):
        self._call(); record = self._find(generation)
        F.need(record["phase"] == "RETIRING" and record["run_state"] in ("NONE", "CLOSED")
               and record["slot"] not in self._handles, "GENERATIONS_RETIRE_CLOSURE_UNKNOWN")
        record["retirement_lower_ms"] = self._time(record, clock); record["phase"] = "RETIRED"
        def commit():
            self._save(record)
            sequence, previous = self.db.execute("SELECT sequence,retired_floor FROM meta WHERE id=1").fetchone()
            unretired = [r["sequence"] for r in self._records()
                         if r is not None and r["phase"] != "RETIRED"]
            floor = min(unretired)-1 if unretired else sequence
            F.need(floor >= previous, "GENERATIONS_FLOOR_REGRESSION")
            self.db.execute("UPDATE meta SET retired_floor=? WHERE id=1", (floor,))
        self._transaction(commit)
        return deepcopy(record)

    def plan_reclamation(self, generation):
        self._call(); record = self._find(generation, retired=True)
        F.need(record["phase"] == "RETIRED" and record["run_state"] in ("NONE", "CLOSED")
               and record["slot"] not in self._handles, "GENERATIONS_RECLAIM_NOT_RETIRED")
        root = self._check_marker(record)
        return {"schema": "DMKN_V5_RECLAMATION_BOUNDARY_PLAN_V1", "root": str(root),
            "generation": generation, "marker_sha256": P.digest(self._generation_marker(record)),
            "maximum_runs": record["config"]["placement"]["max_runs"], "charged_runs": record["runs"],
            "deletion_authorized": False, "slot_remains_occupied": True,
            "required_boundary": "EXACT_ORDINARY_MANAGED_FILE_INVENTORY_AND_FINITE_RECLAIMER_NOT_IMPLEMENTED"}

    def status(self):
        self._call()
        sequence, floor = self.db.execute("SELECT sequence,retired_floor FROM meta WHERE id=1").fetchone()
        return {"schema": "DMKN_V5_TWO_GENERATION_STATUS_V1", "allocated_sequence": sequence,
            "retired_floor": floor, "slots": deepcopy(self._records()),
            "reserved_bytes": sum(s["reserved_bytes"] for s in self.config["slots"]),
            "physical_envelope_adopted": False, "unknown_recovery_supported": False,
            "reclamation_implemented": False, "mathematical_acceptance": False}

    def _release(self):
        self._closed = True
        errors = []
        for name in ("db", "_lock"):
            resource = getattr(self, name)
            if resource is not None:
                try:
                    resource.close(); setattr(self, name, None)
                except BaseException as error:
                    errors.append(error)
        if errors:
            self._poisoned = True
            for unused in errors[1:]: errors[0].add_note("GENERATIONS_ADDITIONAL_CLOSE_FAILURE")
            raise errors[0]

    def close(self):
        F.need(not self._handles, "GENERATIONS_ACTORS_REQUIRE_CLOSE_OR_OUTER_RECOVERY")
        self._release()
