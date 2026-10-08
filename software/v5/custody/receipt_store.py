"""Bounded opaque receipt custody. No receipt decoding or mathematical authority."""
from copy import deepcopy
import hashlib
import sqlite3

from modules import codec as C
from discovery import formal_features as F
from discovery.discovery_store import ordinary

MAX_RECEIPT = 64*1024**2
PROFILE_SCHEMA = "DMKN_V5_RECEIPT_WIRE_PROFILE_V1"
OFFER_SCHEMA = "DMKN_V5_MODULE_RECEIPT_OFFER_V1"
# Exact retained implementation selection, not a portable serialization ABI
# proof. Rlib hashes below identify compiled artifacts; the dependency manifest
# hash identifies their provenance record. Different independent builds are not
# automatically compatible. No local path is itself part of this wire profile.
# LINK-INPUTS is the frozen collection-host record reused by module-host03.
ENCODING = {
    "codec": "bincode", "integer_encoding": "fixed-width", "endianness": "little",
    "trailing_bytes": "reject", "max_bytes": MAX_RECEIPT, "receipt_type": "risc0_zkvm::Receipt",
    "retained_risc0_zkvm_rlib_sha256": "5c5bff2476163fe1fcb6453f9b7d5aa84e1887b349a939ae5fffddd90ee5c434",
    "retained_serde_rlib_sha256": "c2bdec00d6bc0942b77e31495ca7d3aec7df7370e42cf65335b232ff35e32044",
    "retained_bincode_rlib_sha256": "c9dc6a56e36315e813f1f02aeb8a67edd1c5fdc287347fb7810f94c9e310ddfa",
    "retained_dependency_manifest_sha256": "ced49032a348d1784cee327d5a3368e8f942335210854e403053d289b06b5e0a",
    "verifier_context": "RETAINED_SDK_DEFAULT_WITH_DEV_MODE_FALSE_FULL_APPLICATION_NO_ASSUMPTIONS"}
LIMITS = {"receipts": (1, 100000), "offers": (1, 1000000), "offers_per_module": (1, 64),
          "receipt_bytes": (1, MAX_RECEIPT), "logical_bytes": (1024, 2**40), "db_pages": (256, 268435456)}


def public_profile(image, foundation, policy):
    return {"schema": PROFILE_SCHEMA, "encoding": deepcopy(ENCODING),
            "receipt_kind": "succinct-poseidon2", "journal_profile": 2,
            "image": F.hexid(image), "foundation": F.hexid(foundation), "policy": F.hexid(policy)}


def profile_id(profile):
    F.fields(profile, ("schema", "encoding", "receipt_kind", "journal_profile", "image", "foundation", "policy"))
    F.need(F.compact(profile) == F.compact(public_profile(profile["image"], profile["foundation"], profile["policy"])),
           "RECEIPT_WIRE_PROFILE")
    return C.hash_value("receipt-wire-profile", profile)


def receipt_digest(raw):
    F.need(type(raw) is bytes and 0 < len(raw) <= MAX_RECEIPT, "RECEIPT_BLOB_BOUND")
    return hashlib.sha256(raw).hexdigest()


def offer_request(request):
    F.fields(request, ("module_id", "wire_profile_id", "max_offers", "max_bytes"))
    F.hexid(request["module_id"]); F.hexid(request["wire_profile_id"])
    F.uint(request["max_offers"], 1, 8); F.uint(request["max_bytes"], 1024, 16384)


def blob_request(request):
    F.fields(request, ("receipt_sha256", "receipt_bytes"))
    F.hexid(request["receipt_sha256"]); F.uint(request["receipt_bytes"], 1, MAX_RECEIPT)


def verify_offer(value, request):
    offer_request(request)
    F.fields(value, ("schema", "module_id", "wire_profile_id", "receipts", "assurance", "global_complete", "mathematical_acceptance"))
    F.need(value["schema"] == OFFER_SCHEMA and value["module_id"] == request["module_id"]
           and value["wire_profile_id"] == request["wire_profile_id"]
           and value["assurance"] == "UNVERIFIED_RECEIPT_BYTE_LOCATORS_ONLY"
           and value["global_complete"] is False and value["mathematical_acceptance"] is False,
           "RECEIPT_OFFER_BINDING")
    F.need(type(value["receipts"]) is list and len(value["receipts"]) <= request["max_offers"], "RECEIPT_OFFER_COUNT")
    ids = []
    for row in value["receipts"]:
        blob_request(row); ids.append(row["receipt_sha256"])
    F.need(ids == sorted(set(ids)), "RECEIPT_OFFER_ORDER")
    F.need(len(F.compact(value)) <= request["max_bytes"], "RECEIPT_OFFER_BYTES")
    return deepcopy(value)


class ReceiptStore:
    def __init__(self, root, profile, limits, *, create=False):
        self.profile_id = profile_id(profile); self.profile = deepcopy(profile)
        F.fields(limits, LIMITS)
        for key, bounds in LIMITS.items(): F.uint(limits[key], *bounds, "RECEIPT_STORE_LIMIT:"+key)
        self.limits, self.db = dict(limits), None
        self.root = ordinary(root, fresh=create)
        if create: self.root.mkdir()
        path = ordinary(self.root / "receipts.sqlite", fresh=create, directory=False)
        cfg = {"schema": "DMKN_V5_RECEIPT_CUSTODY_V1", "profile": profile, "limits": limits}
        self.db = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE"); self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("PRAGMA foreign_keys=ON"); self.db.execute("PRAGMA temp_store=MEMORY")
            self.db.execute("PRAGMA mmap_size=0"); self.db.execute("PRAGMA cache_size=-2048")
            F.need(self.db.execute("PRAGMA max_page_count="+str(limits["db_pages"])).fetchone()[0] == limits["db_pages"], "RECEIPT_DB_CAP")
            if create:
                self.db.executescript("""
                    BEGIN IMMEDIATE;
                    CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), cfg BLOB NOT NULL,
                        receipts INTEGER NOT NULL, offers INTEGER NOT NULL, logical_bytes INTEGER NOT NULL);
                    CREATE TABLE receipts(digest TEXT PRIMARY KEY, size INTEGER NOT NULL, blob BLOB NOT NULL) WITHOUT ROWID;
                    CREATE TABLE offers(module TEXT NOT NULL, profile TEXT NOT NULL, digest TEXT NOT NULL,
                        PRIMARY KEY(module,profile,digest), FOREIGN KEY(digest) REFERENCES receipts(digest)) WITHOUT ROWID;
                    COMMIT;
                """)
                self.db.execute("INSERT INTO meta VALUES(1,?,0,0,0)", (F.compact(cfg),))
            row = self.db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()
            F.need(row is not None and bytes(row[0]) == F.compact(cfg), "RECEIPT_STORE_CONFIG")
            self.status()
        except BaseException: self.close(); raise

    def close(self):
        if self.db is not None: self.db.close(); self.db = None

    def status(self):
        row = self.db.execute("SELECT receipts,offers,logical_bytes FROM meta WHERE id=1").fetchone()
        F.need(row is not None, "RECEIPT_STORE_META")
        counts = dict(zip(("receipts", "offers", "logical_bytes"), row))
        for key, value in counts.items(): F.uint(value, 0, self.limits[key], "RECEIPT_STORED_QUOTA")
        return {"counts": counts, "wire_profile_id": self.profile_id, "mathematical_acceptance": False}

    def put(self, module, raw, *, before_commit=None):
        F.hexid(module); digest = receipt_digest(raw)
        F.need(len(raw) <= self.limits["receipt_bytes"], "RECEIPT_STORE_OBJECT_CAP")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT size,length(blob) FROM receipts WHERE digest=?", (digest,)).fetchone()
            if old is not None: F.need(self.get(digest, len(raw)) == raw, "RECEIPT_STORE_CONFLICT")
            offer = self.db.execute("SELECT 1 FROM offers WHERE module=? AND profile=? AND digest=?",
                                    (module, self.profile_id, digest)).fetchone()
            added_receipt, added_offer = int(old is None), int(offer is None)
            local = self.db.execute("SELECT count(*) FROM offers WHERE module=? AND profile=?", (module, self.profile_id)).fetchone()[0]
            F.need(local+added_offer <= self.limits["offers_per_module"], "RECEIPT_STORE_LOCAL_OFFERS")
            amounts = {"receipts": added_receipt, "offers": added_offer,
                       "logical_bytes": added_receipt*(len(raw)+64+8)+added_offer*192}
            counts = self.status()["counts"]
            for key, delta in amounts.items(): F.need(counts[key]+delta <= self.limits[key], "RECEIPT_STORE_QUOTA:"+key)
            if added_receipt: self.db.execute("INSERT INTO receipts VALUES(?,?,?)", (digest, len(raw), raw))
            if added_offer: self.db.execute("INSERT INTO offers VALUES(?,?,?)", (module, self.profile_id, digest))
            for key, delta in amounts.items(): self.db.execute("UPDATE meta SET "+key+"="+key+"+? WHERE id=1", (delta,))
            if before_commit is not None: before_commit()
            self.db.execute("COMMIT")
            return {"receipt_sha256": digest, "receipt_bytes": len(raw), "new_receipt": bool(added_receipt),
                    "new_offer": bool(added_offer), "mathematical_acceptance": False}
        except BaseException:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def get(self, digest, size):
        blob_request({"receipt_sha256": digest, "receipt_bytes": size})
        F.need(size <= self.limits["receipt_bytes"], "RECEIPT_STORE_OBJECT_CAP")
        row = self.db.execute("SELECT size,length(blob) FROM receipts WHERE digest=?", (digest,)).fetchone()
        F.need(row is not None and row == (size, size), "RECEIPT_STORE_SIZE_OR_MISSING")
        raw = bytes(self.db.execute("SELECT blob FROM receipts WHERE digest=?", (digest,)).fetchone()[0])
        F.need(len(raw) == size and receipt_digest(raw) == digest, "RECEIPT_STORE_DIGEST")
        return raw

    def offer(self, request):
        offer_request(request)
        F.need(request["wire_profile_id"] == self.profile_id, "RECEIPT_STORE_PROFILE")
        rows = self.db.execute("SELECT r.digest,r.size FROM offers o JOIN receipts r ON o.digest=r.digest "
            "WHERE o.module=? AND o.profile=? ORDER BY o.digest LIMIT ?",
            (request["module_id"], self.profile_id, request["max_offers"])).fetchall()
        value = {"schema": OFFER_SCHEMA, "module_id": request["module_id"], "wire_profile_id": self.profile_id,
                 "receipts": [{"receipt_sha256": digest, "receipt_bytes": size} for digest, size in rows],
                 "assurance": "UNVERIFIED_RECEIPT_BYTE_LOCATORS_ONLY", "global_complete": False, "mathematical_acceptance": False}
        return verify_offer(value, request)
