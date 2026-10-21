"""Focused Terminal-I controls. Every issuer acceptance is explicitly INERT.

The real selected facade, packet stores, in-process provider dispatch, staged
reader and import session run without native verification, sockets or proofs.
The sole imported legacy test file supplies frozen factories; its suite is not
run. No result here establishes cryptographic or mathematical acceptance.
"""
import asyncio
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = PROJECT/"software/v5"
MAP_PATH = PROJECT/"experiments/v5-local-checks/distribution-origin-01-input.json"
MAP_SHA = "2ea8322879b2e45afb2a2f5e8d99500bfcfdbe0982cdf14687b1e8bdd0950556"
REPLACEMENTS = {
    "v5/evidence_network/packet.py": "cf8aaa6190d46c4b41792cb54da7da5983d19450cafb65920af2a188afbbcefd",
    "v5/evidence_network/custody.py": "c039af086cf73d57191187e9d5b02292c5c9b8a3fb455d67dc719ad8f7d183a0",
    "v5/evidence_network/transport.py": "7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827",
    "v5/client/workspace_evidence.py": "8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68",
    "v5/client/workspace_staged.py": "ae3dc1a743a0cf4bd2da7f388ed46d6f75f73330802b9263a03a54a230fafd2b",
}
FIXTURE = "v5/client/test_workspace_mixed.py"
FIXTURE_SHA = "478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e"
FOUNDATION_PATH = PROJECT/"experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json"
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
MIB = 1024**2
OUTPUT = CODE = FOUNDATION = C = B = T = EP = EC = ET = WE = WV = SR = DT = TC = MS = None
SOURCE_COPIES, OBSERVED, FORBIDDEN, LOOP_ERRORS = {}, {}, [], []
ADMISSION = dict(native_cpu_seconds=1, receipt_cpu_seconds=1, wall_seconds=30, memory_mib=64)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def copy_bound(path, expected, target, size=None):
    raw = path.read_bytes()
    if not 0 < len(raw) <= 2*MIB or sha(raw) != expected or size is not None and len(raw) != size:
        raise ValueError("SELECTED_INPUT_CHANGED:"+str(path))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        if stream.write(raw) != len(raw):
            raise ValueError("INPUT_SHORT_WRITE")
    if target.read_bytes() != raw:
        raise ValueError("INPUT_COPY_CHANGED")
    return raw


def stage_sources(output):
    global FOUNDATION
    raw = MAP_PATH.read_bytes()
    if sha(raw) != MAP_SHA:
        raise ValueError("BASIS_MAP_CHANGED")
    basis = json.loads(raw)["sdk_sources"]
    if len(basis) != 114 or not set(REPLACEMENTS) <= set(basis) or FIXTURE in basis:
        raise ValueError("BASIS_MAP_KEYS")
    code = output/"selected-code"
    code.mkdir()
    for logical, row in sorted(basis.items()):
        if logical in REPLACEMENTS:
            path, expected, size = SOURCE/"terminal_i"/logical[3:], REPLACEMENTS[logical], None
        else:
            path, expected, size = Path(row["path"]), row["sha256"], row["bytes"]
            if not path.is_relative_to(SOURCE):
                raise ValueError("BASIS_SOURCE_OUTSIDE_CANONICAL_TREE")
        raw = copy_bound(path, expected, code/logical, size)
        SOURCE_COPIES[logical] = dict(source=str(path), bytes=len(raw), sha256=sha(raw))
    raw = copy_bound(SOURCE/FIXTURE[3:], FIXTURE_SHA, code/FIXTURE)
    SOURCE_COPIES[FIXTURE] = dict(source=str(SOURCE/FIXTURE[3:]), bytes=len(raw), sha256=sha(raw))
    FOUNDATION = copy_bound(FOUNDATION_PATH, FOUNDATION_SHA, output/"foundation.json")
    for name in ("admission", "modules", "client", "mixed_claims", "evidence_network"):
        if name in sys.modules:
            raise ValueError("EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return code


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_NATIVE_OR_NETWORK_CALL")
    raise AssertionError("FORBIDDEN_NATIVE_OR_NETWORK_CALL")


class InertEndpoint:
    """No socket/contact authority: only an explicit in-process dispatch gate."""
    label = "inert-selected-provider"

    def __init__(self):
        self.expired = False

    def validate(self):
        if self.expired:
            raise ValueError("INERT_PROVIDER_CONTACT_EXPIRED")


class InertSearch:
    def report(self):
        return {"inert": True, "actual_search_performed": False}


class Controls(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = OUTPUT/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2))
        self.root.mkdir()
        self.workspaces, self.clients, self.owners, self.readers = [], [], [], []
        self.patches = ExitStack()
        # IsolatedAsyncioTestCase creates its event loop before setUp. Trapping
        # sockets earlier would incorrectly block the loop's own socketpair.
        self.patches.enter_context(patch.object(socket.socket, "__init__", forbidden))
        for name in ("create_subprocess_exec", "create_subprocess_shell", "open_connection", "start_server"):
            self.patches.enter_context(patch.object(asyncio, name, forbidden))

    async def asyncSetUp(self):
        self.loop = asyncio.get_running_loop()
        self.previous_handler = self.loop.get_exception_handler()
        self.loop.set_exception_handler(lambda unused, context: LOOP_ERRORS.append(
            {"test": self._testMethodName, "message": str(context.get("message", "")),
             "exception": repr(context.get("exception"))}))

    async def asyncTearDown(self):
        try:
            for reader in reversed(self.readers):
                reader.close()
            for client in reversed(self.clients):
                if not client._closed:
                    await client.close()
                self.assertFalse(client._cleanup_uncertain)
                self.assertFalse(client._warrants)
            for owners in reversed(self.owners):
                owners.close()
            for workspace in reversed(self.workspaces):
                if not workspace._closed:
                    workspace.close()
        finally:
            self.loop.set_exception_handler(self.previous_handler)

    def tearDown(self):
        self.patches.close()

    def note(self, **values):
        OBSERVED[self._testMethodName] = values

    def workspace(self, name, *, enabled=True):
        cfg = T.configuration()
        cfg.update(schema=WE.SCHEMA, wire_profile=EC.public_profile(T.IMAGE, terminal_i=enabled),
                   terminal_receipt_bytes=65536)
        workspace = WV.Workspace.open(self.root/name, cfg, create=True)
        self.workspaces.append(workspace)
        return workspace

    def operation(self, name, *, enabled=True, legacy=True):
        workspace = self.workspace(name, enabled=enabled)
        grant = workspace.reserve(T.grant_limits())
        owners = T.SyntheticOwners(grant, workspace._envelope, legacy=legacy)
        self.owners.append(owners)
        pins = {CODE/logical: {"bytes": row["bytes"], "sha256": row["sha256"]}
                for logical, row in SOURCE_COPIES.items() if logical.startswith("v5/") and logical.endswith(".py")}
        for owner in (owners.legacy, owners.aggregate, owners.delta):
            if owner is not None:
                owner._pins.update(deepcopy(pins))
        client = workspace.operation(grant, aggregate_owner=owners.aggregate,
            receipt_owner=owners.legacy, delta_owner=owners.delta,
            foundation_bytes=FOUNDATION, foundation_sha256=FOUNDATION_SHA)
        self.clients.append(client)
        return workspace, client, owners

    def packet(self, spec=None, *, rank=0, receipt=None):
        spec = T.spec("terminalI") if spec is None else spec
        exact = T.expected_journal(C.summarize(spec), rank, B.RELATION_IMAGE)
        raw = EP.pack_terminal_i(exact, T.RECEIPT if receipt is None else receipt,
            aggregate_image=T.IMAGE, envelope=T.Envelope(), terminal_i=True)
        return spec, exact, raw

    def stored(self, workspace, raw):
        unused, summary, unused_exact, unused_census = EP.inspect_evidence(
            raw, workspace._envelope, aggregate_image=T.IMAGE, terminal_i=True)
        module = C.summary_id(summary)
        workspace.packets.put(module, raw)
        return module, sha(raw), len(raw)

    def assert_failed(self, client, owners, *, i_calls):
        self.assertEqual(client._state, "FAILED")
        self.assertFalse(client._warrants)
        self.assertFalse(client._receipt_cache)
        self.assertFalse(client._packet_cache)
        self.assertFalse(client._staged)
        self.assertTrue(client._budget.closed)
        self.assertEqual(owners.receives, {"I": i_calls, "A": 0, "mixed": 0})
        for owner in (owners.legacy, owners.aggregate, owners.delta):
            if owner is not None:
                self.assertTrue(owner._closed)
                self.assertFalse(owner._handles)
        self.assertEqual(client._budget.used["verify_attempts"], i_calls)
        self.assertEqual(client._budget.used["worker_cpu_seconds"], i_calls)

    def publish(self, source, publisher, spec, raw, *, bodies=()):
        module = C.module_id(spec)
        opening = C.group_opening(spec, 0)
        name = spec["groups"][0]["declarations"][0]["name"]
        held = publisher.retain_semantics([{"module": module, "opening": opening}], list(bodies))
        self.assertFalse(held["mathematical_acceptance"])
        result = publisher.publish(raw, [name], retention_policy={"mode": "quota-bounded-local-custody"})
        self.assertEqual(result["phase"], "LOCALLY_PUBLISHED")
        self.assertFalse(result["mathematical_acceptance"])
        record = source.adapter.describe(source.adapter.encode_opening(module, name, opening))["record"]
        return module, opening, record, result

    async def connect(self, source, target, client, record):
        provider = ET.CompositeProvider(index=source.index, custody=source.modules, packets=source.packets)
        endpoint, calls = InertEndpoint(), []
        client._acquisition = ET.EvidenceAcquisition(target.adapter, {"p": endpoint},
            target.config["wire_profile"], client._budget, target.modules, target.packets)
        client._search = InertSearch()

        async def exchange(selected, route, request, maximum, timeout):
            self.assertIs(selected, endpoint)
            selected.validate()
            calls.append({"route": route, "request": deepcopy(request)})
            value = provider.dispatch(route, request)
            raw = value if type(value) is bytes else C.canonical(value)
            self.assertLessEqual(len(raw), maximum)
            return dict(status=200, raw=raw, request_bytes=len(C.canonical(request)),
                        reply_bytes=len(raw), header_bytes=0, elapsed_ms=0)

        self.patches.enter_context(patch.object(DT, "exchange", exchange))
        self.patches.enter_context(patch.object(TC, "exchange", exchange))
        candidate = await client.resolve("p", record)
        offer = await client.packet_offers(candidate)
        self.assertEqual(len(offer["packets"]), 1)
        self.assertFalse(offer["mathematical_acceptance"])
        return candidate, offer["packets"][0], endpoint, calls

    async def test_closed_packet_forms_and_profile_gates(self):
        spec, exact, raw = self.packet()
        receipt, claimed, facts = EP.parse_terminal_i(raw, T.Envelope(), aggregate_image=T.IMAGE, terminal_i=True)
        self.assertEqual((receipt, claimed, facts["module"]), (T.RECEIPT, exact, C.module_id(spec)))
        self.assertEqual(EP.inspect_evidence(raw, T.Envelope(), aggregate_image=T.IMAGE, terminal_i=True)[0], "terminal-i")
        refusals = 0
        for capability in (False, None, 1):
            with self.assertRaises(ValueError):
                EP.parse_terminal_i(raw, T.Envelope(), aggregate_image=T.IMAGE, terminal_i=capability)
            refusals += 1
        parsed = C.parse_json(raw)
        malformed = [raw+b"\n"]
        for key, value in (("receipt_hex", ""), ("receipt_hex", "0"), ("receipt_hex", "AB"),
                           ("journal", list(exact[:-1])), ("journal", [True]+list(exact[1:]))):
            changed = deepcopy(parsed); changed[key] = value; malformed.append(C.canonical(changed))
        changed = deepcopy(parsed); changed["header"] = []; malformed.append(C.canonical(changed))
        for offset in (12, 44, 76):
            changed = deepcopy(parsed); changed["journal"][offset] ^= 1
            malformed.append(C.canonical(changed))
        for value in malformed:
            with self.assertRaises(ValueError):
                EP.parse_terminal_i(value, T.Envelope(), aggregate_image=T.IMAGE, terminal_i=True)
            refusals += 1
        with self.assertRaises(ValueError):
            EP.parse_terminal_i(raw, T.Envelope(), aggregate_image=T.IMAGE,
                                terminal_receipt_bytes=len(T.RECEIPT)-1, terminal_i=True)
        unused, unused_exact, too_high = self.packet(spec, rank=2)
        with self.assertRaisesRegex(ValueError, "TERMINAL_I_RANK_BOUND"):
            EP.parse_terminal_i(too_high, replace(T.Envelope(), rank=1), aggregate_image=T.IMAGE, terminal_i=True)
        with self.assertRaises(ValueError):
            EP.parse_terminal(raw, T.Envelope(), aggregate_image=T.IMAGE)
        members, header = T.members_and_header()
        old = EP.pack_terminal(header, members[0], 0, B.opening(members, 0), T.RECEIPT,
                               aggregate_image=T.IMAGE, envelope=T.Envelope())
        self.assertEqual(EP.inspect_evidence(old, T.Envelope(), aggregate_image=T.IMAGE)[0], "terminal")
        with self.assertRaises(ValueError):
            EP.parse_terminal_i(old, T.Envelope(), aggregate_image=T.IMAGE, terminal_i=True)
        mixed, unused = T.mixed_packet()
        self.assertEqual(EP.inspect_evidence(mixed, T.Envelope(), aggregate_image=T.IMAGE)[0], "mixed")
        empty = C.parse_json(mixed); empty["deltas"] = []
        with self.assertRaises(ValueError):
            EP.inspect_evidence(C.canonical(empty), T.Envelope(), aggregate_image=T.IMAGE, terminal_i=True)
        self.note(malformed_or_disabled_refusals=refusals+5, legacy_A_and_mixed_unchanged=True,
                  rank_bounded=True, structural_only=True)

    async def test_exact_V1_V2_custody_offers_and_reopen(self):
        v1, v2 = self.workspace("v1", enabled=False), self.workspace("v2")
        spec, exact, raw = self.packet()
        with self.assertRaisesRegex(ValueError, "TERMINAL_I_NOT_ENABLED"):
            v1.packets.put(C.module_id(spec), raw)
        self.stored(v2, raw)
        for workspace in (v1, v2):
            profile = workspace.config["wire_profile"]
            request = dict(module_id=C.module_id(spec), wire_profile_id=EC.profile_id(profile), max_offers=4, max_bytes=4096)
            offer = workspace.packets.offer(request)
            self.assertEqual(EC.verify_offer(offer, request, profile=profile), offer)
            self.assertFalse(offer["mathematical_acceptance"])
            changed = deepcopy(offer)
            changed["proof_form"] = EC.PROOF_FORM_V2 if workspace is v1 else EC.PROOF_FORM
            with self.assertRaisesRegex(ValueError, "EVIDENCE_OFFER_BINDING"):
                EC.verify_offer(changed, request, profile=profile)
            other = v2.config["wire_profile"] if workspace is v1 else v1.config["wire_profile"]
            with self.assertRaisesRegex(ValueError, "EVIDENCE_OFFER_PROFILE"):
                EC.verify_offer(offer, request, profile=other)
            malformed = deepcopy(profile); malformed["unknown"] = True
            with self.assertRaises(ValueError):
                EC.profile_id(malformed)
        self.assertNotEqual(v1.packets.profile_id, v2.packets.profile_id)
        cfg, path = deepcopy(v2.config), v2.root
        v2.close()
        reopened = WV.Workspace.open(path, cfg)
        self.workspaces.append(reopened)
        self.assertEqual(reopened.packets.get(sha(raw), len(raw)), raw)
        reopened.close()
        wrong = deepcopy(cfg); wrong["wire_profile"] = EC.public_profile(T.IMAGE)
        with self.assertRaisesRegex(ValueError, "CLIENT_WORKSPACE_CONFIG"):
            WV.Workspace.open(path, wrong)
        self.note(V1_refuses_I=True, exact_profile_offers=True, no_implicit_workspace_migration=True,
                  persisted_exact_packet=True, mathematical_acceptance=False)

    async def test_live_I_dispatch_cache_export_and_close(self):
        workspace, client, owners = self.operation("live")
        spec, exact, raw = self.packet()
        args = self.stored(workspace, raw)
        token = client.admit_local(*args, **ADMISSION)
        self.assertEqual(client.describe(token)["kind"], "I")
        self.assertEqual(client.describe(token)["live"]["journal"], exact)
        self.assertEqual(client.export_evidence(token), raw)
        self.assertIs(client.admit_local(*args, **ADMISSION), token)
        self.assertEqual(owners.receives, {"I": 1, "A": 0, "mixed": 0})
        self.assertEqual(client._budget.used["verify_attempts"], 1)
        self.assertEqual(client._budget.used["verification_input_bytes"], len(T.RECEIPT))
        self.assertEqual(client._budget.used["worker_cpu_seconds"], 1)
        self.assertEqual(client._counts["same_live_hits"], 1)
        await client.close()
        self.assertFalse(client._warrants)
        self.assertEqual(workspace.packets.get(sha(raw), len(raw)), raw)
        with self.assertRaisesRegex(ValueError, "CLIENT_CLOSED_FAILED_OR_EXPIRED"):
            client.describe(token)
        self.note(inert_I_calls=1, inert_A_calls=0, inert_mixed_calls=0, one_shared_reservation=True,
                  byte_exact_reexport=True, close_revokes_live_not_data=True)

    async def test_rank_swapped_packet_fresh_and_cache_hit_refuse(self):
        for warm in (False, True):
            with self.subTest(warm=warm):
                workspace, client, owners = self.operation("warm" if warm else "fresh")
                spec, zero, raw_zero = self.packet()
                unused, one, raw_one = self.packet(spec, rank=1)
                self.assertEqual(B.member_journal(zero)["summary"], B.member_journal(one)["summary"])
                self.assertNotEqual(zero, one)
                if warm:
                    token = client.admit_local(*self.stored(workspace, raw_zero), **ADMISSION)
                    self.assertIn(token, client._warrants)
                # Deliberately omit expected_exact_journal. Inert I issuer
                # returns exact rank 0 even for the rank-1 outer data packet.
                with self.assertRaisesRegex(ValueError, "CLIENT_EVIDENCE_LIVE_TARGET"):
                    client.admit_local(*self.stored(workspace, raw_one), **ADMISSION)
                self.assert_failed(client, owners, i_calls=1)
                self.assertEqual(client._counts["same_live_hits"], int(warm))
        self.note(same_ModuleID_different_rank=True, caller_expected_J_omitted=True,
                  fresh_and_cached_unconditional_exact_J_refusal=True,
                  inert_I_calls_each=1, revoked_on_failure=True, charged_on_failure=True)

    async def test_missing_I_and_V1_export_refuse_without_fallback(self):
        workspace, client, owners = self.operation("noI", legacy=False)
        spec, exact, raw = self.packet()
        with self.assertRaisesRegex(ValueError, "CLIENT_I_OWNER_NOT_SELECTED"):
            client.admit_local(*self.stored(workspace, raw), **ADMISSION)
        self.assert_failed(client, owners, i_calls=0)
        unused, old, old_owners = self.operation("old", enabled=False)
        token = old.admit_receipt(T.RECEIPT, C.summarize(spec), cpu_seconds=1, wall_seconds=30, memory_mib=64)
        with self.assertRaisesRegex(ValueError, "TERMINAL_I_NOT_ENABLED"):
            old.export_evidence(token)
        self.assert_failed(old, old_owners, i_calls=1)
        self.note(missing_I_refuses_before_reservation=True, no_A_or_native_fallback=True,
                  existing_V1_I_local_admission_not_new_wire_capability=True)

    async def test_A_remains_A_in_opted_in_facade(self):
        workspace, client, owners = self.operation("A")
        members, header = T.members_and_header()
        raw = EP.pack_terminal(header, members[0], 0, B.opening(members, 0), T.RECEIPT,
                               aggregate_image=T.IMAGE, envelope=workspace._envelope)
        token = client.admit_local(*self.stored(workspace, raw), **ADMISSION)
        self.assertEqual(client.describe(token)["kind"], "A-member")
        self.assertEqual(client.export_evidence(token), raw)
        self.assertEqual(owners.receives, {"I": 0, "A": 1, "mixed": 0})
        self.note(inert_A_calls=1, inert_I_calls=0, inert_mixed_calls=0, exact_A_schema_reexport=True)

    async def test_direct_acquisition_opens_with_I_and_reuses_live_receipt(self):
        source, publisher, source_owners = self.operation("s")
        target, client, owners = self.operation("t")
        spec, exact, raw = self.packet()
        module, opening, record, unused = self.publish(source, publisher, spec, raw)
        candidate, entry, endpoint, calls = await self.connect(source, target, client, record)
        original_budget = client._budget
        token = await client.acquire(candidate, entry, **ADMISSION)
        before = len(calls)
        self.assertIs(await client.acquire(candidate, entry, **ADMISSION), token)
        self.assertEqual(len(calls), before)
        self.assertEqual([row["route"] for row in calls].count(ET.PACKET_ROUTE), 1)
        self.assertEqual(client.describe(token)["live"]["journal"], exact)
        self.assertEqual(client.export_evidence(token), raw)
        self.assertIs(client._acquisition.budget, original_budget)
        self.assertEqual(original_budget.used["verify_attempts"], 1)
        self.assertEqual(owners.receives, {"I": 1, "A": 0, "mixed": 0})
        self.assertEqual(source_owners.receives, {"I": 0, "A": 0, "mixed": 0})
        self.note(in_process_routes=[row["route"] for row in calls], actual_search=False,
                  I_group_open_path=True, warm_no_transfer_or_admission=True, original_budget=True)

    async def test_semantic_reader_stages_body_then_imports_offline(self):
        source, publisher, source_owners = self.operation("s")
        target, client, owners = self.operation("t")
        spec = T.spec("terminalDefinition")
        body = ["sort", ["zero"]]
        declaration = spec["groups"][0]["declarations"][0]
        declaration.update(kind="definition", type=["sort", ["succ", ["zero"]]],
            value_hash=C.body_id(body, 0), meta={"hint": "abbrev", "safety": "safe"})
        unused, exact, raw = self.packet(spec)
        module = C.module_id(spec)
        response = dict(schema=MS.BODY_SCHEMA, module_id=module, relative_name=declaration["name"],
                        universes=0, body_hash=declaration["value_hash"], expression=body)
        unused, opening, record, unused_result = self.publish(source, publisher, spec, raw, bodies=[response])
        candidate, entry, endpoint, calls = await self.connect(source, target, client, record)
        reader = SR.SemanticReader(client, candidate, limits=dict(modules=8, names=32, groups=16,
            bodies=8, steps=128, data_bytes=MIB), definition_mode="eager")
        self.readers.append(reader)
        staged = await reader.stage(candidate, entry)
        self.assertEqual(staged["status"], "STAGED")
        self.assertEqual(len(staged["members"]), 1)
        self.assertEqual(staged["members"][0]["journal"], list(exact))
        self.assertFalse(client._warrants)
        self.assertEqual(client._budget.used["verify_attempts"], 0)
        needed = reader.preview()
        self.assertEqual(needed["status"], SR.NEED)
        self.assertEqual(len(needed["demands"]), 1)
        self.assertEqual(needed["demands"][0]["kind"], "NeedBody")
        self.assertFalse(needed["mathematical_acceptance"])
        await reader.fetch_body(needed["demands"][0], max_bytes=65536)
        preview = reader.preview()
        self.assertEqual(preview["status"], SR.READY)
        self.assertFalse(preview["mathematical_acceptance"])
        self.assertEqual(owners.receives, {"I": 0, "A": 0, "mixed": 0})
        endpoint.expired = True
        before = len(calls)
        result = reader.finish({module: dict(ADMISSION)})
        self.assertEqual(result["status"], "READY")
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(len(calls), before)
        self.assertEqual(owners.receives, {"I": 1, "A": 0, "mixed": 0})
        self.assertEqual(source_owners.receives, {"I": 0, "A": 0, "mixed": 0})
        self.assertIsNotNone(client._session)
        self.assertTrue(client._session._sealed)
        self.assertEqual(client._session._owners, (owners.legacy, owners.aggregate, owners.delta))
        token = next(iter(client._warrants))
        self.assertEqual(client.export_evidence(token), raw)
        await client.close()
        self.assertIsNone(client._context)
        self.assertTrue(client._session._closed)
        self.assertEqual(target.packets.get(sha(raw), len(raw)), raw)
        self.note(singleton_staging_no_authority=True, eager_NeedBody_then_structural_ready=True,
                  actual_unchanged_import_session=True, finish_after_contact_expiry_no_dial=True,
                  inert_I_calls=1, inert_A_calls=0, inert_mixed_calls=0,
                  source_publication_no_admission=True, no_genuine_math_or_crypto_claim=True)

    async def test_staged_packet_corruption_refuses_before_I(self):
        source, publisher, unused_owners = self.operation("s")
        target, client, owners = self.operation("t")
        spec, exact, raw = self.packet()
        unused, unused_opening, record, unused_result = self.publish(source, publisher, spec, raw)
        candidate, entry, endpoint, calls = await self.connect(source, target, client, record)
        token = await client.stage_packet(candidate, entry)
        self.assertFalse(client.describe_staged(token)["mathematical_acceptance"])
        # Corrupt only the fresh test database, not any retained product/evidence.
        target.packets.db.execute("UPDATE packets SET blob=? WHERE digest=?", (raw[:-1]+b" ", sha(raw)))
        endpoint.expired = True
        before = len(calls)
        with self.assertRaises(ValueError):
            client.admit_staged(token, **ADMISSION)
        self.assertEqual(len(calls), before)
        self.assert_failed(client, owners, i_calls=0)
        self.note(actual_staged_readback_refusal=True, no_issuer_or_network_on_corruption=True,
                  staged_and_warrant_maps_revoked=True)

    async def test_profile_symbol_owner_and_foreign_token_refuse(self):
        cases = ("profile", "symbol", "owner", "foreign")
        for mode in cases:
            with self.subTest(mode=mode):
                workspace, client, owners = self.operation(mode)
                unused, unused_exact, raw = self.packet()
                token = client.admit_local(*self.stored(workspace, raw), **ADMISSION)
                with ExitStack() as mutation:
                    if mode == "profile":
                        changed = EC.public_profile(T.IMAGE)
                        workspace.config["wire_profile"] = changed
                        # Arrange mutually consistent mutable fields so this
                        # specifically challenges the facade's original ID,
                        # not the earlier whole-workspace config guard.
                        workspace._config_raw = C.canonical(workspace.config)
                        workspace.packets.profile = deepcopy(changed)
                        workspace.packets.profile_id = EC.profile_id(changed)
                        expected = "CLIENT_EVIDENCE_STORE_PROFILE_CHANGED"
                    elif mode == "symbol":
                        mutation.enter_context(patch.object(EP, "parse_terminal_i", lambda *a, **k: None))
                        expected = "CLIENT_EVIDENCE_IMPORTED_SYMBOL_CHANGED"
                    elif mode == "owner":
                        owners.legacy.close()
                        expected = "TEST_SYNTHETIC_ISSUER_CLOSED_OR_EXPIRED"
                    else:
                        token = WE.LiveWarrant()  # Empty token is not an issued warrant.
                        expected = "CLIENT_FOREIGN_WARRANT"
                    with self.assertRaisesRegex(ValueError, expected):
                        client.export_evidence(token)
                self.assert_failed(client, owners, i_calls=1)
        self.note(closed_owner_profile_symbol_foreign_token_refusals=list(cases),
                  no_patched_warrant_or_facade_safety=True, failures_revoke_owners=True)


SELECTED = (
    "test_closed_packet_forms_and_profile_gates",
    "test_exact_V1_V2_custody_offers_and_reopen",
    "test_live_I_dispatch_cache_export_and_close",
    "test_rank_swapped_packet_fresh_and_cache_hit_refuse",
    "test_missing_I_and_V1_export_refuse_without_fallback",
    "test_A_remains_A_in_opted_in_facade",
    "test_direct_acquisition_opens_with_I_and_reuses_live_receipt",
    "test_semantic_reader_stages_body_then_imports_offline",
    "test_staged_packet_corruption_refuses_before_I",
    "test_profile_symbol_owner_and_foreign_token_refuse",
)


def main():
    global OUTPUT, CODE, C, B, T, EP, EC, ET, WE, WV, SR, DT, TC, MS
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    OUTPUT = Path(sys.argv[2])
    if not OUTPUT.is_absolute() or not OUTPUT.is_dir() or OUTPUT.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    CODE = stage_sources(OUTPUT)
    with ExitStack() as guard:
        guard.enter_context(patch.object(subprocess, "Popen", forbidden))
        guard.enter_context(patch.object(os, "system", forbidden))
        loaded = {}
        for name in ("modules.codec", "aggregate_claims.bindings", "client.test_workspace_mixed",
                     "evidence_network.packet", "evidence_network.custody", "evidence_network.transport",
                     "client.workspace_evidence", "client.workspace_validated", "client.semantic_reader",
                     "delta.transport", "transport.clients", "custody.module_store"):
            module = importlib.import_module(name)
            if Path(module.__file__).resolve() != CODE/"v5"/(name.replace(".", "/")+".py"):
                raise ValueError("SELECTED_MODULE_ORIGIN:"+name)
            loaded[name] = module
        C, B, T, EP, EC, ET, WE, WV, SR, DT, TC, MS = loaded.values()
        suite = unittest.TestSuite(Controls(name) for name in SELECTED)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = (result.wasSuccessful() and result.testsRun == len(SELECTED)
              and not result.skipped and not FORBIDDEN and not LOOP_ERRORS)
    report = dict(schema="DMKN_V5_TERMINAL_I_CONTROLS_V1", status="PASS" if passed else "FAIL",
        scope="INERT_ISSUERS_REAL_FACADE_CUSTODY_STAGING_IMPORT_NO_CRYPTOGRAPHIC_ACCEPTANCE",
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), selected=list(SELECTED), observations=OBSERVED,
        sources=SOURCE_COPIES, basis_map=dict(path=str(MAP_PATH), sha256=MAP_SHA),
        foundation=dict(path=str(FOUNDATION_PATH), bytes=len(FOUNDATION), sha256=FOUNDATION_SHA),
        forbidden_calls=FORBIDDEN, event_loop_errors=LOOP_ERRORS,
        native_calls=0, network_calls=0, proof_calls=0, actual_unknown_ID_discovery=False,
        mathematical_acceptance=False, cryptographic_acceptance=False)
    with (OUTPUT/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
