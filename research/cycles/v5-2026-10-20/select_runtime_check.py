"""Prepare one finite real factory/admission integration; no verifier invocation."""
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT/"experiments/v5-local-checks"
NAME = "client-runtime-check-01"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    prior = CHECKS/"client-retained-reuse-01-plan.json"
    need(pin(prior)["sha256"] ==
         "ad119b77bd672583521e0449ce0454deae163b09d13a444ddd5161f959720d25",
         "RETAINED_PLAN_CHANGED")
    old = json.loads(prior.read_bytes())
    plan = deepcopy(old)
    omitted = {"v5/client/actual_assets02.py", "v5/client/actual_owner03.py",
               "v5/client/actual_assets_atomic.py", "owner/actual_resume_owner.py"}
    need(omitted <= set(old["sources"]), "EXACT_OLD_OWNER_SCOPE")
    plan["sources"] = {key: row for key, row in old["sources"].items()
                       if key not in omitted}
    for key, row in plan["sources"].items():
        role, relative = key.split("/", 1)
        need(pin(Path(plan["source_roots"][role])/relative) == row,
             "RETAINED_SOURCE_CHANGED:"+key)
    for key, relative in (("v5/client/runtime.py", "client/runtime.py"),
                          ("owner/runtime_check.py", "client/runtime_check.py")):
        plan["sources"][key] = pin(ROOT/"software/v5"/relative)
    need(len(plan["sources"]) == 88, "EXACT_NEW_SOURCE_COUNT")
    for row in old["parameters"]["assets"].values():
        need(pin(Path(row["path"])) == {key: row[key] for key in ("bytes", "sha256")},
             "RETAINED_ASSET_CHANGED")

    # Pure fixed-profile/configuration definitions from the verified old map.
    sys.path[:0] = [str(ROOT/"software/v5/portable_runtime"), str(ROOT/"software/v5")]
    from frontier_network.custody import public_profile
    from mixed_claims.packet import Envelope
    assets = old["parameters"]["assets"]
    mib = 1024**2
    config = dict(schema="DMKN_V5_CLIENT_WORKSPACE_V1", wire_profile=public_profile(),
        module_limits=dict(modules=32, groups=128, declarations=512, bodies=256,
                           logical_bytes=32*mib, db_pages=16384),
        packet_limits=dict(packets=4, offers=8, offers_per_module=2, packet_bytes=16*mib,
                           logical_bytes=64*mib, db_pages=32768),
        index_limits=dict(max_objects=128, max_postings=8192, max_features=1024,
                          max_snapshots=256, max_logical_bytes=32*mib, max_db_pages=16384),
        packet_envelope=asdict(Envelope(packet_bytes=16*mib, claims=1,
                                       frontiers=1, deltas=2, edges=3)), max_operations=1,
        max_report_bytes=mib, ledger_pages=1024)
    limits = dict(wall_seconds=120, controller_cpu_seconds=45, calls=32,
        input_bytes=8*mib, worker_cpu_seconds=5, output_bytes=128*mib, output_entries=1024,
        acquisition=dict(requests=1, reply_bytes=mib, verify_attempts=1,
                         verification_input_bytes=mib, worker_cpu_seconds=5),
        imports=dict(max_sources=2, max_members=4, max_receipts=1, max_calls=4096,
                     submitted_bytes=8*mib, data_bytes=4*mib))
    plan.update(name=NAME, owner_entry="runtime_check.py", parameters=dict(
        schema="DMKN_V5_RUNTIME_CHECK_V1",
        runtime_adoption=dict(schema="DMKN_V5_CLIENT_RUNTIME_V1",
            preparation_profile=assets["profile"], native=assets["native"],
            receipt=assets["host"], aggregate=None),
        workspace_config=config, operation_limits=limits,
        foundation=assets["foundation"], receipt=assets["receipt"], bundle=assets["bundle"],
        verification_limits=dict(cpu_seconds=5, wall_seconds=30, memory_mib=128)),
        limits=dict(cpu_seconds=60, wall_seconds=180, memory_mib=256,
                    active_processes=4, stdout_bytes=mib, stderr_bytes=mib),
        output_limits=dict(bytes=128*mib, entries=4096))
    output = CHECKS/(NAME+"-plan.json")
    need(not output.exists() and not (Path(plan["workspace_root"])/NAME).exists(),
         "FRESH_PLAN_AND_RUN")
    with output.open("xb") as stream:
        stream.write(json.dumps(plan, sort_keys=True, indent=2).encode()+b"\n")
    print(json.dumps({"path": str(output), **pin(output), "source_count": 88,
                      "executed": False}))


if __name__ == "__main__":
    main()
