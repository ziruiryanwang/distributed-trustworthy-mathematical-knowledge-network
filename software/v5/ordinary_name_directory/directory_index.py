"""An immutable advisory name projection with authenticated point lookups.

This is not an owner, a mathematical warrant, or current-root validation.
The caller supplies the approved evidence codec and ordinal-vector primitive.
Sortedness and complete historical coverage are established by the exporter;
an arbitrary peer-selected Merkle root does not establish either property.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

SCHEMA = "DMKN_HISTORICAL_NAME_DIRECTORY_V1"
MAX_NAMES = 1048576
MAX_MANIFEST = 8192
HEX_FIELDS = ("semantic_id", "foundation_id", "implementation_id", "store_id",
              "context_root", "source_profile_sha256", "name_codec_sha256")
CLAIMS = {"mathematical_acceptance": False,
          "owner_status": "NOT_REOPENED_BY_LOOKUP",
          "snapshot_integrity": "NOT_CHECKED",
          "scope": "COMPLETE_HISTORICAL_EXPORT_NOT_CURRENT_OR_GLOBAL_ABSENCE"}


def need(value, code):
    if not value:
        raise ValueError("DIRECTORY_" + code)


def hexid(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "HASH")
    return value


def metadata_checked(metadata):
    need(type(metadata) is dict and set(metadata) == set(HEX_FIELDS) | {"exported_at_utc"},
         "METADATA_FIELDS")
    for field in HEX_FIELDS:
        hexid(metadata[field])
    need(type(metadata["exported_at_utc"]) is str and
         re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", metadata["exported_at_utc"]),
         "EXPORT_TIME")
    return dict(metadata)


def context_id(metadata, auth):
    return auth.digest("DMKN-HISTORICAL-NAME-DIRECTORY-CONTEXT-V1", metadata)


def name_digest(key, auth):
    return bytes.fromhex(auth.H("NAME-DIRECTORY-KEY", key))


def record_id(row, auth):
    need(type(row) is bytes and len(row) == 64, "RECORD_SIZE")
    return auth.H("NAME-DIRECTORY-RECORD", row)


def shape(count):
    need(type(count) is int and 0 <= count <= MAX_NAMES, "COUNT")
    power = 1 << (max(1, count)-1).bit_length()
    return power, 64 * count, 32 * (2 * power-1)


def descriptor_checked(raw, expected, *, evidence, auth):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_MANIFEST, "MANIFEST_SIZE")
    need(hashlib.sha256(raw).hexdigest() == hexid(expected), "MANIFEST_PIN")
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "MANIFEST_DUPLICATE")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("DIRECTORY_MANIFEST_NUMBER")
    try:
        doc = json.loads(raw, object_pairs_hook=pairs, parse_float=reject,
                         parse_constant=reject)
    except (RecursionError, UnicodeError) as error:
        raise ValueError("DIRECTORY_MANIFEST_SYNTAX") from error
    need(evidence.canonical_json(doc) == raw, "MANIFEST_CANONICAL")
    need(type(doc) is dict and set(doc) == {"schema", "metadata", "count", "context",
         "tree_root", "vector_commit", "entries_bytes", "tree_bytes", "claims"},
         "MANIFEST_FIELDS")
    need(doc["schema"] == SCHEMA and evidence.canonical_json(doc["claims"]) ==
         evidence.canonical_json(CLAIMS), "MANIFEST_SCHEMA")
    metadata = metadata_checked(doc["metadata"])
    power, entries_size, tree_size = shape(doc["count"])
    need(type(doc["entries_bytes"]) is int and doc["entries_bytes"] == entries_size and
         type(doc["tree_bytes"]) is int and doc["tree_bytes"] == tree_size, "FILE_SIZES")
    need(doc["context"] == context_id(metadata, auth), "CONTEXT")
    root = hexid(doc["tree_root"])
    need(doc["vector_commit"] == auth.vector_commit(doc["context"], doc["count"], root),
         "VECTOR_COMMIT")
    if doc["count"] == 0:
        need(root == auth.vector_empty(doc["context"]), "EMPTY_ROOT")
    return doc


def build(bindings, output, metadata, *, evidence, auth, check, final_check):
    """Write to a fresh empty directory; publish DIRECTORY.json last.

    The caller has already completed the metadata-validating owner export and
    closed its handle. No module loading plan or source state is accepted here.
    The caller also owns ordinary-path/isolation checks and external containment.
    """
    metadata = metadata_checked(metadata)
    need(type(bindings) is dict and callable(check) and callable(final_check), "BUILD_ARGUMENTS")
    power, entries_size, tree_size = shape(len(bindings))
    output = Path(output)
    need(output.is_dir() and not any(output.iterdir()), "EMPTY_OUTPUT_REQUIRED")
    rows = []
    for key, symbol in bindings.items():
        check()
        need(type(key) is bytes and 0 < len(key) <= evidence.DEFAULT_LIMITS.max_bytes, "NAME_KEY")
        name = evidence.strict_json(key)
        need(evidence.name_key(name) == key, "NAME_CANONICAL")
        rows.append(name_digest(key, auth) + bytes.fromhex(hexid(symbol)))
    rows.sort()
    for index in range(1, len(rows)):
        check()
        need(rows[index-1][:32] < rows[index][:32], "DUPLICATE_NAME_DIGEST")
    context = context_id(metadata, auth)
    tree = bytearray(tree_size)
    pad = bytes.fromhex(auth.vector_empty(context))
    for index in range(power):
        check()
        value = bytes.fromhex(auth.node_hash({"kind": "vector-leaf", "context": context,
                  "index": index, "record_id": record_id(rows[index], auth)})) if index < len(rows) else pad
        start = (power-1+index)*32
        tree[start:start+32] = value
    for index in range(power-2, -1, -1):
        check()
        start = (2*index+1)*32
        tree[index*32:index*32+32] = bytes.fromhex(auth.H("NODE", bytes(tree[start:start+32]),
                                                                     bytes(tree[start+32:start+64])))
    root = bytes(tree[:32]).hex()
    doc = {"schema": SCHEMA, "metadata": metadata, "count": len(rows), "context": context,
           "tree_root": root, "vector_commit": auth.vector_commit(context, len(rows), root),
           "entries_bytes": entries_size, "tree_bytes": tree_size, "claims": dict(CLAIMS)}
    raw = evidence.canonical_json(doc)
    expected = hashlib.sha256(raw).hexdigest()
    descriptor_checked(raw, expected, evidence=evidence, auth=auth)
    # No writes occur until the complete bounded map and tree are constructed.
    with (output / "ENTRIES.bin").open("xb") as stream:
        for row in rows:
            check(); need(stream.write(row) == 64, "ENTRY_WRITE")
    with (output / "TREE.bin").open("xb") as stream:
        for start in range(0, len(tree), 1024*1024):
            check(); block = tree[start:start+1024*1024]
            need(stream.write(block) == len(block), "TREE_WRITE")
    need((output / "ENTRIES.bin").stat().st_size == entries_size and
         (output / "TREE.bin").stat().st_size == tree_size, "BUILD_FILE_SIZE")
    final_check(); check()
    with (output / "DIRECTORY.json").open("xb") as stream:
        need(stream.write(raw) == len(raw), "MANIFEST_WRITE")
    return {"directory_manifest_sha256": expected, "directory_manifest": doc,
            "entries": len(rows), "records_bytes": entries_size, "tree_bytes": tree_size}


def lookup_open(manifest_raw, manifest_sha256, entries_reader, tree_reader, names,
                *, evidence, auth, check):
    """Readers accept (offset, length); only final decisions are authenticated.

    They must provide bounded reads of the selected fixed files. File size and
    path validation belong to the wrapper. A corrupted midpoint is allowed to
    misroute binary search, but cannot certify a false hit or false absence.
    """
    doc = descriptor_checked(manifest_raw, manifest_sha256, evidence=evidence, auth=auth)
    need(type(names) is list and 1 <= len(names) <= 8, "QUERY_COUNT")
    need(len(evidence.canonical_json(names)) <= 65536, "QUERY_BYTES")
    keys = [evidence.name_key(name) for name in names]
    need(len(set(keys)) == len(keys), "QUERY_DUPLICATE")
    need(callable(check) and callable(entries_reader) and callable(tree_reader), "QUERY_READERS")
    count, context = doc["count"], doc["context"]
    power, _, _ = shape(count)
    stats = {"entry_reads": 0, "entry_bytes": 0, "tree_reads": 0, "tree_bytes": 0,
             "authenticated_records": 0}

    def row_at(index):
        need(type(index) is int and 0 <= index < count, "INDEX")
        check(); raw = entries_reader(index*64, 64); check()
        need(type(raw) is bytes and len(raw) == 64, "ENTRY_READ")
        stats["entry_reads"] += 1; stats["entry_bytes"] += 64
        return raw

    def verified(index):
        # Authenticate and USE this exact captured row, never a later reread.
        row = row_at(index)
        position, siblings = power-1+index, []
        while position:
            check()
            sibling = position+1 if position % 2 else position-1
            raw = tree_reader(sibling*32, 32); check()
            need(type(raw) is bytes and len(raw) == 32, "TREE_READ")
            stats["tree_reads"] += 1; stats["tree_bytes"] += 32
            siblings.append(raw.hex()); position = (position-1)//2
        auth.verify_vector(context, count, doc["tree_root"], index, record_id(row, auth), siblings)
        stats["authenticated_records"] += 1
        return row

    found, missing = [], []
    for name, key in zip(names, keys):
        check(); target = name_digest(key, auth)
        low, high = 0, count
        while low < high:
            middle = (low+high)//2
            if row_at(middle)[:32] < target:
                low = middle+1
            else:
                high = middle
        right = verified(low) if low < count else None
        if right is not None and right[:32] == target:
            found.append([name, right[32:].hex()])
            continue
        left = verified(low-1) if low else None
        need((right is None or target < right[:32]) and
             (left is None or left[:32] < target), "ABSENCE_INTERVAL")
        # The endpoints are adjacent REAL leaf indices (or an exact array edge).
        # Complete strictly sorted export is the premise that makes this absence.
        missing.append(name)
    check()
    result = {"status": "DIRECTORY_NAMES_MISSING" if missing else "DIRECTORY_QUERY_READY",
              "directory_manifest_sha256": manifest_sha256, "metadata": doc["metadata"],
              "bindings": found, "missing_names": missing, "io": stats,
              "mathematical_acceptance": False, "owner_opened": False,
              "coverage": "SELECTED_HISTORICAL_DIRECTORY_ONLY"}
    if not missing:
        result["specs"] = [{"tag": "type-symbol", "symbol": {
            "kind": "portable-symbol", "symbol_id": symbol}} for _, symbol in found]
    return result
