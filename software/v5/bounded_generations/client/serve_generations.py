"""Compose the existing exact PlacementService; no replacement network/checker."""
import asyncio
from copy import deepcopy
from pathlib import Path
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ROLE_NAMES
from placement.lifecycle import ManagedGenerations, _deadline, _disjoint
from .serve_placement import PlacementService


class GenerationServices:
    """Owner API inside existing finite whole-process containment.

    runtime binds an existing adopted source/install and their exact maps.
    Fresh run directories are allocated only after the durable run charge.
    This object does not adopt imported closure reports or clock timestamps.
    """
    def __init__(self, manager, runtime):
        F.need(type(manager) is ManagedGenerations, "GENERATIONS_EXACT_MANAGER")
        manager._active()
        F.fields(runtime, ("source_root", "installation_root", "source_pins", "role_pins"))
        F.need(type(runtime["source_pins"]) is dict and set(runtime["source_pins"]) == SOURCE_NAMES
               and type(runtime["role_pins"]) is dict and set(runtime["role_pins"]) == ROLE_NAMES,
               "GENERATIONS_LOCATION_SOURCE_MAP")
        for value in (*runtime["source_pins"].values(), *runtime["role_pins"].values()): F.hexid(value)
        for name in ("source_root", "installation_root"):
            root = ordinary(runtime[name])
            F.need(_disjoint(manager.root, root), "GENERATIONS_RUNTIME_ROOT_OVERLAP")
        F.need(getattr(manager, "_services", None) is None, "GENERATIONS_COMPOSER_ALREADY_OWNED")
        self.manager = manager; self.runtime = deepcopy(runtime); self._raw = F.compact(runtime)
        self._tasks = {}
        manager._services = self

    def _active(self):
        self.manager._active()
        F.need(getattr(self.manager, "_services", None) is self
               and F.compact(self.runtime) == self._raw, "GENERATIONS_COMPOSER_CHANGED")

    async def start_slot(self, generation, *, outer_deadline, location_deadline,
                         read_tls_context=None, intake_tls_context=None):
        self._active()
        _deadline(outer_deadline, self.manager.deadline)
        _deadline(location_deadline, outer_deadline-6)
        handle = self.manager.reserve_run(generation, outer_deadline=outer_deadline)
        # Persisted RESERVED now exists. No prior run path is reused on failure.
        task = asyncio.create_task(self._start(handle, location_deadline,
                                              read_tls_context, intake_tls_context))
        self._tasks[generation] = task
        try: return await asyncio.shield(task)
        finally:
            if task.done(): self._tasks.pop(generation, None)

    async def _start(self, handle, location_deadline, read_tls_context, intake_tls_context):
        manager = self.manager; record = manager._owned(handle); generation = record["generation"]
        service = None
        try:
            cfg = record["config"]; spec = manager.config["slots"][record["slot"]]
            manager._check_marker(record)
            path = ordinary(handle.path, fresh=True); path.mkdir()
            adoption = AdoptedLocationRuntime(self.runtime["source_root"], self.runtime["source_pins"],
                installation_root=self.runtime["installation_root"], workspace_root=path)
            config = {**deepcopy(cfg["location"]), "state": str(path/"location-state")}
            location = ServiceLocationProcess(adoption, self.runtime["role_pins"], config,
                                              path/"location-channel", deadline=location_deadline)
            handle.location = location
            fresh = record["phase"] == "PROVISIONING"
            service = PlacementService.open(manager.generation_path(record)/"workspace", cfg["workspace"],
                cfg["placement"], cfg["egress"], location, read_endpoint=spec["read_endpoint"],
                intake_endpoint=spec["intake_endpoint"], limits=cfg["service_limits"],
                outer_deadline=handle.outer_deadline, create=fresh, placement_create=fresh,
                journal_create=fresh, read_tls_context=read_tls_context, intake_tls_context=intake_tls_context)
            manager._attach(handle, service)
            # An interrupted seal is completed before any listener is exposed.
            if record["phase"] in ("SEALING", "SEALED_SERVING"):
                service.controller.seal(service.grant)
            ready = await service.start()
            manager._started(handle)
            return {"generation": generation, "run": record["runs"], "service": ready,
                    "physical_envelope_adopted": False, "mathematical_acceptance": False}
        except BaseException as primary:
            # Keep the original error. Unknown cleanup stays charged/held.
            if service is not None and handle.service is not service:
                # open() acquired actual stores before attachment failed. The
                # local object must be closed, but cannot issue durable CLOSED
                # for a handle to which it was never successfully attached.
                for component, note in ((service, "UNATTACHED_SERVICE_CLOSE_UNCERTAIN"),
                                        (handle.location, "UNATTACHED_LOCATOR_CLOSE_UNCERTAIN")):
                    if component is not None:
                        try: await component.close()
                        except BaseException: primary.add_note("GENERATIONS_"+note)
                try: manager._unknown(handle)
                except BaseException: primary.add_note("GENERATIONS_UNATTACHED_RECORD_UNCERTAIN")
            else:
                try: await self._close_handle(handle)
                except BaseException:
                    primary.add_note("GENERATIONS_ATTACHED_CLOSE_UNCERTAIN")
                    try: manager._unknown(handle)
                    except BaseException: primary.add_note("GENERATIONS_FAILURE_RECORD_UNCERTAIN")
            raise

    def service(self, generation):
        """Current exact owner service; callers retain its existing finite APIs."""
        self._active(); record, handle = self.manager._live(generation)
        F.need(record["phase"] in ("OPEN", "SEALED_SERVING"), "GENERATIONS_SERVICE_PHASE")
        return handle.service

    async def _close_handle(self, handle):
        # Cleanup is attempted even if the manager's operation guard expired;
        # durable close cannot then be asserted without fresh finite authority.
        try: self.manager._closing(handle)
        except BaseException: pass
        if handle.service is not None:
            await handle.service.close()
            return self.manager._closed_run(handle)
        if handle.location is not None:
            await handle.location.close()
        self.manager._unknown(handle)
        raise ValueError("GENERATIONS_CONSTRUCTION_CLOSURE_REQUIRES_EXACT_RECOVERY")

    async def close_slot(self, generation):
        # Await/cancel only this composer's tracked start, within its original
        # finite deadline. Do not leave a late startup orphan after cancellation.
        F.hexid(generation)
        # Same-process cleanup remains possible after the write-authority guard
        # expires. Its durable CLOSED update still requires that guard.
        handle = next((h for h in self.manager._handles.values()
                       if h._binding[1] == generation), None)
        F.need(handle is not None, "GENERATIONS_NO_OWNED_RUN_TO_CLOSE")
        task = self._tasks.get(generation)
        if task is not None and not task.done():
            task.cancel()
            remaining = handle.outer_deadline-time.monotonic()
            F.need(remaining > 0, "GENERATIONS_ORIGINAL_CLOSE_DEADLINE")
            async with asyncio.timeout(remaining):
                await asyncio.shield(asyncio.gather(task, return_exceptions=True))
            F.need(task.done(), "GENERATIONS_START_NOT_DRAINED")
        if handle.closed: return handle.service.report()
        return await self._close_handle(handle)

    async def retire_slot(self, generation, clock):
        self._active(); self.manager.begin_retire(generation, clock)
        record = self.manager._find(generation)
        if record["slot"] in self.manager._handles:
            await self.close_slot(generation)
        return self.manager.commit_retired(generation, clock)

    async def close(self):
        """Attempt both owned roles; one uncertain role never skips the other."""
        generations = [handle._binding[1] for handle in self.manager._handles.values()]
        return await asyncio.gather(*(self.close_slot(generation) for generation in generations),
                                    return_exceptions=True)
