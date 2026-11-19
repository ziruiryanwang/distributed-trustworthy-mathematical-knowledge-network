"""Ordinary-only owned private Node channel; caller supplies hard Job containment.

No remote JSON or caller callback can assert an authenticated channel peer.
This controller creates and owns that channel and its command sequence itself.
"""
import asyncio
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import time
from types import MappingProxyType

from discovery import formal_features as F

MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
SOURCE_NAMES = frozenset(("protocol.mjs", "framing.mjs", "intent.mjs", "runtime.mjs",
    "transport.mjs", "maintained_roles.mjs", "role_composition.mjs",
    "services_composition.mjs", "ipc_wire.mjs", "node_entry.mjs"))
FRAME_BYTES, TOTAL_BYTES, FRAME_COUNT = 16384, 129*1024**2, 8194
COMMANDS = frozenset(("locate", "descriptor", "publish", "withdraw", "status", "stop"))


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

    def source_map(self):
        """Fixed ordinary-only local launch binding, separately pinned from readers."""
        return {"schema": "DMKN_V5_ORDINARY_LOCATION_SOURCE_MAP_V1", "root": str(self.source),
                "installation_root": str(self.installation), "workspace_root": str(self.workspace),
                "files": dict(self.source_pins), "manifest_sha256": MANIFEST_SHA}

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


def state_path(workspace, value, mode):
    F.need(mode in ("create", "reopen"), "ORDINARY_LOCATION_OPEN_MODE")
    if mode == "create":
        return fresh_workspace_path(workspace, value)
    workspace = ordinary(workspace, directory=True)
    path = ordinary(value, directory=True)
    F.need(path != workspace and path.is_relative_to(workspace), "ORDINARY_LOCATION_REOPEN_SCOPE")
    return path


class LocationUnavailable(Exception):
    """No private command was admitted; this reason is safe to report as data."""
    def __init__(self, reason):
        F.need(reason in ("BUSY", "EXHAUSTED", "EXPIRED"), "LOCATION_UNAVAILABLE_REASON")
        self.reason = reason
        super().__init__("LOCATION_UNAVAILABLE:" + reason)


class LocationChannelFailure(Exception):
    """Closed/poisoned private channel; no replacement operation on this role."""


class OrdinaryLocationProcess:
    def __init__(self, adoption, configuration, evidence, *, mode, deadline, service_deadline):
        F.need(type(adoption) is AdoptedLocationRuntime, "LOCATION_OWNER_ADOPTION_REQUIRED")
        self.adoption = self._origin_adoption = adoption
        self.config = deepcopy(configuration)
        F.fields(self.config, ("schema", "role", "state", "semantic_id", "egress", "listen",
                              "announce", "bootstrap", "endpoints", "limits"))
        F.need(self.config["schema"] == "DMKN_V5_ORDINARY_EXPORT_OPERATOR_V1"
               and self.config["role"] in ("gateway", "custodian"), "ORDINARY_LOCATION_CONFIG")
        F.hexid(self.config["semantic_id"])
        F.need(type(self.config["endpoints"]) is list and len(self.config["endpoints"])
               == (0 if self.config["role"] == "gateway" else 1), "ORDINARY_LOCATION_OWN_ENDPOINT")
        limits = self.config["limits"]
        self.command_limit = F.uint(limits["commands"], 1, 8192, "LOCATION_COMMANDS")
        self.byte_limit = F.uint(limits["ipc_bytes"], 3*(FRAME_BYTES+4), TOTAL_BYTES, "LOCATION_IPC_BYTES")
        self.frame_limit = self.command_limit + 2
        self.state = state_path(adoption.workspace, self.config["state"], mode)
        self.evidence = fresh_workspace_path(adoption.workspace, evidence)
        F.need(disjoint(self.state, self.evidence), "LOCATION_STATE_EVIDENCE_OVERLAP")
        F.need(type(deadline) in (int, float) and time.monotonic() < deadline <= time.monotonic()+3600,
               "LOCATION_CONTROLLER_ABSOLUTE_DEADLINE")
        F.need(type(service_deadline) in (int, float) and time.monotonic() < service_deadline <= deadline,
               "LOCATION_CONTROLLER_SERVICE_DEADLINE")
        self.mode, self.deadline = mode, deadline
        self.service_deadline = service_deadline
        self.startup_grant = None
        self.process = None; self.sequence = 0; self.lock = asyncio.Lock()
        self.sent = self.received = self.read_frames = 0
        self.stderr = bytearray(); self.stderr_task = None
        self.channel_failed = self.closed = self.forced_termination = False
        self.pre = self.post = None
        self.failure = self.cleanup_error = None
        self._close_task = self._start_task = self._spawn_task = None
        self.cleanup_seconds = 6

    def _remaining(self, until=None):
        remaining = min(self.deadline, self.deadline if until is None else until)-time.monotonic()
        F.need(remaining > 0 and not self.channel_failed, "LOCATION_CONTROLLER_EXPIRED_OR_FAILED")
        return remaining

    async def _stderr(self):
        while True:
            chunk = await self.process.stderr.read(4096)
            if not chunk:
                return
            self.stderr.extend(chunk)
            if len(self.stderr) > 65536:
                self.channel_failed = self.forced_termination = True
                if self.process.returncode is None:
                    self.process.kill()
                return

    async def _read(self, until):
        async def exact(count):
            try:
                raw = await asyncio.wait_for(self.process.stdout.readexactly(count), self._remaining(until))
            except asyncio.IncompleteReadError as error:
                self.received += len(error.partial)
                raise
            self.received += len(raw)
            F.need(self.received <= self.byte_limit, "LOCATION_CONTROLLER_REPLY_CAP")
            return raw
        size = struct.unpack(">I", await exact(4))[0]
        F.uint(size, 1, FRAME_BYTES, "LOCATION_CONTROLLER_FRAME_CAP")
        self.read_frames += 1
        F.need(self.read_frames <= self.frame_limit, "LOCATION_CONTROLLER_FRAME_COUNT")
        return F.strict(await exact(size), FRAME_BYTES)

    async def start(self):
        F.need(self._start_task is None and not self.closed, "LOCATION_CONTROLLER_ALREADY_STARTED")
        self._start_task = asyncio.create_task(self._start_core())
        try:
            return await asyncio.shield(self._start_task)
        except BaseException as error:
            self.channel_failed = True
            self.failure = {"type": type(error).__name__, "message": str(error)[:500]}
            await self._drain_or_terminal()
            raise LocationChannelFailure("LOCATION_START_FAILED_AND_DRAINED") from error

    async def _start_core(self):
        F.need(not self.closed and self.adoption is self._origin_adoption, "LOCATION_OWNER_ADOPTION_CHANGED")
        F.need(state_path(self.adoption.workspace, self.config["state"], self.mode) == self.state
               and fresh_workspace_path(self.adoption.workspace, self.evidence) == self.evidence,
               "LOCATION_OWNER_OUTPUT_SCOPE_CHANGED")
        self.pre = self.adoption.verify(); self._remaining(self.service_deadline)
        config_raw = F.compact(self.config); map_raw = F.compact(self.adoption.source_map())
        F.need(0 < len(config_raw) <= FRAME_BYTES and 0 < len(map_raw) <= FRAME_BYTES, "LOCATION_LAUNCH_BYTES")
        ordinary(self.evidence.parent, directory=True); self.evidence.mkdir()
        for name, raw in (("config.json", config_raw), ("source-map.json", map_raw)):
            with (self.evidence / name).open("xb") as stream:
                stream.write(raw)
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("NODE", "PYTHON", "LEAN", "RUST", "CARGO", "RISC0"))
               and key.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"] = str(self.adoption.node.parent)
        argv = [str(self.adoption.node), str(self.adoption.source / "node_entry.mjs"),
                "--config", str(self.evidence / "config.json"), "--config-sha", hashlib.sha256(config_raw).hexdigest(),
                "--source-map", str(self.evidence / "source-map.json"), "--source-map-sha", hashlib.sha256(map_raw).hexdigest(),
                "--mode", self.mode]
        F.need(not self.closed, "LOCATION_CONTROLLER_CLOSED_DURING_START")
        self._remaining(self.service_deadline)
        self._spawn_task = asyncio.create_task(asyncio.create_subprocess_exec(*argv,
            cwd=self.adoption.workspace, env=env, stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=65536))
        self.process = await asyncio.wait_for(asyncio.shield(self._spawn_task), self._remaining(self.service_deadline))
        F.need(not self.closed, "LOCATION_CONTROLLER_CLOSED_DURING_START")
        self.stderr_task = asyncio.create_task(self._stderr())
        prepared = await self._read(self.service_deadline)
        F.fields(prepared, ("schema", "sequence", "status", "result"))
        F.need(prepared["schema"] == "DMKN_V5_ORDINARY_LOCATION_IPC_REPLY_V1" and prepared["sequence"] == 0
               and prepared["status"] == "PREPARED", "LOCATION_CONTROLLER_PREPARED")
        F.fields(prepared["result"], ("role", "semantic_id", "mode"))
        F.need(prepared["result"] == {"role": self.config["role"], "semantic_id": self.config["semantic_id"],
                                      "mode": self.mode}, "LOCATION_CONTROLLER_PREPARED_BINDING")
        # Node anchors these durations at its marker BEFORE it emitted PREPARED.
        # That earlier anchor makes transit/startup consume, never extend, this
        # original parent's service and private-channel authority.
        now = time.monotonic()
        grant = {"schema": "DMKN_V5_ORDINARY_LOCATION_IPC_BEGIN_V1",
                 "remaining_service_ms": int((self.service_deadline-now)*1000),
                 "remaining_wall_ms": int((self.deadline-now)*1000)}
        F.uint(grant["remaining_service_ms"], 1, 3600000, "LOCATION_STARTUP_SERVICE_GRANT")
        F.uint(grant["remaining_wall_ms"], grant["remaining_service_ms"], 3600000, "LOCATION_STARTUP_CHANNEL_GRANT")
        begin_raw = F.compact(grant)
        F.need(len(begin_raw) <= FRAME_BYTES and len(begin_raw)+4 <= self.byte_limit,
               "LOCATION_STARTUP_FRAME_BYTES")
        self.startup_grant = deepcopy(grant); self.sent += len(begin_raw)+4
        self.process.stdin.write(struct.pack(">I", len(begin_raw))+begin_raw)
        await asyncio.wait_for(self.process.stdin.drain(), self._remaining(self.service_deadline))
        reply = await self._read(self.service_deadline)
        F.fields(reply, ("schema", "sequence", "status", "result"))
        F.need(reply["schema"] == "DMKN_V5_ORDINARY_LOCATION_IPC_REPLY_V1" and reply["sequence"] == 0
               and reply["status"] == "READY", "LOCATION_CONTROLLER_READY")
        F.need(reply["result"]["role"] == self.config["role"]
               and reply["result"]["semantic_id"] == self.config["semantic_id"], "LOCATION_READY_OWNER_ROLE")
        return reply["result"]

    async def command(self, command, payload, *, until=None):
        F.need(command in COMMANDS and type(payload) is dict, "LOCATION_CONTROLLER_COMMAND")
        F.need(until is None or (type(until) in (int, float) and math.isfinite(until)),
               "LOCATION_CONTROLLER_CALL_DEADLINE")
        if self.closed or self.channel_failed:
            raise LocationChannelFailure("LOCATION_CLOSED_OR_POISONED")
        if self.lock.locked():
            raise LocationUnavailable("BUSY")
        operation_horizon = self.deadline if command in ("status", "stop") else self.service_deadline
        cutoff = min(self.deadline, operation_horizon, self.deadline if until is None else until)
        if cutoff <= time.monotonic():
            raise LocationUnavailable("EXPIRED")
        reserve = 0 if command == "stop" else 1 if command == "status" else 2
        sequence = self.sequence + 1
        if sequence + reserve > self.command_limit:
            raise LocationUnavailable("EXHAUSTED")
        message = {"schema": "DMKN_V5_ORDINARY_LOCATION_IPC_COMMAND_V1", "sequence": sequence,
                   "command": command, "payload": payload,
                   "remaining_wall_ms": max(1, int((cutoff-time.monotonic())*1000))}
        raw = F.compact(message)
        F.need(0 < len(raw) <= FRAME_BYTES, "LOCATION_CONTROLLER_COMMAND_BYTES")
        if (self.sent+len(raw)+4+reserve*(FRAME_BYTES+4) > self.byte_limit
                or self.received+(reserve+1)*(FRAME_BYTES+4) > self.byte_limit
                or self.read_frames+reserve+1 > self.frame_limit):
            raise LocationUnavailable("EXHAUSTED")
        # acquire() returns immediately after the fail-fast check above; no
        # other task can enqueue itself while this task constructs the frame.
        await self.lock.acquire()
        failure = None
        try:
            F.need(self.process is not None and self.process.returncode is None,
                   "LOCATION_CONTROLLER_NOT_RUNNING")
            self._remaining(cutoff)
            self.sequence = sequence; self.sent += len(raw)+4
            self.process.stdin.write(struct.pack(">I", len(raw))+raw)
            await asyncio.wait_for(self.process.stdin.drain(), self._remaining(cutoff))
            reply = await self._read(cutoff)
            F.fields(reply, ("schema", "sequence", "status", "result"))
            F.need(reply["schema"] == "DMKN_V5_ORDINARY_LOCATION_IPC_REPLY_V1"
                   and reply["sequence"] == sequence, "LOCATION_CONTROLLER_REPLY_BINDING")
            F.need(reply["status"] == "OK", "LOCATION_CHILD_REFUSAL:"+str(reply["result"])[:500])
            return reply["result"]
        except BaseException as error:
            self.channel_failed = True
            failure = error
            self.failure = {"type": type(error).__name__, "message": str(error)[:500]}
        finally:
            self.lock.release()
        await self._drain_or_terminal()
        raise LocationChannelFailure("LOCATION_ISSUED_COMMAND_FAILED_AND_DRAINED") from failure

    async def _drain_or_terminal(self):
        try:
            return await self._drain_failure()
        except BaseException as error:
            self.cleanup_error = {"type": type(error).__name__, "message": str(error)[:500]}
            raise LocationChannelFailure("LOCATION_POISONED_CLEANUP_UNCERTAIN") from error

    async def _drain_failure(self):
        if self._close_task is None:
            self.closed = True
            self._close_task = asyncio.create_task(self._close_core())
        # Even caller cancellation cannot make this failed channel reusable or
        # return an ordinary unavailability before owned teardown has settled.
        while not self._close_task.done():
            try:
                await asyncio.shield(self._close_task)
            except asyncio.CancelledError:
                continue
        return self._close_task.result()

    async def close(self):
        self.closed = True
        if self._close_task is None:
            self._close_task = asyncio.create_task(self._close_core())
        await asyncio.shield(self._close_task)

    async def _close_core(self):
        self.closed = True
        cleanup_deadline = min(time.monotonic()+self.cleanup_seconds, self.deadline+self.cleanup_seconds)
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
                if self.process.stdin is not None:
                    self.process.stdin.close()
                try:
                    await asyncio.wait_for(self.process.wait(), min(2, max(0.001, cleanup_deadline-time.monotonic())))
                except asyncio.TimeoutError:
                    self.channel_failed = self.forced_termination = True
                    self.process.kill(); await teardown(self.process.wait())
                if self.stderr_task is not None:
                    await teardown(self.stderr_task)
                if self.process.returncode != 0:
                    self.channel_failed = True
            if self._start_task is not None and self._start_task is not asyncio.current_task():
                try:
                    await teardown(asyncio.shield(self._start_task))
                except BaseException:
                    if not self._start_task.done():
                        raise
        finally:
            self.post = self._origin_adoption.verify()
            F.need(self.adoption is self._origin_adoption, "LOCATION_OWNER_ADOPTION_CHANGED")

    def report(self):
        return {"sent_bytes": self.sent, "received_bytes": self.received, "commands": self.sequence,
                "reply_frames": self.read_frames, "command_limit": self.command_limit,
                "ipc_byte_limit_each_direction": self.byte_limit, "ipc_frame_limit_each_direction": self.frame_limit,
                "channel_failed": self.channel_failed, "closed": self.closed, "mode": self.mode,
                "failure": self.failure, "cleanup_error": self.cleanup_error,
                "startup_grant": self.startup_grant,
                "returncode": None if self.process is None else self.process.returncode,
                "stderr_bytes": len(self.stderr), "runtime_pre": self.pre, "runtime_post": self.post,
                "cleanup_allowance_seconds": self.cleanup_seconds, "forced_termination": self.forced_termination,
                "pipe_receive_scope": "CONSUMED_COMPLETE_OR_EOF_PARTIAL_BYTES_NOT_UNREAD_OS_PIPE_ARRIVALS",
                "mathematical_acceptance": False}


