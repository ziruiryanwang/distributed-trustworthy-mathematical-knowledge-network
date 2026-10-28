"""One new relocated preparer handoff using retained authentic directory specs.

No owner, proof, service, Lean or previously passing lookup/preview campaign.
Outer Run-V5-Check Job owns this controller and its one inert CLI child.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PROFILE = "7687d5276d8a7edc0beeb7066e4cbaae16529b0e88d8a0728b003dad04a4dd34"
DIRECTORY_RESULT = ROOT/"experiments/v5-local-checks/name-directory-lookup01/checks/positive-result/RESULT.json"
DIRECTORY_SHA = "f6ce728d0d5396ddc99fb9eb71a158a98daa6de0b4a897e6ddabd860cad43822"
PRIOR_CONFIG = ROOT/"experiments/v5-local-checks/advisory-query-find-prepared01/config.json"
PRIOR_SHA = "463c3aee55ded3338098dca9f092b6532cd05c501f412deda3db601c6cb758f9"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError("DIRECTORY_KIT_CONTROL_" + code)


def read(path, maximum=MIB):
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "INPUT_CHANGED")
    return raw


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("ascii")
    with path.open("xb") as stream:
        stream.write(raw)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("kit", "manifest-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "PYTHON")
    kit, output = Path(args.kit), Path(args.output)
    need(kit.is_absolute() and output.is_absolute() and not output.exists() and
         output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         Path.cwd() == ROOT, "PATHS")
    manifest_raw = read(kit/"KIT-MANIFEST.json", 2*MIB)
    need(sha(manifest_raw) == args.manifest_sha256, "MANIFEST_PIN")
    manifest = json.loads(manifest_raw)
    need(manifest["profile_sha256"] == PROFILE, "PROFILE")
    selected = {}
    for role in ("operator/prepare.py", "operator/prepare_selected.py", "operator/compatibility.json",
                 "package/PROFILE.json"):
        raw = read(kit/role, 2*MIB)
        need({"bytes": len(raw), "sha256": sha(raw)} == manifest["files"][role], "ROLE_PIN")
        selected[role] = raw
    directory_raw, prior_raw = read(DIRECTORY_RESULT), read(PRIOR_CONFIG)
    need(sha(directory_raw) == DIRECTORY_SHA and sha(prior_raw) == PRIOR_SHA, "INPUT_PIN")
    directory, prior = json.loads(directory_raw), json.loads(prior_raw)
    need(directory["specs"] == prior["specs"] and directory["mathematical_acceptance"] is False,
         "AUTHENTIC_SPECS")
    request = dict(prior, specs=directory["specs"], action="find",
                   operation_output=str(output/"unexecuted-find"))
    output.mkdir()
    save(output/"request.json", request)
    argv = [sys.executable, "-I", "-S", "-B", str(kit/"operator/prepare_selected.py"),
            "--package", str(kit/"package"), "--profile-sha256", PROFILE,
            "--request", str(output/"request.json"), "--output", str(output/"prepared")]
    child = subprocess.run(argv, cwd=kit, capture_output=True, timeout=45)
    need(len(child.stdout) <= MIB and len(child.stderr) <= MIB, "LOG_BOUND")
    for label, raw in (("stdout.txt", child.stdout), ("stderr.txt", child.stderr)):
        with (output/label).open("xb") as stream:
            stream.write(raw)
    need(child.returncode == 0 and child.stderr == b"", "CLI_SUCCESS")
    result = json.loads(child.stdout)
    actual = json.loads(read(output/"prepared/config.json"))
    arguments = json.loads(read(output/"prepared/arguments.json"))
    need(actual == prior and arguments["profile_sha256"] == PROFILE and
         arguments["entry"] == "peer" and arguments["arguments"][0] == "find" and
         arguments["mathematical_acceptance"] is False and
         not (output/"unexecuted-find").exists(), "INERT_HANDOFF")
    need(result["known_noncompiled_roles"] == 50 and result["mathematical_acceptance"] is False,
         "NEW_INTERFACE")
    need(read(kit/"KIT-MANIFEST.json", 2*MIB) == manifest_raw and
         read(DIRECTORY_RESULT) == directory_raw and read(PRIOR_CONFIG) == prior_raw and
         all(read(kit/role, 2*MIB) == raw for role, raw in selected.items()), "INPUTS_UNCHANGED")
    report = dict(status="PASS_RELOCATED_DIRECTORY_FIND_PREPARATION", profile_sha256=PROFILE,
        manifest_sha256=args.manifest_sha256, directory_result_sha256=DIRECTORY_SHA,
        prior_config_sha256=PRIOR_SHA, config_unchanged=True, known_noncompiled_roles=50,
        child_exit_code=child.returncode, stdout_sha256=sha(child.stdout), stderr_sha256=sha(child.stderr),
        owner_opened=False, native_calls=0, network_calls=0, mathematical_acceptance=False)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
