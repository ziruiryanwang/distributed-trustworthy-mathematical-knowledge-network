"""Focused structural-staging controls; all mathematical receivers are INERT.

Actual pure preview, structural parsers/stores, grants and facade methods run.
The imported predecessor fixtures supply constructors/data only: no old suite
runs. Exact issuer objects use explicitly fabricated receive methods; transport
is in-process provider dispatch, not a network. No synthetic result is real A.
"""
import argparse
import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from authoring.context import DEFAULT_LIMITS
from client import test_workspace_evidence as E
from client import test_workspace_mixed as T
from client import workspace_staged as W
from client.workspace_atomic import LiveWarrant
from delta import transport as DT
from delta_claims.claims import expected_journal
from discovery import formal_features as F
from evidence_network.custody import public_profile
from evidence_network.transport import CompositeProvider, EvidenceAcquisition
from modules import codec as C
from transport import clients as TC, semantic_staging as S

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
FOUNDATION_SIZE = 23313
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
FOUNDATION = None
OUTPUT = None
OBSERVED = {"synthetic_receiver_calls": 0, "inert_dispatch_calls": 0}


def sha(raw): return hashlib.sha256(raw).hexdigest()


def staged(spec, rank=0):
    raw, exact = E.terminal(spec, rank)
    return {"module": C.module_id(spec), "journal": list(exact), "summary": C.summarize(spec),
            "packet_sha256": sha(raw), "packet_bytes": len(raw)}


def dependency():
    base, body = E.definitions()
    target = T.spec("usesAlpha")
    target["groups"][0]["declarations"][0]["type"] = [
        "const", ["external", C.module_id(base), [["s", "alpha"]]], []]
    opening = {"module": C.module_id(base), "opening": C.group_opening(base, 0)}
    value = {"module": C.module_id(base), "universes": body["universes"], "expression": body["expression"]}
    return base, target, opening, value


def preview(records, groups, bodies, **kwargs):
    return S.preview(records, groups, bodies, FOUNDATION, FOUNDATION_SHA, **kwargs)


class ExpiringInertEndpoint:
    label = "inert-expiring-provider-no-socket"
    def __init__(self): self.expired = False
    def validate(self):
        if self.expired: raise ValueError("TEST_INERT_CONTACT_EXPIRED")


class StagingControls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2)); self.root.mkdir()
        self.workspaces, self.clients, self.owners = [], [], []

    def tearDown(self):
        for client in reversed(self.clients):
            if not client._closed: asyncio.run(client.close())
        for owners in reversed(self.owners):
            OBSERVED["synthetic_receiver_calls"] += sum(owners.receives.values())
            owners.close()
        for workspace in reversed(self.workspaces):
            if not workspace._closed: workspace.close()

    def operation(self, name, *, max_sources=8):
        workspace = W.Workspace.open(self.root/name, E.configuration(), create=True)
        self.workspaces.append(workspace)
        limits = T.grant_limits(); limits["imports"]["max_sources"] = max_sources
        grant = workspace.reserve(limits)
        owners = T.SyntheticOwners(grant, workspace._envelope); self.owners.append(owners)
        # These are fixture pins, not adopted real-owner construction evidence.
        for relative in ("client/workspace_evidence.py", "client/workspace_resilient.py",
                         "client/workspace_staged.py", "transport/search_resilience.py",
                         "transport/semantic_staging.py", "evidence_network/__init__.py",
                         "evidence_network/packet.py", "evidence_network/custody.py",
                         "evidence_network/transport.py"):
            path = SOURCE/relative; raw = path.read_bytes()
            for owner in (owners.aggregate, owners.delta):
                owner._pins[path] = {"bytes": len(raw), "sha256": sha(raw)}
        client = workspace.operation(grant, aggregate_owner=owners.aggregate,
            delta_owner=owners.delta, foundation_bytes=FOUNDATION, foundation_sha256=FOUNDATION_SHA)
        self.clients.append(client)
        return workspace, client, owners

    def seed(self, workspace, spec, raw, bodies=()):
        module = C.module_id(spec)
        for index in range(len(spec["groups"])):
            workspace.modules.put_group(module, C.group_opening(spec, index))
        for body in bodies:
            workspace.modules.put_body(module, body["relative_name"], body)
        workspace.packets.put(module, raw)

    def dispatch(self, source, target, client):
        provider = CompositeProvider(index=source.index, custody=source.modules, packets=source.packets)
        endpoint = ExpiringInertEndpoint()
        client._acquisition = EvidenceAcquisition(target.adapter, {"p": endpoint}, public_profile(T.IMAGE),
            client._budget, target.modules, target.packets)
        client._search = E.SyntheticSearch()
        calls = []
        async def exchange(actual, route, request, maximum, timeout):
            actual.validate()
            calls.append((route, deepcopy(request))); OBSERVED["inert_dispatch_calls"] += 1
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else C.canonical(value)
            if len(raw) > maximum: raise ValueError("TEST_REPLY_BOUND")
            return {"status": 200, "raw": raw, "request_bytes": len(C.canonical(request)),
                    "reply_bytes": len(raw), "header_bytes": 0, "elapsed_ms": 0}
        return endpoint, calls, exchange

    async def stage(self, client, workspace, spec):
        module = C.module_id(spec); name = spec["groups"][0]["declarations"][0]["name"]
        record = workspace.adapter.describe(workspace.adapter.encode_opening(
            module, name, C.group_opening(spec, 0)))["record"]
        candidate = await client.resolve("p", record)
        offers = await client.packet_offers(candidate, max_offers=2, max_bytes=4096)
        self.assertTrue(offers["packets"])
        token = await client.stage_packet(candidate, offers["packets"][0])
        return token, candidate, offers["packets"][0]

    def pair(self, spec, *, raw=None, max_sources=8):
        source, publisher, unused = self.operation("s")
        target, client, owners = self.operation("t", max_sources=max_sources)
        if raw is None: raw, unused_exact = E.terminal(spec)
        self.seed(source, spec, raw)
        endpoint, calls, exchange = self.dispatch(source, target, client)
        with patch.object(DT, "exchange", exchange), patch.object(TC, "exchange", exchange):
            token, candidate, entry = asyncio.run(self.stage(client, source, spec))
        return source, target, client, owners, token, candidate, entry, endpoint, calls, exchange

    def output_is_data_only(self, value):
        self.assertEqual(set(value), {"status", "demands", "cost", "mathematical_acceptance"})
        self.assertFalse(value["mathematical_acceptance"])
        self.assertNotIn("packet", value); self.assertNotIn("selection_binding", value)
        self.assertNotIn("context", value)
        self.assertEqual(set(value["cost"]), {
            "preview_calls", "staged_modules", "supplied_groups", "supplied_bodies",
            "input_json_values", "serialized_input_bytes", "groups", "declarations",
            "counted_expression_visits", "context_selected_input_bytes", "projected_frontend_packet_bytes",
            "frontend_theorem_ancestor_proof_bytes", "fixed_foundation_proof_bodies_included",
            "expression_counter_is_not_total_cpu_work", "cumulative_operation_budget_required"})
        self.assertEqual(value["cost"]["frontend_theorem_ancestor_proof_bytes"], 0)
        self.assertEqual(value["cost"]["preview_calls"], 1)
        for key in ("fixed_foundation_proof_bodies_included", "expression_counter_is_not_total_cpu_work",
                    "cumulative_operation_budget_required"):
            self.assertIs(value["cost"][key], True)

    def test_actual_preview_progresses_evidence_declaration_body_then_closure(self):
        base, target, opening, body = dependency()
        target_opening = {"module": C.module_id(target), "opening": C.group_opening(target, 0)}
        selected, groups = [staged(target, 1)], [target_opening]
        one = preview(selected, groups, [])
        self.output_is_data_only(one)
        self.assertEqual(one["status"], "NEED_STRUCTURAL_CONTEXT_DATA")
        self.assertEqual(one["demands"], [{"kind": "NeedModuleEvidence", "module": C.module_id(base),
                                          "name": [["s", "alpha"]]}])
        selected.append(staged(base))
        two = preview(selected, groups, [])
        self.assertEqual(two["demands"], [{"kind": "NeedDeclaration", "module": C.module_id(base),
                                          "name": [["s", "alpha"]]}])
        groups.append(opening)
        three = preview(selected, groups, [])
        self.assertEqual(three["demands"], [{"kind": "NeedBody", "module": C.module_id(base),
            "name": [["s", "alpha"]], "universes": 0, "body_hash": C.body_id(body["expression"], 0)}])
        four = preview(selected, groups, [body])
        self.output_is_data_only(four)
        self.assertEqual(four["status"], "STRUCTURAL_CLOSURE_STAGED"); self.assertEqual(four["demands"], [])
        # No theorem proof/receipt is available to this pure planner at all.
        self.assertEqual(len(groups), 2); self.assertEqual(len([body]), 1)
        self.assertEqual(OBSERVED["synthetic_receiver_calls"], 0)

    def test_preview_rejects_missing_evidence_variant_and_uncommitted_semantics(self):
        base, target, opening, body = dependency()
        target_opening = {"module": C.module_id(target), "opening": C.group_opening(target, 0)}
        records, groups = [staged(target, 1), staged(base)], [target_opening, opening]
        mutations = []
        mutations.append(([records[0]], groups, [body]))  # Opening has no exact staged packet record.
        mutations.append((records+[staged(base, 2)], groups, [body]))  # Same ModuleID, another whole-J.
        duplicate = deepcopy(records); duplicate.append(deepcopy(records[1]))
        mutations.append((duplicate, groups, [body]))
        # Rank is deliberately unrestricted structural data; mutate ModuleID,
        # not a rank byte, to test an actually broken journal commitment.
        changed = deepcopy(records); changed[1]["journal"][108] ^= 1
        mutations.append((changed, groups, [body]))
        changed = deepcopy(records); changed[1]["summary"] = records[0]["summary"]
        mutations.append((changed, groups, [body]))
        changed = deepcopy(body); changed["universes"] = 1
        mutations.append((records, groups, [changed]))
        changed = deepcopy(body); changed["expression"] = ["sort", ["succ", ["zero"]]]
        mutations.append((records, groups, [changed]))
        changed = deepcopy(body); changed["expression"] = ["not-an-expression"]
        mutations.append((records, groups, [changed]))
        mutations.append((records, groups+[deepcopy(opening)], [body]))
        mutations.append((records, groups, [body, deepcopy(body)]))
        for index, (selected, openings, bodies) in enumerate(mutations):
            with self.subTest(case=index), self.assertRaises(ValueError): preview(selected, openings, bodies)

    def test_preview_finite_limits_foundation_and_no_authority_output(self):
        spec = T.spec("opaqueProofNotAvailable")
        records = [staged(spec)]; groups = [{"module": C.module_id(spec), "opening": C.group_opening(spec, 0)}]
        value = preview(records, groups, [])
        self.output_is_data_only(value); self.assertEqual(value["status"], "STRUCTURAL_CLOSURE_STAGED")
        for key, amount in (("data_bytes", 1024), ("expression_visits", 1)):
            with self.subTest(limit=key), self.assertRaises(ValueError):
                preview(records, groups, [], limits={**DEFAULT_LIMITS, key: amount})
        with self.assertRaises(ValueError):
            S.preview(records, groups, [], FOUNDATION, "00"*32)
        with self.assertRaises(ValueError):
            S.preview(records, groups, [], b"SYNTHETIC-INVALID-FOUNDATION", sha(b"SYNTHETIC-INVALID-FOUNDATION"))
        wrong = deepcopy(records); wrong[0]["packet_bytes"] = 0
        with self.assertRaises(ValueError): preview(wrong, groups, [])
        wrong = deepcopy(records); wrong[0]["mathematical_acceptance"] = True
        with self.assertRaises(ValueError): preview(wrong, groups, [])
        with self.assertRaisesRegex(ValueError, "STAGING_OPENING_LIST"):
            preview(records, [], [])
        with self.assertRaisesRegex(ValueError, "STAGING_EVIDENCE_LIST"):
            preview(records*(S.MAX_STAGED+1), groups, [])
        # The finite-data pass must refuse before serialization or walker work.
        cycle = []; cycle.append(cycle)
        deep = []
        for unused in range(S.MAX_INPUT_DEPTH+1): deep = [deep]
        for label, raw in (("cycle", cycle), ("depth", deep), ("integer", [2**64]),
                           ("object", [object()]),
                           ("string", ["x"*(C.DEFAULT_LIMITS.max_string_bytes+1)])):
            with self.subTest(bound=label), self.assertRaises(ValueError):
                S._bounded_json(raw, DEFAULT_LIMITS["data_bytes"])
        # Finite census equals canonical bytes, including Unicode and escapes.
        data = {"z": [True, False, None, 184, "\u03b1\n"], "a": {"q\"": "\\"}}
        self.assertEqual(S._bounded_json(data, 4096)[0], len(C.canonical(data)))

    def test_stage_is_not_warrant_and_local_transition_needs_no_live_contact(self):
        spec = T.spec("localAfterStage")
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec)
        grant, deadline, budget = client.grant, client.grant.deadline, deepcopy(client._budget.used)
        report = client.describe_staged(token)
        self.assertIs(type(token), W.StagedEvidence); self.assertNotIsInstance(token, LiveWarrant)
        self.assertFalse(report["mathematical_acceptance"] or report["admission_consumed"])
        self.assertEqual(report["selection"], staged(spec))
        self.assertEqual(client._warrants, {}); self.assertEqual(sum(owners.receives.values()), 0)
        self.assertEqual(budget["verify_attempts"], 0)
        endpoint.expired = True; count = len(calls)
        with patch.object(DT, "exchange", exchange), patch.object(TC, "exchange", exchange):
            warrant = client.admit_staged(token, expected_exact_journal=bytes(report["selection"]["journal"]),
                                          receipt_cpu_seconds=10)
        # The receiver call here is deliberately fabricated by SyntheticOwners.
        self.assertIs(type(warrant), LiveWarrant); self.assertEqual(owners.receives, {"I": 0, "A": 1, "mixed": 0})
        self.assertEqual(len(calls), count); self.assertIs(client.grant, grant)
        self.assertEqual(client.grant.deadline, deadline)
        self.assertEqual(client._budget.used["requests"], budget["requests"])
        self.assertEqual(client._budget.used["verify_attempts"], 1)
        self.assertTrue(client.describe_staged(token)["admission_consumed"])
        with self.assertRaisesRegex(ValueError, "CLIENT_STAGED_ALREADY_CONSUMED"):
            client.admit_staged(token, receipt_cpu_seconds=10)
        self.assertEqual(owners.receives["A"], 1); self.assertEqual(client._staged, {})

    def test_foreign_failure_and_close_revoke_staged_tokens(self):
        spec = T.spec("lifetime")
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec)
        other_workspace, other, other_owners = self.operation("other")
        with self.assertRaisesRegex(ValueError, "CLIENT_FOREIGN_STAGED_EVIDENCE"):
            other.describe_staged(token)
        self.assertEqual(other._staged, {}); self.assertEqual(sum(other_owners.receives.values()), 0)
        with patch.object(owners.aggregate, "receive", side_effect=ValueError("SYNTHETIC_CHECKER_REFUSAL")):
            with self.assertRaisesRegex(ValueError, "SYNTHETIC_CHECKER_REFUSAL"):
                client.admit_staged(token, receipt_cpu_seconds=10)
        self.assertEqual(client._staged, {}); self.assertEqual(client._warrants, {})
        self.assertEqual(client._staging_counts["admission_transitions"], 1)
        self.assertEqual(client._budget.used["verify_attempts"], 1)
        self.assertTrue(owners.aggregate._closed and owners.delta._closed)
        # Separate fresh operation demonstrates ordinary close, not failure cleanup.
        target2, client2, owners2 = self.operation("closed")
        endpoint2, calls2, exchange2 = self.dispatch(source, target2, client2)
        with patch.object(DT, "exchange", exchange2), patch.object(TC, "exchange", exchange2):
            token2, unused, unused_entry = asyncio.run(self.stage(client2, source, spec))
        asyncio.run(client2.close())
        self.assertEqual(client2._staged, {}); self.assertNotIn(token2, client2._warrants)
        self.assertEqual(sum(owners2.receives.values()), 0)

    def test_duplicate_module_and_original_source_limit_refuse_without_transfer(self):
        spec = T.spec("variant")
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec)
        alternate, unused = E.terminal(spec, 2); source.packets.put(C.module_id(spec), alternate)
        async def duplicate():
            offers = await client.packet_offers(candidate, max_offers=2)
            changed = next(row for row in offers["packets"] if row != entry)
            before = len(calls)
            with self.assertRaisesRegex(ValueError, "CLIENT_STAGING_MODULE_ALREADY_SELECTED"):
                await client.stage_packet(candidate, changed)
            self.assertEqual(len(calls), before)
        with patch.object(DT, "exchange", exchange), patch.object(TC, "exchange", exchange): asyncio.run(duplicate())
        self.assertEqual(sum(owners.receives.values()), 0); self.assertEqual(client._staged, {})
        target2, capped, capped_owners = self.operation("cap", max_sources=1)
        endpoint2, calls2, exchange2 = self.dispatch(source, target2, capped)
        second = T.spec("otherModule"); raw, unused = E.terminal(second); self.seed(source, second, raw)
        async def capped_stage():
            await self.stage(capped, source, spec)
            module = C.module_id(second); name = second["groups"][0]["declarations"][0]["name"]
            record = source.adapter.describe(source.adapter.encode_opening(module, name, C.group_opening(second, 0)))["record"]
            next_candidate = await capped.resolve("p", record); offers = await capped.packet_offers(next_candidate)
            before = len(calls2)
            with self.assertRaisesRegex(ValueError, "CLIENT_STAGING_SOURCE_LIMIT"):
                await capped.stage_packet(next_candidate, offers["packets"][0])
            self.assertEqual(len(calls2), before)
        with patch.object(DT, "exchange", exchange2), patch.object(TC, "exchange", exchange2): asyncio.run(capped_stage())
        self.assertEqual(sum(capped_owners.receives.values()), 0)
        self.assertEqual(capped.grant.limits["imports"]["max_sources"], 1)

    def test_local_packet_or_group_change_refuses_before_receiver(self):
        spec = T.spec("readback")
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec)
        with patch.object(target.packets, "get", side_effect=ValueError("TEST_PACKET_MISSING")) as read:
            # Preview uses immutable staged identity and held semantic data,
            # not O(rounds * receipt_bytes) packet readback or live authority.
            opening = {"module": C.module_id(spec), "opening": C.group_opening(spec, 0)}
            forecast = client.preview_context([token], [opening], [])
            self.output_is_data_only(forecast)
            self.assertEqual(forecast["status"], "STRUCTURAL_CLOSURE_STAGED")
            self.assertEqual(read.call_count, 0); self.assertEqual(client._warrants, {})
            self.assertEqual(sum(owners.receives.values()), 0)
            with self.assertRaisesRegex(ValueError, "TEST_PACKET_MISSING"):
                client.admit_staged(token, receipt_cpu_seconds=10)
            self.assertEqual(read.call_count, 1)
        self.assertEqual(sum(owners.receives.values()), 0); self.assertEqual(client._staged, {})
        target2, client2, owners2 = self.operation("changed")
        endpoint2, calls2, exchange2 = self.dispatch(source, target2, client2)
        with patch.object(DT, "exchange", exchange2), patch.object(TC, "exchange", exchange2):
            second, unused, unused_entry = asyncio.run(self.stage(client2, source, spec))
        old_get = target2.modules.get_group
        def changed(*args):
            opening, descriptor = old_get(*args); descriptor = deepcopy(descriptor)
            descriptor["name"] = [["s", "corruptedLocalDescriptor"]]
            return opening, descriptor
        with patch.object(target2.modules, "get_group", changed):
            with self.assertRaisesRegex(ValueError, "CLIENT_STAGED_GROUP_CHANGED"):
                client2.admit_staged(second, receipt_cpu_seconds=10)
        self.assertEqual(sum(owners2.receives.values()), 0); self.assertEqual(client2._staged, {})

    def test_facade_preview_charges_repeated_work_and_requires_actual_custody(self):
        spec, body = E.definitions()
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec)
        opening = {"module": C.module_id(spec), "opening": C.group_opening(spec, 0)}
        before = client.report(); one = client.preview_context([token], [opening], [])
        middle = client.report(); two = client.preview_context([token], [opening], [])
        after = client.report()
        self.output_is_data_only(one); self.assertEqual(one, two)
        self.assertEqual(one["status"], "NEED_STRUCTURAL_CONTEXT_DATA")
        self.assertEqual(one["demands"][0]["kind"], "NeedBody")
        self.assertGreater(middle["submitted_input_bytes"], before["submitted_input_bytes"])
        self.assertGreater(after["submitted_input_bytes"], middle["submitted_input_bytes"])
        self.assertEqual(after["structural_staging"]["previews"], 2)
        self.assertEqual(client._warrants, {}); self.assertEqual(sum(owners.receives.values()), 0)
        row = {"module": C.module_id(spec), "universes": 0, "expression": body["expression"]}
        # A mathematically-shaped body argument is not enough: it was not held.
        with self.assertRaisesRegex(ValueError, "CUSTODY_BODY_NOT_FOUND"):
            client.preview_context([token], [opening], [row])
        self.assertEqual(client._staged, {}); self.assertEqual(sum(owners.receives.values()), 0)
        # Fresh operation acquires the actual body into custody before READY.
        response = deepcopy(body); response["relative_name"] = [["s", "alpha"]]
        source.modules.put_body(C.module_id(spec), response["relative_name"], response)
        target2, client2, owners2 = self.operation("held")
        endpoint2, calls2, exchange2 = self.dispatch(source, target2, client2)
        async def with_body():
            token2, candidate2, unused_entry = await self.stage(client2, source, spec)
            await client2.acquire_body(candidate2, response["body_hash"], max_bytes=4096)
            return token2
        with patch.object(DT, "exchange", exchange2), patch.object(TC, "exchange", exchange2):
            token2 = asyncio.run(with_body())
        endpoint2.expired = True; called = len(calls2)
        ready = client2.preview_context([token2], [opening], [row])
        self.output_is_data_only(ready)
        self.assertEqual(ready["status"], "STRUCTURAL_CLOSURE_STAGED")
        self.assertEqual(ready["demands"], []); self.assertEqual(len(calls2), called)
        self.assertEqual(sum(owners2.receives.values()), 0); self.assertEqual(client2._warrants, {})

    def test_structurally_staged_mixed_packet_never_runs_native_checker(self):
        raw, summary = T.mixed_packet(); spec = C.parse_json(raw)["deltas"][-1]["local_spec"]
        source, target, client, owners, token, candidate, entry, endpoint, calls, exchange = self.pair(spec, raw=raw)
        held = client.describe_staged(token)
        self.assertEqual(held["selection"]["summary"], summary)
        self.assertEqual(held["selection"]["journal"], list(expected_journal(summary, 1, T.B.RELATION_IMAGE)))
        self.assertFalse(held["mathematical_acceptance"])
        self.assertEqual(sum(owners.receives.values()), 0); self.assertEqual(client._warrants, {})
        self.assertEqual(client._budget.used["verify_attempts"], 0)
        with self.assertRaisesRegex(ValueError, "CLIENT_FOREIGN_WARRANT"):
            client.describe(token)
        self.assertEqual(client._staged, {}); self.assertEqual(sum(owners.receives.values()), 0)


SELECTED = (
    "test_actual_preview_progresses_evidence_declaration_body_then_closure",
    "test_preview_rejects_missing_evidence_variant_and_uncommitted_semantics",
    "test_preview_finite_limits_foundation_and_no_authority_output",
    "test_stage_is_not_warrant_and_local_transition_needs_no_live_contact",
    "test_foreign_failure_and_close_revoke_staged_tokens",
    "test_duplicate_module_and_original_source_limit_refuse_without_transfer",
    "test_local_packet_or_group_change_refuses_before_receiver",
    "test_facade_preview_charges_repeated_work_and_requires_actual_custody",
    "test_structurally_staged_mixed_packet_never_runs_native_checker",
)


def pin(path):
    raw = path.read_bytes(); return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def main():
    global FOUNDATION, OUTPUT
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    parser.add_argument("--foundation", required=True); args = parser.parse_args()
    F.need(Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
           and not sys.flags.optimize, "CANONICAL_ISOLATED_STAGING_CONTROLS")
    foundation = Path(args.foundation)
    F.need(foundation.is_absolute() and foundation.resolve() == foundation and foundation.is_file()
           and all(not p.is_symlink() and not p.is_junction() for p in (foundation, *foundation.parents))
           and foundation.stat().st_size == FOUNDATION_SIZE, "SELECTED_ORDINARY_FOUNDATION_INPUT")
    with foundation.open("rb") as stream: FOUNDATION = stream.read(FOUNDATION_SIZE+1)
    F.need(len(FOUNDATION) == FOUNDATION_SIZE and sha(FOUNDATION) == FOUNDATION_SHA, "EXACT_FOUNDATION_PIN")
    OUTPUT = Path(args.output)
    F.need(OUTPUT.is_absolute() and OUTPUT.resolve() == OUTPUT and OUTPUT.is_relative_to(PROJECT/"experiments")
           and not OUTPUT.exists() and OUTPUT.parent.is_dir(), "FRESH_STAGING_OUTPUT")
    OUTPUT.mkdir()
    suite = unittest.TestSuite(StagingControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_PROCESS_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    imports = [{"name": name, **pin(Path(module.__file__))} for name, module in sorted(sys.modules.items())
               if getattr(module, "__file__", None) and Path(module.__file__).is_relative_to(SOURCE)]
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "selected": list(SELECTED), "imports": imports,
        "foundation": {"path": str(foundation), "bytes": FOUNDATION_SIZE, "sha256": FOUNDATION_SHA},
        "scope": "REAL_PURE_PLANNER_CUSTODY_GRANTS_WITH_EXPLICITLY_INERT_RECEIVERS_AND_TRANSPORT",
        "mathematical_acceptance": False, "real_aggregate_checks": 0, "real_native_checks": 0,
        "proof_calls": 0, "network_calls": 0, "subprocess_calls": 0, "fixture_observations": dict(OBSERVED)}
    with (OUTPUT/"RESULT.json").open("xb") as stream: stream.write(F.compact(report))
    print(F.compact(report).decode(), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())
