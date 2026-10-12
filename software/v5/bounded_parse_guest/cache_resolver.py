"""Pure locked-archive selection for the bounded guest resolver successor.

Cargo can read dependency manifests that do not produce compilation units.
Select every available locked archive, not merely the compiled-unit archives.
The explicit forty unavailable versions remain outside this retained target's
observed resolution closure; this is NOT availability of the complete lock set.
No filesystem access, import of project code, or subprocess occurs here.
"""
from __future__ import annotations

import re
import tomllib

REGISTRY = "registry+https://github.com/rust-lang/crates.io-index"
REGISTRY_DIR = "index.crates.io-1949cf8c6b5b557f"
# Every added archive is lock-checksum-bound below, not trusted from this table.
EXTRA_ARCHIVES = {
    "ark-r1cs-std@0.5.0": 103859,
    "bit-vec@0.8.0": 24132,
    "embedded-io@0.4.0": 12901,
    "embedded-io@0.6.1": 13133,
    "getopts@0.2.23": 21409,
    "proptest@1.11.0": 207859,
    "rand_chacha@0.9.0": 18258,
    "rand_xorshift@0.4.0": 10262,
    "rand@0.9.5": 100216,
    "rustc_version@0.4.1": 12245,
    "unarray@0.1.4": 12895,
    "unicode-width@0.2.1": 279344,
    "valuable@0.1.1": 28679,
    "adler2@2.0.1": 13366,
    "fnv@1.0.7": 11266,
    "memchr@2.7.5": 97603,
    "miniz_oxide@0.8.9": 67132,
    "rand_core@0.9.3": 24543,
    "windows_x86_64_msvc@0.52.6": 832564,
    "windows-targets@0.52.6": 6403,
}
MISSING_LOCKED_VERSIONS = frozenset((
    "addr2line@0.25.0", "bitflags@1.3.2", "block@0.1.6", "cc@1.2.0",
    "core-foundation@0.9.4", "core-foundation-sys@0.8.7", "core-graphics-types@0.1.3",
    "dlmalloc@0.2.9", "errno@0.3.14", "foreign-types@0.5.0",
    "foreign-types-macros@0.2.4", "foreign-types-shared@0.3.1", "fortanix-sgx-abi@0.5.0",
    "gimli@0.32.0", "hermit-abi@0.5.2", "libredox@0.1.25", "linux-raw-sys@0.12.1",
    "malloc_buf@0.0.6", "metal@0.29.0", "objc@0.2.7", "object@0.37.1",
    "rand@0.9.1", "redox_users@0.5.3", "r-efi@5.3.0", "r-efi@6.0.0",
    "r-efi-alloc@2.1.0", "rustix@1.1.5", "unwinding@0.2.7",
    "wasi@0.11.1+wasi-snapshot-preview1", "wasip2@1.0.4+wasi-0.2.12",
    "windows_aarch64_gnullvm@0.52.6", "windows_aarch64_msvc@0.52.6",
    "windows_i686_gnu@0.52.6", "windows_i686_gnullvm@0.52.6",
    "windows_i686_msvc@0.52.6", "windows_x86_64_gnu@0.52.6",
    "windows_x86_64_gnullvm@0.52.6", "windows-sys@0.59.0",
    "wit-bindgen@0.57.1", "zerocopy-derive@0.8.59",
))


def need(value, reason):
    if not value:
        raise ValueError(reason)


def index_path(name):
    need(re.fullmatch(r"[a-z0-9_-]+", name), "CRATE_NAME")
    if len(name) == 1:
        return "1/" + name
    if len(name) == 2:
        return "2/" + name
    if len(name) == 3:
        return "3/" + name[0] + "/" + name
    return name[:2] + "/" + name[2:4] + "/" + name


def cache_inputs(old_graph, project_lock_bytes, std_lock_bytes, retained_seed_map):
    """Return (exact file pins, explanation); caller also validates full graph."""
    need(type(old_graph) is dict and set(old_graph) == {"version", "roots", "units"}
         and old_graph["version"] == 1 and type(old_graph["units"]) is list
         and len(old_graph["units"]) == 297, "EXACT_RETAINED_GRAPH")
    need(type(retained_seed_map) is dict, "RETAINED_SEED_MAP")
    versions = {}
    for raw in (project_lock_bytes, std_lock_bytes):
        need(type(raw) is bytes and len(raw) <= 1024**2, "LOCK_BOUND")
        lock = tomllib.loads(raw.decode("utf-8"))
        need(lock["version"] == 4 and type(lock["package"]) is list, "LOCK_SCHEMA")
        seen = set()
        for row in lock["package"]:
            name, version = row["name"], row["version"]
            need(type(name) is str and re.fullmatch(r"[a-z0-9_-]+", name)
                 and type(version) is str and re.fullmatch(r"[0-9A-Za-z.+_-]+", version),
                 "SAFE_LOCK_PACKAGE")
            key = name + "@" + version
            need(key not in seen, "DUPLICATE_LOCK_PACKAGE")
            seen.add(key)
            if "source" not in row:
                continue
            need(row["source"] == REGISTRY and re.fullmatch(r"[0-9a-f]{64}", row["checksum"]),
                 "ONLY_PINNED_REGISTRY_PACKAGES")
            need(key not in versions or versions[key] == row["checksum"], "LOCK_CHECKSUM_CONFLICT")
            versions[key] = row["checksum"]
    names = {key.split("@")[0] for key in versions}
    need(len(versions) == 220 and len(names) == 198, "EXACT_LOCK_UNION")
    compiled = set()
    for unit in old_graph["units"]:
        package = unit["pkg_id"]
        if package.startswith(REGISTRY + "#"):
            key = package[len(REGISTRY) + 1:]
            need(key in versions, "GRAPH_PACKAGE_NOT_LOCKED")
            compiled.add(key)
        else:
            need(package.startswith("path+file:///"), "UNSELECTED_PACKAGE_SOURCE")
    need(len(compiled) == 160, "EXACT_COMPILED_ARCHIVE_SET")
    archive_prefix = "registry/cache/" + REGISTRY_DIR + "/"
    index_prefix = "registry/index/" + REGISTRY_DIR + "/"
    available = {}
    missing = set()
    for key, digest in sorted(versions.items()):
        name, version = key.split("@")
        relative = archive_prefix + name + "-" + version + ".crate"
        if relative in retained_seed_map:
            available[key] = (relative, digest)
        else:
            missing.add(key)
    need(missing == MISSING_LOCKED_VERSIONS and len(missing) == 40
         and len(available) == 180 and compiled <= set(available), "EXACT_AVAILABLE_LOCKED_SET")
    need(set(available) - compiled == set(EXTRA_ARCHIVES), "EXACT_TWENTY_RESOLVER_ARCHIVE_ADDITIONS")
    archives = {relative: digest for relative, digest in available.values()}
    entries = {index_prefix + ".cache/" + index_path(name) for name in names}
    config = index_prefix + "config.json"
    selected = {}
    for relative in sorted(set(archives) | entries | {config}):
        pin = retained_seed_map[relative]
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and type(pin["bytes"]) is int
             and 0 < pin["bytes"] <= 16*1024**2 and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]),
             "RETAINED_CACHE_PIN:" + relative)
        if relative in archives:
            need(pin["sha256"] == archives[relative], "ARCHIVE_LOCK_CHECKSUM:" + relative)
        selected[relative] = dict(pin)
    for key, size in EXTRA_ARCHIVES.items():
        need(selected[available[key][0]]["bytes"] == size, "EXTRA_ARCHIVE_BYTES:" + key)
    compiled_bytes = sum(selected[available[key][0]]["bytes"] for key in compiled)
    archive_bytes = sum(selected[name]["bytes"] for name in archives)
    index_bytes = sum(selected[name]["bytes"] for name in entries)
    need(len(selected) == 379 and len(entries) == 198 and compiled_bytes == 13640297
         and archive_bytes == 15538366 and index_bytes == 9755696
         and sum(EXTRA_ARCHIVES.values()) == 1898069, "EXACT_CACHE_COUNTS_AND_BYTES")
    return selected, {
        "schema": "DMKN_V5_LOCKED_RESOLVER_CACHE_SELECTION_V1",
        "locked_registry_versions": 220, "locked_registry_names": 198,
        "compiled_registry_versions": 160, "selected_available_locked_archives": 180,
        "selected_cache_files": 379, "archive_bytes": archive_bytes, "index_bytes": index_bytes,
        "config_bytes": selected[config]["bytes"],
        "added_archives": {
            key: {"path": available[key][0], **selected[available[key][0]]}
            for key in sorted(EXTRA_ARCHIVES)
        },
        "unavailable_locked_versions": sorted(missing),
        "scope": "RETAINED_TARGET_RESOLUTION_CANDIDATE_NOT_COMPLETE_LOCK_AVAILABILITY",
        "missing_scope": "Inactive in retained successful target graph/build; selected offline command must still succeed.",
    }

