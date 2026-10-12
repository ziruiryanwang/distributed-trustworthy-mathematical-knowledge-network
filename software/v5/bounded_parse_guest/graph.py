"""Pure exact 297-unit relocation and the minimal retained offline cache set.

No filesystem access or subprocess is performed by this module. Cargo's lexical
`..` spelling is deliberate: equality is stricter than resolved-path equality.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import tomllib

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD_RUN = ROOT / "experiments/v5-local-checks/aggregate-guest-build-01"
BINARY = "dmkn-aggregate-claim-guest"
TARGET = "riscv32im-risc0-zkvm-elf"
REGISTRY = "registry+https://github.com/rust-lang/crates.io-index"
REGISTRY_DIR = "index.crates.io-1949cf8c6b5b557f"


def need(value, reason):
    if not value:
        raise ValueError(reason)


def package_id(directory, name, version):
    return "path+" + Path(directory).as_uri() + "#" + name + "@" + version


def normalize_cache(value, directory):
    if isinstance(value, dict):
        return {key: normalize_cache(item, directory) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_cache(item, directory) for item in value]
    if isinstance(value, str):
        directory = Path(directory)
        return value.replace(directory.as_uri(), "<CACHE-URI>").replace(
            str(directory), "<CACHE>").replace(directory.as_posix(), "<CACHE>")
    return value


def canonical_graph(graph):
    need(set(graph) == {"version", "roots", "units"} and graph["version"] == 1, "GRAPH_SCHEMA")
    units = graph["units"]
    need(type(units) is list and len(units) == 297, "EXACT_297_GRAPH_UNITS")
    identities = [json.dumps({key: value for key, value in unit.items() if key != "dependencies"},
                            sort_keys=True, separators=(",", ":")) for unit in units]
    need(len(set(identities)) == len(identities), "UNIQUE_GRAPH_UNITS")
    rows = {}
    for index, unit in enumerate(units):
        edges = []
        for edge in unit["dependencies"]:
            target = edge["index"]
            need(type(target) is int and 0 <= target < len(units), "GRAPH_EDGE_INDEX")
            edges.append({**edge, "index": identities[target]})
        rows[identities[index]] = sorted(edges, key=lambda row: json.dumps(row, sort_keys=True))
    need(type(graph["roots"]) is list and len(graph["roots"]) == 1
         and type(graph["roots"][0]) is int and 0 <= graph["roots"][0] < len(units), "ONE_GRAPH_ROOT")
    return {"version": 1, "roots": [identities[graph["roots"][0]]], "units": rows}


def expected_graph(old_graph, new_run):
    canonical_graph(old_graph)
    new_run = Path(new_run)
    need(new_run.is_absolute() and new_run.parent == OLD_RUN.parent
         and re.fullmatch(r"bounded-parse-guest-build-[0-9]{2}", new_run.name), "FRESH_RUN_SHAPE")
    expected = copy.deepcopy(old_graph)
    old = OLD_RUN / "project/software/v5/aggregate_guest"
    new = new_run / "project/software/v5/bounded_parse_guest"
    specs = (
        ("", "dmkn-aggregate-claim-relation", "0.2.0", "dmkn_aggregate_relation", "lib",
         "../aggregate_claims/lib.rs", "../bounded_parse/aggregate_lib.rs"),
        ("", "dmkn-aggregate-claim-relation", "0.2.0", BINARY, "bin",
         "../aggregate/main.rs", "../aggregate/main.rs"),
        ("module", "dmkn-module-relation", "0.1.0", "dmkn_module_relation", "lib",
         "../../modules/receipt/src/lib.rs", "../../bounded_parse/module_lib.rs"),
        ("checker", "nanoda_lib", "0.4.19", "nanoda_lib", "lib",
         "../../modules/native/proof_validation/lib.rs", "../../modules/native/proof_validation/lib.rs"),
    )
    changed = set()
    for suffix, name, version, target, kind, old_source, new_source in specs:
        matches = [(i, row) for i, row in enumerate(expected["units"])
                   if row["pkg_id"] == package_id(old / suffix, name, version)
                   and row["target"]["name"] == target]
        need(len(matches) == 1, "ONE_PROJECT_UNIT:" + target)
        index, unit = matches[0]
        need(unit["target"]["src_path"] == str(old / suffix / old_source)
             and unit["target"]["kind"] == [kind] and unit["target"]["crate_types"] == [kind]
             and unit["platform"] == TARGET and unit["mode"] == "build"
             and unit["features"] == [], "EXACT_OLD_PROJECT_UNIT:" + target)
        need(unit["profile"]["overflow_checks"] is True and unit["profile"]["panic"] == "abort"
             and unit["profile"]["opt_level"] == "3" and unit["profile"]["lto"] == "true",
             "UNCHANGED_RELEASE_PROFILE")
        unit["pkg_id"] = package_id(new / suffix, name, version)
        unit["target"]["src_path"] = str(new / suffix / new_source)
        changed.add(index)
        if kind == "bin":
            need(old_graph["roots"] == [index], "UNCHANGED_SINGLE_BIN_ROOT")
    need(len(changed) == 4 and not any(str(old) in row["target"]["src_path"]
         for row in expected["units"]), "EXACT_FOUR_PROJECT_UNIT_RELOCATIONS")
    return normalize_cache(expected, OLD_RUN / "cargo-home")


def verify_graph(old_graph, new_graph, new_run):
    expected = expected_graph(old_graph, new_run)
    actual = normalize_cache(new_graph, Path(new_run) / "cargo-home")
    need(canonical_graph(expected) == canonical_graph(actual), "UNSELECTED_GUEST_GRAPH_DELTA")
    units = [row for row in actual["units"] if row["pkg_id"] == REGISTRY + "#serde_json@1.0.151"]
    need(units and all(row["features"] == ["default", "std"] for row in units), "PINNED_GUEST_SERDE_JSON")
    return {"status": "EXACT_297_UNITS_TWO_CHANGED_LIB_ROOTS_AND_PROJECT_CACHE_RELOCATION",
            "old_units": 297, "new_units": 297, "package_feature_profile_edge_changes": 0,
            "changed_library_roots": 2, "relocated_project_units": 4}


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
    canonical_graph(old_graph)
    versions = {}
    for raw in (project_lock_bytes, std_lock_bytes):
        need(type(raw) is bytes and len(raw) <= 1024**2, "LOCK_BOUND")
        lock = tomllib.loads(raw.decode("utf-8"))
        need(lock["version"] == 4 and type(lock["package"]) is list, "LOCK_SCHEMA")
        seen = set()
        for row in lock["package"]:
            key = (row["name"], row["version"])
            need(key not in seen, "DUPLICATE_LOCK_PACKAGE")
            seen.add(key)
            if "source" not in row:
                continue
            need(row["source"] == REGISTRY and re.fullmatch(r"[0-9a-f]{64}", row["checksum"]),
                 "ONLY_PINNED_REGISTRY_PACKAGES")
            need(key not in versions or versions[key] == row["checksum"], "LOCK_CHECKSUM_CONFLICT")
            versions[key] = row["checksum"]
    names = {name for name, _ in versions}
    need(len(versions) == 220 and len(names) == 198, "EXACT_LOCK_UNION")
    compiled = set()
    for unit in old_graph["units"]:
        package = unit["pkg_id"]
        if package.startswith(REGISTRY + "#"):
            name, version = package[len(REGISTRY) + 1:].rsplit("@", 1)
            need((name, version) in versions, "GRAPH_PACKAGE_NOT_LOCKED")
            compiled.add((name, version))
        else:
            need(package.startswith("path+file:///"), "UNSELECTED_PACKAGE_SOURCE")
    need(len(compiled) == 160, "EXACT_COMPILED_ARCHIVE_SET")
    archive_prefix = "registry/cache/" + REGISTRY_DIR + "/"
    index_prefix = "registry/index/" + REGISTRY_DIR + "/"
    archives = {archive_prefix + name + "-" + version + ".crate": versions[(name, version)]
                for name, version in compiled}
    entries = {index_prefix + ".cache/" + index_path(name) for name in names}
    selected = {}
    for relative in sorted(set(archives) | entries | {index_prefix + "config.json"}):
        pin = retained_seed_map[relative]
        need(set(pin) == {"bytes", "sha256"} and type(pin["bytes"]) is int
             and 0 < pin["bytes"] <= 16*1024**2 and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]),
             "RETAINED_CACHE_PIN:" + relative)
        if relative in archives:
            need(pin["sha256"] == archives[relative], "ARCHIVE_LOCK_CHECKSUM:" + relative)
        selected[relative] = dict(pin)
    need(len(selected) == 359 and sum(selected[name]["bytes"] for name in archives) == 13640297
         and sum(selected[name]["bytes"] for name in entries) == 9755696, "EXACT_CACHE_COUNTS_AND_BYTES")
    return selected
