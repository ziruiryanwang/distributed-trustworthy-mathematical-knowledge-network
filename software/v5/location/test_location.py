"""Focused location trust/accounting controls; no DHT, socket or proof run."""
import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import formal_features as F
from transport import clients as HTTP
from transport.http_provider import Endpoint
from location import protocol as P
from location.workflow import WorkflowBudget

NS, FEATURES = "a" * 64, ["1" * 64, "2" * 64]
SEARCH = dict(providers=2, snapshots=2, requests=2, pages=1, examined=32,
              candidates=8, bytes=16384, wall_ms=9000, inflight=1)
LIMITS = dict(wall_ms=10000, route_operations=2, routing_events=16,
              routing_peer_slots=4, descriptor_requests=4, contacts=2, reply_bytes=32768)
EP = {"host": "127.0.0.1", "port": 8765, "tls": False, "server_name": None}


def peer(fill=1):
    raw = b"\0\x24\x08\x01\x12\x20" + bytes([fill]) * 32
    value, out = int.from_bytes(raw, "big"), ""
    while value:
        value, index = divmod(value, 58)
        out = P._B58[index] + out
    return "1" + out


def policy():
    return P.OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
        "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 8765},
                                               {"host": "127.0.0.1", "port": 8766}]})


def descriptor(request, selected_peer=None, endpoints=None):
    return {"schema": P.REPLY_SCHEMA, "namespace": request["namespace"], "role": P.ROLE,
        "route_key": request["route_key"], "nonce": request["nonce"],
        "peer_id": selected_peer or peer(), "endpoints": deepcopy(endpoints or [EP]),
        "assurance": P.ASSURANCE, "global_complete": False, "mathematical_acceptance": False}


class Clock:
    def __init__(self): self.value = 0.0
    def __call__(self): return self.value


class LocationContracts(unittest.TestCase):
    def workflow(self, **limits):
        self.clock = Clock()
        return WorkflowBudget(NS, FEATURES, {**LIMITS, **limits}, SEARCH, policy(), clock=self.clock)

    def located(self, workflow):
        route = workflow.begin_route(FEATURES, event_cap=8, peer_cap=2)
        result = workflow.accept_route(route["ticket"], [peer()])
        return result["route_key"]

    def adopted(self, workflow, age=10000):
        key = self.located(workflow)
        ticket = workflow.begin_descriptor(peer(), key, max_age_ms=age)
        raw = F.compact(descriptor(ticket["request"]))
        result = workflow.accept_descriptor(ticket["ticket"], raw, peer())
        return result["contacts"][0]

    def test_exact_domain_predicate_and_stripe_key_separation(self):
        key = P.route_key(NS, FEATURES, 3)
        expected = hashlib.sha256(b"DMKN-V5-INDEX-RENDEZVOUS-V1\0" + F.compact({
            "namespace": NS, "role": "formal-index-v1", "predicate": {"all": FEATURES}, "stripe": 3})).hexdigest()
        self.assertEqual(key, expected)
        self.assertEqual(len({key, P.route_key(NS, FEATURES, 4), P.route_key(NS, FEATURES[:1], 3),
                              P.route_key("b" * 64, FEATURES, 3)}), 4)
        for features, stripe in ((list(reversed(FEATURES)), 0), ([FEATURES[0]] * 2, 0),
                                 ([], 0), (FEATURES, True), (FEATURES, 256)):
            with self.assertRaises(ValueError): P.route_key(NS, features, stripe)

    def test_peer_id_profile_and_exact_direct_address_policy(self):
        selected = policy()
        self.assertEqual(P.peer_id(peer()), peer())
        self.assertEqual(selected.peer_address("/ip4/127.0.0.1/tcp/8765/p2p/" + peer(), peer()),
                         "/ip4/127.0.0.1/tcp/8765/p2p/" + peer())
        for value in (peer() + "1", peer()[:-1], "0" * 52, "1" * 52):
            with self.assertRaises(ValueError): P.peer_id(value)
        for value in ("/dns4/localhost/tcp/8765", "/ip4/127.0.0.1/tcp/08765",
                      "/ip4/127.0.0.1/tcp/8767", "/ip4/10.0.0.1/tcp/8765",
                      "/ip4/127.0.0.1/tcp/8765/p2p/" + peer(2)):
            with self.assertRaises(ValueError): selected.peer_address(value, peer())

    def test_public_endpoint_egress_and_no_remote_ca_or_url_authority(self):
        selected = P.OwnerEgressPolicy({"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "public-ipv4",
                                       "public_ports": [443], "test_endpoints": []})
        public = {"host": "8.8.8.8", "port": 443, "tls": True, "server_name": "example.org"}
        self.assertIsNone(selected.endpoint(public).ca_file)
        self.assertEqual(selected.peer_address("/ip4/8.8.8.8/tcp/443"), "/ip4/8.8.8.8/tcp/443")
        for fields in ({"host": "127.0.0.1"}, {"host": "10.0.0.1"}, {"host": "169.254.169.254"},
                       {"host": "100.64.0.1"}, {"host": "0.0.0.0"}, {"host": "224.0.0.1"},
                       {"host": "192.0.2.1"}, {"host": "example.org"}, {"host": "::1"},
                       {"tls": False}, {"tls": 1}, {"port": 80}, {"port": True},
                       {"server_name": "example.org/evil"}, {"server_name": "Example.org"},
                       {"ca_file": "C:\\remote.pem"}):
            with self.assertRaises(ValueError): selected.endpoint({**public, **fields})

    def test_descriptor_exact_peer_nonce_key_and_assurance_binding(self):
        request = P.descriptor_request(NS, FEATURES, 0, "b" * 64, 4096)
        good = descriptor(request)
        endpoints = P.verify_descriptor(F.compact(good), request, peer(), policy())
        self.assertEqual(endpoints, (Endpoint(**EP),))
        for key, value in (("peer_id", peer(2)), ("nonce", "c" * 64), ("route_key", "c" * 64),
                           ("namespace", "c" * 64), ("role", "custody"), ("global_complete", True),
                           ("mathematical_acceptance", True), ("assurance", "TRUSTED"),
                           ("endpoints", [EP, EP]), ("extra", "ignored?")):
            with self.assertRaises(ValueError):
                P.verify_descriptor(F.compact({**good, key: value}), request, peer(), policy())
        with self.assertRaises(ValueError):
            P.verify_descriptor(F.compact(good) + b"\n", request, peer(), policy())

    def test_route_failures_and_duplicates_keep_full_allowance(self):
        workflow = self.workflow()
        first = workflow.begin_route(FEATURES, event_cap=8, peer_cap=2)
        first["event_cap"] = 0
        workflow.abandon_route(first["ticket"])
        second = workflow.begin_route(FEATURES, event_cap=8, peer_cap=2)
        with self.assertRaises(ValueError): workflow.accept_route(second["ticket"], [peer(), peer()])
        result = workflow.report()
        self.assertEqual(result["used"]["routing_events"], 16)
        self.assertEqual(result["used"]["routing_peer_slots"], 4)
        self.assertEqual(result["located_peer_route_pairs"], 0)
        self.assertEqual(result["pending_requests"], 0)
        self.assertIsNone(result["dht_wire_bytes"])
        with self.assertRaises(ValueError): workflow.begin_route(FEATURES, event_cap=1, peer_cap=1)

    def test_route_query_subset_and_pending_ticket_protection(self):
        workflow = self.workflow()
        with self.assertRaises(ValueError): workflow.begin_route(["3" * 64], event_cap=1, peer_cap=1)
        first = workflow.begin_route(FEATURES[:1], event_cap=8, peer_cap=2)
        with self.assertRaises(ValueError): workflow.begin_search()
        with self.assertRaises(ValueError): workflow.begin_route(FEATURES, event_cap=1, peer_cap=1)
        with self.assertRaises(ValueError): workflow.abandon_descriptor(first["ticket"])
        self.assertEqual(workflow.report()["pending_requests"], 1)
        workflow.abandon_route(first["ticket"])

    def test_search_preallocation_cannot_be_spent_by_descriptor_failures(self):
        workflow = self.workflow(reply_bytes=SEARCH["bytes"] + 4096)
        key = self.located(workflow)
        ticket = workflow.begin_descriptor(peer(), key, max_bytes=4096)
        self.assertEqual(workflow.report()["committed_reply_capacity"], SEARCH["bytes"] + 4096)
        ticket["max_reply_bytes"] = 1
        workflow.abandon_descriptor(ticket["ticket"])
        self.assertEqual(workflow.report()["used"]["descriptor_reply_bytes"], 4096)
        with self.assertRaises(ValueError): workflow.begin_descriptor(peer(), key, max_bytes=1024)
        with self.assertRaises(ValueError): workflow.begin_search()

    def test_invalid_or_expired_descriptor_charges_before_validation(self):
        for mode in ("peer", "nonce", "expiry", "raw"):
            workflow = self.workflow()
            key = self.located(workflow)
            ticket = workflow.begin_descriptor(peer(), key, max_age_ms=100)
            reply = descriptor(ticket["request"])
            if mode == "nonce": reply["nonce"] = "0" * 64
            if mode == "expiry": self.clock.value = .101
            raw = b"not json" if mode == "raw" else F.compact(reply)
            with self.assertRaises(ValueError):
                workflow.accept_descriptor(ticket["ticket"], raw, peer(2) if mode == "peer" else peer())
            report = workflow.report()
            self.assertEqual(report["used"]["descriptor_reply_bytes"], len(raw))
            self.assertEqual(report["contacts"], 0)
            self.assertEqual(report["pending_requests"], 0)

    def test_contact_duplicates_consume_attempts_but_not_unbounded_memory(self):
        workflow = self.workflow(descriptor_requests=2)
        key = self.located(workflow)
        for unused in range(2):
            ticket = workflow.begin_descriptor(peer(), key)
            workflow.accept_descriptor(ticket["ticket"], F.compact(descriptor(ticket["request"])), peer())
        self.assertEqual(workflow.report()["contacts"], 1)
        self.assertEqual(workflow.report()["used"]["descriptor_requests"], 2)
        with self.assertRaises(ValueError): workflow.begin_descriptor(peer(), key)

    def test_one_search_session_and_absolute_workflow_deadline(self):
        workflow = self.workflow()
        contact = self.adopted(workflow)
        self.clock.value = 3.0
        client = workflow.begin_search()
        self.assertLessEqual(client.session.deadline, 10.0)
        self.assertEqual(workflow.report()["search_reply_allocation"], SEARCH["bytes"])
        with self.assertRaises(ValueError): workflow.begin_search()
        with self.assertRaises(ValueError): workflow.begin_route(FEATURES, event_cap=1, peer_cap=1)
        calls = []
        async def no_offer(endpoint, route, request, maximum, timeout):
            calls.append((endpoint, timeout))
            raw = F.compact({"schema": "DMKN_DISCOVERY_OFFER_V1", "namespace": NS,
                "features": FEATURES, "status": "NO_OFFER", "reason": "ROLE_NOT_SERVED",
                "summary": None, "global_complete": False, "mathematical_acceptance": False})
            return {"status": 200, "raw": raw, "header_bytes": 0,
                    "request_bytes": len(F.compact(request)), "reply_bytes": len(raw)}
        with patch.object(HTTP, "exchange", new=no_offer):
            for unused in range(2):
                self.assertEqual(asyncio.run(client.offer(contact, 8192))["status"], "NO_OFFER")
            with self.assertRaises(ValueError): asyncio.run(client.offer(contact, 8192))
        self.assertEqual(len(calls), 2)
        self.assertEqual(client.report()["session"]["used"]["requests"], 2)
        self.assertEqual(client.report()["session"]["snapshot_budget"]["charged_attempt_slots"], 2)
        self.clock.value = 10.001
        self.assertEqual(workflow.report()["status"], "DEADLINE_EXHAUSTED")

    def test_expiry_or_contact_mutation_refuses_before_dial_and_settles_ticket(self):
        for mode in ("expired", "changed"):
            workflow = self.workflow()
            contact = self.adopted(workflow, age=100)
            client = workflow.begin_search()
            if mode == "expired": self.clock.value = .101
            else: client.endpoints[contact] = Endpoint("127.0.0.1", 8766)
            async def forbidden(*args, **kwargs): raise AssertionError("NETWORK_MUST_NOT_BE_CALLED")
            with patch.object(HTTP, "exchange", new=forbidden):
                with self.assertRaises(ValueError): asyncio.run(client.offer(contact, 8192))
            self.assertEqual(client.session.report()["used"]["bytes"], 8192)
            self.assertEqual(client.session.report()["pending_requests"], 0)
            self.assertEqual(client.report()["http"]["completed_requests"], 0)

    def test_transport_overrun_and_owner_policy_copy(self):
        config = {"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test", "public_ports": [],
                  "test_endpoints": [{"host": "127.0.0.1", "port": 8765}]}
        selected = P.OwnerEgressPolicy(config)
        config["test_endpoints"].append({"host": "127.0.0.1", "port": 9999})
        with self.assertRaises(ValueError): selected.endpoint({**EP, "port": 9999})
        workflow = self.workflow()
        key = self.located(workflow)
        ticket = workflow.begin_descriptor(peer(), key, max_bytes=1024)
        with self.assertRaises(ValueError): workflow.accept_descriptor(ticket["ticket"], b"x" * 1025, peer())
        self.assertEqual(workflow.report()["status"], "TRANSPORT_BYTE_VIOLATION")
        self.assertEqual(workflow.report()["used"]["descriptor_reply_bytes"], 1025)
        self.assertEqual(workflow.report()["contacts"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
