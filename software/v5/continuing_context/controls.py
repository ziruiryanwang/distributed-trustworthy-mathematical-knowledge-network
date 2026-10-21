"""Focused READY-context transition controls; no mathematics is certified here.

Real session/materialization/action methods; fabricated exact-class aggregate
registry, mocked installation/foundation and preconstructed client shell.
No old test module, native worker, receipt verifier, process or socket may run.
"""
from contextlib import ExitStack
from copy import copy, deepcopy
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MAP = PROJECT/"experiments/v5-local-checks/distribution-terminal-i-01-input.json"
MAP_SHA, MAP_BYTES = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0", 2805479
MIB = 1024**2
REPLACEMENTS = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py", "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py", "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
    "v5/mixed_claims/imports_atomic.py": ("continuing_context/mixed_claims/imports_atomic.py", "45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad"),
    "v5/client/workspace_atomic.py": ("continuing_context/client/workspace_atomic.py", "32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773"),
}
C = B = AA = I = A = W = P = T = EXPECTED = None
OUTPUT = None
SOURCES, OBSERVED, FORBIDDEN = {}, {}, []
FAKE_IMAGE = "07"*32
FOUNDATION = b"SYNTHETIC-NOT-A-MATHEMATICAL-FOUNDATION"
FOUNDATION_SHA = "00"*32
INERT_RECEIPT = b"SYNTHETIC-UNCHECKED-REGISTRY-NOT-A-RECEIPT"
STORES = ("_sources", "_receipts", "_nodes", "_summaries", "_selected", "_groups", "_bodies")


def sha(raw): return hashlib.sha256(raw).hexdigest()


def need(value, reason):
    if not value: raise AssertionError(reason)


def write_new(path, raw):
    with path.open("xb") as stream:
        if stream.write(raw) != len(raw): raise ValueError("CONTROL_SHORT_WRITE")


def stage(output):
    raw = MAP.read_bytes()
    need(len(raw) == MAP_BYTES and sha(raw) == MAP_SHA, "CURRENT_MAP_PIN")
    rows = json.loads(raw)["sdk_sources"]
    need(len(rows) == 114 and set(REPLACEMENTS) <= set(rows), "CURRENT_MAP_SHAPE")
    rows = dict(rows)
    for logical, (relative, digest) in REPLACEMENTS.items():
        rows[logical] = dict(path=str(SOURCE/relative), sha256=digest)
    code = output/"selected-code"; code.mkdir()
    for logical, row in sorted(rows.items()):
        path = Path(row["path"])
        if logical not in REPLACEMENTS:
            path = SOURCE/path.relative_to(PROJECT/"software/v5")
        raw = path.read_bytes()
        need(0 < len(raw) <= 2*MIB and sha(raw) == row["sha256"]
             and ("bytes" not in row or len(raw) == row["bytes"]), "SELECTED_SOURCE_PIN:"+logical)
        target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, raw)
        need(target.read_bytes() == raw, "SELECTED_SOURCE_READBACK")
        SOURCES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    need(len(SOURCES) == 114, "EXACT_LOGICAL_SOURCE_COUNT")
    need(not any(name in sys.modules for name in ("mixed_claims", "modules", "client", "admission")),
         "EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]


def forbidden(*unused, **ignored):
    FORBIDDEN.append("FORBIDDEN_PROCESS_SOCKET_OR_MATH")
    raise AssertionError("FORBIDDEN_PROCESS_SOCKET_OR_MATH")


def fake_foundation(raw, pin, view):
    need(raw == FOUNDATION and pin == FOUNDATION_SHA, "EXACT_INERT_FOUNDATION")
    need((view._verifier._foundation, view._verifier._policy) == (B.FOUNDATION, B.POLICY),
         "FOUNDATION_BASIS")
    return dict(groups=[], bodies=[], values=[], names=[]), 0


def fake_trust_check(binding):
    """Only the local-policy persistence check is mocked; no adoption is issued."""
    C.require(type(binding) is T.TrustBinding and not binding._domain.denied,
              "SYNTHETIC_TRUST_WITHDRAWN")
    return binding._domain.identity


def spec(name, *, definition=False):
    body = ["sort", ["zero"]]
    value = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
        groups=[dict(kind="ordinary", declarations=[dict(
            kind="definition" if definition else "theorem", name=[["s", name]],
            universes=0, type=["sort", ["zero"]],
            value_hash=C.body_id(body, 0) if definition else None,
            meta=dict(hint="abbrev", safety="safe") if definition else {})])])
    return value, EXPECTED(C.summarize(value), 0, B.RELATION_IMAGE), body


def batch(value, exact, *, body=None, selected=True, opening=True):
    module = C.module_id(value)
    return C.canonical(dict(selected=[list(exact)] if selected else [],
        openings=[dict(module=module, opening=C.group_opening(value, 0))] if opening else [],
        bodies=[] if body is None else [dict(module=module, universes=0, expression=body)]))


def fake_aggregate(pairs):
    """Exact class but fabricated registry; real crypto/installation are forbidden."""
    owner = object.__new__(AA.AggregateReceiptVerifier)
    owner._aggregate_initialized = True
    owner._members, owner._member_cache, owner._handles = {}, {}, {}
    owner._member_used, owner._used, owner._output_reserved = [0, 0], [0, 0, 0], [0, 0]
    owner._member_caps, owner._caps = (4096, 4096, 64*MIB), (8, 64*MIB, 240)
    owner._output_caps = 128*MIB, 1024
    owner._controller_started, owner._controller_cpu_cap = time.process_time(), 60
    owner._closed = owner._busy = False
    owner._deadline = time.monotonic()+300
    owner._image = owner._adopted_aggregate_image = FAKE_IMAGE
    owner._foundation, owner._policy = B.FOUNDATION, B.POLICY
    owner._profile_id = owner._origin_profile = "08"*32
    domain = SimpleNamespace(denied=False, identity="synthetic-policy-not-adoption")
    binding = object.__new__(T.TrustBinding); binding._domain = domain
    owner._trust_binding = owner._trust_original_binding = binding
    owner._trust_domain, owner._trust_identity = domain, domain.identity
    owner._trust_module, owner._trust_origin = T, Path(T.__file__).resolve()
    owner._check_install = lambda: owner._active()  # Explicit installation mock.
    owner._required_origins = {name: Path(sys.modules[name].__file__).resolve() for name in (
        "aggregate_claims.aggregate_admission", "aggregate_claims", "aggregate_claims.admission_binding",
        "aggregate_claims.bindings", "admission", "admission.verifier", "admission.bindings",
        "modules", "modules.codec")}
    owner._pins = {Path(module.__file__).resolve(): dict(bytes=1, sha256="00"*32)
        for module in tuple(sys.modules.values()) if type(getattr(module, "__file__", None)) is str}
    journals = sorted(exact for _, exact, _ in pairs)
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")
        +bytes.fromhex(FAKE_IMAGE+B.RELATION_IMAGE+B.FOUNDATION+B.POLICY)
        +B.commitment(journals)+len(journals).to_bytes(4, "little")
        +(0).to_bytes(8, "little")+(1).to_bytes(8, "little"))
    aggregate = AA.VerifiedAggregate()
    owner._handles[aggregate] = header, sha(INERT_RECEIPT), len(INERT_RECEIPT)
    members = [owner.select_member(aggregate, exact, journals.index(exact),
               B.opening(journals, journals.index(exact))) for _, exact, _ in pairs]
    return owner, members


def dummy_owner(profile):
    owner = SimpleNamespace(closed=False, profile=profile)
    def active(): need(not owner.closed, "SYNTHETIC_OWNER_WITHDRAWN")
    def close(): owner.closed = True
    owner._active, owner.close = active, close
    owner.report = lambda: dict(profile_id=profile)
    return owner


def client_shell(session, ready, view):
    """Public methods are real; owner acquisition/construction and I/O are not."""
    client = object.__new__(W.CommonsClient)
    grant = W.OperationGrant()
    grant._workspace, grant._id, grant._used = "SYNTHETIC", "23"*32, True
    grant._started, grant._cpu, grant._deadline = time.monotonic()-1, time.process_time(), session._deadline
    grant._directory = OUTPUT
    grant._limits = dict(calls=100, controller_cpu_seconds=60, input_bytes=MIB,
        imports=dict(max_calls=100), output_bytes=2*MIB, output_entries=100)
    workspace = SimpleNamespace(recorded=[], active=True, _envelope=P.Envelope())
    workspace._active = lambda: need(workspace.active, "SYNTHETIC_WORKSPACE_WITHDRAWN")
    workspace._grant_active = lambda value: need(value is grant and grant._used, "ORIGINAL_GRANT")
    workspace._record = lambda *args: workspace.recorded.append(args)
    client.workspace, client.grant = workspace, grant
    client.receipt, client.delta, client.preparation = dummy_owner("11"*32), dummy_owner("12"*32), None
    client.delta._owners = (client.receipt, None)
    client._profiles = ("11"*32, "12"*32)
    client._foundation, client._foundation_sha = FOUNDATION, FOUNDATION_SHA
    client._state, client._busy, client._closed = "OPEN", False, False
    client._calls, client._input_bytes = 3, len(FOUNDATION)+11
    client._warrants, client._receipt_cache, client._packet_cache = {}, {}, {}
    client._candidates, client._failures, client._publications = {}, [], []
    token = W.AuthorContext()
    client._context, client._selection_view = (token, ready["selection_binding"]), view
    client._session = session
    client._channel = client._handoff = client._search = client._acquisition = None
    client._query_used = True
    budget = SimpleNamespace(deadline=grant.deadline, spent=17)
    budget.active = lambda: need(time.monotonic() < budget.deadline, "ORIGINAL_ACQUISITION_DEADLINE")
    client._budget = budget
    client._counts = dict(admission_submissions=2, same_live_hits=1, author_calls=1,
        store_calls=0, publication_attempts=0, new_import_sessions=1)
    client._census = lambda: dict(bytes=0, entries=0)  # No filesystem census qualification.
    client.report = lambda: dict(state=client._state, calls=client._calls)
    return client, token


class Controls(unittest.TestCase):
    def setUp(self):
        self.sessions, self.owners = [], []
        self.foundation = patch.object(I, "_decode_foundation", fake_foundation)
        self.foundation.start()
        self.trust = patch.object(T, "check_binding", fake_trust_check)
        self.trust.start()

    def tearDown(self):
        self.foundation.stop()
        for session in reversed(self.sessions): session.close()
        for owner in reversed(self.owners): owner.close()
        self.trust.stop()

    def make(self, *, second_definition=False, preload=False, ready=True, mode="eager"):
        pairs = [spec("base"), spec("new", definition=second_definition)]
        owner, members = fake_aggregate(pairs)
        self.owners.append(owner)
        session = I.MixedImportSession(aggregate_verifier=owner, max_calls=1000, wall_seconds=180)
        self.sessions.append(session)
        session.use_aggregate_member(members[0], INERT_RECEIPT)
        if preload: session.use_aggregate_member(members[1], INERT_RECEIPT)
        result = view = None
        if ready:
            result, view = session.materialize(batch(*pairs[0][:2]), FOUNDATION, FOUNDATION_SHA,
                                               definition_mode=mode)
            self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
            self.assertIsNotNone(view)
        return SimpleNamespace(session=session, owner=owner, members=members, pairs=pairs,
                               ready=result, view=view)

    def assert_revoked(self, session):
        self.assertTrue(session._closed)
        self.assertIsNone(session._view); self.assertIsNone(session._view_payload)
        self.assertIsNone(session._sealed_state)
        self.assertTrue(all(not getattr(session, name) for name in STORES))

    def test_exact_transition_preserves_original_state_and_reseals(self):
        f = self.make(); s = f.session
        ids = {name: id(getattr(s, name)) for name in STORES}
        maps = {name: dict(getattr(s, name)) for name in STORES}
        fixed = (s._owners, s._origins, s._basis, s._profiles, s._profile, s._caps,
                 s._deadline, s._representation_revision, s._definition_mode, s._origin_definition_mode)
        calls, submitted, data = s._calls, s._submitted_bytes, s._data_bytes
        s.begin_extension(f.view)
        self.assertFalse(s._sealed); self.assertFalse(s._closed)
        self.assertIsNone(s._view); self.assertIsNone(s._view_payload); self.assertIsNone(s._sealed_state)
        self.assertEqual(s._calls, calls+1)
        self.assertEqual((s._submitted_bytes, s._data_bytes), (submitted, data))
        self.assertEqual(fixed, (s._owners, s._origins, s._basis, s._profiles, s._profile, s._caps,
            s._deadline, s._representation_revision, s._definition_mode, s._origin_definition_mode))
        for name in STORES:
            self.assertEqual(id(getattr(s, name)), ids[name]); self.assertEqual(getattr(s, name), maps[name])
        s.use_aggregate_member(f.members[1], INERT_RECEIPT)
        result, view = s.materialize(batch(*f.pairs[1][:2]), FOUNDATION, FOUNDATION_SHA)
        self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertIsNot(view, f.view); s.require_view(view)
        self.assertEqual(len(result["packet"]["imports"]), 2)
        self.assertEqual(len(s._sources), 2); self.assertEqual(len(s._receipts), 1)
        self.assertGreater(s._calls, calls); self.assertGreater(s._submitted_bytes, submitted)
        OBSERVED[self._testMethodName] = dict(real_session_transition=True, old_maps_retained=True,
            one_transition_call=True, new_context_groups=2, cryptographic_admission=False)

    def test_foreign_copied_unsealed_and_reused_views_fail_stop(self):
        for kind in ("copy", "deepcopy", "foreign", "object", "unsealed", "reused"):
            with self.subTest(kind=kind):
                f = self.make(ready=kind != "unsealed"); s = f.session
                if kind == "copy": invalid = copy(f.view)
                elif kind == "deepcopy": invalid = deepcopy(f.view)
                elif kind == "foreign": invalid = self.make().view
                elif kind == "reused":
                    s.begin_extension(f.view)
                    _, new = s.materialize(C.canonical(dict(selected=[], openings=[], bodies=[])),
                                           FOUNDATION, FOUNDATION_SHA)
                    self.assertIsNot(new, f.view); invalid = f.view
                else: invalid = object()
                before = s._calls
                with self.assertRaises((P.DeltaError, C.StructureError)): s.begin_extension(invalid)
                self.assertEqual(s._calls, before+1); self.assert_revoked(s)
        OBSERVED[self._testMethodName] = dict(fresh_fixture_per_refusal=True, variants=6)

    def test_expiry_withdrawal_tamper_and_batch_guard_fail_stop(self):
        for kind in ("session-expiry", "owner-close", "trust-withdrawal", "source-withdrawal", "semantic-tamper", "batch"):
            with self.subTest(kind=kind):
                f = self.make(); s = f.session; before = s._calls
                if kind == "session-expiry": s._deadline = time.monotonic()-1
                elif kind == "owner-close": f.owner.close()
                elif kind == "trust-withdrawal": f.owner._trust_domain.denied = True
                elif kind == "source-withdrawal": f.owner._members.clear()
                elif kind == "semantic-tamper": s._selected["ab"*32] = b"tampered"
                else: s._batching = True
                with self.assertRaises((P.DeltaError, C.StructureError)): s.begin_extension(f.view)
                self.assert_revoked(s); self.assertGreaterEqual(s._calls, before)
                self.assertLessEqual(s._calls, before+1)
        OBSERVED[self._testMethodName] = dict(variants=6, no_revived_view=True)

    def test_call_budget_is_not_renewed_and_failure_never_refunds(self):
        for last_available in (False, True):
            f = self.make(); s = f.session
            caps = list(s._caps); caps[3] = s._calls+int(last_available); s._caps = tuple(caps)
            original_caps, original_calls = s._caps, s._calls
            if last_available:
                s.begin_extension(f.view)
                self.assertEqual(s._calls, original_calls+1)
                with self.assertRaises((P.DeltaError, C.StructureError)):
                    s.materialize(C.canonical(dict(selected=[], openings=[], bodies=[])), FOUNDATION, FOUNDATION_SHA)
            else:
                with self.assertRaises((P.DeltaError, C.StructureError)): s.begin_extension(f.view)
            self.assert_revoked(s); self.assertEqual(s._caps, original_caps)
            self.assertEqual(s._calls, original_calls+int(last_available))
        OBSERVED[self._testMethodName] = dict(original_budget_exhausted=True, refunded_calls=0)

    def test_definition_policy_stays_fixed_across_extension(self):
        for changed in (False, True):
            f = self.make(second_definition=True, mode="interface-only"); s = f.session
            s.begin_extension(f.view); s.use_aggregate_member(f.members[1], INERT_RECEIPT)
            self.assertEqual((s._definition_mode, s._origin_definition_mode), ("interface-only",)*2)
            if changed:
                with self.assertRaises((P.DeltaError, C.StructureError)):
                    s.materialize(batch(*f.pairs[1][:2]), FOUNDATION, FOUNDATION_SHA, definition_mode="eager")
                self.assert_revoked(s)
            else:
                result, view = s.materialize(batch(*f.pairs[1][:2]), FOUNDATION, FOUNDATION_SHA,
                                             definition_mode="interface-only")
                self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
                s.require_view(view)
                self.assertEqual(s._definition_mode, "interface-only")
        OBSERVED[self._testMethodName] = dict(policy_switch_refused=True, unchanged_policy_works=True)

    def test_old_author_operation_cannot_use_replaced_selection(self):
        f = self.make(); s = f.session
        operation = A.MixedSourceOperation(s, FOUNDATION, FOUNDATION_SHA,
            "theorem later : True := by trivial", [[["s", "later"]]], view=f.view)
        try:
            self.assertEqual(operation.prepare()["status"], "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION")
            s.begin_extension(f.view)
            _, view = s.materialize(C.canonical(dict(selected=[], openings=[], bodies=[])), FOUNDATION, FOUNDATION_SHA)
            self.assertIsNot(view, f.view)
            with self.assertRaises((P.DeltaError, C.StructureError)): operation.prepare()
        finally: operation.close()
        OBSERVED[self._testMethodName] = dict(real_source_operation_checked=True, worker_calls=0)

    def test_public_advance_preserves_same_client_session_and_grant(self):
        f = self.make(preload=True); c, token = client_shell(f.session, f.ready, f.view)
        original = (c.workspace, c.grant, c.receipt, c.delta, c._session, c._budget)
        limits, deadline, counts = deepcopy(c.grant._limits), c.grant.deadline, dict(c._counts)
        maps = {name: getattr(c, name) for name in ("_warrants", "_receipt_cache", "_packet_cache", "_candidates")}
        calls, inputs = c._calls, c._input_bytes
        value, exact, _ = f.pairs[1]
        result = c.advance_context(token, warrants=[], selected=[exact],
            openings=[dict(module=C.module_id(value), opening=C.group_opening(value, 0))], bodies=[])
        self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertFalse(result["mathematical_acceptance"]); self.assertIsNot(result["context"], token)
        self.assertEqual(original, (c.workspace, c.grant, c.receipt, c.delta, c._session, c._budget))
        self.assertEqual((c.grant._limits, c.grant.deadline, c._counts), (limits, deadline, counts))
        for name, store in maps.items(): self.assertIs(getattr(c, name), store)
        self.assertEqual(c._calls, calls+1); self.assertGreater(c._input_bytes, inputs)
        self.assertEqual(c._budget.spent, 17); self.assertTrue(c._query_used)
        self.assertFalse(c._busy); self.assertEqual(c._state, "OPEN")
        c._live_context(result["context"])
        with self.assertRaises((P.DeltaError, C.StructureError, ValueError)):
            c._live_context(token)
        OBSERVED[self._testMethodName] = dict(real_public_action=True, synthetic_constructor=True,
            new_import_sessions=c._counts["new_import_sessions"], original_grant=True)

    def test_public_advance_need_then_existing_extend_finishes(self):
        f = self.make(preload=True, second_definition=True); c, token = client_shell(f.session, f.ready, f.view)
        value, exact, body = f.pairs[1]; module = C.module_id(value)
        result = c.advance_context(token, warrants=[], selected=[exact],
            openings=[dict(module=module, opening=C.group_opening(value, 0))], bodies=[])
        self.assertEqual(result["status"], "NEED_AUTHORING_CONTEXT_DATA")
        self.assertIsNone(c._selection_view); self.assertEqual(result["demands"][0]["kind"], "NeedBody")
        next_result = c.extend_context(result["context"], warrants=[], selected=[], openings=[],
            bodies=[dict(module=module, universes=0, expression=body)])
        self.assertEqual(next_result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertIsNotNone(c._selection_view); self.assertIs(c._session, f.session)
        self.assertEqual(c._counts["new_import_sessions"], 1)
        OBSERVED[self._testMethodName] = dict(need_then_existing_extend=True, second_startup=False)

    def test_public_stale_ready_extend_and_post_revoke_error_fail_stop(self):
        for kind in ("foreign", "ready-extend", "malformed-after-revoke"):
            with self.subTest(kind=kind):
                f = self.make(preload=True); c, token = client_shell(f.session, f.ready, f.view)
                calls, inputs = c._calls, c._input_bytes
                try:
                    with self.assertRaises((P.DeltaError, C.StructureError, ValueError)):
                        if kind == "foreign":
                            c.advance_context(W.AuthorContext(), warrants=[], selected=[], openings=[], bodies=[])
                        elif kind == "ready-extend":
                            c.extend_context(token, warrants=[], selected=[], openings=[], bodies=[])
                        else:
                            c.advance_context(token, warrants=[], selected=[], openings=[{"bad": True}], bodies=[])
                    self.assertEqual(c._state, "FAILED"); self.assertFalse(c._busy)
                    self.assertIsNone(c._context); self.assert_revoked(f.session)
                    self.assertTrue(c.receipt.closed and c.delta.closed)
                    self.assertEqual(c._calls, calls+1); self.assertGreaterEqual(c._input_bytes, inputs)
                    if kind == "malformed-after-revoke": self.assertGreater(c._input_bytes, inputs)
                    self.assertTrue(c.workspace.recorded)
                finally:
                    # Fresh fixture per fail-stop case: no recovery of old authority.
                    pass
        OBSERVED[self._testMethodName] = dict(variants=3, old_extend_still_need_only=True,
            failure_after_revocation_has_no_restore=True)


SELECTED = (
    "test_exact_transition_preserves_original_state_and_reseals",
    "test_foreign_copied_unsealed_and_reused_views_fail_stop",
    "test_expiry_withdrawal_tamper_and_batch_guard_fail_stop",
    "test_call_budget_is_not_renewed_and_failure_never_refunds",
    "test_definition_policy_stays_fixed_across_extension",
    "test_old_author_operation_cannot_use_replaced_selection",
    "test_public_advance_preserves_same_client_session_and_grant",
    "test_public_advance_need_then_existing_extend_finishes",
    "test_public_stale_ready_extend_and_post_revoke_error_fail_stop",
)


def main():
    global C, B, AA, I, A, W, P, T, EXPECTED, OUTPUT
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    need(OUTPUT.is_absolute() and OUTPUT.is_dir() and OUTPUT.is_relative_to(PROJECT), "CANONICAL_OUTPUT")
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_WINDOWS")
    stage(OUTPUT)
    with ExitStack() as guards:
        for owner, name in ((subprocess, "Popen"), (os, "system")):
            guards.enter_context(patch.object(owner, name, forbidden))
        def load(name): return importlib.import_module(name)
        C = load("modules.codec"); B = load("aggregate_claims.bindings")
        T = load("admission.trust")
        AA = load("aggregate_claims.aggregate_admission"); I = load("mixed_claims.imports_atomic")
        A = load("mixed_claims.authoring_atomic"); W = load("client.workspace_atomic")
        P = load("mixed_claims.packet"); EXPECTED = load("delta_claims.claims").expected_journal
        # Load Python's socket/ssl class definitions before replacing constructors.
        for name in ("socket", "create_connection"):
            guards.enter_context(patch.object(socket, name, forbidden))
        for name, cls in (("admission.verifier", "ReceiptVerifier"),
                          ("aggregate_claims.aggregate_admission", "AggregateReceiptVerifier"),
                          ("mixed_claims.receiver", "MixedDeltaVerifier")):
            guards.enter_context(patch.object(getattr(load(name), cls), "receive", forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    old_tests = [name for name in sys.modules if name.startswith(("mixed_claims.test_", "client.test_"))
                 or name == "aggregate_claims.aggregate_admission_controls"]
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) == len(OBSERVED) and not result.skipped \
             and not FORBIDDEN and not old_tests
    report = dict(schema="DMKN_CONTINUING_CONTEXT_CONTROLS_V1", status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), observations=OBSERVED, sources=SOURCES, forbidden_calls=FORBIDDEN,
        old_test_imports=old_tests, actual_native_calls=0, actual_proof_calls=0, actual_network_calls=0,
        mathematical_acceptance=False, scope="SYNTHETIC_AUTHORITY_REAL_SESSION_CONTEXT_ACTION_TRANSITIONS",
        mocks=["aggregate admission registry", "installation validation", "foundation decoding", "local trust persistence",
               "client construction and I/mixed owner acquisition", "workspace persistence/census", "acquisition ledger"],
        excludes=["mathematical soundness", "actual local I-to-M authoring", "performance or growth benefit"])
    write_new(OUTPUT/"continuing-context-controls-result.json", json.dumps(report, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__": raise SystemExit(main())
