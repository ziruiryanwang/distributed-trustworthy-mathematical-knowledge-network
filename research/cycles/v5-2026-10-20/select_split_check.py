"""Small source-map selection for one split-custody integration; never runs it.

Reuse exact selection helpers and the completed semantic reader's runtime.
Only two logical source replacements, one reused helper and a new owner change.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CYCLE = ROOT/"research/cycles/v5-2026-10-20"
NAME = "client-split-check-01"
SOURCE_ROOT = ROOT/"product-local/v5-split-reader-source-01"
RUN_ROOT = ROOT/"product-local/v5-split-reader-runs"
MIB = 1024**2


def main():
    if (Path.cwd() != ROOT or not sys.flags.isolated or not sys.flags.no_site
            or not sys.dont_write_bytecode):
        raise ValueError("CANONICAL_ISOLATED_SELECTION")
    if len(sys.argv) != 4 or not all(re.fullmatch(r"[0-9a-f]{64}", arg)
                                     for arg in sys.argv[1:]):
        raise ValueError("THREE_REVIEWED_SOURCE_HASHES_REQUIRED")
    utility_path = CYCLE/"select_semantic_check.py"
    if hashlib.sha256(utility_path.read_bytes()).hexdigest() != (
            "09268d9146b2628afa6c134300b2a10f7100a9aabd986f6d4e677490b8734795"):
        raise ValueError("SELECTION_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("retained_selection", utility_path)
    utility = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utility)
    need, exact, pin, save = utility.need, utility.exact, utility.pin, utility.save
    raw, unused = exact(ROOT/"experiments/v5-local-checks/client-semantic-check-01-plan.json",
        "768c80f3d06ad0cf8fbf47ed09e721b5b77a9b787f6785a448c58510930a25af")
    prior = json.loads(raw)
    need(prior["owner_entry"] == "semantic_check.py" and len(prior["sources"]) == 105,
         "EXACT_COMPLETED_BASIS")
    payloads, sources = {}, {}
    for key, expected in prior["sources"].items():
        role, relative = key.split("/", 1)
        parts = PurePosixPath(relative)
        need(role in ("v5", "portable", "owner") and parts.as_posix() == relative
             and not parts.is_absolute() and ".." not in parts.parts, "SOURCE_RELATIVE")
        data, actual = pin(Path(prior["source_roots"][role]).joinpath(*parts.parts))
        need(actual == expected, "RETAINED_SOURCE_PIN:"+key)
        if role == "owner":
            need(key == "owner/semantic_check.py", "EXACT_OLD_OWNER")
            key = "v5/client/semantic_check.py"
        need(key not in sources, "SOURCE_COLLISION")
        payloads[key], sources[key] = data, actual
    changes = (
        ("v5/client/workspace_evidence.py", "workspace_evidence.py", sys.argv[1], True),
        ("v5/client/semantic_reader.py", "semantic_reader.py", sys.argv[2], True),
        ("owner/split_check.py", "split_check.py", sys.argv[3], False),
    )
    for key, filename, digest, replacement in changes:
        need((key in sources) == replacement, "EXACT_CHANGED_BOUNDARY")
        payloads[key], sources[key] = exact(
            ROOT/"software/v5/client/supplier_selected"/filename, digest)
    need(len(sources) == 106 and sum(map(len, payloads.values())) <= 4*MIB,
         "SMALL_SOURCE_MAP")
    need(not any("/test_" in key or "actual_assets" in key or "terminal_assets" in key
                 for key in sources), "NO_TEST_FIXTURE_AUTHORITY")
    params = deepcopy(prior["parameters"])
    params["schema"] = "DMKN_V5_SPLIT_CUSTODY_CHECK_V1"
    reader = params["reader"]
    # Two already authorized contacts; no new search, request, CPU or byte grant.
    need(reader["query"]["search_limits"]["providers"] == 1, "PRIOR_SINGLE_PROVIDER")
    reader["query"]["search_limits"]["providers"] = 2
    reader.update(workspace_path=str(RUN_ROOT/(NAME+"-reader")), create_workspace=True)
    exact(Path(params["packet"]["path"]), params["packet"]["sha256"])
    plan = deepcopy(prior)
    plan.update(name=NAME, workspace_root=str(RUN_ROOT),
        source_roots={role: str(SOURCE_ROOT/role) for role in ("v5", "portable", "owner")},
        sources=sources, owner_entry="split_check.py", parameters=params)
    output = ROOT/"experiments/v5-local-checks"/(NAME+"-plan.json")
    need(not SOURCE_ROOT.exists() and not RUN_ROOT.exists() and not output.exists(),
         "FRESH_SELECTION_PATHS")
    SOURCE_ROOT.mkdir()
    for role in ("v5", "portable", "owner"):
        (SOURCE_ROOT/role).mkdir()
    for key, data in payloads.items():
        destination = SOURCE_ROOT.joinpath(*PurePosixPath(key).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        save(destination, data)
    need({p.relative_to(SOURCE_ROOT).as_posix() for p in SOURCE_ROOT.rglob("*") if p.is_file()}
         == set(payloads), "EXACT_STAGED_SOURCE_CENSUS")
    RUN_ROOT.mkdir()
    save(output, json.dumps(plan, sort_keys=True, indent=2).encode()+b"\n")
    unused_raw, result = pin(output)
    python = Path(plan["installation_root"])/"receiver/runtime/python/python.exe"
    print(json.dumps({"path": str(output), **result, "sources": len(sources),
        "staged_source_bytes": sum(map(len, payloads.values())), "executed": False,
        "argv": [str(python), "-I", "-S", "-B", str(SOURCE_ROOT/"v5/client/launch.py"),
                 str(output), result["sha256"]]}))


if __name__ == "__main__":
    main()
