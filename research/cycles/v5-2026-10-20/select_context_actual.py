"""Stage one exact installed context-to-contribution request; never execute it.

Usage: pinned installed Python -I -S -B this_file REVIEWED_ADAPTER_SHA256.
The existing release, retained mathematical input and helper remain unchanged.
Only fresh caller data, an empty run root and the public request are created.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PARENT = ROOT/"product-local/v5-distribution-connected-01"
INSTALL = PARENT/"Mathematical Commons v5"
NAME = "installed-context-contribution-01"
MIB = 1024**2
RELEASE_SHA = "69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5"
BUILD_SHA = "557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309"
BASIS_SHA = "768c80f3d06ad0cf8fbf47ed09e721b5b77a9b787f6785a448c58510930a25af"
PACKET_SHA = "6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb"
HELPER_SHA = "ce82e170e1fad04beeb0be8722c89d748e381762b4957dfaf7b5850e2a57495c"
PACKET = ROOT/(
    "product-local/v5-distribution-03/contributor-commons/operations/"
    "e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/"
    "preparation/author-1/mixed-packet.json")


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path, *, directory=False, fresh=False):
    need(path.is_absolute() and path.resolve() == path
         and all(not item.is_symlink() and not item.is_junction()
                 for item in (path, *path.parents)), "ORDINARY_CANONICAL_PATH")
    need(not path.exists() and path.parent.is_dir() if fresh
         else (path.is_dir() if directory else path.is_file()), "PATH_STATE")
    return path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size == path.stat().st_size, "INPUT_SIZE_CHANGED")
    return raw


def checked(path, expected, maximum=MIB):
    raw = read(path, maximum)
    need(sha(raw) == expected, "SELECTED_INPUT_CHANGED:"+str(path))
    return raw


def write(path, raw):
    ordinary(path, fresh=True)
    need(0 < len(raw) <= MIB, "STAGED_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    need(read(path) == raw, "STAGED_READBACK")
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    need(len(sys.argv) == 2 and len(sys.argv[1]) == 64
         and all(ch in "0123456789abcdef" for ch in sys.argv[1]),
         "REVIEWED_ADAPTER_SHA_REQUIRED")
    release = json.loads(checked(INSTALL/"V5-RELEASE.json", RELEASE_SHA, 8*MIB))
    build = json.loads(checked(ROOT/"experiments/v5-local-checks/distribution-connected-01-input.json",
                               BUILD_SHA, 8*MIB))
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V3"
         and release["base_role"] == "mathematical-client-location-v1"
         and release["build_input_sha256"] == BUILD_SHA, "EXACT_RELEASE_SELECTION")
    need(len(release["sdk_sources"]) == 106
         and set(release["sdk_sources"]) == set(build["sdk_sources"])
         and all(release["files"][release["sdk_sources"][key]]
                 == {name: row[name] for name in ("bytes", "sha256")}
                 for key, row in build["sdk_sources"].items()), "EXACT_INSTALLED_SDK_MAP")
    entry = read(INSTALL/"distribution.py")
    need(release["files"]["distribution.py"] == {"bytes": len(entry), "sha256": sha(entry)},
         "INSTALLED_PUBLIC_ENTRY")
    # The launcher revalidates selected runtime/source payloads. Do not duplicate
    # the completed full 842 MB installation readback merely to stage a request.
    basis = json.loads(checked(ROOT/"experiments/v5-local-checks/client-semantic-check-01-plan.json",
                               BASIS_SHA))
    need(basis["parameters"]["packet"] == {"path": str(PACKET), "bytes": 658554,
                                          "sha256": PACKET_SHA}, "EXACT_RETAINED_PACKET_PIN")
    packet_raw = checked(PACKET, PACKET_SHA)
    need(len(packet_raw) == 658554, "EXACT_RETAINED_PACKET_BYTES")
    adapter = checked(ROOT/"software/v5/examples/context_actual.py", sys.argv[1])
    helper = checked(ROOT/"software/v5/examples/contribution.py", HELPER_SHA)
    config = deepcopy(basis["parameters"]["reader"]["workspace_config"])
    envelope = config["packet_envelope"]
    need(envelope["deltas"] == 2 and envelope["edges"] == 3
         and envelope["claims"] == envelope["frontiers"] == 1,
         "EXACT_INPUT_ENVELOPE_BASIS")
    # Input: one I claim, two native deltas, three dependency edges. The
    # successor adds one delta using base+project_summary (two extra edges).
    # This is a fresh caller workspace configuration, never an old-state edit.
    envelope.update(deltas=3, edges=5)
    need(envelope["packet_bytes"] == config["packet_limits"]["packet_bytes"] == 16*MIB
         and config["packet_limits"]["packets"] >= 2
         and config["module_limits"]["modules"] >= 4, "SUCCESSOR_STORAGE_CAPACITY")
    limits = dict(wall_seconds=240, controller_cpu_seconds=90, calls=64,
        input_bytes=32*MIB, worker_cpu_seconds=115, output_bytes=128*MIB, output_entries=1024,
        acquisition=dict(requests=1, reply_bytes=MIB, verify_attempts=2,
                         verification_input_bytes=32*MIB, worker_cpu_seconds=70),
        imports=dict(max_sources=2, max_members=4, max_receipts=1, max_calls=4096,
                     submitted_bytes=16*MIB, data_bytes=4*MIB))
    # Reserve (1I+2native)*10 + (1I+3native)*10 = 70 checking CPU seconds,
    # including a charged repeated I claim; no cache-hit assumption funds work.
    # The separate author allowance is 115-70=45 CPU seconds. One input import
    # has three warranted members (two selected); the child closure has four.
    author = dict(cpu_seconds=45, wall_seconds=90, memory_mib=768)
    admission = dict(native_cpu_seconds=10, receipt_cpu_seconds=10,
                     wall_seconds=60, memory_mib=512)

    data, controls = PARENT/"context-data", PARENT/"context-controls"
    operations, workspace = PARENT/"context-operations", PARENT/"context-commons"
    ordinary(INSTALL, directory=True)
    for path in (data, controls, operations, workspace):
        ordinary(path, directory=True, fresh=True)
        need(not path.is_relative_to(INSTALL) and not INSTALL.is_relative_to(path),
             "FRESH_INSTALLATION_DISJOINT_SCOPE")
    # A fresh entire operation root implies neither public run nor request
    # directory can already exist. Do not create the actual mathematical state.
    data.mkdir()
    controls.mkdir()
    operations.mkdir()
    owner = write(data/"context_actual.py", adapter)
    helper_pin = write(data/"contribution.py", helper)
    packet = write(data/"project-summary-packet.json", packet_raw)
    parameters = dict(schema="DMKN_V5_CONTEXT_ACTUAL_V1",
        runtime_adoption={"$installed": "runtime_adoption"},
        foundation={"$installed": "foundation"}, workspace_path=str(workspace),
        workspace_config=config, operation_limits=limits, packet=packet,
        author_limits=author, admission_limits=admission)
    request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=NAME,
        workspace_root=str(operations), parameters=parameters,
        limits=dict(cpu_seconds=240, wall_seconds=300, memory_mib=1024,
                    active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB),
        output_limits=dict(bytes=128*MIB, entries=4096),
        owner=dict(root=str(data), entry="context_actual.py", sources={
            "context_actual.py": {key: owner[key] for key in ("bytes", "sha256")},
            "contribution.py": {key: helper_pin[key] for key in ("bytes", "sha256")}}),
        runtime_mode="aggregate")
    result = write(controls/(NAME+"-request.json"),
                   json.dumps(request, sort_keys=True, indent=2).encode("utf-8")+b"\n")
    print(json.dumps({"request": result, "release_sha256": RELEASE_SHA,
        "source_basis_sha256": BASIS_SHA, "caller_inputs_staged": 3,
        "runtime_invoked": False, "proof_calls": 0,
        "reservation": {"input_admission_cpu": 30, "output_admission_cpu": 40,
                        "author_cpu": 45, "cache_hits_assumed": False},
        "argv": [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                 str(INSTALL/"distribution.py"), "launch", RELEASE_SHA, "run",
                 result["path"], result["sha256"]]}))


if __name__ == "__main__":
    main()
