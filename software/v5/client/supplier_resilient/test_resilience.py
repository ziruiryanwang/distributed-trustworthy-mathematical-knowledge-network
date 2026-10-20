"""New body-recovery controls; mathematical issuers are explicitly INERT.

Borrow existing fixture constructors only, not predecessor suites. One control
uses two real loopback providers, exact structural validation and real custody.
Other transport controls use real parsing/settlement over bounded fake streams.
No native process, proof, genuine warrant or mathematical admission runs.
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


E = overlay("client.workspace_evidence", "client/supplier_resilient/workspace_evidence.py")
overlay("client.workspace_staged", "staging_members/workspace_staged.py")
H = overlay("client.semantic_reader", "client/supplier_resilient/semantic_reader.py")
from client import test_direct_contacts as D
from client import test_semantic_reader as T
from client.workspace_atomic import Candidate
from evidence_network.transport import CompositeProvider
from modules import codec as C
from transport import acquisition_resilience as R
from transport import http_provider as HTTP

OUTPUT = None
CAP = 65536
OBSERVED = {"real_loopback_requests": 0, "inert_warrant_sentinels": 0,
            "fake_streams": 0, "clean_fake_closures": 0}
RESULTS = {}


def refusal(supplier, reason, body):
    return {"schema": "DMKN_SEMANTIC_BODY_ATTEMPT_V1",
            "status": "UNAVAILABLE_AT_SELECTED_SUPPLIER", "supplier": supplier,
            "reason": reason, "request": {key: deepcopy(body[key]) for key in
                ("module_id", "relative_name", "universes", "body_hash")},
            "settlement": "FULL_REPLY_RESERVATION_CHARGED",
            "global_complete": False, "mathematical_acceptance": False}


class Writer:
    """Explicitly inert stream writer; no socket or task is hidden behind it."""
    def __init__(self, *, cleanup_error=None, write_error=None):
        self.cleanup_error, self.write_error = cleanup_error, write_error
        self.closed = self.waits = 0
        self.sent = bytearray()

    def write(self, raw):
        self.sent.extend(raw)

    async def drain(self):
        if self.write_error is not None:
            raise self.write_error

    def close(self):
        self.closed += 1

    async def wait_closed(self):
        self.waits += 1
        if self.cleanup_error is not None:
            raise self.cleanup_error
        OBSERVED["clean_fake_closures"] += 1


def stream(raw=None, *, status=200, header=None, eof=True, cleanup_error=None,
           write_error=None):
    reader, writer = asyncio.StreamReader(), Writer(
        cleanup_error=cleanup_error, write_error=write_error)
    if raw is not None:
        reader.feed_data((HTTP._header("HTTP/1.1 "+str(status)+" TEST", len(raw))
                          if header is None else header)+raw)
    if eof:
        reader.feed_eof()
    OBSERVED["fake_streams"] += 1
    return reader, writer


class FacadeControls(D.DirectControls):
    """Real facade, contact, acquisition budget, validator and SQLite custody."""
    def client(self):
        result = super().client()
        # Adoption metadata is inert like the existing issuer fixture. The
        # source bytes/origin are real and remain available to source guards.
        for name in ("transport.acquisition_resilience", "transport.search_resilience",
                     "transport.http_provider", "transport.clients", "transport.receipt_client",
                     "transport.located_receipts", "client.direct_contacts",
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
        name = spec["groups"][0]["declarations"][0]["name"]
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        raw = receiver.workspace.adapter.encode_opening(module, name, opening)
        descriptor = receiver.workspace.adapter.describe(raw)
        resolved = {**receiver.workspace.adapter.resolve(descriptor["record"], raw),
                    "opening": opening, "candidate_origin": "INERT_FIXTURE_ORIGIN"}
        receiver.workspace.modules.put_group(module, opening)
        origin = Candidate()
        receiver._candidates[origin] = "peer0", deepcopy(resolved)
        body = {**deepcopy(body), "module_id": module, "relative_name": name}
        return receiver, origin, spec, body

    def no_admission(self, c):
        for key in ("verify_attempts", "verification_input_bytes", "worker_cpu_seconds"):
            self.assertEqual(c._budget.used[key], 0)
        self.assertEqual(c._counts["admission_submissions"], 0)

    def settled(self, c):
        self.assertIsNone(c._budget.pending)
        self.assertEqual(c._acquisition.structural.inflight, 0)
        self.assertEqual(c._acquisition.structural.reserved_bytes, 0)
        self.assertFalse(c._busy)

    def no_body(self, c, body):
        self.assertIsNone(c.workspace.modules.db.execute(
            "SELECT 1 FROM bodies WHERE module=? AND universes=? AND hash=?",
            (body["module_id"], body["universes"], body["body_hash"])).fetchone())

    async def attempt(self, c, origin, body, *, supplier="peer0", timeout=1000):
        return await c.try_acquire_body(origin, body["body_hash"], max_bytes=CAP,
                                       supplier=supplier, attempt_timeout_ms=timeout)

    async def test_real_missing_provider_eof_then_exact_q_body_same_operation(self):
        providers, endpoints, stores = [], [], []
        spec, body = T.E.definitions()
        module, opening = C.module_id(spec), C.group_opening(spec, 0)
        name = spec["groups"][0]["declarations"][0]["name"]
        body = {**deepcopy(body), "module_id": module, "relative_name": name}
        for holds_body in (False, True):
            workspace, unused = self.workspace()
            stores.append(workspace)
            workspace.modules.put_group(module, opening)
            if holds_body:
                workspace.modules.put_body(module, name, body)
            provider = CompositeProvider(index=workspace.index, custody=workspace.modules,
                packets=workspace.packets, max_connections=2, max_requests=4,
                max_reply_bytes=64*1024**2, operation_ms=1000)
            self.providers.append(provider)
            providers.append(provider)
            endpoints.append(await provider.start())
        c, origin, unused, expected = self.fixture(ports=tuple(x.port for x in endpoints))
        before = deepcopy(c._budget.used)
        original_budget, grant, candidate = c._budget, c.grant, deepcopy(c._candidates[origin])
        sentinel, inert_fact = object(), object()
        c._warrants[sentinel] = inert_fact
        OBSERVED["inert_warrant_sentinels"] += 1
        calls = c._calls
        missing = await self.attempt(c, origin, expected)
        self.assertEqual(missing, refusal("peer0", "PEER_EOF", expected))
        self.no_body(c, expected)
        self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
        self.assertEqual(c._state, "OPEN")
        self.assertIs(c._warrants[sentinel], inert_fact)
        self.assertTrue(all(owner is None or owner.closes == 0 for owner in c._origin_owners))
        self.settled(c)
        result = await self.attempt(c, origin, expected, supplier="peer1")
        self.assertEqual(result["status"], "BODY_CUSTODIED")
        self.assertEqual(result["body"], expected)
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(c._candidates[origin], candidate)
        self.assertIs(c._budget, original_budget)
        self.assertIs(c.grant, grant)
        self.assertEqual(c._calls, calls+2)
        self.assertEqual(c._budget.used["requests"], before["requests"]+2)
        self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP+len(C.canonical(expected)))
        self.assertEqual(c.workspace.modules.get_body(module, name, expected["universes"],
                         expected["body_hash"]), expected)
        self.assertIs(c._warrants[sentinel], inert_fact)
        self.settled(c)
        self.no_admission(c)
        for provider in providers:
            await provider.stop()
            self.assertEqual(provider.status()["active"], 0)
            self.assertEqual(provider.status()["reserved_reply_bytes"], 0)
            self.assertEqual(provider.status()["requests"], 1)
        OBSERVED["real_loopback_requests"] += sum(p.status()["requests"] for p in providers)
        self.assertEqual(stores[0].modules.status()["counts"]["bodies"], 0)
        self.assertEqual(stores[1].modules.status()["counts"]["bodies"], 1)
        RESULTS[self._testMethodName] = {"refusal": missing,
            "budget": c._budget.report(), "structural": c._acquisition.structural.report(),
            "providers": [p.status() for p in providers],
            "preserved_authority_scope": "INERT_SENTINEL_ONLY_NO_GENUINE_WARRANT"}

    async def test_framed_unavailable_statuses_charge_full_cap_without_custody(self):
        for status in (404, 503):
            with self.subTest(status=status):
                c, origin, unused, body = self.fixture()
                before = deepcopy(c._budget.used)
                reader, writer = stream(b"{}", status=status)
                with patch.object(asyncio, "open_connection", return_value=(reader, writer)) as dial:
                    result = await self.attempt(c, origin, body)
                self.assertEqual(result, refusal("peer0", "HTTP_"+str(status), body))
                self.assertEqual(dial.call_count, 1)
                self.assertEqual((writer.closed, writer.waits), (1, 1))
                self.assertEqual(c._budget.used["requests"], before["requests"]+1)
                self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
                self.no_body(c, body)
                self.settled(c)
                self.no_admission(c)

    async def test_clean_transport_failures_are_settled_not_retried(self):
        for defect, reason in (("refused", "CONNECTION_REFUSED"), ("eof", "PEER_EOF"),
                               ("reset", "CONNECTION_RESET"), ("pipe", "BROKEN_PIPE"),
                               ("timeout", "ATTEMPT_TIMEOUT")):
            with self.subTest(defect=defect):
                c, origin, unused, body = self.fixture()
                before = deepcopy(c._budget.used)
                reader, writer = stream(eof=defect != "timeout",
                    write_error=ConnectionResetError() if defect == "reset" else
                                BrokenPipeError() if defect == "pipe" else None)
                options = {"side_effect": ConnectionRefusedError()} if defect == "refused" else {
                    "return_value": (reader, writer)}
                with patch.object(asyncio, "open_connection", **options) as dial:
                    result = await self.attempt(c, origin, body, timeout=10)
                self.assertEqual(result, refusal("peer0", reason, body))
                self.assertEqual(dial.call_count, 1)
                self.assertEqual((writer.closed, writer.waits), (0, 0) if defect == "refused" else (1, 1))
                self.assertEqual(c._budget.used["requests"], before["requests"]+1)
                self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
                self.assertEqual(c._state, "OPEN")
                self.no_body(c, body)
                self.settled(c)
                self.no_admission(c)

    async def test_uncertain_stream_cleanup_remains_fatal(self):
        for successful_body in (False, True):
            c, origin, unused, body = self.fixture()
            reader, writer = stream(C.canonical(body) if successful_body else None,
                                    cleanup_error=OSError("INERT_UNCERTAIN_CLOSE"))
            with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                with self.assertRaises(Exception):
                    await self.attempt(c, origin, body)
            self.assertEqual((writer.closed, writer.waits), (1, 1))
            self.failed(c)
            self.no_body(c, body)
            self.settled(c)
            self.no_admission(c)

    async def test_cancel_and_unreturned_connect_failure_remain_fatal(self):
        for error in (asyncio.CancelledError(), TimeoutError("INERT_CONNECT_NOT_RETURNED"),
                      ConnectionResetError("INERT_CONNECT_NOT_RETURNED")):
            c, origin, unused, body = self.fixture()
            before = deepcopy(c._budget.used)
            with patch.object(asyncio, "open_connection", side_effect=error):
                with self.assertRaises(type(error)):
                    await self.attempt(c, origin, body)
            self.failed(c)
            self.assertEqual(c._budget.used["requests"], before["requests"]+1)
            self.assertEqual(c._budget.used["reply_bytes"], before["reply_bytes"]+CAP)
            self.no_body(c, body)
            self.settled(c)

    async def test_malformed_success_and_wrong_commitments_remain_fatal(self):
        for defect in ("json", "noncanonical", "hash", "module", "name", "arity", "refusal"):
            with self.subTest(defect=defect):
                c, origin, unused, body = self.fixture()
                invalid = deepcopy(body)
                if defect == "hash": invalid["expression"] = ["sort", ["succ", ["zero"]]]
                elif defect == "module": invalid["module_id"] = "0"*64
                elif defect == "name": invalid["relative_name"] = [["s", "wrong"]]
                elif defect == "arity": invalid["universes"] += 1
                elif defect == "refusal": invalid = refusal("peer0", "PEER_EOF", body)
                raw = b"not-json" if defect == "json" else C.canonical(invalid)
                if defect == "noncanonical": raw += b"\n"
                reader, writer = stream(raw)
                with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                    with self.assertRaises(Exception):
                        await self.attempt(c, origin, body)
                self.assertEqual((writer.closed, writer.waits), (1, 1))
                self.failed(c)
                self.no_body(c, body)
                self.settled(c)
                self.no_admission(c)

    async def test_bad_status_and_framing_are_not_availability(self):
        for defect in ("400", "trailing", "header"):
            c, origin, unused, body = self.fixture()
            raw = C.canonical(body)
            if defect == "header":
                reader, writer = stream(raw, header=b"HTTP/1.1 200 OK\r\nBad Header\r\n\r\n")
            elif defect == "trailing":
                reader, writer = stream(raw+b"x", header=HTTP._header("HTTP/1.1 200 OK", len(raw)))
            else:
                reader, writer = stream(b"{}", status=400)
            with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                with self.assertRaises(Exception):
                    await self.attempt(c, origin, body)
            self.failed(c)
            self.no_body(c, body)
            self.settled(c)

    async def test_custody_and_after_commit_readback_failures_remain_fatal(self):
        for stage in ("put", "readback"):
            c, origin, unused, body = self.fixture()
            reader, writer = stream(C.canonical(body))
            method = "put_body" if stage == "put" else "get_body"
            with patch.object(asyncio, "open_connection", return_value=(reader, writer)), \
                 patch.object(c.workspace.modules, method, side_effect=ValueError("INERT_CUSTODY_FAILURE")):
                with self.assertRaisesRegex(ValueError, "INERT_CUSTODY_FAILURE"):
                    await self.attempt(c, origin, body)
            self.failed(c)
            self.settled(c)
            if stage == "put": self.no_body(c, body)
            else:
                self.assertEqual(c.workspace.modules.get_body(body["module_id"], body["relative_name"],
                    body["universes"], body["body_hash"]), body)
            self.no_admission(c)

    async def test_alternative_suppliers_never_renew_request_allowance(self):
        c, origin, unused, body = self.fixture()
        original, deadline = c._budget, c.grant.deadline
        for supplier in ("peer0", "peer1", "peer0", "peer1"):
            reader, writer = stream()
            with patch.object(asyncio, "open_connection", return_value=(reader, writer)):
                self.assertEqual(await self.attempt(c, origin, body, supplier=supplier),
                                 refusal(supplier, "PEER_EOF", body))
        with patch.object(asyncio, "open_connection", side_effect=AssertionError("EXHAUSTED_MUST_NOT_DIAL")) as dial:
            with self.assertRaises(ValueError):
                await self.attempt(c, origin, body, supplier="peer1")
        self.assertFalse(dial.called)
        self.assertIs(c._budget, original)
        self.assertEqual(c.grant.deadline, deadline)
        self.assertEqual(original.used["requests"], 8)
        self.assertEqual(len(original.external), 1)
        self.failed(c)
        self.settled(c)

    async def test_unauthorized_expired_or_changed_contact_does_not_dial(self):
        for defect in ("unknown", "expired", "binding"):
            c, origin, unused, body = self.fixture(lifetime=1000)
            supplier = "absent" if defect == "unknown" else "peer1"
            if defect == "binding":
                c._acquisition.structural.endpoints["peer1"] = c._acquisition.endpoints["peer0"]
            clock = patch("transport.located_receipts.time.monotonic",
                return_value=c._search._expiries["peer1"]+0.001) if defect == "expired" else \
                nullcontext()
            with clock, patch.object(asyncio, "open_connection",
                                     side_effect=AssertionError("UNAUTHORIZED_MUST_NOT_DIAL")) as dial:
                with self.assertRaises(ValueError):
                    await self.attempt(c, origin, body, supplier=supplier)
            self.assertFalse(dial.called)
            self.failed(c)
            self.settled(c)

    async def test_missing_source_pin_and_replaced_hook_cannot_forge_refusal(self):
        for defect in ("pin", "hook"):
            c, origin, unused, body = self.fixture()
            if defect == "pin":
                for owner in c._origin_owners:
                    if owner is not None: owner._pins.pop(Path(R.__file__).resolve())
            replacement = patch.object(E, "_try_body", return_value=refusal("peer0", "PEER_EOF", body)) \
                if defect == "hook" else nullcontext()
            with replacement as hook, patch.object(asyncio, "open_connection",
                    side_effect=AssertionError("INVALID_SOURCE_MUST_NOT_DIAL")) as dial:
                with self.assertRaisesRegex(ValueError, "BODY_ATTEMPT_REQUIRED_SOURCE_PIN|BODY_ATTEMPT_SYMBOL_CHANGED"):
                    await self.attempt(c, origin, body)
            self.assertFalse(dial.called)
            if defect == "hook": self.assertFalse(hook.called)
            self.failed(c)
            self.settled(c)
            self.no_body(c, body)


class InertResilientClient(T.InertClient):
    """Helper composition only; no transport/custody/verification authority."""
    def __init__(self, specs):
        super().__init__(specs)
        self.allowed = {"inert-same-provider", "Q"}
        self.refuse = True
        self.bad_refusal = False
        self.raise_error = None
        self.attempts = []

    def check_supplier(self, supplier):
        self._active()
        if supplier not in self.allowed:
            raise ValueError("INERT_SUPPLIER_UNAUTHORIZED")
        return {"status": "AUTHORIZED_LIVE_CONTACT", "supplier": supplier,
                "mathematical_acceptance": False}

    async def try_acquire_body(self, candidate, digest, *, max_bytes, supplier=None,
                               attempt_timeout_ms=5000):
        selected = self.descriptions[candidate]["provider"] if supplier is None else supplier
        self.check_supplier(selected)
        self.attempts.append((selected, digest, max_bytes, attempt_timeout_ms))
        if self.raise_error is not None: raise self.raise_error
        if self.refuse:
            description = self.descriptions[candidate]
            result = refusal(selected, "PEER_EOF", {
                "module_id": description["locator"]["module_id"],
                "relative_name": description["locator"]["relative_name"],
                "universes": description["descriptor"]["universes"], "body_hash": digest})
            if self.bad_refusal: result["mathematical_acceptance"] = True
            return result
        result = await super().acquire_body(candidate, digest, max_bytes=max_bytes)
        return {**result, "status": "BODY_CUSTODIED",
                "assurance": "EXACT_DESCRIPTOR_COMMITTED_BODY", "mathematical_acceptance": False}


class HelperControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        guard = patch.object(H, "CommonsClient", InertResilientClient)
        guard.start()
        self.addCleanup(guard.stop)

    async def start(self):
        spec, body = T.E.definitions()
        c = InertResilientClient([spec])
        h = H.SemanticReader(c, c.origin, limits=deepcopy(T.LIMITS))
        await h.stage(c.origin, c.entries(c.origin)[0])
        demand = T.demand("NeedBody", spec, universes=body["universes"], body_hash=body["body_hash"])
        c.demands = [demand]
        h.preview()
        return c, h, demand

    async def test_refused_helper_preserves_selection_demand_then_q_progresses(self):
        c, h, demand = await self.start()
        pending, selection = deepcopy(h._pending), dict(h._selected)
        revision, retained, steps = h._revision, h._bytes, h._steps
        result = await h.try_fetch_body(demand, max_bytes=CAP)
        self.assertEqual(result, refusal("inert-same-provider", "PEER_EOF", {
            "module_id": demand["module"], "relative_name": demand["name"],
            "universes": demand["universes"], "body_hash": demand["body_hash"]}))
        self.assertEqual(h._pending, pending)
        self.assertEqual(h._selected, selection)
        self.assertEqual((h._revision, h._bytes), (revision, retained))
        self.assertEqual(h._steps, steps+1)
        self.assertEqual(h.report()["state"], "COLLECTING")
        self.assertEqual(h.report()["bodies"], 0)
        self.assertEqual(len(c.attempts), 1)
        c.refuse = False
        result = await h.try_fetch_body(demand, max_bytes=CAP, supplier="Q")
        self.assertEqual(result["status"], "FETCHED")
        self.assertEqual(h.report()["bodies"], 1)
        self.assertEqual([row[0] for row in c.attempts], ["inert-same-provider", "Q"])
        self.assertEqual(c.warrants, {})
        self.assertFalse(any(row[0] in ("admit", "import", "resolve") for row in c.events))

    async def test_helper_fatal_error_and_forged_refusal_do_not_continue(self):
        for defect in ("error", "refusal"):
            c, h, demand = await self.start()
            if defect == "error": c.raise_error = ValueError("INERT_FATAL_BODY_ERROR")
            else: c.bad_refusal = True
            with self.assertRaises(ValueError):
                await h.try_fetch_body(demand, max_bytes=CAP)
            self.assertEqual(h.report()["state"], "FAILED")
            self.assertEqual(h.report()["bodies"], 0)

    async def test_helper_cached_body_still_checks_requested_supplier(self):
        c, h, demand = await self.start()
        c.refuse = False
        await h.try_fetch_body(demand, max_bytes=CAP, supplier="Q")
        before = len(c.attempts)
        result = await h.try_fetch_body(demand, max_bytes=CAP)
        self.assertEqual(result["status"], "NO_PROGRESS")
        self.assertEqual(len(c.attempts), before)
        c.allowed.remove("Q")
        with self.assertRaisesRegex(ValueError, "INERT_SUPPLIER_UNAUTHORIZED"):
            await h.try_fetch_body(demand, max_bytes=CAP, supplier="Q")
        self.assertEqual(len(c.attempts), before)
        self.assertEqual(h.report()["state"], "FAILED")
        # The new attempt argument remains validated on an already-held body;
        # a cache hit must not silently accept an invalid requested envelope.
        c, h, demand = await self.start()
        c.refuse = False
        await h.try_fetch_body(demand, max_bytes=CAP)
        before = len(c.attempts)
        with self.assertRaises(ValueError):
            await h.try_fetch_body(demand, max_bytes=CAP, attempt_timeout_ms=0)
        self.assertEqual(len(c.attempts), before)
        self.assertEqual(h.report()["state"], "FAILED")


FACADE = (
    "test_real_missing_provider_eof_then_exact_q_body_same_operation",
    "test_framed_unavailable_statuses_charge_full_cap_without_custody",
    "test_clean_transport_failures_are_settled_not_retried",
    "test_uncertain_stream_cleanup_remains_fatal",
    "test_cancel_and_unreturned_connect_failure_remain_fatal",
    "test_malformed_success_and_wrong_commitments_remain_fatal",
    "test_bad_status_and_framing_are_not_availability",
    "test_custody_and_after_commit_readback_failures_remain_fatal",
    "test_alternative_suppliers_never_renew_request_allowance",
    "test_unauthorized_expired_or_changed_contact_does_not_dial",
    "test_missing_source_pin_and_replaced_hook_cannot_forge_refusal",
)
HELPER = (
    "test_refused_helper_preserves_selection_demand_then_q_progresses",
    "test_helper_fatal_error_and_forged_refusal_do_not_continue",
    "test_helper_cached_body_still_checks_requested_supplier",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
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
        "scope": "REAL_BODY_ACQUISITION_CUSTODY_AND_LOOPBACK_WITH_INERT_MATHEMATICAL_ISSUERS",
        "selected": [*FACADE, *HELPER], "observed": OBSERVED, "results": RESULTS,
        "native_calls": 0, "proof_calls": 0, "mathematical_acceptance": False,
        "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in (
            "client/supplier_resilient/test_resilience.py",
            "client/supplier_resilient/workspace_evidence.py",
            "client/supplier_resilient/semantic_reader.py",
            "transport/acquisition_resilience.py",
            "client/test_direct_contacts.py", "client/test_semantic_reader.py")}}
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
