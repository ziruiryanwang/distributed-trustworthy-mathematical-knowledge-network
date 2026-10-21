"""Fixed closed-generation layout; exact nonrecursive bounded reclamation.

Only the lifecycle manager calls these helpers. Private enrolled roots with no
other writers/restores are required; this is not hostile-owner OS isolation.
Presence is recorded, not every file's old identity or contents. No payload is
hashed and no mathematical acceptance is performed.
"""
from copy import deepcopy
import os
import stat

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from . import codec as P

LAYOUT = "DMKN_V5_CLOSED_GENERATION_LAYOUT_V1"
OWNERSHIP = "PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1"
SCHEMA = "DMKN_V5_GENERATION_RECLAIM_V1"
MAX_ENTRIES = 20 + 9*4096
_BOUND_FIELDS = ("schema", "root", "identities", "marker_sha256", "entry_count",
                 "presence", "profile")
_DATABASES = ("workspace/workspace.sqlite", "workspace/modules/modules.sqlite",
              "workspace/packets/evidence-packets.sqlite", "workspace/index/discovery.sqlite",
              "workspace/placement.sqlite", "workspace/placement-routes.sqlite")


def layout(runs):
    """Deletion order: files, child-before-parent directories, marker, root."""
    F.uint(runs, 0, 4096, "RECLAIM_RUN_BOUND")
    files = [("workspace/owner.lock", "file")]
    for name in _DATABASES:
        files.extend(((name, "file"), (name+"-journal", "file")))
    dirs = [("workspace/operations", "directory"), ("workspace/modules", "directory"),
            ("workspace/packets", "directory"), ("workspace/index", "directory"),
            ("workspace", "directory")]
    for run in range(1, runs+1):
        base = "run-%04d" % run
        files.extend((base+"/location-state/"+name, "file") for name in
                     ("identity.key", "adopted.json", "metadata.sqlite", "metadata.sqlite-journal"))
        files.extend((base+"/location-channel/"+name, "file") for name in
                     ("config.json", "source-map.json"))
        dirs.extend(((base+"/location-state", "directory"),
                     (base+"/location-channel", "directory"), (base, "directory")))
    result = files + dirs + [("generation.json", "file"), ("", "directory")]
    F.need(len(result) == 20+9*runs, "RECLAIM_LAYOUT_CENSUS")
    return result


def profile(value, slot):
    F.fields(value, ("layout", "ownership", "max_calls", "max_entries_per_call",
                     "max_apparent_bytes"))
    F.need(value["layout"] == LAYOUT and value["ownership"] == OWNERSHIP,
           "RECLAIM_LAYOUT_OR_OWNERSHIP")
    F.uint(value["max_calls"], 1, 8192, "RECLAIM_CALL_BOUND")
    F.uint(value["max_entries_per_call"], 1, MAX_ENTRIES, "RECLAIM_WINDOW_BOUND")
    F.uint(value["max_apparent_bytes"], 1, slot["reserved_bytes"], "RECLAIM_BYTE_BOUND")
    return deepcopy(value)


def _identity(info):
    return [F.uint(info.st_dev, 1, 2**128-1, "RECLAIM_FILESYSTEM_IDENTITY"),
            F.uint(info.st_ino, 1, 2**128-1, "RECLAIM_FILESYSTEM_IDENTITY")]


def _info(path, kind):
    info = path.lstat()
    F.need(not stat.S_ISLNK(info.st_mode)
           and not getattr(info, "st_file_attributes", 0) & 0x400, "RECLAIM_LINK_OR_REPARSE")
    F.need(stat.S_ISDIR(info.st_mode) if kind == "directory" else stat.S_ISREG(info.st_mode),
           "RECLAIM_ENTRY_KIND")
    if kind == "file":
        F.need(info.st_nlink == 1, "RECLAIM_HARDLINK_ALIAS")
        F.uint(info.st_size, 0, 2**50, "RECLAIM_FILE_SIZE")
    return info


def _path(root, relative):
    result = root.joinpath(*relative.split("/")) if relative else root
    F.need(result.is_absolute() and (result == root or result.is_relative_to(root)),
           "RECLAIM_EXACT_TARGET")
    return result


def _small(path, expected):
    info = _info(path, "file")
    F.need(info.st_size == len(expected) <= 131072, "RECLAIM_MARKER_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(len(expected)+1)
    F.need(raw == expected, "RECLAIM_MARKER_BINDING")


def _parents(manager, record, identities, guard):
    guard()
    parent = ordinary(manager.root)
    slot = ordinary(parent/("slot-%d" % record["slot"]))
    actual = [_identity(_info(parent, "directory")), _identity(_info(slot, "directory"))]
    if identities is not None:
        F.need(actual == identities[:2], "RECLAIM_PARENT_IDENTITY_CHANGED")
    _small(parent/"manager.json", manager._marker)
    root = manager.generation_path(record)
    F.need(root.parent == slot and root.name == "g%020d" % record["sequence"],
           "RECLAIM_DERIVED_ROOT")
    # At most one enrolled generation may occupy this exact slot. Unknown
    # siblings are preserved; do not descend into or classify them as trash.
    with os.scandir(slot) as entries:
        count = 0
        for entry in entries:
            guard(); count += 1
            F.need(count <= 1 and entry.name == root.name, "RECLAIM_UNEXPECTED_SLOT_ENTRY")
    return root, actual


def _bits(flags):
    raw = bytearray((len(flags)+7)//8)
    for index, present in enumerate(flags):
        if present: raw[index//8] |= 1 << (index % 8)
    return bytes(raw).hex()


def _flags(value, count):
    F.need(type(value) is str and len(value) == 2*((count+7)//8)
           and all(c in "0123456789abcdef" for c in value), "RECLAIM_BITMAP_ENCODING")
    raw = bytes.fromhex(value)
    flags = [bool(raw[i//8] & (1 << (i % 8))) for i in range(count)]
    F.need(_bits(flags) == value, "RECLAIM_BITMAP_PADDING")
    return flags


def _binding(facet):
    return F.digest("DMKN-V5-RECLAIM-BINDING-V1", {key: facet[key] for key in _BOUND_FIELDS})


def validate(manager, record):
    """Bounded durable syntax/binding checks; no filesystem authority by itself."""
    facet = record["reclaim"]
    F.fields(facet, (*_BOUND_FIELDS, "binding_sha256", "cursor", "window_end", "calls", "failure"))
    F.need(facet["schema"] == SCHEMA and facet["root"] == str(manager.generation_path(record)),
           "RECLAIM_STORED_ROOT")
    F.need(type(facet["identities"]) is list and len(facet["identities"]) == 3,
           "RECLAIM_STORED_IDENTITIES")
    for pair in facet["identities"]:
        F.need(type(pair) is list and len(pair) == 2, "RECLAIM_STORED_IDENTITY")
        for value in pair: F.uint(value, 1, 2**128-1, "RECLAIM_FILESYSTEM_IDENTITY")
    F.need(facet["marker_sha256"] == P.digest(manager._generation_marker(record)),
           "RECLAIM_STORED_MARKER")
    count = 20+9*record["runs"]
    F.need(type(facet["entry_count"]) is int and facet["entry_count"] == count,
           "RECLAIM_STORED_CENSUS")
    flags = _flags(facet["presence"], count)
    F.need(flags[-1] and flags[-2], "RECLAIM_ORIGINAL_MARKER_AND_ROOT")
    selected = profile(facet["profile"], manager.config["slots"][record["slot"]])
    F.uint(facet["calls"], 0, selected["max_calls"], "RECLAIM_STORED_CALLS")
    F.uint(facet["cursor"], 0, count, "RECLAIM_STORED_CURSOR")
    F.uint(facet["window_end"], facet["cursor"], count, "RECLAIM_STORED_WINDOW")
    F.need(facet["window_end"]-facet["cursor"] <= selected["max_entries_per_call"]
           and (facet["calls"] > 0 or facet["cursor"] == facet["window_end"] == 0),
           "RECLAIM_STORED_WINDOW_CHARGE")
    F.need(facet["failure"] in (None, "RECLAIM_STEP_INCOMPLETE"), "RECLAIM_STORED_FAILURE")
    F.need(facet["binding_sha256"] == _binding(facet), "RECLAIM_STORED_BINDING")
    F.need(len(F.compact(facet)) <= manager.config["cleanup_reserved_bytes"],
           "RECLAIM_METADATA_ALLOCATION")
    return flags


def census(manager, record, selected, guard, identities=None):
    """One nonrecursive finite layout walk. Unknown entries stop before descent.

    All known directories are enumerated at most once; file contents are never
    opened except the exact small manager/generation markers. The size sum is
    apparent regular-file bytes, not a physical storage quota.
    """
    items = layout(record["runs"])
    flags = [False]*len(items)
    root, parent_ids = _parents(manager, record, identities, guard)
    if not os.path.lexists(root):
        return {"flags": flags, "identities": None, "apparent_bytes": 0}
    ordinary(root)
    root_id = _identity(_info(root, "directory"))
    if identities is not None:
        F.need(root_id == identities[2], "RECLAIM_ROOT_IDENTITY_CHANGED")
    flags[-1] = True
    children = {}
    for index, (relative, kind) in enumerate(items[:-1]):
        guard()
        parent, name = relative.rsplit("/", 1) if "/" in relative else ("", relative)
        children.setdefault(parent, {})[name] = (index, relative, kind)
    queue, apparent = [""], 0
    while queue:
        relative = queue.pop()
        allowed = children.get(relative, {})
        with os.scandir(_path(root, relative)) as entries:
            count = 0
            for entry in entries:
                guard(); count += 1
                F.need(count <= len(allowed) and entry.name in allowed, "RECLAIM_UNKNOWN_ENTRY")
                index, name, kind = allowed[entry.name]
                info = _info(_path(root, name), kind)
                flags[index] = True
                if kind == "directory": queue.append(name)
                else:
                    apparent += info.st_size
                    F.need(apparent <= selected["max_apparent_bytes"], "RECLAIM_APPARENT_BYTE_CAP")
    if flags[-2]: _small(root/"generation.json", manager._generation_marker(record))
    return {"flags": flags, "identities": parent_ids+[root_id], "apparent_bytes": apparent}


def initial(manager, record, selected, guard):
    observed = census(manager, record, selected, guard)
    F.need(observed["flags"][-1] and observed["flags"][-2], "RECLAIM_INITIAL_MARKER_REQUIRED")
    facet = {"schema": SCHEMA, "root": str(manager.generation_path(record)),
        "identities": observed["identities"], "marker_sha256": P.digest(manager._generation_marker(record)),
        "entry_count": len(observed["flags"]), "presence": _bits(observed["flags"]),
        "profile": selected, "cursor": 0, "window_end": 0, "calls": 0, "failure": None}
    facet["binding_sha256"] = _binding(facet)
    return facet


def reconcile(original, current, cursor, end):
    """Only the previously prepaid window may have lost a present-entry prefix."""
    F.need(len(current) == len(original), "RECLAIM_CENSUS_CHANGED")
    effective, unfinished = cursor, False
    for index, (was, now) in enumerate(zip(original, current)):
        F.need(not now or was, "RECLAIM_UNENROLLED_ENTRY")
        if index < cursor:
            F.need(not now, "RECLAIM_DELETED_ENTRY_REAPPEARED")
        elif index >= end:
            F.need(now == was, "RECLAIM_UNPREPAID_ABSENCE")
        else:
            if was and now: unfinished = True
            if was and not now:
                F.need(not unfinished, "RECLAIM_NONPREFIX_ABSENCE")
            if not unfinished: effective = index+1
    return effective


def execute(manager, record, start, end, guard):
    """Apply an already durable exact window; never recursively delete."""
    facet = record["reclaim"]
    original = validate(manager, record)
    items = layout(record["runs"])
    F.need(facet["cursor"] == start and facet["window_end"] == end and facet["calls"] > 0,
           "RECLAIM_WINDOW_NOT_CHARGED")
    for index in range(start, end):
        guard()
        if not original[index]: continue
        root, unused = _parents(manager, record, facet["identities"], guard)
        F.need(_identity(_info(ordinary(root), "directory")) == facet["identities"][2],
               "RECLAIM_ROOT_IDENTITY_CHANGED")
        relative, kind = items[index]
        target = _path(root, relative)
        ordinary(target, directory=kind == "directory")
        _info(target, kind)
        if relative == "generation.json":
            _small(target, manager._generation_marker(record))
            with os.scandir(root) as remaining:
                count = 0
                for entry in remaining:
                    guard(); count += 1
                    F.need(count == 1 and entry.name == "generation.json", "RECLAIM_MARKER_NOT_LAST_CHILD")
        guard()
        if kind == "file": os.unlink(target)
        else: os.rmdir(target)
        F.need(not os.path.lexists(target), "RECLAIM_EFFECT_ABSENCE_UNCERTAIN")


def absent(manager, record, guard):
    root, unused = _parents(manager, record, record["reclaim"]["identities"], guard)
    F.need(not os.path.lexists(root), "RECLAIM_ROOT_NOT_ABSENT")
