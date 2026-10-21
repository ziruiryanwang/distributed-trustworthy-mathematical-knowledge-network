"""Three extracted-method shutdown controls with explicitly synthetic framed I/O.

No product object construction, full SDK imports, real process, socket or store.
Only root's selected snapshot execution may create the single result JSON.
"""
import argparse
import ast
import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import struct
import sys
import time
from types import ModuleType, SimpleNamespace
import unittest

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUTPUT = PROJECT / "experiments/v5-local-checks/managed-close-drain-controls-01"
RELATIVE = Path("software/v5/managed_close_drain/close_controls.py")
PINS = {
    "software/v5/managed_close_drain/client/serve_placement.py":
        (24566, "c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8"),
    "software/v5/portable_runtime/location/controller.py":
        (15884, "4dc0824d758e72fce591dbd9dddb9e487bcd0506cfaf4a71e894b0166b84e064"),
    "software/v5/retained_advertisement/placement/advertisement.py":
        (23256, "5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510"),
    "software/v5/instantiation_discovery/discovery/formal_features.py":
        (10826, "8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c"),
}
EXTRACTED = {
    "PlacementService": ("_monitor", "close", "_close"),
    "LocationProcess": ("_remaining", "_read", "command", "report"),
    "PlacementAdvertisement": ("health",),
}
FLAGS = ("intake_closed", "retained_closed", "location_closed", "read_closed",
         "journal_closed", "controller_closed", "workspace_closed")
F = None
OBSERVED = {}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction() for item in (path, *path.parents)),
        "CONTROL_ORDINARY_PATH")
    return path


def pin(path, size, digest):
    ordinary(path)
    need(path.is_file() and path.stat().st_size == size, "CONTROL_SOURCE_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(size + 1)
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "CONTROL_SOURCE_PIN")
    return raw


def adopt(sources):
    global F
    raws = {name: pin(sources / name, *row) for name, row in PINS.items()}
    feature = next(name for name in PINS if name.endswith("formal_features.py"))
    F = ModuleType("_close_controls_actual_formal_features")
    F.__file__ = str(sources / feature)
    exec(compile(raws[feature], F.__file__, "exec", dont_inherit=True), F.__dict__)
    specs = (("PlacementService", ServiceFixture, "software/v5/managed_close_drain/client/serve_placement.py"),
             ("LocationProcess", ChannelFixture, "software/v5/portable_runtime/location/controller.py"),
             ("PlacementAdvertisement", AdvertisementFixture,
              "software/v5/retained_advertisement/placement/advertisement.py"))
    for class_name, fixture, source in specs:
        tree = ast.parse(raws[source], filename=str(sources / source))
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name]
        need(len(classes) == 1, "CONTROL_EXACT_CLASS")
        methods = [node for node in classes[0].body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and node.name in EXTRACTED[class_name]]
        need(tuple(node.name for node in methods) == EXTRACTED[class_name], "CONTROL_EXACT_METHODS")
        constants = []
        if class_name == "LocationProcess":
            constants = [node for node in tree.body if isinstance(node, ast.Assign)
                         and len(node.targets) == 1 and isinstance(node.targets[0], ast.Tuple)
                         and tuple(item.id for item in node.targets[0].elts if isinstance(item, ast.Name))
                         == ("FRAME_BYTES", "TOTAL_BYTES", "FRAME_COUNT")]
            need(len(constants) == 1, "CONTROL_EXACT_FRAME_CONSTANTS")
        namespace = dict(F=F, asyncio=asyncio, time=time, struct=struct, deepcopy=deepcopy)
        exec(compile(ast.Module(body=constants + methods, type_ignores=[]), str(sources / source),
                     "exec", dont_inherit=True), namespace)
        for method in EXTRACTED[class_name]:
            setattr(fixture, method, namespace[method])


class SyntheticPipe:
    def __init__(self, process, *, resistant):
        self.process, self.resistant = process, resistant
        self.buffer = bytearray()
        self.ready = asyncio.Event()
        self.pending = None
        self.command = None
        self.cancellations = 0

    def feed(self, message, command):
        need(not self.buffer, "SYNTHETIC_REPLY_ALREADY_PENDING")
        raw = F.compact(message)
        self.buffer.extend(struct.pack(">I", len(raw)) + raw)
        self.command = command
        self.ready.set()

    async def readexactly(self, count):
        while not self.ready.is_set():
            try:
                await self.ready.wait()
            except asyncio.CancelledError:
                self.cancellations += 1
                if not self.resistant:
                    raise
                # Deliberate hostile I/O double, not Python pipe behavior evidence.
        need(len(self.buffer) >= count, "SYNTHETIC_EXACT_READ")
        raw = bytes(self.buffer[:count])
        del self.buffer[:count]
        if not self.buffer:
            self.ready.clear()
            self.process.events.append("reply:" + self.command)
            if self.command == "stop":
                self.process.returncode = 0
        return raw

    def release(self, *, ok=True):
        if self.pending is not None:
            sequence = self.pending
            self.pending = None
            self.feed(self.process.reply(sequence, "status", ok=ok), "status")


class SyntheticInput:
    def __init__(self, process):
        self.process = process

    def write(self, raw):
        size = struct.unpack(">I", raw[:4])[0]
        need(size == len(raw) - 4, "SYNTHETIC_COMMAND_FRAME")
        value = F.strict(raw[4:], 16384)
        process = self.process
        command, sequence = value["command"], value["sequence"]
        process.events.append("write:" + command)
        process.commands.append(command)
        if command == "status" and process.commands.count("status") == 2:
            process.stdout.pending = sequence
            process.status_written.set()
        else:
            process.stdout.feed(process.reply(sequence, command), command)

    async def drain(self):
        return None


class SyntheticProcess:
    def __init__(self, events, *, resistant):
        self.events, self.commands = events, []
        self.returncode = None
        self.kills = 0
        self.status_written = asyncio.Event()
        self.stdout = SyntheticPipe(self, resistant=resistant)
        self.stdin = SyntheticInput(self)

    def reply(self, sequence, command, *, ok=True):
        return dict(schema="DMKN_V5_LOCATION_IPC_REPLY_V1", sequence=sequence,
            status="OK" if ok else "ERROR",
            result=dict(status="STOPPED" if command == "stop" else "RUNNING",
                        namespace="synthetic-namespace", role="index-provider",
                        global_complete=False, mathematical_acceptance=False))

    def kill(self):
        self.kills += 1
        self.events.append("synthetic-kill")
        self.returncode = -15


class ChannelFixture:
    """Not LocationProcess: actual command/read/report methods, fake transport/close."""
    def __init__(self, events, *, resistant):
        self.events = events
        self.process = SyntheticProcess(events, resistant=resistant)
        self.config = dict(limits=dict(operation_ms=400))
        self.deadline = time.monotonic() + 20
        self.lock = asyncio.Lock()
        self.sequence = self.sent = self.received = self.read_frames = 0
        self.stderr = bytearray()
        self.closed = self.channel_failed = self.forced_termination = False
        self.pre = self.post = None
        self.cleanup_seconds = 6

    async def close(self):
        self.events.append("synthetic-location-close")
        need(not self.lock.locked(), "SYNTHETIC_INFLIGHT_CHANNEL_NOT_CLOSED")
        self.closed = True


class StoreFixture:
    def __init__(self, name, events):
        self.name, self.events = name, events
        self.closed = self._busy = False

    def close(self):
        self.events.append("store-close:" + self.name)
        self.closed = True


class AdvertisementFixture(StoreFixture):
    """Actual health method; only local fixture guards, no ledger/adoption checks."""
    def __init__(self, channel, events):
        super().__init__("advertisement", events)
        self.location = channel
        self.health_checks = 0
        self.health_cap = 58
        self._config = dict(namespace="synthetic-namespace")

    def _active(self, until, *, network):
        need(not self.closed and time.monotonic() < until, "SYNTHETIC_HEALTH_ACTIVE")
        need(network and not self.location.closed and not self.location.channel_failed
             and self.location.process.returncode is None, "SYNTHETIC_CHANNEL_LIVE")

    def report(self):
        return dict(synthetic=True, health_checks=self.health_checks, closed=self.closed)


class ReadFixture:
    def __init__(self, events):
        self.events, self.server, self.tasks = events, object(), []

    async def stop(self):
        self.events.append("synthetic-read-stop")
        self.server = None

    def status(self):
        return dict(synthetic=True, closed=self.server is None)


class ServiceFixture:
    """Not PlacementService: extracted orchestration over explicit component doubles."""
    def __init__(self, *, resistant=False):
        self.events = []
        self.location = ChannelFixture(self.events, resistant=resistant)
        self.advertisement = AdvertisementFixture(self.location, self.events)
        self.controller = StoreFixture("controller", self.events)
        self.workspace = StoreFixture("workspace", self.events)
        self.read_provider, self.intake_provider = ReadFixture(self.events), None
        self.grant = SimpleNamespace(closed=False)
        self.limits = dict(health_interval_ms=100)
        self._deadline, self._stop_deadline, self._outer = (time.monotonic() + value for value in (10, 20, 30))
        self._drain_seconds = 5.1
        self._closing = self.closed = False
        self._wake = asyncio.Event()
        self._monitor_task = self._start_task = self._close_task = self._retained_task = None
        self._failure = self._final = None
        self.bindings = dict(synthetic=True)
        self._cleanup = {**{name: False for name in FLAGS}, "errors": []}


class Controls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = None
        self.calls = []
        self.loop_errors = []
        self.loop = asyncio.get_running_loop()
        self.previous_handler = self.loop.get_exception_handler()
        self.loop.set_exception_handler(lambda unused, context: self.loop_errors.append("UNHANDLED_ASYNC"))

    async def asyncTearDown(self):
        try:
            if self.service is not None:
                service = self.service
                service.location.process.stdout.release()
                tasks = {task for task in (service._monitor_task, service._close_task, *self.calls)
                         if task is not None}
                if tasks:
                    done, pending = await asyncio.wait(tasks, timeout=3)
                    self.assertFalse(pending, "SYNTHETIC_TASK_NOT_DRAINED")
                    for task in done:
                        if not task.cancelled():
                            task.exception()
                self.assertFalse(service.location.lock.locked())
                OBSERVED.setdefault(self._testMethodName, {}).update(
                    events=list(service.events), commands=list(service.location.process.commands),
                    synthetic_read_cancellations=service.location.process.stdout.cancellations,
                    synthetic_kills=service.location.process.kills, all_tracked_tasks_drained=True)
            self.assertEqual(self.loop_errors, [])
        finally:
            self.loop.set_exception_handler(self.previous_handler)

    async def held_status(self, *, resistant=False):
        service = self.service = ServiceFixture(resistant=resistant)
        # Initial health succeeds; only the monitor's next real status is held.
        await service.advertisement.health(until=time.monotonic() + 0.4)
        service._monitor_task = asyncio.create_task(service._monitor())
        await asyncio.wait_for(service.location.process.status_written.wait(), 2)
        self.assertTrue(service.location.lock.locked())
        self.assertEqual(service.location.process.commands, ["status", "status"])
        self.assertFalse(service._monitor_task.done())
        return service

    async def start_close(self, service):
        call = asyncio.create_task(service.close())
        self.calls.append(call)
        await asyncio.wait_for(service._wake.wait(), 1)
        return call

    async def test_01_close_joins_written_healthy_status_before_stop(self):
        service = await self.held_status()
        call = await self.start_close(service)
        await asyncio.sleep(0)
        self.assertFalse(call.done())
        self.assertNotIn("stop", service.location.process.commands)
        service.location.process.stdout.release()
        result = await asyncio.wait_for(asyncio.shield(call), 4)
        self.assertEqual(result["status"], "CLOSED")
        self.assertEqual(result["cleanup"]["errors"], [])
        self.assertTrue(all(result["cleanup"][name] for name in FLAGS))
        self.assertEqual(service.location.process.commands, ["status", "status", "stop"])
        self.assertLess(service.events.index("reply:status", 2), service.events.index("write:stop"))
        self.assertFalse(service.location.channel_failed)
        self.assertFalse(service.location.forced_termination)
        self.assertEqual(service.location.process.kills, 0)
        self.assertEqual(service.location.process.stdout.cancellations, 0)
        self.assertTrue(service._monitor_task.done())
        self.assertTrue(service.grant.closed)
        self.assertIs(result["mathematical_acceptance"], False)
        OBSERVED[self._testMethodName] = dict(status=result["status"], reply_before_stop=True)

    async def test_02_failed_reply_remains_failed_and_poisoned(self):
        service = await self.held_status()
        call = await self.start_close(service)
        service.location.process.stdout.release(ok=False)
        result = await asyncio.wait_for(asyncio.shield(call), 4)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_code"], "PLACEMENT_SERVICE_HEALTH_FAILED")
        self.assertTrue(service.location.channel_failed)
        self.assertTrue(service.location.forced_termination)
        self.assertEqual(service.location.process.kills, 1)
        self.assertFalse(result["cleanup"]["location_closed"])
        self.assertIn("location_close", [row["component"] for row in result["cleanup"]["errors"]])
        self.assertNotIn("stop", service.location.process.commands)
        self.assertTrue(service._monitor_task.done())
        OBSERVED[self._testMethodName] = dict(status=result["status"], strict_failure_preserved=True)

    async def test_03_resistant_timeout_blocks_stores_and_returns_bounded(self):
        service = await self.held_status(resistant=True)
        began = time.monotonic()
        call = await self.start_close(service)
        result = await asyncio.wait_for(asyncio.shield(call), 4)
        elapsed = time.monotonic() - began
        self.assertLess(elapsed, 4)
        self.assertEqual(result["status"], "FAILED")
        self.assertFalse(service._monitor_task.done())
        self.assertGreater(service.location.process.stdout.cancellations, 0)
        components = [row["component"] for row in result["cleanup"]["errors"]]
        self.assertIn("_monitor_task", components)
        self.assertIn("live_actor_prevents_store_close", components)
        for name in ("journal_closed", "controller_closed", "workspace_closed"):
            self.assertFalse(result["cleanup"][name])
        self.assertFalse(any(event.startswith("store-close:") for event in service.events))
        self.assertTrue(service.grant.closed)
        OBSERVED[self._testMethodName] = dict(status=result["status"], close_wall_seconds=elapsed,
            monitor_pending_at_return=True, stores_unclosed_at_return=True)
        # Release only after all failed/bounded/live-actor assertions; teardown
        # retrieves the task result, never upgrades the saved FAILED observation.
        service.location.process.stdout.release()


SELECTED = ("test_01_close_joins_written_healthy_status_before_stop",
            "test_02_failed_reply_remains_failed_and_poisoned",
            "test_03_resistant_timeout_blocks_stores_and_returns_bounded")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = ordinary(Path(args.output))
    need(output == OUTPUT and output.is_dir(), "CONTROL_SELECTED_OUTPUT")
    sources = output / "sources"
    need(Path(__file__).resolve() == sources / RELATIVE, "CONTROL_SNAPSHOT_EXECUTION_REQUIRED")
    target = output / "close-drain-controls-result.json"
    need(not target.exists(), "CONTROL_FRESH_RESULT_REQUIRED")
    adopt(sources)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(
        unittest.TestSuite(Controls(name) for name in SELECTED))
    for name, row in PINS.items():
        pin(sources / name, *row)
    report = dict(schema="DMKN_V5_MANAGED_CLOSE_DRAIN_CONTROLS_V1",
        status="PASS" if result.wasSuccessful() else "FAIL", tests_run=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(SELECTED), source_pins={name: row[1] for name, row in PINS.items()},
        extracted=EXTRACTED, observed=OBSERVED, extraction_only=True,
        synthetic_io=True, actual_service_constructed=False, actual_node_or_network=False,
        mathematical_acceptance=False, installed_closure_qualification=False)
    raw = F.compact(report)
    need(len(raw) <= 16384, "CONTROL_RESULT_BOUND")
    with target.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_RESULT_WRITE")
    print(raw.decode("utf-8"))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
