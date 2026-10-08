"""Exact allowed v5 guest graph/lock delta; pure data, no compiler or writes."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tomllib

OLD_PACKAGE = "commons-checker-guest"
NEW_PACKAGE = "dmkn-module-relation"
NEW_BINARY = "dmkn-module-guest"
NEW_LIBRARY = "dmkn_module_relation"
TARGET = "riscv32im-risc0-zkvm-elf"


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def repin_lock(raw: bytes) -> bytes:
    old = tomllib.loads(raw.decode("utf-8"))
    expected = copy.deepcopy(old)
    roots = [package for package in expected["package"] if package["name"] == OLD_PACKAGE]
    need(len(roots) == 1 and roots[0]["version"] == "0.0.2" and "source" not in roots[0],
         "EXACT_OLD_LOCK_ROOT")
    roots[0].update(name=NEW_PACKAGE, version="0.1.0")
    text = raw.decode("utf-8")
    before = 'name = "commons-checker-guest"\nversion = "0.0.2"'
    # Normalize generated-lock newlines; semantically change only this root record.
    normalized = text.replace("\r\n", "\n")
    need(normalized.count(before) == 1, "ONE_EXACT_ROOT_LOCK_RECORD")
    changed = normalized.replace(before, 'name = "dmkn-module-relation"\nversion = "0.1.0"')
    need(tomllib.loads(changed) == expected, "ROOT_ONLY_LOCK_DELTA")
    return changed.encode("utf-8")


def normalize(value, replacements):
    if isinstance(value, dict):
        return {key: normalize(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item, replacements) for item in value]
    if isinstance(value, str):
        for path, label in replacements:
            path = Path(path)
            value = value.replace(path.as_uri(), label + "-URI")
            value = value.replace(str(path), label).replace(path.as_posix(), label)
        return value
    return value


def canonical_graph(graph):
    need(set(graph) == {"version", "roots", "units"} and graph["version"] == 1, "GRAPH_SCHEMA")
    units = graph["units"]
    need(type(units) is list and 1 <= len(units) <= 2048, "GRAPH_UNIT_BOUND")
    identities = [json.dumps({k: v for k, v in unit.items() if k != "dependencies"},
                             sort_keys=True, separators=(",", ":")) for unit in units]
    need(len(identities) == len(set(identities)), "UNIQUE_GRAPH_UNITS")
    rows = {}
    for index, unit in enumerate(units):
        deps = []
        for dependency in unit["dependencies"]:
            target = dependency["index"]
            need(type(target) is int and 0 <= target < len(units), "GRAPH_EDGE_INDEX")
            deps.append({**dependency, "index": identities[target]})
        rows[identities[index]] = sorted(deps, key=lambda x: json.dumps(x, sort_keys=True))
    need(type(graph["roots"]) is list and len(graph["roots"]) == 1
         and type(graph["roots"][0]) is int and 0 <= graph["roots"][0] < len(units), "ONE_GRAPH_ROOT")
    return {"version": 1, "roots": [identities[graph["roots"][0]]], "units": rows}


def verify_delta(old_graph, new_graph, old_prep: Path, new_run: Path):
    old = normalize(old_graph, [(old_prep / "project/guest", "<WRAPPER>"),
        (old_prep / "project/checker", "<CHECKER>"), (old_prep / "cargo-home", "<CACHE>")])
    new = normalize(new_graph, [(new_run / "project/modules/receipt", "<WRAPPER>"),
        (new_run / "project/modules/native/checker", "<CHECKER>"), (new_run / "cargo-home", "<CACHE>")])
    canonical_graph(old); canonical_graph(new)
    json_units = [unit for unit in new["units"] if unit["pkg_id"] ==
                  "registry+https://github.com/rust-lang/crates.io-index#serde_json@1.0.151"]
    need(json_units and all(unit["features"] == ["default", "std"] for unit in json_units),
         "VALUE_IDENTITY_REQUIRES_EXACT_SERDE_JSON_DEFAULT_STD")
    expected = copy.deepcopy(old)
    root = expected["units"][expected["roots"][0]]
    need(root["target"]["name"] == OLD_PACKAGE and root["target"]["kind"] == ["bin"]
         and root["platform"] == TARGET and root["mode"] == "build"
         and root["pkg_id"] == "path+<WRAPPER>-URI#commons-checker-guest@0.0.2",
         "EXACT_OLD_GUEST_ROOT")
    # Path normalization retains the Cargo package prefix before the replaced URI.
    root["pkg_id"] = root["pkg_id"].replace("#commons-checker-guest@0.0.2", "#dmkn-module-relation@0.1.0")
    root["target"]["name"] = NEW_BINARY
    library = copy.deepcopy(root)
    library["target"].update(name=NEW_LIBRARY, kind=["lib"], crate_types=["lib"], doctest=True)
    source = library["target"]["src_path"]
    need(source.endswith(("/src/main.rs", "\\src\\main.rs")), "EXACT_ROOT_MAIN_PATH")
    library["target"]["src_path"] = source[:-7] + "lib.rs"
    library_index = len(expected["units"])
    expected["units"].append(library)
    root["dependencies"].append({"extern_crate_name": NEW_LIBRARY, "index": library_index,
                                 "noprelude": False, "public": False})
    need(canonical_graph(expected) == canonical_graph(new), "UNSELECTED_FULL_GUEST_GRAPH_DELTA")
    return {"status": "EXACT_ROOT_RENAME_ONE_LIBRARY_EDGE_AND_RELOCATED_CHECKER_ONLY",
            "old_units": len(old["units"]), "new_units": len(new["units"]),
            "serde_json_features": ["default", "std"],
            "external_package_feature_profile_or_edge_changes": 0}
