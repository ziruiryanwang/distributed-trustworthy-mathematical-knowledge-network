"""Stage two pinned caller inputs and one public request; never launch software."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PARENT = ROOT/"product-local/v5-distribution-02"
INSTALL = PARENT/"Mathematical Commons v5"
NAME = "relocated-remote-01"
MIB = 1024**2
REMOTE_SHA = "68af53270016f920822942cef153948eeacdca81b501dc461a1b8dec2a756483"
OWNER_SHA = "e2405b7c59cbd9ee1b4bf84e045aeaee2d7f0131812b9bcc3965ecc85ee6c5eb"
PACKET_SHA = "92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f"


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


def pin(path, maximum=MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "INPUT_SIZE_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": hashlib.sha256(raw).hexdigest()}


def copy_exact(source, target, expected):
    need(pin(source) == {"path": str(source), **expected}, "EXACT_CALLER_INPUT")
    ordinary(target, fresh=True)
    with source.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
         "CALLER_INPUT_CHANGED")
    with target.open("xb") as stream:
        stream.write(raw)
    result = pin(target)
    need({key: result[key] for key in ("bytes", "sha256")} == expected, "COPY_READBACK")
    return result


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    need(len(sys.argv) == 2 and len(sys.argv[1]) == 64
         and all(c in "0123456789abcdef" for c in sys.argv[1]),
         "ADOPTED_INSTALLED_RELEASE_SHA_REQUIRED")
    release_path = INSTALL/"V5-RELEASE.json"
    need(pin(release_path, 8*MIB)["sha256"] == sys.argv[1], "ADOPTED_RELEASE_CHANGED")
    release = json.loads(release_path.read_bytes())
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V1"
         and release["base_manifest_sha256"] ==
             "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed",
         "EXACT_BASE_ADOPTION")
    remote_path = ROOT/"experiments/v5-local-checks/client-remote-check-01-plan.json"
    need(pin(remote_path)["sha256"] == REMOTE_SHA, "EXACT_REMOTE_BASIS")
    remote = json.loads(remote_path.read_bytes())
    sdk = {key: row for key, row in remote["sources"].items() if key != "owner/remote_check.py"}
    need(set(release["sdk_sources"]) == set(sdk) and len(sdk) == 102
         and all(release["files"][release["sdk_sources"][key]] == row
                 for key, row in sdk.items()), "EXACT_RELOCATED_SDK_SELECTION")
    entry = pin(INSTALL/"distribution.py", 2*MIB)
    need({key: entry[key] for key in ("bytes", "sha256")} == release["files"]["distribution.py"],
         "INSTALLED_PUBLIC_ENTRY")
    owner_pin = remote["sources"]["owner/remote_check.py"]
    packet_pin = remote["parameters"]["packet"]
    need(owner_pin["sha256"] == OWNER_SHA and packet_pin["sha256"] == PACKET_SHA
         and packet_pin["bytes"] == 554165, "EXACT_RETAINED_CALLER_DATA")
    caller, workspace, controls = (PARENT/name for name in ("caller-data", "operations", "controls"))
    ordinary(INSTALL, directory=True)
    for path in (caller, workspace, controls):
        ordinary(path, directory=True, fresh=True)
        need(not path.is_relative_to(INSTALL) and not INSTALL.is_relative_to(path),
             "CALLER_INSTALLATION_DISJOINT")
    # Root explicitly selects this staging invocation. Partial failures remain;
    # there is no overwrite, cleanup, retry, execution or allowance renewal.
    for path in (caller, workspace, controls):
        path.mkdir()
    copy_exact(Path(remote["source_roots"]["owner"])/"remote_check.py",
               caller/"remote_check.py", owner_pin)
    packet = copy_exact(Path(packet_pin["path"]), caller/"mixed-packet.json",
                       {key: packet_pin[key] for key in ("bytes", "sha256")})
    parameters = deepcopy(remote["parameters"])
    parameters["packet"] = packet
    parameters["reader"]["runtime_adoption"] = {"$installed": "runtime_adoption"}
    parameters["reader"]["foundation"] = {"$installed": "foundation"}
    parameters["reader"]["workspace_path"] = str(workspace/(NAME+"-reader"))
    request = dict(schema="DMKN_V5_INSTALLED_REQUEST_V1", name=NAME,
        workspace_root=str(workspace), parameters=parameters,
        limits=deepcopy(remote["limits"]), output_limits=deepcopy(remote["output_limits"]),
        owner=dict(root=str(caller), entry="remote_check.py",
                   sources={"remote_check.py": deepcopy(owner_pin)}),
        runtime_mode="aggregate")
    raw = json.dumps(request, sort_keys=True, indent=2).encode("utf-8")+b"\n"
    need(len(raw) <= MIB, "REQUEST_BOUND")
    request_path = controls/(NAME+"-request.json")
    with request_path.open("xb") as stream:
        stream.write(raw)
    request_pin = pin(request_path)
    print(json.dumps({"request": request_pin, "release_sha256": sys.argv[1],
        "argv": [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                 str(INSTALL/"distribution.py"), "launch", sys.argv[1], "run",
                 str(request_path), request_pin["sha256"]],
        "caller_inputs_copied": 2, "runtime_invoked": False, "proof_calls": 0}))


if __name__ == "__main__":
    main()
