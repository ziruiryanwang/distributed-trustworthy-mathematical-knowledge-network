"""Select one ordinary HTTP reader integration; no product imports or execution."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT/"experiments/v5-local-checks"
NAME = "client-remote-check-01"
MIB = 1024**2
IMAGE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def selected(path, size, digest):
    value = pin(path)
    need(value == {"bytes": size, "sha256": digest}, "RETAINED_ASSET_CHANGED:"+str(path))
    return {"path": str(path), **value}


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    prior = CHECKS/"client-runtime-check-01-plan.json"
    direct = CHECKS/"direct-contact-controls-01-selection.json"
    need(pin(prior)["sha256"] ==
         "8eea1d8ff69ee381517643db3fdbcec41149ffceaaf66326d88fd11bd25dc8b6",
         "RETAINED_RUNTIME_PLAN_CHANGED")
    need(pin(direct)["sha256"] ==
         "120597af89c992d48cd288f1ff9d0c033fbd23dd74c04b21fec49a652c1d11bd",
         "RETAINED_DIRECT_SELECTION_CHANGED")
    old, controls = json.loads(prior.read_bytes()), json.loads(direct.read_bytes())
    plan = deepcopy(old)
    need("owner/runtime_check.py" in plan["sources"], "RETAINED_OWNER_ENTRY")
    del plan["sources"]["owner/runtime_check.py"]
    for key, row in plan["sources"].items():
        role, relative = key.split("/", 1)
        need(pin(Path(plan["source_roots"][role])/relative) == row,
             "RETAINED_RUNTIME_SOURCE_CHANGED:"+key)
    for key, digest in controls["sources"].items():
        need(pin(ROOT/key)["sha256"] == digest, "RETAINED_DIRECT_SOURCE_CHANGED:"+key)
        if not key.startswith("software/v5/") or Path(key).name.startswith("test_"):
            continue
        if key.startswith("software/v5/portable_runtime/"):
            target = "portable/"+key.removeprefix("software/v5/portable_runtime/")
        else:
            target = "v5/"+key.removeprefix("software/v5/")
        row = pin(ROOT/key)
        need(target not in plan["sources"] or plan["sources"][target] == row,
             "SOURCE_MAP_CONFLICT:"+target)
        plan["sources"][target] = row
    for key, relative, digest in (
        ("v5/client/remote_reader.py", "client/remote_reader.py",
         "4858be2274d9cd354a7abb59b9f65e9055f4f57a1334772e9f8865e806f0ba52"),
        ("owner/remote_check.py", "client/remote_check.py",
         "e2405b7c59cbd9ee1b4bf84e045aeaee2d7f0131812b9bcc3965ecc85ee6c5eb"),
    ):
        row = pin(ROOT/"software/v5"/relative)
        need(row["sha256"] == digest and key not in plan["sources"],
             "FRESH_REVIEWED_ENTRY:"+key)
        plan["sources"][key] = row
    need(len(plan["sources"]) == 103, "EXACT_SOURCE_CLOSURE_COUNT")
    need(not any("test_" in key or "actual_assets" in key or "terminal_assets" in key
                 for key in plan["sources"]), "NO_FIXTURE_FACTORY")
    adoption = deepcopy(old["parameters"]["runtime_adoption"])
    for row in (adoption["preparation_profile"], adoption["native"], adoption["receipt"],
                old["parameters"]["foundation"]):
        need(pin(Path(row["path"])) == {key: row[key] for key in ("bytes", "sha256")},
             "RETAINED_RUNTIME_ASSET_CHANGED")
    aggregate = selected(CHECKS/"small-aggregate-snapshot-host-build-01/small_aggregate_host.exe",
        6630400, "a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05")
    adoption["aggregate"] = {"executable": aggregate, "image": IMAGE}
    packet = selected(ROOT/
        "product-local/v5-client-owner-runs/client-actual-03/work/origin/operations/"
        "4898246455cde36d15d11631b263a7a4fe9bb8d6c18d920504e72f038ca8490b/"
        "preparation/author-1/mixed-packet.json", 554165,
        "92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f")

    config = deepcopy(old["parameters"]["workspace_config"])
    config["schema"] = "DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1"
    config["terminal_receipt_bytes"] = 8*MIB
    wire = config["wire_profile"]
    # Exact public evidence profile. No product import merely to prepare data.
    del wire["packet_schema"], wire["supported_claim_tags"]
    wire.update(schema="DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V1",
        proof_form="mixed-or-certified-terminal-v1", aggregate_image=IMAGE,
        mixed_packet_schema="DMKN_MIXED_DELTA_PACKET_V1",
        terminal_packet_schema="DMKN_CERTIFIED_TERMINAL_MEMBER_V1",
        aggregate_header_magic=b"DMKNA002".hex(), aggregate_header_version=2,
        aggregate_header_bytes=192, terminal_receipt_encoding="lowercase-hex")
    limits = dict(wall_seconds=90, controller_cpu_seconds=30, calls=32,
        input_bytes=8*MIB, worker_cpu_seconds=20, output_bytes=128*MIB, output_entries=1024,
        acquisition=dict(requests=8, reply_bytes=4*MIB, verify_attempts=1,
            verification_input_bytes=MIB, worker_cpu_seconds=20),
        imports=dict(max_sources=2, max_members=4, max_receipts=1, max_calls=4096,
                     submitted_bytes=8*MIB, data_bytes=4*MIB))
    query = dict(
        # Integration replaces only endpoint/policy with actual READY metadata.
        contacts={"provider": {"host": "127.0.0.1", "port": 1,
                              "tls": False, "server_name": None}},
        egress_policy={"schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
                       "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 1}]},
        specs=[{"tag": "declaration-kind", "value": "theorem"}],
        search_limits=dict(providers=1, snapshots=1, requests=4, pages=1, examined=8,
                           candidates=4, bytes=262144, wall_ms=30000, inflight=1),
        contact_lifetime_ms=30000,
        selection=dict(provider="provider", partition_index=0, start=0,
                       candidate_index=0, packet_index=0),
        offer=dict(max_bytes=65536, max_expanded_bytes=131072, max_age_ms=60000,
                   attempt_timeout_ms=5000),
        page=dict(limits=dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
                             record_probes=64, node_reads=10000, hash_calls=200000,
                             sql_vm_steps=100000), attempt_timeout_ms=5000),
        packets=dict(max_offers=1, max_bytes=4096),
        admission=dict(native_cpu_seconds=10, receipt_cpu_seconds=10,
                       wall_seconds=30, memory_mib=512))
    reader = dict(schema="DMKN_V5_REMOTE_READER_V1", runtime_adoption=adoption,
        workspace_path=str(Path(plan["workspace_root"])/(NAME+"-reader")),
        workspace_config=config, create_workspace=True, operation_limits=limits,
        foundation=deepcopy(old["parameters"]["foundation"]), query=query)
    plan.update(name=NAME, owner_entry="remote_check.py",
        parameters=dict(schema="DMKN_V5_REMOTE_CHECK_V1", packet=packet, reader=reader,
            service_limits=dict(max_connections=2, max_requests=8,
                max_reply_bytes=96*MIB, operation_ms=5000, lifetime_seconds=30),
            export_name=[["s", "ClientV5"], ["s", "fusion"]]),
        limits=dict(cpu_seconds=45, wall_seconds=120, memory_mib=512,
                    active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB),
        output_limits=dict(bytes=128*MIB, entries=4096))
    output = CHECKS/(NAME+"-plan.json")
    need(not output.exists(), "FRESH_PLAN")
    for suffix in ("", "-reader", "-custody"):
        need(not (Path(plan["workspace_root"])/(NAME+suffix)).exists(), "FRESH_WORKSPACE")
    with output.open("xb") as stream:
        stream.write(json.dumps(plan, sort_keys=True, indent=2).encode()+b"\n")
    print(json.dumps({"path": str(output), **pin(output), "source_count": 103,
                      "product_imports": 0, "executed": False}))


if __name__ == "__main__":
    main()
