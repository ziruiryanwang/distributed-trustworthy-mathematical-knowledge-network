"""Changed lifecycle/IPC controls and one exact Python/Node vector interchange.

Lifecycle child creation and runtime verification are mocked for race controls.
Only the final vector child is real; it imports source/builtins, not libp2p and
opens no sockets. Root owns the outer hard Job and exact source/runtime pins.
"""
from pathlib import Path
import argparse
import asyncio
import base64
import hashlib
import ipaddress
import json
import os
import struct
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from location import protocol as P
from location.controller import AdoptedLocationRuntime, LocationProcess, LocatedWorkflow, SOURCE_NAMES, ROOT, BASE


def encode(value):
    raw = F.compact(value); return struct.pack(">I", len(raw))+raw


class FakeProcess:
    def __init__(self, frames=()):
        self.returncode = None; self.kills = 0; self.exited = asyncio.Event()
        self.stdout, self.stderr = asyncio.StreamReader(), asyncio.StreamReader()
        self.stderr.feed_eof()
        for frame in frames: self.stdout.feed_data(encode(frame))
        owner = self
        class Input:
            def write(self, data): pass
            async def drain(self): pass
            def close(self): owner.finish(0)
        self.stdin = Input()

    def finish(self, code):
        if self.returncode is None:
            self.returncode = code; self.stdout.feed_eof(); self.exited.set()

    def kill(self): self.kills += 1; self.finish(-9)
    async def wait(self): await self.exited.wait(); return self.returncode


async def run(args):
    out = Path(args.output)
    F.need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
           "CONTROLLER_TEST_INVOCATION")
    F.need(out.is_absolute() and out.resolve() == out and out.is_relative_to(ROOT / "experiments/v5-local-checks")
           and not out.exists(), "CONTROLLER_TEST_FRESH_OUTPUT")
    out.mkdir()
    source = Path(__file__).resolve().parent
    pins = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in SOURCE_NAMES}
    adoption = AdoptedLocationRuntime(source, pins)
    # Explicitly narrow race controls: do not rehash the full runtime per mock.
    adoption.verify = lambda: {"mocked_for_lifecycle_control": True}
    tests = []
    def channel(name): return LocationProcess(adoption, {}, out / name, deadline=time.monotonic()+5)
    ready = {"schema": "DMKN_V5_LOCATION_IPC_REPLY_V1", "sequence": 0, "status": "READY", "result": {}}
    async def expect_error(awaitable, kind):
        try: await awaitable
        except kind: return
        raise AssertionError("Expected "+str(kind))

    for cancel in (False, True):
        value = channel("cancel-start" if cancel else "close-start")
        child = FakeProcess(); entered = asyncio.Event(); release = asyncio.Event()
        async def spawn(*unused, **kwargs): entered.set(); await release.wait(); return child
        with patch("asyncio.create_subprocess_exec", spawn):
            starting = asyncio.create_task(value.start()); await entered.wait()
            if cancel:
                starting.cancel(); await asyncio.sleep(0)
                closing = asyncio.create_task(value.close())
            else: closing = asyncio.create_task(value.close())
            again = asyncio.create_task(value.close()); await asyncio.sleep(0)
            assert not closing.done()
            release.set()
            await asyncio.gather(closing, again)
            await expect_error(starting, asyncio.CancelledError if cancel else ValueError)
        assert child.returncode is not None and value._close_task.done()
        assert value.report()["forced_termination"] and value.post["mocked_for_lifecycle_control"]
        tests.append("cancel-start-during-spawn" if cancel else "close-and-double-close-during-spawn")

    value = channel("close-before-core"); calls = []
    core_entered, release_core = asyncio.Event(), asyncio.Event()
    original_core = value._start_core
    async def held_core():
        core_entered.set(); await release_core.wait(); return await original_core()
    value._start_core = held_core
    async def forbidden_spawn(*unused, **kwargs): calls.append(1); return FakeProcess()
    with patch("asyncio.create_subprocess_exec", forbidden_spawn):
        starting = asyncio.create_task(value.start()); await core_entered.wait()
        closing = asyncio.create_task(value.close())
        for _ in range(4):
            if value.closed: break
            await asyncio.sleep(0)
        assert value.closed and not closing.done()
        release_core.set()
        await closing; await expect_error(starting, ValueError)
    assert calls == [] and value.process is None
    tests.append("close-before-start-core-does-not-spawn")

    value = channel("lock-expired"); value.process = FakeProcess(); await value.lock.acquire()
    value.deadline = time.monotonic()+0.01
    try: await value.command("status", {})
    except asyncio.TimeoutError: pass
    except ValueError as error: assert str(error) == "LOCATION_CONTROLLER_EXPIRED_OR_FAILED"
    else: raise AssertionError("Held lock must not outlive original work deadline")
    value.lock.release(); await value.close()
    assert value.sequence == 0 and value.process.returncode == 0
    tests.append("original-deadline-bounds-lock-acquisition")

    for malformed_ready in (True, False):
        value = channel("bad-ready" if malformed_ready else "bad-reply")
        wrong = {"schema": "DMKN_V5_LOCATION_IPC_REPLY_V1", "sequence": 999, "status": "OK", "result": {}}
        child = FakeProcess([wrong] if malformed_ready else [ready, wrong])
        async def spawn(*unused, **kwargs): return child
        with patch("asyncio.create_subprocess_exec", spawn):
            if malformed_ready: await expect_error(value.start(), ValueError)
            else:
                await value.start(); await expect_error(value.command("status", {}), ValueError); await value.close()
        assert value.channel_failed and child.returncode is not None
        tests.append("malformed-ready-reaped" if malformed_ready else "malformed-sequence-reply-reaped")

    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    raw_peer = b"\0\x24\x08\x01\x12\x20"+bytes(range(32))
    integer = int.from_bytes(raw_peer, "big"); encoded = ""
    while integer: integer, digit = divmod(integer, 58); encoded = alphabet[digit]+encoded
    peer = P.peer_id("1"+encoded)
    ns, features = "a"*64, ["1"*64, "2"*64]
    endpoint = {"host": "127.0.0.1", "port": 8765, "tls": False, "server_name": None}
    policy_config = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
                     "test_endpoints": [{"host": "127.0.0.1", "port": 8765}]}
    policy = P.OwnerEgressPolicy(policy_config)
    limits = dict(wall_ms=5000, route_operations=2, routing_events=16, routing_peer_slots=2,
                  descriptor_requests=1, contacts=1, reply_bytes=16384)
    search_limits = dict(providers=1, snapshots=1, requests=2, pages=1, examined=32, candidates=8,
                         bytes=8192, wall_ms=3000, inflight=1)
    value = channel("ticket-settlement")
    workflow = LocatedWorkflow(value, ns, features, limits, search_limits, policy)
    async def bad_route(*unused, **kwargs): return {"ticket": 1, "route_key": "0"*64, "peers": [peer]}
    value.command = bad_route
    await expect_error(workflow.route(features, event_cap=8, peer_cap=1), ValueError)
    report = workflow.report()["workflow"]
    assert report["pending_requests"] == 0 and report["used"]["routing_events"] == 8
    async def good_route(unused, ticket, **kwargs): return {"ticket": ticket["ticket"], "route_key": ticket["route_key"], "peers": [peer]}
    value.command = good_route
    located = await workflow.route(features, event_cap=8, peer_cap=1)
    async def bad_descriptor(unused, ticket, **kwargs):
        assert "until" not in ticket and kwargs["until"] <= workflow.deadline
        return {"ticket": ticket["ticket"], "authenticated_peer": peer, "raw_base64": base64.b64encode(b"bad").decode()}
    value.command = bad_descriptor
    await expect_error(workflow.descriptor(peer, located["route_key"]), (ValueError, json.JSONDecodeError))
    report = workflow.report()["workflow"]
    assert report["pending_requests"] == 0 and report["used"]["descriptor_reply_bytes"] == 3
    tests.append("private-ticket-failure-settles-once-without-refund")

    routes = []
    for namespace, selected, stripe in ((ns, features, 0), (ns, features, 255), ("c"*64, features[:1], 3)):
        request = P.descriptor_request(namespace, selected, stripe, "b"*64, 4096)
        routes.append({"namespace": namespace, "features": selected, "stripe": stripe, "nonce": "b"*64,
                       "max_bytes": 4096, "key": request["route_key"], "request_base64": base64.b64encode(F.compact(request)).decode()})
    addresses = []
    for address in ("0.255.255.255", "1.0.0.0", "100.63.255.255", "100.64.0.0", "100.127.255.255", "100.128.0.0",
                    "192.0.0.8", "192.0.0.9", "192.0.0.10", "192.0.0.11", "223.255.255.255", "224.0.0.0"):
        ip = ipaddress.IPv4Address(address)
        addresses.append({"address": address, "public": ip.is_global and not any((ip.is_multicast, ip.is_reserved, ip.is_link_local, ip.is_loopback, ip.is_unspecified))})
    config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_V1", "state": str(out / "not-created-node-state"), "namespace": ns,
        "egress": policy_config, "listen": ["/ip4/127.0.0.1/tcp/8765"], "announce": [], "bootstrap": [], "endpoints": [endpoint],
        "limits": {"service_ms": 10000, "operation_ms": 1000, "query_events": 8, "provider_limit": 2,
            "advertised_keys": 2, "provider_ttl_ms": 3000, "reprovide_interval_ms": 500, "maintenance_ms": 1000,
            "commands": 8, "descriptor_requests": 4, "descriptor_reply_bytes": 16384, "metadata": {},
            "transport": {"outbound_attempts": 4, "inbound_upgrades": 4, "receive_bytes": 65536, "send_bytes": 65536}}}
    fixture = F.compact(dict(routes=routes, addresses=addresses, policy=policy_config, endpoint=endpoint, peer=peer, config=config))
    path = out / "vectors.json"
    with path.open("xb") as stream: stream.write(fixture)
    node = Path(args.node); assert node == BASE / "runtime/node/node.exe"
    env = {key: val for key, val in os.environ.items() if not key.upper().startswith("NODE")}
    child = await asyncio.create_subprocess_exec(str(node), str(source / "controller_controls.mjs"), str(path),
        hashlib.sha256(fixture).hexdigest(), cwd=ROOT, env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=65536)
    try: stdout, stderr = await asyncio.wait_for(child.communicate(), 15)
    except BaseException: child.kill(); await child.wait(); raise
    assert child.returncode == 0, stderr.decode(errors="replace")
    assert len(stdout) <= 16384 and len(stderr) <= 16384
    vectors = json.loads(stdout)
    assert vectors["status"] == "PASS" and vectors["route_vectors"] == [row["key"] for row in routes]
    descriptor = base64.b64decode(vectors["descriptor_base64"], validate=True)
    request = P.descriptor_request(ns, features, 0, "b"*64, 4096)
    checked = P.verify_descriptor(descriptor, request, peer, policy)
    assert len(checked) == 1 and checked[0] == policy.endpoint(endpoint)
    report = {"status": "PASS", "python_controls": tests, "node_controls": vectors, "actual_vector_child_processes": 1,
              "lifecycle_processes_mocked": True, "runtime_tree_checks_mocked_in_lifecycle_tests": True,
              "actual_sockets": 0, "mathematical_acceptance": False}
    with (out / "RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--node", required=True); parser.add_argument("--output", required=True)
    asyncio.run(run(parser.parse_args()))
