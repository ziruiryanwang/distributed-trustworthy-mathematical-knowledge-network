"""Root-selected actual owner request preparation, no Lean or acceptance event.

This fixed local adapter uses the independently adopted recovery context. Its
one-time file-to-unit lookup assembly is experiment setup, not a global search
algorithm or permission to adopt a foreign database. Existing catalogs stay
read-only; the generic owner_request API uses selected point lookups.
"""
from pathlib import Path
import hashlib
import json
import os
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import owner_request as P

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
ORIGIN = LOCAL / "ordinary-native-admission-01"
RECOVERY = LOCAL / "ordinary-native-recovery-01"
STORE = RECOVERY / "native-recovery/catalog"
CONTEXT = "4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026"
PROFILE = "fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219"
BASIS = "cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299"
DB_SHA = "bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9"
ORIGIN_MANIFEST = LOCAL / "ordinary-native-recovery-01-inputs/RECOVERY-MANIFEST.json"
MANIFEST_SHA = "4af119ba2ae759634529f01093555ba45bdf420307ab057f61b2085f16f23bef"


def need(ok, code):
    if not ok:
        raise ValueError(code)


def pin_read(path, expected, maximum):
    need(path.is_absolute() and path.resolve() == path and path.is_file() and
         path.stat().st_size <= maximum, "FIXED_INPUT_PATH_OR_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == expected, "FIXED_INPUT_PIN")
    return raw


def name(*parts):
    return [[0, {"$bytes": list(part.encode())}] for part in parts]


def write_new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    output = Path(sys.argv[1])
    source = Path(__file__).resolve().parent
    need(Path.cwd() == ROOT and source.parents[2] == output / "sources" and
         output.is_relative_to(LOCAL) and len(sys.argv) == 2, "SELECTED_PREPARATION_INVOCATION")
    need(not (STORE / "WITHDRAWN").exists(), "ADOPTED_LOCAL_CONTEXT_WITHDRAWN")
    db = STORE / "catalog.sqlite"
    pin_read(db, DB_SHA, 16 * 1024**2)
    # This exact locally protected DB was adopted with real worker events by
    # the root. No peer database or success report is a substitute for that fact.
    connection = sqlite3.connect(db.as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        records = {key: E.strict_json(raw) for key, raw in
                   connection.execute("SELECT id, record FROM roots")}
        need(len(records) == 4, "ADOPTED_ROOT_CENSUS")
    finally:
        connection.close()
    reverse, seen, current = [], set(), CONTEXT
    while current:
        need(current in records and current not in seen, "ADOPTED_PARENT_CHAIN")
        seen.add(current)
        row = records[current]
        need(row["root"] == current and row["profile_id"] == PROFILE, "ADOPTED_ROOT_BINDING")
        reverse.append(row)
        current = row["parent"]
    need(len(reverse) == 4 and reverse[-1]["root"] == BASIS, "ADOPTED_BASIS")
    bindings = {}
    for row in reversed(reverse):
        artifact = STORE / "operations" / row["operation"] / "chunk.olean"
        raw = pin_read(artifact, row["artifact_sha256"], 64 * 1024**2)
        need(len(raw) == row["artifact_bytes"], "ADOPTED_ARTIFACT_SIZE")
        del raw
        for n, symbol in row["bindings"]:
            key = E.name_key(n)
            need(key not in bindings, "ADOPTED_BINDING_OVERWRITE")
            bindings[key] = E._hex(symbol)
    need(len(bindings) == 3622, "ADOPTED_BINDING_CENSUS")
    manifest = json.loads(pin_read(ORIGIN_MANIFEST, MANIFEST_SHA, 2 * 1024**2))
    # Setup only: one bounded inventory of the existing numbered evidence files.
    # Do not claim this fixture map is an installed persistent object index.
    locations, input_bytes = {}, 0
    for index in range(2852):
        relative = f"native-admission/evidence/{index:05d}.json"
        selected = manifest["files"][relative]
        path = ORIGIN / relative
        raw = pin_read(path, selected["sha256"], E.DEFAULT_LIMITS.max_bytes)
        need(len(raw) == selected["bytes"], "ORIGIN_EVIDENCE_SIZE")
        input_bytes += len(raw)
        need(input_bytes <= 64 * 1024**2, "ORIGIN_EVIDENCE_TOTAL")
        # Exact previously validated bytes only. Selected fetches below re-enter
        # the unchanged strict evidence validator in owner_request.prepare.
        doc = json.loads(raw)
        need(doc["profile_id"] == PROFILE and doc["schema"] == E.SCHEMA, "ORIGIN_EVIDENCE_PROFILE")
        unit_id = hashlib.sha256(E.EVIDENCE_DOMAIN.encode() + b"\0" + raw).hexdigest()
        for row in doc["unit"][2]:
            key = E.name_key(row[0])
            symbol = E.export_id(PROFILE, unit_id, row[0])
            need(key not in locations and bindings.get(key) == symbol, "ORIGIN_ACCEPTED_EVIDENCE_BINDING")
            locations[key] = (path, selected["sha256"], symbol)
        del raw, doc

    requested = [name("DMKN", "ReadFootprint", part)
                 for part in ("ReadsOnly", "Avoids", "readsOnly_insertMany")]
    targets = [[n, bindings[E.name_key(n)]] for n in requested]
    prefix = name("DMKN", "ReadFootprint")

    def fetch(n, symbol):
        path, digest, expected = locations[E.name_key(n)]
        need(symbol == expected, "SELECTED_EVIDENCE_SYMBOL")
        return pin_read(path, digest, E.DEFAULT_LIMITS.max_bytes)

    prepared = P.prepare(profile_id=PROFILE, context_id=CONTEXT, basis_id=BASIS,
        inventory_raw=pin_read(ROOT / "software/assets/foundation/seed-inventory-json.json",
                               P.INVENTORY, 1024**2),
        targets=targets, warranted_symbol=lambda n: bindings.get(E.name_key(n)),
        fetch_evidence=fetch, owner_absent=lambda n: n[:2] == prefix)
    need(prepared.materialized_units <= 1024, "OWNER_CHECKED_UNIT_BUDGET")
    request = output / "owner-request"
    request.mkdir()
    write_new(request / "header.json", prepared.header)
    for index, raw in enumerate(prepared.groups):
        write_new(request / f"group-{index:05d}.json", raw)
    pin_read(db, DB_SHA, 16 * 1024**2)
    need(not (STORE / "WITHDRAWN").exists(), "ADOPTED_LOCAL_CONTEXT_WITHDRAWN")
    result = {"status": "PASS_ACTUAL_REQUEST_PREPARATION_NOT_OWNER_USE", "profile_id": PROFILE,
        "context_id": CONTEXT, "targets": targets, "groups": len(prepared.groups),
        "materialized_units": prepared.materialized_units,
        "payload_bytes": prepared.payload_bytes, "selected_evidence_bytes": prepared.acquired_bytes,
        "selected_evidence_nodes": prepared.acquired_nodes, "setup_index_bytes": input_bytes,
        "request_files": {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                  "bytes": p.stat().st_size} for p in sorted(request.iterdir())},
        "claims": "ROOT_ADOPTED_LOCAL_CONTEXT_AND_SELECTED_SEMANTICS_NOT_SEARCH_OR_MATH_ACCEPTANCE",
        "owner_presence_hint": "KNOWN_FIXTURE_IMPORTS_STD_NOT_DMKN_READFOOTPRINT_CHECK_ACTUAL_IN_LEAN"}
    write_new(output / "PREPARE-RESULT.json", json.dumps(result, indent=2).encode())
    print(json.dumps({k: v for k, v in result.items() if k != "request_files"}), flush=True)


if __name__ == "__main__":
    main()
