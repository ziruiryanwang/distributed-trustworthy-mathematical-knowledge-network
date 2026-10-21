"""Focused native-free controls for standalone/enclosed mixed validation.

Exact-class structural shells exercise actual selected guards and check bodies.
They have real local trust records and real pin files, but no native executable,
constructor adoption, mathematical handles, receive operation or proof claim.
Counting wrappers delegate to original methods; no saved report is authority.
"""
import ast
from collections import Counter
from contextlib import ExitStack
from contextvars import copy_context
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
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-terminal-i-01-input.json"
MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
REPLACEMENTS = {
    "v5/admission/pin_phase.py": "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881",
    "v5/mixed_claims/receiver.py": "835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced",
    "v5/mixed_claims/imports_atomic.py": "8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595",
}
REFERENCES = {
    "runtime_efficient/mixed_claims/receiver.py":
        "aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f",
    "interface_views/imports_atomic.py":
        "e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459",
}
MIXED_MODULES = (
    "mixed_claims", "mixed_claims.packet", "mixed_claims.receiver",
    "admission", "admission.verifier", "admission.bindings", "admission.pin_phase",
    "aggregate_claims", "aggregate_claims.aggregate_admission", "aggregate_claims.admission_binding",
    "aggregate_claims.bindings", "modules", "modules.codec", "delta", "delta.packet",
    "delta.receiver", "delta_claims", "delta_claims.receiver", "delta_claims.claims",
    "production", "production.producer",
)
IMPORT_MODULES = tuple(dict.fromkeys(MIXED_MODULES+(
    "mixed_claims.imports_atomic", "authoring", "authoring.context", "authoring.imports",
    "modules.model", "modules.source_rows",
)))
OUTPUT = CODE = C = T = PP = V = M = I = B = None
SOURCE_COPIES, REFERENCE_READS, OBSERVED = {}, {}, {}
FORBIDDEN = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stage_sources(output):
    raw = MAP_PATH.read_bytes()
    if sha(raw) != MAP_SHA:
        raise ValueError("BASIS_MAP_CHANGED")
    basis = json.loads(raw)["sdk_sources"]
    if len(basis) != 114 or not set(REPLACEMENTS) <= set(basis):
        raise ValueError("BASIS_MAP_COUNT_OR_REPLACEMENTS")
    code = output/"selected-code"
    code.mkdir()
    for logical, row in sorted(basis.items()):
        if logical in REPLACEMENTS:
            path = SOURCE/"standalone_validation"/logical[3:]
            expected = REPLACEMENTS[logical]
            raw = path.read_bytes()
            size = len(raw)
        else:
            path = SOURCE/Path(row["path"]).relative_to(PROJECT/"software/v5")
            expected, size = row["sha256"], row["bytes"]
            raw = path.read_bytes()
        if not 0 < size <= 2*1024**2 or len(raw) != size or sha(raw) != expected:
            raise ValueError("SELECTED_SOURCE_CHANGED:"+logical)
        target = code/logical
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            if stream.write(raw) != len(raw):
                raise ValueError("SOURCE_SHORT_WRITE")
        if target.read_bytes() != raw:
            raise ValueError("SOURCE_COPY_CHANGED")
        SOURCE_COPIES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    for name in ("admission", "modules", "client", "mixed_claims"):
        if name in sys.modules:
            raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return code


def support():
    return {"schema": "DMKN_LOCAL_TRUST_SUPPORT_V1", "identities": {
        "relation_image": B.RELATION_IMAGE, "aggregate_image": None,
        "foundation": B.FOUNDATION, "policy": B.POLICY,
        "receipt_scheme": "resolved-succinct-poseidon2"},
        "roles": {"inert/control.py": {"bytes": 1, "sha256": sha(b"x")}}}


def origins(names):
    return {name: CODE/"v5"/(name.replace(".", "/")+
            ("/__init__.py" if "." not in name else ".py")) for name in names}


def body(raw, cls, method):
    tree = ast.parse(raw)
    owner = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == cls)
    function = next(node for node in owner.body if isinstance(node, ast.FunctionDef) and node.name == method)
    return [ast.dump(node, include_attributes=False) for node in function.body]


class Controls(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT/self._testMethodName
        self.root.mkdir()
        self.serial = 0
        self.reads, self.pins, self.resolves, self.deadlines, self.bodies = [], [], [], [], []
        self.guards = Counter()
        self.after_pin = self.after_resolve = None
        self.real_resolve, self.real_read = Path.resolve, T._read
        self.trust_path = self.real_resolve(Path(T.__file__))
        self.trust_file = T.__file__
        self.real_i_active, self.real_m_active = V.ReceiptVerifier._active, M.MixedDeltaVerifier._active
        self.real_check_phase = M.MixedDeltaVerifier._check_phase
        self.stack = ExitStack()

        def counted_read(path):
            self.reads.append(str(path))
            return self.real_read(path)

        def counted_resolve(path, *args, **kwargs):
            result = self.real_resolve(path, *args, **kwargs)
            if str(path) == str(self.trust_path):
                self.resolves.append(str(path))
                if self.after_resolve is not None:
                    self.after_resolve(path, result)
            return result

        def i_active(owner):
            self.guards["I"] += 1
            return self.real_i_active(owner)

        def m_active(owner, deadline=None):
            self.guards["mixed"] += 1
            self.deadlines.append(deadline)
            return self.real_m_active(owner, deadline)

        def check_phase(owner, deadline=None):
            view = PP._CURRENT.get()
            event = dict(owner=owner, view=view, phase=None if view is None else view.phase, completed=False)
            self.bodies.append(event)
            result = self.real_check_phase(owner, deadline)
            event["completed"] = True
            return result

        for target, name, value in (
            (T, "_read", counted_read), (Path, "resolve", counted_resolve),
            (V.ReceiptVerifier, "_active", i_active),
            (M.MixedDeltaVerifier, "_active", m_active),
            (M.MixedDeltaVerifier, "_check_phase", check_phase),
        ):
            self.stack.enter_context(patch.object(target, name, value))
        self.assert_restored()

    def tearDown(self):
        self.stack.close()
        self.assertEqual(T.__file__, self.trust_file)
        self.assert_restored()

    def assert_restored(self):
        self.assertIsNone(PP._CURRENT.get())
        self.assertIsNone(PP._ORIGIN_PHASE.get())
        self.assertIsNone(T._VALIDATION_PHASE.get())

    def reset(self):
        for values in (self.reads, self.pins, self.resolves, self.deadlines, self.bodies):
            values.clear()
        self.guards.clear()

    def observe(self, **values):
        OBSERVED[self._testMethodName] = values

    def fixture(self, extra_pins=3):
        self.serial += 1
        root = self.root/str(self.serial)
        root.mkdir()
        domain = T.TrustDomain.create(root/"trust", sha(str(root).encode()), support())
        binding = domain.bind()
        required = origins(IMPORT_MODULES)
        paths = list(required.values())+[self.trust_path]
        extras = []
        for index in range(extra_pins):
            path = root/("pin-"+str(index)+".txt")
            path.write_bytes(("inert-pin-"+str(index)).encode())
            paths.append(path)
            extras.append(path)
        pins = {path: dict(bytes=path.stat().st_size, sha256=sha(path.read_bytes())) for path in paths}

        def checker(path):
            self.pins.append(str(path))
            raw = path.read_bytes()
            result = dict(bytes=len(raw), sha256=sha(raw))
            if self.after_pin is not None:
                self.after_pin(path)
            return result

        def bounded_read(path, bound):
            raw = path.read_bytes()
            if len(raw) > bound:
                raise AssertionError("CONTROL_READ_BOUND")
            return raw

        supervisor = SimpleNamespace(pin=checker, bounded_read=bounded_read, supervise=forbidden)
        issuer = object.__new__(V.ReceiptVerifier)
        issuer._closed, issuer._busy, issuer._handles = False, False, {}
        issuer._deadline = time.monotonic()+3600
        issuer._trust_binding = issuer._trust_original_binding = binding
        issuer._trust_module, issuer._trust_origin = T, self.trust_path
        issuer._trust_identity, issuer._trust_domain = domain.identity(), domain
        issuer._image, issuer._foundation, issuer._policy = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
        issuer._caps, issuer._used = (1, 1, 1), [0, 0, 0]
        issuer._install = root
        issuer._manifest = root/"manifest.json"
        issuer._manifest_raw = b'{"inert":true}'
        issuer._manifest.write_bytes(issuer._manifest_raw)
        issuer._loaded_pins, issuer._pins = {}, dict(pins)
        issuer._supervisor, issuer._job = supervisor, object()
        issuer._pin_phase_origin = CODE/"v5/admission/pin_phase.py"
        issuer._profile_id = sha((str(root)+"I").encode())

        mixed = object.__new__(M.MixedDeltaVerifier)
        mixed._owners = mixed._origins = issuer, None
        mixed._profiles = issuer._profile_id, None
        mixed._image, mixed._foundation, mixed._policy = B.RELATION_IMAGE, B.FOUNDATION, B.POLICY
        mixed._aggregate_image = None
        mixed._donor, mixed._A, mixed._Job = issuer, supervisor, issuer._job
        mixed._started, mixed._cpu_started = time.monotonic(), time.process_time()
        mixed._caps = (8, 1024**2, 3600, 3600, 3600, 1024**2, 4096)
        mixed._deadline = issuer._deadline
        mixed._closed = mixed._busy = False
        mixed._used, mixed._observed_worker = [0, 0, 0], 0.0
        mixed._handles, mixed._cache = {}, {}
        mixed._pins, mixed._required_origins = dict(pins), origins(MIXED_MODULES)
        mixed._profile_id = mixed._origin_profile = sha((str(root)+"mixed").encode())
        mixed._output, mixed._owner_raw = root, b'{"inert-owner":true}'
        (root/"owner.json").write_bytes(mixed._owner_raw)

        imports = object.__new__(I.MixedImportSession)
        imports._owners = imports._origins = issuer, None, mixed
        imports._profiles = issuer._profile_id, None, mixed._profile_id
        imports._basis = I.RelationBasis()
        imports._aggregate_image = imports._origin_aggregate_image = None
        imports._deadline = issuer._deadline
        imports._caps, imports._closed = (64, 1024, 128, 4096, 1024**2, 1024**2), False
        imports._calls = imports._submitted_bytes = imports._data_bytes = imports._representation_revision = 0
        imports._sources, imports._receipts, imports._nodes, imports._summaries = {}, {}, {}, {}
        imports._selected, imports._groups, imports._bodies = {}, {}, {}
        imports._sealed = imports._batching = False
        imports._view = imports._view_payload = imports._sealed_state = None
        imports._definition_mode, imports._origin_definition_mode = "eager", None
        imports._required_origins = required
        imports._profile = imports._origin_profile = sha((str(root)+"import").encode())
        self.assertNotIn("_executable", issuer.__dict__)
        self.assertNotIn("_native", mixed.__dict__)
        self.assertEqual((issuer._handles, mixed._handles, mixed._cache, imports._sources), ({}, {}, {}, {}))
        return SimpleNamespace(root=root, domain=domain, binding=binding, issuer=issuer,
            mixed=mixed, imports=imports, pins=pins, extras=extras, checker=checker)

    def test_original_bodies_and_order_are_unchanged(self):
        references = {}
        for relative, expected in REFERENCES.items():
            path = SOURCE/relative
            raw = path.read_bytes()
            self.assertEqual(sha(raw), expected)
            references[relative] = raw
            REFERENCE_READS[relative] = dict(path=str(path), bytes=len(raw), sha256=sha(raw), executed=False)
        self.assertEqual(body(references["runtime_efficient/mixed_claims/receiver.py"],
                              "MixedDeltaVerifier", "_check"),
                         body((CODE/"v5/mixed_claims/receiver.py").read_bytes(),
                              "MixedDeltaVerifier", "_check_phase"))
        self.assertEqual(body(references["interface_views/imports_atomic.py"],
                              "MixedImportSession", "_live_phase"),
                         body((CODE/"v5/mixed_claims/imports_atomic.py").read_bytes(),
                              "MixedImportSession", "_live_phase"))
        self.observe(exact_check_body_and_order=True, exact_import_body_and_order=True,
                     predecessor_sources_only_parsed=True)

    def test_actual_standalone_real_reads_are_scoped(self):
        rows = []
        for extra in (1, 7):
            f = self.fixture(extra)
            self.reset()
            # The exact unchanged predecessor body, not an old suite or import.
            f.mixed._check_phase()
            ordinary = dict(trust=len(self.reads), pins=len(self.pins), guards=dict(self.guards))
            self.reset()
            f.mixed._check()
            self.assertEqual(len(self.reads), 4)
            self.assertEqual(len(self.resolves), 2)
            self.assertEqual(Counter(self.pins), Counter({str(path): 2 for path in f.pins}))
            self.assertGreater(ordinary["trust"], len(self.reads))
            self.assertGreater(self.guards["mixed"], ordinary["guards"]["mixed"])
            self.assertFalse(f.mixed._closed)
            self.assertEqual(f.mixed._handles, {})
            rows.append(dict(distinct_pins=len(f.pins), unphased=ordinary,
                phased=dict(trust=len(self.reads), pins=len(self.pins), guards=dict(self.guards)),
                real_trust_origin_resolves=len(self.resolves)))
            self.assert_restored()
        self.observe(cases=rows, unchanged_body_comparison=True, cpu_speedup_claim=False)

    def test_actual_import_borrows_original_owner_once(self):
        f = self.fixture()
        self.reset()
        f.imports._live()
        self.assertEqual(len(self.bodies), 1)
        event = self.bodies[0]
        self.assertTrue(event["completed"])
        self.assertIs(event["owner"], f.mixed)
        self.assertEqual(event["phase"].borrowers, (f.mixed,))
        self.assertFalse(event["view"].open)
        self.assertFalse(event["phase"].open)
        self.assertEqual(event["phase"].records, {})
        self.assertEqual(Counter(self.pins), Counter({str(path): 2 for path in f.pins}))
        self.assertEqual(len(self.reads), 6)
        self.assertEqual(len(self.resolves), 2)
        self.assertFalse(f.imports._closed or f.mixed._closed or f.issuer._closed)
        self.observe(distinct_pins=len(f.pins), real_pin_reads=len(self.pins),
            real_trust_reads=len(self.reads), trust_origin_resolves=len(self.resolves),
            mixed_checks=len(self.bodies), single_root_and_final_sweep=True,
            empty_source_inventory_no_mathematical_handles=True)

    def test_supplied_deadline_at_first_final_and_borrowed_pin(self):
        rows = []
        for mode in ("first", "final", "borrowed"):
            f = self.fixture(1)
            self.reset()
            now = [time.monotonic()]
            tight = now[0]+10
            watched = f.extras[0]
            point = 2 if mode == "final" else 1

            def expire(path):
                if path == watched and self.pins.count(str(path)) == point:
                    now[0] = tight

            self.after_pin = expire
            try:
                with patch.object(time, "monotonic", lambda: now[0]):
                    with self.assertRaisesRegex(Exception, "MIXED_ORIGINAL_DEADLINE"):
                        if mode == "borrowed":
                            with PP.phase(f.issuer._active, borrowers=(f.mixed,)):
                                f.mixed._check(tight)
                        else:
                            f.mixed._check(tight)
            finally:
                self.after_pin = None
            self.assertTrue(f.mixed._closed)
            self.assertLess(tight, f.issuer._deadline)
            self.assertTrue(self.deadlines and all(value == tight for value in self.deadlines))
            self.assertEqual(f.mixed._handles, {})
            rows.append(dict(point=mode, supplied_deadline=tight,
                broader_owner_deadline=f.issuer._deadline, original_body_completed=self.bodies[0]["completed"]))
            self.assert_restored()
        self.observe(cases=rows, all_added_mixed_callbacks_use_supplied_deadline=True,
                     simulated_clock_no_sleep=True)

    def test_original_binding_denial_profile_and_cpu_guards_remain(self):
        rows = []
        errors = {"binding": "ADMISSION_ORIGINAL_TRUST_BINDING",
                  "withdrawal": "TRUST_DENIAL_LATCHED", "profile": "MIXED_PROFILE_CHANGED",
                  "cpu": "MIXED_CONTROLLER_CPU", "origin": "MIXED_CLOSED_OR_CHANGED_ORIGIN"}
        for mode, message in errors.items():
            f = self.fixture(1)
            other_binding = f.domain.bind()
            self.reset()

            def change(path):
                if path != f.extras[0] or self.pins.count(str(path)) != 1:
                    return
                if mode == "binding":
                    f.issuer._trust_binding = other_binding
                elif mode == "withdrawal":
                    f.domain.withdraw("inert focused-control withdrawal")
                elif mode == "profile":
                    f.mixed._profile_id = "ff"*32
                elif mode == "cpu":
                    f.mixed._cpu_started = -1000000
                else:
                    f.mixed._owners = None, None

            self.after_pin = change
            try:
                with self.assertRaisesRegex(Exception, message):
                    f.mixed._check()
            finally:
                self.after_pin = None
            self.assertTrue(f.mixed._closed)
            self.assertFalse(self.bodies[0]["completed"])
            rows.append(dict(change=mode, refused=True, mixed_revoked=True, real_trust_reads=len(self.reads)))
            self.assert_restored()
        self.observe(cases=rows, actual_original_active_methods_delegated=True)

    def test_wrong_owner_unregistered_and_default_nesting_are_independent(self):
        rows = []
        for mode in ("wrong-owner", "unregistered", "default-nested"):
            f = self.fixture(1)
            path = f.extras[0]
            expected = f.pins[path]
            registration = (object(),) if mode == "wrong-owner" else ()
            self.reset()
            with PP.phase(f.issuer._active, borrowers=registration):
                outer = PP._CURRENT.get()
                self.assertTrue(PP.check_pin(f.checker, path, expected))
                manager = (PP.phase(f.issuer._active) if mode == "default-nested" else
                    PP.borrow_or_phase(f.issuer._active, owner=f.mixed))
                with manager:
                    inner = PP._CURRENT.get()
                    self.assertIsNot(inner.phase, outer.phase)
                    self.assertTrue(PP.check_pin(f.checker, path, expected))
                self.assertIs(PP._CURRENT.get(), outer)
                self.assertTrue(PP.check_pin(f.checker, path, expected))
            self.assertEqual(self.pins.count(str(path)), 4)
            self.assertFalse(inner.open or outer.open)
            rows.append(dict(mode=mode, real_pin_reads=4, independent_phases=True,
                             real_trust_reads=len(self.reads)))
            self.assert_restored()
        self.observe(cases=rows)

    def test_copied_root_and_borrow_views_expire(self):
        f = self.fixture(1)
        path, expected = f.extras[0], f.pins[f.extras[0]]
        owner = object()
        self.reset()
        with PP.phase(lambda: None, borrowers=(owner,)):
            root_view = PP._CURRENT.get()
            root_copy = copy_context()
            self.assertTrue(PP.check_pin(f.checker, path, expected))
            with PP.borrow_or_phase(lambda: None, owner=owner):
                borrowed = PP._CURRENT.get()
                borrowed_copy = copy_context()
                self.assertIs(borrowed.phase, root_view.phase)
                self.assertTrue(PP.check_pin(f.checker, path, expected))
            self.assertTrue(root_view.open)
            with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_CLOSED"):
                borrowed_copy.run(PP.check_pin, f.checker, path, expected)
            self.assertTrue(PP.check_pin(f.checker, path, expected))
        for context in (root_copy, borrowed_copy):
            with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_CLOSED"):
                context.run(PP.check_pin, f.checker, path, expected)

            def enter_closed():
                with PP.borrow_or_phase(lambda: None, owner=owner):
                    self.fail("CLOSED_CONTEXT_WAS_REVIVED")

            with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_CLOSED"):
                context.run(enter_closed)
        self.assertEqual(root_view.phase.records, {})
        self.assertEqual(self.pins.count(str(path)), 2)
        self.observe(real_pin_reads=2, copied_borrow_refuses_while_root_live=True,
            both_copies_refuse_after_root_closure=True, permissive_callbacks_do_not_bypass_lifetime=True)

    def test_borrowed_pin_conflicts_and_registration_shape(self):
        f = self.fixture(1)
        path, expected = f.extras[0], f.pins[f.extras[0]]
        self.reset()
        for registration in ([f.mixed], (None,)):
            with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_BORROWER_IDENTITIES"):
                with PP.phase(f.issuer._active, borrowers=registration):
                    self.fail("INVALID_REGISTRATION_ACCEPTED")
        with PP.phase(f.issuer._active, borrowers=(f.mixed,)):
            outer = PP._CURRENT.get()
            self.assertTrue(PP.check_pin(f.checker, path, expected))
            with PP.borrow_or_phase(f.issuer._active, owner=f.mixed):
                self.assertIs(PP._CURRENT.get().phase, outer.phase)
                with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_CHECKER_CONFLICT"):
                    PP.check_pin(lambda selected: f.checker(selected), path, expected)
                with self.assertRaisesRegex(PP.PinPhaseError, "PIN_PHASE_EXPECTED_CONFLICT"):
                    PP.check_pin(f.checker, path, {**expected, "bytes": expected["bytes"]+1})
                self.assertTrue(PP.check_pin(f.checker, path, expected))
        self.assertEqual(self.pins.count(str(path)), 2)
        self.observe(checker_and_expected_conflicts_refused=True, tuple_shape_required=True,
                     good_record_not_overwritten=True, real_pin_reads=2)

    def test_deferred_pin_trust_origin_failure_revokes_correct_owners(self):
        rows = []
        for enclosing in (False, True):
            for mode in ("pin", "withdrawn-marker", "adoption-record", "origin-exception"):
                f = self.fixture(1)
                self.reset()

                def mutate(path):
                    if path != f.extras[0] or self.pins.count(str(path)) != 1:
                        return
                    if mode == "pin":
                        path.write_bytes(b"changed inert local pin")
                    elif mode == "withdrawn-marker":
                        (f.root/"trust/WITHDRAWN").write_bytes(b"")
                    elif mode == "adoption-record":
                        record = f.root/"trust/ADOPTION.json"
                        record.write_bytes(record.read_bytes()+b"\n")

                def fail_final_origin(path, resolved):
                    state = PP._ORIGIN_PHASE.get()
                    if mode == "origin-exception" and state is not None and state.finalizing:
                        raise OSError("CONTROL_AFTER_REAL_FINAL_ORIGIN_RESOLVE")

                messages = {"pin": "PIN_PHASE_FINAL_PIN_CHANGED", "withdrawn-marker": "TRUST_WITHDRAWN",
                            "adoption-record": "TRUST_ADOPTION_CHANGED",
                            "origin-exception": "CONTROL_AFTER_REAL_FINAL_ORIGIN_RESOLVE"}
                self.after_pin, self.after_resolve = mutate, fail_final_origin
                try:
                    with self.assertRaisesRegex(Exception, messages[mode]):
                        f.imports._live() if enclosing else f.mixed._check()
                finally:
                    self.after_pin = self.after_resolve = None
                self.assertTrue(self.bodies and self.bodies[0]["completed"])
                self.assertTrue(f.mixed._closed)
                self.assertEqual(f.mixed._handles, {})
                self.assertEqual(f.mixed._cache, {})
                if enclosing:
                    self.assertTrue(f.imports._closed)
                    self.assertEqual(f.imports._sources, {})
                # The extra finalization cleanup does not close an independent I owner.
                self.assertFalse(f.issuer._closed)
                if mode in ("withdrawn-marker", "adoption-record"):
                    self.assertTrue(f.domain._denied)
                rows.append(dict(enclosing_import=enclosing, failure=mode,
                    mixed_body_completed=True, mixed_revoked=True,
                    import_closed=f.imports._closed, independent_issuer_not_closed=True))
                self.assert_restored()
        self.observe(cases=rows, origin_exception_follows_real_filesystem_resolution=True,
                     no_native_or_mathematical_authority=True)

    def test_body_failure_preserves_prior_revocation_and_restores_outer(self):
        f = self.fixture(1)
        f.imports._required_origins["mixed_claims"] = f.root/"wrong-origin.py"
        with self.assertRaisesRegex(Exception, "MIXED_IMPORT_LOADED_SOURCE_ORIGIN"):
            f.imports._live()
        self.assertTrue(f.imports._closed)
        self.assertFalse(f.mixed._closed or f.issuer._closed)
        self.assert_restored()

        original = self.fixture(1)
        substitute = self.fixture(1)
        original.imports._owners = original.issuer, None, substitute.mixed
        with self.assertRaisesRegex(Exception, "MIXED_IMPORT_CLOSED_CHANGED_OR_EXPIRED"):
            original.imports._live()
        self.assertFalse(original.mixed._closed or substitute.mixed._closed)
        self.assertTrue(original.imports._closed)
        self.assert_restored()

        failing = self.fixture(1)
        outer = self.fixture(1)
        path, expected = outer.extras[0], outer.pins[outer.extras[0]]
        failing.mixed._profile_id = "ff"*32
        self.reset()
        with PP.phase(outer.issuer._active):
            root_view = PP._CURRENT.get()
            root_trust, root_origins = T._VALIDATION_PHASE.get(), PP._ORIGIN_PHASE.get()
            self.assertTrue(PP.check_pin(outer.checker, path, expected))
            with self.assertRaisesRegex(Exception, "MIXED_PROFILE_CHANGED"):
                failing.mixed._check()
            self.assertIs(PP._CURRENT.get(), root_view)
            self.assertIs(T._VALIDATION_PHASE.get(), root_trust)
            self.assertIs(PP._ORIGIN_PHASE.get(), root_origins)
            self.assertTrue(PP.check_pin(outer.checker, path, expected))
        self.assertTrue(failing.mixed._closed)
        self.assertFalse(outer.issuer._closed)
        self.assertEqual(self.pins.count(str(path)), 2)
        self.assert_restored()
        outer.mixed._check()
        self.assertFalse(outer.mixed._closed)
        self.observe(body_only_import_failure_does_not_revoke_mixed=True,
            substituted_owner_never_borrowed_or_revoked=True,
            all_three_outer_contexts_restored=True, fresh_independent_check_succeeds=True)


SELECTED = (
    "test_original_bodies_and_order_are_unchanged",
    "test_actual_standalone_real_reads_are_scoped",
    "test_actual_import_borrows_original_owner_once",
    "test_supplied_deadline_at_first_final_and_borrowed_pin",
    "test_original_binding_denial_profile_and_cpu_guards_remain",
    "test_wrong_owner_unregistered_and_default_nesting_are_independent",
    "test_copied_root_and_borrow_views_expire",
    "test_borrowed_pin_conflicts_and_registration_shape",
    "test_deferred_pin_trust_origin_failure_revokes_correct_owners",
    "test_body_failure_preserves_prior_revocation_and_restores_outer",
)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_NATIVE_OR_NETWORK_OR_RECEIVE_CALL")
    raise AssertionError("FORBIDDEN_NATIVE_OR_NETWORK_OR_RECEIVE_CALL")


def main():
    global OUTPUT, CODE, C, T, PP, V, M, I, B
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or OUTPUT.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    CODE = stage_sources(OUTPUT)
    with ExitStack() as guard:
        for target, name in ((subprocess, "Popen"), (os, "system"), (socket.socket, "__init__")):
            guard.enter_context(patch.object(target, name, forbidden))
        C = importlib.import_module("modules.codec")
        T = importlib.import_module("admission.trust")
        PP = importlib.import_module("admission.pin_phase")
        V = importlib.import_module("admission.verifier")
        M = importlib.import_module("mixed_claims.receiver")
        I = importlib.import_module("mixed_claims.imports_atomic")
        B = importlib.import_module("aggregate_claims.bindings")
        for name in IMPORT_MODULES+("admission.trust",):
            module = sys.modules.get(name)
            if module is None or Path(module.__file__).resolve() != origins((name,))[name]:
                raise ValueError("SELECTED_MODULE_ORIGIN:"+name)
        aggregate = importlib.import_module("aggregate_claims.aggregate_admission")
        for owner in (V.ReceiptVerifier, M.MixedDeltaVerifier, aggregate.AggregateReceiptVerifier):
            guard.enter_context(patch.object(owner, "receive", forbidden))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_V5_STANDALONE_VALIDATION_CONTROLS_V1", status="PASS" if passed else "FAIL",
        scope="ACTUAL_GUARDS_CHECK_LIVE_REAL_LOCAL_TRUST_PINS_NO_MATHEMATICAL_AUTHORITY",
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        selected=list(SELECTED), observations=OBSERVED, sources=SOURCE_COPIES,
        source_only_references=REFERENCE_READS, forbidden_calls=FORBIDDEN,
        native_calls=0, network_calls=0, proof_calls=0, mathematical_acceptance=False)
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
