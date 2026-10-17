"""Explicit I-only profile over unchanged mixed packet bytes and mathematics.

The profile restricts terminal claims to genuine I receipts. No aggregate image
is configured and no A claim is accepted. Stored packets remain untrusted until
the unchanged mixed verifier admits them. Old A-capable stores are not migrated.
"""
from copy import deepcopy
from dataclasses import asdict
import sqlite3

from aggregate_claims import bindings as B
from custody.receipt_store import ENCODING
from delta.custody import (
    PacketStore as BlobStore, LIMITS, MAX_PACKET,
    packet_digest, offer_request, blob_request)
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from mixed_claims.packet import Envelope, SCHEMA as PACKET_SCHEMA, parse_packet
from modules import codec as C

PROFILE_SCHEMA = "DMKN_V5_I_FRONTIER_DELTA_WIRE_PROFILE_V1"
OFFER_SCHEMA = "DMKN_V5_I_FRONTIER_DELTA_OFFER_V1"
CUSTODY_SCHEMA = "DMKN_V5_I_FRONTIER_DELTA_CUSTODY_V1"
PROOF_FORM = "bounded-i-frontier-mixed-delta-v1"
ASSURANCE = "UNVERIFIED_I_FRONTIER_PACKET_LOCATORS_ONLY"


def public_profile():
    """One exact locally selected profile; remote peers select no foundations."""
    return {"schema": PROFILE_SCHEMA, "proof_form": PROOF_FORM,
            "packet_schema": PACKET_SCHEMA, "relation_schema": "DMKN_CERTIFIED_MODULES_V2",
            "journal_profile": 2, "relation_image": B.RELATION_IMAGE,
            "aggregate_image": None, "supported_claim_tags": [0],
            "foundation": B.FOUNDATION, "policy": B.POLICY,
            "receipt_kind": "succinct-poseidon2", "receipt_encoding": deepcopy(ENCODING)}


def profile_id(profile):
    expected = public_profile()
    F.fields(profile, expected)
    F.need(F.compact(profile) == F.compact(expected), "I_FRONTIER_WIRE_PROFILE")
    return C.hash_value("i-frontier-mixed-delta-wire-profile-v1", profile)


def verify_offer(value, request):
    offer_request(request)
    F.need(request["wire_profile_id"] == profile_id(public_profile()), "I_FRONTIER_OFFER_PROFILE")
    F.fields(value, ("schema", "module_id", "wire_profile_id", "proof_form", "packets",
                     "assurance", "global_complete", "mathematical_acceptance"))
    F.need(value["schema"] == OFFER_SCHEMA and value["module_id"] == request["module_id"]
           and value["wire_profile_id"] == request["wire_profile_id"]
           and value["proof_form"] == PROOF_FORM and value["assurance"] == ASSURANCE
           and value["global_complete"] is False and value["mathematical_acceptance"] is False,
           "I_FRONTIER_OFFER_BINDING")
    F.need(type(value["packets"]) is list and len(value["packets"]) <= request["max_offers"],
           "I_FRONTIER_OFFER_COUNT")
    digests = []
    for row in value["packets"]:
        blob_request(row); digests.append(row["packet_sha256"])
    F.need(digests == sorted(set(digests)), "I_FRONTIER_OFFER_ORDER")
    F.need(len(F.compact(value)) <= request["max_bytes"], "I_FRONTIER_OFFER_BYTES")
    return deepcopy(value)


class PacketStore(BlobStore):
    """Fresh profile-specific SQLite state, reusing only opaque blob mechanics.

    Inherited put/get/status/close use this instance's fields and self.inspect;
    no inherited legacy profile constructor, parser or offer method is used.
    """
    def __init__(self, root, profile, limits, *, envelope=None, create=False):
        self.profile_id = profile_id(profile); self.profile = deepcopy(profile)
        self.envelope = Envelope() if envelope is None else envelope
        F.need(type(self.envelope) is Envelope, "I_FRONTIER_CUSTODY_EXACT_ENVELOPE")
        self.envelope.validate()
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items(): F.uint(limits[key], *bounds, "I_FRONTIER_CUSTODY_LIMIT:"+key)
        F.need(limits["packet_bytes"] <= self.envelope.packet_bytes, "I_FRONTIER_CUSTODY_PACKET_ENVELOPE")
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        if create: self.root.mkdir()
        path = ordinary(self.root/"i-frontier-packets.sqlite", fresh=create, directory=False)
        cfg = {"schema": CUSTODY_SCHEMA, "profile": profile,
               "limits": limits, "envelope": asdict(self.envelope)}
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-2048")
            F.need(self.db.execute("PRAGMA max_page_count="+str(limits["db_pages"])).fetchone()[0]
                   == limits["db_pages"], "I_FRONTIER_CUSTODY_DB_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
                        packets INTEGER NOT NULL, offers INTEGER NOT NULL, logical_bytes INTEGER NOT NULL);
                    CREATE TABLE packets(digest TEXT PRIMARY KEY, size INTEGER NOT NULL,
                        module TEXT NOT NULL, blob BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE offers(module TEXT NOT NULL, profile TEXT NOT NULL, digest TEXT NOT NULL,
                        PRIMARY KEY(module,profile,digest), FOREIGN KEY(digest) REFERENCES packets(digest)) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,0,0,0)", (F.compact(cfg),))
            row = self.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()
            F.need(row is not None and bytes(row[0]) == F.compact(cfg), "I_FRONTIER_CUSTODY_CONFIG")
            self.status()
        except BaseException:
            self.close(); raise

    def inspect(self, module, raw):
        F.need(profile_id(self.profile) == self.profile_id, "I_FRONTIER_CUSTODY_PROFILE_CHANGED")
        F.hexid(module); packet_digest(raw)
        F.need(len(raw) <= self.limits["packet_bytes"], "I_FRONTIER_CUSTODY_OBJECT_CAP")
        unused_claims, unused_frontiers, witnesses, census = parse_packet(
            raw, self.envelope, aggregate_image=None)
        target = witnesses[-1][2]
        F.need(C.summary_id(target) == module, "I_FRONTIER_CUSTODY_TARGET_BINDING")
        # The parser rejects tag-1 before mathematical processing and binds I/F/P.
        # Receipt blobs remain uninterpreted here; custody is not admission.
        return target, census

    def offer(self, request):
        offer_request(request)
        F.need(profile_id(self.profile) == self.profile_id
               and request["wire_profile_id"] == self.profile_id, "I_FRONTIER_CUSTODY_WIRE_PROFILE")
        rows = self.db.execute("SELECT p.digest,p.size FROM offers o JOIN packets p ON o.digest=p.digest "
            "WHERE o.module=? AND o.profile=? ORDER BY o.digest LIMIT ?",
            (request["module_id"], self.profile_id, request["max_offers"])).fetchall()
        value = {"schema": OFFER_SCHEMA, "module_id": request["module_id"], "wire_profile_id": self.profile_id,
                 "proof_form": PROOF_FORM,
                 "packets": [{"packet_sha256": digest, "packet_bytes": size} for digest, size in rows],
                 "assurance": ASSURANCE, "global_complete": False, "mathematical_acceptance": False}
        return verify_offer(value, request)
