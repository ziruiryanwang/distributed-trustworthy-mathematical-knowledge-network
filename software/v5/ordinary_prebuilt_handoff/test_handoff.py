"""One exact prebuilt pack/relocation and one unchanged state-free public query."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
PROFILE = "ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
ASSEMBLY = "ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c"
SOURCE = "f5134135204f980b90df449a3a9a07bfed61fd9ff6b9fd5b5dde305b00cd2861"
NATIVE_TYPE = LOCAL / "ordinary-query-public-01/public/query-local/native-type.json"
BINDINGS = LOCAL / "ordinary-query-public-01/public/fixtures/known-bindings.json"
NATIVE_SHA = "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480"
BINDINGS_SHA = "0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f"
QUERY_SHA = "eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a"
NAMESPACE = "d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c"
KEY_PROFILE = "09fceff93c77a65852e6509db9badfb3330d20737aea5297bd031f8b8845a953"
SPEC = {"tag": "declared-type-key", "value": "4d860a3d87fd9a65cf565fc2af70c6ac46d4d56974bb1eb0702f2248aaa42c0b"}
FEATURES = ["f2796ba9d490a8692c7509e69a45480c91582a31901ae5ba2d8b12278f4becb6"]
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError("PREBUILT_TEST_" + code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "assembly-receipt", "packer-sha256", "source-handoff", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 135 and time.process_time()-cpu < 65, "ALLOWANCE")

    packer_path = Path(__file__).absolute().parent / "pack_handoff.py"
    with packer_path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() == args.packer_sha256, "PACKER_PIN")
    spec = importlib.util.spec_from_file_location("_selected_prebuilt_packer", packer_path)
    P = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(packer_path), "exec"), P.__dict__)
    H = P.helpers()
    package = H.ordinary(Path(args.package), directory=True)
    receipt_path = H.ordinary(Path(args.assembly_receipt))
    source = H.ordinary(Path(args.source_handoff), directory=True)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    for path in (package, receipt_path, source, packer_path.parent, PYTHON, LEAN):
        need(not output.is_relative_to(path) and not path.is_relative_to(output), "OUTPUT_OVERLAP")
    profile, profile_pin = H.read_json(package / "PROFILE.json", PROFILE, check)
    installation, install_pin = H.read_json(package / "installation/INSTALLATION.json", INSTALLATION, check)
    assembly, assembly_pin = H.read_json(receipt_path, ASSEMBLY, check)
    # Independent derivation; do not treat the packer's map as the expected map.
    files = dict(profile["files"])
    native = {"installation/" + name: pin for name, pin in installation["files"].items()
              if not name.startswith(("python_runtime/", "lean_runtime/"))}
    need(len(files) == 117 and len(native) == 27 and len(assembly["documentation_files"]) == 8,
         "INPUT_ROLE_COUNTS")
    need(not set(files).intersection(native) and
         not (set(files) | set(native)).intersection(assembly["documentation_files"]), "INPUT_MAP_OVERLAP")
    files.update(native)
    files.update(assembly["documentation_files"])
    files.update({"PROFILE.json": profile_pin, "installation/INSTALLATION.json": install_pin})
    need(len(files) == 154 and sum(pin["bytes"] for pin in files.values()) == 39148493,
         "INPUT_MAP_CENSUS")
    for name, pin in files.items():
        H.relative(name); H.pin_shape(pin)
    source_manifest, source_pin = H.read_json(source / "COMMONS-SOURCE-MANIFEST.json", SOURCE, check)
    source_guide_pin = H.pin(source / "README.md", check, 2*MIB)
    need(source_guide_pin == source_manifest["files"]["README.md"], "SOURCE_GUIDE_ASSOCIATION")
    need(H.pin(NATIVE_TYPE, check)["sha256"] == NATIVE_SHA and
         H.pin(BINDINGS, check)["sha256"] == BINDINGS_SHA, "QUERY_INPUTS")
    output.mkdir()

    packed = P.pack(package, receipt_path, output / "handoff", check=check)
    handoff, relocated = output / "handoff", output / "handoff/relocated"
    saved = json.loads((handoff / "RECEIPT.json").read_bytes())
    need(saved == packed and saved["files"] == files and saved["payload_files"] == 154 and
         saved["archive_files"] == 154 and saved["payload_bytes"] == 39148493 and
         saved["profile_sha256"] == PROFILE and saved["installation_manifest_sha256"] == INSTALLATION and
         saved["assembly_receipt"] == assembly_pin and
         saved["status"] == "PACKED_AND_RELOCATED_EXACT_PREBUILT_NOT_EXECUTED", "PACK_RECEIPT")
    need(H.pin(handoff / "package.zip", check, 64*MIB) == saved["archive"] and
         H.pin(handoff / "README.md", check, 2*MIB) == saved["guide"] and
         H.pin(packer_path, check, 2*MIB) == saved["utility"], "PACK_OUTPUT_PINS")
    # Independent exact ZIP readback. The packer already made the sole extraction.
    with zipfile.ZipFile(handoff / "package.zip") as archive:
        members = archive.infolist()
        need(archive.comment == b"" and [row.filename for row in members] == sorted(files) and
             len({row.filename.casefold() for row in members}) == 154, "ZIP_NAMES")
        for row in members:
            check()
            pin = files[row.filename]
            need(not row.is_dir() and row.compress_type == zipfile.ZIP_STORED and
                 row.file_size == row.compress_size == pin["bytes"] and row.flag_bits == 0 and
                 row.date_time == (1980, 1, 1, 0, 0, 0) and row.create_system == 3 and
                 row.external_attr == 0o100644 << 16 and row.extra == row.comment == b"", "ZIP_METADATA")
            count, digest = 0, hashlib.sha256()
            with archive.open(row) as stream:
                while block := stream.read(MIB):
                    check(); count += len(block); digest.update(block)
                    need(count <= pin["bytes"], "ZIP_STREAM_BOUND")
            need({"bytes": count, "sha256": digest.hexdigest()} == pin, "ZIP_PAYLOAD")
    H.census(relocated, files, check)
    for name, pin in files.items():
        need(H.pin(relocated / name, check) == pin, "RELOCATED_PIN:" + name)

    refusals = []
    def refuses(label, callback, expected):
        check()
        try:
            callback()
        except ValueError as error:
            need(str(error) == expected, "WRONG_REFUSAL:" + label + ":" + str(error))
            refusals.append({"case": label, "error": str(error)})
        else:
            raise ValueError("PREBUILT_TEST_ACCEPTED_BAD_CASE:" + label)

    refuses("existing-output", lambda: P.pack(package, receipt_path, handoff, check=check),
            "FAIR_ASSEMBLY_OUTPUT_EXISTS")
    bad_profile = output / "bad-profile"
    bad_profile.mkdir(); H.fresh_bytes(bad_profile / "PROFILE.json", b"{}")
    refuses("unapproved-profile", lambda: P.selected_map(H, bad_profile, receipt_path, check),
            "FAIR_ASSEMBLY_JSON_PIN")
    bad_receipt = output / "bad-receipt.json"
    H.fresh_bytes(bad_receipt, b"{}")
    refuses("unapproved-receipt", lambda: P.selected_map(H, package, bad_receipt, check),
            "FAIR_ASSEMBLY_JSON_PIN")
    tiny = {"item.txt": {"bytes": 8, "sha256": H.digest(b"original")}}
    changed = output / "changed-payload"
    changed.mkdir(); H.fresh_bytes(changed / "item.txt", b"modified")
    refuses("changed-payload", lambda: P.check_tree(H, changed, tiny, check),
            "PREBUILT_HANDOFF_PAYLOAD_PIN:item.txt")
    extra = output / "extra-payload"
    extra.mkdir(); H.fresh_bytes(extra / "item.txt", b"original")
    H.fresh_bytes(extra / "extra.txt", b"extra")
    refuses("extra-payload", lambda: P.check_tree(H, extra, tiny, check), "FAIR_ASSEMBLY_EXACT_CENSUS")
    alias_zip = output / "aliased-members.zip"
    with alias_zip.open("xb") as stream, zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted("readme.md" if name == "README.md" else name for name in files):
            check(); archive.writestr(name, b"x")
    refuses("case-changed-archive-member", lambda: P.inspect_archive(H, alias_zip, files, check),
            "PREBUILT_HANDOFF_ZIP_CENSUS")
    need(len(refusals) == 6, "REFUSAL_COUNT")
    H.fresh_bytes(output / "FILE-GATE.json", H.canonical({"status": "PASS_EXACT_FILE_RELOCATION",
        "files": files, "archive": saved["archive"], "refusals": refusals,
        "claim": "FILE_GATE_ONLY_PUBLIC_QUERY_NOT_YET_EXECUTED"}))

    # One public manual-mode query loads full package/runtime; no owner/state flags.
    check(); need(135-(time.monotonic()-started) >= 45, "QUERY_REMAINING_ALLOWANCE")
    argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(relocated / "run.py"),
        "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
        "--diagnostics", str(output / "query-launch"), "--wall-seconds", "35",
        "--cpu-seconds", "10", "--memory-mib", "512", "--active-processes", "1",
        "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "query", "--",
        "--native-type", str(NATIVE_TYPE), "--bindings", str(BINDINGS), "--output", str(output / "query")]
    H.fresh_bytes(output / "QUERY-COMMAND.json", H.canonical({"argv": argv, "timeout_seconds": 45}))
    with (output / "query-launcher-stdout.txt").open("xb") as stdout, \
            (output / "query-launcher-stderr.txt").open("xb") as stderr:
        completed = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout,
                                   stderr=stderr, timeout=45, check=False)
    check()
    need(completed.returncode == 0 and (output / "query-launcher-stderr.txt").stat().st_size == 0,
         "QUERY_LAUNCHER_EXIT")
    def small_json(path):
        need(H.ordinary(path).stat().st_size <= 2*MIB, "REPORT_BOUND")
        with path.open("rb") as stream:
            return json.loads(stream.read(2*MIB+1))
    run = small_json(output / "query-launch/RUN.json")
    supervision = small_json(output / "query-launch/SUPERVISION.json")
    printed = small_json(output / "query-launcher-stdout.txt")
    inner = small_json(output / "query-launch/child/stdout.txt")
    result = small_json(output / "query/RESULT.json")
    need(printed == run and run["ok"] is True and run["status"] == "CLI_EXITED_ZERO" and
         run["tool"] == "query" and run["profile_sha256"] == PROFILE, "QUERY_PUBLIC_RESULT")
    need(supervision["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         supervision["child_exit_code"] == 0 and supervision["direct_child_reaped"] is True and
         supervision["job_closed"] is True and supervision["cleanup_errors"] == [] and
         supervision["termination_requested"] is False and
         supervision["final_job"]["active_processes"] == supervision["final_job"]["terminated_processes"] == 0,
         "QUERY_CLEAN_CLOSURE")
    need((output / "query-launch/child/stderr.txt").stat().st_size == 0 and inner == result and
         result["ok"] is True and result["operation"] == "prepare-query" and
         result["profile_sha256"] == PROFILE and result["mathematical_acceptance"] is False and
         result["native_type_sha256"] == NATIVE_SHA and result["bindings_sha256"] == BINDINGS_SHA and
         result["query_sha256"] == QUERY_SHA and result["namespace"] == NAMESPACE and
         result["key_profile"] == KEY_PROFILE and result["specs"] == [SPEC] and
         result["features"] == FEATURES and result["cost"]["worker_cpu_seconds"] == 0,
         "QUERY_EXACT_SEMANTIC_OUTPUT")
    need(H.pin(output / "query/QUERY.json", check)["sha256"] == QUERY_SHA and
         small_json(output / "query/SPECS.json") == [SPEC], "QUERY_OUTPUT_FILES")
    P.check_tree(H, relocated, files, check)
    P.check_tree(H, package, files, check)
    need(H.pin(handoff / "package.zip", check, 64*MIB) == saved["archive"] and
         H.pin(source / "COMMONS-SOURCE-MANIFEST.json", check, 2*MIB) == source_pin and
         H.pin(source / "README.md", check, 2*MIB) == source_guide_pin and
         H.pin(NATIVE_TYPE, check)["sha256"] == NATIVE_SHA and
         H.pin(BINDINGS, check)["sha256"] == BINDINGS_SHA and
         H.pin(packer_path, check, 2*MIB)["sha256"] == args.packer_sha256, "FINAL_INPUTS")
    check()
    report = {"status": "PASS_PREBUILT_RELOCATION_AND_STATE_FREE_PUBLIC_QUERY", "payload_files": 154,
        "payload_bytes": 39148493, "expected_refusals": refusals, "archive": saved["archive"],
        "source_handoff_manifest": source_pin, "public_query": result, "public_launcher": run,
        "wall_seconds": time.monotonic()-started, "harness_cpu_seconds": time.process_time()-cpu,
        "claim": "BYTE_PRESERVING_DEPLOYMENT_CONVENIENCE_NOT_NEW_MATHEMATICS_OR_FINAL_V5"}
    H.fresh_bytes(output / "RESULT.json", H.canonical(report))
    print(json.dumps({"status": report["status"], "payload_files": 154, "expected_refusals": 6,
                      "output": str(output)}), flush=True)


if __name__ == "__main__":
    main()
