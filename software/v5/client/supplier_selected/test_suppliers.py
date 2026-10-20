"""Changed supplier boundary only; issuers and HTTP exchange are INERT.

Real facade/decorators/contact guards/budget/custody are exercised with a
mocked HTTP exchange. Helper composition uses an explicitly inert facade.
No native process, proof, live admission or network is permitted.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
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


E = overlay("client.workspace_evidence", "client/supplier_selected/workspace_evidence.py")
overlay("client.workspace_staged", "staging_members/workspace_staged.py")
H = overlay("client.semantic_reader", "client/supplier_selected/semantic_reader.py")
from client import test_direct_contacts as D
from client import test_semantic_reader as T
from client.workspace_atomic import Candidate
from modules import codec as C
from transport import clients as HTTP

MIB = 1024**2
OUTPUT = None
OBSERVED = {"mock_http": 0, "helper_supplier_checks": 0}


class FacadeControls(D.DirectControls):
    """Borrow fixture constructors, never execute the predecessor test suite."""
    def fixture(self, *, contact_lifetime_ms=60000):
        receiver = self.client()
        contacts, policy = self.contacts((21001, 21002))
        self.bind(receiver, contacts=contacts, policy=policy,
                  contact_lifetime_ms=contact_lifetime_ms)
        spec, body = T.E.definitions()
        name = spec["groups"][0]["declarations"][0]["name"]
        module = C.module_id(spec)
        opening = C.group_opening(spec, 0)
        raw = receiver.workspace.adapter.encode_opening(module, name, opening)
        descriptor = receiver.workspace.adapter.describe(raw)
        resolved = {**receiver.workspace.adapter.resolve(descriptor["record"], raw),
                    "opening": opening, "candidate_origin": "INERT_FIXTURE_ORIGIN"}
        receiver.workspace.modules.put_group(module, opening)
        origin = Candidate()
        receiver._candidates[origin] = "peer0", deepcopy(resolved)
        body = {**deepcopy(body), "module_id": module, "relative_name": name}
        calls = []

        async def exchange(endpoint, route, request, maximum, timeout):
            endpoint.validate()  # Actual selected-contact guard before mock I/O.
            calls.append((endpoint.port, route, deepcopy(request)))
            OBSERVED["mock_http"] += 1
            value = opening if route == "/v5/modules/group" else body
            encoded = C.canonical(value)
            self.assertLessEqual(len(encoded), maximum)
            return {"status": 200, "raw": encoded, "request_bytes": len(C.canonical(request)),
                    "reply_bytes": len(encoded), "header_bytes": 0}
        return receiver, origin, spec, body, calls, exchange

    async def test_exact_q_resolution_and_body_preserve_p_origin_and_shared_budget(self):
        c, origin, spec, body, calls, exchange = self.fixture()
        before = deepcopy(c._candidates[origin])
        budget, grant, deadline = c._budget, c.grant, c.grant.deadline
        initial = deepcopy(budget.used)
        with patch.object(HTTP, "exchange", side_effect=exchange):
            self.assertEqual(c.check_supplier("peer1"), {
                "status": "AUTHORIZED_LIVE_CONTACT", "supplier": "peer1",
                "mathematical_acceptance": False})
            self.assertEqual(budget.used, initial)
            self.assertEqual(calls, [])
            q = await c.resolve_declaration(origin, body["module_id"], body["relative_name"],
                                             max_bytes=65536, supplier="peer1")
            result = await c.acquire_body(origin, body["body_hash"], max_bytes=65536,
                                           supplier="peer1")
        self.assertEqual(c._candidates[origin], before)
        self.assertEqual(c.describe_candidate(q)["provider"], "peer1")
        self.assertEqual(result["body"], body)
        self.assertEqual([row[0] for row in calls], [21002, 21002])
        self.assertEqual(c.workspace.modules.get_body(body["module_id"], body["relative_name"],
                         body["universes"], body["body_hash"]), body)
        self.assertIs(c._budget, budget)
        self.assertIs(c.grant, grant)
        self.assertEqual(c.grant.deadline, deadline)
        self.assertEqual(budget.used["requests"], initial["requests"]+2)
        self.assertEqual(len(budget.external), 1)
        self.assertIsNone(budget.pending)
        self.no_verification(c)

    async def test_default_supplier_remains_candidate_origin(self):
        c, origin, unused, body, calls, exchange = self.fixture()
        with patch.object(HTTP, "exchange", side_effect=exchange):
            resolved = await c.resolve_declaration(origin, body["module_id"],
                body["relative_name"], max_bytes=65536)
            await c.acquire_body(resolved, body["body_hash"], max_bytes=65536)
        self.assertEqual([row[0] for row in calls], [21001, 21001])
        self.assertEqual(c.describe_candidate(resolved)["provider"], "peer0")
        self.no_verification(c)

    async def test_unauthorized_or_expired_selected_contact_never_dials(self):
        for defect in ("unknown", "expired"):
            with self.subTest(defect=defect):
                c, origin, unused, body, calls, exchange = self.fixture(contact_lifetime_ms=1000)
                deadline = c.grant.deadline
                # Advance only to contact expiry while retaining the original
                # operation's later deadline; no sleep or budget mutation.
                if defect == "expired":
                    expiry = c._search._expiries["peer1"]
                    self.assertLess(expiry+0.001, deadline)
                    clock = patch("transport.located_receipts.time.monotonic",
                                  return_value=expiry+0.001)
                else:
                    clock = patch.object(HTTP, "exchange",
                        side_effect=AssertionError("UNAUTHORIZED_MUST_NOT_EXCHANGE"))
                with clock, patch.object(HTTP, "exchange", side_effect=exchange):
                    with self.assertRaises(ValueError):
                        c.check_supplier("absent" if defect == "unknown" else "peer1")
                self.assertEqual(c.grant.deadline, deadline)
                self.assertEqual(calls, [])  # Real contact validation precedes mock I/O.
                self.no_verification(c)

    async def test_p_and_q_share_one_request_ceiling(self):
        c, origin, unused, body, calls, exchange = self.fixture()
        original = c._budget
        with patch.object(HTTP, "exchange", side_effect=exchange):
            for supplier in ("peer0", "peer1", "peer0", "peer1"):
                await c.resolve_declaration(origin, body["module_id"], body["relative_name"],
                                             max_bytes=65536, supplier=supplier)
            with self.assertRaises(ValueError):
                await c.resolve_declaration(origin, body["module_id"], body["relative_name"],
                                             max_bytes=65536, supplier="peer1")
        self.assertIs(c._budget, original)
        self.assertEqual(original.used["requests"], 8)  # Four search reservations + four fetches.
        self.assertEqual(len(calls), 4)
        self.assertEqual(len(original.external), 1)
        self.assertIsNone(original.pending)
        self.no_verification(c)

    async def test_q_cannot_substitute_a_different_committed_body(self):
        c, origin, unused, body, calls, exchange = self.fixture()
        expected = body["body_hash"]
        body["expression"] = ["sort", ["succ", ["zero"]]]
        with patch.object(HTTP, "exchange", side_effect=exchange):
            with self.assertRaises(ValueError):
                await c.acquire_body(origin, expected, max_bytes=65536, supplier="peer1")
        self.assertEqual(len(calls), 1)
        self.assertIsNone(c.workspace.modules.db.execute(
            "SELECT 1 FROM bodies WHERE module=? AND universes=? AND hash=?",
            (body["module_id"], body["universes"], expected)).fetchone())
        self.no_verification(c)


class InertSupplierClient(T.InertClient):
    """No real contact/budget/authority; helper routing composition only."""
    def __init__(self, specs):
        super().__init__(specs)
        self.allowed = {"inert-same-provider", "Q"}
        self.expired_suppliers = set()
        self.by_supplier = {}
        for (module, name), candidate in list(self.candidates.items()):
            self.by_supplier["inert-same-provider", module, name] = candidate
            other = object()
            self.descriptions[other] = {**deepcopy(self.descriptions[candidate]), "provider": "Q"}
            self.by_supplier["Q", module, name] = other

    def check_supplier(self, supplier):
        self._active()
        OBSERVED["helper_supplier_checks"] += 1
        if supplier not in self.allowed or supplier in self.expired_suppliers:
            raise ValueError("INERT_SUPPLIER_UNAUTHORIZED_OR_EXPIRED")
        return {"status": "AUTHORIZED_LIVE_CONTACT", "supplier": supplier, "mathematical_acceptance": False}

    async def resolve_declaration(self, origin, module, name, *, max_bytes, supplier=None):
        self._active()
        chosen = self.descriptions[origin]["provider"] if supplier is None else supplier
        self.check_supplier(chosen)
        if origin is not self.origin or not 0 < max_bytes <= MIB:
            raise ValueError("INERT_RESOLUTION_SELECTION")
        self.events.append(("resolve", module, C.name_key(name), chosen))
        return self.by_supplier[chosen, module, C.name_key(name)]

    async def acquire_body(self, candidate, digest, *, max_bytes, supplier=None):
        chosen = self.descriptions[candidate]["provider"] if supplier is None else supplier
        self.check_supplier(chosen)
        answer = await super().acquire_body(candidate, digest, max_bytes=max_bytes)
        self.events.append(("supplier_body", chosen, candidate))
        return answer


class HelperControls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        selected = patch.object(H, "CommonsClient", InertSupplierClient)
        selected.start()
        self.addCleanup(selected.stop)

    async def start(self, **caps):
        spec, body = T.E.definitions()
        c = InertSupplierClient([spec])
        helper = H.SemanticReader(c, c.origin, limits={**deepcopy(T.LIMITS), **caps})
        await helper.stage(c.origin, c.entries(c.origin)[0])
        chosen = T.demand("NeedBody", spec, universes=0, body_hash=body["body_hash"])
        c.demands = [chosen]
        helper.preview()
        return c, helper, chosen

    async def test_q_variant_is_not_hidden_by_p_address_cache(self):
        c, h, demand = await self.start()
        before = deepcopy(c.descriptions[c.origin])
        p = await h.resolve(demand, max_bytes=65536)
        q = await h.resolve(demand, max_bytes=65536, supplier="Q")
        again = await h.resolve(demand, max_bytes=65536, supplier="Q")
        self.assertIs(p["candidate"], c.origin)
        self.assertIsNot(q["candidate"], c.origin)
        self.assertEqual(q["description"]["provider"], "Q")
        self.assertIs(again["candidate"], q["candidate"])
        self.assertEqual(again["status"], "NO_PROGRESS")
        self.assertEqual(sum(row[0] == "resolve" for row in c.events), 1)
        self.assertEqual(c.descriptions[c.origin], before)
        self.assertEqual((h.report()["names"], h.report()["groups"]), (1, 1))
        self.assertEqual(h.report()["supplier_candidates"], 2)
        c.demands = []
        h.preview()
        result = h.finish({T.module_id(next(iter(c.specs.values()))): deepcopy(T.ADMISSION)})
        self.assertEqual(result["status"], "READY")
        self.assertEqual(sum(row[0] == "admit" for row in c.events), 1)

    async def test_q_body_uses_held_p_descriptor_without_redundant_name_fetch(self):
        c, h, demand = await self.start()
        answer = await h.fetch_body(demand, max_bytes=65536, supplier="Q")
        self.assertEqual(answer["status"], "FETCHED")
        self.assertEqual(sum(row[0] == "resolve" for row in c.events), 0)
        actual = [row for row in c.events if row[0] == "supplier_body"]
        self.assertEqual(actual, [("supplier_body", "Q", c.origin)])
        again = await h.fetch_body(demand, max_bytes=65536)
        self.assertEqual(again["status"], "NO_PROGRESS")
        self.assertEqual(h.report()["bodies"], 1)
        self.assertEqual(sum(row[0] == "body" for row in c.events), 1)

    async def test_cached_supplier_or_body_cannot_bypass_explicit_authorization(self):
        for cache in ("name", "body"):
            for defect in ("unknown", "expired"):
                with self.subTest(cache=cache, defect=defect):
                    c, h, demand = await self.start()
                    method = h.resolve if cache == "name" else h.fetch_body
                    await method(demand, max_bytes=65536, supplier="Q")
                    supplier = "absent" if defect == "unknown" else "Q"
                    if defect == "expired":
                        c.expired_suppliers.add("Q")
                    before = len(c.events)
                    with self.assertRaisesRegex(ValueError, "SUPPLIER_UNAUTHORIZED_OR_EXPIRED"):
                        await method(demand, max_bytes=65536, supplier=supplier)
                    self.assertEqual(len(c.events), before)
                    self.assertEqual(h.report()["state"], "FAILED")
        # Supplier aliases consume the existing name cap; they do not create
        # an unbounded providers-by-names cache. A contradictory Q description
        # cannot replace the first held mathematical address either.
        for defect in ("cap", "content"):
            c, h, demand = await self.start(**({"names": 1} if defect == "cap" else {}))
            if defect == "content":
                q = c.by_supplier["Q", demand["module"], C.name_key(demand["name"])]
                c.descriptions[q]["descriptor"]["universes"] = 1
            with self.assertRaisesRegex(ValueError, "NAME_LIMIT|SUPPLIER_CONTENT_CONFLICT"):
                await h.resolve(demand, max_bytes=65536, supplier="Q")
            self.assertEqual(h.report()["state"], "FAILED")


FACADE = (
    "test_exact_q_resolution_and_body_preserve_p_origin_and_shared_budget",
    "test_default_supplier_remains_candidate_origin",
    "test_unauthorized_or_expired_selected_contact_never_dials",
    "test_p_and_q_share_one_request_ceiling",
    "test_q_cannot_substitute_a_different_committed_body",
)
HELPER = (
    "test_q_variant_is_not_hidden_by_p_address_cache",
    "test_q_body_uses_held_p_descriptor_without_redundant_name_fetch",
    "test_cached_supplier_or_body_cannot_bypass_explicit_authorization",
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
         patch.object(__import__("asyncio"), "open_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors),
        "scope": "REAL_FACADE_CONTACT_BUDGET_CUSTODY_MOCK_HTTP_AND_INERT_HELPER_COMPOSITION",
        "selected": [*FACADE, *HELPER], "observed": OBSERVED,
        "network_requests": 0, "native_calls": 0, "proof_calls": 0,
        "mathematical_acceptance": False,
        "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in (
            "client/supplier_selected/test_suppliers.py",
            "client/supplier_selected/workspace_evidence.py",
            "client/supplier_selected/semantic_reader.py",
            "client/test_direct_contacts.py", "client/test_semantic_reader.py")}}
    with (OUTPUT/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
