"""Stage a small exact source map for one retained-result semantic integration.

No product import, owner construction, proof, installation build or execution.
The original installed source, mathematical evidence and workspace stay intact.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT/"experiments/v5-local-checks"
NAME = "client-semantic-check-01"
SOURCE_ROOT = ROOT/"product-local/v5-semantic-reader-source-01"
RUN_ROOT = ROOT/"product-local/v5-semantic-reader-runs"
MIB = 1024**2


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path, "CANONICAL_PATH")
    for item in (path, *path.parents[:-1]):
        info = item.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400, "NO_REPARSE_PATH")
    need(stat.S_ISREG(path.stat().st_mode), "REGULAR_FILE")
    return path


def pin(path, maximum=2*MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "INPUT_SIZE_BOUND")
    raw = path.read_bytes()
    need(len(raw) == size and path.stat().st_size == size, "STABLE_INPUT_SIZE")
    return raw, {"bytes": size, "sha256": hashlib.sha256(raw).hexdigest()}


def exact(path, digest, maximum=2*MIB):
    raw, row = pin(path, maximum)
    need(row["sha256"] == digest, "EXACT_SOURCE:"+str(path))
    return raw, row


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
    need(path.read_bytes() == raw, "FRESH_WRITE_READBACK")


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    need(len(sys.argv) == 2 and re.fullmatch(r"[0-9a-f]{64}", sys.argv[1]),
         "REVIEWED_ADAPTER_HASH_REQUIRED")
    prior_path = ROOT/"product-local/v5-distribution-03/operations/relocated-remote-01/plan.json"
    raw, unused = exact(prior_path,
        "1d583332afc9ba01610196ec59cbcf301348cc99cc8917f6070d5380358a80d7")
    old = json.loads(raw)
    need(old["owner_entry"] == "remote_check.py" and len(old["sources"]) == 104,
         "EXACT_INSTALLED_READER_BASIS")
    payloads, sources = {}, {}
    for key, expected in old["sources"].items():
        if key.startswith("owner/"):
            need(key == "owner/remote_check.py", "EXACT_OLD_OWNER")
            continue
        role, relative = key.split("/", 1)
        parts = PurePosixPath(relative)
        need(role in ("v5", "portable") and parts.as_posix() == relative
             and not parts.is_absolute() and ".." not in parts.parts, "SOURCE_RELATIVE")
        data, actual = pin(Path(old["source_roots"][role]).joinpath(*parts.parts))
        need(actual == expected, "INSTALLED_SDK_PIN:"+key)
        payloads[key], sources[key] = data, actual
    changes = (
        ("v5/client/workspace_staged.py", "software/v5/staging_members/workspace_staged.py",
         "1a0922c395eb233f6fb4f1e8b10b5c538d69d445c732a9ae492539b568877f8d"),
        ("v5/client/semantic_reader.py", "software/v5/client/semantic_reader.py",
         "175de65f72f056681237387c854d21671d7b3787b61f6685789a382b8a06ae18"),
        ("owner/semantic_check.py", "software/v5/client/semantic_check.py", sys.argv[1]),
    )
    for key, relative, digest in changes:
        need((key in sources) == (key == "v5/client/workspace_staged.py"),
             "EXACT_SOURCE_DELTA")
        payloads[key], sources[key] = exact(ROOT/relative, digest)
    need(len(sources) == 105 and sum(map(len, payloads.values())) <= 4*MIB,
         "SMALL_SOURCE_MAP_BOUND")
    need(not any("/test_" in key or "actual_assets" in key or "terminal_assets" in key
                 for key in sources), "NO_TEST_FIXTURE_AUTHORITY")
    reader = deepcopy(old["parameters"]["reader"])
    packet_path = ROOT/(
        "product-local/v5-distribution-03/contributor-commons/operations/"
        "e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/"
        "preparation/author-1/mixed-packet.json")
    packet_raw, packet = exact(packet_path,
        "6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb")
    need(len(packet_raw) == 658554, "EXACT_RETAINED_CONTRIBUTION")
    packet = {"path": str(packet_path), **packet}
    # Changed-boundary allocations are chosen before the only possible run.
    # They cover up to 32 acquisitions and 256 public calls, not a renewal.
    reader["operation_limits"] = {
        "wall_seconds": 120, "controller_cpu_seconds": 90, "calls": 256,
        "input_bytes": 32*MIB, "worker_cpu_seconds": 30,
        "output_bytes": 128*MIB, "output_entries": 1024,
        "acquisition": {"requests": 32, "reply_bytes": 16*MIB,
            "verify_attempts": 1, "verification_input_bytes": MIB,
            "worker_cpu_seconds": 30},
        "imports": {"max_sources": 2, "max_members": 4, "max_receipts": 1,
            "max_calls": 4096, "submitted_bytes": 16*MIB, "data_bytes": 4*MIB},
    }
    reader["query"]["contact_lifetime_ms"] = 75000
    reader["query"]["search_limits"]["wall_ms"] = 30000
    reader["query"]["admission"].update(native_cpu_seconds=10,
        receipt_cpu_seconds=10, wall_seconds=30, memory_mib=512)
    reader.update(workspace_path=str(RUN_ROOT/(NAME+"-reader")), create_workspace=True)
    plan = deepcopy(old)
    plan.update(name=NAME, workspace_root=str(RUN_ROOT),
        source_roots={role: str(SOURCE_ROOT/role) for role in ("v5", "portable", "owner")},
        sources=sources, owner_entry="semantic_check.py",
        parameters={"schema": "DMKN_V5_SEMANTIC_CHECK_V1", "packet": packet,
            "reader": reader, "export_name": [["s", "ClientV5"], ["s", "project_summary"]],
            "helper_limits": {"modules": 4, "names": 32, "groups": 32,
                "bodies": 32, "steps": 128, "data_bytes": 4*MIB},
            "max_rounds": 32, "semantic_max_bytes": MIB,
            "service_limits": {"max_connections": 2, "max_requests": 32,
                "max_reply_bytes": 96*MIB, "operation_ms": 5000,
                "lifetime_seconds": 75}},
        limits={"cpu_seconds": 105, "wall_seconds": 150, "memory_mib": 512,
            "active_processes": 4, "stdout_bytes": MIB, "stderr_bytes": MIB},
        output_limits={"bytes": 128*MIB, "entries": 4096})
    output = CHECKS/(NAME+"-plan.json")
    need(not SOURCE_ROOT.exists() and not RUN_ROOT.exists() and not output.exists(),
         "FRESH_SOURCES_RUNS_AND_PLAN")
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
        "argv": [str(python), "-I", "-S", "-B",
                 str(SOURCE_ROOT/"v5/client/launch.py"), str(output), result["sha256"]]}))


if __name__ == "__main__":
    main()
