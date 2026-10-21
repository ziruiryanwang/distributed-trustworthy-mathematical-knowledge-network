"""Five located-generation controls: real parsers, INERT channel and owners.

Only already selected fixture helpers are reused. No inherited test suite,
process startup, network authentication or mathematical acceptance is exercised.
"""
import asyncio
import base64
from copy import deepcopy
import importlib
import json
from pathlib import Path
import socket
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / "portable_runtime"), str(SOURCE)]
I = importlib.import_module("iterative_queries.controls")
L = I.overlay("client.located_queries", "located_queries/client/located_queries.py")
from location import protocol as P, observed_route as OR
from location.controller import AdoptedLocationRuntime, SOURCE_NAMES
from location.controller_services import ServiceLocationProcess, ServiceLocatedWorkflow, ROLE_NAMES

OUTPUT = None
OBSERVED = {}
LOCATION = dict(wall_ms=30000, route_operations=1, routing_events=8,
                routing_peer_slots=1, descriptor_requests=1, contacts=1,
                reply_bytes=I.QUERY["bytes"]+4096)
LOCATION_ADDITIVE = tuple(key for key in LOCATION if key != "wall_ms")
ENDPOINT = dict(host="127.0.0.1", port=21001, tls=False, server_name=None)


def envelope(count=2):
    return {"search": I.envelope(I.QUERY, count),
            "location": {**LOCATION, **{key: LOCATION[key]*count for key in LOCATION_ADDITIVE}}}


def peer():
    value, result = int.from_bytes(b"\0\x24\x08\x01\x12\x20"+b"\x01"*32, "big"), ""
    while value:
        value, index = divmod(value, 58)
        result = P._B58[index]+result
    return P.peer_id("1"+result)


class LocatedControls(unittest.IsolatedAsyncioTestCase):
    workspace = I.IterativeControls.workspace
    selected = I.IterativeControls.selected
    dispatch = I.IterativeControls.dispatch
    contacts = I.IterativeControls.contacts

    def setUp(self):
        I.OUTPUT = OUTPUT
        I.IterativeControls.setUp(self)
        self.workflows = []
        original = ServiceLocatedWorkflow.__init__
        def record(workflow, *args, **kwargs):
            original(workflow, *args, **kwargs)
            self.workflows.append(workflow)
        guard = patch.object(ServiceLocatedWorkflow, "__init__", record)
        guard.start(); self.addCleanup(guard.stop)

    async def asyncTearDown(self):
        await I.IterativeControls.asyncTearDown(self)

    def client(self):
        # The larger original fixture grant funds up to twelve location/search
        # attempts plus two acquisitions. No live grant is enlarged or restored.
        limits = I.T.grant_limits()
        limits["acquisition"]["requests"] = 16
        with patch.object(I.T, "grant_limits", return_value=limits):
            client = I.IterativeControls.client(self)
        path = Path(L.__file__).resolve()
        held = I.T.pin(path)
        for owner in client._origin_owners:
            if owner is not None:
                owner._pins[path] = {key: held[key] for key in ("bytes", "sha256")}
        return client

    def channel(self, client):
        unused, policy = self.contacts()
        # Use real owner-path constructors, but never verify/use the explicitly
        # inert runtime/source pin values to launch a child.
        adoption = AdoptedLocationRuntime(SOURCE/"portable_runtime/location",
            {name: "aa"*32 for name in SOURCE_NAMES},
            installation_root=SOURCE/"portable_runtime", workspace_root=self.root)
        config = {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": "reader",
            "namespace": client.workspace.adapter.namespace, "egress": deepcopy(policy._config),
            "state": str(client.grant.directory/"inert-location-state"),
            "limits": {"service_ms": 60000, "commands": 32}}
        channel = ServiceLocationProcess(adoption, {name: "bb"*32 for name in ROLE_NAMES},
            config, client.grant.directory/"inert-location-evidence", deadline=client.grant.deadline)
        script = SimpleNamespace(mode="good", starts=0, closes=0, commands=[],
            entered=asyncio.Event(), release=asyncio.Event(), first_key=None, first_nonce=None)

        async def start():
            self.assertFalse(channel.closed)
            script.starts += 1
            self.assertEqual(script.starts, 1)
            channel.process = SimpleNamespace(returncode=None)
            channel._start_task = asyncio.get_running_loop().create_future()
            channel._start_task.set_result({"role": "reader"})
            return {"role": "reader", "scope": "INERT_CHANNEL_NO_CHILD"}

        async def close():
            if not channel.closed:
                script.closes += 1
                channel.closed = True
                if channel.process is not None: channel.process.returncode = 0
                channel._close_task = asyncio.get_running_loop().create_future()
                channel._close_task.set_result(None)

        async def command(name, ticket, *, until=None):
            self.assertFalse(channel.closed)
            self.assertLessEqual(until, channel.deadline)
            async with channel.lock:
                channel.sequence += 1
                script.commands.append({"command": name, "ticket": deepcopy(ticket), "until": until})
                if script.mode == "cancel_"+name:
                    script.entered.set()
                    try: await script.release.wait()
                    except BaseException:
                        channel.channel_failed = True
                        raise
                if name == "locate":
                    if script.first_key is None: script.first_key = ticket["route_key"]
                    key = script.first_key if script.mode == "stale_key" else ticket["route_key"]
                    return {"ticket": ticket["ticket"], "route_key": key,
                        "peers": [] if script.mode == "empty" else [peer()],
                        "termination": "ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE", "error": None,
                        "census": {**{key: 0 for key in OR.CENSUS}, "events": 1,
                                   "last_query_error": None},
                        "routing_peers_before": 1, "routing_peers_after": 1,
                        "assurance": P.ASSURANCE, "global_complete": False,
                        "mathematical_acceptance": False}
                self.assertEqual(name, "descriptor")
                self.assertNotIn("until", ticket)
                if script.mode == "unavailable":
                    return {"status": "DESCRIPTOR_UNAVAILABLE", "ticket": ticket["ticket"],
                        "peer": ticket["peer"], "reason": "TCP_CONNECT_UNAVAILABLE",
                        "mathematical_acceptance": False}
                request = ticket["request"]
                if script.first_nonce is None: script.first_nonce = request["nonce"]
                nonce = script.first_nonce if script.mode == "stale_nonce" else request["nonce"]
                raw = I.F.compact({"schema": P.REPLY_SCHEMA, "namespace": request["namespace"],
                    "role": P.ROLE, "route_key": request["route_key"], "nonce": nonce,
                    "peer_id": ticket["peer"], "endpoints": [deepcopy(ENDPOINT)],
                    "assurance": P.ASSURANCE, "global_complete": False,
                    "mathematical_acceptance": False})
                return {"ticket": ticket["ticket"], "authenticated_peer": ticket["peer"],
                    "raw_base64": base64.b64encode(raw).decode("ascii"),
                    "request_body_bytes": len(I.F.compact(request)), "reply_body_bytes": len(raw),
                    "framed_reply_bytes": len(raw)+4, "assurance": P.ASSURANCE,
                    "mathematical_acceptance": False}

        channel.start, channel.close, channel.command = start, close, command
        channel.report = lambda: {"scope": "INERT_CHANNEL_NO_CHILD_OR_AUTHENTICATION",
            "commands": channel.sequence, "starts": script.starts, "closes": script.closes,
            "closed": channel.closed, "channel_failed": channel.channel_failed,
            "mathematical_acceptance": False}
        return channel, script, policy

    def reserve(self, client, chosen=None):
        channel, script, policy = self.channel(client)
        L.reserve_located_queries(client, channel, deepcopy(envelope() if chosen is None else chosen), policy)
        return channel, script

    async def next(self, client, typ=I.TYPE_A):
        specifications = I.specs(typ)
        features = client.workspace.adapter.compile_query(specifications)
        routes = [{"features": features, "stripe": 0, "event_cap": 8, "peer_cap": 1, "descriptors": 1}]
        return await L.next_located_query(client, specifications, deepcopy(LOCATION), deepcopy(I.QUERY),
            routes=routes, descriptor_bytes=4096, descriptor_age_ms=10000)

    async def discover(self, client):
        self.assertEqual(len(client._search.endpoints), 1)
        provider = next(iter(client._search.endpoints))
        offer = await client.search_offer(provider, 65536, max_expanded_bytes=131072)
        self.assertEqual(offer["status"], "OFFERED")
        partitions = [item for item in offer["partitions"] if item["anchor_count"]]
        self.assertEqual(len(partitions), 1)
        page = await client.search_page(provider, offer["snapshot_id"], partitions[0]["partition"], 0,
                                        deepcopy(I.T.PAGE), candidates_only=True)
        self.assertEqual(len(page["new_matches"]), 1)
        return await client.resolve(provider, page["new_matches"][0])

    def allocated(self, client, count):
        report = client.report()["iterative_queries"]
        self.assertEqual(report["search_allocated"], {key: I.QUERY[key]*count for key in I.ADDITIVE})
        self.assertEqual(report["location_allocated"], {key: LOCATION[key]*count for key in LOCATION_ADDITIVE})
        self.assertEqual(len(report["generations"]), count)
        return report

    async def test_two_located_queries_real_structural_acquisition(self):
        remote, unused = self.workspace()
        first = self.selected(remote, "located-first-unproved", I.TYPE_A)
        second = self.selected(remote, "located-second-unproved", I.TYPE_B)
        client = self.client()
        original = client._budget, client.grant, client._origin_owners
        chosen = envelope(3)  # Leave one funded slot to isolate later deadline refusal.
        channel, script = self.reserve(client, chosen)
        prepaid = deepcopy(client._budget.used)
        exchange, calls = self.dispatch(remote)
        with patch.object(I.R, "_exchange", exchange), patch.object(I.TC, "exchange", exchange), \
             patch.object(I.DT, "exchange", exchange):
            self.assertEqual((await self.next(client))["status"], "QUERY_CONTACTS_READY")
            a = await self.discover(client)
            self.assertEqual(client.describe_candidate(a)["locator"]["module_id"], first["module"])
            old_workflow, old_search, old_acquisition = self.workflows[-1], client._search, client._acquisition
            old_contact = next(iter(old_acquisition.endpoints.values()))
            expiry = next(iter(old_workflow._workflow._expiries.values()))
            self.assertEqual(next(iter(old_search._expiries.values())), expiry)
            self.assertEqual(old_contact._expires, expiry)
            self.assertEqual((await self.next(client, I.TYPE_B))["status"], "QUERY_CONTACTS_READY")
            self.assertEqual(old_workflow._workflow._state, "RETIRED")
            with self.assertRaises(ValueError): old_contact.validate()
            with self.assertRaises(ValueError): old_search.session.begin_offer("stale", 1024)
            b = await self.discover(client)
            self.assertEqual(client.describe_candidate(b)["locator"]["module_id"], second["module"])
        self.assertIs(client._budget, original[0]); self.assertIs(client.grant, original[1])
        self.assertEqual(client._origin_owners, original[2])
        self.assertEqual(client._budget.used["requests"], prepaid["requests"]+2)
        self.assertEqual(prepaid["requests"], 12)
        self.assertEqual(prepaid["reply_bytes"], chosen["location"]["reply_bytes"])
        self.assertEqual(len(client._budget.external), 1)
        self.assertEqual(script.starts, 1)
        self.assertEqual(len(script.commands), 4)
        keys = [row["ticket"]["route_key"] for row in script.commands if row["command"] == "locate"]
        self.assertNotEqual(*keys)
        self.assertEqual(client.workspace.modules.get_group(first["module"], first["name"])[0], first["opening"])
        self.assertEqual(client.workspace.modules.get_group(second["module"], second["name"])[0], second["opening"])
        OBSERVED["two_queries"] = {"report": self.allocated(client, 2),
            "in_memory_http_dispatches": len(calls), "inert_channel_commands": deepcopy(script.commands),
            "exact_original_descriptor_expiry": True, "mathematical_acceptance": False}
        # A search subdeadline does not revoke local work under the still-live
        # original grant. Advance only the monotonic clock, never a deadline.
        after_search = client._query_envelope.deadline+0.001
        self.assertLess(after_search, client.grant.deadline)
        commands_before = len(script.commands)
        with patch.object(L.time, "monotonic", return_value=after_search):
            self.assertEqual(client.describe_candidate(b)["locator"]["module_id"], second["module"])
            with self.assertRaises(ValueError): await self.next(client)
        self.assertEqual(len(script.commands), commands_before)
        OBSERVED["expired_search_preserves_local_describe_but_not_next_query"] = True
        await client.close()
        self.assertTrue(channel.closed and original[0].closed)
        self.assertEqual(script.closes, 1)
        # Independently normal channel closure is not a failed mathematical
        # action. The original grant still permits read-only/local activity.
        probe = self.client()
        probe_channel, probe_script = self.reserve(probe)
        await probe_channel.close()
        probe._active()
        self.assertFalse(probe._budget.closed)
        self.assertEqual(probe._state, "OPEN")
        await probe.close()
        self.assertTrue(probe._budget.closed)
        self.assertEqual(probe_script.closes, 1)
        self.assertTrue(all(owner is None or owner.closes == 1 for owner in probe._origin_owners))
        OBSERVED["normal_closed_channel_preserves_original_local_lifetime"] = True

    async def test_empty_and_unavailable_retire_then_continue(self):
        summaries = []
        for mode in ("empty", "unavailable"):
            client = self.client(); channel, script = self.reserve(client)
            script.mode = mode
            answer = await self.next(client)
            self.assertEqual(answer["status"], "NO_CONTACTS_IN_SELECTED_ROUTE_PLAN")
            workflow = self.workflows[-1]
            self.assertIsNone(client._search); self.assertIsNone(client._acquisition)
            self.assertEqual(workflow._workflow.report()["pending_requests"], 0)
            self.assertEqual(workflow._workflow._state, "RETIRED_NO_CONTACTS")
            before = deepcopy(client._budget.used)
            if mode == "unavailable":
                self.assertEqual(workflow._workflow._used["descriptor_reply_bytes"], 4096)
            script.mode = "good"
            self.assertEqual((await self.next(client, I.TYPE_B))["status"], "QUERY_CONTACTS_READY")
            self.assertEqual(workflow._workflow._state, "RETIRED_NO_CONTACTS")
            self.assertEqual(client._budget.used, before)
            self.assertEqual(script.starts, 1)
            summaries.append({"case": mode, "report": self.allocated(client, 2)})
        OBSERVED["settled_no_contact_continuation"] = summaries

    async def test_cross_generation_reply_binding_refuses(self):
        for mode in ("stale_key", "stale_nonce"):
            client = self.client(); channel, script = self.reserve(client)
            await self.next(client)
            script.mode = mode
            with self.assertRaisesRegex(ValueError, "OBSERVED_ROUTE_CHANNEL_BINDING|LOCATION_DESCRIPTOR_BINDING"):
                await self.next(client, I.TYPE_B)
            self.assertEqual(self.workflows[-1]._workflow.report()["pending_requests"], 0)
            self.assertEqual(client._state, "FAILED")
            self.assertTrue(channel.closed and client._budget.closed)
            self.assertEqual(len(client._budget.external), 1)
            self.allocated(client, 2)
        OBSERVED["cross_generation_real_parser_refusal"] = True

    async def test_route_and_descriptor_cancellation_settle_without_renewal(self):
        summaries = []
        for phase in ("locate", "descriptor"):
            client = self.client(); channel, script = self.reserve(client)
            script.mode = "cancel_"+phase
            task = asyncio.create_task(self.next(client))
            entered = asyncio.create_task(script.entered.wait())
            done, unused_pending = await asyncio.wait((task, entered), return_when=asyncio.FIRST_COMPLETED)
            if task in done:
                entered.cancel()
                await asyncio.gather(entered, return_exceptions=True)
                await task  # Surface construction errors instead of waiting until the suite cap.
                self.fail("INERT_COMMAND_DID_NOT_REACH_CANCELLATION_BOUNDARY")
            await entered
            workflow = self.workflows[-1]._workflow
            self.assertIsNotNone(workflow._pending)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError): await task
            self.assertIsNone(workflow._pending)
            self.assertEqual(workflow._used["routing_events"], 8)
            if phase == "descriptor": self.assertEqual(workflow._used["descriptor_reply_bytes"], 4096)
            self.assertEqual(client._state, "FAILED")
            self.assertFalse(client._busy)
            self.assertTrue(channel.closed and client._budget.closed)
            self.assertTrue(all(owner is None or owner.closes == 1 for owner in client._origin_owners))
            self.assertEqual(client.report()["iterative_queries"]["status"], "FAILED")
            self.allocated(client, 1)
            summaries.append({"phase": phase, "used": deepcopy(workflow._used)})
        OBSERVED["cancel_settlement"] = summaries

    async def test_aggregate_location_cap_refuses_before_command(self):
        client = self.client(); chosen = envelope()
        chosen["location"]["route_operations"] = 1
        channel, script = self.reserve(client, chosen)
        await self.next(client)
        before, commands = deepcopy(client._budget.used), len(script.commands)
        with self.assertRaises(ValueError): await self.next(client, I.TYPE_B)
        self.assertEqual(len(script.commands), commands)
        self.assertEqual(client._budget.used, before)
        self.assertEqual(script.starts, 1)
        self.assertTrue(channel.closed and client._budget.closed)
        self.assertEqual(client._state, "FAILED")
        OBSERVED["location_cap_no_io_or_renewal"] = True


SELECTED = (
    "test_two_located_queries_real_structural_acquisition",
    "test_empty_and_unavailable_retire_then_continue",
    "test_cross_generation_reply_binding_refuses",
    "test_route_and_descriptor_cancellation_settle_without_renewal",
    "test_aggregate_location_cap_refuses_before_command",
)


def main():
    global OUTPUT
    if len(sys.argv) != 3 or sys.argv[1] != "--output": raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output: raise ValueError("CANONICAL_OUTPUT_REQUIRED")
    OUTPUT = output/"located-fixtures"; OUTPUT.mkdir()
    suite = unittest.TestSuite(LocatedControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "open_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")), \
         patch.object(socket, "create_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "errors": len(result.errors), "failures": len(result.failures), "skipped": len(result.skipped),
        "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "REAL_LOCATION_TICKET_PARSERS_STRUCTURAL_SEARCH_INERT_CHANNEL_AND_OWNERS",
        "mathematical_acceptance": False, "channel_authentication_tested": False,
        "native_calls": 0, "proof_calls": 0, "network_operations": 0}
    with (output/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())
