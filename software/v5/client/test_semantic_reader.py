"""New helper/member controls; mathematical authority and semantic walk are INERT.

Reuse only frozen canonical fixture constructors, never their old test suites.
Canonical inventory/subset parsing and readback rebinding are real pure checks.
The helper's client is explicitly patched; readback stores/accounting are inert.
No owner, live warrant, foundation import, network, native check or proof runs.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
import client

# Root selects this unused overlay explicitly; never silently test its frozen
# predecessor. No actual facade/owner is constructed by this import.
overlay_spec = importlib.util.spec_from_file_location(
    "client.workspace_staged", SOURCE/"staging_members/workspace_staged.py")
W = importlib.util.module_from_spec(overlay_spec)
sys.modules[overlay_spec.name] = W
overlay_spec.loader.exec_module(W)
client.workspace_staged = W
from client import semantic_reader as H
from client import test_workspace_evidence as E
from client import test_workspace_mixed as T
from delta_claims.claims import expected_journal
from modules import codec as C

MIB = 1024**2
LIMITS = {"modules": 8, "names": 32, "groups": 32, "bodies": 16,
          "steps": 64, "data_bytes": MIB}
ADMISSION = {"native_cpu_seconds": 2, "receipt_cpu_seconds": 2,
             "wall_seconds": 10, "memory_mib": 128}
COUNTS = {"inert_stages": 0, "inert_admissions": 0, "inert_imports": 0,
          "inert_resolves": 0, "inert_body_fetches": 0}


def module_id(spec):
    return C.module_id(spec)


class InertClient:
    """Only public composition surfaces, with explicitly synthetic outcomes."""
    def __init__(self, specs):
        self.specs = {module_id(spec): deepcopy(spec) for spec in specs}
        self.grant = SimpleNamespace(_limits={"imports": {
            "max_sources": 8, "max_members": 16, "data_bytes": MIB}})
        self.expired = self.closed = False
        self.active_calls = 0
        self.descriptions, self.candidates, self.tokens, self.warrants = {}, {}, {}, {}
        self.events, self.demands = [], []
        self.preview_acceptance = False
        self.preview_extra_context = False
        self.packet_members, self.no_standalone_offer = {}, set()
        self.describe_members_override = None
        self.fail_admission = None
        self.import_status = "UNTRUSTED_AUTHORING_CONTEXT_READY"
        self.context = object()  # INERT sentinel, not an actual authoring context.
        self.import_arguments = None
        for module, spec in self.specs.items():
            for index, group in enumerate(spec["groups"]):
                for descriptor in group["declarations"]:
                    candidate = object()
                    name = descriptor["name"]
                    self.candidates[module, C.name_key(name)] = candidate
                    self.descriptions[candidate] = {
                        "provider": "inert-same-provider",
                        "locator": {"module_id": module, "relative_name": deepcopy(name),
                                    "group_index": index},
                        "opening": C.group_opening(spec, index),
                        "descriptor": deepcopy(descriptor),
                    }
        first = specs[0]
        self.origin = self.candidates[module_id(first),
                                      C.name_key(first["groups"][0]["declarations"][0]["name"])]

    def _active(self):
        self.active_calls += 1
        if self.closed or self.expired:
            raise ValueError("INERT_ORIGINAL_CLIENT_DEADLINE_OR_CLOSE")

    def describe_candidate(self, candidate):
        return deepcopy(self.descriptions[candidate])

    def entries(self, candidate):
        module = self.descriptions[candidate]["locator"]["module_id"]
        if module in self.no_standalone_offer:
            return []
        return [{"packet_sha256": hashlib.sha256((module+":"+str(rank)).encode()).hexdigest(),
                 "packet_bytes": 1000+rank} for rank in (0, 1)]

    def member(self, module, rank=0):
        summary = C.summarize(self.specs[module])
        return {"module": module, "summary": summary,
                "journal": list(expected_journal(summary, rank, T.B.RELATION_IMAGE))}

    async def packet_offers(self, candidate, **unused):
        self.events.append(("offers", candidate))
        return {"packets": self.entries(candidate)}

    async def stage_packet(self, candidate, entry):
        self._active()
        entries = self.entries(candidate)
        if entry not in entries:
            raise ValueError("INERT_UNOFFERED_PACKET")
        rank = entries.index(entry)
        description = self.describe_candidate(candidate)
        module = description["locator"]["module_id"]
        token = object()
        root = self.member(module, rank)
        members = self.packet_members.get(module, [root])
        self.tokens[token] = {"status": "STAGED_UNTRUSTED_EVIDENCE",
            "selection": {**deepcopy(root), **entry},
            "members": deepcopy(members),
            "provider": description["provider"],
            "candidate": {key: value for key, value in description.items() if key != "provider"},
            "admission_consumed": False, "mathematical_acceptance": False}
        self.events.append(("stage", module, deepcopy(entry)))
        COUNTS["inert_stages"] += 1
        return token

    def describe_staged(self, token):
        return deepcopy(self.tokens[token])

    async def resolve_declaration(self, origin, module, name, *, max_bytes):
        self._active()
        if origin is not self.origin or not 0 < max_bytes <= MIB:
            raise ValueError("INERT_RESOLUTION_SELECTION")
        self.events.append(("resolve", module, C.name_key(name)))
        COUNTS["inert_resolves"] += 1
        return self.candidates[module, C.name_key(name)]

    async def acquire_body(self, candidate, body_hash, *, max_bytes):
        self._active()
        description = self.descriptions[candidate]
        module, name = description["locator"]["module_id"], description["locator"]["relative_name"]
        options = (["sort", ["zero"]], ["sort", ["succ", ["zero"]]])
        expression = next((value for value in options if C.body_id(value, 0) == body_hash), None)
        if expression is None or not 0 < max_bytes <= MIB:
            raise ValueError("INERT_BODY_SELECTION")
        self.events.append(("body", module, body_hash))
        COUNTS["inert_body_fetches"] += 1
        return {"status": "VERIFIED_BODY", "body": {
            "schema": E.BODY_SCHEMA, "module_id": module, "relative_name": deepcopy(name),
            "universes": 0, "body_hash": body_hash, "expression": expression}}

    def preview_context(self, tokens, openings, bodies, *, limits=None, selected_members=None):
        self._active()
        if len(tokens) != len(set(tokens)):
            raise ValueError("INERT_DUPLICATE_PACKET_TOKEN")
        if any(self.tokens[token]["admission_consumed"] for token in tokens):
            raise ValueError("INERT_PREVIEW_AFTER_CONSUMPTION")
        if selected_members is not None:
            modules = set()
            for row in selected_members:
                if row["token"] not in tokens or row["module"] in modules:
                    raise ValueError("INERT_FOREIGN_TOKEN_OR_DUPLICATE_MODULE")
                if not any(member["module"] == row["module"]
                           and bytes(member["journal"]) == row["journal"]
                           for member in self.tokens[row["token"]]["members"]):
                    raise ValueError("INERT_UNHELD_MEMBER_JOURNAL")
                modules.add(row["module"])
        self.events.append(("preview", len(tokens), len(openings), len(bodies)))
        result = {"status": "NEED_STRUCTURAL_CONTEXT_DATA" if self.demands else "STRUCTURAL_CLOSURE_STAGED",
                "demands": deepcopy(self.demands), "mathematical_acceptance": self.preview_acceptance,
                "cost": {"frontend_theorem_ancestor_proof_bytes": 0, "synthetic": True}}
        if self.preview_extra_context:
            result["context"] = self.context
        return result

    def admit_staged(self, token, *, expected_exact_journal, **limits):
        self._active()
        row = self.tokens[token]
        if row["admission_consumed"] or bytes(row["selection"]["journal"]) != expected_exact_journal:
            raise ValueError("INERT_REUSED_OR_CHANGED_ADMISSION")
        if limits != ADMISSION:
            raise ValueError("INERT_CHANGED_ADMISSION_SELECTION")
        row["admission_consumed"] = True
        module = row["selection"]["module"]
        self.events.append(("admit", module))
        COUNTS["inert_admissions"] += 1
        if module == self.fail_admission:
            raise ValueError("INERT_LATER_ADMISSION_FAILURE")
        warrant = object()
        self.warrants[warrant] = row
        return warrant

    def describe(self, warrant):
        row = self.warrants[warrant]
        live = deepcopy(row["selection"])
        live["journal"] = bytes(live["journal"])
        members = row["members"] if self.describe_members_override is None else self.describe_members_override
        return {"kind": "mixed", "live": live, "members": deepcopy(members)}

    def import_context(self, sources, selected, openings, bodies, **unused):
        self._active()
        if any(source["warrant"] not in self.warrants for source in sources):
            raise ValueError("INERT_PREVIEW_TOKEN_USED_AS_WARRANT")
        self.events.append(("import", len(sources)))
        COUNTS["inert_imports"] += 1
        self.import_arguments = sources, selected, openings, bodies
        ready = self.import_status == "UNTRUSTED_AUTHORING_CONTEXT_READY"
        return {"status": self.import_status, "context": self.context if ready else None,
                "demands": [] if ready else [{"kind": "INERT_LIVE_IMPORT_DEMAND"}],
                "cost": {"synthetic": True}}


def demand(kind, spec, name=None, **extra):
    if name is None:
        name = spec["groups"][0]["declarations"][0]["name"]
    return {"kind": kind, "module": module_id(spec), "name": deepcopy(name), **extra}


class StructuralControls(unittest.TestCase):
    """New inventory/subset code is real; no issuer, storage or semantic walk."""
    def inspect(self, raw):
        return E.P.inspect_evidence(raw, T.Envelope(), aggregate_image=T.IMAGE,
                                    terminal_receipt_bytes=65536)

    def inventory(self, raw, *, maximum=16):
        kind, unused_summary, exact, unused_census = self.inspect(raw)
        return W._member_inventory(raw, kind, exact, envelope=T.Envelope(),
                                   aggregate_image=T.IMAGE, max_members=maximum)

    def mixed_snapshot(self):
        raw, summary = T.mixed_packet()
        unused_kind, unused_summary, exact, unused_census = self.inspect(raw)
        spec = T.spec("syntheticChild")
        descriptor = spec["groups"][0]["declarations"][0]
        opening = C.group_opening(spec, 0)
        selection = {"module": C.summary_id(summary), "journal": list(exact),
            "summary": summary, "packet_sha256": hashlib.sha256(raw).hexdigest(),
            "packet_bytes": len(raw)}
        snapshot = {"selection": selection, "members": self.inventory(raw),
            "provider": "INERT-HELD-DATA",
            "candidate": {"locator": {"module_id": selection["module"],
                "relative_name": descriptor["name"], "group_index": 0},
                "opening": opening, "descriptor": descriptor}}
        return raw, snapshot

    def test_exact_frontier_delta_and_terminal_inventories(self):
        raw, snapshot = self.mixed_snapshot()
        aggregate_members, unused_header = T.members_and_header()
        child = expected_journal(C.summarize(T.spec("syntheticChild")), 1, T.B.RELATION_IMAGE)
        actual = [bytes(row["journal"]) for row in snapshot["members"]]
        self.assertEqual(actual, sorted([aggregate_members[0], child]))
        self.assertNotIn(aggregate_members[1], actual)  # Unopened aggregate member.
        # Ordinary mixed packets can carry I directly, with no standalone
        # terminal-A packet offer for that internal module.
        i_value = C.parse_json(raw)
        i_frontier = i_value["frontiers"][0]
        i_value["claims"][0]["tag"] = 0
        i_value["claims"][0]["statement"] = i_frontier["journal"]
        i_frontier["member_index"], i_frontier["siblings"] = 0, []
        self.assertEqual(self.inventory(C.canonical(i_value)), snapshot["members"])
        for row in snapshot["members"]:
            parsed = T.B.member_journal(bytes(row["journal"]))
            self.assertEqual((row["module"], row["summary"]),
                             (parsed["module"], parsed["summary"]))
            self.assertEqual(set(row), {"module", "journal", "summary"})
        terminal, exact = E.terminal(T.spec("terminalSelectedMember"), 2)
        self.assertEqual(self.inventory(terminal), [{
            "module": T.B.member_journal(exact)["module"], "journal": list(exact),
            "summary": T.B.member_journal(exact)["summary"]}])
        with self.assertRaisesRegex(ValueError, "MEMBER_INVENTORY_LIMIT"):
            self.inventory(raw, maximum=1)

    def test_exact_subset_rejects_foreign_forged_and_duplicate_module_choices(self):
        unused_raw, snapshot = self.mixed_snapshot()
        token, foreign = W.StagedEvidence(), W.StagedEvidence()
        snapshots = {token: snapshot}
        choices = [{"token": token, "module": row["module"], "journal": bytes(row["journal"])}
                   for row in snapshot["members"]]
        selected = W._select_member_rows(snapshots, choices, 16)
        self.assertEqual(len(selected), 2)
        for choice, row in zip(choices, selected):
            self.assertEqual(row["module"], choice["module"])
            self.assertEqual(bytes(row["journal"]), choice["journal"])
            self.assertEqual(row["packet_sha256"], snapshot["selection"]["packet_sha256"])
            self.assertEqual(set(row), {"module", "journal", "summary",
                                       "packet_sha256", "packet_bytes"})
        # A genuine-shaped other rank is still not this packet's exact member.
        parsed = T.B.member_journal(choices[0]["journal"])
        forged = expected_journal(parsed["summary"], parsed["rank"]+1, T.B.RELATION_IMAGE)
        mutations = ([], [dict(choices[0], token=foreign)],
                     [dict(choices[0], journal=forged)],
                     [dict(choices[0], journal=list(choices[0]["journal"]))],
                     [choices[0], dict(choices[0])])
        for index, changed in enumerate(mutations):
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                W._select_member_rows(snapshots, changed, 16)
        with self.assertRaisesRegex(ValueError, "SELECTED_MEMBER_LIST"):
            W._select_member_rows(snapshots, choices, 1)

    def test_readback_rejects_changed_cached_inventory(self):
        raw, snapshot = self.mixed_snapshot()
        token = W.StagedEvidence()
        held = deepcopy(snapshot)
        envelope = T.Envelope()

        class InertHeldData:
            _stage = W.CommonsClient._stage
            _structural_members = W.CommonsClient._structural_members
            _read_stage = W.CommonsClient._read_stage

            def __init__(self):
                self._staged = {token: (C.canonical(held), False)}
                self._aggregate_image = T.IMAGE
                self.grant = SimpleNamespace(_limits={"imports": {"max_members": 16}})
                self.workspace = SimpleNamespace(_envelope=envelope,
                    packets=SimpleNamespace(get=lambda *unused: raw),
                    modules=SimpleNamespace(get_group=lambda *unused:
                        (held["candidate"]["opening"], held["candidate"]["descriptor"])))

            def _inspect(self, value):
                return E.P.inspect_evidence(value, envelope, aggregate_image=T.IMAGE,
                                           terminal_receipt_bytes=65536)

            @staticmethod
            def _store(method, *args):
                return method(*args)

            @staticmethod
            def _charge(value):
                pass  # Explicitly inert accounting; no operation/owner exists.

        inert = InertHeldData()
        returned, actual_raw, consumed = inert._read_stage(token)
        self.assertEqual(returned, snapshot)
        self.assertEqual(actual_raw, raw)
        self.assertIs(consumed, False)
        held["members"] = held["members"][:1]
        inert._staged[token] = C.canonical(held), False
        with self.assertRaisesRegex(ValueError, "MEMBER_INVENTORY_CHANGED"):
            inert._read_stage(token)


class Controls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client_patch = patch.object(H, "CommonsClient", InertClient)
        self.client_patch.start()
        self.addCleanup(self.client_patch.stop)

    def session(self, specs, **caps):
        client = InertClient(specs)
        session = H.SemanticReader(client, client.origin, limits={**LIMITS, **caps})
        return client, session

    async def start(self, specs, **caps):
        client, session = self.session(specs, **caps)
        await session.stage(client.origin, client.entries(client.origin)[0])
        return client, session

    async def add_module(self, client, session, spec, *, variant=0):
        selected = demand("NeedModuleEvidence", spec)
        client.demands = [selected]
        preview = session.preview()
        self.assertNotIn("context", preview)
        resolved = await session.resolve(selected, max_bytes=65536)
        candidate = resolved["candidate"]
        await session.stage(candidate, client.entries(candidate)[variant])
        return candidate

    def limits_for(self, specs):
        return {module_id(spec): deepcopy(ADMISSION) for spec in specs}

    async def test_arbitrary_third_module_stages_before_any_admission(self):
        specs = [T.spec(name) for name in ("unfamiliarRoot", "secondDependency", "arbitraryThird")]
        client, session = await self.start(specs)
        await self.add_module(client, session, specs[1])
        await self.add_module(client, session, specs[2])
        self.assertFalse(any(event[0] in ("admit", "import") for event in client.events))
        self.assertEqual(session.report()["modules"], 3)
        client.demands = []
        preview = session.preview()
        self.assertEqual(preview["status"], "STRUCTURAL_CLOSURE_STAGED")
        self.assertIs(preview["mathematical_acceptance"], False)
        self.assertNotIn("context", preview)
        answer = session.finish(self.limits_for(specs))
        self.assertEqual(answer["status"], "READY")
        self.assertIs(answer["context"], client.context)
        last_stage = max(index for index, row in enumerate(client.events) if row[0] == "stage")
        first_admit = min(index for index, row in enumerate(client.events) if row[0] == "admit")
        self.assertLess(last_stage, first_admit)
        self.assertEqual([row[1] for row in client.events if row[0] == "admit"],
                         sorted(map(module_id, specs)))
        self.assertEqual(session.report()["state"], "READY")
        self.assertIs(session.report()["mathematical_acceptance"], False)

    async def test_internal_modules_need_no_standalone_offer_and_one_packet_admission(self):
        specs = [T.spec(name) for name in ("packetRoot", "internalBase", "internalDelta")]
        client, session = self.session(specs)
        root = module_id(specs[0])
        inventory = [client.member(module_id(spec), rank) for rank, spec in enumerate(specs)]
        client.packet_members[root] = inventory
        client.no_standalone_offer.update(map(module_id, specs[1:]))
        staged = await session.stage(client.origin, client.entries(client.origin)[0])
        self.assertEqual(staged["members"], inventory)
        self.assertNotIn("context", staged)
        self.assertEqual((session.report()["packets"], session.report()["modules"]), (1, 1))
        for spec, member in zip(specs[1:], inventory[1:]):
            selected = demand("NeedModuleEvidence", spec)
            client.demands = [selected]
            session.preview()
            exact = bytes(member["journal"])
            answer = session.select_member(root, exact)
            self.assertEqual(answer["status"], "SELECTED_MEMBER")
            self.assertEqual(session.select_member(root, exact)["status"], "NO_PROGRESS")
            candidate = (await session.resolve(selected, max_bytes=65536))["candidate"]
            self.assertEqual(client.entries(candidate), [])
        self.assertEqual((session.report()["packets"], session.report()["modules"]), (1, 3))
        self.assertEqual(sum(row[0] == "stage" for row in client.events), 1)
        self.assertFalse(any(row[0] in ("offers", "admit", "import") for row in client.events))
        client.demands = []
        self.assertNotIn("context", session.preview())
        resolution = {bytes(inventory[1]["journal"]): "existing"}
        answer = session.finish(self.limits_for([specs[0]]), resolutions={root: resolution})
        self.assertEqual(answer["status"], "READY")
        self.assertIs(answer["context"], client.context)
        self.assertEqual(sum(row[0] == "admit" for row in client.events), 1)
        sources, selected, openings, unused_bodies = client.import_arguments
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["resolutions"], resolution)
        self.assertEqual(set(selected), {bytes(row["journal"]) for row in inventory})
        self.assertEqual({row["module"] for row in openings}, set(map(module_id, specs)))

    async def test_internal_member_nonheld_undemanded_variant_and_cap_refuse(self):
        specs = [T.spec("variantPacket"), T.spec("internalVariant")]
        root, internal = map(module_id, specs)
        for defect in ("nonheld", "undemanded", "variant", "cap"):
            with self.subTest(defect=defect):
                client, session = self.session(specs, modules=1 if defect == "cap" else 8)
                base, changed = client.member(internal), client.member(internal, 1)
                client.packet_members[root] = [client.member(root), base, changed]
                await session.stage(client.origin, client.entries(client.origin)[0])
                if defect != "undemanded":
                    client.demands = [demand("NeedModuleEvidence", specs[1])]
                    session.preview()
                if defect == "variant":
                    session.select_member(root, bytes(base["journal"]))
                exact = (bytes(client.member(internal, 2)["journal"]) if defect == "nonheld"
                         else bytes(changed["journal"]) if defect == "variant"
                         else bytes(base["journal"]))
                with self.assertRaises(ValueError):
                    session.select_member(root, exact)
                self.assertEqual(session.report()["state"], "FAILED")
                self.assertFalse(any(row[0] in ("admit", "import") for row in client.events))

    async def test_actual_admission_inventory_mismatch_cannot_reach_import(self):
        spec = T.spec("changedActualInventory")
        client, session = await self.start([spec])
        session.preview()
        client.describe_members_override = []
        with self.assertRaisesRegex(ValueError, "ACTUAL_MEMBER_INVENTORY"):
            session.finish(self.limits_for([spec]))
        self.assertEqual(session.report()["state"], "FAILED")
        self.assertEqual(sum(row[0] == "admit" for row in client.events), 1)
        self.assertFalse(any(row[0] == "import" for row in client.events))

    async def test_packet_variant_choice_is_explicit_and_exact_duplicate_is_no_progress(self):
        spec = T.spec("explicitVariant")
        client, session = self.session([spec])
        selected = client.entries(client.origin)[1]
        await session.stage(client.origin, selected)
        before = len(client.events)
        repeated = await session.stage(client.origin, deepcopy(selected))
        self.assertEqual(repeated["status"], "NO_PROGRESS")
        self.assertEqual(len(client.events), before)
        self.assertFalse(any(row[0] == "offers" for row in client.events))
        self.assertEqual(next(iter(client.tokens.values()))["selection"]["packet_sha256"],
                         selected["packet_sha256"])
        with self.assertRaises(ValueError):
            await session.stage(client.origin, client.entries(client.origin)[0])
        self.assertEqual(session.report()["state"], "FAILED")
        self.assertEqual(sum(row[0] == "stage" for row in client.events), 1)

    async def test_same_address_names_groups_and_bodies_deduplicate(self):
        spec, body = E.definitions()
        # Names have distinct valid ordinary groups and share one addressed body.
        client, session = await self.start([spec])
        alpha, beta = [group["declarations"][0]["name"] for group in spec["groups"]]
        declaration = demand("NeedDeclaration", spec, beta)
        client.demands = [declaration]
        session.preview()
        await session.resolve(declaration, max_bytes=65536)
        repeated = await session.resolve(declaration, max_bytes=65536)
        self.assertEqual(repeated["status"], "NO_PROGRESS")
        self.assertEqual(session.report()["names"], 2)
        self.assertEqual(session.report()["groups"], 2)
        for name in (alpha, beta):
            selected = demand("NeedBody", spec, name, universes=0, body_hash=body["body_hash"])
            client.demands = [selected]
            session.preview()
            result = await session.fetch_body(selected, max_bytes=65536)
            if name == beta:
                self.assertEqual(result["status"], "NO_PROGRESS")
        self.assertEqual(session.report()["bodies"], 1)
        self.assertEqual(sum(row[0] == "resolve" for row in client.events), 1)
        self.assertEqual(sum(row[0] == "body" for row in client.events), 1)

    async def test_unsolicited_candidate_and_nonreturned_demand_refuse(self):
        specs = [T.spec("selectedRoot"), T.spec("notDemanded")]
        client, session = await self.start(specs)
        outsider = client.candidates[module_id(specs[1]),
                                     C.name_key(specs[1]["groups"][0]["declarations"][0]["name"])]
        with self.assertRaises(ValueError):
            await session.stage(outsider, client.entries(outsider)[0])
        self.assertEqual(sum(row[0] == "stage" for row in client.events), 1)
        client2, session2 = await self.start(specs)
        client2.demands = []
        session2.preview()
        with self.assertRaises(ValueError):
            await session2.resolve(demand("NeedModuleEvidence", specs[1]), max_bytes=65536)
        self.assertFalse(any(row[0] == "resolve" for row in client2.events))

    async def test_caps_and_no_progress_never_renew_steps(self):
        spec = T.spec("stepBound")
        client, session = self.session([spec], steps=3)
        entry = client.entries(client.origin)[0]
        await session.stage(client.origin, entry)
        for unused in range(2):
            self.assertEqual((await session.stage(client.origin, entry))["status"], "NO_PROGRESS")
        with self.assertRaises(ValueError):
            await session.stage(client.origin, entry)
        self.assertEqual(sum(row[0] == "stage" for row in client.events), 1)
        self.assertEqual(session.report()["state"], "FAILED")
        second = T.spec("beyondModuleCap")
        client2, session2 = await self.start([spec, second], modules=1)
        selected = demand("NeedModuleEvidence", second)
        client2.demands = [selected]
        session2.preview()
        candidate = (await session2.resolve(selected, max_bytes=65536))["candidate"]
        with self.assertRaises(ValueError):
            await session2.stage(candidate, client2.entries(candidate)[0])
        self.assertEqual(sum(row[0] == "stage" for row in client2.events), 1)
        client3, session3 = await self.start([spec, second], names=1)
        client3.demands = [selected]
        session3.preview()
        with self.assertRaises(ValueError):
            await session3.resolve(selected, max_bytes=65536)
        self.assertFalse(any(row[0] == "resolve" for row in client3.events))
        definition, unused = E.definitions()
        beta = definition["groups"][1]["declarations"][0]["name"]
        client4, session4 = await self.start([definition], groups=1)
        declaration = demand("NeedDeclaration", definition, beta)
        client4.demands = [declaration]
        session4.preview()
        with self.assertRaises(ValueError):
            await session4.resolve(declaration, max_bytes=65536)
        self.assertEqual(session4.report()["groups"], 1)
        with self.assertRaises(ValueError):
            self.session([spec], data_bytes=1)

    async def test_body_limit_and_changed_candidate_conflicts_refuse(self):
        spec, body = E.definitions()
        alpha = spec["groups"][0]["declarations"][0]["name"]
        beta = spec["groups"][1]["declarations"][0]["name"]
        second_body = ["sort", ["succ", ["zero"]]]
        beta_descriptor = spec["groups"][1]["declarations"][0]
        beta_descriptor["type"] = ["sort", ["succ", ["succ", ["zero"]]]]
        beta_descriptor["value_hash"] = C.body_id(second_body, 0)
        client, session = await self.start([spec], bodies=1)
        first = demand("NeedBody", spec, alpha, universes=0, body_hash=body["body_hash"])
        client.demands = [first]
        session.preview()
        await session.fetch_body(first, max_bytes=65536)
        second = demand("NeedBody", spec, beta, universes=0, body_hash=beta_descriptor["value_hash"])
        client.demands = [second]
        session.preview()
        await session.resolve(second, max_bytes=65536)
        with self.assertRaises(ValueError):
            await session.fetch_body(second, max_bytes=65536)
        self.assertEqual(sum(row[0] == "body" for row in client.events), 1)
        self.assertEqual(session.report()["bodies"], 1)
        client2, session2 = await self.start([T.spec("candidateConflict")])
        client2.descriptions[client2.origin]["provider"] = "changed-provider"
        with self.assertRaises(ValueError):
            await session2.stage(client2.origin, client2.entries(client2.origin)[0])
        self.assertEqual(sum(row[0] == "stage" for row in client2.events), 1)
        self.assertEqual(session2.report()["state"], "FAILED")

    async def test_original_client_deadline_and_grant_identity_are_not_replaced(self):
        spec = T.spec("originalLifetime")
        for change in ("deadline", "grant"):
            client, session = self.session([spec])
            if change == "deadline":
                client.expired = True
            else:
                client.grant = SimpleNamespace(_limits=deepcopy(client.grant._limits))
            with self.subTest(change=change), self.assertRaises(ValueError):
                await session.stage(client.origin, client.entries(client.origin)[0])
            self.assertEqual(session.report()["state"], "FAILED")
            self.assertFalse(client.events)

    async def test_preview_cannot_supply_authority_or_finish_missing_closure(self):
        specs = [T.spec("notReadyRoot"), T.spec("missingDependency")]
        client, session = await self.start(specs)
        client.demands = [demand("NeedModuleEvidence", specs[1])]
        preview = session.preview()
        self.assertNotIn("context", preview)
        with self.assertRaises(ValueError):
            session.finish(self.limits_for([specs[0]]))
        self.assertFalse(any(row[0] in ("admit", "import") for row in client.events))
        client2, session2 = await self.start([specs[0]])
        client2.preview_acceptance = True
        with self.assertRaises(ValueError):
            session2.preview()
        self.assertEqual(session2.report()["state"], "FAILED")
        client3, session3 = await self.start([specs[0]])
        client3.preview_extra_context = True
        preview3 = session3.preview()
        self.assertNotIn("context", preview3)
        self.assertFalse(any(row[0] in ("admit", "import") for row in client3.events))

    async def test_later_admission_failure_is_one_shot_and_never_partial_ready(self):
        specs = [T.spec("firstStaged"), T.spec("laterFailure")]
        client, session = await self.start(specs)
        await self.add_module(client, session, specs[1])
        client.demands = []
        session.preview()
        client.fail_admission = sorted(map(module_id, specs))[1]
        with self.assertRaisesRegex(ValueError, "INERT_LATER_ADMISSION_FAILURE"):
            session.finish(self.limits_for(specs))
        self.assertEqual(session.report()["state"], "FAILED")
        self.assertEqual(sum(row[0] == "admit" for row in client.events), 2)
        self.assertFalse(any(row[0] == "import" for row in client.events))
        before = len(client.events)
        with self.assertRaises(ValueError):
            session.finish(self.limits_for(specs))
        self.assertEqual(len(client.events), before)

    async def test_live_import_demands_never_return_preview_or_partial_context(self):
        spec = T.spec("liveImportStillRequired")
        client, session = await self.start([spec])
        session.preview()
        client.import_status = "NEED_AUTHORING_CONTEXT_DATA"
        answer = session.finish(self.limits_for([spec]))
        self.assertEqual(answer["status"], "NEED_SEMANTICS")
        self.assertIsNone(answer["context"])
        self.assertTrue(answer["demands"])
        self.assertEqual(session.report()["state"], "INCOMPLETE")
        before = len(client.events)
        with self.assertRaises(ValueError):
            session.finish(self.limits_for([spec]))
        self.assertEqual(len(client.events), before)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output:
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
                               for test_class in (StructuralControls, Controls))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "scope": "INERT_FACADE_COMPOSITION_AND_PURE_STAGED_MEMBER_DATA_BOUNDARY",
        "actual_admission_exercised": False, "actual_semantic_preview_exercised": False,
        "actual_structural_inventory_and_subset_exercised": True,
        "sources": {relative: hashlib.sha256((SOURCE/relative).read_bytes()).hexdigest()
            for relative in ("client/semantic_reader.py", "client/test_semantic_reader.py",
                             "client/test_workspace_mixed.py", "client/test_workspace_evidence.py",
                             "staging_members/workspace_staged.py")},
        "inert_calls": COUNTS, "native_calls": 0, "proof_calls": 0, "network_requests": 0}
    with (output/"controls.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
