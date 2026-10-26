"""One exact archive-only installation and inert public query, not a new installer.

Run only inside the selected outer Windows Job. That Job owns descendant cleanup,
aggregate CPU/memory/process limits and failure containment. No retry or renewal.
This driver imports no product code and never supplies missing checkout sources.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
WALL = 550
ZIP_PIN = {"bytes": 3789448, "sha256": "897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0"}
RECEIPT_SHA = "053bdcf14f7c67a4685081c0f6044a9b76defec89907040b28a5954e05ba075b"
MANIFEST_PIN = {"bytes": 21331, "sha256": "f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1"}
TYPE_SHA = "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480"
BINDINGS_SHA = "0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f"
QUERY_SHA = "eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a"
PREFIX = "software/v5/"
BUILDER = PREFIX + "ordinary_bounded_operations/build.py"
SOURCE_MAP = PREFIX + "ordinary_bounded_operations/source-map.json"
BUNDLE = PREFIX + "ordinary_release_bundle/bundle.py"
FAIR = PREFIX + "ordinary_fair_search/"
FAIR_FILES = {"profile.py": "profile.py", "peer_api.py": "peer_api.py", "README.md": "README.md",
              "support/transport/fair_exchange.py": "fair_exchange.py",
              "support/discovery/fair_search.py": "fair_search.py"}


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < WALL and time.process_time()-CPU < 60,
         "ORIGINAL_DRIVER_ALLOWANCE")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024, "RELATIVE_PATH")
    path = PurePosixPath(value)
    need(not path.is_absolute() and path.as_posix() == value and len(path.parts) <= 16 and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and
             not any(ord(c) < 32 or c in ':*?"<>|\\' for c in part) for part in path.parts),
         "RELATIVE_PATH")
    return value


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path != Path(path.anchor) and len(path.parts) <= 128 and len(str(path)) <= 32767,
         "ABSOLUTE_LOCAL_PATH")
    for part in path.parts[1:]:
        relative(part)
    for ancestor in (*reversed(path.parents), path):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            need(fresh and ancestor == path, "MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if ancestor != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(not fresh, "OUTPUT_EXISTS")
    return path


def read(path, maximum=2*MIB):
    check(); path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "READ_CHANGED")
    return raw


def digest_file(path, maximum=128*MIB):
    check(); path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); count += len(block)
            need(count <= size, "FILE_GREW")
            digest.update(block)
    need(count == size and ordinary(path).stat().st_size == size, "FILE_CHANGED")
    return {"bytes": count, "sha256": digest.hexdigest()}


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_KEY")
            result[key] = value
        return result
    def number(value):
        result = float(value)
        need(math.isfinite(result), "NONFINITE_JSON")
        return result
    def invalid(_):
        raise AssertionError("NONFINITE_JSON")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=number, parse_constant=invalid)


def document(path):
    return decode(read(path))


def save(path, value):
    raw = canonical(value)
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    with ordinary(path, fresh=True).open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def census(root, expected):
    names, dirs, pending, count = set(), set(), [root], 0
    allowed_dirs = {p.as_posix() for name in expected for p in PurePosixPath(name).parents
                    if p.as_posix() != "."}
    while pending:
        folder = pending.pop()
        with os.scandir(ordinary(folder, directory=True)) as rows:
            for row in rows:
                check(); count += 1
                need(count <= 512, "CENSUS_BOUND")
                path = Path(row.path)
                name = relative(path.relative_to(root).as_posix())
                if row.is_dir(follow_symlinks=False):
                    ordinary(path, directory=True)
                    need(name in allowed_dirs and name.casefold() not in dirs, "EXTRA_DIRECTORY")
                    dirs.add(name.casefold()); pending.append(path)
                else:
                    ordinary(path)
                    need(name in expected and name.casefold() not in names, "EXTRA_FILE")
                    names.add(name.casefold())
    need(names == {n.casefold() for n in expected} and
         dirs == {n.casefold() for n in allowed_dirs}, "EXACT_CENSUS")


def exact_files(root, expected):
    need(len(expected) <= 256 and sum(p["bytes"] for p in expected.values()) <= 768*MIB,
         "MAP_BOUND")
    census(root, expected)
    for name, expected_pin in expected.items():
        need(digest_file(root/relative(name)) == expected_pin, "EXACT_FILE:"+name)


def clean_job(value):
    need(value.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         value.get("child_exit_code") == 0 and value.get("direct_child_reaped") is True and
         value.get("job_closed") is True and value.get("termination_requested") is False and
         value.get("cleanup_errors") == [] and value.get("final_job", {}).get("active_processes") == 0 and
         value["final_job"].get("terminated_processes") == 0 and
         type(value["final_job"].get("cpu_seconds")) in (int, float) and
         math.isfinite(value["final_job"]["cpu_seconds"]) and value["final_job"]["cpu_seconds"] >= 0,
         "UNCLEAN_NESTED_JOB")


def public(args, label, tokens, timeout, report):
    check()
    need(WALL-(time.monotonic()-START) > timeout+5, "NO_ROOM_FOR_STAGE:"+label)
    argv = [str(args.python_runtime/"python.exe"), "-I", "-S", "-B", *map(str, tokens)]
    stdout, stderr = args.output/(label+"-stdout.txt"), args.output/(label+"-stderr.txt")
    record = {"argv": argv, "cwd": str(ROOT), "timeout_seconds": timeout,
              "outer_job_owns_descendant_cleanup": True}
    save(args.output/(label+"-COMMAND.json"), record)
    started, child = time.monotonic(), None
    try:
        with stdout.open("xb") as out, stderr.open("xb") as err:
            child = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
            while child.poll() is None:
                check()
                need(time.monotonic()-started < timeout, "STAGE_TIMEOUT:"+label)
                need(stdout.stat().st_size <= MIB and stderr.stat().st_size <= MIB,
                     "STAGE_LOG_BOUND:"+label)
                time.sleep(0.05)
            record.update(exit_code=child.wait(), direct_child_reaped=True)
        need(record["exit_code"] == 0 and stderr.stat().st_size == 0 and
             stdout.stat().st_size <= MIB, "PUBLIC_STAGE_FAILED:"+label)
        value = document(stdout)
        record.update(result=value, wall_seconds=time.monotonic()-started)
        save(args.output/(label+"-PROCESS.json"), record)
        report["public"][label] = record
        return value
    except BaseException as error:
        if child is not None:
            if child.poll() is None:
                child.kill()  # Only the direct child; outer Job settles descendants.
            record.update(exit_code=child.wait(timeout=5), direct_child_reaped=True)
        record.update(error_type=type(error).__name__, error=str(error)[:1000],
                      wall_seconds=time.monotonic()-started,
                      descendant_outcome="REQUIRES_OUTER_JOB_CLOSURE_NOT_ASSERTED_BY_DRIVER")
        save(args.output/(label+"-FAILURE.json"), record)
        raise


def extract(args, report):
    archive_raw, receipt_raw = read(args.archive, 8*MIB), read(args.archive_receipt)
    need(pin(archive_raw) == ZIP_PIN and pin(receipt_raw)["sha256"] == RECEIPT_SHA, "ARCHIVE_SELECTION")
    receipt = decode(receipt_raw)
    need(receipt.get("status") == "PACKED_SOURCE_NOT_BUILT" and
         receipt.get("archive") == ZIP_PIN and receipt.get("manifest") == MANIFEST_PIN and
         receipt.get("payload_files") == 143 and receipt.get("archive_files") == 144,
         "ARCHIVE_RECEIPT")
    destination = args.output/"source"
    with zipfile.ZipFile(io.BytesIO(archive_raw), "r") as archive:
        rows = archive.infolist()
        need(len(rows) == 144 and archive.comment == b"", "ZIP_CENSUS")
        manifest_raw = archive.read("SOURCE-MANIFEST.json")
        need(pin(manifest_raw) == MANIFEST_PIN, "MANIFEST_PIN")
        manifest = decode(manifest_raw)
        files = manifest["files"]
        need(manifest["schema"] == "DMKN_ORDINARY_RELEASE_SOURCE_DISTRIBUTION_V1" and
             len(files) == 143 and canonical(manifest) == manifest_raw and
             len({n.casefold() for n in files}) == 143, "MANIFEST_SHAPE")
        expected = {**files, "SOURCE-MANIFEST.json": MANIFEST_PIN}
        need([r.filename for r in rows] == sorted(expected) and
             sum(p["bytes"] for p in expected.values()) <= 8*MIB, "ZIP_EXACT_NAMES")
        for row in rows:
            relative(row.filename)
            need(not row.is_dir() and row.compress_type == zipfile.ZIP_STORED and
                 row.flag_bits == 0 and row.file_size == row.compress_size == expected[row.filename]["bytes"] and
                 row.create_system == 3 and stat.S_ISREG(row.external_attr >> 16), "ZIP_MEMBER_LAYOUT")
        ordinary(destination, directory=True, fresh=True).mkdir()
        for row in rows:
            check(); raw = archive.read(row)
            need(pin(raw) == expected[row.filename], "ZIP_MEMBER_PIN")
            target = destination/relative(row.filename)
            need(target.is_relative_to(destination), "EXTRACTION_ESCAPE")
            target.parent.mkdir(parents=True, exist_ok=True)
            with ordinary(target, fresh=True).open("xb") as out:
                out.write(raw)
    exact_files(destination, expected)
    verified = public(args, "verify", [destination/BUNDLE, "verify", "--source-root", destination,
        "--manifest-sha256", MANIFEST_PIN["sha256"]], 20, report)
    need(verified.get("status") == "VERIFIED_EXACT_SOURCE_NOT_BUILT" and
         verified.get("manifest") == MANIFEST_PIN and verified.get("payload_files") == 143,
         "PUBLIC_VERIFY_RESULT")
    report["archive"] = receipt
    return destination, files, expected


def package_map(package, receipt, expected_count, expected_aux):
    profile_raw = read(package/"PROFILE.json")
    profile = decode(profile_raw)
    installation_raw = read(package/"installation/INSTALLATION.json")
    installation = decode(installation_raw)
    need(receipt["profile_sha256"] == pin(profile_raw)["sha256"] and
         receipt["installation_manifest_sha256"] == profile["installation_manifest_sha256"] ==
         pin(installation_raw)["sha256"] and Path(receipt["package"]) == package and
         receipt["files_excluding_profile"] == expected_count-1 and
         receipt["auxiliary_files"] == len(profile["files"]) == expected_aux, "PACKAGE_RECEIPT_BINDING")
    own_files = {"installation/"+n: p for n, p in installation["files"].items()
                 if not n.startswith(("python_runtime/", "lean_runtime/"))}
    need(len(own_files) == 27, "INSTALLATION_CENSUS")
    files = {**profile["files"], **own_files, **receipt["documentation_files"],
             "installation/INSTALLATION.json": pin(installation_raw), "PROFILE.json": pin(profile_raw)}
    need(len(files) == expected_count, "PACKAGE_CENSUS")
    exact_files(package, files)
    return files


def build_chain(args, source, sources, report):
    build = args.output/"build"
    result = public(args, "build", [source/BUILDER, "--source-root", source,
        "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
        "--output", build, "--wall-seconds", "480", "--cpu-seconds", "360", "--memory-mib", "2048"],
        490, report)
    receipt_path = build/"_build/BUILD-RESULT.json"
    need(result == document(receipt_path) and result.get("status") == "BUILT_NOT_ADOPTED" and
         result.get("builder") == sources[BUILDER] and
         result.get("source_map_sha256") == sources[SOURCE_MAP]["sha256"] and
         result.get("child_cpu_complete") is True, "BUILD_TERMINAL_RECEIPT")
    staged = document(build/"_build/SOURCES.json")
    declared = document(source/SOURCE_MAP)["sources"]
    expected_staged = {**declared, BUILDER: sources[BUILDER], SOURCE_MAP: sources[SOURCE_MAP]}
    need(Path(staged["source_root"]) == source and len(expected_staged) == 86 and
         staged["files"] == expected_staged and
         all(sources.get(n) == p for n, p in expected_staged.items()), "ARCHIVE_ONLY_BUILD_INPUTS")
    for name in ("base-job", "extractor-job", "query-job"):
        saved = document(build/("_build/"+name+"-SUPERVISION.json"))
        need(saved.get("cpu_complete") is True, "BUILD_CHILD_CPU_UNKNOWN")
        clean_job(saved["supervision"])
    clean_job(document(build/"_build/base/_build/SUPERVISION.json"))
    package = build/"package"
    current_map = package_map(package, result, 146, 113)
    initial_installation = result["installation_manifest_sha256"]
    report["packages"] = [{"stage": "build", "receipt": str(receipt_path),
        "receipt_pin": digest_file(receipt_path), "profile_sha256": result["profile_sha256"],
        "file_count": len(current_map)}]
    stages = [("fair", "ordinary_fair_search", 148, 115),
              ("contact", "ordinary_contact_federation", 150, 116),
              ("sparse", "ordinary_sparse_access", 152, 117),
              ("transport", "ordinary_transport_release", 154, 117)]
    for label, folder, count, aux in stages:
        predecessor, predecessor_receipt = result, digest_file(receipt_path)
        output = args.output/label
        entry = source/(PREFIX+folder+"/assemble.py")
        receipt_option = "--base-build-receipt" if label == "fair" else "--base-receipt"
        tokens = [entry, "--source-root", source, "--base-package", package,
            "--base-profile-sha256", predecessor["profile_sha256"], receipt_option, receipt_path,
            receipt_option+"-sha256", predecessor_receipt["sha256"], "--output", output,
            "--wall-seconds", "30", "--cpu-seconds", "20"]
        if label == "fair":
            changes = {n: sources[FAIR+f] for n, f in FAIR_FILES.items()}
        else:
            overlay = source/(PREFIX+folder+"/OVERLAY.json")
            overlay_pin = digest_file(overlay)
            changes = document(overlay)["files"]
            tokens += ["--overlay", overlay, "--overlay-sha256", overlay_pin["sha256"]]
        result = public(args, label, tokens, 40, report)
        receipt_path, package = output/"ASSEMBLY.json", output/"package"
        need(result == document(receipt_path) and result.get("status") == "ASSEMBLED_NOT_ADOPTED" and
             result.get("base_profile_sha256") == predecessor["profile_sha256"] and
             result.get("base_build_receipt" if label == "fair" else "base_receipt") == predecessor_receipt and
             result.get("changed_or_added") == changes and
             result.get("assembler") == sources[PREFIX+folder+"/assemble.py"] and
             result.get("installation_manifest_sha256") == initial_installation,
             "FRESH_IMMEDIATE_RECEIPT:"+label)
        if label != "fair":
            need(result.get("overlay") == overlay_pin, "OVERLAY_RECEIPT")
        expected_map = {**current_map, **changes, "PROFILE.json": digest_file(package/"PROFILE.json")}
        need(len(expected_map) == count and len(document(package/"PROFILE.json")["files"]) == aux and
             result.get("files_excluding_profile") == count-1 and result.get("auxiliary_files") == aux and
             Path(result["package"]) == package and
             result["profile_sha256"] == expected_map["PROFILE.json"]["sha256"], "OVERLAY_CENSUS")
        exact_files(package, expected_map)
        current_map = expected_map
        report["packages"].append({"stage": label, "receipt": str(receipt_path),
            "receipt_pin": digest_file(receipt_path), "profile_sha256": result["profile_sha256"],
            "file_count": count})
    need(package_map(package, result, 154, 117) == current_map, "FINAL_PACKAGE_CLOSURE")
    report["installation_manifest_sha256"] = initial_installation
    return package, result, current_map


def query(args, package, assembled, report):
    output, diagnostics = args.output/"query", args.output/"query-diagnostics"
    result = public(args, "manual-query", [package/"run.py",
        "--profile-sha256", assembled["profile_sha256"], "--python-runtime", args.python_runtime,
        "--lean-runtime", args.lean_runtime, "--diagnostics", diagnostics,
        "--wall-seconds", "60", "--cpu-seconds", "30", "--memory-mib", "512", "--active-processes", "4",
        "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "query", "--",
        "--native-type", args.native_type, "--bindings", args.bindings, "--output", output], 75, report)
    need(result == document(diagnostics/"RUN.json") and result.get("status") == "CLI_EXITED_ZERO" and
         result.get("ok") is True and result.get("mathematical_disposition") == "NOT_INTERPRETED" and
         result.get("profile_sha256") == assembled["profile_sha256"], "PUBLIC_QUERY_LAUNCH")
    clean_job(document(diagnostics/"SUPERVISION.json"))
    actual = document(output/"RESULT.json")
    need(actual.get("ok") is True and actual.get("mathematical_acceptance") is False and
         actual.get("operation") == "prepare-query" and actual.get("profile_sha256") == assembled["profile_sha256"] and
         actual.get("native_type_sha256") == TYPE_SHA and actual.get("bindings_sha256") == BINDINGS_SHA and
         actual.get("query_sha256") == QUERY_SHA and digest_file(output/"QUERY.json")["sha256"] == QUERY_SHA and
         actual.get("cost", {}).get("worker_cpu_seconds") == 0, "INERT_EXACT_QUERY")
    report["query"] = actual


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("archive", "archive-receipt", "native-type", "bindings", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True, type=Path)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "DRIVER_PROFILE")
    for name in ("archive", "archive_receipt", "native_type", "bindings"):
        ordinary(getattr(args, name))
    ordinary(args.python_runtime, directory=True); ordinary(args.lean_runtime, directory=True)
    need(Path(sys.executable).resolve() == args.python_runtime/"python.exe", "PYTHON_RUNTIME_SELECTION")
    ordinary(args.output, directory=True, fresh=True)
    need(args.output.is_relative_to(ROOT) and all(not args.output.is_relative_to(p) and
         not p.is_relative_to(args.output) for p in (args.archive, args.archive_receipt,
         args.native_type, args.bindings, args.python_runtime, args.lean_runtime)), "OUTPUT_OVERLAP")
    need(digest_file(args.native_type)["sha256"] == TYPE_SHA and
         digest_file(args.bindings)["sha256"] == BINDINGS_SHA, "FIXED_QUERY_INPUTS")
    args.output.mkdir()
    report = {"schema": "DMKN_ARCHIVE_INSTALL_TEST_V1", "status": "INCOMPLETE", "public": {},
        "scope": "LOCAL_ARCHIVE_ONLY_BUILD_FOUR_OVERLAYS_INERT_PUBLIC_QUERY",
        "mathematical_acceptance": False, "network_operations": 0, "owner_state_opened": False,
        "original_wall_seconds": WALL, "outer_job_required": True}
    try:
        source, files, source_map = extract(args, report)
        package, assembled, output_map = build_chain(args, source, files, report)
        query(args, package, assembled, report)
        exact_files(source, source_map); exact_files(package, output_map)
        need(digest_file(args.archive) == ZIP_PIN and digest_file(args.archive_receipt)["sha256"] == RECEIPT_SHA and
             digest_file(args.native_type)["sha256"] == TYPE_SHA and
             digest_file(args.bindings)["sha256"] == BINDINGS_SHA, "ORIGINAL_INPUTS_PRESERVED")
        check()
        report.update(status="PASS_LOCAL_ARCHIVE_INSTALL_NOT_FULL_V5", final_package=str(package),
            final_profile_sha256=assembled["profile_sha256"], source_payloads=143,
            final_package_files=154, wall_seconds=time.monotonic()-START,
            driver_cpu_seconds=time.process_time()-CPU,
            cpu_scope="DRIVER_ONLY;CHILD_CPU_IN_OUTER_JOB_DO_NOT_SUM_NESTED_REPORTS")
        save(args.output/"RESULT.json", report)
        print(json.dumps(report, sort_keys=True, allow_nan=False))
        return 0
    except BaseException as error:
        report.update(status="FAILED_OR_INCOMPLETE", error_type=type(error).__name__, error=str(error)[:2000],
            wall_seconds=time.monotonic()-START, driver_cpu_seconds=time.process_time()-CPU,
            retention="PRESERVED_NO_RETRY;OUTER_JOB_CLOSURE_REQUIRED")
        try:
            save(args.output/"FAILURE.json", report)
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
