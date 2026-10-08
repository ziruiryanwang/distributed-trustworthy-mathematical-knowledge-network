"""Required-service launch successor; inherited private-pipe lifecycle and tickets.

Only the five additional source pins, selected entry/config map and concrete
channel type differ from the frozen controller. Work/teardown budgets do not.
"""
import asyncio
from copy import deepcopy
import hashlib
import os

from discovery import formal_features as F
from . import controller as B
from .workflow import WorkflowBudget

ROLE_NAMES = frozenset(("maintained_roles.mjs", "role_composition.mjs", "node_entry_roles.mjs",
                        "services_composition.mjs", "node_entry_services.mjs"))


class ServiceLocationProcess(B.LocationProcess):
    def __init__(self, adoption, role_pins, configuration, evidence, *, deadline):
        super().__init__(adoption, configuration, evidence, deadline=deadline)
        F.need(type(role_pins) is dict and set(role_pins) == ROLE_NAMES, "LOCATION_ROLE_SOURCE_MAP")
        self.role_pins = deepcopy(role_pins)
        for value in self.role_pins.values(): F.hexid(value)
        F.need(self.config.get("schema") == "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1"
               and self.config.get("role") in ("reader", "index-provider"), "LOCATION_OWNER_ROLE_REQUIRED")
        self.role_pre = self.role_post = None

    def _verify_roles(self):
        result = {}
        for name, expected in self.role_pins.items():
            row = B.pin(self.adoption.source / name, 2*1024**2)
            F.need(row["sha256"] == expected, "LOCATION_ROLE_SOURCE_PIN:"+name)
            result[name] = row
        return result

    async def _start_core(self):
        # This follows the frozen startup core with only extra source adoption
        # and the explicitly selected role-aware entry filename changed.
        F.need(not self.closed, "LOCATION_CONTROLLER_CLOSED_DURING_START")
        self.role_pre = self._verify_roles()
        self.pre = self.adoption.verify(); self._remaining()
        B.ordinary(self.evidence.parent, directory=True); self.evidence.mkdir()
        config_raw = F.compact(self.config)
        F.need(len(config_raw) <= B.FRAME_BYTES, "LOCATION_CONTROLLER_CONFIG_SIZE")
        mapping = {"schema": "DMKN_V5_LOCAL_NODE_SOURCE_MAP_V1", "root": str(self.adoption.source),
                   "files": {**self.adoption.source_pins, **self.role_pins}, "manifest_sha256": B.MANIFEST_SHA}
        map_raw = F.compact(mapping)
        for name, raw in (("config.json", config_raw), ("source-map.json", map_raw)):
            with (self.evidence / name).open("xb") as stream: stream.write(raw)
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("NODE", "PYTHON", "LEAN", "RUST", "CARGO", "RISC0"))
               and key.upper() not in ("PATH", "VIRTUAL_ENV")}
        env["PATH"] = str(self.adoption.node.parent)
        argv = [str(self.adoption.node), str(self.adoption.source / "node_entry_services.mjs"),
                "--config", str(self.evidence / "config.json"), "--config-sha", hashlib.sha256(config_raw).hexdigest(),
                "--source-map", str(self.evidence / "source-map.json"), "--source-map-sha", hashlib.sha256(map_raw).hexdigest()]
        F.need(not self.closed, "LOCATION_CONTROLLER_CLOSED_DURING_START")
        self._spawn_task = asyncio.create_task(asyncio.create_subprocess_exec(*argv, cwd=B.ROOT, env=env,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=65536))
        self.process = await asyncio.wait_for(asyncio.shield(self._spawn_task), self._remaining())
        F.need(not self.closed, "LOCATION_CONTROLLER_CLOSED_DURING_START")
        self.stderr_task = asyncio.create_task(self._stderr())
        reply = await self._read(self.deadline)
        F.fields(reply, ("schema", "sequence", "status", "result"))
        F.need(reply["schema"] == "DMKN_V5_LOCATION_IPC_REPLY_V1" and reply["sequence"] == 0
               and reply["status"] == "READY", "LOCATION_CONTROLLER_READY")
        F.need(reply["result"]["role"] == self.config["role"], "LOCATION_READY_OWNER_ROLE")
        return reply["result"]

    async def _close_core(self):
        try: return await super()._close_core()
        finally: self.role_post = self._verify_roles()

    def report(self):
        return {**super().report(), "role": self.config["role"], "role_pre": self.role_pre, "role_post": self.role_post}


class ServiceLocatedWorkflow(B.LocatedWorkflow):
    def __init__(self, channel, namespace, features, limits, search_limits, policy):
        F.need(type(channel) is ServiceLocationProcess and channel.config["role"] == "reader", "LOCATION_PRIVATE_READER_CHILD_REQUIRED")
        self.channel = channel
        self._workflow = WorkflowBudget(namespace, features, limits, search_limits, policy)
        self.deadline = min(channel.deadline, self._workflow._deadline)
        self._workflow._deadline = self.deadline
