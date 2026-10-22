"""Read-only pre-open metadata gates for the managed apparent-stream profile.

Identity/lineage comes from the fresh manager and its trusted writer binding,
not from file lengths. No database is opened, repaired, deleted or migrated.
Private ordinary paths, no concurrent writers/restores and the pinned runtime
remain caller premises. These checks do not reserve physical free disk.
"""
import os
from pathlib import Path
import stat

from discovery import formal_features as F
from . import storage_profile as SP


def _ordinary(path, *, fresh=False, directory=False):
    # Lazy import: discovery_store itself uses these guards before connecting.
    from discovery.discovery_store import ordinary
    return ordinary(path, fresh=fresh, directory=directory)


def _file(path, maximum, *, minimum=0):
    path = _ordinary(path)
    info = path.lstat()
    F.need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
           "MANAGED_STORAGE_FILE_OR_ALIAS")
    F.uint(info.st_size, minimum, maximum, "MANAGED_STORAGE_FILE_BOUND")
    return info.st_size


def preopen_lock(path, *, create):
    """A fresh lock is absent; an enrolled lock is exactly one ordinary byte."""
    F.need(type(create) is bool, "MANAGED_STORAGE_CREATE_FLAG")
    if create:
        _ordinary(path, fresh=True)
    else:
        _file(path, 1, minimum=1)


def preopen_database(path, *, max_pages, create):
    """Check main/journal before sqlite connect can perform recovery.

    The managed caller must have checked profile lineage and closed directory
    grammar first. A direct nonmanaged caller gets only these metadata guards.
    """
    F.need(type(create) is bool, "MANAGED_STORAGE_CREATE_FLAG")
    bound = SP.database_envelope(max_pages)
    path = _ordinary(path, fresh=create)
    if not create:
        _file(path, bound["main_bytes"])
    journal = Path(str(path)+"-journal")
    if create:
        F.need(not os.path.lexists(journal), "MANAGED_STORAGE_FRESH_JOURNAL")
    elif os.path.lexists(journal):
        _file(journal, bound["journal_bytes"])
    for suffix in ("-wal", "-shm"):
        F.need(not os.path.lexists(str(path)+suffix), "MANAGED_STORAGE_UNSUPPORTED_SIDECAR")
    return path


def _scan(root, files, directories, *, guard):
    """Bounded metadata-only traversal; never follow or enumerate unknown dirs."""
    root = _ordinary(root, directory=True)
    F.need("" in directories and not set(files) & set(directories),
           "MANAGED_STORAGE_INTERNAL_LAYOUT")
    pending, observed = [""], 0
    limit = len(files)+len(directories)-1
    while pending:
        relative = pending.pop()
        guard()
        parent = root.joinpath(*relative.split("/")) if relative else root
        _ordinary(parent, directory=True)
        with os.scandir(parent) as entries:
            for entry in entries:
                guard(); observed += 1
                F.need(observed <= limit, "MANAGED_STORAGE_LAYOUT_BOUND")
                name = relative+"/"+entry.name if relative else entry.name
                F.need(name in files or name in directories, "MANAGED_STORAGE_UNEXPECTED_ENTRY")
                path = root.joinpath(*name.split("/"))
                if name in files:
                    minimum, maximum = files[name]
                    _file(path, maximum, minimum=minimum)
                else:
                    _ordinary(path, directory=True)
                    pending.append(name)
    return observed


def registry_preopen(root, expected_marker, *, max_pages):
    """Authenticate enrollment before lock mutation or writable registry open.

    Slot subdirectories are not traversed here: registry configuration is
    needed to interpret their generation identities. The selected generation
    is checked separately before any of its writers open.
    """
    F.need(type(expected_marker) is bytes and 0 < len(expected_marker) <= 131072,
           "MANAGED_STORAGE_MARKER_ARGUMENT")
    root = _ordinary(root, directory=True)
    allowed = {"manager.json", "owner.lock", "generations.sqlite",
               "generations.sqlite-journal", "slot-0", "slot-1"}
    present = set()
    with os.scandir(root) as entries:
        for entry in entries:
            F.need(entry.name in allowed and entry.name not in present,
                   "MANAGED_STORAGE_REGISTRY_ENTRY")
            present.add(entry.name)
    F.need(allowed-{ "generations.sqlite-journal" } <= present,
           "MANAGED_STORAGE_REGISTRY_MISSING")
    marker = root/"manager.json"
    _file(marker, len(expected_marker), minimum=len(expected_marker))
    with marker.open("rb") as stream:
        F.need(stream.read(len(expected_marker)+1) == expected_marker,
               "MANAGED_STORAGE_REGISTRY_LINEAGE")
    preopen_lock(root/"owner.lock", create=False)
    for slot in ("slot-0", "slot-1"):
        _ordinary(root/slot, directory=True)
    preopen_database(root/"generations.sqlite", max_pages=max_pages, create=False)


def generation_preopen(root, config, runs, *, guard):
    """Check only this generation's fixed layout before any store can recover.

    Caller first checks the manager-derived generation marker and writer
    profile, and validates the full config. Missing files remain missing;
    actual create/reopen code decides which are required. Empty operations is
    enforced by the closed grammar, so host custody cannot grow proof outputs.
    """
    F.uint(runs, 0, 4096, "MANAGED_STORAGE_USED_RUNS")
    maximum = F.uint(config["placement"]["max_runs"], 1, 4096,
                     "MANAGED_STORAGE_CONFIGURED_RUNS")
    F.need(runs <= maximum, "MANAGED_STORAGE_USED_RUNS")
    metadata = SP.node_metadata(config["location"]["limits"]["metadata"])
    files = {"generation.json": (1, 131072), "workspace/owner.lock": (1, 1)}
    directories = {"", "workspace", "workspace/operations", "workspace/modules",
                   "workspace/packets", "workspace/index"}

    def database(name, pages):
        bound = SP.database_envelope(pages)
        files[name] = (0, bound["main_bytes"])
        files[name+"-journal"] = (0, bound["journal_bytes"])

    database("workspace/workspace.sqlite", config["workspace"]["ledger_pages"])
    database("workspace/modules/modules.sqlite", config["workspace"]["module_limits"]["db_pages"])
    database("workspace/packets/evidence-packets.sqlite", config["workspace"]["packet_limits"]["db_pages"])
    database("workspace/index/discovery.sqlite", config["workspace"]["index_limits"]["max_db_pages"])
    database("workspace/placement.sqlite", config["placement"]["ledger_pages"])
    database("workspace/placement-routes.sqlite", config["service_limits"]["journal_pages"])
    for run in range(1, runs+1):
        guard()
        base = "run-%04d" % run
        directories.update((base, base+"/location-state", base+"/location-channel"))
        database(base+"/location-state/metadata.sqlite", metadata["pages"])
        for name in ("identity.key", "adopted.json"):
            files[base+"/location-state/"+name] = (1, 1024)
        for name in ("config.json", "source-map.json"):
            files[base+"/location-channel/"+name] = (1, 16384)
    F.need(len(files) == 14+6*runs and len(directories) == 6+3*runs,
           "MANAGED_STORAGE_INTERNAL_CENSUS")
    return {"scope": "METADATA_ONLY_NOT_LINEAGE_AUTHORITY",
            "observed_entries": _scan(root, files, directories, guard=guard),
            "possible_entries": len(files)+len(directories),
            "physical_envelope_adopted": False}
