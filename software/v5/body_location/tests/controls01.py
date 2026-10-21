"""Selected exact-custody boundaries; source authored, execution root-selected.

Real structural reader/store/codec/accounting; explicitly INERT mathematical
issuers and location/HTTP edges. No old suite, proof, native worker or socket.
The selected SDK is copied to one logical tree before import, so exact source
guards do not accidentally traverse scattered predecessor implementations.
"""
import asyncio
import base64
from copy import copy, deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[2]
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-projection-01-input.json"
MAP_SHA = "ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f"
FOUNDATION_PATH = PROJECT/"experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json"
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
NODE = PROJECT/"product-local/v4-library-commons-02/commons-v4/runtime/node/node.exe"
NODE_SHA = "b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3"
MIB, CAP = 1024**2, 65536
OUTPUT = None
RESULTS, SOURCE_COPIES = {}, {}
NEW = (
    "portable/location/protocol.py", "portable/location/protocol.mjs",
    "portable/location/intent.mjs", "portable/location/maintained_roles.mjs",
    "portable/location/ipc_wire.mjs", "portable/location/node_entry_services.mjs",
    "portable/location/controller_services.py", "v5/client/body_custody.py",
    "v5/client/workspace_evidence.py", "v5/client/semantic_reader.py",
    "v5/client/serve_advertised.py", "v5/transport/acquisition_resilience.py",
    "distribution.py",
)
FIXTURES = ("client/test_direct_contacts.py", "client/test_workspace_evidence.py",
            "client/test_workspace_mixed.py")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stage_sources(output):
    raw = MAP_PATH.read_bytes()
    if sha(raw) != MAP_SHA:
        raise ValueError("BASIS_MAP_CHANGED")
    selected = json.loads(raw)["sdk_sources"]
    if len(selected) != 113:
        raise ValueError("BASIS_MAP_CENSUS")
    sources = {}
    for logical, row in selected.items():
        relative = Path(row["path"]).relative_to(PROJECT/"software/v5")
        sources[logical] = (SOURCE/relative, row)
    for logical in NEW:
        relative = logical[3:] if logical.startswith("v5/") else logical
        sources[logical] = (SOURCE/"body_location"/relative, None)
    for relative in FIXTURES:
        sources["v5/"+relative] = (SOURCE/relative, None)
    code = output/"selected-code"
    code.mkdir()
    for logical, (path, expected) in sorted(sources.items()):
        raw = path.read_bytes()
        if not 0 < len(raw) <= 2*MIB:
            raise ValueError("SOURCE_BOUND:"+logical)
        if expected is not None and (len(raw) != expected["bytes"] or sha(raw) != expected["sha256"]):
            raise ValueError("BASIS_SOURCE_CHANGED:"+logical)
        target = code/logical
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
        if target.read_bytes() != raw:
            raise ValueError("SOURCE_COPY_CHANGED:"+logical)
        SOURCE_COPIES[logical] = {"source": str(path), "bytes": len(raw), "sha256": sha(raw)}
    sys.path[:0] = [str(code/"portable"), str(code/"v5")]
    # No selected implementation may have been imported before exact staging.
    for name in ("client", "location", "modules", "transport", "discovery"):
        if name in sys.modules:
            raise ValueError("EARLY_PRODUCT_IMPORT:"+name)
    return code


def imports():
    global C, F, B, P, BC, AR, DR, HTTP, L, SR, WE, WS, WV, ADVERT, D, E, ET, TC, DT
    global AcquisitionBudget, AdoptedLocationRuntime, ServiceLocationProcess, SOURCE_NAMES, ROLE_NAMES, DIST
    C = importlib.import_module("modules.codec")
    F = importlib.import_module("discovery.formal_features")
    B = importlib.import_module("aggregate_claims.bindings")
    P = importlib.import_module("location.protocol")
    BC = importlib.import_module("client.body_custody")
    AR = importlib.import_module("transport.acquisition_resilience")
    DR = importlib.import_module("transport.declaration_resilience")
    HTTP = importlib.import_module("transport.http_provider")
    L = importlib.import_module("client.located_queries")
    SR = importlib.import_module("client.semantic_reader")
    WE = importlib.import_module("client.workspace_evidence")
    WS = importlib.import_module("client.workspace_staged")
    WV = importlib.import_module("client.workspace_validated")
    ADVERT = importlib.import_module("client.serve_advertised")
    D = importlib.import_module("client.test_direct_contacts")
    E = importlib.import_module("client.test_workspace_evidence")
    ET = importlib.import_module("evidence_network.transport")
    TC = importlib.import_module("transport.clients")
    DT = importlib.import_module("delta.transport")
    AcquisitionBudget = importlib.import_module("transport.receipt_client").AcquisitionBudget
    ctl = importlib.import_module("location.controller")
    svc = importlib.import_module("location.controller_services")
    AdoptedLocationRuntime, SOURCE_NAMES = ctl.AdoptedLocationRuntime, ctl.SOURCE_NAMES
    ServiceLocationProcess, ROLE_NAMES = svc.ServiceLocationProcess, svc.ROLE_NAMES
    spec = importlib.util.spec_from_file_location("exact_custody_distribution", CODE/"distribution.py")
    DIST = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(DIST)


def peer(seed):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int.from_bytes(b"\0\x24\x08\x01\x12\x20"+bytes([seed])*32, "big")
    result = ""
    while value:
        value, index = divmod(value, 58)
        result = alphabet[index]+result
    return P.peer_id("1"+result)


def query_limits():
    return dict(providers=1, snapshots=1, requests=2, pages=1, examined=8,
                candidates=4, bytes=131072, wall_ms=30000, inflight=1)


def location_limits():
    return dict(wall_ms=30000, route_operations=1, routing_events=8,
                routing_peer_slots=1, descriptor_requests=1, contacts=1,
                reply_bytes=query_limits()["bytes"]+4096)


def body_limits():
    return dict(schema="DMKN_V5_BODY_LOCATION_ALLOWANCE_V1", route_operations=4,
                routing_events=32, routing_peer_slots=8, descriptor_requests=8, capabilities=8)


class Writer:
    def __init__(self, cleanup_error=None):
        self.cleanup_error = cleanup_error
        self.closed = self.waits = 0
        self.sent = bytearray()

    def write(self, raw): self.sent.extend(raw)
    async def drain(self): pass
    def close(self): self.closed += 1
    async def wait_closed(self):
        self.waits += 1
        if self.cleanup_error is not None: raise self.cleanup_error


def stream(raw, status=200, cleanup_error=None):
    reader, writer = asyncio.StreamReader(), Writer(cleanup_error)
    reader.feed_data(HTTP._header("HTTP/1.1 "+str(status)+" TEST", len(raw))+raw)
    reader.feed_eof()
    return reader, writer


class ExactCustodyControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.workspaces, self.clients, self.readers, self.channels = [], [], [], []
        self.serial = 0
        self.loop_errors = []
        loop = self._asyncioRunner.get_loop()
        previous = loop.get_exception_handler()
        def handler(active, context):
            self.loop_errors.append({"message": str(context.get("message", ""))[:500],
                "exception": str(context.get("exception", ""))[:500]})
            if previous is None: active.default_exception_handler(context)
            else: previous(active, context)
        loop.set_exception_handler(handler)
        self.addCleanup(loop.set_exception_handler, previous)
        for owner, name in ((socket.socket, "__init__"), (subprocess, "Popen"),
                            (asyncio, "create_subprocess_exec"), (asyncio, "create_subprocess_shell"),
                            (asyncio, "open_connection"), (asyncio, "start_server")):
            guard = patch.object(owner, name, side_effect=AssertionError("UNSELECTED_IO:"+name))
            guard.start(); self.addCleanup(guard.stop)
        for cls, name, replacement in ((WE.M.CommonsClient, "_active", D.inert_active),
                (WV.CommonsClient, "_census", lambda client: {"scope": "INERT_CENSUS"}),
                (WS.CommonsClient, "report", D.inert_report)):
            guard = patch.object(cls, name, replacement)
            guard.start(); self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        errors = []
        for reader in reversed(self.readers):
            try: reader.close()
            except BaseException as error: errors.append("reader:"+str(error))
        for client in reversed(self.clients):
            if not client._closed:
                try: await client.close()
                except BaseException as error: errors.append("client:"+str(error))
        for workspace in reversed(self.workspaces):
            if not workspace._closed:
                try: workspace.close()
                except BaseException as error: errors.append("workspace:"+str(error))
        await asyncio.sleep(0)
        RESULTS.setdefault(self._testMethodName, {})["loop_exceptions"] = list(self.loop_errors)
        if errors or self.loop_errors:
            self.fail("UNCLEAN_TEST_LIFECYCLE:"+repr(errors+self.loop_errors))

    def workspace(self, *, populated=False):
        self.assertFalse(populated)
        config = D.configuration()
        config["index_limits"].update(max_features=1024, max_postings=2048, max_objects=32,
                                      max_snapshots=64, max_db_pages=16384)
        result = WV.Workspace.open(self.root/("workspace-"+str(len(self.workspaces))), config, create=True)
        self.workspaces.append(result)
        return result, None

    def client(self, *, requests=64):
        selected_limits = D.grant_limits()
        selected_limits["acquisition"].update(requests=requests, reply_bytes=8*MIB)
        selected_limits.update(input_bytes=8*MIB, calls=256)
        with patch.object(D, "grant_limits", return_value=selected_limits):
            client = D.DirectControls.client(self)
        client._query_envelope = client._origin_query_envelope = None
        client._body_pool = client._origin_body_pool = None
        client._origin_stores = client.workspace.modules, client.workspace.packets, client.workspace.index
        client._definition_mode = client._origin_definition_mode = "eager"
        foundation = FOUNDATION_PATH.read_bytes()
        self.assertEqual(sha(foundation), FOUNDATION_SHA)
        client._foundation, client._foundation_sha = foundation, FOUNDATION_SHA
        # Inert issuer authority; exact selected source bytes/origins are real.
        for path in sorted((CODE/"v5").rglob("*.py")):
            pin = D.pin(path)
            for owner in client._origin_owners:
                if owner is not None:
                    owner._pins[path] = {k: pin[k] for k in ("bytes", "sha256")}
        return client

    def channel(self, client, *, commands=32):
        policy = P.OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": p} for p in (21001, 21002)]})
        adoption = AdoptedLocationRuntime(CODE/"portable/location", {n: "aa"*32 for n in SOURCE_NAMES},
            installation_root=CODE/"portable", workspace_root=self.root)
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V2", "role": "reader",
            "namespace": client.workspace.adapter.namespace, "body_domain": {"foundation": B.FOUNDATION, "policy": B.POLICY},
            "egress": deepcopy(policy._config), "state": str(client.grant.directory/"inert-location-state"),
            "limits": {"service_ms": 60000, "commands": commands, "query_events": 32, "provider_limit": 8}}
        channel = ServiceLocationProcess(adoption, {n: "bb"*32 for n in ROLE_NAMES}, config,
            client.grant.directory/"inert-location-evidence", deadline=client.grant.deadline)
        script = SimpleNamespace(starts=0, closes=0, commands=[], mode="good", descriptor_peers=[])
        async def start():
            script.starts += 1; self.assertEqual(script.starts, 1)
            channel.process = SimpleNamespace(returncode=None)
            channel._start_task = asyncio.get_running_loop().create_future()
            channel._start_task.set_result({"role": "reader"})
            return {"role": "reader"}
        async def close():
            if not channel.closed:
                script.closes += 1; channel.closed = True
                if channel.process is not None: channel.process.returncode = 0
                channel._close_task = asyncio.get_running_loop().create_future()
                channel._close_task.set_result(None)
        async def command(name, ticket, *, until=None):
            self.assertFalse(channel.closed)
            self.assertLessEqual(until, channel.deadline)
            async with channel.lock:
                channel.sequence += 1
                script.commands.append({"command": name, "ticket": deepcopy(ticket)})
                is_body = name.endswith("-body")
                if name in ("locate", "locate-body"):
                    peers = [peer(2)] if is_body else [peer(1)]
                    if is_body and script.mode == "empty": peers = []
                    return {"ticket": ticket["ticket"], "route_key": ticket["route_key"], "peers": peers,
                        "termination": "ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE", "error": None,
                        "census": {"events": 1, "send_query": 0, "peer_response": 0, "final_peer": 0,
                            "query_error": 0, "provider": 0, "add_provider_write": 0, "last_query_error": None},
                        "routing_peers_before": 1, "routing_peers_after": 1,
                        "assurance": P.ASSURANCE, "global_complete": False, "mathematical_acceptance": False}
                self.assertIn(name, ("descriptor", "descriptor-body"))
                script.descriptor_peers.append(ticket["peer"])
                if is_body and script.mode == "unavailable":
                    return {"status": "DESCRIPTOR_UNAVAILABLE", "ticket": ticket["ticket"],
                        "peer": ticket["peer"], "reason": "TCP_CONNECT_UNAVAILABLE",
                        "mathematical_acceptance": False}
                request = ticket["request"]
                response = {"schema": "DMKN_V5_BODY_DESCRIPTOR_V1" if is_body else P.REPLY_SCHEMA,
                    "namespace": request["namespace"], "role": request["role"], "route_key": request["route_key"],
                    "nonce": request["nonce"], "peer_id": ticket["peer"],
                    "endpoints": [{"host": "127.0.0.1", "port": 21002 if is_body else 21001,
                                    "tls": False, "server_name": None}],
                    "assurance": P.ASSURANCE, "global_complete": False, "mathematical_acceptance": False}
                if is_body and script.mode == "wrong_nonce": response["nonce"] = "ff"*32
                raw = F.compact(response)
                return {"ticket": ticket["ticket"], "authenticated_peer": ticket["peer"],
                    "raw_base64": base64.b64encode(raw).decode("ascii"), "request_body_bytes": len(F.compact(request)),
                    "reply_body_bytes": len(raw), "framed_reply_bytes": len(raw)+4,
                    "assurance": P.ASSURANCE, "mathematical_acceptance": False}
        channel.start, channel.close, channel.command = start, close, command
        channel.report = lambda: {"scope": "INERT_CHANNEL_NO_AUTHENTICATION", "commands": channel.sequence,
            "starts": script.starts, "closes": script.closes, "closed": channel.closed,
            "channel_failed": channel.channel_failed, "mathematical_acceptance": False}
        self.channels.append(channel)
        return channel, script, policy

    def reservation(self, *, pool_limits=None, reserve=True, commands=32, requests=64):
        client = self.client(requests=requests)
        channel, script, policy = self.channel(client, commands=commands)
        loc, search = location_limits(), query_limits()
        envelope = {"location": loc, "search": {**search, "generations": 1}}
        L.reserve_located_queries(client, channel, deepcopy(envelope), policy)
        if reserve: client.reserve_body_location(deepcopy(body_limits() if pool_limits is None else pool_limits))
        return client, script, loc, search

    async def begin(self, **options):
        client, script, loc, search = self.reservation(**options)
        specs = [{"tag": "declaration-kind", "value": "definition"}]
        features = client.workspace.adapter.compile_query(specs)
        await L.next_located_query(client, specs, deepcopy(loc), deepcopy(search), routes=[{
            "features": features, "stripe": 0, "event_cap": 8, "peer_cap": 1, "descriptors": 1}])
        return client, script

    def failed(self, f):
        self.assertEqual(f.reader._state, "FAILED")
        self.assertEqual(f.client._state, "FAILED")
        self.assertFalse(f.reader._busy or f.client._busy)
        self.assertEqual(f.client._body_pool.report()["retained_capabilities"], 0)
        self.assertEqual(f.client._counts["admission_submissions"], 0)
        self.settled(f.client)

    async def fixture(self, **options):
        client, script = await self.begin(**options)
        remote, unused = self.workspace()
        spec, body = E.definitions()
        # One definition suffices; do not introduce an unrelated missing sibling.
        spec["groups"] = spec["groups"][:1]
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        name = opening["group"]["declarations"][0]["name"] if "group" in opening else spec["groups"][0]["declarations"][0]["name"]
        body.update(module_id=module, relative_name=name)
        remote.modules.put_group(module, opening)
        remote.modules.put_body(module, name, body)
        client.workspace.modules.put_group(module, opening)
        raw = client.workspace.adapter.encode_opening(module, name, opening)
        record = client.workspace.adapter.describe(raw)["record"]
        resolved = {**client.workspace.adapter.resolve(record, raw), "opening": opening,
                    "candidate_origin": "EXPLICIT_STRUCTURAL_FIXTURE_ORIGIN_NOT_INDEX_RESULT"}
        origin = importlib.import_module("client.workspace_atomic").Candidate()
        provider_name = next(iter(client._search.endpoints))
        client._candidates[origin] = provider_name, deepcopy(resolved)
        with patch.object(E.T, "IMAGE", D.IMAGE): packet, exact = E.terminal(spec)
        remote.packets.put(module, packet)
        provider = ET.CompositeProvider(index=remote.index, custody=remote.modules, packets=remote.packets)
        async def exchange(endpoint, route, request, maximum, timeout):
            endpoint.validate()
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else C.canonical(value)
            self.assertLessEqual(len(raw), maximum)
            return {"status": 200, "raw": raw, "request_bytes": len(C.canonical(request)),
                    "reply_bytes": len(raw), "header_bytes": 0, "elapsed_ms": 0}
        reader = SR.SemanticReader(client, origin, limits={"modules": 8, "names": 32,
            "groups": 32, "bodies": 16, "steps": 64, "data_bytes": MIB})
        self.readers.append(reader)
        with patch.object(TC, "exchange", exchange), patch.object(DT, "exchange", exchange):
            offered = await client.packet_offers(origin)
            self.assertEqual(offered["packets"], [{"packet_sha256": sha(packet), "packet_bytes": len(packet)}])
            await reader.stage(origin, {"packet_sha256": sha(packet), "packet_bytes": len(packet)})
        preview = reader.preview()
        self.assertEqual(preview["status"], SR.NEED)
        self.assertEqual(len(preview["demands"]), 1)
        demand = preview["demands"][0]
        self.assertEqual(demand, {"kind": "NeedBody", "module": module, "name": name,
                                  "universes": body["universes"], "body_hash": body["body_hash"]})
        return SimpleNamespace(client=client, script=script, reader=reader, origin=origin,
            body=body, demand=demand, remote=remote, provider=provider, exact=exact)

    async def locate(self, f, **options):
        result = await f.reader.locate_body(f.demand, event_cap=8, peer_cap=1,
            descriptor_requests=1, **options)
        self.assertEqual(result["status"], "BODY_CUSTODIANS_LOCATED")
        self.assertEqual(len(result["capabilities"]), 1)
        self.assertFalse(result["global_complete"])
        self.assertFalse(result["mathematical_acceptance"])
        return result["capabilities"][0]

    async def fetch(self, f, capability, *, raw=None, status=200, cleanup_error=None):
        reader, writer = stream(C.canonical(f.body) if raw is None else raw, status, cleanup_error)
        with patch.object(asyncio, "open_connection", return_value=(reader, writer)) as dial:
            result = await f.reader.try_fetch_body_from(f.demand, capability, max_bytes=CAP,
                                                       attempt_timeout_ms=1000)
        self.assertEqual(dial.call_count, 1)
        self.assertEqual((writer.closed, writer.waits), (1, 1))
        return result

    def invariants(self, f):
        c, r = f.client, f.reader
        return {"owners": (id(c), id(c.grant), id(c._budget), id(c._search), id(c._acquisition),
                           id(c._acquisition.structural), id(r)),
                "candidate": deepcopy(c._candidates[f.origin]),
                "contacts": (dict(c._search.endpoints), dict(c._search._adopted_endpoints),
                             dict(c._acquisition.endpoints), dict(c._acquisition.structural.endpoints)),
                "deadlines": (c.grant.deadline, c._budget.deadline, c._search.session.deadline,
                              c._acquisition.structural.deadline)}

    def settled(self, c):
        self.assertIsNone(c._budget.pending)
        self.assertEqual(c._acquisition.structural.inflight, 0)
        self.assertEqual(c._acquisition.structural.reserved_bytes, 0)

    async def test_new_custodian_preserves_reader_and_exact_maps(self):
        f = await self.fixture()
        old = self.invariants(f)
        self.assertEqual(len(f.client._search.endpoints), 1)
        cap = await self.locate(f)
        self.assertEqual(self.invariants(f), old)
        with self.assertRaises(ValueError): f.client._selected_supplier(peer(2))
        before = deepcopy(f.client._budget.used)
        self.assertEqual((await self.fetch(f, cap))["status"], "FETCHED")
        self.assertEqual(self.invariants(f), old)
        self.assertEqual(f.client._budget.used["requests"], before["requests"]+1)
        self.assertEqual(f.client._budget.used["reply_bytes"], before["reply_bytes"]+len(C.canonical(f.body)))
        self.assertEqual(f.reader.preview()["status"], SR.READY)
        self.assertEqual(f.client.workspace.modules.get_body(f.body["module_id"], f.body["relative_name"],
            f.body["universes"], f.body["body_hash"]), f.body)
        self.assertEqual(f.script.starts, 1)
        self.assertEqual([r["command"] for r in f.script.commands],
                         ["locate", "descriptor", "locate-body", "descriptor-body"])
        self.settled(f.client)
        self.assertEqual(f.client._counts["admission_submissions"], 0)
        RESULTS[self._testMethodName] = {"reader": f.reader.report(), "body_pool": f.client._body_pool.report(),
            "budget": f.client._budget.report(), "same_original_maps": True,
            "origin": "EXPLICIT_STRUCTURAL_FIXTURE_P", "location": "INERT_Q_DESCRIPTOR"}

    async def test_prepaid_pool_and_original_aggregate(self):
        f = await self.fixture(pool_limits={**body_limits(), "route_operations": 1,
            "routing_events": 8, "routing_peer_slots": 1, "descriptor_requests": 1, "capabilities": 1})
        pool = f.client._body_pool
        prepayments = f.client._budget.external
        self.assertEqual(len([r for r in prepayments if r["label"] == "body-location"]), 1)
        self.assertIn({"label": "body-location", "requests": 2, "reply_bytes": 4096}, prepayments)
        before = deepcopy(f.client._budget.used)
        await self.locate(f)
        self.assertEqual(f.client._budget.used, before)
        count = len(f.script.commands)
        result = await f.reader.locate_body(f.demand, event_cap=8, peer_cap=1, descriptor_requests=1)
        self.assertEqual(result["status"], "BODY_LOCATION_BUDGET_EXHAUSTED")
        self.assertEqual(result["capabilities"], [])
        self.assertEqual(len(f.script.commands), count)
        self.assertEqual(f.client._budget.used, before)
        self.assertIs(f.client._body_pool, pool)
        stale = await self.fixture()
        outer = deepcopy(stale.client._budget.used)
        stale.script.mode = "empty"
        answer = await stale.reader.locate_body(stale.demand, event_cap=8, peer_cap=1, descriptor_requests=1)
        self.assertEqual(answer["status"], "NO_BODY_CUSTODIAN_WITHIN_ALLOWANCE")
        self.assertEqual(stale.client._body_pool.used["descriptor_requests_issued"], 0)
        stale.script.mode = "unavailable"
        answer = await stale.reader.locate_body(stale.demand, event_cap=8, peer_cap=1, descriptor_requests=1)
        self.assertEqual(answer["status"], "NO_BODY_CUSTODIAN_WITHIN_ALLOWANCE")
        self.assertEqual(answer["attempts"]["descriptor_unavailable"], 1)
        stale.script.mode = "wrong_nonce"
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_DESCRIPTOR_BINDING"):
            await stale.reader.locate_body(stale.demand, event_cap=8, peer_cap=1, descriptor_requests=1)
        self.failed(stale)
        self.assertEqual(stale.client._budget.used, outer)
        self.assertEqual(stale.client._body_pool.used["route_operations_issued"], 3)
        self.assertEqual(stale.client._body_pool.used["descriptor_requests_issued"], 2)
        self.assertEqual(stale.client._body_pool.used["descriptor_reply_bytes_reserved"], 8192)
        self.assertEqual(stale.script.closes, 1)
        RESULTS[self._testMethodName] = {"pool": pool.report(), "budget": f.client._budget.report(),
            "empty_unavailable_malformed_nonrefundable": stale.client._body_pool.report()}

    async def test_settled_absence_consumes_token_without_reader_loss(self):
        f = await self.fixture()
        cap = await self.locate(f)
        before, old = f.reader.report(), self.invariants(f)
        budget = deepcopy(f.client._budget.used)
        result = await self.fetch(f, cap, raw=b"{}", status=404)
        self.assertEqual(result["status"], "UNAVAILABLE_AT_SELECTED_SUPPLIER")
        self.assertFalse(result["global_complete"])
        self.assertEqual(self.invariants(f), old)
        after = f.reader.report()
        for key in ("revision", "bodies", "packets", "modules", "data_bytes"):
            self.assertEqual(after[key], before[key])
        self.assertEqual(f.client._budget.used["reply_bytes"], budget["reply_bytes"]+CAP)
        self.settled(f.client)
        next_cap = await self.locate(f)
        self.assertIsNot(next_cap, cap)
        self.assertEqual((await self.fetch(f, next_cap))["status"], "FETCHED")
        self.assertEqual(f.reader.preview()["status"], SR.READY)
        RESULTS[self._testMethodName] = {"pool": f.client._body_pool.report(), "reader": f.reader.report()}

    async def test_original_located_contact_exact_class_for_both_attempts(self):
        f = await self.fixture()
        c = f.client
        provider = next(iter(c._acquisition.endpoints))
        contact = c._acquisition.endpoints[provider]
        self.assertIs(type(contact), L._Contact)
        bound = AR._binding(c._acquisition, provider)
        self.assertIs(bound["contact"], contact)
        self.assertIs(DR._binding, AR._binding)
        body_reader, writer = stream(C.canonical(f.body))
        with patch.object(asyncio, "open_connection", return_value=(body_reader, writer)):
            result = await c.try_acquire_body(f.origin, f.body["body_hash"], supplier=provider, max_bytes=CAP)
        self.assertEqual(result["status"], "BODY_CUSTODIED")
        declaration = f.provider.dispatch("/v5/modules/group", {"module_id": f.body["module_id"],
            "relative_name": f.body["relative_name"], "group_index": None})
        raw = declaration if type(declaration) is bytes else C.canonical(declaration)
        group_reader, unused_writer = stream(raw)
        with patch.object(asyncio, "open_connection", return_value=(group_reader, unused_writer)):
            result = await c.try_resolve_declaration(f.origin, f.body["module_id"], f.body["relative_name"],
                                                     supplier=provider, max_bytes=CAP)
        self.assertEqual(result["status"], "DECLARATION_CUSTODIED")
        class ForeignContact(L._Contact): pass
        fake = ForeignContact.__new__(ForeignContact)
        fake.__dict__.update(contact.__dict__)
        c._acquisition.endpoints[provider] = c._acquisition.structural.endpoints[provider] = fake
        try:
            with self.assertRaises(ValueError): AR._binding(c._acquisition, provider)
        finally:
            c._acquisition.endpoints[provider] = c._acquisition.structural.endpoints[provider] = contact
        self.settled(c)
        RESULTS[self._testMethodName] = {"body_and_declaration_same_exact_located_contact": True,
                                        "arbitrary_subclass_refused": True}

    async def test_protocol_exact_vectors_and_domain_separation(self):
        domain = {"foundation": "11"*32, "policy": "22"*32}
        body = {"module_id": "33"*32, "export_id": "44"*32, "universes": 3, "body_hash": "55"*32}
        namespace = P.body_namespace(domain)
        independent = lambda tag, value: sha(tag.encode("ascii")+b"\0"+
            json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())
        self.assertEqual(namespace, independent("DMKN-V5-BODY-CUSTODY-NAMESPACE-V1", {
            "module_schema": "DMKN_MODULE_SPEC_V1", "body_schema": "DMKN_MODULE_BODY_V1", **domain}))
        spec = {"namespace": namespace, "role": "committed-body-v1", "body": body}
        key = independent("DMKN-V5-BODY-RENDEZVOUS-V1", spec)
        self.assertEqual(P.body_route_spec(namespace, body), spec)
        self.assertEqual(P.body_route_key(namespace, body), key)
        request = P.body_descriptor_request(namespace, body, "66"*32)
        self.assertEqual(P.validate_body_request(request), request)
        features = ["77"*32]
        index_spec = {"namespace": "88"*32, "role": "formal-index-v1",
                      "predicate": {"all": features}, "stripe": 3}
        index_key = independent("DMKN-V5-INDEX-RENDEZVOUS-V1", index_spec)
        self.assertEqual(P.route_spec("88"*32, features, 3), index_spec)
        self.assertEqual(P.route_key("88"*32, features, 3), index_key)
        # Index profile changes the index key, not this exact semantic address.
        self.assertNotEqual(index_key, P.route_key("99"*32, features, 3))
        self.assertEqual(key, P.body_route_key(P.body_namespace(deepcopy(domain)), body))
        for field in body:
            changed = deepcopy(body)
            changed[field] = 4 if field == "universes" else "aa"*32
            self.assertNotEqual(key, P.body_route_key(namespace, changed))
        for field in domain:
            self.assertNotEqual(namespace, P.body_namespace({**domain, field: "ab"*32}))
        long_name = [["s", "component"+str(i)+"x"*120] for i in range(8)]
        C.validate_name(long_name)
        long_ref = {**body, "export_id": C.export_id(body["module_id"], long_name)}
        long_request = P.body_descriptor_request(namespace, long_ref, "66"*32)
        self.assertLessEqual(len(F.compact(long_request)), 2048)
        self.assertNotIn("relative_name", long_request["body"])
        policy_data = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 21002}]}
        policy = P.OwnerEgressPolicy(policy_data)
        endpoint = {"host": "127.0.0.1", "port": 21002, "tls": False, "server_name": None}
        reply = {"schema": P.BODY_REPLY_SCHEMA, "namespace": namespace, "role": P.BODY_ROLE,
            "route_key": key, "nonce": request["nonce"], "peer_id": peer(2), "endpoints": [endpoint],
            "assurance": P.ASSURANCE, "global_complete": False, "mathematical_acceptance": False}
        self.assertEqual(P.verify_body_descriptor(F.compact(reply), request, peer(2), policy),
                         (policy.endpoint(endpoint),))
        refusals = 0
        for field, value in (("schema", P.REPLY_SCHEMA), ("role", P.ROLE), ("namespace", "aa"*32),
                ("route_key", "aa"*32), ("nonce", "aa"*32), ("peer_id", peer(1)),
                ("endpoints", [endpoint, endpoint]), ("global_complete", True), ("mathematical_acceptance", True)):
            bad = {**reply, field: value}
            with self.subTest(field=field), self.assertRaises(ValueError):
                P.verify_body_descriptor(F.compact(bad), request, peer(2), policy)
            refusals += 1
        for bad in ({**body, "universes": True}, {**body, "extra": 0}, {**body, "export_id": "x"}):
            with self.assertRaises(ValueError): P.body_ref(bad)
        with self.assertRaises(ValueError): P.body_namespace({**domain, "index_profile": "aa"*32})
        RESULTS[self._testMethodName] = {"domain": domain, "body": body, "namespace": namespace,
            "spec": spec, "key": key, "request": request, "reply": reply, "policy": policy_data,
            "index_spec": index_spec, "index_key": index_key, "refusals": refusals}

    async def test_prequery_duplicate_late_and_joint_reservation_refusal(self):
        c, script, unused_loc, unused_search = self.reservation()
        before = deepcopy(c._budget.used)
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_FRESH_CLIENT_POOL"):
            c.reserve_body_location(body_limits())
        self.assertEqual(c._budget.used, before)
        self.assertEqual(script.starts, 0)
        late, late_script = await self.begin(reserve=False)
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_PREQUERY_RESERVATION"):
            late.reserve_body_location(body_limits())
        self.assertIsNone(late._body_pool)
        low, low_script, unused_loc, unused_search = self.reservation(reserve=False, commands=15)
        prepaid = deepcopy(low._budget.used)
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_COMBINED_COMMAND_CAP"):
            low.reserve_body_location(body_limits())
        self.assertEqual(low._budget.used, prepaid)
        self.assertEqual(low_script.starts, 0)
        self.assertEqual(late_script.starts, 1)
        RESULTS[self._testMethodName] = {"duplicate": "REFUSED_NO_NEW_PREPAYMENT",
            "late": "REFUSED", "joint_child_command_cap": "REFUSED_BEFORE_START"}

    async def test_exact_private_capability_source_and_reader_bindings(self):
        rows = []
        # Every public refusal receives a fresh operation: fail-stop is intentional.
        for mode in ("forged", "copied", "wrong-demand", "changed-symbol", "changed-source-pin"):
            f = await self.fixture()
            cap = await self.locate(f)
            selected, demand = cap, deepcopy(f.demand)
            if mode == "forged": selected = BC.BodySupplier()
            if mode == "copied":
                selected = copy(cap)
                self.assertIsNot(selected, cap)
            if mode == "wrong-demand": demand["body_hash"] = "ab"*32
            before = deepcopy(f.client._budget.used)
            guard = None
            if mode == "changed-symbol": guard = patch.object(WE, "_try_body_from", lambda *a, **k: None)
            if mode == "changed-source-pin":
                path = Path(BC.__file__).resolve()
                for owner in f.client._origin_owners:
                    if owner is not None: owner._pins.pop(path)
            if guard is not None: guard.start()
            try:
                with self.assertRaises(ValueError):
                    await f.reader.try_fetch_body_from(demand, selected, max_bytes=CAP)
            finally:
                if guard is not None: guard.stop()
            # Wrong semantic demand is refused by the reader before the facade.
            self.assertEqual(f.reader._state, "FAILED")
            self.assertEqual(f.client._body_pool.report()["retained_capabilities"], 0)
            self.assertEqual(f.client._budget.used, before)
            self.settled(f.client)
            rows.append({"mode": mode, "reader": f.reader._state, "client": f.client._state,
                         "requests_unchanged": True})
        own, foreign = await self.fixture(), await self.fixture()
        own_cap, foreign_cap = await self.locate(own), await self.locate(foreign)
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_UNKNOWN_CAPABILITY"):
            await own.reader.try_fetch_body_from(own.demand, foreign_cap, max_bytes=CAP)
        self.failed(own)
        self.assertIn(foreign_cap, foreign.client._body_pool._entries)
        self.assertNotIn(own_cap, own.client._body_pool._entries)
        bindings = await self.fixture()
        token = await self.locate(bindings)
        c, r = bindings.client, bindings.reader
        pool, row = c._body_pool, c._body_pool._entries[token]
        context = row["context"]
        mutation_table = (
            (r, "_grant", object(), "reader-grant"),
            (r, "_client", object(), "reader-client"),
            (c, "_budget", object(), "original-budget"),
            (c, "_acquisition", object(), "original-acquisition"),
            (context, "request", {**context.request, "body_hash": "ab"*32}, "exact-request"),
            (context, "ref", {**context.ref, "universes": 1}, "exact-reference"),
            (context, "held", b"{}", "held-origin-description"),
            (pool.policy, "_config", {}, "original-owner-egress"),
        )
        private_refusals = []
        before = deepcopy(c._budget.used)
        for owner, name, value, label in mutation_table:
            # Deliberately bypass public decoration only to isolate the private
            # integrity guard; no fetch/admission/state transition is performed.
            c._busy = r._busy = True
            try:
                with patch.object(owner, name, value), self.assertRaises(ValueError):
                    pool.begin_attempt(r, bindings.demand, token)
            finally:
                c._busy = r._busy = False
            self.assertEqual(row["state"], "ISSUED")
            self.assertEqual(pool.used["capabilities_consumed"], 0)
            self.assertEqual(c._budget.used, before)
            private_refusals.append(label)
        with patch.object(c, "_body_pool", None):
            with self.assertRaisesRegex(ValueError, "CLIENT_BODY_POOL_ORIGIN_CHANGED"):
                c._active()
        self.assertEqual((await self.fetch(bindings, token))["status"], "FETCHED")
        RESULTS[self._testMethodName] = {"refusals": rows, "foreign_operation_isolated": True,
            "private_binding_refusals": private_refusals, "actual_facade_pool_origin_guard": True}

    async def test_token_lifecycle_and_clean_locator_shutdown(self):
        f = await self.fixture()
        first, second = await self.locate(f), await self.locate(f)
        rows = [f.client._body_pool._entries[token] for token in (first, second)]
        # Stopped rendezvous does not revoke an issued HTTP hint by itself.
        await f.client._channel.close()
        self.assertEqual((await self.fetch(f, first))["status"], "FETCHED")
        self.assertEqual(f.client._body_pool.report()["retained_capabilities"], 0)
        self.assertTrue(all(row["state"] == "SPENT" for row in rows))
        self.assertEqual(f.reader.preview()["status"], SR.READY)
        closed = await self.fixture()
        token = await self.locate(closed)
        row = closed.client._body_pool._entries[token]
        closed.reader.close()
        self.assertEqual(row["state"], "SPENT")
        self.assertNotIn(token, closed.client._body_pool._entries)
        retired = await self.fixture()
        token = await self.locate(retired)
        row = retired.client._body_pool._entries[token]
        # Exact same private retirement used by next_located_query; no new query.
        retired.client._query_envelope.retire()
        self.assertEqual(retired.client._body_pool.report()["retained_capabilities"], 0)
        self.assertEqual(row["state"], "SPENT")
        replay = await self.fixture()
        token = await self.locate(replay)
        await self.fetch(replay, token, raw=b"{}", status=404)
        before = deepcopy(replay.client._budget.used)
        with self.assertRaisesRegex(ValueError, "BODY_LOCATION_UNKNOWN_CAPABILITY"):
            await replay.reader.try_fetch_body_from(replay.demand, token, max_bytes=CAP)
        self.assertEqual(replay.client._budget.used, before)
        self.failed(replay)
        channel_faults = []
        for mode in ("nonzero-exit", "forced", "failed-close"):
            f = await self.fixture()
            token = await self.locate(f)
            row = f.client._body_pool._entries[token]
            channel = f.client._channel
            if mode == "nonzero-exit": channel.process.returncode = 7
            elif mode == "forced": channel.forced_termination = True
            else:
                channel.process.returncode = 0
                channel._close_task = asyncio.get_running_loop().create_future()
                channel._close_task.set_exception(ValueError("SELECTED_CLOSE_FAULT"))
                # Explicitly retrieve it: the helper must still inspect failure.
                self.assertIsInstance(channel._close_task.exception(), ValueError)
            before = deepcopy(f.client._budget.used)
            with self.assertRaises(ValueError):
                await f.reader.try_fetch_body_from(f.demand, token, max_bytes=CAP)
            self.failed(f)
            self.assertEqual(row["state"], "SPENT")
            self.assertEqual(f.client._budget.used, before)
            channel_faults.append(mode)
        RESULTS[self._testMethodName] = {"fulfillment_revokes_other_tokens": True,
            "clean_location_close_preserves_http_token": True, "reader_close_revokes": True,
            "query_retirement_revokes": True, "spent_replay_refused_before_begin": True,
            "known_uncertain_channel_refusals": channel_faults}

    async def test_outer_refusal_and_predial_expiry_conserve_original_budget(self):
        f = await self.fixture()
        cap = await self.locate(f)
        pool, row = f.client._body_pool, f.client._body_pool._entries[cap]
        # Consume the real remaining original envelope through its ticket API.
        # No live cap/deadline mutation and no replacement budget.
        remaining = f.client._budget.limits["reply_bytes"]-f.client._budget.used["reply_bytes"]
        ticket = f.client._budget.begin(remaining)
        f.client._budget.settle(ticket, remaining)
        before = deepcopy(f.client._budget.used)
        with self.assertRaisesRegex(ValueError, "RECEIPT_AGGREGATE_BUDGET"):
            await f.reader.try_fetch_body_from(f.demand, cap, max_bytes=CAP)
        self.failed(f)
        self.assertEqual(row["state"], "SPENT")
        self.assertEqual(f.client._budget.used, before)
        self.assertEqual((pool.used["capabilities_consumed"], pool.used["body_attempts"]), (1, 0))
        expired = await self.fixture()
        cap = await self.locate(expired)
        pool, row = expired.client._body_pool, expired.client._body_pool._entries[cap]
        after_hint = row["expires"]+0.001
        self.assertLess(after_hint, expired.client.grant.deadline)
        before = deepcopy(expired.client._budget.used)
        # Substitute only the helper's clock object; ordinary monotonic clocks,
        # actual asyncio deadlines and adopted grant caps remain unchanged.
        with patch.object(BC, "time", SimpleNamespace(monotonic=lambda: after_hint)):
            with self.assertRaisesRegex(ValueError, "BODY_LOCATION_CAPABILITY_EXPIRED"):
                await expired.reader.try_fetch_body_from(expired.demand, cap, max_bytes=CAP)
        self.failed(expired)
        self.assertEqual(row["state"], "SPENT")
        self.assertEqual((pool.used["capabilities_consumed"], pool.used["body_attempts"]), (1, 1))
        self.assertEqual(expired.client._budget.used["requests"], before["requests"]+1)
        self.assertEqual(expired.client._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
        RESULTS[self._testMethodName] = {"outer_begin_refusal_consumed_not_attempted": True,
            "expired_predial_token_consumed_charged_without_socket": True}

    async def test_wrong_body_readback_and_transport_cleanup_are_fatal(self):
        observations = []
        for mode in ("wrong-body", "readback", "cleanup", "cancel"):
            f = await self.fixture()
            cap = await self.locate(f)
            row = f.client._body_pool._entries[cap]
            body = deepcopy(f.body)
            if mode == "wrong-body": body["expression"] = ["sort", ["succ", ["zero"]]]
            raw = C.canonical(body)
            cleanup = RuntimeError("SELECTED_CLEANUP_FAULT") if mode == "cleanup" else (
                asyncio.CancelledError("SELECTED_CANCEL_FAULT") if mode == "cancel" else None)
            read, writer = stream(raw, cleanup_error=cleanup)
            getter = f.client.workspace.modules.get_body
            def broken_get(*args):
                # Verify the real post-commit read, then fault the readback seam.
                actual = getter(*args)
                self.assertEqual(actual, f.body)
                raise ValueError("SELECTED_READBACK_FAULT")
            guard = patch.object(f.client.workspace.modules, "get_body", side_effect=broken_get) if mode == "readback" else None
            if guard is not None: guard.start()
            try:
                with patch.object(asyncio, "open_connection", return_value=(read, writer)) as dial:
                    error_type, reason = {
                        "wrong-body": (ValueError, "BODY_HASH_BINDING"),
                        "readback": (ValueError, "SELECTED_READBACK_FAULT"),
                        "cleanup": (AR.BodyCleanupError, "BODY_SOCKET_CLOSURE_UNCERTAIN"),
                        "cancel": (asyncio.CancelledError, "SELECTED_CANCEL_FAULT"),
                    }[mode]
                    with self.assertRaisesRegex(error_type, reason):
                        await f.reader.try_fetch_body_from(f.demand, cap, max_bytes=CAP)
                self.assertEqual(dial.call_count, 1)
            finally:
                if guard is not None: guard.stop()
            self.failed(f)
            self.assertEqual(row["state"], "SPENT")
            self.assertEqual((writer.closed, writer.waits), (1, 1))
            self.assertEqual(f.client._body_pool.used["settled_unavailable"], 0)
            if mode == "readback": self.assertEqual(getter(f.body["module_id"], f.body["relative_name"],
                f.body["universes"], f.body["body_hash"]), f.body)
            else:
                with self.assertRaises(ValueError): getter(f.body["module_id"], f.body["relative_name"],
                    f.body["universes"], f.body["body_hash"])
            observations.append({"mode": mode, "status": "FAILED_NOT_ORDINARY_ABSENCE",
                "pool": f.client._body_pool.report(), "budget": f.client._budget.report()})
        RESULTS[self._testMethodName] = {"faults": observations}

    async def test_provider_finite_body_readback_and_builder_dispatch(self):
        f = await self.fixture()
        address = {key: deepcopy(f.body[key]) for key in ("module_id", "relative_name", "universes", "body_hash")}
        original = deepcopy(address)
        got = ADVERT._body_readback(f.remote, [address], time.monotonic()+5)
        self.assertEqual(address, original)
        self.assertEqual(got["refs"], [{"module_id": address["module_id"],
            "export_id": C.export_id(address["module_id"], address["relative_name"]),
            "universes": address["universes"], "body_hash": address["body_hash"]}])
        self.assertEqual(got["observations"]["bodies_read"], 1)
        self.assertFalse(got["observations"]["remote_placement_confirmed"])
        for rows in ([], [address, address], [address]*9, [{**address, "extra": None}]):
            with self.assertRaises(ValueError): ADVERT._body_routes(rows)
        with self.assertRaises(ValueError):
            ADVERT._body_readback(f.client.workspace, [address], time.monotonic()+5)
        with self.assertRaisesRegex(ValueError, "ADVERTISED_BODY_READBACK_DEADLINE"):
            ADVERT._body_readback(f.remote, [address], time.monotonic()-1)
        with patch.object(f.remote, "_lock", None):
            with self.assertRaisesRegex(ValueError, "ADVERTISED_BODY_WORKSPACE_LOCK"):
                ADVERT._body_readback(f.remote, [address], time.monotonic()+5)
        for role in DIST.BASE_ROLES:
            self.assertIn("v5/client/body_custody.py", DIST.required_sources(role))
        params = {"schema": ADVERT.SCHEMA_V3, "location": {}, "index_view": None,
                  "body_routes": [address]}
        selected = DIST.builtin_parameters(CODE, DIST.LOCATION_ROLE, "serve-advertised", params)
        self.assertEqual(selected["schema"], ADVERT.SCHEMA_V3)
        self.assertEqual(selected["location"], {"installation_root": str(CODE/"base")})
        self.assertEqual(params["location"], {})
        with self.assertRaises(ValueError): DIST.builtin_parameters(CODE, DIST.BASE_ROLE, "serve-advertised", params)
        with self.assertRaises(ValueError): DIST.builtin_parameters(CODE, DIST.LOCATION_ROLE, "serve", params)
        RESULTS[self._testMethodName] = {"readback": got, "body_only_v3_builder_dispatch": True,
            "missing_body_refused": True, "lock_and_deadline_required": True}


SELECTED = (
    "test_protocol_exact_vectors_and_domain_separation",
    "test_new_custodian_preserves_reader_and_exact_maps",
    "test_prepaid_pool_and_original_aggregate",
    "test_settled_absence_consumes_token_without_reader_loss",
    "test_original_located_contact_exact_class_for_both_attempts",
    "test_prequery_duplicate_late_and_joint_reservation_refusal",
    "test_exact_private_capability_source_and_reader_bindings",
    "test_token_lifecycle_and_clean_locator_shutdown",
    "test_outer_refusal_and_predial_expiry_conserve_original_budget",
    "test_wrong_body_readback_and_transport_cleanup_are_fatal",
    "test_provider_finite_body_readback_and_builder_dispatch",
)


def main():
    global OUTPUT, CODE
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    if Path.cwd() != PROJECT or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise ValueError("CANONICAL_ISOLATED_CONTROLS")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_dir() or OUTPUT.resolve() != OUTPUT or not OUTPUT.is_relative_to(PROJECT/"experiments"):
        raise ValueError("EXISTING_OUTPUT_REQUIRED")
    CODE = stage_sources(OUTPUT)
    imports()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(ExactCustodyControls(n) for n in SELECTED))
    node_result = {"status": "NOT_RUN_PYTHON_CONTROLS_FAILED"}
    if result.wasSuccessful():
        vectors = OUTPUT/"protocol-vectors.json"
        with vectors.open("x", encoding="utf-8") as stream:
            json.dump(RESULTS["test_protocol_exact_vectors_and_domain_separation"], stream, sort_keys=True)
        if sha(NODE.read_bytes()) != NODE_SHA: raise ValueError("RETAINED_NODE_PIN")
        child = subprocess.run([str(NODE), str(SOURCE/"body_location/tests/controls01.mjs"),
            "--code", str(CODE), "--vectors", str(vectors),
            "--output", str(OUTPUT/"node-controls-result.json")],
            cwd=PROJECT, stdin=subprocess.DEVNULL, capture_output=True, timeout=25,
            creationflags=subprocess.CREATE_NO_WINDOW)
        for name, raw in (("node-stdout.txt", child.stdout), ("node-stderr.txt", child.stderr)):
            if len(raw) > 65536: raise ValueError("NODE_CONTROL_OUTPUT_BOUND")
            with (OUTPUT/name).open("xb") as stream: stream.write(raw)
        node_report = OUTPUT/"node-controls-result.json"
        if node_report.is_file() and node_report.stat().st_size <= MIB:
            node_result = json.loads(node_report.read_bytes())
        else: node_result = {"status": "MISSING_OR_OVERSIZED_NODE_RESULT"}
        node_result["exit_code"] = child.returncode
    expected_node_groups = {"protocol_cross_language_and_role_isolation",
        "same_locator_wrappers_and_shared_publication_caps", "intent_atomic_role_validation_and_withdrawal",
        "shared_descriptor_stream_caps_and_ipc"}
    groups = node_result.get("groups", {})
    node_passed = (node_result.get("schema") == "DMKN_V5_EXACT_CUSTODY_NODE_CONTROLS_V1"
        and node_result.get("status") == "PASS" and node_result.get("exit_code") == 0
        and node_result.get("mathematical_acceptance") is False
        and type(groups) is dict and set(groups) == expected_node_groups
        and all(row.get("status") == "PASS" for row in groups.values()))
    passed = result.wasSuccessful() and node_passed
    report = {"status": "PASS" if passed else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": SELECTED, "results": RESULTS, "sources": SOURCE_COPIES,
        "scope": "REAL_STRUCTURAL_CUSTODY_READER_ACCOUNTING_INERT_OWNERS_LOCATION_AND_HTTP",
        "mathematical_acceptance": False, "native_calls": 0, "proof_calls": 0,
        "network_calls": 0, "location_child_calls": 0, "pure_node_controls": node_result}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())
