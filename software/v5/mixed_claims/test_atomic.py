"""Changed-boundary synthetic controls. ZERO cryptographic or native validation.

The exact-class owners below are deliberately fabricated, not genuine warrants.
Installation checks and foundation decoding are mocked. No prior suite is run.
These controls measure authority plumbing and logical scan counts, not CPU speed.
"""
from copy import copy, deepcopy
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission_controls import fake_owner, FAKE_IMAGE
from aggregate_claims.aggregate_admission import VerifiedAggregate
from delta_claims.claims import expected_journal
from mixed_claims import authoring as OLD_A
from mixed_claims import imports as OLD_I
from mixed_claims import authoring_atomic as A
from mixed_claims import imports_atomic as I
from mixed_claims import packet as P
from mixed_claims.test_imports import fake_foundation, new_witness
from modules import codec as C
from client import workspace_atomic as W

FOUNDATION = b"SYNTHETIC-NOT-A-FOUNDATION"
FOUNDATION_SHA = "00"*32
SOURCE = "theorem next : True := by trivial"
ROOTS = [[["s", "next"]]]


def fixture(count=1, *, definition=False):
    body = ["sort", ["zero"]]
    groups = []
    for index in range(count):
        groups.append({"kind": "ordinary", "declarations": [{
            "kind": "definition" if definition and index == 0 else "theorem",
            "name": [["s", "item"+str(index)]], "universes": 0,
            "type": ["sort", ["zero"]],
            "value_hash": C.body_id(body, 0) if definition and index == 0 else None,
            "meta": {}}]})
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION,
            "policy": B.POLICY, "groups": groups}
    exact = expected_journal(C.summarize(spec), 0, B.RELATION_IMAGE)
    return spec, exact, body


def session_for(spec, exact, *, legacy=False, **caps):
    owner, unused, unused2, unused3, unused4 = fake_owner()
    receipt = b"SYNTHETIC-NOT-A-RECEIPT"
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")
              +bytes.fromhex(FAKE_IMAGE+B.RELATION_IMAGE+B.FOUNDATION+B.POLICY)
              +B.commitment([exact])+(1).to_bytes(4, "little")
              +(0).to_bytes(8, "little")+(1).to_bytes(8, "little"))
    batch = VerifiedAggregate()
    import hashlib
    owner._handles[batch] = header, hashlib.sha256(receipt).hexdigest(), len(receipt)
    # TEST ONLY. Nothing in this fake map is an installation adoption.
    owner._pins = {Path(module.__file__).resolve(): {"bytes": 1, "sha256": "00"*32}
                   for module in tuple(sys.modules.values())
                   if type(getattr(module, "__file__", None)) is str}
    scans = [0]
    def installation():
        scans[0] += 1
        owner._active()
    owner._check_install = installation
    member = owner.select_member(batch, exact, 0, [])
    session = (OLD_I.MixedImportSession if legacy else I.MixedImportSession)(
        aggregate_verifier=owner, **caps)
    session.use_aggregate_member(member, receipt)
    return session, owner, member, receipt, scans


def batch_for(spec, exact, *, body=None, select=True, openings=True):
    module = C.module_id(spec)
    return C.canonical({"selected": [list(exact)] if select else [],
        "openings": [{"module": module, "opening": C.group_opening(spec, index)}
                     for index in range(len(spec["groups"]))] if openings else [],
        "bodies": [] if body is None else [{"module": module, "universes": 0, "expression": body}]})


class AtomicImportControls(unittest.TestCase):
    def setUp(self):
        self.owners = []
        # Exact pure-helper patch target is fixed by the selected successor.
        self.foundation = patch.object(I, "_decode_foundation", fake_foundation)
        self.foundation.start()

    def tearDown(self):
        self.foundation.stop()
        for session, owner in reversed(self.owners):
            session.close(); owner.close()

    def make(self, count=1, *, definition=False, legacy=False, **caps):
        spec, exact, body = fixture(count, definition=definition)
        session, owner, member, receipt, scans = session_for(spec, exact, legacy=legacy, **caps)
        self.owners.append((session, owner))
        return session, owner, member, receipt, scans, spec, exact, body

    def ready(self, count=1, *, definition=False):
        values = self.make(count, definition=definition)
        session, owner, member, receipt, scans, spec, exact, body = values
        ready, view = session.materialize(batch_for(spec, exact, body=body if definition else None),
                                          FOUNDATION, FOUNDATION_SHA)
        self.assertEqual(ready["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertIsNotNone(view)
        return values, ready, view

    def test_context_selection_and_onward_equal_incremental_semantics(self):
        values, ready, view = self.ready(3, definition=True)
        current, owner, member, receipt, scans, spec, exact, body = values
        old, old_owner, unused, unused2, unused3, _, _, _ = self.make(3, definition=True, legacy=True)
        module = old.select_warrant(exact)
        for index in range(3): old.open_group(module, C.group_opening(spec, index))
        old.supply_body(module, 0, body)
        with patch.object(OLD_A, "_decode_foundation", fake_foundation):
            expected = OLD_A.prepare_mixed_context(old, FOUNDATION, FOUNDATION_SHA)
        self.assertEqual(ready["packet"], expected["packet"])
        self.assertEqual(current.view_selection(view), old.selection())
        witness, binding = new_witness(old)
        # Old onward route on a sealed new session must use the stored selection,
        # never reconstruct it by calling the obsolete per-group scan path.
        actual_packet, actual_census = current.onward_packet(witness, binding, P.Envelope())
        old_packet, old_census = old.onward_packet(witness, binding, P.Envelope())
        self.assertEqual((actual_packet, actual_census), (old_packet, old_census))
        self.assertFalse(ready["mathematical_acceptance"])

    def test_need_is_extendable_then_ready_seals(self):
        session, owner, member, receipt, scans, spec, exact, body = self.make(definition=True)
        need, view = session.materialize(batch_for(spec, exact), FOUNDATION, FOUNDATION_SHA)
        self.assertEqual(need["status"], "NEED_AUTHORING_CONTEXT_DATA")
        self.assertIsNone(view); self.assertEqual(need["demands"][0]["kind"], "NeedBody")
        session.require_selection(need["selection_binding"])
        ready, view = session.materialize(batch_for(spec, exact, body=body, select=False, openings=False),
                                          FOUNDATION, FOUNDATION_SHA)
        self.assertEqual(ready["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        session.require_view(view)

    def test_all_public_and_internal_semantic_writers_refuse_seal(self):
        values, ready, view = self.ready()
        session, owner, member, receipt, scans, spec, exact, body = values
        module = C.module_id(spec); before = session.view_selection(view)
        mutations = (
            lambda: session.use_aggregate_member(member, receipt),
            lambda: session.use_legacy_handle(None, b"fake"),
            lambda: session.use_delta_handle(None),
            lambda: session._direct(1, member, receipt, None),
            lambda: session._merge(None, None, None, None, None),
            lambda: session.select_warrant(exact),
            lambda: session.open_group(module, C.group_opening(spec, 0)),
            lambda: session.supply_body(module, 0, body),
            lambda: session.materialize(batch_for(spec, exact), FOUNDATION, FOUNDATION_SHA))
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with self.assertRaises((P.DeltaError, C.StructureError)): mutation()
                self.assertEqual(session.view_selection(view), before)

    def test_views_are_identity_bound_and_return_detached_data(self):
        (session, *unused), ready, view = self.ready()
        (foreign, *unused2), _, other_view = self.ready()
        for invalid in (copy(view), deepcopy(view), other_view, ready, object()):
            with self.assertRaises((P.DeltaError, C.StructureError)):
                session.require_view(invalid)
        exposed = session.view_context(view)
        exposed["packet"]["imports"].clear()
        selected, binding = session.view_selection(view); selected.clear()
        self.assertEqual(session.view_context(view)["packet"], ready["packet"])
        self.assertEqual(len(session.view_selection(view)[0]), 1)
        foreign.close()
        with self.assertRaises((P.DeltaError, C.StructureError)): foreign.require_view(other_view)

    def test_owner_close_and_session_expiry_revoke_view(self):
        for expire in (False, True):
            values, ready, view = self.ready()
            session, owner, *unused = values
            if expire: session._deadline = time.monotonic()-1
            else: owner.close()
            with self.assertRaises((P.DeltaError, C.StructureError)): session.require_view(view)
            self.assertTrue(session._closed)

    def test_malformed_second_record_never_commits_first_and_is_charged(self):
        session, owner, member, receipt, scans, spec, exact, body = self.make(2)
        value = C.parse_json(batch_for(spec, exact))
        value["openings"][1]["opening"]["summary"]["group_count"] += 1
        raw = C.canonical(value); before_bytes, before_calls = session._submitted_bytes, session._calls
        with self.assertRaises((P.DeltaError, C.StructureError)):
            session.materialize(raw, FOUNDATION, FOUNDATION_SHA)
        self.assertFalse(session._groups); self.assertFalse(session._selected)
        self.assertGreaterEqual(session._submitted_bytes, before_bytes+len(raw))
        self.assertGreater(session._calls, before_calls)

    def test_exact_bytes_and_canonical_batch_required(self):
        for transform in (bytearray, lambda raw: raw+b" ",
                          lambda raw: C.canonical({**C.parse_json(raw), "extra": 1})):
            session, owner, member, receipt, scans, spec, exact, body = self.make()
            with self.assertRaises((P.DeltaError, C.StructureError)):
                session.materialize(transform(batch_for(spec, exact)), FOUNDATION, FOUNDATION_SHA)
            self.assertFalse(session._groups)
        invoked = []
        class CustomLimits:
            def __iter__(self):
                invoked.append(True)
                return iter(())
        session, owner, member, receipt, scans, spec, exact, body = self.make()
        with self.assertRaises((P.DeltaError, C.StructureError)):
            session.materialize(batch_for(spec, exact), FOUNDATION, FOUNDATION_SHA, limits=CustomLimits())
        self.assertEqual(invoked, [])

    def test_call_data_and_submitted_caps_are_not_bypassed(self):
        for which in ("calls", "data", "submitted"):
            session, owner, member, receipt, scans, spec, exact, body = self.make(4, definition=which == "data")
            raw = batch_for(spec, exact)
            if which == "data":
                need, view = session.materialize(raw, FOUNDATION, FOUNDATION_SHA)
                self.assertIsNone(view)
                self.assertEqual(need["status"], "NEED_AUTHORING_CONTEXT_DATA")
                raw = batch_for(spec, exact, body=body, select=False, openings=False)
                self.assertLess(len(raw), session._data_bytes)
            caps = list(session._caps)
            if which == "calls": caps[3] = session._calls+2
            elif which == "data": caps[5] = session._data_bytes
            else: caps[4] = session._submitted_bytes+1
            session._caps = tuple(caps)
            before = session._calls
            with self.assertRaises((P.DeltaError, C.StructureError)):
                session.materialize(raw, FOUNDATION, FOUNDATION_SHA)
            self.assertFalse(session._groups)
            self.assertGreaterEqual(session._calls, before)

    def test_entry_and_exit_failure_revoke_without_publish(self):
        for fail_at in (1, 2):
            session, owner, member, receipt, scans, spec, exact, body = self.make()
            original = session._live; calls = [0]
            def boundary():
                calls[0] += 1
                if calls[0] == fail_at:
                    owner.close()
                return original()
            before_bytes = session._submitted_bytes
            with patch.object(session, "_live", boundary):
                with self.assertRaises((P.DeltaError, C.StructureError)):
                    session.materialize(batch_for(spec, exact), FOUNDATION, FOUNDATION_SHA)
            self.assertTrue(session._closed); self.assertFalse(session._groups)
            self.assertGreaterEqual(session._submitted_bytes, before_bytes)

    def test_authoring_preparation_reuses_same_sealed_view(self):
        values, ready, view = self.ready(4)
        session = values[0]
        operation = A.MixedSourceOperation(session, FOUNDATION, FOUNDATION_SHA, SOURCE, ROOTS, view=view)
        def obsolete(*args, **kwargs): raise AssertionError("OBSOLETE_PER_GROUP_REOPEN")
        with patch.object(session, "_group", obsolete):
            prepared = operation.prepare()
            self.assertEqual(prepared["status"], "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION")
            self.assertEqual(C.parse_json(prepared["request"])["context"], ready["packet"])
        operation.close()
        with self.assertRaises((P.DeltaError, C.StructureError)): operation.prepare()

    def test_installation_scan_count_has_no_group_multiplier(self):
        counts = []
        for size in (1, 16):
            session, owner, member, receipt, scans, spec, exact, body = self.make(size)
            start = scans[0]
            ready, view = session.materialize(batch_for(spec, exact), FOUNDATION, FOUNDATION_SHA)
            materialize_count = scans[0]-start
            start = scans[0]
            operation = A.MixedSourceOperation(session, FOUNDATION, FOUNDATION_SHA, SOURCE, ROOTS, view=view)
            operation.prepare(); operation.close()
            counts.append((materialize_count, scans[0]-start))
        self.assertGreater(counts[0][0], 0)
        self.assertGreater(counts[0][1], 0)
        self.assertEqual(counts[0], counts[1])

    def test_client_routes_one_atomic_batch_and_refuses_ready_extension(self):
        session, owner, member, receipt, scans, spec, exact, body = self.make()
        charges = []
        client = SimpleNamespace(_session=session, _foundation=FOUNDATION,
            _foundation_sha=FOUNDATION_SHA, _charge=charges.append, _selection_view=None)
        client._live_context = lambda token: W.CommonsClient._live_context(client, token)
        value = C.parse_json(batch_for(spec, exact))
        def obsolete(*args, **kwargs): raise AssertionError("CLIENT_INCREMENTAL_PATH_USED")
        with patch.object(session, "select_warrant", obsolete), patch.object(session, "open_group", obsolete), \
             patch.object(session, "supply_body", obsolete):
            result = W.CommonsClient._context_data(client, [], [exact], value["openings"], [])
        self.assertEqual(len(charges), 1)
        self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertIsNotNone(client._selection_view)
        with self.assertRaisesRegex(ValueError, "READY_CONTEXT_SEALED"):
            W.CommonsClient.extend_context.__wrapped__(client, result["context"],
                warrants=[], selected=[], openings=[], bodies=[])

    def test_client_passes_sealed_view_to_author_and_closes_operation(self):
        values, ready, view = self.ready()
        session = values[0]; context = W.AuthorContext(); charges, calls, closed = [], [], []
        operation = SimpleNamespace(close=lambda: closed.append(True))
        def construct(*args, **kwargs):
            self.assertIs(args[0], session); self.assertIs(kwargs["view"], view)
            return operation
        preparation = SimpleNamespace(author=lambda *args, **kwargs: calls.append((args, kwargs)) or {"test": True})
        client = SimpleNamespace(_session=session, _context=(context, ready["selection_binding"]),
            _selection_view=view, _foundation=FOUNDATION, _foundation_sha=FOUNDATION_SHA,
            _charge=charges.append, preparation=preparation, _counts={"author_calls": 0},
            workspace=SimpleNamespace(_envelope=P.Envelope()),
            grant=SimpleNamespace(remaining_seconds=lambda: 60))
        client._live_context = lambda token: W.CommonsClient._live_context(client, token)
        with patch.object(W, "MixedSourceOperation", construct):
            result = W.CommonsClient.author.__wrapped__(client, context, SOURCE, ROOTS,
                cpu_seconds=1, wall_seconds=2)
        self.assertEqual(result, {"test": True}); self.assertEqual(closed, [True])
        self.assertEqual(len(calls), 1); self.assertEqual(len(charges), 2)


if __name__ == "__main__": unittest.main(verbosity=2)
