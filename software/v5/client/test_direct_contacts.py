"""Focused direct-contact controls: real structures, explicitly INERT issuers.

Only issuer construction, client liveness/census and reporting are substituted.
The exact validated facade, decorators, bind, search, acquisition, original
budget, grants, custody and index are exercised. No mathematical warrant exists.
"""
import argparse
import asyncio
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from aggregate_claims import bindings as B
from client import direct_contacts as D
from client import workspace_validated as W
from client.workspace_atomic import Candidate
from client.workspace_evidence import SCHEMA as WORKSPACE_SCHEMA
from discovery import formal_features as F
from discovery.search_session import SearchSession
from evidence_network.custody import public_profile
from evidence_network.transport import CompositeProvider, EvidenceAcquisition
from location.protocol import OwnerEgressPolicy
from location.workflow import _LocatedSearchClient
from mixed_claims.packet import Envelope
from modules import codec as C
from transport.receipt_client import AcquisitionBudget

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
IMAGE = "81"*32
OUTPUT = None
SPECS = [{"tag": "declaration-kind", "value": "theorem"},
         {"tag": "result-head", "head": {"tag": "sort"}}]
SEARCH = dict(providers=2, snapshots=2, requests=4, pages=2, examined=32,
              candidates=8, bytes=262144, wall_ms=30000, inflight=1)
PAGE = dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
            record_probes=64, node_reads=10000, hash_calls=200000,
            sql_vm_steps=100000)
OBSERVED = {"inert_clients": 0, "real_loopback_requests": 0,
            "resolved_structural_candidates": 0}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def configuration():
    return {
        "schema": WORKSPACE_SCHEMA, "wire_profile": public_profile(IMAGE),
        "module_limits": dict(modules=8, groups=16, declarations=32, bodies=8,
                              logical_bytes=MIB, db_pages=256),
        "packet_limits": dict(packets=8, offers=16, offers_per_module=4,
                             packet_bytes=65536, logical_bytes=MIB, db_pages=256),
        "index_limits": dict(max_objects=8, max_postings=1024, max_features=128,
                            max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        "packet_envelope": asdict(Envelope()), "terminal_receipt_bytes": 65536,
        "max_operations": 8, "max_report_bytes": MIB, "ledger_pages": 256,
    }


def grant_limits():
    return dict(
        wall_seconds=60, controller_cpu_seconds=30, calls=128, input_bytes=4*MIB,
        worker_cpu_seconds=1, output_bytes=128*MIB, output_entries=1024,
        acquisition=dict(requests=8, reply_bytes=MIB, verify_attempts=1,
                         verification_input_bytes=65536, worker_cpu_seconds=1),
        imports=dict(max_sources=8, max_members=16, max_receipts=8,
                     max_calls=4096, submitted_bytes=MIB, data_bytes=MIB))


class InertOwner:
    def __init__(self, pins):
        self._pins, self.closes = deepcopy(pins), 0

    def close(self):
        self.closes += 1


def inert_active(client):
    F.need(client._state == "OPEN" and not client._closed, "INERT_CLIENT_NOT_OPEN")
    F.need(all(owner is None or owner.closes == 0 for owner in client._origin_owners),
           "INERT_OWNER_CLOSED")
    client._budget.active()
    # This is an explicit fixture check, not genuine owner adoption/verification.
    for name, path in client._required_origins.items():
        F.need(Path(sys.modules[name].__file__).resolve() == path, "INERT_SOURCE_ORIGIN_CHANGED")
        held = client._source_pins[path]
        actual = pin(path)
        F.need(held == {key: actual[key] for key in ("bytes", "sha256")},
               "INERT_SOURCE_BYTES_CHANGED")


def inert_report(client):
    return {"status": client._state, "closed": client._closed,
            "scope": "INERT_ISSUERS_NOT_MATHEMATICAL_AUTHORITY", "mathematical_acceptance": False}


class DirectControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.workspaces, self.clients, self.providers = [], [], []
        for name, replacement in (
            ("_active", inert_active),
            ("_census", lambda client: {"scope": "INERT_CENSUS"}),
            ("report", inert_report),
        ):
            guard = patch.object(W.CommonsClient, name, replacement)
            guard.start()
            self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        for provider in reversed(self.providers):
            await provider.stop()
        for client in reversed(self.clients):
            if not client._closed:
                await client.close()
        for workspace in reversed(self.workspaces):
            if not workspace._closed:
                workspace.close()

    def workspace(self, *, populated=False):
        workspace = W.Workspace.open(self.root/("workspace-"+str(len(self.workspaces))),
                                     configuration(), create=True)
        self.workspaces.append(workspace)
        if not populated:
            return workspace, None
        name = [["s", "syntheticDirectContactDescriptor"]]
        spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
                "groups": [{"kind": "ordinary", "declarations": [{
                    "kind": "theorem", "name": name, "universes": 0,
                    "type": ["sort", ["zero"]], "value_hash": None, "meta": {}}]}]}
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        workspace.modules.put_group(module, opening)
        raw = workspace.adapter.encode_opening(module, name, opening)
        record = workspace.adapter.describe(raw)["record"]
        workspace.index.admit(raw, expected_id=record["object_id"])
        return workspace, SimpleNamespace(module=module, name=name, opening=opening,
                                           record=record, raw=raw)

    def client(self):
        workspace, unused = self.workspace()
        grant = workspace.reserve(grant_limits())
        client = W.CommonsClient.__new__(W.CommonsClient)
        path = Path(D.__file__).resolve()
        selected = pin(path)
        pins = {path: {key: selected[key] for key in ("bytes", "sha256")}}
        owners = tuple(InertOwner(pins) for unused in range(3))+(None,)
        client.receipt, client.aggregate, client.delta, client.preparation = owners
        client.workspace, client.grant, client._origin_owners = workspace, grant, owners
        client._aggregate_image = IMAGE
        client._required_origins, client._source_pins = {}, {}
        client._state, client._busy, client._closed = "OPEN", False, False
        client._calls = client._input_bytes = 0
        client._cleanup_uncertain = False
        client._warrants, client._receipt_cache, client._packet_cache = {}, {}, {}
        client._aggregate_cache, client._candidates, client._staged = {}, {}, {}
        client._context = client._selection_view = client._session = None
        client._channel = client._handoff = client._search = client._acquisition = None
        client._query_used = False
        client._budget = AcquisitionBudget(grant.deadline, grant.limits["acquisition"])
        client._failures, client._publications = [], []
        client._counts = {key: 0 for key in ("admission_submissions", "same_live_hits", "author_calls",
            "store_calls", "publication_attempts", "new_import_sessions")}
        client._staging_counts = dict(packets_staged=0, admission_transitions=0, previews=0)
        self.clients.append(client)
        OBSERVED["inert_clients"] += 1
        return client

    def contacts(self, ports=(21001,), *, approved=None):
        records = {"peer"+str(i): {"host": "127.0.0.1", "port": port,
                    "tls": False, "server_name": None} for i, port in enumerate(ports)}
        policy = OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
            "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": port}
                for port in sorted(set(ports if approved is None else approved))]})
        return records, policy

    def bind(self, client, *, contacts=None, policy=None, limits=None, **options):
        if contacts is None:
            contacts, policy = self.contacts()
        return D.bind(client, contacts, deepcopy(SPECS), policy,
                      deepcopy(SEARCH) if limits is None else limits, **options)

    def failed(self, client):
        self.assertEqual(client._state, "FAILED")
        self.assertTrue(client._budget.closed)
        self.assertEqual(client._warrants, {})
        self.assertFalse(client._busy)
        self.assertTrue(all(owner is None or owner.closes == 1
                            for owner in client._origin_owners))

    def no_verification(self, client):
        for key in ("verify_attempts", "verification_input_bytes", "worker_cpu_seconds"):
            self.assertEqual(client._budget.used[key], 0)
        self.assertEqual(client._counts["admission_submissions"], 0)
        self.assertEqual(client._warrants, {})

    async def test_bind_prepays_original_budget_and_copies_owner_choices_without_io(self):
        client = self.client()
        contacts, policy = self.contacts()
        limits, specs = deepcopy(SEARCH), deepcopy(SPECS)
        original_budget, original_grant = client._budget, client.grant
        with patch.object(asyncio, "open_connection", side_effect=AssertionError("BIND_MUST_NOT_DIAL")):
            ready = D.bind(client, contacts, specs, policy, limits)
        self.assertEqual(ready["status"], "QUERY_CONTACTS_READY")
        self.assertFalse(ready["mathematical_acceptance"] or ready["global_complete"]
                         or ready["location_performed"])
        self.assertIsNone(client._channel)
        self.assertIsNone(client._handoff)
        self.assertIs(client.grant, original_grant)
        self.assertIs(client._budget, original_budget)
        self.assertIs(type(client._search), _LocatedSearchClient)
        self.assertIs(type(client._search.session), SearchSession)
        self.assertIs(type(client._acquisition), EvidenceAcquisition)
        self.assertIs(client._acquisition._search, client._search)
        self.assertIs(client._acquisition.budget, original_budget)
        self.assertIsNone(client._acquisition.verifier)
        self.assertEqual(original_budget.external, [
            {"label": "direct-contact-search", "requests": 4, "reply_bytes": 262144}])
        self.assertEqual(original_budget.used["requests"], 4)
        self.assertEqual(original_budget.used["reply_bytes"], 262144)
        self.assertLessEqual(client._search.session.deadline, original_grant.deadline)
        self.assertTrue(all(expiry <= original_grant.deadline
                            for expiry in client._search._expiries.values()))
        contacts["peer0"]["port"] = 21002
        limits["requests"] = 999
        specs.clear()
        self.assertEqual(client._search.endpoints["peer0"].port, 21001)
        self.assertEqual(client._search.session.limits["requests"], 4)
        self.assertEqual(len(client._search.session.features), 2)
        self.no_verification(client)

    async def test_exact_client_endpoint_policy_and_duplicates_are_required(self):
        for case in ("wrong-client", "bad-label", "duplicate", "unapproved", "public-http"):
            with self.subTest(case=case):
                client = self.client()
                contacts, policy = self.contacts()
                if case == "wrong-client":
                    class ForeignClient(W.CommonsClient):
                        pass
                    client.__class__ = ForeignClient
                elif case == "bad-label":
                    contacts["bad\nlabel"] = contacts.pop("peer0")
                elif case == "duplicate":
                    contacts["other"] = deepcopy(contacts["peer0"])
                elif case == "unapproved":
                    contacts["peer0"]["port"] = 21002
                else:
                    policy = OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1",
                        "mode": "public-ipv4", "public_ports": [443], "test_endpoints": []})
                    contacts["peer0"] = {"host": "1.1.1.1", "port": 443,
                                         "tls": False, "server_name": None}
                with patch.object(asyncio, "open_connection",
                                  side_effect=AssertionError("REFUSAL_MUST_NOT_DIAL")) as dial:
                    with self.assertRaises(ValueError):
                        self.bind(client, contacts=contacts, policy=policy)
                self.assertFalse(dial.called)
                self.assertEqual(client._budget.external, [])
                self.assertIsNone(client._acquisition)
                self.failed(client)

    async def test_missing_or_disagreeing_adopted_source_pin_refuses_before_prepay(self):
        for disagree in (False, True):
            client = self.client()
            path = Path(D.__file__).resolve()
            if disagree:
                client.delta._pins[path]["sha256"] = "0"*64
            else:
                for owner in client._origin_owners[:3]:
                    owner._pins.clear()
            with self.assertRaisesRegex(ValueError, "DIRECT_REQUIRED_SOURCE_PIN"):
                self.bind(client)
            self.assertEqual(client._budget.external, [])
            self.assertIsNone(client._search)
            self.failed(client)

    async def test_second_bind_and_existing_query_never_renew_original_allowance(self):
        client = self.client()
        self.bind(client)
        before = deepcopy(client._budget.used)
        selected = client._search
        with self.assertRaisesRegex(ValueError, "DIRECT_ONE_FRESH_QUERY"):
            self.bind(client)
        self.assertEqual(client._budget.used, before)
        self.assertEqual(len(client._budget.external), 1)
        self.assertIs(client._search, selected)
        self.failed(client)
        occupied = self.client()
        occupied._query_used = True
        with self.assertRaisesRegex(ValueError, "DIRECT_ONE_FRESH_QUERY"):
            self.bind(occupied)
        self.assertEqual(occupied._budget.external, [])
        self.failed(occupied)

    async def test_search_prepayment_cannot_exceed_original_requests_bytes_or_provider_cap(self):
        for case in ("requests", "bytes", "providers"):
            client = self.client()
            limits = deepcopy(SEARCH)
            contacts, policy = self.contacts((21001, 21002))
            limits[case] = 9 if case == "requests" else 2*MIB if case == "bytes" else 1
            with self.assertRaisesRegex(ValueError,
                    "RECEIPT_AGGREGATE_BUDGET|INTEGER_BOUND|DIRECT_PROVIDER_SUBALLOCATION"):
                self.bind(client, contacts=contacts, policy=policy, limits=limits)
            self.assertEqual(client._budget.external, [])
            self.assertIsNone(client._acquisition)
            self.failed(client)

    async def test_acquisition_contact_guard_rejects_disconnected_originating_search(self):
        client = self.client()
        self.bind(client)
        acquisition = client._acquisition
        # One guarded consistency error, not hostile in-process tamper coverage.
        # Trusted callers must not replace or mutate the entry's internal objects.
        acquisition._search = None
        with patch.object(asyncio, "open_connection",
                          side_effect=AssertionError("ORIGIN_REFUSAL_MUST_NOT_DIAL")) as dial:
            with self.assertRaisesRegex(ValueError, "DIRECT_ORIGINAL_ACQUISITION"):
                await acquisition.declaration("peer0", "1"*64, [["s", "unused"]], 65536)
        self.assertFalse(dial.called)
        self.assertIsNone(client._budget.pending)
        self.no_verification(client)

    async def test_expired_contact_refuses_search_and_acquisition_without_renewal(self):
        client = self.client()
        self.bind(client, contact_lifetime_ms=50)
        grant_deadline = client.grant.deadline
        search = client._search
        await asyncio.sleep(0.06)
        with patch.object(asyncio, "open_connection",
                          side_effect=AssertionError("EXPIRED_CONTACT_MUST_NOT_DIAL")) as dial:
            refusal = await client.search_offer("peer0", 65536, max_expanded_bytes=131072)
            self.assertEqual(refusal["reason"], "CONTACT_EXPIRED")
            self.assertEqual(refusal["settlement"], "ABANDONED_CONSERVATIVELY_CHARGED")
            self.assertEqual(search.session.used["requests"], 1)
            self.assertEqual(search.session.used["bytes"], 65536)
            before = deepcopy(client._budget.used)
            with self.assertRaisesRegex(ValueError, "LOCATED_CUSTODY_CONTACT_EXPIRED"):
                await client._acquisition.declaration("peer0", "1"*64, [["s", "unused"]], 65536)
        self.assertFalse(dial.called)
        self.assertEqual(client.grant.deadline, grant_deadline)
        self.assertIs(client._search, search)
        self.assertEqual(client._budget.used["requests"], before["requests"]+1)
        self.assertEqual(client._budget.used["reply_bytes"], before["reply_bytes"]+65536)
        self.assertIsNone(client._budget.pending)
        self.no_verification(client)

    async def test_record_not_returned_by_bound_search_cannot_be_resolved(self):
        client = self.client()
        unused_workspace, held = self.workspace(populated=True)
        self.bind(client)
        with patch.object(asyncio, "open_connection",
                          side_effect=AssertionError("UNSEEN_RECORD_MUST_NOT_DIAL")) as dial:
            with self.assertRaisesRegex(ValueError, "DELTA_CANDIDATE_NOT_RETURNED_BY_ORIGINATING_SEARCH"):
                await client.resolve("peer0", held.record)
        self.assertFalse(dial.called)
        self.assertEqual(client._budget.used["requests"], 4)
        self.assertEqual(client._budget.used["reply_bytes"], 262144)
        self.failed(client)

    async def test_real_loopback_unknown_id_offer_candidate_and_structural_resolve(self):
        remote, held = self.workspace(populated=True)
        provider = CompositeProvider(index=remote.index, custody=remote.modules,
            packets=remote.packets, max_connections=2, max_requests=4,
            max_reply_bytes=32*MIB, operation_ms=1000)
        self.providers.append(provider)
        endpoint = await provider.start("127.0.0.1", 0)
        client = self.client()
        contacts, policy = self.contacts((endpoint.port,))
        self.bind(client, contacts=contacts, policy=policy)
        offer = await client.search_offer("peer0", 65536, max_expanded_bytes=131072)
        self.assertEqual(offer["status"], "OFFERED")
        self.assertFalse(offer["mathematical_acceptance"] or offer["global_complete"])
        # Select only from authenticated returned metadata; no expected ID or
        # partition is supplied to bind, the formal query or page selection.
        partitions = [row for row in offer["partitions"] if row["anchor_count"] > 0]
        self.assertEqual(len(partitions), 1)
        found = await client.search_page("peer0", offer["snapshot_id"],
            partitions[0]["partition"], 0, deepcopy(PAGE), candidates_only=True)
        self.assertEqual(len(found["new_matches"]), 1)
        record = found["new_matches"][0]
        self.assertEqual(record, held.record)
        token = await client.resolve("peer0", record)
        self.assertIs(type(token), Candidate)
        resolved = client.describe_candidate(token)
        self.assertEqual(resolved["opening"], held.opening)
        self.assertEqual(resolved["locator"]["module_id"], held.module)
        self.assertFalse(resolved["mathematical_acceptance"])
        self.assertEqual(client.workspace.modules.get_group(held.module, held.name)[0], held.opening)
        self.assertEqual(provider.requests, 3)
        self.assertEqual(provider.failures, 0)
        self.assertEqual(client._search.session.used["requests"], 2)
        self.assertEqual(client._budget.used["requests"], 5)
        self.assertEqual(len(client._budget.external), 1)
        self.assertIs(client._acquisition._search, client._search)
        self.assertIsNone(client._handoff)
        self.assertIsNone(client._channel)
        self.no_verification(client)
        OBSERVED["real_loopback_requests"] += provider.requests
        OBSERVED["resolved_structural_candidates"] += 1
        closed = await client.close()
        self.assertEqual(closed["status"], "CLOSED")
        self.assertTrue(closed["closed"])
        await provider.stop()
        self.assertIsNone(provider.server)
        self.assertFalse(provider.tasks)


SELECTED = (
    "test_bind_prepays_original_budget_and_copies_owner_choices_without_io",
    "test_exact_client_endpoint_policy_and_duplicates_are_required",
    "test_missing_or_disagreeing_adopted_source_pin_refuses_before_prepay",
    "test_second_bind_and_existing_query_never_renew_original_allowance",
    "test_search_prepayment_cannot_exceed_original_requests_bytes_or_provider_cap",
    "test_acquisition_contact_guard_rejects_disconnected_originating_search",
    "test_expired_contact_refuses_search_and_acquisition_without_renewal",
    "test_record_not_returned_by_bound_search_cannot_be_resolved",
    "test_real_loopback_unknown_id_offer_candidate_and_structural_resolve",
)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_DIRECT_CONTROLS")
    OUTPUT = Path(args.output)
    F.need(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT
           and OUTPUT.is_relative_to(PROJECT/"experiments") and not OUTPUT.exists()
           and OUTPUT.parent.is_dir(), "FRESH_DIRECT_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.TestSuite(DirectControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = [{"name": name, **pin(Path(module.__file__))}
               for name, module in sorted(sys.modules.items())
               if getattr(module, "__file__", None) and Path(module.__file__).is_relative_to(SOURCE)]
    report = {
        "status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "selected": list(SELECTED), "imports": imports,
        "scope": "REAL_DIRECT_SEARCH_CUSTODY_BUDGETS_WITH_EXPLICITLY_INERT_ISSUERS_AND_LIVENESS",
        "mathematical_acceptance": False, "real_aggregate_checks": 0, "real_native_checks": 0,
        "proof_calls": 0, "subprocess_calls": 0, "public_network_calls": 0,
        "fixture_observations": dict(OBSERVED),
    }
    with (OUTPUT/"RESULT.json").open("xb") as stream:
        stream.write(encoded(report))
    print(encoded(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
