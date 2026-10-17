"""Changed two-form boundary; synthetic issuers, no cryptographic acceptance.

Reuse frozen fixture construction, NOT its old test suite. Provider dispatch,
stores, parsers, budgets and client methods are real. HTTP exchange and the
originating search are explicitly inert fixtures: no socket or DHT is started.
This is not qualification of public networking, actual A or mathematical reuse.
"""
import asyncio
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from client import test_workspace_mixed as T
from client import workspace_evidence as W
from custody.module_store import BODY_SCHEMA
from delta import transport as DT
from delta_claims.claims import expected_journal
from evidence_network import packet as P
from evidence_network.custody import PacketStore, public_profile
from evidence_network.transport import CompositeProvider, EvidenceAcquisition
from mixed_claims.packet import Envelope, parse_packet
from modules import codec as C
from transport import clients as TC

B, MIB, EVIDENCE = T.B, T.MIB, None
RETENTION = {"mode": "quota-bounded-local-custody"}


def configuration():
    result = T.configuration()
    result.update(schema=W.SCHEMA, wire_profile=public_profile(T.IMAGE),
                  terminal_receipt_bytes=65536)
    return result


def terminal(spec, rank=0):
    exact = expected_journal(C.summarize(spec), rank, B.RELATION_IMAGE)
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")+bytes.fromhex(T.IMAGE)
        +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
        +B.commitment([exact])+(1).to_bytes(4, "little")
        +rank.to_bytes(8, "little")+(1).to_bytes(8, "little"))
    raw = P.pack_terminal(header, exact, 0, [], T.RECEIPT, aggregate_image=T.IMAGE,
                          envelope=Envelope(), terminal_receipt_bytes=65536)
    return raw, exact


def definitions():
    spec = T.spec("alpha")
    body = ["sort", ["zero"]]
    descriptor = {"kind": "definition", "name": [["s", "alpha"]], "universes": 0,
        "type": ["sort", ["succ", ["zero"]]], "value_hash": C.body_id(body, 0),
        "meta": {"hint": "abbrev", "safety": "safe"}}
    sibling = deepcopy(descriptor); sibling["name"] = [["s", "beta"]]
    spec["groups"] = [{"kind": "ordinary", "declarations": [descriptor]},
                      {"kind": "ordinary", "declarations": [sibling]}]
    module = C.module_id(spec)
    response = {"schema": BODY_SCHEMA, "module_id": module,
        "relative_name": sibling["name"], "universes": 0,
        "body_hash": sibling["value_hash"], "expression": body}
    return spec, response


class SyntheticEndpoint:
    label = "inert-provider-dispatch-not-network"
    def validate(self):
        pass


class SyntheticSearch:
    def report(self):
        return {"synthetic": True, "search_executed": False}


class EvidenceControls(unittest.TestCase):
    def setUp(self):
        self.root = EVIDENCE/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2))
        self.root.mkdir()
        self.workspaces, self.clients, self.owners = [], [], []

    def tearDown(self):
        for client in reversed(self.clients):
            if not client._closed: asyncio.run(client.close())
        for owner in reversed(self.owners): owner.close()
        for workspace in reversed(self.workspaces):
            if not workspace._closed: workspace.close()

    def operation(self, name="w", *, existing=None, cpu=120):
        workspace = W.Workspace.open(self.root/name, configuration(), create=existing is None)
        self.workspaces.append(workspace)
        grant = workspace.reserve(T.grant_limits(cpu))
        owners = T.SyntheticOwners(grant, workspace._envelope)
        self.owners.append(owners)
        base = Path(W.__file__).resolve().parents[1]
        for relative in ("client/workspace_evidence.py", "evidence_network/__init__.py",
                         "evidence_network/packet.py", "evidence_network/custody.py",
                         "evidence_network/transport.py"):
            path = base/relative; raw = path.read_bytes()
            for owner in (owners.aggregate, owners.delta):
                owner._pins[path] = {"bytes": len(raw), "sha256": T.sha(raw)}
        client = workspace.operation(grant, aggregate_owner=owners.aggregate,
            delta_owner=owners.delta, foundation_bytes=T.FOUNDATION_BYTES,
            foundation_sha256=T.sha(T.FOUNDATION_BYTES))
        self.clients.append(client)
        return workspace, client, owners

    def put(self, workspace, raw, spec):
        module = C.module_id(spec)
        workspace.packets.put(module, raw)
        return module, T.sha(raw), len(raw)

    def retain(self, client, spec, bodies=()):
        module = C.module_id(spec)
        return client.retain_semantics(
            [{"module": module, "opening": C.group_opening(spec, i)}
             for i in range(len(spec["groups"]))], list(bodies))

    def dispatch_fixture(self, source, target, client):
        provider = CompositeProvider(index=source.index, custody=source.modules, packets=source.packets)
        acquisition = EvidenceAcquisition(target.adapter, {"p": SyntheticEndpoint()},
            public_profile(T.IMAGE), client._budget, target.modules, target.packets)
        client._acquisition = acquisition
        client._search = SyntheticSearch()
        calls = []

        async def exchange(endpoint, route, request, maximum, timeout):
            calls.append((route, deepcopy(request)))
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else C.canonical(value)
            if len(raw) > maximum: raise ValueError("TEST_REPLY_BOUND")
            return {"status": 200, "raw": raw, "request_bytes": len(C.canonical(request)),
                    "reply_bytes": len(raw), "header_bytes": 0, "elapsed_ms": 0}
        return exchange, calls

    def record(self, workspace, spec, name=None):
        module = C.module_id(spec)
        chosen = spec["groups"][0]["declarations"][0]["name"] if name is None else name
        raw = workspace.adapter.encode_opening(module, chosen, C.group_opening(spec, 0))
        return workspace.adapter.describe(raw)["record"]

    def test_canonical_closed_dispatch_and_terminal_binding(self):
        spec = T.spec("target"); raw, exact = terminal(spec)
        args = dict(aggregate_image=T.IMAGE, terminal_receipt_bytes=65536)
        kind, summary, held, census = P.inspect_evidence(raw, Envelope(), **args)
        self.assertEqual((kind, summary, held), ("terminal", C.summarize(spec), exact))
        self.assertEqual(census["deltas"], 0)
        receipt, header, held, index, siblings, member = P.parse_terminal(raw, Envelope(), **args)
        self.assertEqual((receipt, held, index, siblings), (T.RECEIPT, exact, 0, ()))
        self.assertEqual(member["module"], C.module_id(spec))
        with self.assertRaises(ValueError): parse_packet(raw, Envelope(), aggregate_image=T.IMAGE)
        for change in ("schema", "extra", "bool-byte", "path", "receipt-uppercase", "wrong-image"):
            value = C.parse_json(raw)
            if change == "schema": value["schema"] = "not-selected"
            elif change == "extra": value["accepted"] = True
            elif change == "bool-byte": value["journal"][0] = True
            elif change == "path": value["siblings"] = [[0]*32]
            elif change == "receipt-uppercase": value["receipt_hex"] = "AB"
            else: value["header"][12] ^= 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                P.inspect_evidence(C.canonical(value), Envelope(), **args)
        for malformed in (raw+b"\n", b'{"schema":"x","schema":"y"}',
                          raw.replace(b'"member_index":0', b'"member_index":0.0')):
            with self.assertRaises(ValueError): P.inspect_evidence(malformed, Envelope(), **args)
        with self.assertRaises(ValueError):
            P.parse_terminal(raw, Envelope(), aggregate_image=T.IMAGE, terminal_receipt_bytes=1)
        ranked, _ = terminal(spec, rank=2)
        with self.assertRaises(ValueError):
            P.inspect_evidence(ranked, Envelope(rank=1), **args)

    def test_two_forms_preserve_exact_target_and_one_store_profile(self):
        workspace, client, owners = self.operation()
        mixed, summary = T.mixed_packet(); spec = C.parse_json(mixed)["deltas"][-1]["local_spec"]
        sealed, exact = terminal(spec, rank=1)
        self.assertIs(type(workspace.packets), PacketStore)
        module, _, _ = self.put(workspace, mixed, spec); self.put(workspace, sealed, spec)
        for raw in (mixed, sealed):
            _, held_summary, held_j, _ = P.inspect_evidence(raw, workspace._envelope,
                aggregate_image=T.IMAGE, terminal_receipt_bytes=65536)
            self.assertEqual((held_summary, held_j), (summary, exact))
            self.assertEqual(workspace.packets.inspect(module, raw)[0], summary)
        offer = workspace.packets.offer({"module_id": module,
            "wire_profile_id": workspace.packets.profile_id, "max_offers": 4, "max_bytes": 4096})
        self.assertEqual(len(offer["packets"]), 2)
        self.assertFalse(offer["mathematical_acceptance"])
        self.assertEqual(sum(owners.receives.values()), 0)
        with self.assertRaises(ValueError): workspace.packets.put("00"*32, sealed)

    def test_local_typed_admission_export_and_one_reservation(self):
        workspace, client, owners = self.operation(cpu=30)
        mixed, _ = T.mixed_packet(); spec = C.parse_json(mixed)["deltas"][-1]["local_spec"]
        sealed, exact = terminal(spec, rank=1)
        terminal_args = self.put(workspace, sealed, spec)
        token = client.admit_local(*terminal_args, expected_exact_journal=exact,
            native_cpu_seconds=10, receipt_cpu_seconds=10)
        self.assertEqual(client.describe(token)["kind"], "A-member")
        self.assertEqual(client.export_evidence(token), sealed)
        self.assertEqual((owners.receives["A"], owners.receives["mixed"]), (1, 0))
        repeat = client.admit_local(*terminal_args, expected_exact_journal=exact,
            native_cpu_seconds=10, receipt_cpu_seconds=10)
        self.assertEqual(client.describe(repeat)["live"]["journal"], exact)
        other = client.admit_local(*self.put(workspace, mixed, spec), expected_exact_journal=exact,
            native_cpu_seconds=10, receipt_cpu_seconds=10)
        self.assertEqual(client.export_evidence(other), mixed)
        self.assertEqual((owners.receives["A"], owners.receives["mixed"]), (1, 1))
        used = client.report()["acquisition"]["used"]
        self.assertEqual((used["verify_attempts"], used["worker_cpu_seconds"]), (2, 30))

    def test_same_module_different_journal_refuses_cold_and_warm(self):
        spec = T.spec("ranked"); raw, exact = terminal(spec)
        other = expected_journal(C.summarize(spec), 1, B.RELATION_IMAGE)
        self.assertNotEqual(exact, other)
        for warm in (False, True):
            workspace, client, owners = self.operation("warm" if warm else "cold")
            args = self.put(workspace, raw, spec)
            if warm: client.admit_local(*args, expected_exact_journal=exact, receipt_cpu_seconds=10)
            with self.assertRaises(ValueError):
                client.admit_local(*args, expected_exact_journal=other, receipt_cpu_seconds=10)
            self.assertEqual(owners.receives["A"], int(warm))
            self.assertTrue(owners.aggregate._closed)
            self.assertEqual(client._warrants, {})

    def test_acquisition_structural_dispatch_and_typed_live_reuse(self):
        source, publisher, _ = self.operation("s")
        target, client, owners = self.operation("t")
        spec = T.spec("remote"); raw, exact = terminal(spec)
        self.retain(publisher, spec)
        publisher.publish(raw, [spec["groups"][0]["declarations"][0]["name"]], retention_policy=RETENTION)
        exchange, calls = self.dispatch_fixture(source, target, client)
        async def exercise():
            candidate = await client.resolve("p", self.record(source, spec))
            offer = await client.packet_offers(candidate)
            token = await client.acquire(candidate, offer["packets"][0], expected_exact_journal=exact,
                                         receipt_cpu_seconds=10)
            second = await client.acquire(candidate, offer["packets"][0], expected_exact_journal=exact,
                                          receipt_cpu_seconds=10)
            return token, second
        with patch.object(DT, "exchange", exchange), patch.object(TC, "exchange", exchange):
            token, second = asyncio.run(exercise())
        self.assertEqual(client.describe(token)["live"]["journal"], exact)
        self.assertEqual(client.describe(second)["kind"], "A-member")
        self.assertEqual((owners.receives["A"], owners.receives["mixed"]), (1, 0))
        self.assertEqual(client._budget.used["verify_attempts"], 1)
        self.assertEqual(client._budget.used["requests"], len(calls))
        self.assertEqual({route for route, _ in calls},
                         {"/v5/modules/group", DT.OFFER_ROUTE, DT.PACKET_ROUTE})
        self.assertIs(client._acquisition.budget, client._budget)
        self.assertIsNone(client._acquisition.verifier)

    def test_other_group_semantics_use_same_provider_budget_without_authority(self):
        source, publisher, _ = self.operation("s")
        target, client, owners = self.operation("t")
        spec, body = definitions(); self.retain(publisher, spec, [body])
        raw, _ = terminal(spec)
        publisher.publish(raw, [spec["groups"][0]["declarations"][0]["name"]], retention_policy=RETENTION)
        exchange, calls = self.dispatch_fixture(source, target, client)
        async def exercise():
            first = await client.resolve("p", self.record(source, spec))
            sibling = await client.resolve_declaration(first, C.module_id(spec), body["relative_name"], max_bytes=65536)
            result = await client.acquire_body(sibling, body["body_hash"], max_bytes=65536)
            return sibling, result
        with patch.object(DT, "exchange", exchange), patch.object(TC, "exchange", exchange):
            sibling, result = asyncio.run(exercise())
        self.assertEqual(result["body"], body)
        self.assertEqual(client.describe_candidate(sibling)["locator"]["relative_name"], body["relative_name"])
        self.assertEqual(target.modules.get_body(C.module_id(spec), body["relative_name"], 0, body["body_hash"]), body)
        self.assertEqual(len(calls), 3)
        self.assertIsNone(calls[1][1]["group_index"])
        self.assertEqual(client._budget.used["requests"], 3)
        self.assertEqual(sum(owners.receives.values()), 0)
        self.assertEqual(client._warrants, {})

    def test_terminal_publication_partial_reconcile_preserves_semantics(self):
        workspace, client, _ = self.operation()
        spec, body = definitions(); raw, exact = terminal(spec)
        self.retain(client, spec)  # Deliberately no body: not an availability promise.
        with patch.object(workspace.index, "admit", side_effect=ValueError("TEST_INDEX_FAILURE")):
            with self.assertRaises(W.PartialPublicationError) as raised:
                client.publish(raw, [body["relative_name"]], retention_policy=RETENTION)
        row = workspace.db.execute("SELECT id FROM publications").fetchone()
        self.assertIsNotNone(row)
        asyncio.run(client.close()); workspace.close()
        reopened, fresh, owners = self.operation(existing=True)
        result = fresh.reconcile(row[0])
        self.assertEqual(result["phase"], "LOCALLY_PUBLISHED")
        self.assertGreater(result["missing_bodies"], 0)
        self.assertFalse(result["all_future_bodies_covered"])
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(result["intent"]["module"], C.module_id(spec))
        self.assertEqual(sum(owners.receives.values()), 0)
        held, _ = reopened.modules.get_group(C.module_id(spec), body["relative_name"])
        self.assertEqual(held, C.group_opening(spec, 1))
        self.assertEqual(reopened.packets.get(T.sha(raw), len(raw)), raw)

    def test_missing_publication_semantics_and_corrupt_body_refuse(self):
        workspace, client, owners = self.operation("missing")
        spec, body = definitions(); raw, _ = terminal(spec)
        with self.assertRaises(ValueError):
            client.publish(raw, [body["relative_name"]], retention_policy=RETENTION)
        self.assertEqual(workspace.db.execute("SELECT COUNT(*) FROM publications").fetchone()[0], 0)
        self.assertEqual(sum(owners.receives.values()), 0)
        workspace2, client2, owners2 = self.operation("badbody")
        corrupt = deepcopy(body); corrupt["expression"] = ["sort", ["succ", ["zero"]]]
        with self.assertRaises(ValueError): self.retain(client2, spec, [corrupt])
        self.assertEqual(workspace2.modules.status()["counts"]["bodies"], 0)
        self.assertEqual(sum(owners2.receives.values()), 0)

    def test_reopen_keeps_evidence_not_authority(self):
        workspace, client, owners = self.operation()
        spec = T.spec("durable"); raw, exact = terminal(spec)
        self.retain(client, spec)
        client.publish(raw, [spec["groups"][0]["declarations"][0]["name"]], retention_policy=RETENTION)
        token = client.admit_local(C.module_id(spec), T.sha(raw), len(raw), expected_exact_journal=exact,
                                   receipt_cpu_seconds=10)
        asyncio.run(client.close()); workspace.close()
        reopened, fresh, new_owners = self.operation(existing=True)
        self.assertEqual(fresh._warrants, {})
        self.assertNotIn(token, fresh._warrants)
        replacement = fresh.admit_local(C.module_id(spec), T.sha(raw), len(raw), expected_exact_journal=exact,
                                        receipt_cpu_seconds=10)
        self.assertEqual(new_owners.receives["A"], 1)
        self.assertIsNot(token, replacement)
        self.assertEqual(fresh.export_evidence(replacement), raw)

    def test_offered_blob_mutation_refuses_before_issuer(self):
        source, publisher, _ = self.operation("s")
        target, client, owners = self.operation("t")
        spec = T.spec("mutated"); raw, exact = terminal(spec)
        changed = C.parse_json(raw)
        tail = "1" if changed["receipt_hex"][-1] == "0" else "0"
        changed["receipt_hex"] = changed["receipt_hex"][:-1]+tail
        alternate = C.canonical(changed)
        self.assertEqual(len(alternate), len(raw))
        self.retain(publisher, spec)
        publisher.publish(raw, [spec["groups"][0]["declarations"][0]["name"]], retention_policy=RETENTION)
        exchange, calls = self.dispatch_fixture(source, target, client)
        async def mutated(endpoint, route, request, maximum, timeout):
            result = await exchange(endpoint, route, request, maximum, timeout)
            if route == DT.PACKET_ROUTE:
                result.update(raw=alternate, reply_bytes=len(alternate))
            return result
        async def exercise():
            candidate = await client.resolve("p", self.record(source, spec))
            offers = await client.packet_offers(candidate)
            return await client.acquire(candidate, offers["packets"][0], expected_exact_journal=exact,
                                        receipt_cpu_seconds=10)
        with patch.object(DT, "exchange", mutated), patch.object(TC, "exchange", mutated):
            with self.assertRaises(ValueError): asyncio.run(exercise())
        self.assertEqual(sum(owners.receives.values()), 0)
        self.assertTrue(owners.aggregate._closed)
        self.assertEqual(client._budget.used["verify_attempts"], 0)
        self.assertEqual(client._budget.used["requests"], 3)


SELECTED = (
    "test_canonical_closed_dispatch_and_terminal_binding",
    "test_two_forms_preserve_exact_target_and_one_store_profile",
    "test_local_typed_admission_export_and_one_reservation",
    "test_same_module_different_journal_refuses_cold_and_warm",
    "test_acquisition_structural_dispatch_and_typed_live_reuse",
    "test_other_group_semantics_use_same_provider_budget_without_authority",
    "test_terminal_publication_partial_reconcile_preserves_semantics",
    "test_missing_publication_semantics_and_corrupt_body_refuse",
    "test_reopen_keeps_evidence_not_authority",
    "test_offered_blob_mutation_refuses_before_issuer",
)
