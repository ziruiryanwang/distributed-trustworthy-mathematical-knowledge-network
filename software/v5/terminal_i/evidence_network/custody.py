"""One bounded exact-byte store; terminal-I is opt-in under a closed V2 profile."""
from copy import deepcopy
from dataclasses import asdict
import sqlite3

from aggregate_claims import bindings as B
from custody.receipt_store import ENCODING
from delta.custody import (
    PacketStore as LegacyPacketStore, LIMITS, MAX_PACKET,
    packet_digest, offer_request, blob_request)
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from mixed_claims.packet import Envelope, SCHEMA as MIXED_SCHEMA
from modules import codec as C
from . import packet as P

PROFILE_SCHEMA = "DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V1"
PROFILE_SCHEMA_V2 = "DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2"
OFFER_SCHEMA = "DMKN_V5_MODULE_EVIDENCE_OFFER_V1"
PROOF_FORM = "mixed-or-certified-terminal-v1"
PROOF_FORM_V2 = "mixed-or-certified-terminal-v2"


def public_profile(aggregate_image, terminal_i=False):
    B._adopted_image(aggregate_image)
    F.need(type(terminal_i) is bool, "EVIDENCE_TERMINAL_I_CAPABILITY")
    result = {"schema": PROFILE_SCHEMA, "proof_form": PROOF_FORM,
            "mixed_packet_schema": MIXED_SCHEMA, "terminal_packet_schema": P.SCHEMA,
            "relation_schema": "DMKN_CERTIFIED_MODULES_V2", "journal_profile": 2,
            "relation_image": B.RELATION_IMAGE, "aggregate_image": aggregate_image,
            "foundation": B.FOUNDATION, "policy": B.POLICY,
            "aggregate_header_magic": B.MAGIC.hex(), "aggregate_header_version": B.VERSION,
            "aggregate_header_bytes": B.HEADER_BYTES, "terminal_receipt_encoding": "lowercase-hex",
            "receipt_kind": "succinct-poseidon2", "receipt_encoding": deepcopy(ENCODING)}
    if terminal_i:
        result.update(schema=PROFILE_SCHEMA_V2, proof_form=PROOF_FORM_V2,
                      terminal_i_packet_schema=P.I_SCHEMA)
    return result


def profile_id(profile):
    F.need(type(profile) is dict and "aggregate_image" in profile, "EVIDENCE_WIRE_PROFILE")
    expected = public_profile(profile["aggregate_image"],
                              terminal_i=profile.get("schema") == PROFILE_SCHEMA_V2)
    F.fields(profile, expected)
    F.need(F.compact(profile) == F.compact(expected), "EVIDENCE_WIRE_PROFILE")
    return C.hash_value("module-evidence-wire-profile", profile)


def verify_offer(value, request, *, profile):
    offer_request(request)
    # An opaque profile ID alone cannot identify its proof form. Require the
    # exact selected profile even for V1; never accept either form globally.
    F.need(profile_id(profile) == request["wire_profile_id"], "EVIDENCE_OFFER_PROFILE")
    proof_form = profile["proof_form"]
    F.fields(value, ("schema", "module_id", "wire_profile_id", "proof_form", "packets",
                     "assurance", "global_complete", "mathematical_acceptance"))
    F.need(value["schema"] == OFFER_SCHEMA and value["module_id"] == request["module_id"]
           and value["wire_profile_id"] == request["wire_profile_id"] and value["proof_form"] == proof_form
           and value["assurance"] == "UNVERIFIED_EVIDENCE_LOCATORS_ONLY"
           and value["global_complete"] is False and value["mathematical_acceptance"] is False,
           "EVIDENCE_OFFER_BINDING")
    F.need(type(value["packets"]) is list and len(value["packets"]) <= request["max_offers"],
           "EVIDENCE_OFFER_COUNT")
    digests = []
    for row in value["packets"]:
        blob_request(row); digests.append(row["packet_sha256"])
    F.need(digests == sorted(set(digests)), "EVIDENCE_OFFER_ORDER")
    F.need(len(F.compact(value)) <= request["max_bytes"], "EVIDENCE_OFFER_BYTES")
    return deepcopy(value)


class PacketStore(LegacyPacketStore):
    """Fresh typed database; inherited transactions grant no proof authority."""
    def __init__(self, root, profile, limits, *, envelope=None,
                 terminal_receipt_bytes=P.MAX_RECEIPT, create=False):
        self.profile_id = profile_id(profile); self.profile = deepcopy(profile)
        self.envelope = Envelope() if envelope is None else envelope
        P.validate_limits(self.envelope, terminal_receipt_bytes)
        self.terminal_receipt_bytes = terminal_receipt_bytes
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items(): F.uint(limits[key], *bounds, "EVIDENCE_CUSTODY_LIMIT:"+key)
        F.need(limits["packet_bytes"] <= self.envelope.packet_bytes, "EVIDENCE_CUSTODY_PACKET_ENVELOPE")
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        if create: self.root.mkdir()
        path = ordinary(self.root/"evidence-packets.sqlite", fresh=create, directory=False)
        cfg = {"schema": "DMKN_V5_MODULE_EVIDENCE_CUSTODY_V1", "profile": profile,
               "limits": limits, "envelope": asdict(self.envelope),
               "terminal_receipt_bytes": terminal_receipt_bytes}
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-2048")
            F.need(self.db.execute("PRAGMA max_page_count="+str(limits["db_pages"])).fetchone()[0]
                   == limits["db_pages"], "EVIDENCE_CUSTODY_DB_CAP")
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
            F.need(row is not None and bytes(row[0]) == F.compact(cfg), "EVIDENCE_CUSTODY_CONFIG")
            self.status()
        except BaseException:
            self.close(); raise

    def inspect(self, module, raw):
        F.hexid(module); packet_digest(raw)
        F.need(profile_id(self.profile) == self.profile_id, "EVIDENCE_CUSTODY_PROFILE_CHANGED")
        F.need(len(raw) <= self.limits["packet_bytes"], "EVIDENCE_CUSTODY_OBJECT_CAP")
        unused_kind, target, unused_journal, census = P.inspect_evidence(raw, self.envelope,
            aggregate_image=self.profile["aggregate_image"], terminal_receipt_bytes=self.terminal_receipt_bytes,
            terminal_i=self.profile["schema"] == PROFILE_SCHEMA_V2)
        F.need(C.summary_id(target) == module, "EVIDENCE_CUSTODY_TARGET_BINDING")
        return target, census

    def offer(self, request):
        offer_request(request)
        F.need(profile_id(self.profile) == self.profile_id, "EVIDENCE_CUSTODY_PROFILE_CHANGED")
        F.need(request["wire_profile_id"] == self.profile_id, "EVIDENCE_CUSTODY_WIRE_PROFILE")
        rows = self.db.execute("SELECT p.digest,p.size FROM offers o JOIN packets p ON o.digest=p.digest "
            "WHERE o.module=? AND o.profile=? ORDER BY o.digest LIMIT ?",
            (request["module_id"], self.profile_id, request["max_offers"])).fetchall()
        value = {"schema": OFFER_SCHEMA, "module_id": request["module_id"], "wire_profile_id": self.profile_id,
                 "proof_form": self.profile["proof_form"],
                 "packets": [{"packet_sha256": digest, "packet_bytes": size} for digest, size in rows],
                 "assurance": "UNVERIFIED_EVIDENCE_LOCATORS_ONLY", "global_complete": False,
                 "mathematical_acceptance": False}
        return verify_offer(value, request, profile=self.profile)
