"""Focused pair-planner controls; execution requires root's separate selection.

Real canonical exports, SQLite indexes, authenticated summaries/pages and actual
direct/located factories. Mathematical issuers and location edges are INERT.
No proof, native process, Node child, socket or historical test suite is run.
"""
import asyncio
import base64
from copy import deepcopy
import hashlib
import importlib
from itertools import combinations
import json
from pathlib import Path
import socket
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-body-custody-01-input.json"
MAP_SHA = "995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be"
FIXTURE_SHA = "5707cc9c334ca602fe41b56079e5725be30c5c21cc6b2c7591c77b0c9953906b"
MIB = 1024**2
REPLACEMENTS = {
    "v5/discovery/module_export_adapter.py": "c7fde37659753a9238506d399e0be5c44ebb5e3a012b5a681dfa1a1551884fd1",
    "v5/client/direct_contacts.py": "1f4224808ceb65feff3fd80353a3dbea3923e2ad091e7c435193fd82f4dc54c8",
    "v5/client/located_queries.py": "4ffb84789deefb524f7f290b2a8879e3b9a1eadc0febf53ad2f5e1a3e168c66a",
}
OUTPUT = CODE = None
OBSERVED, SOURCE_COPIES = {}, {}
QUERY = dict(providers=1, snapshots=1, requests=2, pages=1, examined=8,
             candidates=4, bytes=131072, wall_ms=30000, inflight=1)
LOCATION = dict(wall_ms=30000, route_operations=1, routing_events=8,
                routing_peer_slots=1, descriptor_requests=1, contacts=1,
                reply_bytes=135168)
INDEX = dict(max_objects=256, max_postings=16384, max_features=4096,
             max_snapshots=256, max_logical_bytes=128*MIB, max_db_pages=32768)
PAGE = dict(examined=32, matches=8, bytes=MIB, timeout_ms=1000, node_reads=100000)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def stage_sources(output):
    raw = MAP_PATH.read_bytes()
    if sha(raw) != MAP_SHA: raise ValueError("BASIS_MAP_CHANGED")
    selected = json.loads(raw)["sdk_sources"]
    if len(selected) != 114: raise ValueError("BASIS_MAP_CENSUS")
    sources = {}
    for logical, row in selected.items():
        relative = Path(row["path"]).relative_to(PROJECT/"software/v5")
        sources[logical] = (SOURCE/relative, row)
    sources["v5/discovery/_pair_planning_baseline.py"] = sources["v5/discovery/module_export_adapter.py"]
    fixture = SOURCE/"client/test_direct_contacts.py"
    fixture_raw = fixture.read_bytes()
    if sha(fixture_raw) != FIXTURE_SHA: raise ValueError("FIXTURE_SOURCE_CHANGED")
    sources["v5/client/test_direct_contacts.py"] = (fixture, dict(bytes=len(fixture_raw), sha256=FIXTURE_SHA))
    for logical, digest in REPLACEMENTS.items():
        path = SOURCE/"pair_planning"/logical[3:]
        raw = path.read_bytes()
        if sha(raw) != digest: raise ValueError("REVIEWED_SUCCESSOR_CHANGED:"+logical)
        sources[logical] = (path, dict(bytes=len(raw), sha256=digest))
    code = output/"selected-code"
    code.mkdir()
    for logical, (path, expected) in sorted(sources.items()):
        raw = path.read_bytes()
        if not 0 < len(raw) <= 2*MIB: raise ValueError("SOURCE_BOUND:"+logical)
        if expected is not None and (len(raw) != expected["bytes"] or sha(raw) != expected["sha256"]):
            raise ValueError("BASIS_SOURCE_CHANGED:"+logical)
        target = code/logical
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream: stream.write(raw)
        if target.read_bytes() != raw: raise ValueError("SOURCE_COPY_CHANGED:"+logical)
        SOURCE_COPIES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    for name in ("client", "location", "modules", "transport", "discovery"):
        if name in sys.modules: raise ValueError("EARLY_PRODUCT_IMPORT:"+name)
    sys.path[:0] = [str(code/"portable"), str(code/"v5")]
    return code


def imports():
    global C, F, B, E, OLD, S, Q, D, L, T, P, OR, WE, WS, WV
    global AdoptedLocationRuntime, ServiceLocationProcess, SOURCE_NAMES, ROLE_NAMES
    C = importlib.import_module("modules.codec")
    F = importlib.import_module("discovery.formal_features")
    B = importlib.import_module("aggregate_claims.bindings")
    E = importlib.import_module("discovery.module_export_adapter")
    OLD = importlib.import_module("discovery._pair_planning_baseline")
    S = importlib.import_module("discovery.discovery_store")
    Q = importlib.import_module("discovery.discovery_query")
    D = importlib.import_module("client.direct_contacts")
    L = importlib.import_module("client.located_queries")
    T = importlib.import_module("client.test_direct_contacts")
    P = importlib.import_module("location.protocol")
    OR = importlib.import_module("location.observed_route")
    WE = importlib.import_module("client.workspace_evidence")
    WS = importlib.import_module("client.workspace_staged")
    WV = importlib.import_module("client.workspace_validated")
    controller = importlib.import_module("location.controller")
    services = importlib.import_module("location.controller_services")
    AdoptedLocationRuntime, SOURCE_NAMES = controller.AdoptedLocationRuntime, controller.SOURCE_NAMES
    ServiceLocationProcess, ROLE_NAMES = services.ServiceLocationProcess, services.ROLE_NAMES


def name(label): return [["s", label]]
def const(label): return ["const", ["foundation", name(label)], []]
def atom(label):
    return dict(tag="type-symbol", symbol=dict(kind="foundation-name",
        name_hash=C.hash_value("foundation-symbol", name(label))))


def profile(*pairs):
    return dict(schema=E.PAIR_PROFILE_SCHEMA,
        pairs=sorted([sorted([deepcopy(a), deepcopy(b)], key=F.compact) for a, b in pairs], key=F.compact))


def adapter(selected=None):
    return E.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)


def export_raw(adopted, label, symbols):
    # Unproved structural exports, NOT kernel-checked formulas or new foundation
    # declarations. Actual codec commitments/ModuleIDs/ExportIDs are never forged.
    typ = const("PUnit")
    for symbol in symbols: typ = ["forall", "default", const(symbol), typ]
    spec = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
        groups=[dict(kind="ordinary", declarations=[dict(name=name(label), kind="theorem",
            universes=0, type=typ, value_hash=None, meta={})])])
    module = C.module_id(spec)
    return adopted.encode_opening(module, name(label), C.group_opening(spec, 0))


def selected_three():
    symbols = ("Prod", "PProd", "HEq")
    return symbols, profile((atom(symbols[0]), atom(symbols[1])),
                            (atom(symbols[0]), atom(symbols[2])))


def guards(test):
    # Preserve socket.socket's actual class: replacing it broke Windows Proactor
    # callbacks in an earlier, already preserved unrelated harness.
    for owner, attribute in ((socket.socket, "__init__"), (subprocess, "Popen"),
            (asyncio, "create_subprocess_exec"), (asyncio, "create_subprocess_shell"),
            (asyncio, "open_connection"), (asyncio, "start_server")):
        guard = patch.object(owner, attribute, side_effect=AssertionError("UNSELECTED_IO:"+attribute))
        guard.start(); test.addCleanup(guard.stop)


class PlannerControls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        guards(self)

    def assert_plan(self, adopted, specs):
        before = deepcopy(specs)
        result = adopted.plan_query(specs)
        self.assertEqual(specs, before)
        self.assertEqual(set(result), {"schema", "namespace", "status", "legacy_features", "features",
            "eligible_pair_features", "added_pair_features", "omitted_pair_features",
            "global_complete", "mathematical_acceptance"})
        self.assertEqual(result["schema"], "DMKN_MODULE_EXPORT_PAIR_QUERY_PLAN_V1")
        self.assertEqual(result["namespace"], adopted.namespace)
        self.assertFalse(result["global_complete"] or result["mathematical_acceptance"])
        legacy = adopted.compile_query(specs)
        self.assertEqual(result["legacy_features"], legacy)
        self.assertLessEqual(set(legacy), set(result["features"]))
        self.assertLessEqual(len(result["features"]), 8)
        for key in ("features", "legacy_features", "eligible_pair_features", "added_pair_features", "omitted_pair_features"):
            self.assertEqual(result[key], sorted(set(result[key])))
        self.assertEqual(set(result["features"]), set(legacy)|set(result["added_pair_features"]))
        self.assertEqual(set(result["eligible_pair_features"])-set(legacy),
                         set(result["added_pair_features"])|set(result["omitted_pair_features"]))
        self.assertFalse(set(result["added_pair_features"])&set(result["omitted_pair_features"]))
        expected = "WIRE_CAP" if result["omitted_pair_features"] else (
            "ALL_ELIGIBLE" if result["added_pair_features"] else "NO_EXTRA_PAIR")
        self.assertEqual(result["status"], expected)
        return result

    def test_default_and_nonpair_profile_bytes_unchanged(self):
        symbols, pair = selected_three()
        fingerprint = dict(schema=E.FINGERPRINT_PROFILE_SCHEMA, paths=[[]])
        for selected in (None, pair, dict(schema=E.PATTERN_PROFILE_SCHEMA), fingerprint):
            new = adapter(selected)
            old = OLD.ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=selected)
            specs = [atom(symbol) for symbol in symbols]
            raw = export_raw(new, "same-unproved-export", symbols)
            self.assertEqual(new.namespace, old.namespace)
            self.assertEqual(new.feature_schema, old.feature_schema)
            self.assertEqual(new.compile_query(specs), old.compile_query(specs))
            self.assertEqual(C.canonical(new.describe(raw)), C.canonical(old.describe(raw)))
            plan = self.assert_plan(new, specs)
            if selected != pair:
                self.assertEqual(plan["status"], "NO_EXTRA_PAIR")
                self.assertEqual(plan["features"], old.compile_query(specs))
        OBSERVED[self._testMethodName] = dict(profiles=4, unchanged_records_and_default_compilation=True)

    def test_exhaustive_three_atom_profiles_queries_and_truth_tables(self):
        symbols = ("Prod", "PProd", "HEq")
        pairs = list(combinations(range(3), 2))
        comparisons = 0
        for profile_bits in range(1, 8):
            selected = profile(*[(atom(symbols[a]), atom(symbols[b]))
                                 for i, (a, b) in enumerate(pairs) if profile_bits&(1<<i)])
            adopted = adapter(selected)
            records = [adopted.extract(export_raw(adopted, "truth"+str(bits),
                [symbol for i, symbol in enumerate(symbols) if bits&(1<<i)])) for bits in range(8)]
            for query_bits in range(1, 8):
                specs = [atom(symbol) for i, symbol in enumerate(symbols) if query_bits&(1<<i)]
                result = self.assert_plan(adopted, specs)
                atomic = {E.feature_id(adopted.namespace, spec) for spec in specs}
                expected_pairs = [E.pair_feature_id(adopted.namespace, pair) for pair in selected["pairs"]
                    if {E.feature_id(adopted.namespace, item) for item in pair} <= atomic]
                self.assertEqual(result["eligible_pair_features"], sorted(expected_pairs))
                self.assertFalse(result["omitted_pair_features"])
                for bits, record in enumerate(records):
                    wanted = query_bits&bits == query_bits
                    self.assertEqual(set(result["features"]) <= set(record["features"]), wanted)
                    self.assertEqual(set(result["legacy_features"]) <= set(record["features"]), wanted)
                    comparisons += 1
        self.assertEqual(comparisons, 392)
        OBSERVED[self._testMethodName] = dict(predicate_comparisons=comparisons, real_export_commitments=True)

    def test_four_atom_complete_and_eight_atom_capped_plans(self):
        four = [atom("a"+str(i)) for i in range(4)]
        adopted = adapter(profile(*list(combinations(four, 2))))
        result = self.assert_plan(adopted, four)
        self.assertEqual((len(result["eligible_pair_features"]), len(result["features"])), (6, 8))
        self.assertEqual(result["status"], "ALL_ELIGIBLE")
        eight = [atom("a"+str(i)) for i in range(8)]
        selected = profile(*([(eight[0], eight[i]) for i in range(1, 8)]+[(eight[1], eight[2])]))
        adopted = adapter(selected)
        result = self.assert_plan(adopted, eight)
        self.assertEqual(result["status"], "WIRE_CAP")
        self.assertEqual((len(result["legacy_features"]), len(result["features"]),
                          len(result["added_pair_features"]), len(result["omitted_pair_features"])), (7, 8, 1, 6))
        # Canonical profile order is the deliberate cap policy, not an optimality claim.
        eligible = [E.pair_feature_id(adopted.namespace, pair) for pair in selected["pairs"]]
        self.assertEqual(result["added_pair_features"], [eligible[1]])
        for count in range(1, len(result["legacy_features"])+1):
            for route in combinations(result["legacy_features"], count):
                self.assertLessEqual(set(route), set(result["features"]))
        original = deepcopy(result)
        result["features"].clear(); result["legacy_features"].clear()
        self.assertEqual(adopted.plan_query(eight), original)
        OBSERVED[self._testMethodName] = dict(full_four_atom_keys=8, capped_eight_atom_keys=8,
            added=1, omitted=6, legacy_route_subsets=127)

    def test_raw_feature_and_profile_refusals_are_not_bypassed(self):
        symbols, selected = selected_three()
        adopted = adapter(selected)
        invalid = [[], ["00"*32], [dict(tag="atomic-pair", atoms=selected["pairs"][0])],
                   [atom("a"+str(i)) for i in range(9)]]
        for specs in invalid:
            with self.assertRaises(ValueError): adopted.plan_query(specs)
        adopted._profile_raw = b"changed"
        with self.assertRaisesRegex(ValueError, "EXPORT_PAIR_PROFILE_CHANGED"):
            adopted.plan_query([atom(symbol) for symbol in symbols])
        OBSERVED[self._testMethodName] = dict(invalid_inputs=4, changed_profile_refused=True)

    def scan(self, store, snapshot, features):
        raw = store.summary(snapshot, features)
        summary = Q.verify_summary(snapshot, store.namespace, features, raw)
        coverage = Q.Coverage(summary)
        hits, examined, pages = [], 0, 0
        plan_count = sum(row["anchor_count"] for row in Q.plan_partitions(summary))
        for planned in Q.plan_partitions(summary):
            position = 0
            for unused in range(8):
                if position == planned["anchor_count"]: break
                request = dict(schema="DMKN_FORMAL_QUERY_REQUEST_V1", namespace=store.namespace,
                    snapshot_id=snapshot, features=features, partition=planned["partition"],
                    anchor=planned["anchor"], start=position, limits=deepcopy(PAGE))
                response = store.page(request)
                checked = coverage.accept(request, response)
                self.assertGreater(checked["next"], position)
                position = checked["next"]
                examined += response["charged"]["examined"]; pages += 1
                hits.extend(row["object_id"] for row in checked["matches"])
            self.assertEqual(position, planned["anchor_count"])
        self.assertEqual(examined, plan_count)
        status = coverage.report()
        self.assertTrue(status["complete_committed_anchor_domain"])
        self.assertFalse(status["global_complete"] or status["mathematical_acceptance"])
        return dict(hits=sorted(hits), examined=examined, pages=pages,
                    summary_bytes=len(F.compact(raw)), coverage=status)

    def test_exact_export_corpus_later_pair_reduces_actual_verified_scan(self):
        symbols, selected = selected_three()
        adopted = adapter(selected)
        by_atom = {F.compact(atom(symbol)): symbol for symbol in symbols}
        first_symbols = [by_atom[F.compact(item)] for item in selected["pairs"][0]]
        missing = next(symbol for symbol in symbols if symbol not in first_symbols)
        store = S.Store(self.root/"store", adopted, deepcopy(INDEX), create=True)
        self.addCleanup(store.close)
        ids = []
        for i in range(96):
            for prefix, present in (("hot", first_symbols), ("separate", [missing])):
                raw = export_raw(adopted, prefix+str(i), present)
                described = adopted.describe(raw)
                declared = C.parse_json(raw)
                self.assertEqual(described["record"]["object_id"],
                                 C.export_id(declared["module_id"], declared["relative_name"]))
                accepted = store.admit(raw, expected_id=described["record"]["object_id"])
                ids.append(accepted["record"]["object_id"])
        target = store.admit(export_raw(adopted, "all-three", symbols))
        self.assertEqual(len(set(ids+[target["record"]["object_id"]])), 193)
        snapshot = target["snapshot_id"]
        specs = [atom(symbol) for symbol in symbols]
        plan = self.assert_plan(adopted, specs)
        before = self.scan(store, snapshot, plan["legacy_features"])
        after = self.scan(store, snapshot, plan["features"])
        self.assertEqual(before["hits"], after["hits"])
        self.assertEqual(after["hits"], [target["record"]["object_id"]])
        self.assertEqual(after["examined"], 1)
        self.assertGreater(before["examined"], after["examined"])
        self.assertGreater(after["summary_bytes"], before["summary_bytes"])
        for old, new in zip(before["coverage"]["partitions"], after["coverage"]["partitions"]):
            self.assertEqual(old["partition"], new["partition"])
            self.assertLessEqual(new["anchor_count"], old["anchor_count"])
        OBSERVED[self._testMethodName] = dict(objects=193, exact_export_ids=True,
            synthetic_posting_adapter_used=False, mathematical_acceptance=False,
            natural_partitioning=True, old=before, enriched=after, query_plan=plan)


def peer():
    value, result = int.from_bytes(b"\0\x24\x08\x01\x12\x20"+b"\x01"*32, "big"), ""
    while value:
        value, index = divmod(value, 58)
        result = P._B58[index]+result
    return P.peer_id("1"+result)


class FactoryControls(unittest.IsolatedAsyncioTestCase):
    contacts = lambda self: T.DirectControls.contacts(self)

    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.workspaces, self.clients = [], []
        self.loop_errors = []
        loop = self._asyncioRunner.get_loop()
        previous = loop.get_exception_handler()
        def handler(active, context):
            self.loop_errors.append(dict(message=str(context.get("message", ""))[:500],
                                         exception=str(context.get("exception", ""))[:500]))
            if previous is None: active.default_exception_handler(context)
            else: previous(active, context)
        loop.set_exception_handler(handler)
        self.addCleanup(loop.set_exception_handler, previous)
        guards(self)
        for cls, key, replacement in ((WE.M.CommonsClient, "_active", T.inert_active),
                (WV.CommonsClient, "_census", lambda client: {"scope": "INERT_CENSUS"}),
                (WS.CommonsClient, "report", T.inert_report)):
            guard = patch.object(cls, key, replacement)
            guard.start(); self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        errors = []
        for client in reversed(self.clients):
            try:
                if not client._closed: await client.close()
            except BaseException as error: errors.append("client:"+str(error))
        for workspace in reversed(self.workspaces):
            try:
                if not workspace._closed: workspace.close()
            except BaseException as error: errors.append("workspace:"+str(error))
        await asyncio.sleep(0)
        OBSERVED.setdefault(self._testMethodName, {})["loop_exceptions"] = list(self.loop_errors)
        if errors or self.loop_errors: self.fail("UNCLEAN_TEST_LIFECYCLE:"+repr(errors+self.loop_errors))

    def workspace(self, *, populated=False):
        self.assertFalse(populated)
        config = T.configuration()
        config.update(schema=WE.CONJUNCTION_SCHEMA, discovery_profile=selected_three()[1])
        config["index_limits"].update(max_features=1024, max_postings=2048, max_objects=32,
                                      max_snapshots=64, max_db_pages=16384)
        workspace = WV.Workspace.open(self.root/("workspace-"+str(len(self.workspaces))), config, create=True)
        self.workspaces.append(workspace)
        return workspace, None

    def client(self):
        limits = T.grant_limits()
        limits["acquisition"].update(requests=16, reply_bytes=2*MIB)
        with patch.object(T, "grant_limits", return_value=limits):
            client = T.DirectControls.client(self)
        client._query_envelope = client._origin_query_envelope = None
        client._body_pool = client._origin_body_pool = None
        client._origin_stores = client.workspace.modules, client.workspace.packets, client.workspace.index
        client._definition_mode = client._origin_definition_mode = "eager"
        for path in sorted((CODE/"v5").rglob("*.py")):
            row = T.pin(path)
            for owner in client._origin_owners:
                if owner is not None: owner._pins[path] = {key: row[key] for key in ("bytes", "sha256")}
        return client

    def channel(self, client, *, empty=False):
        endpoints, policy = self.contacts()
        adoption = AdoptedLocationRuntime(CODE/"portable/location", {key: "aa"*32 for key in SOURCE_NAMES},
            installation_root=CODE/"portable", workspace_root=self.root)
        config = dict(schema="DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", role="reader",
            namespace=client.workspace.adapter.namespace, egress=deepcopy(policy._config),
            state=str(client.grant.directory/"inert-location-state"),
            limits=dict(service_ms=60000, commands=32))
        channel = ServiceLocationProcess(adoption, {key: "bb"*32 for key in ROLE_NAMES}, config,
            client.grant.directory/"inert-location-evidence", deadline=client.grant.deadline)
        script = SimpleNamespace(starts=0, closes=0, commands=[])
        async def start():
            script.starts += 1
            self.assertEqual(script.starts, 1)
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
        async def command(command, ticket, *, until=None):
            self.assertFalse(channel.closed)
            self.assertLessEqual(until, channel.deadline)
            async with channel.lock:
                channel.sequence += 1
                script.commands.append(dict(command=command, ticket=deepcopy(ticket)))
                if command == "locate":
                    return dict(ticket=ticket["ticket"], route_key=ticket["route_key"],
                        peers=[] if empty else [peer()], termination="ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE",
                        error=None, census={**{key: 0 for key in OR.CENSUS}, "events": 1, "last_query_error": None},
                        routing_peers_before=1, routing_peers_after=1, assurance=P.ASSURANCE,
                        global_complete=False, mathematical_acceptance=False)
                self.assertEqual(command, "descriptor")
                request = ticket["request"]
                raw = F.compact(dict(schema=P.REPLY_SCHEMA, namespace=request["namespace"], role=P.ROLE,
                    route_key=request["route_key"], nonce=request["nonce"], peer_id=ticket["peer"],
                    endpoints=[deepcopy(endpoints["peer0"])], assurance=P.ASSURANCE,
                    global_complete=False, mathematical_acceptance=False))
                return dict(ticket=ticket["ticket"], authenticated_peer=ticket["peer"],
                    raw_base64=base64.b64encode(raw).decode("ascii"), request_body_bytes=len(F.compact(request)),
                    reply_body_bytes=len(raw), framed_reply_bytes=len(raw)+4, assurance=P.ASSURANCE,
                    mathematical_acceptance=False)
        channel.start, channel.close, channel.command = start, close, command
        channel.report = lambda: dict(scope="INERT_CHANNEL_NO_CHILD_OR_AUTHENTICATION",
            commands=channel.sequence, starts=script.starts, closes=script.closes,
            closed=channel.closed, channel_failed=channel.channel_failed, mathematical_acceptance=False)
        return channel, script, policy

    def specs(self): return [atom(symbol) for symbol in selected_three()[0]]

    def original(self, client):
        return (client.grant, client._budget, client._origin_owners,
                client.grant.deadline, deepcopy(client._budget.limits))

    def unchanged(self, client, original):
        grant, budget, owners, deadline, limits = original
        self.assertIs(client.grant, grant); self.assertIs(client._budget, budget)
        self.assertEqual(client._origin_owners, owners)
        self.assertEqual(client.grant.deadline, deadline)
        self.assertEqual(client._budget.limits, limits)
        self.assertEqual(client._counts["admission_submissions"], 0)
        self.assertEqual(client._budget.used["verify_attempts"], 0)
        self.assertFalse(client._warrants)

    async def test_direct_default_optin_and_immutable_original_session(self):
        rows = []
        for option in (False, True):
            client = self.client(); original = self.original(client)
            contacts, policy = self.contacts()
            D.reserve_queries(client, {**QUERY, "generations": 1}, policy)
            prepaid = deepcopy(client._budget.used)
            expected = client.workspace.adapter.plan_query(self.specs())
            arguments = {"plan_pairs": True} if option else {}
            result = D.next_query(client, contacts, self.specs(), deepcopy(QUERY), **arguments)
            row = client._query_envelope.generations[0]
            features = expected["features" if option else "legacy_features"]
            self.assertEqual(client._search.session.features, features)
            self.assertEqual(row["query_sha256"], sha(C.canonical(dict(namespace=client.workspace.adapter.namespace,
                                                                      features=features))))
            self.assertEqual(client._budget.used, prepaid)
            self.assertEqual("query_plan" in result, option)
            self.assertEqual("query_plan" in row, option)
            if option:
                self.assertEqual(result["query_plan"], expected)
                self.assertEqual(row["query_plan"], expected)
                result["query_plan"]["features"].clear()
                self.assertEqual(row["query_plan"], expected)
                self.assertEqual(client._search.session.features, expected["features"])
            self.unchanged(client, original)
            rows.append(dict(opt_in=option, features=features, prepayment=prepaid))
        OBSERVED[self._testMethodName] = dict(cases=rows, inert_math=True)

    async def test_located_success_preserves_legacy_route_and_original_owners(self):
        rows = []
        for option in (False, True):
            client = self.client(); original = self.original(client)
            channel, script, policy = self.channel(client)
            L.reserve_located_queries(client, channel, dict(location=deepcopy(LOCATION),
                search={**QUERY, "generations": 1}), policy)
            prepaid = deepcopy(client._budget.used)
            expected = client.workspace.adapter.plan_query(self.specs())
            legacy = expected["legacy_features"]
            arguments = {"plan_pairs": True} if option else {}
            result = await L.next_located_query(client, self.specs(), deepcopy(LOCATION), deepcopy(QUERY),
                routes=[dict(features=legacy, stripe=0, event_cap=8, peer_cap=1, descriptors=1)],
                descriptor_bytes=4096, descriptor_age_ms=10000, **arguments)
            row = client._query_envelope.generations[0]
            self.assertEqual(result["status"], "QUERY_CONTACTS_READY")
            self.assertEqual(client._search.session.features, expected["features" if option else "legacy_features"])
            self.assertEqual(script.commands[0]["ticket"]["route_key"], P.route_key(client.workspace.adapter.namespace, legacy, 0))
            self.assertEqual([item["command"] for item in script.commands], ["locate", "descriptor"])
            self.assertEqual(client._budget.used, prepaid)
            self.assertEqual("query_plan" in result, option)
            self.assertEqual("query_plan" in row, option)
            if option:
                self.assertEqual(row["query_plan"], expected)
                result["query_plan"]["added_pair_features"].clear()
                self.assertEqual(row["query_plan"], expected)
            self.unchanged(client, original)
            self.assertIs(client._channel, channel)
            self.assertEqual(script.starts, 1)
            rows.append(dict(opt_in=option, route=legacy, command_count=len(script.commands)))
        OBSERVED[self._testMethodName] = dict(cases=rows, inert_location=True)

    async def test_located_no_contacts_retains_optin_plan_without_reallocation(self):
        client = self.client(); original = self.original(client)
        channel, script, policy = self.channel(client, empty=True)
        L.reserve_located_queries(client, channel, dict(location=deepcopy(LOCATION),
            search={**QUERY, "generations": 1}), policy)
        expected = client.workspace.adapter.plan_query(self.specs())
        prepaid = deepcopy(client._budget.used)
        result = await L.next_located_query(client, self.specs(), deepcopy(LOCATION), deepcopy(QUERY),
            routes=[dict(features=expected["legacy_features"], stripe=0, event_cap=8, peer_cap=1, descriptors=1)],
            plan_pairs=True)
        self.assertEqual(result["status"], "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN")
        self.assertEqual(result["query_plan"], expected)
        self.assertEqual(client._query_envelope.generations[0]["query_plan"], expected)
        self.assertIsNone(client._search); self.assertIsNone(client._acquisition)
        self.assertEqual(client._budget.used, prepaid)
        self.assertEqual(len(script.commands), 1)
        self.unchanged(client, original)
        OBSERVED[self._testMethodName] = dict(no_contact_not_global_absence=True, generations=1)

    async def test_both_factories_require_strict_boolean_optin(self):
        cases = 0
        for invalid in (1, "yes", None):
            for located in (False, True):
                client = self.client()
                if located:
                    channel, script, policy = self.channel(client)
                    L.reserve_located_queries(client, channel, dict(location=deepcopy(LOCATION),
                        search={**QUERY, "generations": 1}), policy)
                    with self.assertRaisesRegex(ValueError, "PAIR_QUERY_PLAN_OPTION"):
                        await L.next_located_query(client, self.specs(), deepcopy(LOCATION), deepcopy(QUERY),
                            routes=[], plan_pairs=invalid)
                    self.assertEqual(script.starts, 0)
                else:
                    contacts, policy = self.contacts()
                    D.reserve_queries(client, {**QUERY, "generations": 1}, policy)
                    with self.assertRaisesRegex(ValueError, "PAIR_QUERY_PLAN_OPTION"):
                        D.next_query(client, contacts, self.specs(), deepcopy(QUERY), plan_pairs=invalid)
                self.assertFalse(client._query_envelope.generations)
                cases += 1
        OBSERVED[self._testMethodName] = dict(strict_boolean_refusals=cases)


PLANNER_TESTS = (
    "test_default_and_nonpair_profile_bytes_unchanged",
    "test_exhaustive_three_atom_profiles_queries_and_truth_tables",
    "test_four_atom_complete_and_eight_atom_capped_plans",
    "test_raw_feature_and_profile_refusals_are_not_bypassed",
    "test_exact_export_corpus_later_pair_reduces_actual_verified_scan",
)
FACTORY_TESTS = (
    "test_direct_default_optin_and_immutable_original_session",
    "test_located_success_preserves_legacy_route_and_original_owners",
    "test_located_no_contacts_retains_optin_plan_without_reallocation",
    "test_both_factories_require_strict_boolean_optin",
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
    tests = [PlannerControls(name) for name in PLANNER_TESTS]+[FactoryControls(name) for name in FACTORY_TESTS]
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))
    passed = result.wasSuccessful() and result.testsRun == 9 and not result.skipped
    report = dict(schema="DMKN_V5_PAIR_PLANNING_CONTROLS_V1", status="PASS" if passed else "FAIL",
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(PLANNER_TESTS+FACTORY_TESTS), observations=OBSERVED, sources=SOURCE_COPIES,
        scope="REAL_EXPORT_INDEX_QUERY_FACTORIES_INERT_MATHEMATICAL_OWNERS_AND_LOCATION",
        mathematical_acceptance=False, native_calls=0, proof_calls=0, network_calls=0, location_child_calls=0)
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())
