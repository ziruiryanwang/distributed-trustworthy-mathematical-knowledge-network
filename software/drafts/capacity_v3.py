"""Prospective v3 capacity parsing and local physical-supply observations.

Draft, not installed or qualified. No cryptographic or mathematical authority.
Disk availability is a sample under an owner-supplied-capacity premise, not an
OS reservation. This module neither launches a process nor writes a file.
"""
from pathlib import Path
import os
import re

MIB = 1048576
GIB = 1024 * MIB
MAX_REQUESTS, MAX_STAGES, MAX_RESERVED, MAX_GRANTS = 4096, 256, 64 * GIB, 64
METADATA_PAGES = (8192, 16384, 32768, 65536)
SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")


def require(ok, code):
    if not ok:
        # Delayed only to avoid a capacity/storage module-import cycle. Callers
        # invoke these helpers after the storage module has finished loading.
        from storage import Refusal
        raise Refusal(code)


def integer(value, low, high, code):
    require(type(value) is int and low <= value <= high, code)
    return value


def initial_authorization(limits):
    require(type(limits) is dict, "INITIAL_CAPACITY_FIELDS")
    requests = integer(limits.get("requests"), 1, MAX_REQUESTS, "INITIAL_REQUESTS")
    stages = integer(limits.get("stages"), 1, MAX_STAGES, "INITIAL_STAGES")
    stage_bytes = integer(limits.get("stage_bytes"), MIB, 512 * MIB, "STAGE_GRANT")
    request_bytes = integer(limits.get("request_bytes"), 65536, 16 * MIB, "REQUEST_GRANT")
    reserved = integer(limits.get("staging_bytes"), stage_bytes + request_bytes,
                       MAX_RESERVED, "INITIAL_RESERVED_BYTES")
    pages = limits.get("metadata_pages")
    require(type(pages) is int and pages in METADATA_PAGES, "INITIAL_METADATA_PAGES")
    return {"requests": requests, "stages": stages, "reserved_bytes": reserved,
            "metadata_pages": pages, "grants": 0}


def parse_grant(raw, config_id):
    from storage import decode
    require(type(raw) is bytes and 0 < len(raw) <= 4096, "GRANT_ENVELOPE_BOUND")
    require(type(config_id) is str and re.fullmatch(r"[a-f0-9]{64}", config_id), "CONFIG_ID")
    grant = decode(raw)
    required = {"schema", "op", "grant_id", "config", "add"}
    require(type(grant) is dict and required <= set(grant) <= required | {"metadata_cap_mib"},
            "GRANT_FIELDS")
    require(type(grant["schema"]) is int and grant["schema"] == 1
            and grant["op"] == "renew", "GRANT_SCHEMA")
    require(grant["config"] == config_id, "GRANT_CONFIG")
    require(type(grant["grant_id"]) is str and SAFE_ID.fullmatch(grant["grant_id"]), "GRANT_ID")
    additions = grant["add"]
    require(type(additions) is dict and set(additions) == {"requests", "stages", "reserved_bytes"},
            "GRANT_ADDITION_FIELDS")
    for key, ceiling in (("requests", MAX_REQUESTS), ("stages", MAX_STAGES), ("reserved_bytes", MAX_RESERVED)):
        integer(additions[key], 0, ceiling, "GRANT_ADD:" + key)
    pages = None
    if "metadata_cap_mib" in grant:
        size = grant["metadata_cap_mib"]
        require(type(size) is int and size in (32, 64, 128, 256), "GRANT_METADATA_CAP")
        pages = size * MIB // 4096
    # A provided but nonincreasing cap is rejected against durable state later.
    require(any(additions.values()) or pages is not None, "GRANT_NO_INCREASE")
    return {"grant_id": grant["grant_id"], "add": dict(additions), "metadata_pages": pages}


def existing_parent(value):
    path = Path(value)
    require(path.is_absolute() and len(str(path)) <= 32767, "SUPPLY_ABSOLUTE_PATH")
    path = path.resolve()
    for _ in range(128):
        if path.exists():
            require(path.is_dir(), "SUPPLY_DIRECTORY")
            return path
        require(path.parent != path, "SUPPLY_EXISTING_PARENT")
        path = path.parent
    require(False, "SUPPLY_PATH_DEPTH")


def physical_supply(root, scratch, remaining_bytes, metadata_pages, *, enforce=True):
    """Same-volume NTFS/free-space sample; does not promise future availability."""
    import ctypes as C
    from ctypes import wintypes as W
    require(os.name == "nt", "WINDOWS_STORAGE_PROFILE")
    require(type(enforce) is bool, "SUPPLY_OBSERVATION_MODE")
    integer(remaining_bytes, 0, MAX_RESERVED, "REMAINING_CAPACITY")
    require(type(metadata_pages) is int and metadata_pages in METADATA_PAGES, "METADATA_CAP")
    require(scratch is not None, "SUPPLY_SCRATCH_REQUIRED")
    paths = [existing_parent(value) for value in (root, scratch)]
    kernel = C.WinDLL("kernel32", use_last_error=True)
    kernel.GetVolumePathNameW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD]
    kernel.GetVolumePathNameW.restype = W.BOOL
    kernel.GetVolumeNameForVolumeMountPointW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD]
    kernel.GetVolumeNameForVolumeMountPointW.restype = W.BOOL
    kernel.GetDriveTypeW.argtypes = [W.LPCWSTR]
    kernel.GetDriveTypeW.restype = W.UINT
    kernel.GetVolumeInformationW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD,
        C.POINTER(W.DWORD), C.POINTER(W.DWORD), C.POINTER(W.DWORD), W.LPWSTR, W.DWORD]
    kernel.GetVolumeInformationW.restype = W.BOOL
    kernel.GetDiskFreeSpaceExW.argtypes = [W.LPCWSTR, C.POINTER(C.c_ulonglong),
                                          C.POINTER(C.c_ulonglong), C.POINTER(C.c_ulonglong)]
    kernel.GetDiskFreeSpaceExW.restype = W.BOOL
    volumes = []
    for path in paths:
        mount, name = C.create_unicode_buffer(32768), C.create_unicode_buffer(128)
        require(kernel.GetVolumePathNameW(str(path), mount, len(mount)), "VOLUME_PATH_QUERY")
        require(kernel.GetDriveTypeW(mount.value) == 3, "LOCAL_FIXED_VOLUME_REQUIRED")
        require(kernel.GetVolumeNameForVolumeMountPointW(mount.value, name, len(name)), "VOLUME_ID_QUERY")
        filesystem = C.create_unicode_buffer(64)
        require(kernel.GetVolumeInformationW(mount.value, None, 0, None, None, None,
                                             filesystem, len(filesystem)), "FILESYSTEM_QUERY")
        require(filesystem.value.upper() == "NTFS", "NTFS_STORAGE_REQUIRED")
        volumes.append(name.value.lower())
    require(volumes[0] == volumes[1], "STATE_SCRATCH_VOLUME")
    available, total, free = C.c_ulonglong(), C.c_ulonglong(), C.c_ulonglong()
    require(kernel.GetDiskFreeSpaceExW(volumes[0], C.byref(available), C.byref(total), C.byref(free)),
            "FREE_SPACE_QUERY")
    required = remaining_bytes + 2 * metadata_pages * 4096 + GIB
    sufficient = available.value >= required
    require(not enforce or sufficient, "PHYSICAL_SUPPLY")
    return {"volume": volumes[0], "filesystem": "NTFS", "available_bytes": available.value,
            "required_bytes": required, "remaining_authorized_bytes": remaining_bytes,
            "metadata_pages": metadata_pages, "sufficient": sufficient,
            "sample_only": True, "reserved_by_os": False}
