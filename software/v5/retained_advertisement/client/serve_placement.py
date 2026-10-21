"""Trusted-owner finite placement service API; no remote grant or source execution."""
import asyncio
from copy import deepcopy
import math
import ssl
import time
from types import MappingProxyType

from client.workspace_evidence import Workspace
from discovery import formal_features as F
from evidence_network.transport import CompositeProvider
from location.controller_services import ServiceLocationProcess
from location.protocol import OwnerEgressPolicy
from placement.advertisement import PlacementAdvertisement
from placement.controller import PlacementController
from placement.ledger import PlacementLedger

READ_LIMITS = {"max_connections":(1,8),"max_requests":(1,1000000),
               "max_reply_bytes":(1024,2**40),"operation_ms":(1,60000)}
INTAKE_LIMITS = {"max_connections":(1,8),"max_requests":(1,4096),
                 "incoming_bytes":(25600,2**40),"outgoing_bytes":(90112,2**40),
                 "operation_ms":(1,60000)}


def _endpoint(value, policy, tls):
    endpoint = policy.endpoint(value)
    F.need(endpoint.tls == (tls is not None), "PLACEMENT_SERVICE_TLS_BINDING")
    if tls is not None:
        F.need(type(tls) is ssl.SSLContext and tls.protocol == ssl.PROTOCOL_TLS_SERVER
               and tls.minimum_version >= ssl.TLSVersion.TLSv1_2, "PLACEMENT_SERVICE_TLS_CONTEXT")
    return {name:getattr(endpoint,name) for name in ("host","port","tls","server_name")}


def _limits(value):
    F.fields(value,("lifetime_seconds","controller_cpu_seconds","controller_calls",
                    "health_interval_ms","journal_pages","read","intake"))
    for key,lo,hi in (("lifetime_seconds",1,3600),("controller_cpu_seconds",1,3600),
                      ("controller_calls",1,8192),("health_interval_ms",100,3600000),
                      ("journal_pages",256,65536)):
        F.uint(value[key],lo,hi,"PLACEMENT_SERVICE_LIMIT:"+key)
    for group,spec in (("read",READ_LIMITS),("intake",INTAKE_LIMITS)):
        F.fields(value[group],spec)
        for key,bounds in spec.items(): F.uint(value[group][key],*bounds,"PLACEMENT_SERVICE_LIMIT:"+key)
    return deepcopy(value)


class PlacementService:
    """Open once; start, issue local tokens, serve, and close early when finished.

    The supplied exact fresh locator is built by a trusted owner using existing
    runtime adoption/pins. This class owns its lifecycle after open succeeds.
    External whole-process containment remains a caller obligation.
    """
    @classmethod
    def open(cls, workspace_path, workspace_config, placement_config, egress, location, *,
             read_endpoint, intake_endpoint, limits, outer_deadline,
             create=False, placement_create=False, journal_create=False,
             read_tls_context=None, intake_tls_context=None):
        selected = _limits(limits); policy = OwnerEgressPolicy(egress)
        read = _endpoint(read_endpoint,policy,read_tls_context)
        intake = _endpoint(intake_endpoint,policy,intake_tls_context)
        F.need((read["host"],read["port"]) != (intake["host"],intake["port"]),
               "PLACEMENT_SERVICE_SEPARATE_LISTENERS")
        F.need(type(location) is ServiceLocationProcess and location.process is None
               and location._start_task is None and location._spawn_task is None
               and location._close_task is None and not location.closed
               and not location.channel_failed and location.sequence == 0,
               "PLACEMENT_SERVICE_FRESH_LOCATOR")
        F.need(location.config["schema"] == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1"
               and location.config["role"] == "index-provider"
               and location.config["namespace"] == placement_config["namespace"]
               and location.config["endpoints"] == [read]
               and location.config["egress"] == egress, "PLACEMENT_SERVICE_LOCATOR_BINDING")
        for value in (create,placement_create,journal_create):
            F.need(type(value) is bool,"PLACEMENT_SERVICE_CREATE")
        now = time.monotonic()
        F.need(type(outer_deadline) in (int,float) and math.isfinite(outer_deadline)
               and now < outer_deadline <= now+3600, "PLACEMENT_SERVICE_OUTER_DEADLINE")
        operation = location.config["limits"]["operation_ms"]/1000
        drain = max(selected["read"]["operation_ms"],selected["intake"]["operation_ms"])/1000+5
        # Intake and read roles each retain their original drain allowance.
        reserve = 2*drain+2*operation+location.cleanup_seconds+5
        stop = min(location.deadline,outer_deadline-location.cleanup_seconds-drain-2)
        active_end = min(now+selected["lifetime_seconds"],stop-2*operation,
                         outer_deadline-reserve)
        F.need(active_end-now >= 1 and location.deadline <= outer_deadline-location.cleanup_seconds
               and location.config["limits"]["service_ms"] >= math.ceil((stop-now)*1000),
               "PLACEMENT_SERVICE_CLEANUP_MARGIN")
        health_cap = math.ceil(selected["lifetime_seconds"]*1000/selected["health_interval_ms"])+2
        F.need(health_cap+2*placement_config["max_cells"]+1 <=
               min(location.config["limits"]["commands"],60), "PLACEMENT_SERVICE_COMMAND_RESERVATION")
        self = cls.__new__(cls)
        self.workspace = self.ledger = self.controller = self.grant = self.advertisement = None
        self.read_provider = self.intake_provider = None
        self.location = location
        self.limits = selected; self._limits_raw = F.compact(selected)
        self.read_endpoint,self.intake_endpoint = read,intake
        self._endpoints_raw = F.compact([read,intake])
        self._tls = read_tls_context,intake_tls_context
        self.outer_deadline,self._outer = outer_deadline,outer_deadline
        self._stop_deadline,self._drain_seconds = stop,drain
        self.closed,self._closing,self._started = False,False,False
        self._start_task = self._close_task = self._monitor_task = None
        self._retained_task = None
        self._wake = asyncio.Event(); self._failure = None
        self._cleanup = {"intake_closed":False,"retained_closed":False,"location_closed":False,"read_closed":False,
                         "journal_closed":False,"controller_closed":False,"workspace_closed":False,
                         "errors":[]}
        self._final = None
        try:
            self.workspace = Workspace.open(workspace_path,workspace_config,create=create)
            self.ledger = PlacementLedger.open(self.workspace,placement_config,create=placement_create)
            self.controller = PlacementController(self.ledger,egress)
            wall = math.floor(active_end-time.monotonic())
            F.need(wall >= 1,"PLACEMENT_SERVICE_STARTUP_INTERVAL")
            self.grant = self.controller.start_service(wall_seconds=wall,
                controller_cpu_seconds=selected["controller_cpu_seconds"],calls=selected["controller_calls"])
            self.deadline = self.grant.deadline; self._deadline = self.deadline
            self.bindings = MappingProxyType({name:self.ledger.config[name] for name in
                ("service_epoch","generation","namespace","wire_profile_id")})
            self._bindings_raw = F.compact(dict(self.bindings))
            self.read_provider = CompositeProvider(index=self.workspace.index,custody=self.workspace.modules,
                                                  packets=self.workspace.packets,**selected["read"])
            self.advertisement = PlacementAdvertisement.open(self.controller,self.grant,location,
                self.read_provider,read,health_cap=health_cap,journal_pages=selected["journal_pages"],
                create=journal_create)
            self._roles = (self.workspace,self.ledger,self.controller,self.grant,self.advertisement,
                           self.location,self.read_provider)
            self._active()
            return self
        except BaseException as error:
            # No listeners/processes have started. Preserve construction failure
            # while attempting every acquired local resource close.
            for name in ("advertisement","controller","ledger","workspace"):
                component = getattr(self,name,None)
                if component is not None:
                    try: component.close()
                    except BaseException: error.add_note("PLACEMENT_SERVICE_PARTIAL_CLOSE:"+name)
            self.closed = True
            raise

    def _active(self):
        F.need(not self.closed and not self._closing,"PLACEMENT_SERVICE_CLOSED")
        F.need(all(actual is original for actual,original in zip(
                (self.workspace,self.ledger,self.controller,self.grant,self.advertisement,
                 self.location,self.read_provider),self._roles)),
               "PLACEMENT_SERVICE_OWNER_ROLES")
        F.need(self.deadline == self._deadline and self.outer_deadline == self._outer
               and F.compact(dict(self.bindings)) == self._bindings_raw
               and F.compact(self.limits) == self._limits_raw
               and F.compact([self.read_endpoint,self.intake_endpoint]) == self._endpoints_raw,
               "PLACEMENT_SERVICE_CONFIGURATION_CHANGED")
        self.controller._active(self.grant)
        F.need(time.monotonic() < self._deadline,"PLACEMENT_SERVICE_EXPIRED")

    async def start(self):
        self._active()
        F.need(self._start_task is None,"PLACEMENT_SERVICE_ALREADY_STARTED")
        self._start_task = asyncio.create_task(self._start())
        try: return await asyncio.shield(self._start_task)
        except BaseException:
            self._failure = "PLACEMENT_SERVICE_START_FAILED"
            await self.close()
            raise

    async def _start(self):
        from placement.network import PlacementProvider
        async with asyncio.timeout_at(self._deadline):
            actual = await self.read_provider.start(self.read_endpoint["host"],self.read_endpoint["port"],
                                                    tls_context=self._tls[0])
            F.need((actual.host,actual.port,actual.tls) == tuple(self.read_endpoint[name]
                   for name in ("host","port","tls")),"PLACEMENT_SERVICE_READ_ENDPOINT_CHANGED")
            self._active()
            ready = await self.location.start()
            F.need(ready.get("namespace") == self.bindings["namespace"]
                   and ready.get("role") == "index-provider" and ready.get("status") == "RUNNING",
                   "PLACEMENT_SERVICE_LOCATION_START")
            await self.advertisement.health(until=min(self._deadline,
                time.monotonic()+self.location.config["limits"]["operation_ms"]/1000))
            self.intake_provider = PlacementProvider(self,limits=self.limits["intake"])
            actual = await self.intake_provider.start(self.intake_endpoint["host"],self.intake_endpoint["port"],
                                                      tls_context=self._tls[1])
            F.need((actual.host,actual.port,actual.tls) == tuple(self.intake_endpoint[name]
                   for name in ("host","port","tls")),"PLACEMENT_SERVICE_INTAKE_ENDPOINT_CHANGED")
            self._active(); self._started = True
            self._monitor_task = asyncio.create_task(self._monitor())
            return self.ready()

    def ready(self):
        self._active(); F.need(self._started,"PLACEMENT_SERVICE_NOT_STARTED")
        return {"schema":"DMKN_V5_PLACEMENT_SERVICE_READY_V1","bindings":dict(self.bindings),
            "read_endpoint":deepcopy(self.read_endpoint),"intake_endpoint":deepcopy(self.intake_endpoint),
            "deadline":self._deadline,"outer_deadline":self._outer,
            "tls_scope":"OWNER_CONTEXT_AND_CLIENT_CERTIFICATE_VALIDATION_NOT_NOISE_IDENTITY",
            "ingress_scope":"POST_HANDSHAKE_APP_LIMITS_NOT_A_TLS_HANDSHAKE_CONCURRENCY_CAP",
            "mathematical_acceptance":False,"global_complete":False}

    def issue_token(self,source,*,write_until_ms,retention_until_ms,limits):
        self._active(); F.need(self._started,"PLACEMENT_SERVICE_NOT_STARTED")
        # Sole secret-bearing return: only to the trusted local caller. Never
        # save this return into ready/report/configuration or an HTTP route.
        return self.controller.issue_token(self.grant,source,write_until_ms=write_until_ms,
            retention_until_ms=retention_until_ms,limits=limits)

    async def submit(self,token,manifest_bytes,*,until):
        self._active(); F.need(self._started,"PLACEMENT_SERVICE_NOT_STARTED")
        F.need(type(until) in (int,float) and math.isfinite(until)
               and time.monotonic() < until <= self._deadline,"PLACEMENT_SERVICE_REQUEST_DEADLINE")
        return await self.advertisement.submit(token,manifest_bytes,until=until)

    def status(self,token,request_id,*,until):
        self._active(); F.need(self._started,"PLACEMENT_SERVICE_NOT_STARTED")
        F.need(type(until) in (int,float) and math.isfinite(until)
               and time.monotonic() < until <= self._deadline,"PLACEMENT_SERVICE_REQUEST_DEADLINE")
        return self.advertisement.status(token,request_id,until=until)

    async def advertise_retained(self,request_id,*,until):
        """Local owner only; no public token or wire route starts restoration."""
        self._active(); F.need(self._started,"PLACEMENT_SERVICE_NOT_STARTED")
        F.need(type(until) in (int,float) and math.isfinite(until)
               and time.monotonic() < until <= self._deadline,"PLACEMENT_SERVICE_REQUEST_DEADLINE")
        F.need(self._retained_task is None,"PLACEMENT_SERVICE_RETAINED_BUSY")
        task = asyncio.create_task(self.advertisement.advertise_retained(request_id,until=until))
        self._retained_task = task
        try:
            return await task
        finally:
            # A pending/cancellation-resistant task stays owned by close().
            if task.done() and self._retained_task is task: self._retained_task = None

    async def _monitor(self):
        try:
            interval = self.limits["health_interval_ms"]/1000
            while not self._wake.is_set():
                remaining = self._deadline-time.monotonic()
                if remaining <= 0: break
                try: await asyncio.wait_for(self._wake.wait(),min(interval,remaining))
                except TimeoutError: pass
                if self._wake.is_set(): return
                if time.monotonic() >= self._deadline: break
                await self.advertisement.health(until=min(self._deadline,
                    time.monotonic()+self.location.config["limits"]["operation_ms"]/1000))
        except asyncio.CancelledError:
            raise
        except BaseException:
            self._failure = "PLACEMENT_SERVICE_HEALTH_FAILED"
        finally:
            if not self._closing and self._close_task is None:
                # The same tracked close task enforces finite lifetime even
                # when an owner chooses not to wait on this service directly.
                self._close_task = asyncio.create_task(self._close())

    async def close(self):
        if self._close_task is None: self._close_task = asyncio.create_task(self._close())
        return await asyncio.shield(self._close_task)

    async def _close(self):
        self._closing = True; self._wake.set()
        errors = self._cleanup["errors"]
        def failed(component): errors.append({"component":component,"code":"CLEANUP_UNCERTAIN"})
        async def bounded(awaitable,seconds):
            remaining = min(seconds,self._outer-time.monotonic())
            if remaining <= 0:
                if hasattr(awaitable,"close"): awaitable.close()
                raise RuntimeError("PLACEMENT_SERVICE_CLEANUP_DEADLINE")
            async with asyncio.timeout(remaining): return await awaitable
        for name in ("_monitor_task","_start_task"):
            task = getattr(self,name)
            if task is not None and task is not asyncio.current_task() and not task.done():
                task.cancel()
                try: await bounded(asyncio.gather(task,return_exceptions=True),1)
                except BaseException: failed(name)
        # Both actors share one original drain interval. Cancel owner work
        # before draining HTTP so its cancellation can make progress concurrently.
        intake_until = min(self._outer,time.monotonic()+self._drain_seconds)
        retained = self._retained_task
        if retained is not None and not retained.done(): retained.cancel()
        if self.intake_provider is None:
            self._cleanup["intake_closed"] = True
        else:
            try:
                await self.intake_provider.stop(until=intake_until)
                self._cleanup["intake_closed"] = (self.intake_provider.server is None
                                                   and not self.intake_provider.tasks)
                F.need(self._cleanup["intake_closed"],"PLACEMENT_SERVICE_INTAKE_CLOSE")
            except BaseException: failed("intake")
        try:
            if retained is not None and not retained.done():
                F.need(time.monotonic() < intake_until,"PLACEMENT_SERVICE_RETAINED_DRAIN_DEADLINE")
                async with asyncio.timeout_at(intake_until):
                    await asyncio.shield(asyncio.gather(retained,return_exceptions=True))
                F.need(time.monotonic() < intake_until,"PLACEMENT_SERVICE_RETAINED_DRAIN_DEADLINE")
            self._cleanup["retained_closed"] = retained is None or retained.done()
            F.need(self._cleanup["retained_closed"],"PLACEMENT_SERVICE_RETAINED_CLOSE")
            if retained is not None:
                if not retained.cancelled(): retained.exception()
                if self._retained_task is retained: self._retained_task = None
        except BaseException: failed("retained")
        # No new/late custody or journal commit after the attempted intake
        # drain. A missed actor cannot retain the old live write authority.
        self.grant.closed = True
        try:
            n = self.location
            if n.process is not None and n.process.returncode is None and not n.closed and not n.channel_failed:
                until = min(self._stop_deadline,time.monotonic()+n.config["limits"]["operation_ms"]/1000)
                value = await n.command("stop",{},until=until)
                F.need(value.get("status") == "STOPPED","PLACEMENT_SERVICE_STOP_UNCONFIRMED")
        except BaseException: failed("location_stop")
        try:
            # Native teardown keeps its own six-second bound. Exact runtime
            # and role validation use only the original remaining close budget.
            # Keep a read-provider drain and final margin after this cutoff.
            location_until = self._outer-self._drain_seconds-2
            F.need(time.monotonic() < location_until,"PLACEMENT_SERVICE_LOCATION_CLOSE_DEADLINE")
            async with asyncio.timeout_at(location_until):
                await self.location.close()
            # Synchronous validation cannot be interrupted by an asyncio timer.
            F.need(time.monotonic() < location_until,"PLACEMENT_SERVICE_LOCATION_CLOSE_DEADLINE")
            state = self.location.report()
            self._cleanup["location_closed"] = (state["closed"] and state["returncode"] in (None,0)
                and not state["channel_failed"] and not state["forced_termination"])
            F.need(self._cleanup["location_closed"],"PLACEMENT_SERVICE_LOCATION_CLOSE")
        except BaseException: failed("location_close")
        try:
            await bounded(self.read_provider.stop(),self._drain_seconds)
            self._cleanup["read_closed"] = self.read_provider.server is None and not self.read_provider.tasks
            F.need(self._cleanup["read_closed"],"PLACEMENT_SERVICE_READ_CLOSE")
        except BaseException: failed("read")
        # Do not close SQLite out from under an actor whose cancellation failed.
        idle = (self._cleanup["intake_closed"] and self._cleanup["retained_closed"]
                and (self._retained_task is None or self._retained_task.done()) and self._cleanup["read_closed"]
                and not self.controller._busy and not self.advertisement._busy)
        if idle:
            for name,field in (("advertisement","journal_closed"),("controller","controller_closed"),
                               ("workspace","workspace_closed")):
                try:
                    getattr(self,name).close(); self._cleanup[field] = True
                except BaseException: failed(name)
        else: failed("live_actor_prevents_store_close")
        observations = {}
        for name,component,method in (("intake",self.intake_provider,"report"),
                                      ("read",self.read_provider,"status"),
                                      ("location",self.location,"report")):
            if component is None:
                observations[name] = None
            else:
                try: observations[name] = getattr(component,method)()
                except BaseException:
                    observations[name] = None; failed(name+"_report")
        self.closed = True
        ok = not errors and all(self._cleanup[key] for key in
            ("intake_closed","retained_closed","location_closed","read_closed","journal_closed","controller_closed","workspace_closed"))
        if time.monotonic() >= self._outer:
            ok = False; failed("original_outer_deadline")
        self._final = {"schema":"DMKN_V5_PLACEMENT_SERVICE_RESULT_V1",
            "status":"CLOSED" if ok and self._failure is None else "FAILED",
            "failure_code":self._failure,"bindings":dict(self.bindings),"cleanup":deepcopy(self._cleanup),
            "route":self.advertisement.report(),"observed":observations,
            "mathematical_acceptance":False,"global_complete":False,
            "public_deployment_qualified":False}
        return deepcopy(self._final)

    def report(self):
        if self._final is not None: return deepcopy(self._final)
        return {"schema":"DMKN_V5_PLACEMENT_SERVICE_STATUS_V1","started":self._started,
            "closing":self._closing,"closed":self.closed,"bindings":dict(self.bindings),
            "retained_active":self._retained_task is not None and not self._retained_task.done(),
            "route":self.advertisement.report(),"failure_code":self._failure,
            "mathematical_acceptance":False,"global_complete":False}

    async def __aenter__(self):
        await self.start(); return self

    async def __aexit__(self,*unused):
        report = await self.close()
        F.need(report["status"] == "CLOSED","PLACEMENT_SERVICE_CLEANUP_FAILED")
