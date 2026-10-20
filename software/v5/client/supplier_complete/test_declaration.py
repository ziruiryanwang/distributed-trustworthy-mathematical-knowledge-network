"""Selected declaration-continuation controls; mathematical issuers are INERT.

Borrow fixture constructors, never predecessor suites. Exercise real facade,
original contacts/budget, exact group validation and SQLite custody. One small
loopback control covers supplier absence followed by explicit alternative use.
Helper-only controls use an explicitly inert client. No native/proof runs.
"""
import asyncio
from contextlib import nullcontext
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
import client


def overlay(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE/relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(client, name.rsplit(".", 1)[1], module)
    return module


E = overlay("client.workspace_evidence", "client/supplier_complete/workspace_evidence.py")
overlay("client.workspace_staged", "staging_members/workspace_staged.py")
H = overlay("client.semantic_reader", "client/supplier_complete/semantic_reader.py")
from client import test_direct_contacts as D
from client import test_semantic_reader as T
from client.workspace_atomic import Candidate
from evidence_network.transport import CompositeProvider
from modules import codec as C
from transport import declaration_resilience as R
from transport import http_provider as HTTP

OUTPUT = None
CAP = 65536
OBSERVED = {"real_loopback_requests": 0, "fake_streams": 0,
            "inert_helper_attempts": 0, "inert_warrant_sentinels": 0}
RESULTS = {}


def refusal(supplier, reason, module, name):
    return {"schema": "DMKN_SEMANTIC_DECLARATION_ATTEMPT_V1",
            "status": "UNAVAILABLE_AT_SELECTED_SUPPLIER", "supplier": supplier,
            "reason": reason, "request": {"module_id": module,
                "relative_name": deepcopy(name), "group_index": None},
            "settlement": "FULL_REPLY_RESERVATION_CHARGED",
            "global_complete": False, "mathematical_acceptance": False}


class Writer:
    """Inert stream with no hidden socket/task; records exact route and closure."""
    def __init__(self, cleanup_error=None):
        self.cleanup_error = cleanup_error
        self.sent = bytearray()
        self.closed = self.waits = 0

    def write(self, raw):
        self.sent.extend(raw)

    async def drain(self):
        pass

    def close(self):
        self.closed += 1

    async def wait_closed(self):
        self.waits += 1
        if self.cleanup_error is not None:
            raise self.cleanup_error


def stream(raw=None, *, status=200, cleanup_error=None):
    reader, writer = asyncio.StreamReader(), Writer(cleanup_error)
    if raw is not None:
        reader.feed_data(HTTP._header("HTTP/1.1 "+str(status)+" TEST", len(raw))+raw)
    reader.feed_eof()
    OBSERVED["fake_streams"] += 1
    return reader, writer


class FacadeControls(D.DirectControls):
    """Actual contacts, accounting, group validation/custody; inert issuers."""
    def client(self):
        result = super().client()
        for name in ("transport.acquisition_resilience", "transport.declaration_resilience",
                     "transport.search_resilience", "transport.http_provider", "transport.clients",
                     "transport.receipt_client", "transport.located_receipts", "client.direct_contacts",
                     "custody.module_store", "discovery.formal_features"):
            path = Path(sys.modules[name].__file__).resolve()
            selected = D.pin(path)
            for owner in result._origin_owners:
                if owner is not None:
                    owner._pins[path] = {key: selected[key] for key in ("bytes", "sha256")}
        return result

    def fixture(self, *, ports=(21001, 21002), lifetime=60000):
        receiver = self.client()
        contacts, policy = self.contacts(ports)
        self.bind(receiver, contacts=contacts, policy=policy, contact_lifetime_ms=lifetime)
        spec, body = T.E.definitions()
        module = C.module_id(spec)
        first = spec["groups"][0]["declarations"][0]["name"]
        opening = C.group_opening(spec, 0)
        raw = receiver.workspace.adapter.encode_opening(module, first, opening)
        described = receiver.workspace.adapter.describe(raw)
        resolved = {**receiver.workspace.adapter.resolve(described["record"], raw),
                    "opening": opening, "candidate_origin": "INERT_FIXTURE_ORIGIN"}
        receiver.workspace.modules.put_group(module, opening)
        origin = Candidate()
        receiver._candidates[origin] = "peer0", deepcopy(resolved)
        return receiver, origin, spec, deepcopy(body["relative_name"])

    def settled(self, c):
        self.assertIsNone(c._budget.pending)
        self.assertEqual(c._acquisition.structural.inflight, 0)
        self.assertEqual(c._acquisition.structural.reserved_bytes, 0)
        self.assertFalse(c._busy)

    def no_target(self, c, spec):
        self.assertIsNone(c.workspace.modules.db.execute(
            "SELECT 1 FROM groups WHERE module=? AND idx=1", (C.module_id(spec),)).fetchone())

    async def attempt(self, c, origin, spec, name, *, supplier="peer0", timeout=1000):
        return await c.try_resolve_declaration(origin, C.module_id(spec), name,
            max_bytes=CAP, supplier=supplier, attempt_timeout_ms=timeout)

    async def test_loopback_absent_p_then_exact_q_preserves_original_operation(self):
        providers, endpoints = [], []
        spec, body = T.E.definitions()
        module, name = C.module_id(spec), body["relative_name"]
        for holds_target in (False, True):
            workspace, unused = self.workspace()
            workspace.modules.put_group(module, C.group_opening(spec, 0))
            if holds_target:
                workspace.modules.put_group(module, C.group_opening(spec, 1))
            provider = CompositeProvider(index=workspace.index, custody=workspace.modules,
                packets=workspace.packets, max_connections=2, max_requests=4,
                max_reply_bytes=64*1024**2, operation_ms=1000)
            self.providers.append(provider); providers.append(provider)
            endpoints.append(await provider.start())
        c, origin, spec, name = self.fixture(ports=tuple(row.port for row in endpoints))
        original_budget, original_grant = c._budget, c.grant
        before, candidates = deepcopy(c._budget.used), dict(c._candidates)
        counts = deepcopy(c.workspace.modules.status()["counts"])
        sentinel, inert_fact = object(), object()
        c._warrants[sentinel] = inert_fact
        OBSERVED["inert_warrant_sentinels"] += 1
        missing = await self.attempt(c, origin, spec, name)
        self.assertEqual(missing, refusal("peer0", "PEER_EOF", module, name))
        self.assertEqual(c._candidates, candidates)
        self.assertEqual(c.workspace.modules.status()["counts"], counts)
        self.assertEqual(c._state, "OPEN")
        self.assertIs(c._warrants[sentinel], inert_fact)
        self.assertTrue(all(owner is None or owner.closes == 0 for owner in c._origin_owners))
        self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
        self.settled(c); self.no_target(c, spec)
        response = await self.attempt(c, origin, spec, name, supplier="peer1")
        self.assertEqual(response["status"], "DECLARATION_CUSTODIED")
        self.assertFalse(response["mathematical_acceptance"])
        self.assertEqual(len(c._candidates), len(candidates)+1)
        self.assertEqual(c._candidates[origin], candidates[origin])
        provider, resolved = c._candidates[response["candidate"]]
        self.assertEqual(provider, "peer1")
        self.assertEqual(resolved["candidate_origin"], "EXACT_NAME_NOT_INDEX_SEARCH")
        self.assertEqual({key: resolved["locator"][key] for key in
                          ("module_id", "relative_name", "group_index")}, {
            "module_id": module, "relative_name": name, "group_index": 1})
        held, descriptor = c.workspace.modules.get_group(module, name, 1)
        self.assertEqual(held, C.group_opening(spec, 1))
        self.assertEqual(descriptor, resolved["descriptor"])
        self.assertIs(c._budget, original_budget); self.assertIs(c.grant, original_grant)
        self.assertIs(c._warrants[sentinel], inert_fact)
        self.assertEqual(c._budget.used["requests"], before["requests"]+2)
        self.assertEqual(c._budget.used["reply_bytes"],
                         before["reply_bytes"]+CAP+len(C.canonical(held)))
        self.assertEqual(c._counts["admission_submissions"], 0)
        self.assertEqual(c._budget.used["verify_attempts"], 0)
        self.settled(c)
        for provider in providers:
            await provider.stop()
            self.assertEqual(provider.status()["active"], 0)
            self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
            self.assertEqual(provider.status()["requests"], 1)
        OBSERVED["real_loopback_requests"] += 2
        RESULTS[self._testMethodName] = {"refusal": missing, "budget": c._budget.report(),
            "structural": c._acquisition.structural.report(),
            "providers": [provider.status() for provider in providers],
            "preserved_authority_scope": "INERT_SENTINEL_ONLY_NOT_GENUINE_WARRANT"}

    async def test_group_route_refusal_is_settled_without_candidate_or_custody(self):
        for status in (404, 503):
            with self.subTest(status=status):
                c, origin, spec, name = self.fixture()
                before, candidates = deepcopy(c._budget.used), dict(c._candidates)
                reader, writer = stream(b"{}", status=status)
                with patch.object(asyncio, "open_connection", return_value=(reader, writer)) as dial:
                    result = await self.attempt(c, origin, spec, name)
                self.assertEqual(result, refusal("peer0", "HTTP_"+str(status), C.module_id(spec), name))
                self.assertEqual(dial.call_count, 1)
                head, raw = bytes(writer.sent).split(b"\r\n\r\n", 1)
                self.assertTrue(head.startswith(b"POST /v5/modules/group HTTP/1.1\r\n"))
                self.assertEqual(C.parse_json(raw), result["request"])
                self.assertEqual((writer.closed, writer.waits), (1, 1))
                self.assertEqual(c._candidates, candidates)
                self.assertEqual(c._budget.used["requests"], before["requests"]+1)
                self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
                self.assertEqual(c._state, "OPEN")
                self.settled(c); self.no_target(c, spec); self.no_verification(c)

    async def test_successful_reply_requires_canonical_exact_valid_opening(self):
        for defect in ("json", "noncanonical", "wrong_module", "wrong_name", "commitment", "refusal", "http400"):
            with self.subTest(defect=defect):
                c, origin, spec, name = self.fixture()
                opening = C.group_opening(spec, 1)
                requested_name = name
                if defect == "wrong_module":
                    other = deepcopy(spec)
                    other["groups"][0]["declarations"][0]["name"] = [["s", "different"]]
                    opening = C.group_opening(other, 1)
                elif defect == "wrong_name": requested_name = [["s", "absent"]]
                elif defect == "commitment":
                    opening["group"]["declarations"][0]["universes"] += 1
                elif defect == "refusal": opening = refusal("peer0", "PEER_EOF", C.module_id(spec), name)
                raw = b"not-json" if defect == "json" else C.canonical(opening)
                if defect == "noncanonical": raw += b"\n"
                reader, writer = stream(raw, status=400 if defect == "http400" else 200)
                with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                    with self.assertRaises(Exception):
                        await self.attempt(c, origin, spec, requested_name)
                self.assertEqual((writer.closed, writer.waits), (1, 1))
                self.failed(c); self.settled(c); self.no_target(c, spec); self.no_verification(c)

    async def test_cancel_and_uncertain_cleanup_are_fatal_not_continuations(self):
        for defect in ("cancel", "cleanup"):
            c, origin, spec, name = self.fixture()
            before = deepcopy(c._budget.used)
            reader, writer = stream(cleanup_error=OSError("INERT_UNCERTAIN_CLOSE"))
            options = {"side_effect": asyncio.CancelledError()} if defect == "cancel" else {
                "return_value": (reader, writer)}
            with patch.object(asyncio, "open_connection", **options):
                with self.assertRaises(asyncio.CancelledError if defect == "cancel" else R.DeclarationCleanupError):
                    await self.attempt(c, origin, spec, name)
            self.assertEqual(c._budget.used["requests"], before["requests"]+1)
            self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
            self.failed(c); self.settled(c); self.no_target(c, spec)

    async def test_custody_readback_and_final_binding_remain_fatal(self):
        for defect in ("put", "readback", "final_binding"):
            c, origin, spec, name = self.fixture()
            reader, writer = stream(C.canonical(C.group_opening(spec, 1)))
            if defect == "final_binding":
                original_settle = c._budget.settle
                def changed_after_settlement(*args, **kwargs):
                    result = original_settle(*args, **kwargs)
                    c._acquisition.structural.endpoints["peer1"] = c._acquisition.endpoints["peer0"]
                    return result
                fault = patch.object(c._budget, "settle", side_effect=changed_after_settlement)
            else:
                fault = patch.object(c.workspace.modules, "put_group" if defect == "put" else "get_group",
                                     side_effect=ValueError("INERT_CUSTODY_FAILURE"))
            with fault, patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                with self.assertRaises(Exception):
                    await self.attempt(c, origin, spec, name, supplier="peer1")
            self.failed(c); self.settled(c); self.no_verification(c)
            if defect == "readback":
                self.assertEqual(c.workspace.modules.get_group(C.module_id(spec), name)[0],
                                 C.group_opening(spec, 1))
            else: self.no_target(c, spec)

    async def test_alternative_attempts_do_not_renew_original_allowance(self):
        c, origin, spec, name = self.fixture()
        budget, deadline = c._budget, c.grant.deadline
        for supplier in ("peer0", "peer1", "peer0", "peer1"):
            reader, writer = stream()
            with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                self.assertEqual(await self.attempt(c, origin, spec, name, supplier=supplier),
                    refusal(supplier, "PEER_EOF", C.module_id(spec), name))
        with patch.object(asyncio, "open_connection", side_effect=AssertionError("EXHAUSTED_MUST_NOT_DIAL")) as dial:
            with self.assertRaises(ValueError):
                await self.attempt(c, origin, spec, name, supplier="peer1")
        self.assertFalse(dial.called)
        self.assertIs(c._budget, budget); self.assertEqual(c.grant.deadline, deadline)
        self.assertEqual(budget.used["requests"], 8)
        self.assertEqual(len(budget.external), 1)
        self.failed(c); self.settled(c); self.no_target(c, spec)

    async def test_invalid_contact_or_attempt_source_never_dials(self):
        for defect in ("unknown", "expired", "binding", "pin", "hook"):
            c, origin, spec, name = self.fixture(lifetime=1000)
            supplier = "absent" if defect == "unknown" else "peer1"
            if defect == "binding":
                c._acquisition.structural.endpoints["peer1"] = c._acquisition.endpoints["peer0"]
            if defect == "pin":
                for owner in c._origin_owners:
                    if owner is not None: owner._pins.pop(Path(R.__file__).resolve())
            clock = patch("transport.located_receipts.time.monotonic",
                return_value=c._search._expiries["peer1"]+0.001) if defect == "expired" else nullcontext()
            hook = patch.object(E, "_try_declaration", return_value=refusal(
                "peer1", "PEER_EOF", C.module_id(spec), name)) if defect == "hook" else nullcontext()
            with clock, hook as replacement, patch.object(asyncio, "open_connection",
                    side_effect=AssertionError("INVALID_BINDING_MUST_NOT_DIAL")) as dial:
                with self.assertRaises(ValueError):
                    await self.attempt(c, origin, spec, name, supplier=supplier)
            self.assertFalse(dial.called)
            if defect == "hook": self.assertFalse(replacement.called)
            self.failed(c); self.settled(c); self.no_target(c, spec)


class InertDeclarationClient(T.InertClient):
    """Helper composition only; no transport/custody/mathematical authority."""
    def __init__(self, specs):
        super().__init__(specs)
        self.allowed = {"inert-same-provider", "Q"}
        self.refuse, self.bad_refusal, self.raise_error = True, False, None
        self.attempts = []

    def check_supplier(self, supplier):
        self._active()
        if supplier not in self.allowed: raise ValueError("INERT_SUPPLIER_UNAUTHORIZED")
        return {"status": "AUTHORIZED_LIVE_CONTACT", "supplier": supplier,
                "mathematical_acceptance": False}

    async def try_resolve_declaration(self, origin, module, name, *, max_bytes,
                                      supplier=None, attempt_timeout_ms=5000):
        selected = self.descriptions[origin]["provider"] if supplier is None else supplier
        self.check_supplier(selected)
        self.attempts.append((selected, module, C.name_key(name), max_bytes, attempt_timeout_ms))
        OBSERVED["inert_helper_attempts"] += 1
        if self.raise_error is not None: raise self.raise_error
        if self.refuse:
            result = refusal(selected, "PEER_EOF", module, name)
            if self.bad_refusal: result["request"]["relative_name"] = [["s", "wrong"]]
            return result
        held = await super().resolve_declaration(origin, module, name, max_bytes=max_bytes)
        candidate = object()
        self.descriptions[candidate] = {**self.describe_candidate(held), "provider": selected}
        return {"status": "DECLARATION_CUSTODIED", "candidate": candidate,
                "mathematical_acceptance": False}


class HelperControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        guard = patch.object(H, "CommonsClient", InertDeclarationClient)
        guard.start(); self.addCleanup(guard.stop)

    async def start(self, *, steps=None):
        spec, body = T.E.definitions()
        c = InertDeclarationClient([spec])
        limits = deepcopy(T.LIMITS)
        if steps is not None: limits["steps"] = steps
        h = H.SemanticReader(c, c.origin, limits=limits)
        await h.stage(c.origin, c.entries(c.origin)[0])
        first = spec["groups"][0]["declarations"][0]["name"]
        body_demand = T.demand("NeedBody", spec, name=first,
            universes=body["universes"], body_hash=body["body_hash"])
        c.demands = [body_demand]; h.preview()
        await h.fetch_body(body_demand, max_bytes=CAP)
        demand = T.demand("NeedDeclaration", spec, name=body["relative_name"])
        c.demands = [demand]; h.preview()
        return c, h, demand

    def retained(self, h):
        return {name: dict(getattr(h, name)) for name in ("_pending", "_selected", "_members",
            "_names", "_supplier_names", "_by_token", "_groups", "_bodies")} | {
            "_revision": h._revision, "_bytes": h._bytes, "_ready_revision": h._ready_revision}

    async def test_refusal_preserves_all_retained_work_then_q_resolves_exactly(self):
        c, h, demand = await self.start()
        before, steps = self.retained(h), h._steps
        self.assertTrue(h._bodies and h._groups and h._members and h._selected)
        result = await h.try_resolve(demand, max_bytes=CAP)
        self.assertEqual(result, refusal("inert-same-provider", "PEER_EOF", demand["module"], demand["name"]))
        self.assertEqual(self.retained(h), before)
        self.assertEqual(h._steps, steps+1)
        self.assertEqual(h.report()["state"], "COLLECTING")
        c.refuse = False
        result = await h.try_resolve(demand, max_bytes=CAP, supplier="Q")
        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["description"]["provider"], "Q")
        self.assertEqual(result["description"]["locator"]["relative_name"], demand["name"])
        self.assertEqual(len(h._groups), len(before["_groups"])+1)
        self.assertEqual(h._pending, before["_pending"])
        self.assertEqual(h._bodies, before["_bodies"])
        self.assertEqual([row[0] for row in c.attempts], ["inert-same-provider", "Q"])
        self.assertEqual(c.warrants, {})
        self.assertFalse(any(row[0] in ("admit", "import") for row in c.events))

    async def test_fatal_or_wrong_request_refusal_cannot_preserve_reader(self):
        for defect in ("error", "refusal"):
            c, h, demand = await self.start()
            if defect == "error": c.raise_error = ValueError("INERT_DECLARATION_FATAL")
            else: c.bad_refusal = True
            with self.assertRaises(ValueError):
                await h.try_resolve(demand, max_bytes=CAP)
            self.assertEqual(h.report()["state"], "FAILED")
            self.assertEqual(len(c.attempts), 1)

    async def test_cache_checks_contact_and_timeout_and_refusals_consume_steps(self):
        for defect in ("contact", "timeout"):
            c, h, demand = await self.start()
            c.refuse = False
            await h.try_resolve(demand, max_bytes=CAP, supplier="Q")
            before = len(c.attempts)
            self.assertEqual((await h.try_resolve(demand, max_bytes=CAP, supplier="Q"))["status"], "NO_PROGRESS")
            if defect == "contact": c.allowed.remove("Q")
            with self.assertRaises(ValueError):
                await h.try_resolve(demand, max_bytes=CAP, supplier="Q",
                    attempt_timeout_ms=0 if defect == "timeout" else 1000)
            self.assertEqual(len(c.attempts), before)
            self.assertEqual(h.report()["state"], "FAILED")
        c, h, demand = await self.start(steps=5)
        self.assertEqual(h._steps, 4)
        await h.try_resolve(demand, max_bytes=CAP)
        with self.assertRaisesRegex(ValueError, "SEMANTIC_READER_STEP_LIMIT"):
            await h.try_resolve(demand, max_bytes=CAP, supplier="Q")
        self.assertEqual(len(c.attempts), 1)
        self.assertEqual(h.report()["state"], "FAILED")


FACADE = (
    "test_loopback_absent_p_then_exact_q_preserves_original_operation",
    "test_group_route_refusal_is_settled_without_candidate_or_custody",
    "test_successful_reply_requires_canonical_exact_valid_opening",
    "test_cancel_and_uncertain_cleanup_are_fatal_not_continuations",
    "test_custody_readback_and_final_binding_remain_fatal",
    "test_alternative_attempts_do_not_renew_original_allowance",
    "test_invalid_contact_or_attempt_source_never_dials",
)
HELPER = (
    "test_refusal_preserves_all_retained_work_then_q_resolves_exactly",
    "test_fatal_or_wrong_request_refusal_cannot_preserve_reader",
    "test_cache_checks_contact_and_timeout_and_refusals_consume_steps",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_dir() or OUTPUT.resolve() != OUTPUT:
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    D.OUTPUT = OUTPUT
    suite = unittest.TestSuite([*(FacadeControls(name) for name in FACADE),
                               *(HelperControls(name) for name in HELPER)])
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "scope": "REAL_DECLARATION_ACQUISITION_CUSTODY_LOOPBACK_WITH_INERT_MATHEMATICAL_ISSUERS",
        "selected": [*FACADE, *HELPER], "observed": OBSERVED, "results": RESULTS,
        "native_calls": 0, "proof_calls": 0, "mathematical_acceptance": False,
        "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in (
            "client/supplier_complete/test_declaration.py",
            "client/supplier_complete/workspace_evidence.py", "client/supplier_complete/semantic_reader.py",
            "transport/declaration_resilience.py", "transport/acquisition_resilience.py",
            "client/test_direct_contacts.py", "client/test_semantic_reader.py")}}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
