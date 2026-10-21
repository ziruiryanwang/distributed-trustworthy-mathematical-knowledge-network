"""Finite query-generation controls with explicitly INERT mathematical owners.

Real structural stores, provider dispatch, search authentication and acquisition
are exercised in memory. Issuer construction/liveness/census and parent report
are fixture substitutes. No socket, native check, proof or mathematical warrant.
"""
import asyncio
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / "portable_runtime"), str(SOURCE)]


def overlay(name, relative):
    parent = importlib.import_module(name.rsplit(".", 1)[0])
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(parent, name.rsplit(".", 1)[1], module)
    return module


F = overlay("discovery.formal_features", "type_pattern/discovery/formal_features.py")
TP = overlay("discovery.type_pattern", "type_pattern/discovery/type_pattern.py")
overlay("discovery.authenticated_index", "type_pattern/discovery/authenticated_index.py")
overlay("discovery.discovery_store", "type_pattern/discovery/discovery_store.py")
EA = overlay("discovery.module_export_adapter", "type_pattern/discovery/module_export_adapter.py")
overlay("modules.source_rows", "nat_literals/source_rows.py")
overlay("admission.pin_phase", "runtime_efficient/admission/pin_phase.py")
overlay("admission.trust", "trust_withdrawal/admission/trust.py")
overlay("admission.verifier", "trust_withdrawal/admission/verifier.py")
overlay("aggregate_claims.aggregate_admission", "trust_withdrawal/aggregate_claims/aggregate_admission.py")
overlay("mixed_claims.receiver", "runtime_efficient/mixed_claims/receiver.py")
overlay("mixed_claims.imports_atomic", "interface_views/imports_atomic.py")
overlay("mixed_claims.interface_projection", "interface_views/projection.py")
overlay("mixed_claims.authoring_atomic", "interface_views/authoring_atomic.py")
overlay("transport.semantic_staging", "interface_views/semantic_staging.py")
ET = overlay("evidence_network.transport", "iterative_queries/evidence_network/transport.py")
WA = overlay("client.workspace_atomic", "conjunction_index/client/workspace_atomic.py")
WE = overlay("client.workspace_evidence", "type_pattern/client/workspace_evidence.py")
WS = overlay("client.workspace_staged", "interface_views/workspace_staged.py")
WV = overlay("client.workspace_validated", "iterative_queries/client/workspace_validated.py")
D = overlay("client.direct_contacts", "iterative_queries/client/direct_contacts.py")
SR = overlay("client.semantic_reader", "iterative_queries/client/semantic_reader.py")
from client import test_direct_contacts as T
from client import test_workspace_evidence as TE
from delta import transport as DT
from modules import codec as C
from transport import clients as TC, search_resilience as R

OUTPUT = None
OBSERVED = {}
ADDITIVE = ("providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes")
SMALL = dict(providers=1, snapshots=1, requests=1, pages=1, examined=1,
             candidates=1, bytes=1024, wall_ms=30000, inflight=1)
QUERY = dict(providers=1, snapshots=1, requests=2, pages=1, examined=8,
             candidates=4, bytes=131072, wall_ms=30000, inflight=1)
TYPE_A = ["sort", ["zero"]]
TYPE_B = ["forall", "default", ["sort", ["zero"]], ["sort", ["zero"]]]


def envelope(query=QUERY, count=2):
    return {**query, **{key: query[key]*count for key in ADDITIVE}, "generations": count}


def specs(typ=TYPE_A):
    return [{"tag": "declaration-kind", "value": "theorem"},
            TP.pattern_spec(C, "11"*32, 0, deepcopy(typ))]


class IterativeControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.workspaces, self.clients, self.providers = [], [], []
        for cls, name, replacement in (
            (WS.CommonsClient, "_active", T.inert_active),
            (WV.CommonsClient, "_census", lambda client: {"scope": "INERT_CENSUS"}),
            # Keep the NEW iterative report itself real; only its unchanged
            # superclass report would otherwise ask inert owners for authority.
            (WS.CommonsClient, "report", T.inert_report),
        ):
            guard = patch.object(cls, name, replacement)
            guard.start()
            self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        for client in reversed(self.clients):
            if not client._closed:
                await client.close()
        for workspace in reversed(self.workspaces):
            if not workspace._closed:
                workspace.close()

    contacts = T.DirectControls.contacts

    def workspace(self, *, populated=False):
        self.assertFalse(populated)
        config = T.configuration()
        config.update(schema=WE.TYPE_PATTERN_SCHEMA,
                      discovery_profile={"schema": EA.PATTERN_PROFILE_SCHEMA})
        workspace = WV.Workspace.open(self.root/("workspace-"+str(len(self.workspaces))),
                                      config, create=True)
        self.workspaces.append(workspace)
        return workspace, None

    def client(self):
        # Reuse only fixture construction, never its old tests or claims.
        client = T.DirectControls.client(self)
        client._query_envelope = client._origin_query_envelope = None
        return client

    def reserve(self, client, chosen=None, policy=None):
        if policy is None:
            unused, policy = self.contacts()
        return D.reserve_queries(client, deepcopy(envelope() if chosen is None else chosen), policy)

    def next(self, client, typ=TYPE_A, *, contacts=None, limits=None):
        if contacts is None:
            contacts, unused = self.contacts()
        return D.next_query(client, contacts, specs(typ), deepcopy(QUERY if limits is None else limits))

    def selected(self, workspace, label, typ):
        name = [["s", label]]
        spec = {"schema": C.SPEC_SCHEMA, "foundation": T.B.FOUNDATION, "policy": T.B.POLICY,
            "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem", "name": name,
                "universes": 0, "type": deepcopy(typ), "value_hash": None, "meta": {}}]}]}
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        workspace.modules.put_group(module, opening)
        raw = workspace.adapter.encode_opening(module, name, opening)
        record = workspace.adapter.describe(raw)["record"]
        workspace.index.admit(raw, expected_id=record["object_id"])
        # Both old fixtures use explicitly synthetic images. Select the same
        # inert image on both sides; do not relax real packet/profile checking.
        with patch.object(TE.T, "IMAGE", T.IMAGE):
            packet, exact = TE.terminal(spec)
        workspace.packets.put(module, packet)
        return {"module": module, "name": name, "opening": opening,
                "record": record, "packet": packet, "exact": exact}

    def dispatch(self, workspace):
        provider = ET.CompositeProvider(index=workspace.index, custody=workspace.modules,
                                         packets=workspace.packets)
        calls = []

        async def exchange(endpoint, route, request, maximum, timeout):
            endpoint.validate()  # Preserve the direct binding's predial guard.
            calls.append(route)
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else C.canonical(value)
            F.need(len(raw) <= maximum, "INERT_DISPATCH_REPLY_BOUND")
            return {"status": 200, "raw": raw, "request_bytes": len(C.canonical(request)),
                    "reply_bytes": len(raw), "header_bytes": 0, "elapsed_ms": 0}

        return exchange, calls

    async def discover(self, client):
        offer = await client.search_offer("peer0", 65536, max_expanded_bytes=131072)
        self.assertEqual(offer["status"], "OFFERED")
        partitions = [item for item in offer["partitions"] if item["anchor_count"]]
        self.assertEqual(len(partitions), 1)
        page = await client.search_page("peer0", offer["snapshot_id"],
            partitions[0]["partition"], 0, deepcopy(T.PAGE), candidates_only=True)
        self.assertEqual(len(page["new_matches"]), 1)
        return await client.resolve("peer0", page["new_matches"][0])

    async def test_two_distinct_queries_real_structural_acquisition(self):
        remote, unused = self.workspace()
        first = self.selected(remote, "first-unproved", TYPE_A)
        second = self.selected(remote, "second-unproved", TYPE_B)
        client = self.client()
        budget, grant, owners = client._budget, client.grant, client._origin_owners
        # Identity marker only: NOT a LiveWarrant, never admitted/described/used.
        marker = object()
        client._warrants[marker] = "INERT_RETENTION_MARKER_NOT_MATHEMATICAL_AUTHORITY"
        first_contacts, policy = self.contacts((21001,), approved=(21001, 21002))
        second_contacts, unused_policy = self.contacts((21002,))
        self.reserve(client, policy=policy)
        search_deadline = client._query_envelope.deadline
        prepaid = deepcopy(budget.used)
        self.next(client, contacts=first_contacts)
        old_search, old_acquisition = client._search, client._acquisition
        old_contact = old_acquisition.endpoints["peer0"]
        exchange, calls = self.dispatch(remote)
        with patch.object(R, "_exchange", exchange), patch.object(TC, "exchange", exchange), \
             patch.object(DT, "exchange", exchange):
            a = await self.discover(client)
            self.assertEqual(client.describe_candidate(a)["locator"]["module_id"], first["module"])
            helper = SR.SemanticReader(client, a,
                limits=dict(modules=8, names=8, groups=8, bodies=8, steps=32, data_bytes=65536))
            offers = await client.packet_offers(a)
            staged = await client.stage_packet(a, offers["packets"][0])
            before = deepcopy(budget.used)
            self.next(client, TYPE_B, contacts=second_contacts)
            self.assertNotEqual(old_search.endpoints["peer0"], client._search.endpoints["peer0"])
            self.assertEqual(budget.used, before)
            self.assertIs(client._budget, budget)
            self.assertIs(client.grant, grant)
            self.assertEqual(client._query_envelope.deadline, search_deadline)
            self.assertLessEqual(client._search.session.deadline, search_deadline)
            self.assertEqual(client._origin_owners, owners)
            self.assertIn(marker, client._warrants)
            self.assertEqual(client._staging_counts["packets_staged"], 1)
            self.assertNotIn(staged, client._staged)
            self.assertNotIn(a, client._candidates)
            with self.assertRaises(ValueError): old_search.session.begin_offer("old", 1024)
            with self.assertRaises(ValueError): old_contact.validate()
            with self.assertRaises(ValueError): await old_acquisition.declaration("peer0", first["module"], first["name"], 65536)
            with self.assertRaises(ValueError): helper.preview()
            helper.close()
            b = await self.discover(client)
            self.assertEqual(client.describe_candidate(b)["locator"]["module_id"], second["module"])
        self.assertNotEqual(old_search.session.features, client._search.session.features)
        self.assertEqual(client.workspace.modules.get_group(first["module"], first["name"])[0], first["opening"])
        self.assertEqual(client.workspace.modules.get_group(second["module"], second["name"])[0], second["opening"])
        self.assertEqual(len(budget.external), 1)
        self.assertEqual(budget.external[0]["label"], "direct-query-envelope")
        self.assertEqual(budget.used["requests"], prepaid["requests"]+4)
        self.assertEqual(budget.used["verify_attempts"], 0)
        report = client.report()["iterative_queries"]
        self.assertEqual(len(report["generations"]), 2)
        self.assertEqual(report["allocated"], {key: QUERY[key]*2 for key in ADDITIVE})
        OBSERVED["two_query_structural_loop"] = {"dispatches": len(calls),
            "module_ids": [first["module"], second["module"]],
            "same_label_different_authorized_endpoints": [21001, 21002],
            "original_budget_preserved": True, "inert_marker_preserved": True,
            "mathematical_acceptance": False, "report": report}
        await client.close()
        self.assertTrue(budget.closed)
        self.assertTrue(all(owner is None or owner.closes == 1 for owner in owners))

    async def test_each_aggregate_dimension_exhausts_without_refund(self):
        for dimension in ADDITIVE:
            with self.subTest(dimension=dimension):
                client = self.client()
                plan = envelope(SMALL, 3)
                plan[dimension] = SMALL[dimension]*2
                self.reserve(client, plan)
                self.next(client, limits=SMALL)
                self.next(client, TYPE_B, limits=SMALL)
                before = deepcopy(client._budget.used)
                with self.assertRaises(ValueError): self.next(client, limits=SMALL)
                self.assertEqual(client._budget.used, before)
                self.assertEqual(len(client._budget.external), 1)
                self.assertEqual(client._state, "FAILED")
        OBSERVED["independent_consumptive_dimensions"] = list(ADDITIVE)

    async def test_generation_cap_fixed_deadline_and_inflight(self):
        client = self.client()
        self.reserve(client, envelope(SMALL, 1))
        original_deadline = client.grant.deadline
        self.next(client, limits=SMALL)
        fixed = client._search.session.deadline
        with self.assertRaises(ValueError): self.next(client, TYPE_B, limits=SMALL)
        self.assertEqual(client.grant.deadline, original_deadline)
        self.assertLessEqual(fixed, original_deadline)
        other = self.client()
        self.reserve(other, envelope(SMALL, 2))
        with self.assertRaises(ValueError): self.next(other, limits={**SMALL, "inflight": 2})
        self.assertEqual(other._budget.sequence, 0)
        OBSERVED["generation_and_fixed_inflight_caps"] = True

    async def test_pending_rotation_and_retired_close_cannot_close_shared_budget(self):
        for kind in ("search", "acquisition", "structural-inflight", "structural-reserved"):
            with self.subTest(kind=kind):
                client = self.client()
                self.reserve(client)
                self.next(client)
                acquisition, search = client._acquisition, client._search
                ticket = None
                if kind == "search": ticket = search.session.begin_offer("held", 1024)["ticket"]
                elif kind == "acquisition": ticket = client._budget.begin(1024)
                elif kind == "structural-inflight": acquisition.structural.inflight = 1
                else: acquisition.structural.reserved_bytes = 1024
                try:
                    with self.assertRaises(ValueError): self.next(client, TYPE_B)
                    self.assertEqual(client._state, "FAILED")
                finally:
                    # These are explicit no-task fixtures; settle their pending
                    # reservation after observing refusal, never restore a client.
                    if kind == "search" and ticket in search.session.pending: search.session.abandon(ticket)
                    if kind == "acquisition" and client._budget.pending is not None: client._budget.settle(ticket)
                    acquisition.structural.inflight = acquisition.structural.reserved_bytes = 0
        client = self.client()
        self.reserve(client)
        self.next(client)
        retired = client._acquisition
        self.next(client, TYPE_B)
        ticket = client._budget.begin(1024)
        retired.close()
        self.assertFalse(client._budget.closed)
        self.assertEqual(client._budget.pending[0], ticket)
        client._budget.settle(ticket)
        OBSERVED["quiescence_and_retired_close"] = True

    async def test_retirement_failure_stays_charged_and_fail_stops(self):
        client = self.client()
        self.reserve(client)
        self.next(client)
        budget, acquisition = client._budget, client._acquisition
        before = deepcopy(budget.used)
        with patch.object(acquisition, "retire_generation", side_effect=OSError("INERT_RETIRE_FAILURE")):
            with self.assertRaisesRegex(OSError, "INERT_RETIRE_FAILURE"):
                self.next(client, TYPE_B)
        self.assertEqual(client._state, "FAILED")
        self.assertIs(client._budget, budget)
        self.assertEqual(budget.used, before)
        self.assertEqual(len(budget.external), 1)
        self.assertFalse(client._busy)
        self.assertEqual(client.report()["iterative_queries"]["status"], "FAILED")
        await client.close()
        self.assertEqual(client.report()["iterative_queries"]["status"], "FAILED")
        OBSERVED["retirement_failure_no_renewal"] = True

    async def test_diagnostic_close_failure_still_closes_original_owners(self):
        client = self.client()
        self.reserve(client)
        self.next(client)
        selected, budget, owners = client._query_envelope, client._budget, client._origin_owners
        with patch.object(selected, "terminal", side_effect=OSError("INERT_TERMINAL_DIAGNOSTIC")):
            report = await client.close()
        self.assertTrue(client._closed and budget.closed)
        self.assertTrue(all(owner is None or owner.closes == 1 for owner in owners))
        self.assertTrue(client._cleanup_uncertain and client.workspace._poisoned)
        self.assertEqual(report["status"], "CLEANUP_INCOMPLETE")
        self.assertTrue(any(item.startswith("query_cleanup:") for item in client._failures))
        OBSERVED["diagnostic_error_does_not_skip_mandatory_cleanup"] = True

    async def test_partial_new_acquisition_failure_retains_full_allocation(self):
        client = self.client()
        self.reserve(client)
        self.next(client)
        budget, old_search = client._budget, client._search
        owners, before = client._origin_owners, deepcopy(client._budget.used)
        with patch.object(D, "EvidenceAcquisition", side_effect=OSError("INERT_ACQUISITION_CONSTRUCTOR")):
            with self.assertRaisesRegex(OSError, "INERT_ACQUISITION_CONSTRUCTOR"):
                self.next(client, TYPE_B)
        self.assertEqual(client._state, "FAILED")
        self.assertIs(client._budget, budget)
        self.assertEqual(budget.used, before)
        self.assertEqual(len(budget.external), 1)
        self.assertTrue(budget.closed)
        self.assertTrue(all(owner is None or owner.closes == 1 for owner in owners))
        self.assertFalse(client._busy)
        self.assertIsNot(client._search, old_search)
        self.assertIsNone(client._acquisition)
        self.assertEqual(old_search.session.state, "RETIRED")
        self.assertEqual(client._search.session.state, "CLIENT_FAILED")
        report = client.report()["iterative_queries"]
        self.assertEqual(report["status"], "FAILED")
        self.assertEqual(report["allocated"], {key: QUERY[key]*2 for key in ADDITIVE})
        self.assertEqual([row["status"] for row in report["generations"]], ["RETIRED", "FAILED"])
        OBSERVED["partial_new_acquisition_fail_stop"] = report

    async def test_stale_candidate_and_staged_public_actions_refuse(self):
        for kind in ("candidate", "stage"):
            client = self.client()
            self.reserve(client)
            self.next(client)
            if kind == "candidate":
                token = WA.Candidate()
                client._candidates[token] = "peer0", {"INERT": True}
            else:
                token = WS.StagedEvidence()
                client._staged[token] = C.canonical({"INERT": True}), False
            self.next(client, TYPE_B)
            method = client.describe_candidate if kind == "candidate" else client.describe_staged
            with self.assertRaisesRegex(ValueError, "FOREIGN_CANDIDATE|FOREIGN_STAGED_EVIDENCE"):
                method(token)
            self.assertEqual(client._state, "FAILED")
        OBSERVED["old_lookup_capabilities_refuse"] = True

    async def test_late_reservation_legacy_bind_and_located_slot_do_not_reset(self):
        client = self.client()
        ticket = client._budget.begin(1024)
        client._budget.settle(ticket)
        with self.assertRaises(ValueError): self.reserve(client)
        self.assertEqual(client._budget.external, [])
        for kind in ("legacy-first", "envelope-first", "located-slot"):
            client = self.client()
            contacts, policy = self.contacts()
            if kind == "legacy-first":
                D.bind(client, contacts, specs(), policy, deepcopy(QUERY))
                self.assertNotIn("iterative_queries", client.report())
                before = deepcopy(client._budget.used)
                with self.assertRaises(ValueError): self.reserve(client)
            elif kind == "envelope-first":
                self.reserve(client, policy=policy)
                before = deepcopy(client._budget.used)
                with self.assertRaises(ValueError): D.bind(client, contacts, specs(), policy, deepcopy(QUERY))
            else:
                client._query_used = True  # Existing located-query slot fixture.
                before = deepcopy(client._budget.used)
                with self.assertRaises(ValueError): self.reserve(client)
            self.assertEqual(client._budget.used, before)
            self.assertEqual(client._state, "FAILED")
        OBSERVED["legacy_and_preallocation_guards"] = True


SELECTED = (
    "test_two_distinct_queries_real_structural_acquisition",
    "test_each_aggregate_dimension_exhausts_without_refund",
    "test_generation_cap_fixed_deadline_and_inflight",
    "test_pending_rotation_and_retired_close_cannot_close_shared_budget",
    "test_retirement_failure_stays_charged_and_fail_stops",
    "test_diagnostic_close_failure_still_closes_original_owners",
    "test_partial_new_acquisition_failure_retains_full_allocation",
    "test_stale_candidate_and_staged_public_actions_refuse",
    "test_late_reservation_legacy_bind_and_located_slot_do_not_reset",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output/"iterative-fixtures"
    OUTPUT.mkdir()
    suite = unittest.TestSuite(IterativeControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "open_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")), \
         patch.object(socket, "create_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "REAL_STRUCTURAL_QUERY_LIFECYCLE_IN_MEMORY_DISPATCH_INERT_ISSUERS",
        "mathematical_acceptance": False, "proof_calls": 0, "native_calls": 0,
        "network_operations": 0, "inert_retention_markers_are_warrants": False}
    with (output/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())
