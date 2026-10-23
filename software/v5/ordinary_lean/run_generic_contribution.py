"""One selected generic-source contribution above a retained local owner.

The exact local fork below preserves completed experiment bytes. It is NOT a
peer import, recovery protocol, normal per-contribution requirement or warrant
from a saved PASS. Root must explicitly adopt the original local store and pin
its complete closed tree. Source is owner-approved executable Lean, not hostile
input. No foundation, acquisition, index or certificate campaign is repeated.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import sys
import time

MIB = 1024**2


def fork_local_owner(A, original, destination, directories, files, check):
    """Bounded exact local diagnostic fork while holding original owner lock."""
    import msvcrt
    C, P, need = A.C, A.P, A.need
    original = C.ordinary(Path(original), directory=True)
    destination = C.ordinary(Path(destination), directory=True, fresh=True)
    need(not destination.is_relative_to(original) and not original.is_relative_to(destination),
         "GENERIC_FORK_OVERLAP")
    need(type(directories) is list and 2 <= len(directories) <= 128
         and len(set(directories)) == len(directories) and type(files) is dict
         and 3 <= len(files) <= 512, "GENERIC_FORK_CENSUS_BOUND")
    need({"catalog", "custody"} <= set(directories) and
         {"catalog/ADOPTION.json", "catalog/owner.lock", "catalog/catalog.sqlite",
          "custody/ordinary.sqlite"} <= set(files), "GENERIC_FORK_REQUIRED_PATHS")
    total = 0
    for rel in [*directories, *files]:
        path = A.relative(rel)
        need(path.parts[0] in ("catalog", "custody") and
             (path.parent.as_posix() == "." or path.parent.as_posix() in directories),
             "GENERIC_FORK_PATH")
        need(not any(part.endswith(("-journal", "-wal", "-shm")) or part == "WITHDRAWN"
                     for part in path.parts), "GENERIC_FORK_UNCLEAN_SOURCE")
    need(len({rel.casefold() for rel in [*directories, *files]}) == len(directories)+len(files),
         "GENERIC_FORK_PATH_ALIAS")
    for pin in files.values():
        P.fields(pin, ("bytes", "sha256"), "GENERIC_FORK_PIN")
        total += P.uint(pin["bytes"], 0, 64*MIB, "GENERIC_FORK_FILE_BOUND")
        C.hexid(pin["sha256"])
    need(total <= 128*MIB and files["catalog/owner.lock"] ==
         {"bytes": 1, "sha256": hashlib.sha256(b"\0").hexdigest()}, "GENERIC_FORK_TOTAL")

    def verify_file(path, pin, lock=None):
        check(); C.ordinary(path)
        need(path.stat().st_size == pin["bytes"], "GENERIC_FORK_SIZE")
        digest, size = hashlib.sha256(), 0
        if lock is not None:
            lock.seek(0); raw = lock.read(2)
            digest.update(raw); size = len(raw)
        else:
            with path.open("rb") as incoming:
                while raw := incoming.read(MIB):
                    check(); size += len(raw)
                    need(size <= pin["bytes"], "GENERIC_FORK_GREW")
                    digest.update(raw)
        need(size == pin["bytes"] and digest.hexdigest() == pin["sha256"],
             "GENERIC_FORK_CHANGED")

    def verify_tree(lock=None):
        for rel in directories:
            check(); directory = C.ordinary(original/rel, directory=True)
            expected = {A.relative(item).name for item in [*directories, *files]
                        if A.relative(item).parent.as_posix() == rel}
            actual = set()
            with os.scandir(directory) as entries:
                for entry in entries:
                    check()
                    need(entry.name in expected, "GENERIC_FORK_EXTRA_PATH")
                    actual.add(entry.name)
            need(actual == expected, "GENERIC_FORK_MISSING_PATH")
        for rel, pin in files.items():
            verify_file(original/rel, pin, lock if rel == "catalog/owner.lock" else None)

    verify_tree()
    with (original/"catalog/owner.lock").open("r+b") as lock:
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        verify_tree(lock)
        destination.mkdir()
        for rel in sorted(directories, key=lambda value: (value.count("/"), value)):
            check(); C.ordinary(destination/rel, directory=True, fresh=True).mkdir()
        for rel, pin in sorted(files.items()):
            check(); target = C.ordinary(destination/rel, fresh=True)
            with target.open("xb") as outgoing:
                if rel == "catalog/owner.lock":
                    lock.seek(0); outgoing.write(lock.read(1))
                else:
                    size = 0
                    with (original/rel).open("rb") as incoming:
                        while raw := incoming.read(MIB):
                            check(); size += len(raw)
                            need(size <= pin["bytes"], "GENERIC_FORK_COPY_GREW")
                            outgoing.write(raw)
                outgoing.flush(); os.fsync(outgoing.fileno())
            verify_file(target, pin)
        verify_tree(lock)
    verify_tree()
    return {"files": len(files), "bytes": total,
            "authority": "OWNER_SELECTED_LOCAL_FORK_NOT_PEER_SNAPSHOT_ACCEPTANCE"}


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--plan-sha256", required=True)
    return p.parse_args()


def main():
    args = arguments()
    started, cpu_started, worker_cpu = time.monotonic(), time.process_time(), 0.0
    with Path(args.plan).open("rb") as stream:
        raw = stream.read(2*MIB+1)
    if not (0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == args.plan_sha256):
        raise ValueError("GENERIC_EXACT_OWNER_PLAN")
    plan = json.loads(raw)
    if plan["schema"] != "DMKN_GENERIC_CONTRIBUTION_LOCAL_PLAN_V1":
        raise ValueError("GENERIC_PLAN_SCHEMA")
    output = Path(args.output)
    v5 = Path(__file__).resolve().parents[1]
    # Only already owner-selected installed core grants mathematical authority.
    sys.path[:0] = [str(Path(plan["installation"])/"py"), str(v5/"ordinary_lean"), str(v5)]
    import ordinary_admission as A
    import ordinary_contribution as G
    from transport.ordinary_acquisition import OrdinaryStore
    need, C, P, E, S = A.need, A.C, A.P, A.E, A.S
    plan = E.strict_json(raw, E.Limits(max_bytes=2*MIB))
    P.fields(plan, ("schema", "installation", "manifest_sha256", "runtime_roots",
        "source_directory", "directories", "files", "parent_root", "store_id",
        "custody_limits", "helper_paths", "source_body", "acquired_targets",
        "output_names", "wall_seconds", "cpu_seconds", "memory_mib"), "GENERIC_PLAN_FIELDS")
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "GENERIC_OWNER_PROFILE")
    need(output.is_absolute() and v5 == output/"sources/software/v5", "GENERIC_SNAPSHOT_LOCATION")
    C.ordinary(output, directory=True)
    P.uint(plan["wall_seconds"], 60, 300, "GENERIC_WALL_ENVELOPE")
    P.uint(plan["cpu_seconds"], 10, 180, "GENERIC_CPU_ENVELOPE")
    P.uint(plan["memory_mib"], 256, 1792, "GENERIC_MEMORY_ENVELOPE")
    deadline = started + plan["wall_seconds"]

    def check():
        need(time.monotonic() < deadline and
             time.process_time()-cpu_started+worker_cpu < plan["cpu_seconds"],
             "GENERIC_ORIGINAL_PARENT_ALLOCATION")

    def account(seconds):
        nonlocal worker_cpu
        need(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
             "GENERIC_WORKER_CHARGE")
        worker_cpu += seconds

    def budget():
        check()
        wall = math.floor(deadline-time.monotonic())-3
        cpu = math.floor(plan["cpu_seconds"]-(time.process_time()-cpu_started)-worker_cpu)-1
        need(wall >= 30 and cpu >= 2, "GENERIC_REMAINING_BUDGET")
        value = A.OperationBudget(wall, cpu, plan["memory_mib"], output_bytes=16*MIB)
        value.deadline = min(value.deadline, deadline)
        return value

    def save(filename, value):
        P.PortableCatalog._write_fresh(output/filename, E.canonical_json(value))

    installed = C.ordinary(Path(plan["installation"]), directory=True)
    installation = A.NativeInstallation.open(installed,
        C.read_bounded(installed/"INSTALLATION.json", 2*MIB), plan["manifest_sha256"],
        runtime_roots={key: Path(path) for key, path in plan["runtime_roots"].items()})
    check()
    forked = fork_local_owner(A, plan["source_directory"], output/"fork",
                              plan["directories"], plan["files"], check)
    save("FORK.json", forked)
    adoption = E.strict_json(C.read_bounded(output/"fork/catalog/ADOPTION.json", 2*MIB))
    need(adoption["store_id"] == plan["store_id"] and
         adoption["implementation"] == installation.doc["implementation"], "GENERIC_LOCAL_OWNER_MATCH")
    helpers = tuple(C.ordinary(Path(value), directory=True) for value in plan["helper_paths"])
    selection = json.loads(C.read_bounded(output/"selection.json", 2*MIB))
    pins = []
    for relative, digest in selection["sources"].items():
        path = C.ordinary(output/"sources"/str(A.relative(relative)))
        pins.append((path, path.stat().st_size, digest))
    # Native authoring support only; installation owns the separately pinned
    # runtime. Do not reread an entire runtime library per source contribution.
    for selected, digest in selection["runtime_pins"].items():
        path = Path(selected)
        if any(path.parent == helper for helper in helpers):
            path = C.ordinary(path)
            pins.append((path, path.stat().st_size, digest))
    profile = G.AuthoringProfile(installation_manifest_sha256=installation.manifest_sha256,
        helper_paths=helpers, author_worker_script=v5/"ordinary_lean/run_ordinary_api_producer.py",
        file_pins=tuple(pins))
    source_body = C.read_bounded(v5.parent.parent/str(A.relative(plan["source_body"])), MIB)
    custody = owner = None
    try:
        custody = OrdinaryStore(output/"fork/custody", installation.semantic_id,
                                plan["custody_limits"])
        owner = A.OrdinaryAdmission.open(installation, output/"fork/catalog", plan["store_id"],
            evidence_store=custody, limits=P.Limits(**adoption["limits"]))
        result = G.contribute_source(owner, plan["parent_root"], plan["acquired_targets"],
            source_body, plan["output_names"], output_directory=output/"contribution",
            profile=profile, parent_deadline=deadline, make_budget=budget,
            account_worker_cpu=account, check_parent=check)
        # Fixture-specific usefulness/reuse assertions stay in this diagnostic
        # caller, never the generic mathematical admission or contribution API.
        need([row["name"] for row in result["targets"]] == plan["output_names"],
             "GENERIC_CALLER_OUTPUTS")
        items = [A.PE.read_evidence(C.read_bounded(Path(row["file"]), MIB))
                 for row in result["units"]]
        kinds = {E.name_key(row[0]): row[1] for item in items for row in item.document["unit"][2]}
        need([kinds[E.name_key(name)] for name in plan["output_names"]] == [1, 2],
             "GENERIC_BARE_DEFINITION_AND_THEOREM")
        imports = {(E.name_key(name), identity) for item in items
                   for name, identity in item.document["imports"]}
        need(all((E.name_key(row["name"]), row["export_id"]) in imports
                 for row in plan["acquired_targets"]), "GENERIC_BOTH_METHODS_USED")
        check()
        # Timing uses normal JSON: canonical mathematics JSON deliberately
        # excludes floats. This is an observation, not a portable truth record.
        report = {"status": "PASS_GENERIC_MULTITARGET_LOCAL_CONTRIBUTION", "result": result,
            "fork": forked, "worker_cpu_seconds": worker_cpu,
            "controller_cpu_seconds": time.process_time()-cpu_started,
            "wall_seconds": time.monotonic()-started,
            "claim": "LOCAL_GENERIC_SOURCE_AND_OUTPUTS_NOT_NOVELTY_GROWTH_OR_GLOBAL_RELEASE"}
        P.PortableCatalog._write_fresh(output/"GENERIC-RESULT.json",
            json.dumps(report, sort_keys=True, allow_nan=False).encode("utf-8"))
        print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    finally:
        if owner is not None: owner.close()
        if custody is not None: custody.close()


if __name__ == "__main__":
    main()
