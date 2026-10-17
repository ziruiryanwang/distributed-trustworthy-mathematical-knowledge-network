"""Owner-created bounded private Node channel; caller must supply hard Job containment.

No remote JSON or caller callback can assert an authenticated channel peer.
This controller creates and owns that channel and all workflow tickets itself.
"""
import asyncio
import base64
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import struct
import time
from types import MappingProxyType

from discovery import formal_features as F
from .workflow import WorkflowBudget

MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
SOURCE_NAMES = frozenset(("protocol.mjs", "framing.mjs", "intent.mjs", "runtime.mjs",
    "maintained.mjs", "transport.mjs", "composition.mjs", "ipc_wire.mjs", "node_entry.mjs"))
FRAME_BYTES, TOTAL_BYTES, FRAME_COUNT = 16384, 1024**2, 64


def ordinary(path, *, directory=False):
    path = Path(path)
    F.need(path.is_absolute() and str(path.resolve()) == str(path), "LOCATION_CONTROLLER_CANONICAL")
    for item in (path, *path.parents):
        F.need(not item.is_symlink() and not item.is_junction(), "LOCATION_CONTROLLER_NO_LINKS")
    F.need(path.is_dir() if directory else path.is_file(), "LOCATION_CONTROLLER_FILE_KIND")
    return path


def pin(path, maximum=128*1024**2):
    path = ordinary(path); size = path.stat().st_size
    F.need(0 <= size <= maximum, "LOCATION_CONTROLLER_FILE_SIZE")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    F.need(path.stat().st_size == size, "LOCATION_CONTROLLER_FILE_CHANGED")
    return {"bytes": size, "sha256": digest}


def disjoint(left, right):
    return not left.is_relative_to(right) and not right.is_relative_to(left)


def fresh_workspace_path(workspace, value):
    """Owner-only fresh output; ordinary ancestors, never a textual prefix."""
    workspace = ordinary(workspace, directory=True)
    F.need(isinstance(value, (str, Path)), "LOCATION_WORKSPACE_PATH_TYPE")
    path = Path(value)
    F.need(path.is_absolute() and str(path.resolve()) == str(path) and path != workspace
           and path.is_relative_to(workspace) and not path.exists()
           and not path.is_symlink() and not path.is_junction(),
           "LOCATION_FRESH_WORKSPACE_PATH")
    ordinary(path.parent, directory=True)
    return path


@dataclass(frozen=True, init=False, slots=True)
class AdoptedLocationRuntime:
    """Immutable owner paths for one fixed Windows runtime, never remote input."""
    source: Path
    installation: Path
    workspace: Path
    source_pins: object
    node: Path

    def __init__(self, source_directory, source_pins, *, installation_root, workspace_root):
        source = ordinary(source_directory, directory=True)
        installation = ordinary(installation_root, directory=True)
        workspace = ordinary(workspace_root, directory=True)
        F.need(disjoint(workspace, source) and disjoint(workspace, installation),
               "LOCATION_WORKSPACE_IMMUTABLE_ROOT_OVERLAP")
        F.need(type(source_pins) is dict and set(source_pins) == SOURCE_NAMES, "LOCATION_CONTROLLER_SOURCE_MAP")
        pins = deepcopy(source_pins)
        for value in pins.values(): F.hexid(value)
        for name, value in (("source", source), ("installation", installation), ("workspace", workspace),
                            ("source_pins", MappingProxyType(pins)),
                            ("node", installation / "runtime/node/node.exe")):
            object.__setattr__(self, name, value)

    def source_map(self, role_pins):
        """Fixed-shape local launch binding; caller supplies adopted role pins."""
        return {"schema": "DMKN_V5_LOCAL_NODE_SOURCE_MAP_V2", "root": str(self.source),
                "installation_root": str(self.installation), "workspace_root": str(self.workspace),
                "files": {**self.source_pins, **role_pins}, "manifest_sha256": MANIFEST_SHA}

    def verify(self):
        began = time.process_time(); wall = time.monotonic()
        for root in (self.source, self.installation, self.workspace): ordinary(root, directory=True)
        manifest_path = self.installation / "RELEASE-MANIFEST.json"
        F.need(pin(manifest_path, 8*1024**2)["sha256"] == MANIFEST_SHA, "LOCATION_CONTROLLER_MANIFEST")
        manifest = json.loads(manifest_path.read_bytes())
        selected = {name: row for name, row in manifest["files"].items()
                    if name.startswith(("overlay/", "runtime/node/"))}
        F.need(len(selected) == 5896, "LOCATION_CONTROLLER_RUNTIME_MAP")
        actual, directories = set(), 0
        for start in (self.installation / "overlay", self.installation / "runtime/node"):
            for parent, children, files in os.walk(start, followlinks=False):
                parent = ordinary(Path(parent), directory=True); directories += 1
                F.need(directories <= 10000, "LOCATION_CONTROLLER_TREE_BOUND")
                for child in children: ordinary(parent / child, directory=True)
                for name in files:
                    actual.add((parent / name).relative_to(self.installation).as_posix())
                    F.need(len(actual) <= 10000, "LOCATION_CONTROLLER_TREE_BOUND")
        F.need(actual == set(selected), "LOCATION_CONTROLLER_RUNTIME_CENSUS")
        total = 0
        for name, expected in selected.items():
            F.need(pin(self.installation / name) == expected, "LOCATION_CONTROLLER_RUNTIME_PIN:" + name)
            total += expected["bytes"]
        F.need(total <= 192*1024**2, "LOCATION_CONTROLLER_RUNTIME_TOTAL")
        for name, expected in self.source_pins.items():
            F.need(pin(self.source / name, 2*1024**2)["sha256"] == expected, "LOCATION_CONTROLLER_SOURCE_PIN:" + name)
        return {"files": len(selected), "bytes": total, "cpu_seconds": time.process_time()-began,
                "wall_seconds": time.monotonic()-wall,
                "parent_job_containment": "REQUIRED_CALLER_CONTRACT_NOT_CHECKED_HERE"}


class LocationProcess:
    def __init__(self, adoption, configuration, evidence, *, deadline):
        F.need(type(adoption) is AdoptedLocationRuntime, "LOCATION_OWNER_ADOPTION_REQUIRED")
        self.adoption, self.config = adoption, deepcopy(configuration)
        self._origin_adoption = adoption
        self.evidence = fresh_workspace_path(adoption.workspace, evidence)
        F.need(type(deadline) in (int, float) and time.monotonic() < deadline <= time.monotonic()+3600,
               "LOCATION_CONTROLLER_ABSOLUTE_DEADLINE")
        self.deadline = deadline; self.process = None; self.sequence = 0; self.lock = asyncio.Lock()
        self.sent = self.received = self.read_frames = 0; self.stderr = bytearray(); self.stderr_task = None
        self.channel_failed = False; self.closed = False; self.pre = self.post = None
        self._close_task = self._start_task = self._spawn_task = None
        self.cleanup_seconds = 6
        self.forced_termination = False

    def _remaining(self, until=None):
        remaining = min(self.deadline, until if until is not None else self.deadline) - time.monotonic()
        F.need(remaining > 0 and not self.channel_failed, "LOCATION_CONTROLLER_EXPIRED_OR_FAILED")
        return remaining

    async def _stderr(self):
        while True:
            chunk = await self.process.stderr.read(4096)
            if not chunk: return
            self.stderr.extend(chunk)
            if len(self.stderr) > 65536:
                self.channel_failed = True; self.process.kill(); return

    async def _read(self, until):
        async def exact(count):
            try: raw = await asyncio.wait_for(self.process.stdout.readexactly(count), self._remaining(until))
            except asyncio.IncompleteReadError as error:
                self.received += len(error.partial); raise
            self.received += len(raw)
            F.need(self.received <= TOTAL_BYTES, "LOCATION_CONTROLLER_REPLY_CAP")
            return raw
        size = struct.unpack(">I", await exact(4))[0]
        F.uint(size, 1, FRAME_BYTES, "LOCATION_CONTROLLER_FRAME_CAP")
        self.read_frames += 1; F.need(self.read_frames <= FRAME_COUNT, "LOCATION_CONTROLLER_FRAME_COUNT")
        return F.strict(await exact(size), FRAME_BYTES)

    async def start(self):
        F.need(self._start_task is None and not self.closed, "LOCATION_CONTROLLER_ALREADY_STARTED")
        self._start_task = asyncio.create_task(self._start_core())
        try:
            return await asyncio.shield(self._start_task)
        except BaseException:
            self.channel_failed = True
            await self.close()
            raise

    async def _start_core(self):
        # Only the reviewed role-aware successor has a portable V2 bootstrap.
        # The retained legacy Node entry is pinned, not a public launch route.
        F.need(False, "LOCATION_PORTABLE_SERVICE_ENTRY_REQUIRED")

    async def command(self, command, payload, *, until=None):
        await asyncio.wait_for(self.lock.acquire(), self._remaining(until))
        try:
            F.need(self.process is not None and not self.closed and self.process.returncode is None,
                   "LOCATION_CONTROLLER_NOT_RUNNING")
            remaining = self._remaining(until)
            F.need(self.sequence + 2 < FRAME_COUNT, "LOCATION_CONTROLLER_COMMAND_CAP")
            self.sequence += 1
            message = {"schema": "DMKN_V5_LOCATION_IPC_COMMAND_V1", "sequence": self.sequence,
                       "command": command, "payload": payload, "remaining_wall_ms": max(1, int(remaining*1000))}
            raw = F.compact(message)
            F.need(len(raw) <= FRAME_BYTES and self.sent+4+len(raw) <= TOTAL_BYTES, "LOCATION_CONTROLLER_SEND_CAP")
            self.sent += 4+len(raw)
            try:
                self.process.stdin.write(struct.pack(">I", len(raw))+raw)
                await asyncio.wait_for(self.process.stdin.drain(), self._remaining(until))
                reply = await self._read(min(self.deadline, until or self.deadline))
                F.fields(reply, ("schema", "sequence", "status", "result"))
                F.need(reply["schema"] == "DMKN_V5_LOCATION_IPC_REPLY_V1" and reply["sequence"] == self.sequence,
                       "LOCATION_CONTROLLER_REPLY_BINDING")
                F.need(reply["status"] == "OK", "LOCATION_CHILD_REFUSAL:"+str(reply["result"])[:500])
                return reply["result"]
            except BaseException:
                self.channel_failed = True
                if self.process.returncode is None:
                    self.forced_termination = True; self.process.kill()
                raise
        finally:
            self.lock.release()

    async def close(self):
        if self._close_task is None:
            self._close_task = asyncio.create_task(self._close_core())
        await asyncio.shield(self._close_task)

    async def _close_core(self):
        self.closed = True
        cleanup_deadline = time.monotonic()+self.cleanup_seconds
        async def teardown(awaitable):
            remaining = cleanup_deadline-time.monotonic()
            F.need(remaining > 0, "LOCATION_CONTROLLER_TEARDOWN_DEADLINE")
            return await asyncio.wait_for(awaitable, remaining)
        try:
            if self._spawn_task is not None:
                if not self._spawn_task.done():
                    def kill_late(future):
                        if not future.cancelled() and future.exception() is None:
                            child = future.result()
                            if self.closed and child.returncode is None:
                                self.forced_termination = True; child.kill()
                    self._spawn_task.add_done_callback(kill_late)
                self.process = await teardown(asyncio.shield(self._spawn_task))
            if self.process is not None:
                if self.process.stdin is not None: self.process.stdin.close()
                try: await asyncio.wait_for(self.process.wait(), min(2, max(0.001, cleanup_deadline-time.monotonic())))
                except asyncio.TimeoutError:
                    self.channel_failed = True; self.forced_termination = True; self.process.kill()
                    await teardown(self.process.wait())
                if self.stderr_task is not None: await teardown(self.stderr_task)
            if self._start_task is not None and self._start_task is not asyncio.current_task():
                # The core has no recursive close call. Reaping causes any READY
                # read to fail; completed startup errors are retained by start.
                try: await teardown(asyncio.shield(self._start_task))
                except BaseException:
                    if not self._start_task.done(): raise
        finally:
            self.post = self._origin_adoption.verify()
            F.need(self.adoption is self._origin_adoption, "LOCATION_OWNER_ADOPTION_CHANGED")

    def report(self):
        return {"sent_bytes": self.sent, "received_bytes": self.received, "commands": self.sequence,
                "reply_frames": self.read_frames, "channel_failed": self.channel_failed, "closed": self.closed,
                "returncode": None if self.process is None else self.process.returncode,
                "stderr_bytes": len(self.stderr), "runtime_pre": self.pre, "runtime_post": self.post,
                "cleanup_allowance_seconds": self.cleanup_seconds, "forced_termination": self.forced_termination,
                "pipe_receive_scope": "CONSUMED_COMPLETE_OR_EOF_PARTIAL_BYTES_NOT_UNREAD_OS_PIPE_ARRIVALS",
                "mathematical_acceptance": False}


class LocatedWorkflow:
    def __init__(self, channel, namespace, features, limits, search_limits, policy):
        F.need(type(channel) is LocationProcess, "LOCATION_PRIVATE_CHILD_REQUIRED")
        self.channel = channel
        self._workflow = WorkflowBudget(namespace, features, limits, search_limits, policy)
        self.deadline = min(channel.deadline, self._workflow._deadline)
        self._workflow._deadline = self.deadline

    async def route(self, features, stripe=0, *, event_cap, peer_cap):
        ticket = self._workflow.begin_route(features, stripe, event_cap=event_cap, peer_cap=peer_cap)
        settled = False
        try:
            ticket["remaining_wall_ms"] = max(0, int((self.deadline-time.monotonic())*1000))
            reply = await self.channel.command("locate", ticket, until=self.deadline)
            F.need(reply["ticket"] == ticket["ticket"] and reply["route_key"] == ticket["route_key"], "LOCATION_ROUTE_CHANNEL_BINDING")
            settled = True
            return self._workflow.accept_route(ticket["ticket"], reply["peers"])
        finally:
            if not settled: self._workflow.abandon_route(ticket["ticket"])

    async def descriptor(self, peer, route_key, *, max_bytes=4096, max_age_ms=10000):
        ticket = self._workflow.begin_descriptor(peer, route_key, max_bytes=max_bytes, max_age_ms=max_age_ms)
        settled = False
        try:
            until = min(self.deadline, ticket.pop("until"))
            ticket["remaining_wall_ms"] = max(0, int((until-time.monotonic())*1000))
            reply = await self.channel.command("descriptor", ticket, until=until)
            F.need(reply["ticket"] == ticket["ticket"] and reply["authenticated_peer"] == peer, "LOCATION_DESCRIPTOR_CHANNEL_BINDING")
            raw = base64.b64decode(reply["raw_base64"], validate=True)
            settled = True
            return self._workflow.accept_descriptor(ticket["ticket"], raw, reply["authenticated_peer"])
        finally:
            if not settled: self._workflow.abandon_descriptor(ticket["ticket"])

    def begin_search(self): return self._workflow.begin_search()
    def report(self): return {"workflow": self._workflow.report(), "location_transport": self.channel.report()}
