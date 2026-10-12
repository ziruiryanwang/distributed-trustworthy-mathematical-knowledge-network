"""Pure exact lock/unit-graph transformation for the adopted aggregate overlay."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tomllib

PACKAGE = "dmkn-aggregate-claim-relation"
BINARY = "dmkn-aggregate-claim-guest"
LIBRARY = "dmkn_aggregate_relation"
TARGET = "riscv32im-risc0-zkvm-elf"


def need(value, reason):
    if not value: raise ValueError(reason)


def repin_lock(raw: bytes) -> bytes:
    old = tomllib.loads(raw.decode("utf-8"))
    need(old["version"] == 4 and type(old["package"]) is list,"ADOPTED_LOCK_SCHEMA")
    roots = [row for row in old["package"] if row["name"] == "dmkn-module-relation"]
    need(roots == [{"name":"dmkn-module-relation","version":"0.1.0",
        "dependencies":["nanoda_lib","risc0-zkvm","serde","serde_json"]}],"EXACT_MODULE_LOCK_RECORD")
    checkers = [row for row in old["package"] if row["name"] == "nanoda_lib"]
    need(len(checkers) == 1 and checkers[0]["version"] == "0.4.19" and "source" not in checkers[0],
        "EXACT_LOCAL_CHECKER_LOCK_RECORD")
    need(not any(row["name"] == PACKAGE for row in old["package"]),"FRESH_AGGREGATE_LOCK_RECORD")
    added = {"name":PACKAGE,"version":"0.2.0",
        "dependencies":["dmkn-module-relation","risc0-zkvm","serde_json"]}
    expected = copy.deepcopy(old); expected["package"].append(added)
    text = raw.decode("utf-8").replace("\r\n","\n").rstrip()+"\n\n"
    text += ('[[package]]\nname = "dmkn-aggregate-claim-relation"\nversion = "0.2.0"\n'
        'dependencies = [\n "dmkn-module-relation",\n "risc0-zkvm",\n "serde_json",\n]\n')
    need(tomllib.loads(text) == expected,"ONLY_ONE_LOCAL_PACKAGE_ADDED_TO_LOCK")
    return text.encode("utf-8")


def normalize_cache(value, directory):
    if isinstance(value, dict): return {key:normalize_cache(item,directory) for key,item in value.items()}
    if isinstance(value, list): return [normalize_cache(item,directory) for item in value]
    if isinstance(value, str):
        path = Path(directory)
        return value.replace(path.as_uri(),"<CACHE-URI>").replace(str(path),"<CACHE>").replace(path.as_posix(),"<CACHE>")
    return value


def canonical_graph(graph):
    need(set(graph) == {"version","roots","units"} and graph["version"] == 1,"GRAPH_SCHEMA")
    units = graph["units"]
    need(type(units) is list and 1 <= len(units) <= 2048,"GRAPH_UNIT_BOUND")
    identities = [json.dumps({key:value for key,value in unit.items() if key != "dependencies"},
        sort_keys=True,separators=(",",":")) for unit in units]
    need(len(set(identities)) == len(identities),"UNIQUE_GRAPH_UNITS")
    rows = {}
    for index,unit in enumerate(units):
        edges = []
        for edge in unit["dependencies"]:
            target = edge["index"]
            need(type(target) is int and 0 <= target < len(units),"GRAPH_EDGE_INDEX")
            edges.append({**edge,"index":identities[target]})
        rows[identities[index]] = sorted(edges,key=lambda edge:json.dumps(edge,sort_keys=True))
    need(type(graph["roots"]) is list and len(graph["roots"]) == 1
        and type(graph["roots"][0]) is int and 0 <= graph["roots"][0] < len(units),"ONE_GRAPH_ROOT")
    return {"version":1,"roots":[identities[graph["roots"][0]]],"units":rows}


def package_id(directory, name, version):
    return "path+"+Path(directory).as_uri()+"#"+name+"@"+version


def expected_delta(old_graph, old_run: Path, new_run: Path):
    canonical_graph(old_graph)
    expected = copy.deepcopy(old_graph)
    units = expected["units"]
    old_module = old_run/"project/modules/receipt"
    old_checker = old_run/"project/modules/native/checker"
    project = new_run/"project/software/v5"
    module_package = project/"aggregate_guest/module"
    checker_package = project/"aggregate_guest/checker"
    aggregate_package = project/"aggregate_guest"
    old_module_id = package_id(old_module,"dmkn-module-relation","0.1.0")
    old_checker_id = package_id(old_checker,"nanoda_lib","0.4.19")
    modules = [(index,unit) for index,unit in enumerate(units)
        if unit["pkg_id"] == old_module_id and unit["target"]["kind"] == ["lib"]]
    checkers = [(index,unit) for index,unit in enumerate(units) if unit["pkg_id"] == old_checker_id]
    root_index = expected["roots"][0]; root = units[root_index]
    need(len(units) == 296 and len(modules) == len(checkers) == 1
        and root["pkg_id"] == old_module_id and root["target"]["name"] == "dmkn-module-guest"
        and root["target"]["kind"] == ["bin"] and root["target"]["crate_types"] == ["bin"]
        and Path(root["target"]["src_path"]) == old_module/"src/main.rs", "ADOPTED_MODULE_GUEST_ROOT")
    module_index,module = modules[0]; checker_index,checker = checkers[0]
    need(module["target"]["name"] == "dmkn_module_relation"
        and Path(module["target"]["src_path"]) == old_module/"src/lib.rs"
        and checker["target"]["name"] == "nanoda_lib" and checker["target"]["kind"] == ["lib"]
        and Path(checker["target"]["src_path"]) == old_checker/"src/lib.rs","ADOPTED_PROJECT_LIBRARY_TARGETS")
    for unit in (root,module,checker):
        need(unit["platform"] == TARGET and unit["mode"] == "build" and unit["features"] == []
            and unit["profile"] == root["profile"] and unit["profile"]["overflow_checks"] is True
            and unit["profile"]["panic"] == "abort" and unit["profile"]["opt_level"] == "3",
            "ADOPTED_PROJECT_PROFILES")
    module["pkg_id"] = package_id(module_package,"dmkn-module-relation","0.1.0")
    module["target"]["src_path"] = str(project/"modules/receipt/src/lib.rs")
    checker["pkg_id"] = package_id(checker_package,"nanoda_lib","0.4.19")
    checker["target"]["src_path"] = str(project/"modules/native/proof_validation/lib.rs")
    old_direct = {edge["extern_crate_name"] for edge in root["dependencies"] if not edge["noprelude"]}
    need(old_direct == {"dmkn_module_relation","nanoda_lib","risc0_zkvm","serde","serde_json"},
        "EXACT_OLD_ROOT_DEPENDENCIES")
    need(all(edge["public"] is False for edge in root["dependencies"] if not edge["noprelude"]),
        "EXACT_OLD_PRIVATE_DIRECT_EDGES")
    deps = [edge for edge in root["dependencies"] if edge["noprelude"]
        or edge["extern_crate_name"] in {"dmkn_module_relation","risc0_zkvm","serde_json"}]
    need([edge["index"] for edge in deps if edge["extern_crate_name"] == "dmkn_module_relation"] == [module_index],
        "EXACT_MODULE_DEPENDENCY")
    root["pkg_id"] = package_id(aggregate_package,PACKAGE,"0.2.0")
    root["target"]["name"] = BINARY
    root["target"]["src_path"] = str(project/"aggregate/main.rs")
    root["dependencies"] = copy.deepcopy(deps)
    library = copy.deepcopy(root)
    library["target"].update(name=LIBRARY,kind=["lib"],crate_types=["lib"],doctest=True,
        src_path=str(project/"aggregate_claims/lib.rs"))
    library_index = len(units); units.append(library)
    root["dependencies"].append({"extern_crate_name":LIBRARY,"index":library_index,"noprelude":False,"public":False})
    return normalize_cache(expected,old_run/"cargo-home")


def verify_delta(old_graph,new_graph,old_run: Path,new_run: Path):
    expected = expected_delta(old_graph,old_run,new_run)
    actual = normalize_cache(new_graph,new_run/"cargo-home")
    need(canonical_graph(expected) == canonical_graph(actual),"UNSELECTED_FULL_AGGREGATE_GUEST_GRAPH_DELTA")
    json_units = [unit for unit in actual["units"]
        if unit["pkg_id"] == "registry+https://github.com/rust-lang/crates.io-index#serde_json@1.0.151"]
    need(json_units and all(unit["features"] == ["default","std"] for unit in json_units),
        "VALUE_IDENTITY_REQUIRES_EXACT_SERDE_JSON_DEFAULT_STD")
    return {"status":"EXACT_TWO_RELOCATED_LIBRARIES_REPLACED_ROOT_AND_ONE_AGGREGATE_LIBRARY",
        "old_units":len(old_graph["units"]),"new_units":len(new_graph["units"]),
        "external_package_feature_profile_or_edge_changes":0,"serde_json_features":["default","std"]}
