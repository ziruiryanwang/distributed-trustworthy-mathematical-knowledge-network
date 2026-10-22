"""Focused packet-preflight controls; only root selects and executes this file.

Real parsers and method bodies, one bounded loopback exchange, explicit doubles
for failure injection and mathematical authority. No verifier/prover execution.
"""
import asyncio
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import MethodType, SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MAP = PROJECT/"experiments/v5-local-checks/distribution-exact-packet-01-input.json"
MAP_SHA = "328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561"
SELF = "software/v5/candidate_preflight/controls.py"
OVERLAYS = {
    "v5/delta/custody.py": "software/v5/offer_enumeration/delta/custody.py",
    "v5/admission/clean_refusal.py": "software/v5/candidate_admission/admission/clean_refusal.py",
    "v5/admission/verifier.py": "software/v5/candidate_admission/admission/verifier.py",
    "v5/aggregate_claims/aggregate_admission.py": "software/v5/candidate_admission/aggregate_claims/aggregate_admission.py",
    "v5/evidence_network/transport.py": "software/v5/candidate_preflight/evidence_network/transport.py",
    "v5/client/workspace_evidence.py": "software/v5/candidate_preflight/client/workspace_evidence.py",
    "v5/client/managed_owner.py": "software/v5/candidate_preflight/client/managed_owner.py",
}
SELECTED = (
    "test_01_real_parser_policy_boundary",
    "test_02_resource_and_exception_chains_are_fatal",
    "test_03_strict_exchange_closure",
    "test_04_original_transfer_accounting_and_binding",
    "test_05_public_trial_noninterference_and_fatal_boundaries",
)
OBSERVED, FORBIDDEN, SOURCE_ROWS = {}, [], {}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def entry(raw):
    return dict(packet_sha256=sha(raw), packet_bytes=len(raw))


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not part.is_symlink() and not part.is_junction() for part in (path, *path.parents)),
        "PREFLIGHT_CONTROL_ORDINARY")
    return path


def write_new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_PROCESS")
    raise AssertionError(FORBIDDEN[-1])


def stage(output):
    selection = json.loads((output/"selection.json").read_bytes())
    pins, snapshot = selection["sources"], output/"sources"
    need(len(pins) == 138 and Path(__file__).resolve() == snapshot/SELF,
         "PREFLIGHT_CONTROL_EXACT_SNAPSHOT")
    need(sha((snapshot/SELF).read_bytes()) == pins[SELF], "PREFLIGHT_CONTROL_SELF_PIN")
    raw = ordinary(MAP).read_bytes()
    need(len(raw) == 2813358 and sha(raw) == MAP_SHA, "PREFLIGHT_CONTROL_MAP_PIN")
    basis = json.loads(raw)["sdk_sources"]
    need(len(basis) == 129 and not set(OVERLAYS)-set(basis)-{"v5/admission/clean_refusal.py"},
         "PREFLIGHT_CONTROL_OVERLAY_KEYS")
    code = output/"selected-code"; code.mkdir()
    for logical in sorted(set(basis) | set(OVERLAYS)):
        if logical in OVERLAYS:
            relative = OVERLAYS[logical]; expected = pins[relative]
        else:
            row = basis[logical]
            relative = Path(row["path"]).relative_to(PROJECT).as_posix()
            expected = row["sha256"]
            need(pins[relative] == expected, "PREFLIGHT_CONTROL_BASE_PIN")
        data = ordinary(snapshot/relative).read_bytes()
        need(0 < len(data) <= 2*1024**2 and sha(data) == expected, "PREFLIGHT_CONTROL_SOURCE_PIN")
        target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, data)
        need(target.read_bytes() == data, "PREFLIGHT_CONTROL_READBACK")
        SOURCE_ROWS[logical] = dict(source=relative, bytes=len(data), sha256=expected)
    need(len(SOURCE_ROWS) == 130 and not any(name in sys.modules for name in
         ("admission", "aggregate_claims", "client", "modules")), "PREFLIGHT_CONTROL_IMPORT_ORDER")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]


def mathematical_data(name="preflightFixture"):
    """Structurally valid invented mathematics, never certified or claimed true."""
    spec = dict(schema=C.SPEC_SCHEMA, foundation=B.FOUNDATION, policy=B.POLICY,
        groups=[dict(kind="ordinary", declarations=[dict(name=[["s", name]], kind="theorem",
            universes=0, type=["sort", ["zero"]], value_hash=None, meta={})])])
    summary = C.summarize(spec)
    exact = EXPECTED(summary, 0, B.RELATION_IMAGE)
    image = "11"*32
    envelope = ENV(packet_bytes=65536, witness_bytes=32768, receipt_bytes=4096)
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")+bytes.fromhex(image)
        +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
        +B.commitment([exact])+(1).to_bytes(4, "little")+(0).to_bytes(8, "little")
        +(1).to_bytes(8, "little"))
    raw_i = EP.pack_terminal_i(exact, b"\0", aggregate_image=image, envelope=envelope,
                               terminal_receipt_bytes=4096, terminal_i=True)
    raw_a = EP.pack_terminal(header, exact, 0, [], b"\0", aggregate_image=image,
                             envelope=envelope, terminal_receipt_bytes=4096)
    image_words = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4], "little")
                   for i in range(0, 32, 4)]
    mixed = C.canonical(dict(schema=MP.SCHEMA, claims=[], frontiers=[], deltas=[dict(
        schema="DMKN_CERTIFIED_MODULES_V2", image=image_words, rank=0, local_spec=spec,
        rows=[], parents=[], bodies=[])]))
    return SimpleNamespace(spec=spec, summary=summary, exact=exact, image=image,
        envelope=envelope, header=header, raw_i=raw_i, raw_a=raw_a, mixed=mixed,
        profile=EC.public_profile(image, terminal_i=True), module=C.summary_id(summary))


def preflight(data, raw, selected=None, summary=None, **overrides):
    kwargs = dict(envelope=data.envelope, aggregate_image=data.image,
                  terminal_receipt_bytes=4096, terminal_i=True)
    kwargs.update(overrides)
    return ET.preflight_packet(raw, entry(raw) if selected is None else selected,
        data.summary if summary is None else summary, **kwargs)


def acquisition_fixture(data):
    """Real acquisition/budget/contact classes, inert in-memory custody doubles."""
    budget = AB(time.monotonic()+60, dict(requests=8, reply_bytes=1024**2,
        verify_attempts=4, verification_input_bytes=65536, worker_cpu_seconds=20))
    policy = P.OwnerEgressPolicy(dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
        public_ports=[], test_endpoints=[dict(host="127.0.0.1", port=45991)]))
    endpoint = policy.endpoint(dict(host="127.0.0.1", port=45991, tls=False, server_name=None))
    contact = CONTACT(endpoint, budget.deadline, policy, budget)
    modules = MS.__new__(MS); modules.foundation, modules.policy = B.FOUNDATION, B.POLICY
    opening = C.group_opening(data.spec, 0); descriptor = opening["group"]["declarations"][0]
    modules.get_group = lambda module, name, index=None: (deepcopy(opening), deepcopy(descriptor))
    packets = EC.PacketStore.__new__(EC.PacketStore)
    packets.profile, packets.profile_id = deepcopy(data.profile), EC.profile_id(data.profile)
    packets.envelope, packets.terminal_receipt_bytes = data.envelope, 4096
    packets.limits = dict(packet_bytes=65536)
    held, puts = {}, []
    def put(module, raw, *, before_commit=None):
        packets.inspect(module, raw)
        if before_commit is not None: before_commit()
        puts.append((module, raw)); held[(sha(raw), len(raw))] = raw
    packets.put = put
    packets.get = lambda digest, size: held[(digest, size)]
    adapter = SimpleNamespace(foundation=B.FOUNDATION, policy=B.POLICY, codec=C)
    acquisition = ET.EvidenceAcquisition(adapter, {"selected": contact}, data.profile,
                                         budget, modules, packets)
    resolved = dict(locator=dict(module_id=data.module, relative_name=[["s", "preflightFixture"]],
                                 group_index=0), opening=opening, descriptor=descriptor)
    return SimpleNamespace(acquisition=acquisition, budget=budget, contact=contact,
        packets=packets, modules=modules, held=held, puts=puts, resolved=resolved)


def facade_fixture(data):
    """Actual facade methods/parser; explicit inert issuer and authority guards."""
    f = acquisition_fixture(data)
    candidate, old_token, old_handle = object(), object(), object()
    session, context, view = object(), object(), object()
    staged = {object(): (b"preserved-staged-bytes", False)}
    calls, inputs, fatal, issued = [], [], [], {}
    client = SimpleNamespace(_receipt_cache={}, _aggregate_cache={}, _packet_cache={},
        _profiles=("explicit-I-double", "explicit-A-double", "explicit-mixed-double"),
        _aggregate_image=data.image, _counts=dict(admission_submissions=0, same_live_hits=0),
        _warrants={}, _session=session, _context=context, _selection_view=view, _staged=staged,
        _busy=False, _budget=f.budget, _acquisition=f.acquisition,
        grant=SimpleNamespace(directory=OUTPUT/"inert-issuer-output", deadline=f.budget.deadline,
            remaining_seconds=lambda: 30, _cpu=time.process_time(), _limits={"controller_cpu_seconds": 30}),
        workspace=SimpleNamespace(packets=f.packets, modules=f.modules, _envelope=data.envelope,
            config=dict(wire_profile=deepcopy(data.profile), terminal_receipt_bytes=4096)))
    class Issuer:
        def __init__(self, kind):
            self.kind, self._deadline, self.refuse = kind, f.budget.deadline, False
        def try_receive(self, raw, statement, output, **limits):
            calls.append((self.kind, "trial", raw))
            return None if self.refuse else object()
        def receive(self, raw, statement, output, **limits):
            calls.append((self.kind, "strict", raw))
            if self.refuse: raise ValueError("EXPLICIT_STRICT_ISSUER_REFUSAL")
            return object()
        def select_member(self, handle, journal, index, siblings): return handle
        def open_group(self, handle, opening): return C.verify_group_opening(data.module, opening)
    client.receipt, client.aggregate = Issuer("I"), Issuer("A-member")
    client.delta = SimpleNamespace(_deadline=f.budget.deadline)
    client._origin_owners = (client.receipt, client.aggregate, client.delta, None)
    def issue(kind, handle, raw):
        token = object()
        live = dict(module=data.module, summary=data.summary, journal=data.exact,
            profile_id=client._profiles[0 if kind == "I" else 1], receipt_sha256=sha(raw))
        issued[token] = kind, handle, raw, live
        client._warrants[token] = issued[token]
        return token
    prior = dict(module=data.module, summary=data.summary, journal=data.exact,
                 profile_id=client._profiles[0], receipt_sha256=sha(b"\0"))
    issued[old_token] = "I", old_handle, b"\0", prior
    client._warrants[old_token] = issued[old_token]
    client._issue, client._warrant = issue, lambda token: issued[token]
    client._aggregate_fact = lambda handle, raw, header: dict(header=header,
        receipt_sha256=sha(raw), receipt_bytes=len(raw), profile_id=client._profiles[1])
    client._candidate = lambda value: ("selected", f.resolved) if value is candidate else (
        (_ for _ in ()).throw(ValueError("EXPLICIT_FOREIGN_CANDIDATE")))
    client._charge = inputs.append
    client._store = lambda method, *args: method(*args)
    client._body_attempt_sources = lambda: None  # Explicit origin-guard double only.
    client._active = f.acquisition._active
    client._census = lambda: None
    client._enter = lambda: setattr(client, "_busy", True)
    client._fail = fatal.append
    for name in ("_inspect", "_expected", "_admit_i", "_admit_a_member", "_admit_evidence", "_acquire_packet"):
        setattr(client, name, MethodType(getattr(FE.CommonsClient, name), client))
    client._terminal_trial_result = FE.CommonsClient._terminal_trial_result
    f.client, f.candidate, f.calls, f.inputs, f.fatal = client, candidate, calls, inputs, fatal
    f.old_token, f.old_handle = old_token, old_handle
    f.originals = (session, context, view, staged)
    return f


def response(raw, status=200):
    return dict(status=status, raw=raw, request_bytes=100, reply_bytes=len(raw), header_bytes=150, elapsed_ms=0)


class Controls(unittest.TestCase):
    def test_01_real_parser_policy_boundary(self):
        data = mathematical_data()
        snapshots = deepcopy(data.__dict__)
        for raw, kind in ((data.raw_i, "terminal-i"), (data.raw_a, "terminal"), (data.mixed, "mixed")):
            result = preflight(data, raw)
            self.assertEqual(result["status"], "CANDIDATE_PREFLIGHT_PASSED")
            self.assertEqual(result["evidence_kind"], kind)
            self.assertEqual(result["journal"], data.exact)
            self.assertEqual(result["summary"], data.summary)
        malformed = [b"{", b'{"schema":"x","schema":"x"}', b'{ "schema":"x"}',
                     C.canonical(dict(schema="unknown-future-form"))]
        changed = C.parse_json(data.raw_i); changed["journal"][0] ^= 1
        malformed.append(C.canonical(changed))
        changed = C.parse_json(data.raw_i); changed["receipt_hex"] = "GG"
        malformed.append(C.canonical(changed))
        changed = C.parse_json(data.raw_a); changed["header"][140] ^= 1
        malformed.append(C.canonical(changed))
        malformed.append(C.canonical(dict(schema=MP.SCHEMA, claims=[], frontiers=[], deltas=[])))
        for index, raw in enumerate(malformed):
            with self.subTest(case=index):
                result = preflight(data, raw)
                self.assertEqual(result["status"], "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY")
                self.assertIs(result["mathematical_acceptance"], False)
                self.assertNotIn("warrant", result)
        wrong = entry(data.raw_i); wrong["packet_sha256"] = "00"*32
        self.assertEqual(preflight(data, data.raw_i, wrong)["status"],
                         "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY")
        other = mathematical_data("differentTarget")
        self.assertEqual(preflight(data, other.raw_i)["status"],
                         "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY")
        self.assertEqual(preflight(data, data.raw_i, terminal_i=False)["status"],
                         "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY")
        for overrides in (dict(aggregate_image="invalid"), dict(terminal_receipt_bytes=0),
                          dict(terminal_i=1), dict(envelope=replace(data.envelope, depth=0))):
            with self.assertRaises((C.StructureError, DP.DeltaError, ValueError)):
                preflight(data, data.raw_i, **overrides)
        with self.assertRaises((C.StructureError, ValueError)):
            preflight(data, data.raw_i, selected={"packet_sha256": "bad", "packet_bytes": len(data.raw_i)})
        self.assertEqual(data.__dict__, snapshots)
        OBSERVED[self._testMethodName] = dict(real_parser=True, valid_forms=3,
            malformed_forms=len(malformed), wrong_hash_target_and_disabled_i=True,
            trusted_argument_failures_fatal=True, mathematical_acceptance=False)

    def test_02_resource_and_exception_chains_are_fatal(self):
        data = mathematical_data()
        class UnexpectedStructure(C.StructureError):
            pass
        errors = [MemoryError("injected"), RecursionError("injected"),
                  RuntimeError("injected"), UnexpectedStructure("injected")]
        for inner in (MemoryError("chained"), RecursionError("chained"),
                      RuntimeError("unknown"), OSError("owner-error")):
            for slot in ("__cause__", "__context__"):
                outer = C.StructureError("explicit-injected-wrapper")
                setattr(outer, slot, inner); errors.append(outer)
        cyclic = C.StructureError("cycle"); cyclic.__cause__ = cyclic; errors.append(cyclic)
        for index, error in enumerate(errors):
            def injected(*args, **kwargs): raise error
            # Satisfy the explicit alias identity guard; this is disclosed injection.
            with self.subTest(case=index), patch.object(ET, "inspect_evidence", new=injected), \
                    patch.object(EP, "inspect_evidence", new=injected):
                with self.assertRaises(BaseException) as caught:
                    preflight(data, data.raw_i)
                self.assertIs(caught.exception, error)
        # These are deliberate typed parser failures, not verifier responses.
        for error in (C.StructureError("declared-bound"), DP.DeltaError("RESOURCE_INCOMPLETE", "declared-bound")):
            def injected(*args, **kwargs): raise error
            with patch.object(ET, "inspect_evidence", new=injected), patch.object(EP, "inspect_evidence", new=injected):
                self.assertEqual(preflight(data, data.raw_i)["status"],
                                 "CANDIDATE_REJECTED_UNDER_SELECTED_POLICY")
        OBSERVED[self._testMethodName] = dict(scope="EXPLICIT_PARSER_EXCEPTION_INJECTION",
            fatal_cases=len(errors), typed_policy_cases=2, no_actual_resource_exhaustion=True)

    def test_03_strict_exchange_closure(self):
        async def scenario():
            raw = b"{}"; selected = entry(raw)
            server_errors, finished = [], asyncio.Event()
            async def serve(reader, writer):
                try:
                    head = await reader.readuntil(b"\r\n\r\n")
                    lengths = [line.split(b":", 1)[1].strip() for line in head.split(b"\r\n")
                               if line.lower().startswith(b"content-length:")]
                    need(len(lengths) == 1, "CONTROL_REQUEST_LENGTH")
                    request = await reader.readexactly(int(lengths[0]))
                    need(json.loads(request) == selected, "CONTROL_REQUEST_BINDING")
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n"
                                 b"Content-Type: application/octet-stream\r\nConnection: close\r\n\r\n"+raw)
                    await writer.drain()
                except BaseException as error:
                    server_errors.append(type(error).__name__+":"+str(error))
                finally:
                    try:
                        writer.close()
                        async with asyncio.timeout(1): await writer.wait_closed()
                    except BaseException as error:
                        server_errors.append("closure:"+type(error).__name__)
                    finished.set()
            server = await asyncio.start_server(serve, "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]
            policy = P.OwnerEgressPolicy(dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
                public_ports=[], test_endpoints=[dict(host="127.0.0.1", port=port)]))
            endpoint = policy.endpoint(dict(host="127.0.0.1", port=port, tls=False, server_name=None))
            try:
                result = await ET._exchange_packet_settled(endpoint, selected,
                    timeout_ms=2000, deadline=time.monotonic()+3)
                self.assertEqual(result["raw"], raw); self.assertEqual(result["status"], 200)
                async with asyncio.timeout(2): await finished.wait()
                self.assertEqual(server_errors, [])
            finally:
                server.close(); await server.wait_closed()
            cases = ("normal", "close_error", "wait_error", "wait_cancel", "wait_timeout", "bad_length")
            for mode in cases:
                reader = asyncio.StreamReader()
                count = 3 if mode == "bad_length" else 2
                reader.feed_data(b"HTTP/1.1 200 OK\r\nContent-Length: "+str(count).encode()+b"\r\n"
                    b"Content-Type: application/octet-stream\r\nConnection: close\r\n\r\n"+raw)
                reader.feed_eof()
                events = []
                injected = (asyncio.CancelledError("INJECTED_WAIT_CANCEL") if mode == "wait_cancel"
                    else RuntimeError("INJECTED_"+mode.upper()))
                class Writer:
                    def write(self, data): events.append("write")
                    async def drain(self): events.append("drain")
                    def close(self):
                        events.append("close")
                        if mode == "close_error": raise injected
                    async def wait_closed(self):
                        events.append("wait")
                        if mode in ("wait_error", "wait_cancel"): raise injected
                        if mode == "wait_timeout": await asyncio.Event().wait()
                writer = Writer()
                async def connect(*args, **kwargs): return reader, writer
                deadline = time.monotonic()+(0.02 if mode == "wait_timeout" else 2)
                with patch.object(asyncio, "open_connection", new=connect):
                    if mode == "normal":
                        result = await ET._exchange_packet_settled(endpoint, selected,
                            timeout_ms=1000, deadline=deadline)
                        self.assertEqual(result["raw"], raw); self.assertIn("wait", events)
                    else:
                        expected_type = (asyncio.CancelledError if mode == "wait_cancel"
                            else ValueError if mode == "bad_length" else ET.PacketCleanupError)
                        with self.assertRaises(expected_type) as caught:
                            await ET._exchange_packet_settled(endpoint, selected,
                                timeout_ms=1000, deadline=deadline)
                        self.assertIn("close", events)
                        if mode != "close_error": self.assertIn("wait", events)
                        if mode == "wait_cancel": self.assertIs(caught.exception, injected)
                        elif mode == "bad_length":
                            self.assertEqual(str(caught.exception), "DELTA_HTTP_EXACT_CONTENT_LENGTH")
                        else:
                            self.assertEqual(str(caught.exception), "PACKET_SOCKET_CLOSURE_UNCERTAIN")
                            if mode == "wait_timeout":
                                self.assertIs(type(caught.exception.__cause__), TimeoutError)
                            else: self.assertIs(caught.exception.__cause__, injected)
            return len(cases)
        count = asyncio.run(scenario())
        OBSERVED[self._testMethodName] = dict(actual_loopback_successes=1,
            explicit_stream_writer_cases=count, closure_timeout_is_bounded=True,
            no_provider_general_shutdown_claim=True)

    def test_04_original_transfer_accounting_and_binding(self):
        async def scenario():
            data = mathematical_data()
            modes = ("success", "caller_entry_mutation", "closure_error", "cancel", "non200",
                     "contact_expired", "budget_replaced", "profile_changed", "settlement_error")
            for mode in modes:
                f = acquisition_fixture(data); a, budget = f.acquisition, f.budget
                selected = entry(data.raw_i); original = dict(selected); deadlines = (budget.deadline, a.structural.deadline)
                seen = []
                injected = (asyncio.CancelledError("EXPLICIT_TRANSFER_CANCEL") if mode == "cancel"
                    else ET.PacketCleanupError("EXPLICIT_CLOSURE_ERROR"))
                async def exchange(endpoint, request, **kwargs):
                    seen.append((endpoint, dict(request)))
                    self.assertIs(endpoint, f.contact); self.assertEqual(request, original)
                    if mode == "caller_entry_mutation": selected["packet_sha256"] = "00"*32
                    if mode in ("closure_error", "cancel"): raise injected
                    if mode == "contact_expired": f.contact._expires = time.monotonic()-1
                    if mode == "budget_replaced": a.budget = AB(time.monotonic()+60, budget.limits)
                    if mode == "profile_changed": a.profile["foundation"] = "00"*32
                    return response(data.raw_i, 404 if mode == "non200" else 200)
                if mode == "settlement_error":
                    def settle(ticket, count=None):
                        AB.settle(budget, ticket, count)
                        raise ValueError("EXPLICIT_POST_SETTLEMENT_ERROR")
                    budget.settle = settle
                with self.subTest(mode=mode), patch.object(ET, "_exchange_packet_settled", new=exchange):
                    if mode in ("success", "caller_entry_mutation"):
                        raw, bound = await a._trial_packet_bytes("selected", data.module, selected, offered=False)
                        self.assertEqual(raw, data.raw_i); self.assertIs(bound["budget"], budget)
                        ET._packet_trial_unchanged(bound)
                    else:
                        expected_type = (type(injected) if mode in ("closure_error", "cancel") else ValueError)
                        with self.assertRaises(expected_type) as caught:
                            await a._trial_packet_bytes("selected", data.module, selected, offered=False)
                        if mode in ("closure_error", "cancel"):
                            self.assertIs(caught.exception, injected)
                        else:
                            self.assertEqual(str(caught.exception), {
                                "non200": "DELTA_HTTP_ERROR",
                                "contact_expired": "BODY_ATTEMPT_CONTACT_CHANGED",
                                "budget_replaced": "DELTA_ACQUISITION_ORIGIN_OR_CLOSED",
                                "profile_changed": "PACKET_TRIAL_PROFILE_OR_LIMITS_CHANGED",
                                "settlement_error": "EXPLICIT_POST_SETTLEMENT_ERROR"}[mode])
                self.assertEqual(len(seen), 1)
                self.assertIs(seen[0][0], f.contact); self.assertEqual(seen[0][1], original)
                self.assertIsNone(budget.pending)
                self.assertEqual((budget.used["requests"], budget.used["reply_bytes"]), (1, len(data.raw_i)))
                self.assertEqual((budget.used["verify_attempts"], budget.used["verification_input_bytes"]), (0, 0))
                self.assertEqual((a.structural.inflight, a.structural.reserved_bytes), (0, 0))
                self.assertEqual(deadlines, (budget.deadline, a.structural.deadline))
                self.assertEqual(f.puts, []); self.assertEqual(f.held, {})
            f = acquisition_fixture(data)
            with self.assertRaisesRegex(ValueError, "^DELTA_PACKET_NOT_OFFERED_BY_SELECTED_PROVIDER$"):
                await f.acquisition._trial_packet_bytes("selected", data.module, entry(data.raw_i), offered=True)
            self.assertEqual(f.budget.used["requests"], 0)
            return len(modes)
        count = asyncio.run(scenario())
        OBSERVED[self._testMethodName] = dict(scope="REAL_BUDGET_BINDING_AND_METHODS_WITH_EXCHANGE_AND_CUSTODY_DOUBLES",
            charged_cases=count, unoffered_before_dispatch=True, pending_cleared=True,
            no_custody_or_verification=True, deadlines_not_renewed=True)

    def test_05_public_trial_noninterference_and_fatal_boundaries(self):
        async def run_case(mode):
            data = mathematical_data(); f = facade_fixture(data); client = f.client
            raw = b"{" if mode in ("reject", "offered_reject", "census_deadline") else data.raw_i
            if mode == "mixed": raw = data.mixed
            if mode == "aggregate": raw = data.raw_a
            selected = entry(raw); staged_before = dict(client._staged); warrants_before = dict(client._warrants)
            prior_fact_before = deepcopy(client._warrants[f.old_token][3])
            expected = data.exact
            if mode == "exact_j": expected = EXPECTED(data.summary, 1, B.RELATION_IMAGE)
            if mode == "verifier_refusal": client.receipt.refuse = True
            if mode in ("offered_reject", "offered_valid"):
                f.acquisition._offers.add(("selected", data.module, selected["packet_sha256"], selected["packet_bytes"]))
            if mode == "put_error":
                def bad_put(*args, **kwargs): raise C.StructureError("EXPLICIT_STORE_ERROR_NOT_PEER_TRIAGE")
                f.packets.put = bad_put
            if mode == "readback_error": f.packets.get = lambda *args: b"wrong readback"
            if mode == "source_guard":
                def guard(): raise ValueError("EXPLICIT_SOURCE_GUARD_ERROR")
                client._body_attempt_sources = guard
            if mode.startswith("cached_"):
                f.held[(sha(raw), len(raw))] = b"{" if mode == "cached_corrupt" else raw
                key = sha(raw), len(raw), C.canonical(data.summary)
                client._packet_cache[key] = f.old_token
                client._receipt_cache[(sha(b"\0"), 1, C.canonical(data.summary))] = f.old_token
            if mode == "census_deadline":
                client._census = lambda: setattr(client.grant, "deadline", time.monotonic()-1)
            if mode == "cached_pending":
                client._census = lambda: setattr(f.budget, "pending", (99, 1))
            if mode == "cached_inflight":
                client._census = lambda: setattr(f.acquisition.structural, "inflight", 1)
            if mode == "cached_reserved":
                client._census = lambda: setattr(f.acquisition.structural, "reserved_bytes", 1)
            seen = []
            async def exchange(endpoint, request, **kwargs):
                seen.append(dict(request)); return response(raw)
            fatal_expected = {
                "exact_j": (ValueError, "CLIENT_EXPECTED_EXACT_J_MISMATCH"),
                "put_error": (C.StructureError, "EXPLICIT_STORE_ERROR_NOT_PEER_TRIAGE"),
                "readback_error": (ValueError, "DELTA_PACKET_COMMIT_READBACK"),
                "source_guard": (ValueError, "EXPLICIT_SOURCE_GUARD_ERROR"),
                "foreign": (ValueError, "EXPLICIT_FOREIGN_CANDIDATE"),
                "unoffered": (ValueError, "CLIENT_UNOFFERED_PACKET"),
                "cached_corrupt": (C.StructureError, "JSON_DECODE"),
                "cached_pending": (ValueError, "CLIENT_TERMINAL_TRIAL_NETWORK_NOT_SETTLED"),
                "cached_inflight": (ValueError, "CLIENT_TERMINAL_TRIAL_NETWORK_NOT_SETTLED"),
                "cached_reserved": (ValueError, "CLIENT_TERMINAL_TRIAL_NETWORK_NOT_SETTLED"),
                "census_deadline": (ValueError, "CLIENT_TERMINAL_TRIAL_DEADLINE"),
                "strict_malformed": (C.StructureError, "JSON_DECODE"),
                "local_corrupt": (C.StructureError, "JSON_DECODE"),
            }
            with patch.object(ET, "_exchange_packet_settled", new=exchange):
                if mode in fatal_expected:
                    error_type, reason = fatal_expected[mode]
                    with self.assertRaises(error_type) as caught:
                        if mode == "local_corrupt":
                            f.held[(selected["packet_sha256"], selected["packet_bytes"])] = b"{"
                            FE.CommonsClient.try_admit_terminal_local(client, data.module, **selected,
                                expected_exact_journal=expected, receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
                        elif mode == "strict_malformed":
                            malformed = b"{"; bad_selected = entry(malformed)
                            async def strict_exchange(*args, **kwargs): return response(malformed)
                            with patch.object(ET.D, "exchange", new=strict_exchange):
                                await FE.CommonsClient.acquire_exact(client, f.candidate, bad_selected,
                                    receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
                        else:
                            method = FE.CommonsClient.try_acquire_terminal if mode == "unoffered" else FE.CommonsClient.try_acquire_terminal_exact
                            await method(client, object() if mode == "foreign" else f.candidate, selected,
                                expected_exact_journal=expected, receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
                    self.assertIs(type(caught.exception), error_type)
                    self.assertEqual(str(caught.exception), reason)
                    self.assertEqual(len(f.fatal), 1); self.assertFalse(client._busy)
                    self.assertIs(f.fatal[0], caught.exception)
                    if mode == "exact_j": self.assertEqual(f.puts, [])
                    if mode in ("foreign", "unoffered", "source_guard") or mode.startswith("cached_"):
                        self.assertEqual(seen, [])
                else:
                    method = FE.CommonsClient.try_acquire_terminal if mode.startswith("offered_") else FE.CommonsClient.try_acquire_terminal_exact
                    result = await method(client, f.candidate, selected, expected_exact_journal=expected,
                        receipt_cpu_seconds=1, wall_seconds=20, memory_mib=64)
                    status = ("CANDIDATE_REJECTED_UNDER_SELECTED_POLICY" if mode in ("reject", "offered_reject")
                        else "UNSUPPORTED_TRIAL_FORM" if mode == "mixed"
                        else "NOT_ADMITTED" if mode == "verifier_refusal" else "ADMITTED")
                    self.assertEqual(result["status"], status); self.assertEqual(f.fatal, [])
                    self.assertEqual(f.budget.used["requests"], 1)
                    self.assertEqual(f.budget.used["reply_bytes"], len(raw))
                    self.assertEqual(f.inputs.count(raw), 1)
                    self.assertEqual(len(f.puts), 0 if status.startswith("CANDIDATE_REJECTED") else 1)
                    self.assertEqual(len(f.calls), 0 if status in ("CANDIDATE_REJECTED_UNDER_SELECTED_POLICY", "UNSUPPORTED_TRIAL_FORM") else 1)
                    self.assertIs(client._session, f.originals[0]); self.assertIs(client._context, f.originals[1])
                    self.assertIs(client._selection_view, f.originals[2]); self.assertIs(client._staged, f.originals[3])
                    self.assertEqual(client._staged, staged_before)
                    self.assertIs(client._warrants[f.old_token], warrants_before[f.old_token])
                    self.assertEqual(client._warrants[f.old_token][3], prior_fact_before)
                    if status != "ADMITTED": self.assertEqual(client._warrants, warrants_before)
                    self.assertIsNone(f.budget.pending)
                    self.assertEqual((f.acquisition.structural.inflight, f.acquisition.structural.reserved_bytes), (0, 0))
            return mode
        modes = ("reject", "offered_reject", "valid", "offered_valid", "aggregate", "mixed", "verifier_refusal",
                 "exact_j", "put_error", "readback_error", "source_guard", "foreign", "unoffered",
                 "cached_corrupt", "cached_pending", "cached_inflight", "cached_reserved", "census_deadline",
                 "strict_malformed", "local_corrupt")
        for mode in modes:
            with self.subTest(mode=mode): asyncio.run(run_case(mode))
        OBSERVED[self._testMethodName] = dict(scope="REAL_PUBLIC_METHODS_PARSER_AND_BUDGET_WITH_EXPLICIT_AUTHORITY_CUSTODY_GUARD_DOUBLES",
            cases=len(modes), offered_and_exact=True, staged_contents_and_identity_preserved=True,
            expected_j_before_put=True, strict_local_cache_failures_not_recovered=True,
            cached_final_quiescence_refusals=3, cryptographic_verifications=0)


def main():
    global OUTPUT, C, B, EP, EC, ET, MP, DP, ENV, EXPECTED, FE, P, AB, SA, CONTACT, MS
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "PREFLIGHT_CONTROL_OUTPUT")
    OUTPUT = ordinary(Path(sys.argv[2]))
    need(OUTPUT.is_dir() and OUTPUT.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "PREFLIGHT_CONTROL_ISOLATED_WINDOWS")
    stage(OUTPUT)
    with patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden):
        from modules import codec
        from aggregate_claims import bindings
        from evidence_network import packet, custody, transport
        from mixed_claims import packet as mixed_packet
        from delta import packet as delta_packet
        from delta_claims.claims import expected_journal
        from client import workspace_evidence
        from location import protocol
        from transport.receipt_client import AcquisitionBudget, _SharedAcquisition
        from transport.located_receipts import _ExpiringContact
        from custody.module_store import ModuleStore
        C, B, EP, EC, ET = codec, bindings, packet, custody, transport
        MP, DP, ENV, EXPECTED = mixed_packet, delta_packet, mixed_packet.Envelope, expected_journal
        FE, P, AB, SA, CONTACT, MS = workspace_evidence, protocol, AcquisitionBudget, _SharedAcquisition, _ExpiringContact, ModuleStore
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_V5_CANDIDATE_PREFLIGHT_CONTROLS_V1", status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests_run=result.testsRun, failures=len(result.failures),
        errors=len(result.errors), skipped=len(result.skipped), forbidden_calls=FORBIDDEN,
        sources=SOURCE_ROWS, observations=OBSERVED, source_map_sha256=MAP_SHA,
        mathematical_acceptance=False, native_calls=0, proof_calls=0, actual_cryptographic_verifications=0,
        scope="REAL_PARSERS_METHODS_BUDGET_AND_ONE_LOOPBACK_WITH_EXPLICIT_FAILURE_AND_AUTHORITY_DOUBLES")
    write_new(OUTPUT/"candidate-preflight-controls-result.json",
        json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
