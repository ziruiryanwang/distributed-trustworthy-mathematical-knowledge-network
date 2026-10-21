"""Finite real-constructor M -> M+V integration; never a peer entry point.

One explicitly adopted owner, one retained I verification, two native checks,
one exact warm-prefix reuse. No proof production, authoring, imports or network.
Run only through the selected bounded runner. Saved reports grant no authority.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib
import json
import os
import stat
import sys

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MIB = 1024**2
MAP_BYTES = 2805479
MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
REPLACEMENTS = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py",
        "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py": ("standalone_validation/mixed_claims/imports_atomic.py",
        "8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py",
        "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
}
PACKETS = (
    (498641, "efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b"),
    (549456, "30566df7734d2d0d407cc553b923617453a3162c68a36afafe9a970eb4eb8dfc"),
)
MODULES = (
    "bbf0845d2622374699a93a9d8ccc6e565dd1c985e72441ec0eeae41bb03fc0c5",
    "540f82c8f0b75c4703074c92f5de514f33d2fb84ec45317b672fadb4fe946c17",
)
GROUP_ROOTS = (
    "f0505daeabecea8f16b53feb8674db02233578dc02e8e775a70f3c2de1ffcc16",
    "d25b0ad3365251ea432d7696152612e6b721282740456af8d7c61140308ce341",
)
WITNESSES = (
    (50017, "8b84084486b0aadceb9ee353a28654b2777e297a726693135c575d5c50e85f5a"),
    (50814, "bca4534a839390c72732f40d9a3665bdb8f12c7039cbc1656920b789ff308b48"),
)
HELPERS = ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py")
EXECUTED = "NATIVE_EXECUTED_CONDITIONAL_CHECK"
REUSED = "SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION"


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path, directory=False):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts and path.is_relative_to(PROJECT),
         "CANONICAL_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not (getattr(info, "st_file_attributes", 0)
             & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)), "REDIRECTED_PATH")
    need(path.is_dir() if directory else path.is_file(), "ORDINARY_PATH_KIND")
    return path


def read(path, limit):
    path = ordinary(path)
    need(0 < path.stat().st_size <= limit, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    need(0 < len(raw) <= limit, "READ_BOUND")
    return raw


def pin(row, limit=128*MIB):
    need(type(row) is dict and set(row) == {"path", "bytes", "sha256"}, "FILE_ROW")
    need(type(row["bytes"]) is int and 0 < row["bytes"] <= limit
         and type(row["sha256"]) is str and len(row["sha256"]) == 64
         and all(ch in "0123456789abcdef" for ch in row["sha256"]), "FILE_PIN_SHAPE")
    path = ordinary(row["path"])
    need(path.stat().st_size == row["bytes"], "FILE_PIN_SIZE")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(digest == row["sha256"] and path.stat().st_size == row["bytes"], "FILE_PIN_CHANGED")
    return path


def pair(row):
    return {key: row[key] for key in ("bytes", "sha256")}


def write_new(path, raw):
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())


def save(path, value):
    write_new(path, json.dumps(value, sort_keys=True, separators=(",", ":"),
                               allow_nan=False).encode() + b"\n")


def stage(output, map_row):
    need(map_row["sha256"] == MAP_SHA and map_row["bytes"] == MAP_BYTES, "CURRENT_MAP_IDENTITY")
    raw = read(pin(map_row, MAP_BYTES), MAP_BYTES)
    need(sha(raw) == MAP_SHA, "MAP_READBACK")
    basis = json.loads(raw)["sdk_sources"]
    need(type(basis) is dict and len(basis) == 114 and set(REPLACEMENTS) <= set(basis),
         "CURRENT_MAP_SHAPE")
    code = output / "selected-code"
    code.mkdir()
    selected = {}
    for logical, row in sorted(basis.items()):
        relative = PurePosixPath(logical)
        need(not relative.is_absolute() and relative.as_posix() == logical
             and all(part not in ("", ".", "..") and "\\" not in part for part in relative.parts),
             "LOGICAL_SOURCE_PATH")
        if logical in REPLACEMENTS:
            name, expected = REPLACEMENTS[logical]
            source = SOURCE/name
            contents = read(source, 2*MIB)
            size = len(contents)
        else:
            source = SOURCE/Path(row["path"]).relative_to(PROJECT/"software/v5")
            expected, size = row["sha256"], row["bytes"]
            contents = read(source, 2*MIB)
        need(len(contents) == size and sha(contents) == expected, "SELECTED_SOURCE_PIN:"+logical)
        target = code.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, contents)
        need(read(target, 2*MIB) == contents, "STAGED_SOURCE_READBACK")
        selected[logical] = {"path": str(target), "source": str(source),
                             "bytes": size, "sha256": expected}
    need(not any(name in sys.modules for name in ("admission", "mixed_claims", "modules")),
         "EARLY_PRODUCT_IMPORT")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return selected


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--output", required=True)
    args.add_argument("--input", required=True)
    argv = args.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_OWNER")
    output = ordinary(argv.output, directory=True)
    input_path = ordinary(argv.input)
    input_raw = read(input_path, MIB)
    request = json.loads(input_raw)
    need(type(request) is dict and set(request) == {"schema", "map", "installation",
         "supervisor_manifest", "native", "receipt", "python_runtime", "packets"}
         and request["schema"] == "DMKN_INCREMENTAL_NATIVE_INTEGRATION_INPUT_V1", "INPUT_SCHEMA")
    installation = ordinary(request["installation"], directory=True)
    manifest_path = pin(request["supervisor_manifest"], 8*MIB)
    need(manifest_path == installation/"base/RELEASE-MANIFEST.json", "SUPERVISOR_INSTALLATION")
    manifest_raw = read(manifest_path, 8*MIB)
    need(sha(manifest_raw) == request["supervisor_manifest"]["sha256"], "MANIFEST_READBACK")
    manifest = json.loads(manifest_raw)
    native, receipt = pin(request["native"]), pin(request["receipt"])
    need(native == installation/"assets/native/native_delta.exe"
         and receipt == installation/"assets/receipt/module_host.exe", "EXECUTABLE_ROLES")
    runtime = request["python_runtime"]
    need(type(runtime) is list and len(runtime) == 18, "PYTHON_RUNTIME_COUNT")
    runtime_pins = {str(pin(row)): pair(row) for row in runtime}
    need(len(runtime_pins) == 18 and str(Path(sys.executable).resolve()) in runtime_pins,
         "ACTUAL_SELECTED_PYTHON")
    packet_rows = request["packets"]
    need(type(packet_rows) is list and len(packet_rows) == 2, "PACKET_PAIR")
    packet_bytes = []
    for row, expected in zip(packet_rows, PACKETS):
        need((row["bytes"], row["sha256"]) == expected, "EXACT_RETAINED_PACKET")
        contents = read(pin(row, MIB), MIB)
        need((len(contents), sha(contents)) == expected, "PACKET_READBACK")
        packet_bytes.append(contents)
    selected = stage(output, request["map"])
    source_pins = {row["path"]: pair(row) for name, row in selected.items() if name.endswith(".py")}
    need(len(source_pins) == 100, "EXACT_PYTHON_SOURCE_COUNT")
    C = importlib.import_module("modules.codec")
    T = importlib.import_module("admission.trust")
    V = importlib.import_module("admission.verifier")
    M = importlib.import_module("mixed_claims.receiver")
    B = importlib.import_module("aggregate_claims.bindings")
    roles = {"source/"+name: pair(row) for name, row in selected.items()}
    roles.update({"runtime/"+str(index): pair(row) for index, row in enumerate(runtime)})
    for name in ("supervisor_manifest", "native", "receipt", "map"):
        roles["configuration/"+name] = pair(request[name])
    for name in HELPERS:
        row = {"path": str(manifest_path.parent/name), **manifest["files"][name]}
        pin(row, 4*MIB)
        roles["supervisor/"+name] = pair(row)
    own = read(Path(__file__).resolve(), 2*MIB)
    roles["owner/adapter"] = {"bytes": len(own), "sha256": sha(own)}
    roles["owner/request"] = {"bytes": len(input_raw), "sha256": sha(input_raw)}
    support = {"schema": T.SUPPORT_SCHEMA, "identities": {"relation_image": B.RELATION_IMAGE,
        "aggregate_image": None, "foundation": B.FOUNDATION, "policy": B.POLICY,
        "receipt_scheme": "resolved-succinct-poseidon2"}, "roles": roles}
    receipt_pins = {**source_pins, **runtime_pins, str(receipt): pair(request["receipt"])}
    native_pins = {**source_pins, str(native): pair(request["native"])}
    need(len(receipt_pins) == 119 and len(native_pins) == 101, "EXACT_OWNER_PIN_COUNTS")
    save(output/"integration-sources.json", selected)
    save(output/"integration-support.json", support)
    domain = receipt_owner = mixed = None
    observations, cleanup, errors = [], {}, []
    try:
        domain = T.TrustDomain.create(output/"trust", sha(str(output).encode()+input_raw), support)
        need(domain.identity()["support_id"] == T.support_id(support), "EXACT_ADOPTED_SUPPORT")
        receipt_owner = V.ReceiptVerifier(supervisor_manifest=str(manifest_path),
            supervisor_manifest_sha256=request["supervisor_manifest"]["sha256"],
            executable=str(receipt), runtime_pins=receipt_pins, image_id=B.RELATION_IMAGE,
            foundation=B.FOUNDATION, policy=B.POLICY, operations=1, submitted_bytes=223594,
            reserved_cpu_seconds=10, wall_seconds=150, trust_binding=domain.bind())
        mixed = M.MixedDeltaVerifier(legacy_verifier=receipt_owner, aggregate_verifier=None,
            native_executable=str(native), runtime_pins=native_pins, output_directory=output/"mixed",
            operations=2, submitted_bytes=1048097, reserved_cpu_seconds=50,
            controller_cpu_seconds=60, wall_seconds=150, output_bytes=64*MIB, output_entries=512)
        for index, contents in enumerate(packet_bytes):
            summary = {"schema": "DMKN_MODULE_SUMMARY_V1", "foundation": B.FOUNDATION,
                "policy": B.POLICY, "group_count": index+1, "group_root": GROUP_ROOTS[index]}
            handle = mixed.receive(contents, summary, native_cpu_seconds=10,
                receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)
            fact = mixed.describe(handle)
            need(fact["module"] == MODULES[index] and fact["summary"] == summary
                 and fact["packet_sha256"] == PACKETS[index][1], "GENUINE_TARGET_DESCRIPTION")
            fact["journal"] = list(fact["journal"])
            report, receipt_report = mixed.report(), receipt_owner.report()
            expected = {"attempts": index+1, "native_check_attempts": index+1,
                "native_reuse_observations": index, "retained_native_records": index+1,
                "retained_native_witness_bytes": (50017, 100831)[index],
                "reserved_worker_cpu": (20, 50)[index], "submitted_bytes": (498641, 1048097)[index]}
            need(all(report[key] == value for key, value in expected.items()) and not report["closed"],
                 "EXACT_MIXED_COUNTERS")
            need(receipt_report["attempts"] == 1 and receipt_report["submitted_bytes"] == 223594
                 and receipt_report["reserved_cpu_seconds"] == 10 and not receipt_report["closed"],
                 "ONE_GENUINE_I_CHECK")
            result = json.loads(read(output/"mixed"/str(index+1)/"RESULT.json", MIB))
            native_observations = result["native_observations"]
            need(len(native_observations) == index+1, "NATIVE_OBSERVATION_COUNT")
            for position, observation in enumerate(native_observations):
                need(observation["index"] == position and
                     (observation["witness_bytes"], observation["witness_sha256"]) == WITNESSES[position]
                     and observation["observation"] == (REUSED if index == 1 and position == 0 else EXECUTED),
                     "EXACT_NATIVE_OBSERVATION")
            need(native_observations[-1]["journal"] == fact["journal"], "ACTUAL_TARGET_JOURNAL")
            if index == 1:
                need(native_observations[0]["journal"] == observations[0]["description"]["journal"],
                     "EXACT_REUSED_M_JOURNAL")
                for absent in ("delta-0.json", "native-0", "process-0.json", "claim-0"):
                    need(not (output/"mixed/2"/absent).exists(), "NO_FABRICATED_HIT_EXECUTION")
            observation = {"description": fact, "mixed_report": report,
                           "receipt_report": receipt_report, "native_observations": native_observations}
            observations.append(observation)
            save(output/("admission-"+str(index+1)+".json"), observation)
        for present in ("1/claim-0/process.json", "1/claim-0/command/stdout.txt",
                        "1/process-0.json", "1/native-0/stdout.txt",
                        "2/process-1.json", "2/native-1/stdout.txt"):
            ordinary(output/"mixed"/present)
        need(read(input_path, MIB) == input_raw, "INPUT_FINAL_READBACK")
        for row, contents in zip(packet_rows, packet_bytes):
            need(read(row["path"], MIB) == contents, "RETAINED_PACKET_FINAL_READBACK")
    except BaseException as error:
        errors.append(type(error).__name__+": "+str(error)[:2000])
    finally:
        for name, owner in (("mixed", mixed), ("receipt", receipt_owner)):
            if owner is not None:
                try:
                    owner.close()
                    cleanup[name] = owner.report()
                    need(cleanup[name]["closed"] and cleanup[name]["live_handles"] == 0, "OWNER_CLOSED")
                except BaseException as error:
                    errors.append("cleanup/"+name+": "+type(error).__name__+": "+str(error)[:2000])
        if domain is not None:
            try:
                domain.withdraw("Completed finite incremental-native integration; no future owner authority.")
                ordinary(output/"trust/WITHDRAWN")
                cleanup["withdrawn"] = True
            except BaseException as error:
                errors.append("cleanup/trust: "+type(error).__name__+": "+str(error)[:2000])
    passed = not errors and len(observations) == 2 and cleanup.get("withdrawn") is True
    result = {"schema": "DMKN_INCREMENTAL_NATIVE_INTEGRATION_RESULT_V1",
        "status": "PASS" if passed else "FAIL", "input_sha256": sha(input_raw),
        "observations": observations, "cleanup": cleanup, "errors": errors,
        "constructor_adoption_exercised": receipt_owner is not None and mixed is not None,
        "scope": "REAL_I_AND_NATIVE_SAME_OWNER_WARM_PREFIX_REUSE_WITH_CURRENT_PREMISES",
        "authority": "SAVED_INTEGRATION_EVIDENCE_NOT_TRANSFERABLE_PROOF",
        "new_proof_production": False, "full_cost_growth_claim": False}
    save(output/"integration-result.json", result)
    print(json.dumps({"status": result["status"], "admissions": len(observations), "errors": errors}), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
