"""Immutable reader1 custody inputs for the selected actual02 continuation.

No report flag, database row or stored judgment confers mathematical authority.
The fresh consumer still verifies one actual receipt and both native deltas.
"""
from pathlib import Path
import sqlite3

from delta import network_actual02 as N

ROOT = N.ROOT / "experiments/v5-local-checks/delta-network-actual-02/evidence"
PATHS = {"recipient_result":ROOT/"reader1-result.json",
         "packet_db":ROOT/"reader1-packets/delta-packets.sqlite",
         "module_db":ROOT/"reader1-modules/modules.sqlite"}


def pins(value):
    N.fields(value, tuple(PATHS))
    for key, path in PATHS.items():
        N.require(N.pin_fields(value[key],32*N.MIB) == path, "CONTINUATION_EXACT_RETAINED_SOURCE")
        for item in (path,*path.parents):
            N.require(not item.is_symlink() and not item.is_junction(), "CONTINUATION_RETAINED_NO_LINKS")
        N.read_pin(value[key],32*N.MIB)
        if key.endswith("_db"):
            N.require(all(not Path(str(path)+suffix).exists() for suffix in ("-wal","-shm","-journal")),
                      "CONTINUATION_CLOSED_DATABASE_REQUIRED")


def _read_db(row, queries, active):
    path = N.pin_fields(row,32*N.MIB)
    db = sqlite3.connect(path.as_uri()+"?mode=ro&immutable=1",uri=True,timeout=1)
    work = 0
    def progress():
        nonlocal work
        work += 1000
        if work > 200000: return 1
        try: active(); return 0
        except BaseException: return 1
    try:
        db.execute("PRAGMA query_only=ON"); db.execute("PRAGMA trusted_schema=OFF")
        db.set_progress_handler(progress,1000)
        return [db.execute(sql,args).fetchall() for sql,args in queries]
    finally: db.close()


def load(value, active):
    """Read finite exact preserved bytes, never open the predecessor store writable."""
    pins(value); active()
    report = N.parse(N.read_pin(value["recipient_result"],4*N.MIB))
    # These are lineage/selection bindings, not accepting flags or live handles.
    N.require(report["name"] == "reader1", "CONTINUATION_RECIPIENT_LINEAGE")
    entry = report["packet"]; N.fields(entry,("packet_sha256","packet_bytes"))
    N.digest(entry["packet_sha256"]); N.uint(entry["packet_bytes"],16*N.MIB,1)
    N.digest(report["module"]); module = report["module"]
    rows, offers = _read_db(value["packet_db"],[
        ("SELECT digest,size,module,blob FROM packets LIMIT 2",()),
        ("SELECT module,profile,digest FROM offers LIMIT 2",())],active)
    N.require(len(rows) == 1 and len(offers) == 1, "CONTINUATION_SINGLE_RECEIVED_PACKET")
    digest_value,size,stored_module,raw = rows[0]; raw = bytes(raw)
    N.require(digest_value == entry["packet_sha256"] and size == entry["packet_bytes"]
              and stored_module == module and len(raw) == size and N.sha(raw) == digest_value,
              "CONTINUATION_RETAINED_PACKET_BINDING")
    N.require(offers[0] == (module,report["acquired"]["wire_profile_id"],digest_value)
              and report["acquired"]["packet_sha256"] == digest_value
              and report["acquired"]["packet_bytes"] == size
              and report["acquired"]["module_id"] == module,
              "CONTINUATION_RETAINED_OFFER_LINEAGE")
    N.parse_packet(raw,N.Envelope())
    packet = N.C.parse_json(raw)
    N.require(len(packet["frontiers"]) == 1 and len(packet["deltas"]) == 2
              and N.C.module_id(packet["deltas"][-1]["local_spec"]) == module,
              "CONTINUATION_PACKET_TARGET")
    group_rows,body_rows = _read_db(value["module_db"],[
        ("SELECT module,idx,opening FROM groups ORDER BY module,idx LIMIT 129",()),
        ("SELECT module,universes,hash,expression FROM bodies ORDER BY module,universes,hash LIMIT 257",())],active)
    N.require(0 < len(group_rows) <= 128 and 0 < len(body_rows) <= 256,
              "CONTINUATION_RETAINED_SEMANTICS_BOUND")
    groups = {(owner,index):bytes(opening) for owner,index,opening in group_rows}
    bodies = {(owner,arity,h):bytes(expr) for owner,arity,h,expr in body_rows}
    N.require(len(groups) == len(group_rows) and len(bodies) == len(body_rows),
              "CONTINUATION_RETAINED_SEMANTIC_UNIQUENESS")
    active(); pins(value)
    return {"packet":raw,"module":module,"entry":entry,"record":report["record"],
            "wire_profile_id":report["acquired"]["wire_profile_id"],
            "groups":groups,"bodies":bodies,"pins":value}


def populate(retained, modules, packets, adapter, active):
    """Reconstitute fresh custody and compare every persisted semantic object."""
    raw,module = retained["packet"],retained["module"]
    packets.put(module,raw,before_commit=active)
    groups,bodies,census = N.semantic_material(raw,modules,active)
    N.require({key:N.C.canonical(value) for key,value in groups.items()} == retained["groups"],
              "CONTINUATION_ALL_RETAINED_GROUPS_MATCH_PACKET")
    N.require({key:N.C.canonical(value["expression"]) for key,value in bodies.items()} == retained["bodies"],
              "CONTINUATION_ALL_RETAINED_BODIES_MATCH_PACKET")
    N.require(packets.profile_id == retained["wire_profile_id"],
              "CONTINUATION_PACKET_PROFILE")
    locator = retained["record"]["locator"]
    N.require(locator["module_id"] == module,"CONTINUATION_EXPORT_TARGET")
    opening,unused = modules.get_group(module,locator["relative_name"],locator["group_index"])
    exported = adapter.encode_opening(module,locator["relative_name"],opening)
    N.require(adapter.extract(exported) == retained["record"],"CONTINUATION_RETAINED_EXPORT_BINDING")
    N.require(packets.get(retained["entry"]["packet_sha256"],retained["entry"]["packet_bytes"]) == raw,
              "CONTINUATION_PACKET_READBACK")
    active()
    return exported,{**census,"origin":"PINNED_READER1_IMMUTABLE_CUSTODY_ONLY",
                     "all_retained_groups_matched":True,"all_retained_bodies_matched":True}
