"""Changed-boundary A-client controls; all issuer acceptance is SYNTHETIC.

Real workspace/grants/client/budget and pure member bindings are exercised.
Exact issuer classes are allocated with __new__: their native receive/install
methods are replaced ONLY in these fixtures. No constructor, native verifier,
Lean, Node, proof, network service or old test module is invoked. A synthetic
handle here is not evidence for genuine mathematical acceptance.
"""
import asyncio
from copy import deepcopy
from dataclasses import asdict
import hashlib
from pathlib import Path
import time
import unittest
from unittest.mock import patch

from admission.verifier import ReceiptVerifier, VerifiedModule
from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier, VerifiedAggregate
from client import workspace_atomic as OLD
from client import workspace_mixed as W
from delta_claims.claims import expected_journal
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.packet import Envelope, parse_packet
from mixed_claims.receiver import MixedDeltaVerifier, VerifiedMixedDelta
from mixed_network.custody import PacketStore, public_profile
from modules import codec as C

MIB = 1024**2
EVIDENCE = None
IMAGE = "7a"*32  # Inert test adoption, NOT a built or proven A image.
RECEIPT = b"SYNTHETIC-NOT-A-CRYPTOGRAPHIC-RECEIPT"
FOUNDATION_BYTES = b"SYNTHETIC-FOUNDATION-NOT-IMPORTED"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def configuration():
    return {"schema": W.SCHEMA, "wire_profile": public_profile(IMAGE),
        "module_limits": dict(modules=8, groups=16, declarations=32, bodies=8,
                              logical_bytes=MIB, db_pages=256),
        "packet_limits": dict(packets=8, offers=16, offers_per_module=4, packet_bytes=65536,
                              logical_bytes=MIB, db_pages=256),
        "index_limits": dict(max_objects=8, max_postings=1024, max_features=128,
                             max_snapshots=16, max_logical_bytes=4*MIB, max_db_pages=2048),
        "packet_envelope": asdict(Envelope()), "max_operations": 8,
        "max_report_bytes": MIB, "ledger_pages": 256}


def grant_limits(cpu=120):
    return dict(wall_seconds=60, controller_cpu_seconds=30, calls=128,
        input_bytes=4*MIB, worker_cpu_seconds=cpu+10,
        output_bytes=128*MIB, output_entries=512,
        acquisition=dict(requests=8, reply_bytes=MIB, verify_attempts=8,
                         verification_input_bytes=65536, worker_cpu_seconds=cpu),
        imports=dict(max_sources=8, max_members=16, max_receipts=8, max_calls=4096,
                     submitted_bytes=MIB, data_bytes=MIB))


def spec(label):
    return {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "groups": [{"kind": "ordinary", "declarations": [{"kind": "theorem",
            "name": [["s", label]], "universes": 0, "type": ["sort", ["zero"]],
            "value_hash": None, "meta": {}}]}]}


def members_and_header(height=1):
    members = sorted(expected_journal(C.summarize(spec(label)), 0, B.RELATION_IMAGE)
                     for label in ("syntheticLeft", "syntheticRight"))
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")+bytes.fromhex(IMAGE)
        +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
        +B.commitment(members)+len(members).to_bytes(4, "little")
        +(0).to_bytes(8, "little")+height.to_bytes(8, "little"))
    B.decode_header(header, adopted_image=IMAGE)
    return members, header


def mixed_packet():
    """Structurally genuine A-frontier packet; receipt/proof bytes are fabricated."""
    members, header = members_and_header()
    target = spec("syntheticChild")
    image = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4], "little")
             for i in range(0, 32, 4)]
    value = {"schema": "DMKN_MIXED_DELTA_PACKET_V1",
        "claims": [{"tag": 1, "statement": list(header), "receipt_hex": RECEIPT.hex()}],
        "frontiers": [{"claim_index": 0, "journal": list(members[0]), "member_index": 0,
                       "siblings": [list(part) for part in B.opening(members, 0)]}],
        "deltas": [{"schema": "DMKN_CERTIFIED_MODULES_V2", "image": image, "rank": 1,
            "local_spec": target, "rows": [], "bodies": [],
            "parents": [{"journal": list(members[0]), "openings": []}]}]}
    return C.canonical(value), C.summarize(target)


class SyntheticOwners:
    """Test-only exact instances, NOT constructed/installed mathematical owners.

    A select_member/describe/member-cache/report methods are real pure methods;
    the cryptographic receive and installation/lifetime origin checks are
    explicitly fabricated. Client-side owner/profile/budget checks remain real.
    """
    def __init__(self, grant, envelope, *, legacy=False, preparation=False):
        self.grant = grant
        self.receives = {"I": 0, "A": 0, "mixed": 0}
        self.closes = {"I": 0, "A": 0, "mixed": 0, "preparation": 0}
        root = Path(__file__).resolve().parents[1]
        required = ("client/__init__.py", "client/workspace_atomic.py", "client/workspace_mixed.py",
                    "mixed_network/__init__.py", "mixed_network/custody.py", "mixed_network/transport.py")
        self.pins = {}
        for relative in required:
            path = root/relative
            raw = path.read_bytes()
            self.pins[path] = {"bytes": len(raw), "sha256": sha(raw)}
        self.legacy = self._make(ReceiptVerifier, "I", B.RELATION_IMAGE) if legacy else None
        self.aggregate = self._make(AggregateReceiptVerifier, "A", IMAGE)
        a = self.aggregate
        a._member_used, a._output_reserved = [0, 0], [0, 0]
        a._members, a._member_cache = {}, {}
        a._member_caps = (4096, 16, MIB)
        a._controller_started = time.process_time()
        a._controller_cpu_cap = grant._limits["controller_cpu_seconds"]
        a._output_caps = grant._limits["output_bytes"], grant._limits["output_entries"]
        a._check_live = a._active

        def aggregate_receive(raw, header, output, **limits):
            a._active(); B.decode_header(header, adopted_image=a._image)
            self.receives["A"] += 1
            a._used[0] += 1; a._used[1] += len(raw); a._used[2] += limits["cpu_seconds"]
            handle = VerifiedAggregate()  # FABRICATED AFTER NO CRYPTOGRAPHIC CHECK.
            a._handles[handle] = header, sha(raw), len(raw)
            return handle
        a.receive = aggregate_receive

        if self.legacy is not None:
            i = self.legacy
            i._check_install = i._active
            def legacy_receive(raw, summary, output, **limits):
                i._active(); self.receives["I"] += 1
                i._used[0] += 1; i._used[1] += len(raw); i._used[2] += limits["cpu_seconds"]
                handle = VerifiedModule()  # FABRICATED, NOT A MATHEMATICAL WARRANT.
                exact = expected_journal(summary, 0, B.RELATION_IMAGE)
                i._handles[handle] = C.summary_id(summary), C.canonical(summary), exact, sha(raw)
                return handle
            i.receive = legacy_receive

        d = self.delta = self._make(MixedDeltaVerifier, "mixed", B.RELATION_IMAGE)
        d._owners = d._origins = self.legacy, a
        d._aggregate_image = IMAGE
        d._started = time.monotonic(); d._observed_worker = 0.0
        d._envelope = envelope; d._cache = {}
        d._output = grant.directory/"delta"; d._output.mkdir()
        d._caps = (grant._limits["acquisition"]["verify_attempts"], 65536,
                   grant._limits["acquisition"]["worker_cpu_seconds"], 30, 60, 128*MIB, 512)
        d._check = d._active
        def delta_receive(raw, summary, **limits):
            d._active(); self.receives["mixed"] += 1
            claims, frontiers, witnesses, census = parse_packet(raw, envelope, aggregate_image=IMAGE)
            if witnesses[-1][2] != summary: raise ValueError("TEST_SYNTHETIC_SUMMARY_MISMATCH")
            d._used[0] += 1; d._used[1] += len(raw)
            d._used[2] += census["claims"]*limits["receipt_cpu_seconds"]+census["deltas"]*limits["native_cpu_seconds"]
            exact = expected_journal(summary, witnesses[-1][3], B.RELATION_IMAGE)
            inventory = tuple(row[1] for row in frontiers)+(exact,)
            representations = {item: ("synthetic-unverified-test-only", sha(raw)) for item in inventory}
            handle = VerifiedMixedDelta()  # NO NATIVE OR RECEIPT VERIFICATION.
            d._handles[handle] = exact, raw, (), inventory, representations
            return handle
        d.receive = delta_receive

        self.preparation = None
        if preparation:
            p = self.preparation = MixedOwnerPreparation.__new__(MixedOwnerPreparation)
            p._closed = False; p._started = time.monotonic(); p._deadline = grant.deadline-1
            p._allowance = {"worker_cpu_seconds": 10, "controller_cpu_seconds": 30}
            p._output = grant.directory/"preparation"; p._output.mkdir()
            p._check = lambda: None
            p.report = lambda: {"calls": 0, "closed": p._closed, "test_only": True}
            def preparation_close():
                self.closes["preparation"] += 1; p._closed = True
            p.close = preparation_close

    def _make(self, cls, tag, image):
        owner = cls.__new__(cls)
        owner._closed = owner._busy = False
        owner._deadline = self.grant.deadline-1
        owner._image, owner._foundation, owner._policy = image, B.FOUNDATION, B.POLICY
        owner._profile_id = {"I": "11", "A": "22", "mixed": "33"}[tag]*32
        owner._caps = (8, 65536, self.grant._limits["acquisition"]["worker_cpu_seconds"])
        owner._used, owner._handles = [0, 0, 0], {}
        owner._pins = deepcopy(self.pins)
        def active(*unused):
            if owner._closed or time.monotonic() >= owner._deadline:
                raise ValueError("TEST_SYNTHETIC_ISSUER_CLOSED_OR_EXPIRED")
        owner._active = active
        original_close = cls.close
        def close():
            self.closes[tag] += 1
            original_close(owner)
        owner.close = close
        return owner

    def close(self):
        for owner in (self.preparation, self.delta, self.aggregate, self.legacy):
            if owner is not None: owner.close()


class MixedWorkspaceControls(unittest.TestCase):
    def setUp(self):
        # Short stable paths avoid making Windows path length depend on prose
        # test names; SELECTED in RESULT.json preserves the ordinal mapping.
        self.root = EVIDENCE/("c"+str(SELECTED.index(self._testMethodName)+1).zfill(2)); self.root.mkdir()
        self.workspaces, self.clients, self.owners = [], [], []

    def tearDown(self):
        for client in reversed(self.clients):
            if not client._closed: asyncio.run(client.close())
        for owners in reversed(self.owners): owners.close()
        for workspace in reversed(self.workspaces):
            if not workspace._closed: workspace.close()

    def setup_operation(self, name="workspace", *, legacy=False, preparation=False, cpu=120):
        workspace = W.Workspace.open(self.root/name, configuration(), create=True)
        self.workspaces.append(workspace)
        grant = workspace.reserve(grant_limits(cpu))
        owners = SyntheticOwners(grant, workspace._envelope, legacy=legacy, preparation=preparation)
        self.owners.append(owners)
        return workspace, grant, owners

    def connect(self, workspace, grant, owners, **overrides):
        arguments = dict(aggregate_owner=owners.aggregate, receipt_owner=owners.legacy,
            delta_owner=owners.delta, preparation_owner=owners.preparation,
            foundation_bytes=FOUNDATION_BYTES, foundation_sha256=sha(FOUNDATION_BYTES))
        arguments.update(overrides)
        client = workspace.operation(grant, **arguments)
        self.clients.append(client); return client

    def admit(self, client, index=0, *, receipt=RECEIPT, height=1):
        members, header = members_and_header(height)
        return client.admit_aggregate_member(receipt, header, members[index], index,
            B.opening(members, index), cpu_seconds=10, wall_seconds=20)

    def test_required_A_optional_I_and_persistent_profile(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                workspace, grant, owners = self.setup_operation("with-I" if legacy else "A-only", legacy=legacy)
                client = self.connect(workspace, grant, owners)
                self.assertIs(type(workspace.packets), PacketStore)
                self.assertEqual(workspace.packets.profile, public_profile(IMAGE))
                self.assertIs(client.receipt, owners.legacy)
                self.assertIs(client.aggregate, owners.aggregate)
                self.assertEqual(client.report()["schema"], W.REPORT_SCHEMA)
                self.assertFalse(workspace.status()["mathematical_acceptance"])
        self.assertNotEqual(W.SCHEMA, OLD.SCHEMA)
        wrong = configuration(); wrong["schema"] = OLD.SCHEMA
        with self.assertRaisesRegex(ValueError, "WORKSPACE_SCHEMA"):
            W.Workspace.open(self.root/"wrong-schema", wrong, create=True)

    def test_wrong_owner_image_pairing_and_missing_A_refuse_before_transfer(self):
        for defect in ("missing", "wrong-image", "wrong-pair", "unselected-I"):
            with self.subTest(defect=defect):
                workspace, grant, owners = self.setup_operation(defect, legacy=defect == "unselected-I")
                overrides = {}
                if defect == "missing": overrides["aggregate_owner"] = None
                elif defect == "wrong-image": owners.aggregate._image = "7b"*32
                elif defect == "wrong-pair": owners.delta._owners = (None, object())
                else: overrides["receipt_owner"] = None
                with self.assertRaisesRegex(ValueError, "EXACT_REAL_OWNERS|SHARED_MIXED_ORIGIN"):
                    self.connect(workspace, grant, owners, **overrides)
                self.assertFalse(grant._used)
                self.assertIsNone(workspace._client)
                self.assertEqual(sum(owners.receives.values()), 0)
                self.assertEqual(owners.closes["A"], 0)

    def test_pristine_A_and_original_suballocations_are_required(self):
        for defect in ("used-member", "cpu", "member-storage", "deadline", "source-pin"):
            with self.subTest(defect=defect):
                workspace, grant, owners = self.setup_operation(defect)
                if defect == "used-member": owners.aggregate._member_used[0] = 1
                elif defect == "cpu": owners.aggregate._caps = (8, 65536, 121)
                elif defect == "member-storage": owners.aggregate._member_caps = (4096, 17, MIB)
                elif defect == "deadline": owners.aggregate._deadline = grant.deadline+1
                else:
                    path = Path(W.__file__).resolve()
                    owners.aggregate._pins.pop(path); owners.delta._pins.pop(path)
                with self.assertRaisesRegex(ValueError, "PRISTINE|SUBALLOCATION|DEADLINE|REQUIRED_SOURCE"):
                    self.connect(workspace, grant, owners)
                self.assertFalse(grant._used)
                self.assertEqual(sum(owners.receives.values()), 0)

    def test_same_live_receipt_two_members_normalizes_exact_facts(self):
        workspace, grant, owners = self.setup_operation()
        client = self.connect(workspace, grant, owners)
        left = self.admit(client, 0); right = self.admit(client, 1); again = self.admit(client, 0)
        members, header = members_and_header()
        left_fact = client.describe(left); right_fact = client.describe(right)
        self.assertEqual(left_fact["kind"], "A-member")
        self.assertEqual(left_fact["live"]["journal"], members[0])
        self.assertEqual(right_fact["live"]["journal"], members[1])
        self.assertEqual(right_fact["live"]["member_index"], 1)
        self.assertNotEqual(left_fact["live"]["journal"], right_fact["live"]["journal"])
        self.assertIs(client._warrants[left][1], client._warrants[again][1])
        normalized = client._warrants[right][3]
        self.assertEqual(normalized["journal"], list(members[1]))
        self.assertEqual(normalized["aggregate_header"], list(header))
        self.assertEqual(normalized["siblings"], [list(x) for x in B.opening(members, 1)])
        C.canonical(normalized)
        self.assertEqual(owners.receives["A"], 1)
        self.assertEqual(len(client._aggregate_cache), 1)
        self.assertEqual(client._budget.report()["used"]["verify_attempts"], 1)
        self.assertEqual(client._budget.report()["used"]["worker_cpu_seconds"], 10)
        self.assertEqual(owners.aggregate.report()["live_members"], 2)

    def test_receipt_cache_binds_exact_header_and_receipt_bytes(self):
        workspace, grant, owners = self.setup_operation()
        client = self.connect(workspace, grant, owners)
        self.admit(client, height=1)
        self.admit(client, height=2)
        self.admit(client, receipt=RECEIPT+b"-different", height=2)
        self.assertEqual(owners.receives["A"], 3)
        self.assertEqual(len(client._aggregate_cache), 3)
        self.assertEqual(client._budget.report()["used"]["verify_attempts"], 3)

    def test_wrong_member_path_cannot_hit_receipt_cache_and_fail_closes_owners(self):
        workspace, grant, owners = self.setup_operation(legacy=True, preparation=True)
        client = self.connect(workspace, grant, owners)
        self.admit(client)
        members, header = members_and_header()
        wrong = [bytes(32) for unused in B.opening(members, 1)]
        with self.assertRaises(ValueError):
            client.admit_aggregate_member(RECEIPT, header, members[1], 1, wrong,
                                         cpu_seconds=10, wall_seconds=20)
        self.assertEqual(owners.receives["A"], 1)
        self.assertEqual(client._state, "FAILED")
        self.assertFalse(client._warrants); self.assertFalse(client._aggregate_cache)
        for tag in ("I", "A", "mixed", "preparation"):
            self.assertGreaterEqual(owners.closes[tag], 1)

    def test_direct_A_mixed_and_I_share_one_admission_budget(self):
        workspace, grant, owners = self.setup_operation(legacy=True, cpu=30)
        client = self.connect(workspace, grant, owners)
        self.admit(client)  # 10 reserved synthetic verification CPU.
        raw, summary = mixed_packet(); module = C.summary_id(summary)
        workspace.packets.put(module, raw)
        token = client.admit_local(module, sha(raw), len(raw), native_cpu_seconds=10,
                                  receipt_cpu_seconds=10, wall_seconds=20)
        self.assertEqual(client.describe(token)["kind"], "mixed")
        material = client.semantic_material(token)
        self.assertEqual(material["status"], "AVAILABLE_PACKET_SEMANTICS")
        self.assertFalse(material["mathematical_acceptance"])
        used = client._budget.report()["used"]
        self.assertEqual((used["verify_attempts"], used["worker_cpu_seconds"]), (2, 30))
        self.assertEqual(used["verification_input_bytes"], len(RECEIPT)+len(raw))
        with self.assertRaisesRegex(ValueError, "RECEIPT_VERIFY_BUDGET"):
            client.admit_receipt(b"SYNTHETIC-I", C.summarize(spec("otherI")), cpu_seconds=10, wall_seconds=20)
        self.assertEqual(owners.receives, {"I": 0, "A": 1, "mixed": 1})
        self.assertEqual(client._budget.report()["used"]["worker_cpu_seconds"], 30)
        self.assertEqual(client._state, "FAILED")

    def test_missing_I_owner_has_no_fallback(self):
        workspace, grant, owners = self.setup_operation()
        client = self.connect(workspace, grant, owners)
        with self.assertRaisesRegex(ValueError, "I_OWNER_NOT_SELECTED"):
            client.admit_receipt(b"NOT-I", C.summarize(spec("Irefused")))
        self.assertEqual(sum(owners.receives.values()), 0)
        self.assertTrue(owners.aggregate._closed)

    def test_cache_cannot_survive_owner_profile_change(self):
        workspace, grant, owners = self.setup_operation()
        client = self.connect(workspace, grant, owners)
        self.admit(client)
        owners.aggregate._profile_id = "44"*32  # Deliberate owner-state corruption.
        with self.assertRaisesRegex(ValueError, "ISSUER_PROFILE_CHANGED"):
            self.admit(client)
        self.assertEqual(owners.receives["A"], 1)
        self.assertFalse(client._aggregate_cache)
        self.assertTrue(owners.aggregate._closed)

    def test_substitution_closes_original_owners_not_untransferred_replacement(self):
        class Untransferred:
            def __init__(self): self.close_calls = 0
            def close(self): self.close_calls += 1
        for attribute in ("receipt", "aggregate", "delta", "preparation"):
            with self.subTest(attribute=attribute):
                workspace, grant, owners = self.setup_operation(attribute, legacy=True, preparation=True)
                client = self.connect(workspace, grant, owners); token = self.admit(client)
                member = client._warrants[token][1]
                replacement = Untransferred()
                setattr(client, attribute, replacement)  # Deliberate caller-state corruption.
                with self.assertRaisesRegex(ValueError, "MIXED_ORIGIN_CHANGED"):
                    client.describe(token)
                self.assertEqual(client._state, "FAILED")
                self.assertFalse(client._warrants); self.assertFalse(client._aggregate_cache)
                for owner in (owners.legacy, owners.aggregate, owners.delta, owners.preparation):
                    self.assertTrue(owner._closed)
                self.assertFalse(owners.aggregate._handles)
                self.assertFalse(owners.aggregate._members)
                self.assertFalse(owners.aggregate._member_cache)
                with self.assertRaisesRegex(ValueError, "ISSUER_CLOSED_OR_EXPIRED"):
                    owners.aggregate.describe_member(member)
                report = asyncio.run(client.close())
                self.assertEqual(report["status"], "FAILED")
                self.assertEqual(report["aggregate"]["attempts"], 1)
                self.assertEqual(report["aggregate"]["profile_id"], "22"*32)
                self.assertEqual(report["mixed"]["attempts"], 0)
                self.assertEqual(report["receipt"]["attempts"], 0)
                self.assertTrue(report["preparation"]["test_only"])
                self.assertEqual(replacement.close_calls, 0)

    def test_failed_cleanup_remains_uncertain_after_later_successful_close(self):
        workspace, grant, owners = self.setup_operation(legacy=True, preparation=True)
        client = self.connect(workspace, grant, owners); self.admit(client)
        original_close = owners.aggregate.close
        attempts = []
        def fail_once():
            attempts.append(1)
            if len(attempts) == 1: raise RuntimeError("TEST_INJECTED_CLEANUP_UNCERTAINTY")
            return original_close()
        owners.aggregate.close = fail_once
        members, header = members_and_header()
        with self.assertRaises(ValueError):
            client.admit_aggregate_member(RECEIPT, header, members[1], 1, [bytes(32)],
                                         cpu_seconds=10, wall_seconds=20)
        self.assertTrue(client._cleanup_uncertain); self.assertTrue(workspace._poisoned)
        self.assertFalse(owners.aggregate._closed)
        report = asyncio.run(client.close())
        self.assertEqual(len(attempts), 2)
        self.assertTrue(owners.aggregate._closed)
        self.assertFalse(owners.aggregate._members)
        self.assertTrue(report["cleanup_uncertain"])
        self.assertEqual(report["status"], "CLEANUP_INCOMPLETE")
        self.assertTrue(workspace._poisoned)
        with self.assertRaisesRegex(ValueError, "CLEANUP_UNCERTAIN"):
            workspace.reserve(grant_limits())

    def test_foreign_warrant_refuses_without_reusing_foreign_authority(self):
        w1, g1, o1 = self.setup_operation("one")
        c1 = self.connect(w1, g1, o1); token = self.admit(c1)
        w2, g2, o2 = self.setup_operation("two")
        c2 = self.connect(w2, g2, o2)
        with self.assertRaisesRegex(ValueError, "FOREIGN_WARRANT"):
            c2.describe(token)
        self.assertEqual(sum(o2.receives.values()), 0)
        self.assertTrue(o2.aggregate._closed)
        self.assertFalse(o1.aggregate._closed)
        self.assertEqual(c1.describe(token)["kind"], "A-member")

    def test_closed_or_expired_A_issuer_revokes_cached_warrant(self):
        for defect in ("closed", "expired"):
            with self.subTest(defect=defect):
                workspace, grant, owners = self.setup_operation(defect)
                client = self.connect(workspace, grant, owners); token = self.admit(client)
                if defect == "closed": owners.aggregate.close()
                else: owners.aggregate._deadline = time.monotonic()-1
                with self.assertRaisesRegex(ValueError, "ISSUER_CLOSED_OR_EXPIRED"):
                    client.describe(token)
                self.assertEqual(client._state, "FAILED")
                self.assertFalse(client._warrants)
                self.assertEqual(owners.receives["A"], 1)

    def test_A_member_import_dispatch_uses_same_three_owners(self):
        workspace, grant, owners = self.setup_operation(legacy=True)
        client = self.connect(workspace, grant, owners); token = self.admit(client)
        observed = {}
        class InertImport:
            # Explicit routing stub: no actual semantic import/materialization.
            def __init__(self, **kwargs): observed["owners"] = kwargs
            def use_aggregate_member(self, handle, raw, *, resolutions):
                observed["member"] = handle, raw, resolutions
            def materialize(self, batch, foundation, foundation_sha):
                observed["batch"] = C.parse_json(batch)
                return {"status": "SYNTHETIC_NEED_MATERIAL", "selection_binding": "55"*32,
                        "demands": [], "cost": {"synthetic": True}}, None
            def close(self): observed["closed"] = True
        with patch.object(W, "MixedImportSession", InertImport):
            result = client.import_context([{"warrant": token, "resolutions": None}], [], [], [])
        self.assertEqual(result["status"], "SYNTHETIC_NEED_MATERIAL")
        self.assertIs(observed["owners"]["legacy_verifier"], owners.legacy)
        self.assertIs(observed["owners"]["aggregate_verifier"], owners.aggregate)
        self.assertIs(observed["owners"]["delta_verifier"], owners.delta)
        self.assertIs(observed["member"][0], client._warrants[token][1])
        self.assertEqual(observed["member"][1], RECEIPT)
        self.assertFalse(result["mathematical_acceptance"])
        asyncio.run(client.close()); self.assertTrue(observed["closed"])

    def test_orderly_close_and_reopen_restore_no_A_authority(self):
        workspace, grant, owners = self.setup_operation(legacy=True, preparation=True)
        client = self.connect(workspace, grant, owners); token = self.admit(client)
        identifier = grant.identifier
        report = asyncio.run(client.close())
        self.assertEqual(report["status"], "CLOSED")
        for tag in ("I", "A", "mixed", "preparation"):
            self.assertGreaterEqual(owners.closes[tag], 1)
        self.assertFalse(client._warrants); self.assertFalse(client._aggregate_cache)
        workspace.close()
        again = W.Workspace.open(self.root/"workspace", configuration(), create=False)
        self.workspaces.append(again)
        record = again.read_record("operations", identifier)
        self.assertFalse(record["mathematical_acceptance"])
        fresh = again.reserve(grant_limits())
        new_owners = SyntheticOwners(fresh, again._envelope); self.owners.append(new_owners)
        new_client = self.connect(again, fresh, new_owners)
        self.assertEqual(new_owners.aggregate.report()["live_aggregates"], 0)
        with self.assertRaisesRegex(ValueError, "FOREIGN_WARRANT"):
            new_client.describe(token)
        self.assertEqual(sum(new_owners.receives.values()), 0)

    def test_standalone_A_is_not_silently_a_mixed_packet(self):
        workspace, grant, owners = self.setup_operation()
        client = self.connect(workspace, grant, owners)
        raw, summary = mixed_packet()
        _, _, witnesses, _ = parse_packet(raw, workspace._envelope, aggregate_image=IMAGE)
        self.assertEqual(witnesses[-1][2], summary)
        bad = C.parse_json(raw); bad["deltas"] = []
        with self.assertRaisesRegex(ValueError, "MIXED_COUNTS"):
            workspace.packets.inspect(C.summary_id(summary), C.canonical(bad))
        self.assertEqual(sum(owners.receives.values()), 0)


SELECTED = (
    "test_required_A_optional_I_and_persistent_profile",
    "test_wrong_owner_image_pairing_and_missing_A_refuse_before_transfer",
    "test_pristine_A_and_original_suballocations_are_required",
    "test_same_live_receipt_two_members_normalizes_exact_facts",
    "test_receipt_cache_binds_exact_header_and_receipt_bytes",
    "test_wrong_member_path_cannot_hit_receipt_cache_and_fail_closes_owners",
    "test_direct_A_mixed_and_I_share_one_admission_budget",
    "test_missing_I_owner_has_no_fallback",
    "test_cache_cannot_survive_owner_profile_change",
    "test_substitution_closes_original_owners_not_untransferred_replacement",
    "test_failed_cleanup_remains_uncertain_after_later_successful_close",
    "test_foreign_warrant_refuses_without_reusing_foreign_authority",
    "test_closed_or_expired_A_issuer_revokes_cached_warrant",
    "test_A_member_import_dispatch_uses_same_three_owners",
    "test_orderly_close_and_reopen_restore_no_A_authority",
    "test_standalone_A_is_not_silently_a_mixed_packet",
)
