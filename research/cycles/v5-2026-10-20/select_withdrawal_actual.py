"""Stage one persisted-withdrawal public-owner control; never launch/import it.

Use installed Python -I -S -B this_file REVIEWED_SOURCE_HASHES_JSON.
Four selected SDK replacements plus one new trust helper; one fresh owner.
Existing binaries, runtimes, installations, inputs and used evidence stay intact.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT/"experiments/v5-local-checks"
PARENT = ROOT/"product-local/v5-distribution-interface-01"
INSTALL = PARENT/"Mathematical Commons v5"
NAME = "trust-withdrawal-actual-01"
MIB = 1024**2
BASIS = PARENT/"evaluator-operations/installed-evaluator-method-01/plan.json"
BASIS_SHA = "66fc6f10c400f693cf870ce9e7c17f9f9029c39ad1086d06436dd981b126c410"
RELEASE_SHA = "c249d086928e62a00ec194f1b556c6cffa918c1106159102e32a8617c9fbadf0"
BASE_MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
OVERLAYS = {
    "v5/admission/trust.py": "admission/trust.py",
    "v5/admission/verifier.py": "admission/verifier.py",
    "v5/aggregate_claims/aggregate_admission.py": "aggregate_claims/aggregate_admission.py",
    "v5/client/runtime.py": "client/runtime.py",
    "v5/client/remote_reader.py": "client/remote_reader.py",
}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def ordinary(path, *, directory=False, fresh=False):
    need(path.is_absolute() and path.resolve() == path
         and all(not part.is_symlink() and not part.is_junction()
                 for part in (path, *path.parents)), "ORDINARY_CANONICAL_PATH")
    need(not path.exists() and path.parent.is_dir() if fresh
         else (path.is_dir() if directory else path.is_file()), "PATH_STATE:"+str(path))
    return path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def checked(path, expected, maximum=2*MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size == path.stat().st_size and sha(raw) == expected,
         "SELECTED_INPUT_CHANGED:"+str(path))
    return raw


def encoded(value):
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode()+b"\n"


def write(path, raw):
    ordinary(path, fresh=True)
    need(0 < len(raw) <= 2*MIB, "STAGED_FILE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    need(checked(path, sha(raw)) == raw, "STAGED_READBACK")
    return {"bytes": len(raw), "sha256": sha(raw)}


def fresh_directory(path):
    ordinary(path, directory=True, fresh=True)
    path.mkdir()


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    need(len(sys.argv) == 2 and len(sys.argv[1]) <= 32768, "REVIEWED_MAP_ARGUMENT")
    reviewed = json.loads(sys.argv[1])
    required = {"software/v5/trust_withdrawal/"+name for name in (*OVERLAYS.values(), "actual.py")}
    need(type(reviewed) is dict and set(reviewed) == required, "EXACT_REVIEWED_SOURCE_SET")
    need(all(type(value) is str and len(value) == 64
             and all(ch in "0123456789abcdef" for ch in value) for value in reviewed.values()),
         "REVIEWED_HASH_FORMAT")
    pending = {key: checked(ROOT/key, digest) for key, digest in reviewed.items()}
    prior = json.loads(checked(BASIS, BASIS_SHA))
    release = json.loads(checked(INSTALL/"V5-RELEASE.json", RELEASE_SHA, 8*MIB))
    checked(INSTALL/"base/RELEASE-MANIFEST.json", BASE_MANIFEST_SHA, 8*MIB)
    need(prior["schema"] == "DMKN_V5_CLIENT_LAUNCH_V1"
         and prior["name"] == "installed-evaluator-method-01"
         and prior["installation_root"] == str(INSTALL/"base"), "EXACT_PRIOR_LAUNCH")
    need(prior["source_roots"]["v5"] == str(INSTALL/"sdk/v5")
         and prior["source_roots"]["portable"] == str(INSTALL/"sdk/portable")
         and len(prior["sources"]) == 109, "EXACT_PRIOR_SOURCE_ROOTS")
    old_sdk = {key: row for key, row in prior["sources"].items()
               if key.startswith(("v5/", "portable/"))}
    need(len(old_sdk) == 108 and set(old_sdk) == set(release["sdk_sources"])
         and all(row == release["files"][release["sdk_sources"][key]]
                 for key, row in old_sdk.items()), "EXACT_PRIOR_INSTALLED_MAP")
    # Validate/retain only the ~1.2 MB selected source graph, not another full
    # installation readback. Existing launcher/owners check their runtime pins.
    held = {}
    for key, row in old_sdk.items():
        role, relative = key.split("/", 1)
        raw = checked(Path(prior["source_roots"][role])/relative, row["sha256"])
        need(len(raw) == row["bytes"], "EXACT_PRIOR_SOURCE_BYTES")
        if role == "v5":
            held[key] = raw
    need(len(held) == 87, "EXACT_PRIOR_V5_CENSUS")
    for key, name in OVERLAYS.items():
        held[key] = pending["software/v5/trust_withdrawal/"+name]
    need(len(held) == 88, "EXACT_NEW_V5_CENSUS")
    params = deepcopy(prior["parameters"])
    for key in ("receipt", "bundle", "foundation"):
        row = params[key]
        need(len(checked(Path(row["path"]), row["sha256"])) == row["bytes"], "RETAINED_DATA_PIN")
    profile = params["runtime_adoption"]["preparation_profile"]
    need(len(checked(Path(profile["path"]), profile["sha256"])) == profile["bytes"],
         "RETAINED_PREPARATION_PROFILE")
    need(params["schema"] == "DMKN_V5_EVALUATOR_METHOD_ACTUAL_V1"
         and params["receipt"]["sha256"] == "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"
         and params["bundle"]["sha256"] == "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"
         and params["workspace_config"]["max_operations"] == 1,
         "EXACT_OPERATION_BASIS")

    inputs = CHECKS/(NAME+"-inputs")
    operations = CHECKS/(NAME+"-runs")
    workspace = CHECKS/(NAME+"-commons")
    domain = CHECKS/(NAME+"-domain")
    for path in (inputs, operations, workspace, domain):
        ordinary(path, directory=True, fresh=True)
        need(path.is_relative_to(CHECKS) and not path.is_relative_to(INSTALL)
             and not INSTALL.is_relative_to(path), "FRESH_CANONICAL_OUTPUT_SCOPE")
    need(not (operations/NAME).exists(), "FRESH_ACTUAL_RUN")
    # Everything was validated before any staged file was created. Failures
    # preserve partial fresh output; no cleanup/retry/overwrite is automatic.
    fresh_directory(inputs)
    fresh_directory(operations)
    fresh_directory(inputs/"sdk")
    fresh_directory(inputs/"sdk/v5")
    fresh_directory(inputs/"owner")
    selected = {key: deepcopy(row) for key, row in old_sdk.items() if key.startswith("portable/")}
    for key, raw in sorted(held.items()):
        path = inputs/"sdk"/key
        missing = []
        parent = path.parent
        while not parent.exists():
            missing.append(parent); parent = parent.parent
        for directory in reversed(missing):
            fresh_directory(directory)
        selected[key] = write(path, raw)
    selected["owner/actual.py"] = write(inputs/"owner/actual.py",
        pending["software/v5/trust_withdrawal/actual.py"])
    need(len(selected) == 110, "EXACT_SELECTED_SOURCE_CENSUS")
    params = {key: params[key] for key in ("runtime_adoption", "foundation",
        "workspace_config", "operation_limits", "receipt", "bundle", "receipt_limits")}
    params.update(schema="DMKN_V5_WITHDRAWAL_ACTUAL_V1", workspace_path=str(workspace),
        domain_path=str(domain), domain_id=sha(b"DMKN owner adoption: trust-withdrawal-actual-01"))
    params["workspace_config"]["max_operations"] = 2
    params["operation_limits"].update(wall_seconds=120, worker_cpu_seconds=10)
    params["operation_limits"]["acquisition"].update(verify_attempts=1, worker_cpu_seconds=10)
    need(params["receipt_limits"] == dict(cpu_seconds=10, wall_seconds=60, memory_mib=512),
         "ONE_EXISTING_RECEIPT_ENVELOPE")
    plan = deepcopy(prior)
    plan.update(name=NAME, workspace_root=str(operations), owner_entry="actual.py",
        source_roots={"v5": str(inputs/"sdk/v5"), "portable": prior["source_roots"]["portable"],
                      "owner": str(inputs/"owner")}, sources=selected, parameters=params,
        limits=dict(cpu_seconds=120, wall_seconds=180, memory_mib=1024,
                    active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB))
    need(plan["output_limits"] == dict(bytes=128*MIB, entries=4096),
         "UNCHANGED_OUTPUT_ENVELOPE")
    plan_path = inputs/"plan.json"
    plan_pin = write(plan_path, encoded(plan))
    report = {"schema": "DMKN_V5_WITHDRAWAL_ACTUAL_SELECTION_V1", "basis_plan_sha256": BASIS_SHA,
        "plan": {"path": str(plan_path), **plan_pin}, "reviewed_sources": reviewed,
        "source_count": len(selected), "sdk_files": len(held),
        "runtime_invoked": False, "proof_calls": 0, "author_calls": 0, "native_calls": 0,
        "network_calls": 0, "release_rebuilt": False,
        "scope": "ONE_EXISTING_RECEIPT_AND_PERSISTENT_WITHDRAWAL_NOT_NEW_PUBLIC_DISTRIBUTION",
        "argv": [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                 str(inputs/"sdk/v5/client/launch.py"), str(plan_path), plan_pin["sha256"]]}
    report_pin = write(inputs/"SELECTION.json", encoded(report))
    print(json.dumps({**report, "selection": {"path": str(inputs/"SELECTION.json"), **report_pin}}))


if __name__ == "__main__":
    main()

