"""Prepare one installed authoring request from retained data; never execute it."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PARENT = ROOT/"product-local/v5-distribution-02"
INSTALL = PARENT/"Mathematical Commons v5"
NAME = "installed-contribution-01"
MIB = 1024**2
REMOTE_SHA = "68af53270016f920822942cef153948eeacdca81b501dc461a1b8dec2a756483"
SOURCE_SHA = "2a96222392de58aaf5c10fd6f1dffd2e69045c8599fc01251a18a16d83bd60b8"
SOURCE_REQUEST = ROOT/"product-local/v5-client-owner-runs/client-retained-reuse-01/work/consumer/operations/3ccb36e321eba4294d4b5867cccfd4cc385ede3a87c071fd9708df46db8493bd/preparation/author-1/source-request.json"
SOURCE_REQUEST_SHA = "6766dc75e0c78f8026e8b7d083046c9b83d4a73519f66b689505ebc74b90af3a"
MODULE = "b42957064314b6667bf05cd3eec27ce39b925491c756a69f23a739d39ebb9f94"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path, *, directory=False, fresh=False):
    need(path.is_absolute() and path.resolve() == path
         and all(not part.is_symlink() and not part.is_junction()
                 for part in (path, *path.parents)), "ORDINARY_CANONICAL_PATH")
    if fresh:
        need(not path.exists() and path.parent.is_dir(), "FRESH_OUTPUT")
    else:
        need(path.is_dir() if directory else path.is_file(), "EXISTING_INPUT")
    return path


def read(path, maximum=MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "INPUT_SIZE_CHANGED")
    return raw


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


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
    need(len(sys.argv) == 3 and all(len(value) == 64
         and all(c in "0123456789abcdef" for c in value) for value in sys.argv[1:]),
         "ADOPTED_RELEASE_AND_REVIEWED_EXAMPLE_SHA_REQUIRED")
    release_raw = read(INSTALL/"V5-RELEASE.json", 8*MIB)
    need(sha(release_raw) == sys.argv[1], "ADOPTED_RELEASE_CHANGED")
    release = json.loads(release_raw)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V1", "RELEASE_SCHEMA")
    remote_raw = read(ROOT/"experiments/v5-local-checks/client-remote-check-01-plan.json")
    need(sha(remote_raw) == REMOTE_SHA, "EXACT_REMOTE_BASIS")
    remote = json.loads(remote_raw)
    sdk = {key: row for key, row in remote["sources"].items() if key != "owner/remote_check.py"}
    need(set(release["sdk_sources"]) == set(sdk) and len(sdk) == 102
         and all(release["files"][release["sdk_sources"][key]] == row
                 for key, row in sdk.items()), "EXACT_INSTALLED_SDK_SELECTION")
    entry = read(INSTALL/"distribution.py")
    need(release["files"]["distribution.py"] == {"bytes": len(entry), "sha256": sha(entry)},
         "INSTALLED_PUBLIC_ENTRY")
    owner_raw = read(ROOT/"software/v5/examples/contribute.py")
    need(sha(owner_raw) == sys.argv[2], "REVIEWED_EXAMPLE_CHANGED")
    request_raw = read(SOURCE_REQUEST)
    need(len(request_raw) == 63593 and sha(request_raw) == SOURCE_REQUEST_SHA,
         "EXACT_RETAINED_SOURCE_REQUEST")
    previous = json.loads(request_raw)
    source = previous["source"].encode("utf-8")
    roots = [[["s", "ClientV5"], ["s", "project_summary"]]]
    need(len(source) == 916 and sha(source) == SOURCE_SHA == previous["source_sha256"]
         and previous["roots"] == roots, "EXACT_RETAINED_LEAN_SOURCE")
    packet_pin = remote["parameters"]["packet"]
    packet_raw = read(Path(packet_pin["path"]))
    need(len(packet_raw) == packet_pin["bytes"] == 554165 and
         sha(packet_raw) == packet_pin["sha256"] ==
             "92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f",
         "EXACT_RETAINED_INPUT_PACKET")
    data, controls = PARENT/"contributor-data", PARENT/"contributor-controls"
    operations, workspace = PARENT/"operations", PARENT/"contributor-commons"
    ordinary(operations, directory=True)
    for path in (data, controls, workspace, operations/NAME, operations/(NAME+"-request")):
        ordinary(path, directory=True, fresh=True)
        need(not path.is_relative_to(INSTALL) and not INSTALL.is_relative_to(path),
             "FRESH_INSTALLATION_DISJOINT_SCOPE")
    # Create only caller inputs and the public request. The product creates its
    # own workspace/run/profile later, if root separately selects execution.
    data.mkdir()
    controls.mkdir()
    owner = write(data/"contribute.py", owner_raw)
    packet = write(data/"mixed-packet.json", packet_raw)
    source_pin = write(data/"contribution.lean", source)
    limits = dict(wall_seconds=180, controller_cpu_seconds=90, calls=64,
        input_bytes=16*MIB, worker_cpu_seconds=80, output_bytes=128*MIB, output_entries=1024,
        acquisition=dict(requests=1, reply_bytes=MIB, verify_attempts=2,
                         verification_input_bytes=4*MIB, worker_cpu_seconds=50),
        imports=dict(max_sources=2, max_members=4, max_receipts=1, max_calls=4096,
                     submitted_bytes=16*MIB, data_bytes=4*MIB))
    parameters = dict(schema="DMKN_V5_CONTRIBUTE_EXAMPLE_V1",
        runtime_adoption={"$installed": "runtime_adoption"},
        foundation={"$installed": "foundation"},
        workspace_path=str(workspace),
        workspace_config=deepcopy(remote["parameters"]["reader"]["workspace_config"]),
        create_workspace=True, operation_limits=limits,
        input=dict(mode="local-packet", module=MODULE, packet=packet),
        source=source_pin, roots=roots, export_names=deepcopy(roots),
        author_limits=dict(cpu_seconds=30, wall_seconds=60, memory_mib=768),
        admission_limits=dict(native_cpu_seconds=10, receipt_cpu_seconds=10,
                              wall_seconds=60, memory_mib=512))
    request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=NAME,
        workspace_root=str(operations), parameters=parameters,
        limits=dict(cpu_seconds=150, wall_seconds=240, memory_mib=1024,
                    active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB),
        output_limits=dict(bytes=128*MIB, entries=4096),
        owner=dict(root=str(data), entry="contribute.py",
                   sources={"contribute.py": {key: owner[key] for key in ("bytes", "sha256")}}),
        runtime_mode="aggregate")
    result = write(controls/(NAME+"-request.json"),
                   json.dumps(request, sort_keys=True, indent=2).encode("utf-8")+b"\n")
    print(json.dumps({"request": result, "release_sha256": sys.argv[1],
        "source_extraction": {"path": str(SOURCE_REQUEST), "sha256": SOURCE_REQUEST_SHA},
        "caller_inputs_staged": 3, "runtime_invoked": False, "proof_calls": 0,
        "argv": [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                 str(INSTALL/"distribution.py"), "launch", sys.argv[1], "run",
                 result["path"], result["sha256"]]}))


if __name__ == "__main__":
    main()
