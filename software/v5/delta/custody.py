"""Separate bounded custody for complete native-delta packet bytes.

Structural parsing/hash binding is NOT checking, a receipt or admission. No
remote write endpoint is supplied. SQLite state is trusted owner-maintained data.
"""
from copy import deepcopy
from dataclasses import asdict
import hashlib
import sqlite3

from custody.receipt_store import public_profile as receipt_profile, profile_id as receipt_profile_id
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from modules import codec as C
from .packet import Envelope, SCHEMA as PACKET_SCHEMA, MIB, parse_packet

MAX_PACKET = 32*MIB
PROFILE_SCHEMA = "DMKN_V5_NATIVE_DELTA_WIRE_PROFILE_V1"
OFFER_SCHEMA = "DMKN_V5_NATIVE_DELTA_OFFER_V1"
LIMITS = {"packets": (1, 100000), "offers": (1, 1000000), "offers_per_module": (1, 64),
          "packet_bytes": (1, MAX_PACKET), "logical_bytes": (1024, 2**40), "db_pages": (256, 268435456)}


def public_profile(image, foundation, policy):
    frontier = receipt_profile(image, foundation, policy)
    return {"schema": PROFILE_SCHEMA, "proof_form": "bounded-native-delta-v1",
            "packet_schema": PACKET_SCHEMA, "relation_schema": "DMKN_CERTIFIED_MODULES_V2",
            "journal_profile": 2, "image": F.hexid(image), "foundation": F.hexid(foundation),
            "policy": F.hexid(policy), "frontier_receipt_profile": frontier}


def profile_id(profile):
    F.fields(profile, ("schema", "proof_form", "packet_schema", "relation_schema", "journal_profile",
                       "image", "foundation", "policy", "frontier_receipt_profile"))
    expected = public_profile(profile["image"], profile["foundation"], profile["policy"])
    F.need(F.compact(profile) == F.compact(expected), "DELTA_WIRE_PROFILE")
    receipt_profile_id(profile["frontier_receipt_profile"])
    return C.hash_value("native-delta-wire-profile", profile)


def packet_digest(raw):
    F.need(type(raw) is bytes and 0 < len(raw) <= MAX_PACKET, "DELTA_PACKET_BLOB_BOUND")
    return hashlib.sha256(raw).hexdigest()


def offer_request(value):
    F.fields(value, ("module_id", "wire_profile_id", "max_offers", "max_bytes"))
    F.hexid(value["module_id"]); F.hexid(value["wire_profile_id"])
    F.uint(value["max_offers"], 1, 8); F.uint(value["max_bytes"], 1024, 16384)


def blob_request(value):
    F.fields(value, ("packet_sha256", "packet_bytes"))
    F.hexid(value["packet_sha256"]); F.uint(value["packet_bytes"], 1, MAX_PACKET)


def verify_offer(value, request):
    offer_request(request)
    F.fields(value, ("schema", "module_id", "wire_profile_id", "proof_form", "packets",
                     "assurance", "global_complete", "mathematical_acceptance"))
    F.need(value["schema"] == OFFER_SCHEMA and value["module_id"] == request["module_id"]
           and value["wire_profile_id"] == request["wire_profile_id"]
           and value["proof_form"] == "bounded-native-delta-v1"
           and value["assurance"] == "UNVERIFIED_DELTA_PACKET_LOCATORS_ONLY"
           and value["global_complete"] is False and value["mathematical_acceptance"] is False,
           "DELTA_OFFER_BINDING")
    F.need(type(value["packets"]) is list and len(value["packets"]) <= request["max_offers"],
           "DELTA_OFFER_COUNT")
    digests = []
    for row in value["packets"]:
        blob_request(row); digests.append(row["packet_sha256"])
    F.need(digests == sorted(set(digests)), "DELTA_OFFER_ORDER")
    F.need(len(F.compact(value)) <= request["max_bytes"], "DELTA_OFFER_BYTES")
    return deepcopy(value)


class PacketStore:
    """Immutable exact blobs plus untrusted per-target offers, in one transaction."""
    def __init__(self, root, profile, limits, *, envelope=None, create=False):
        self.profile_id = profile_id(profile); self.profile = deepcopy(profile)
        self.envelope = Envelope() if envelope is None else envelope
        F.need(type(self.envelope) is Envelope, "DELTA_CUSTODY_EXACT_ENVELOPE")
        self.envelope.validate()
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items(): F.uint(limits[key], *bounds, "DELTA_CUSTODY_LIMIT:"+key)
        F.need(limits["packet_bytes"] <= self.envelope.packet_bytes, "DELTA_CUSTODY_PACKET_ENVELOPE")
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        if create: self.root.mkdir()
        path = ordinary(self.root/"delta-packets.sqlite", fresh=create, directory=False)
        cfg = {"schema": "DMKN_V5_NATIVE_DELTA_CUSTODY_V1", "profile": profile,
               "limits": limits, "envelope": asdict(self.envelope)}
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-2048")
            F.need(self.db.execute("PRAGMA max_page_count="+str(limits["db_pages"])).fetchone()[0]
                   == limits["db_pages"], "DELTA_CUSTODY_DB_CAP")
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
            F.need(row is not None and bytes(row[0]) == F.compact(cfg), "DELTA_CUSTODY_CONFIG")
            self.status()
        except BaseException:
            self.close(); raise

    def close(self):
        if self.db is not None: self.db.close(); self.db = None

    def status(self):
        row = self.db.execute("SELECT packets,offers,logical_bytes FROM meta WHERE id=1").fetchone()
        F.need(row is not None, "DELTA_CUSTODY_META")
        counts = dict(zip(("packets", "offers", "logical_bytes"), row))
        for key, value in counts.items(): F.uint(value, 0, self.limits[key], "DELTA_CUSTODY_STORED_QUOTA")
        return {"counts": counts, "wire_profile_id": self.profile_id, "mathematical_acceptance": False}

    def inspect(self, module, raw):
        """Bound the full submitted packet; structural target equality is not validity."""
        F.hexid(module); packet_digest(raw)
        F.need(len(raw) <= self.limits["packet_bytes"], "DELTA_CUSTODY_OBJECT_CAP")
        received, witnesses, census = parse_packet(raw, self.envelope)
        target = witnesses[-1][2]
        F.need(C.summary_id(target) == module, "DELTA_CUSTODY_TARGET_BINDING")
        image = bytes.fromhex(self.profile["image"])
        words = [int.from_bytes(image[i:i+4], "little") for i in range(0, 32, 4)]
        summaries = [C.parse_json(summary) for unused, summary in received]
        for witness, parents, summary, rank in witnesses:
            F.need(C.parse_json(witness)["image"] == words, "DELTA_CUSTODY_IMAGE")
            summaries.append(summary)
        F.need(all(s["foundation"] == self.profile["foundation"] and s["policy"] == self.profile["policy"]
                   for s in summaries), "DELTA_CUSTODY_SEMANTIC_PROFILE")
        return target, census

    def put(self, module, raw, *, before_commit=None):
        self.inspect(module, raw); digest = packet_digest(raw)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT size,module FROM packets WHERE digest=?", (digest,)).fetchone()
            if old is not None:
                F.need(old == (len(raw), module) and self.get(digest, len(raw)) == raw,
                       "DELTA_CUSTODY_PACKET_CONFLICT")
            exists = self.db.execute("SELECT 1 FROM offers WHERE module=? AND profile=? AND digest=?",
                                    (module, self.profile_id, digest)).fetchone()
            added_packet, added_offer = int(old is None), int(exists is None)
            local = self.db.execute("SELECT count(*) FROM offers WHERE module=? AND profile=?",
                                    (module, self.profile_id)).fetchone()[0]
            F.need(local+added_offer <= self.limits["offers_per_module"], "DELTA_CUSTODY_LOCAL_OFFERS")
            amounts = {"packets": added_packet, "offers": added_offer,
                       "logical_bytes": added_packet*(len(raw)+128+8)+added_offer*192}
            counts = self.status()["counts"]
            for key, change in amounts.items():
                F.need(counts[key]+change <= self.limits[key], "DELTA_CUSTODY_QUOTA:"+key)
            if added_packet: self.db.execute("INSERT INTO packets VALUES(?,?,?,?)", (digest, len(raw), module, raw))
            if added_offer: self.db.execute("INSERT INTO offers VALUES(?,?,?)", (module, self.profile_id, digest))
            for key, change in amounts.items(): self.db.execute("UPDATE meta SET "+key+"="+key+"+? WHERE id=1", (change,))
            if before_commit is not None: before_commit()
            self.db.execute("COMMIT")
            return {"packet_sha256": digest, "packet_bytes": len(raw), "new_packet": bool(added_packet),
                    "new_offer": bool(added_offer), "mathematical_acceptance": False}
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def get(self, digest, size):
        blob_request({"packet_sha256": digest, "packet_bytes": size})
        F.need(size <= self.limits["packet_bytes"], "DELTA_CUSTODY_OBJECT_CAP")
        row = self.db.execute("SELECT size,length(blob) FROM packets WHERE digest=?", (digest,)).fetchone()
        F.need(row == (size, size), "DELTA_CUSTODY_SIZE_OR_MISSING")
        raw = bytes(self.db.execute("SELECT blob FROM packets WHERE digest=?", (digest,)).fetchone()[0])
        F.need(len(raw) == size and packet_digest(raw) == digest, "DELTA_CUSTODY_DIGEST")
        return raw

    def offer(self, request):
        offer_request(request)
        F.need(request["wire_profile_id"] == self.profile_id, "DELTA_CUSTODY_WIRE_PROFILE")
        rows = self.db.execute("SELECT p.digest,p.size FROM offers o JOIN packets p ON o.digest=p.digest "
            "WHERE o.module=? AND o.profile=? ORDER BY o.digest LIMIT ?",
            (request["module_id"], self.profile_id, request["max_offers"])).fetchall()
        value = {"schema": OFFER_SCHEMA, "module_id": request["module_id"], "wire_profile_id": self.profile_id,
                 "proof_form": "bounded-native-delta-v1",
                 "packets": [{"packet_sha256": digest, "packet_bytes": size} for digest, size in rows],
                 "assurance": "UNVERIFIED_DELTA_PACKET_LOCATORS_ONLY", "global_complete": False,
                 "mathematical_acceptance": False}
        return verify_offer(value, request)
