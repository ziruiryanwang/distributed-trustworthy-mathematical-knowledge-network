"""One fixed-order matched RC/general execution screen; no proof production.

Run only through the root-selected finite Run-V5-Check envelope. The retained
supervisor owns each host process tree. Shared preparation is measured once,
charged fully to each standalone arm, and counted only once in pair totals.
"""
import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
MIB = 1024**2
HOST_LIMITS = dict(cpu_seconds=180, wall_seconds=120, memory_mib=3072,
                   active_processes=2, stdout_bytes=MIB, stderr_bytes=MIB)
ARM_WALL = 240
PAIR_WALL = 530
NATIVE_RESULT = "24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd"
CONTROL_BINARY = "9711910d7c0a32a08df3233bad2416fe0a88a89dae392e4fe71986e95b83e559"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path, *, directory=False, fresh=False):
    path = Path(path)
    need(path.is_absolute() and path.is_relative_to(ROOT) and ".." not in path.parts,
         "CANONICAL_PROJECT_PATH")
    for item in reversed(path.parents):
        info = item.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "ORDINARY_ANCESTRY")
    if fresh:
        need(not path.exists() and not path.is_symlink() and not path.is_junction(), "FRESH_OUTPUT")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)), "ORDINARY_KIND")
    need(path.resolve(strict=not fresh) == path, "EXACT_CANONICAL_PATH")
    return path


def bounded(path, maximum, *, empty=False):
    path = ordinary(path)
    size = path.stat().st_size
    need((empty or size > 0) and size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) == size and path.stat().st_size == size, "READ_EXTENT_CHANGED")
    return raw


def parse(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "DUPLICATE_RECORD_KEY")
            value[key] = item
        return value
    def invalid(value):
        raise ValueError("NONFINITE_RECORD_NUMBER:" + value)
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    json.dumps(value, allow_nan=False)
    return value


def save(path, raw):
    ordinary(path, fresh=True)
    with Path(path).open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())


def save_json(path, value):
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    need(len(raw) <= 2*MIB, "REPORT_BOUND")
    save(path, raw)


def clean_job(value):
    need(value["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and value["child_exit_code"] == 0
         and value["job_closed"] is True and value["direct_child_reaped"] is True
         and value["cleanup_errors"] == [] and value["final_job"]["active_processes"] == 0
         and value["final_job"]["terminated_processes"] == 0, "CLEAN_OWNED_COMMAND")


class Inputs:
    def __init__(self):
        self.pins, self.absent = {}, set()

    def read(self, item, maximum=2*MIB):
        need(type(item) is dict and set(item) == {"path", "bytes", "sha256"}
             and type(item["bytes"]) is int and 0 < item["bytes"] <= maximum, "EXACT_PIN_SHAPE")
        path = ordinary(item["path"])
        raw = bounded(path, maximum)
        need(len(raw) == item["bytes"] and digest(raw) == item["sha256"], "INPUT_PIN:" + str(path))
        row = (dict(item), maximum)
        need(path not in self.pins or self.pins[path] == row, "CONSISTENT_INPUT_PIN")
        self.pins[path] = row
        return raw

    def record(self, item):
        value = parse(self.read(item))
        need(type(value) is dict, "OBJECT_RECORD")
        return value

    def no_override(self, path):
        path = Path(path)
        need(not path.exists() and not path.is_symlink() and not path.is_junction(), "FINALIZATION_OVERRIDE")
        self.absent.add(path)

    def rebind(self):
        for item, maximum in list(self.pins.values()):
            self.read(item, maximum)
        for path in self.absent:
            self.no_override(path)


def supervisor(inputs):
    raw = bounded(BASE / "RELEASE-MANIFEST.json", 2*MIB)
    need(digest(raw) == MANIFEST_SHA, "RETAINED_SUPERVISOR_MANIFEST")
    inputs.read(dict(path=str(BASE / "RELEASE-MANIFEST.json"), bytes=len(raw), sha256=MANIFEST_SHA))
    manifest = parse(raw)
    held = {}
    for name, relative in (("supervisor", "operator/commons.py"),
                           ("domains", "receiver/helpers/domains.py"),
                           ("job", "receiver/helpers/run_stage.py")):
        path = BASE / relative
        content = inputs.read({"path": str(path), **manifest["files"][relative]})
        module_name = "domains" if name == "domains" else "_rc_pair_" + name
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        exec(compile(content, str(path), "exec"), module.__dict__)
        held[name] = module
    return held["supervisor"], held["job"]


def host(inputs, role, records):
    need(set(records) == {"result", "attempt", "selection", "source_map", "command"}, "HOST_RECORD_SET")
    rows = {name: inputs.record(pin) if name != "command" else parse(inputs.read(pin))
            for name, pin in records.items()}
    result, selected = rows["result"], rows["selection"]
    root = HERE / ("small-aggregate-snapshot-host-build-01" if role == "general" else "restricted-snapshot-host-build-01")
    stem = "SMALL_AGGREGATE_SNAPSHOT_HOST" if role == "general" else "RC_SNAPSHOT_HOST"
    expected_status = "PASS_SMALL_AGGREGATE_SNAPSHOT_HOST_ONE_LINK_ONLY" if role == "general" else "PASS_RC_SNAPSHOT_HOST_ONE_LINK_ONLY"
    need(Path(records["result"]["path"]) == root / "RESULT.json"
         and Path(records["attempt"]["path"]) == HERE / (root.name + "-attempt.json")
         and Path(records["selection"]["path"]) == HERE / (root.name + "-selection.json")
         and Path(records["source_map"]["path"]) == root / "source-map.json"
         and Path(records["command"]["path"]) == root / "compile-command.json"
         and result["schema"] == "DMKN_V5_" + stem + "_BUILD_RESULT_V1" and result["status"] == expected_status
         and selected["schema"] == "DMKN_V5_" + stem + "_BUILD_V1" and selected["name"] == root.name
         and selected["authorizes_compile_only"] is True
         and result["selection_sha256"] == records["selection"]["sha256"]
         and selected["sources"] == rows["source_map"] and len(rows["source_map"]) == 3
         and rows["attempt"] == {"status": expected_status, "result_sha256": records["result"]["sha256"]},
         "ACTUAL_SELECTED_HOST_BUILD")
    inputs.no_override(root / "FINALIZATION-FAILED.json")
    commands = result["commands"]
    need(len(commands) == 1 and commands[0]["argv"] == rows["command"]
         and commands[0]["status"] == "COMMAND_COMPLETED" and commands[0]["exit_code"] == 0
         and commands[0]["cleanup_errors"] == [] and result["job"]["active_processes"] == 0
         and result["job"]["terminated_processes"] == 0
         and all(result[key] == 0 for key in ("backend_rebuilds", "relation_rebuilds", "checker_rebuilds",
                 "host_calls", "guest_calls", "proof_calls", "network_calls")), "HOST_BUILD_SCOPE_AND_CLOSURE")
    need(rows["source_map"]["software/v5/aggregate_small/aggregate_host.rs"]["sha256"] ==
         "6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25"
         and rows["source_map"]["software/v5/aggregate/receipt.rs"]["sha256"] ==
         "41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254", "UNCHANGED_HOST_AND_RECEIPT")
    if role == "restricted":
        need(result["rc_native_result_sha256"] == NATIVE_RESULT and
             "dmkn_aggregate_relation=" + str(HERE / "restricted-composition-build-02/libdmkn_aggregate_relation.rlib")
             in rows["command"], "RC_NATIVE_LINK_EDGE")
    executable = result["executable"]
    need(Path(executable["path"]).parent == root, "HOST_OUTPUT_ROOT")
    inputs.read(executable, 16*MIB)
    return executable


def image(inputs, role, records):
    need(set(records) == {"result", "outer", "guest_result", "guest_attempt"}, "IMAGE_RECORD_SET")
    rows = {name: inputs.record(pin) for name, pin in records.items()}
    assembled, outer, built = rows["result"], rows["outer"], rows["guest_result"]
    assembly_root = HERE / ("typed-guest-image-assembly-01" if role == "general" else "restricted-guest-image-assembly-01")
    guest_root = HERE / ("typed-guest-build-01" if role == "general" else "restricted-guest-build-03")
    prefix = "TYPED" if role == "general" else "RC"
    need(Path(records["outer"]["path"]) == assembly_root / "RESULT.json"
         and Path(records["result"]["path"]) == assembly_root / "assembly/RESULT.json"
         and Path(records["guest_result"]["path"]) == guest_root / "RESULT.json"
         and Path(records["guest_attempt"]["path"]) == HERE / (guest_root.name + "-attempt.json")
         and outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1", "EXACT_IMAGE_BUILD_ROOTS")
    clean_job(outer["result"])
    need(assembled["schema"] == "DMKN_V5_" + prefix + "_GUEST_IMAGE_ASSEMBLY_RESULT_V1"
         and assembled["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
         and assembled["assembler_calls"] == 1 and assembled["guest_executions"] == assembled["proof_calls"] == 0
         and assembled["mathematical_admission"] is False
         and assembled["guest_build_result"] == records["guest_result"]
         and assembled["selection_sha256"] == built["selection_sha256"]
         and assembled["image_id_origin"] == "ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256"
         and rows["guest_attempt"] == {"status": built["status"], "result_sha256": records["guest_result"]["sha256"]},
         "ADOPTED_ACTUAL_GUEST_ASSEMBLY")
    wanted = "PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY" if role == "general" else "PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY"
    need(built["schema"] == "DMKN_V5_" + prefix + "_GUEST_FOUR_CRATE_BUILD_RESULT_V1"
         and built["status"] == wanted and built["job"]["active_processes"] == built["job"]["terminated_processes"] == 0,
         "CLOSED_GUEST_BUILD")
    inputs.no_override(guest_root / "FINALIZATION-FAILED.json")
    artifact = assembled["image"]
    need(Path(artifact["path"]) == assembly_root / "assembly/aggregate_image.bin", "ACTUAL_IMAGE_PATH")
    inputs.read(artifact, 64*MIB)
    return assembled["image_id"], artifact


def statistics(diagnostic, directory, pin_file):
    rows = diagnostic["retained_segments"]
    stats = diagnostic["session_stats"]
    need(type(rows) is list and 1 <= len(rows) <= 256 and stats["segment_count"] == len(rows), "EXACT_SEGMENT_COUNT")
    totals = dict(rows=0, padding_rows=0, instructions=0, bytes=0)
    histogram = {}
    for index, row in enumerate(rows):
        need(row["index"] == index and type(row["po2"]) is int and 0 <= row["po2"] <= 18,
             "ORDERED_BOUNDED_SEGMENTS")
        for key in totals:
            need(type(row[key]) is int and row[key] >= 0, "UNSIGNED_SEGMENT_STAT")
            totals[key] += row[key]
        need(row["rows"] == 1 << row["po2"] and row["padding_rows"] <= row["rows"], "PADDED_ROWS_DEFINITION")
        path = directory / (str(index) + ".segment")
        need(pin_file(path, 64*MIB) == dict(path=str(path), bytes=row["bytes"], sha256=row["sha256"]),
             "EXACT_RETAINED_SEGMENT")
        histogram[str(row["po2"])] = histogram.get(str(row["po2"]), 0) + 1
    need(totals["rows"] == stats["row_count"] and totals["padding_rows"] == stats["padding_row_count"]
         and totals["instructions"] == stats["instruction_count"]
         and totals["bytes"] == diagnostic["retained_segment_bytes"], "COMPLETE_SESSION_STATS")
    need({p.name for p in directory.iterdir()} == {str(i) + ".segment" for i in range(len(rows))}, "EXACT_SEGMENT_DIRECTORY")
    # SDK row_count already includes padding; adding padding_row_count again
    # would be wrong. Nonpadding work is row_count minus padding_row_count.
    return dict(segment_count=len(rows), padded_rows=totals["rows"], padding_rows=totals["padding_rows"],
                nonpadding_rows=totals["rows"]-totals["padding_rows"], instructions=totals["instructions"],
                segment_bytes=totals["bytes"], segment_histogram=histogram)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True); parser.add_argument("--input-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_PAIR")
    source = Path(__file__).resolve(strict=True)
    need(source.is_relative_to(HERE) and source.parents[3].name == "sources", "SELECTED_SOURCE_SNAPSHOT")
    sys.path.insert(0, str(source.parents[1]))
    from restricted_composition import prepare_execution as P, fixtures as F, run_controls as K
    from aggregate_claims import bindings as B
    for module, relative in ((P, "restricted_composition/prepare_execution.py"),
                             (F, "restricted_composition/fixtures.py"),
                             (K, "restricted_composition/run_controls.py"),
                             (B, "aggregate_claims/bindings.py")):
        need(Path(module.__file__).resolve(strict=True) == source.parents[1] / relative, "SELECTED_MODULE_ORIGIN")
    inputs = Inputs()
    raw = bounded(args.input, 2*MIB)
    need(digest(raw) == args.input_sha, "ROOT_SELECTED_PAIR_CONFIG")
    inputs.read(dict(path=args.input, bytes=len(raw), sha256=args.input_sha))
    config = parse(raw)
    need(set(config) == {"schema", "fixture", "controls", "receipt", "general", "restricted"}
         and config["schema"] == "DMKN_RC_MATCHED_EXECUTION_INPUT_V1", "PAIR_CONFIG")
    need(Path(config["receipt"]["path"]) == HERE / "module-base-production-01/finish-0/receipt.bin",
         "EXACT_RETAINED_BASE_RECEIPT_PATH")
    output = ordinary(args.output, fresh=True)
    need(output.is_relative_to(HERE) and output.parent == source.parents[4], "PAIR_OUTPUT_IN_SELECTED_RUN")
    output.mkdir()
    save(output / "configuration.json", raw)
    report = dict(schema="DMKN_RC_MATCHED_EXECUTION_RESULT_V1", status="FAIL", arms=[], errors=[],
                  order=["general", "restricted"], proof_calls=0, mathematical_admission=False,
                  full_v5_release=False, full_cost_growth_claim=False, one_pair_not_timing_significance=True)
    arm_cpu = 0.0
    try:
        supervisor_api, jobs = supervisor(inputs)
        controls = config["controls"]
        need(set(controls) == {"result", "outer", "selection"}, "CONTROL_RECORD_SET")
        checked, outer, selection = (inputs.record(controls[key]) for key in ("result", "outer", "selection"))
        control_root = HERE / "restricted-composition-controls-01"
        need(Path(controls["result"]["path"]) == control_root / "evidence/result.json"
             and Path(controls["outer"]["path"]) == control_root / "RESULT.json"
             and Path(controls["selection"]["path"]) == HERE / (control_root.name + "-selection.json")
             and Path(config["fixture"]["path"]) == control_root / "evidence/fixture.json"
             and outer["selection_sha256"] == controls["selection"]["sha256"], "EXACT_NATIVE_CONTROL_FIXTURE")
        clean_job(outer["result"])
        native = checked["native"]
        need(checked["schema"] == "DMKN_RC_CONTROL_RUN_V1" and checked["status"] == "PASS"
             and checked["exit_code"] == 0 and checked["test_binary_sha256"] == CONTROL_BINARY
             and native["status"] == "PASS" and native["errors"] == []
             and [row["name"] for row in native["executed"]] == list(K.EXPECTED_NAMES)
             and all(row["status"] == "PASS" for row in native["executed"])
             and native["expected_refusals"] == list(K.EXPECTED_REFUSALS)
             and (checked["fixture_sha256"], checked["fixture_bytes"]) ==
                 (config["fixture"]["sha256"], config["fixture"]["bytes"])
             and selection["sources"]["software/v5/restricted_composition/fixtures.py"] ==
                 digest(bounded(Path(F.__file__), MIB)), "ADOPTED_EXACT_DIFFERENTIAL_FIXTURE")
        for role in ("general", "restricted"):
            need(set(config[role]) == {"host_build", "assembly"}, "ARM_ADOPTION_FIELDS")
        endpoints = {role: dict(host=host(inputs, role, config[role]["host_build"]))
                     for role in ("general", "restricted")}
        for role in endpoints:
            endpoints[role]["image_id"], endpoints[role]["image"] = image(inputs, role, config[role]["assembly"])
        fixture, receipt = inputs.read(config["fixture"], 4*MIB), inputs.read(config["receipt"], MIB)
        prepared = P.prepare_pair(fixture, fixture_sha256=config["fixture"]["sha256"], parent_receipt=receipt,
            general_image=endpoints["general"]["image_id"], restricted_image=endpoints["restricted"]["image_id"])
        need(B.member_journal(prepared["target"])["module"] == native["executed"][0]["detail"]["module"],
             "ACTUAL_DIFFERENTIAL_TARGET")
        save_json(output / "derivation.json", prepared["derivation"])
        report["derivation"] = prepared["derivation"]
        inputs.rebind()
        for role in ("general", "restricted"):
            wall, cpu = time.monotonic(), time.process_time()
            need(BOOT_WALL + PAIR_WALL - wall >= ARM_WALL + 5, "ORIGINAL_PAIR_REMAINDER")
            arm = dict(role=role, status="FAIL", host_attempts=0, guest_execute_calls=None, proof_calls=0)
            report["arms"].append(arm)
            arm_dir = output / role; ordinary(arm_dir, fresh=True); arm_dir.mkdir()
            host_info = endpoints[role]
            wire, header = prepared[role]["wire"], prepared[role]["header"]
            wire_path, header_path = arm_dir / "wire.bin", arm_dir / "header.bin"
            capsule, diagnostic = arm_dir / "aggregate.snapshot", arm_dir / "diagnostic.json"
            segment_dir = Path(str(capsule) + ".segments")
            def pin_file(path, maximum):
                value = bounded(path, maximum)
                return dict(path=str(path), bytes=len(value), sha256=digest(value))
            try:
                save(wire_path, wire); save(header_path, header)
                argv = [host_info["host"]["path"], "snapshot", host_info["image_id"], host_info["image"]["path"],
                        str(wire_path), str(header_path), str(2**26), "18", "stats", str(capsule), str(diagnostic),
                        "1", config["receipt"]["path"]]
                arm["host_attempts"] = 1
                run = supervisor_api.supervise(argv, ROOT, arm_dir / "command", dict(HOST_LIMITS), jobs.Job,
                                               started=time.monotonic())
                arm["job"] = run
                save_json(arm_dir / "host-job.json", run)
                if diagnostic.exists():
                    arm["diagnostic"] = pin_file(diagnostic, 8*MIB)
                clean_job(run)
                actual = parse(bounded(arm_dir / "command/stdout.txt", MIB))
                data = parse(bounded(diagnostic, 8*MIB))
                need(actual["schema"] == "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1"
                     and actual["status"] == "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED"
                     and actual["aggregate_image"] == host_info["image_id"] and bytes(actual["header"]) == header
                     and actual["capsule_path"] == str(capsule) and actual["assumptions"] == 1
                     and actual["guest_execute_calls"] == 1 and actual["proof_calls"] == 0
                     and actual["mathematical_admission"] is False, "ACTUAL_EXACT_CAPSULE_RESULT")
                need(data["schema"] == "DMKN_SMALL_AGGREGATE_EXECUTION_DIAGNOSTIC_V1"
                     and data["status"] == "CAPSULE_RETAINED_NOT_CERTIFICATE" and data["result"] == actual
                     and data["aggregate_image"] == host_info["image_id"] and bytes(data["header"]) == header
                     and data["elf_sha256"] == host_info["image"]["sha256"]
                     and data["wire_sha256"] == digest(wire) and data["wire_bytes"] == len(wire)
                     and data["cycles_cap"] == 2**26 and data["segment_po2"] == 18
                     and data["samples"]["enabled"] is False and data["error"] is None
                     and data["guest_execute_calls"] == 1 and data["proof_calls"] == 0
                     and data["mathematical_admission"] is False and data["segment_directory"] == str(segment_dir),
                     "COMPLETE_MATCHED_DIAGNOSTIC")
                parents = data["parents"]
                need(len(parents) == 1 and parents[0] == dict(path=config["receipt"]["path"], bytes=len(receipt),
                     sha256=digest(receipt), image=B.RELATION_IMAGE, journal_sha256=digest(prepared["parent"])),
                     "ACTUAL_IDENTICAL_GENUINE_PARENT")
                capsule_pin = pin_file(capsule, 96*MIB)
                need((capsule_pin["bytes"], capsule_pin["sha256"]) ==
                     (actual["capsule_bytes"], actual["capsule_sha256"]), "EXACT_CAPSULE_BYTES")
                stats = statistics(data, ordinary(segment_dir, directory=True), pin_file)
                need(stats["segment_count"] == actual["segments"]
                     and bounded(wire_path, 16*MIB) == wire and bounded(header_path, 192) == header,
                     "FINAL_ARM_INPUT_BINDING")
                arm.update(status="PASS_EXACT_EXECUTION_NOT_CERTIFICATE", capsule=capsule_pin,
                           statistics=stats, header=list(header), guest_execute_calls=1)
            except BaseException as error:
                arm["error"] = type(error).__name__ + ": " + str(error)[:2000]
                raise
            finally:
                arm["controller_cpu_seconds"] = time.process_time() - cpu
                arm["wall_seconds"] = time.monotonic() - wall
                arm_cpu += arm["controller_cpu_seconds"]
                if arm.get("job", {}).get("final_job") is not None:
                    arm["incremental_known_cpu_seconds"] = arm["controller_cpu_seconds"] + arm["job"]["final_job"]["cpu_seconds"]
                if arm["wall_seconds"] > ARM_WALL:
                    arm["status"] = "FAIL_ARM_WALL"
                save_json(arm_dir / "arm-result.json", arm)
            need(arm["status"] == "PASS_EXACT_EXECUTION_NOT_CERTIFICATE", "ARM_FAILED_NO_RETRY")
        general, restricted = report["arms"]
        need(bytes(general["header"])[:12] == bytes(restricted["header"])[:12]
             and bytes(general["header"])[44:] == bytes(restricted["header"])[44:], "MATCHED_H_EXCEPT_IMAGE")
        report["screen"] = dict(padded_rows_at_most_three_quarters=
            4 * restricted["statistics"]["padded_rows"] <= 3 * general["statistics"]["padded_rows"],
            restricted_at_most_64_po18_segments=restricted["statistics"]["segment_count"] <= 64,
            no_cpu_regression=restricted["incremental_known_cpu_seconds"] <= general["incremental_known_cpu_seconds"])
        report["status"] = "PASS_RC_INVESTMENT_SCREEN" if all(report["screen"].values()) else "FAIL_RC_INVESTMENT_SCREEN"
    except BaseException as error:
        report["errors"].append(type(error).__name__ + ": " + str(error)[:2000])
    try:
        inputs.rebind()
        need(time.monotonic() - BOOT_WALL <= PAIR_WALL and time.process_time() - BOOT_CPU <= 60,
             "ORIGINAL_PAIR_CONTROLLER_ENVELOPE")
        entries, total = 0, 0
        for path in output.rglob("*"):
            entries += 1
            need(entries <= 1024 and not path.is_symlink() and not path.is_junction(), "PAIR_OUTPUT_ENTRY_BOUND")
            if path.is_file():
                total += path.stat().st_size
            need(total <= 424*MIB, "PAIR_OUTPUT_BYTE_BOUND")
        report["sampled_output_before_result"] = dict(entries=entries, bytes=total)
    except BaseException as error:
        report["status"] = "FAIL_FINAL_BINDING"
        report["errors"].append(type(error).__name__ + ": " + str(error)[:2000])
    measured_controller = time.process_time() - BOOT_CPU
    shared = measured_controller - arm_cpu
    need(shared >= 0, "DISJOINT_CONTROLLER_ACCOUNTING")
    for arm in report["arms"]:
        if "incremental_known_cpu_seconds" in arm:
            arm["standalone_known_cpu_with_full_shared_prep"] = arm["incremental_known_cpu_seconds"] + shared
    report["accounting"] = dict(shared_preparation_setup_final_binding_and_bookkeeping_cpu=shared,
        adapter_controller_cpu=measured_controller,
        pair_known_cpu_before_report=measured_controller + sum(arm["job"]["final_job"]["cpu_seconds"]
            for arm in report["arms"] if arm.get("job", {}).get("final_job") is not None),
        rule="FULL_SHARED_PREP_TO_EACH_STANDALONE_ARM;ONCE_IN_PAIR;ARM_SUPERVISION_ALREADY_IN_CONTROLLER",
        outer_owner_cost="REPORT_FROM_OUTER_RUN_V5_CHECK;DO_NOT_ADD_NESTED_JOB_TOTALS_TO_INCLUSIVE_OUTER_JOB",
        excluded_tail="FINAL_REPORT_SERIALIZATION_WRITE_EXIT_AND_PYTHON_STARTUP;OUTER_OWNER_CAPTURES_PROCESS_COST",
        build_costs="ONE_TIME_GUEST_HOST_BUILDS_AND_ASSEMBLY_NOT_IN_EXECUTION_SCREEN;REQUIRED_FOR_LATER_INVESTMENT_PRICING")
    report["wall_seconds_before_final_report"] = time.monotonic() - BOOT_WALL
    save_json(output / "RESULT.json", report)
    print(json.dumps({key: report[key] for key in ("status", "errors")}), flush=True)
    return 0 if report["status"] == "PASS_RC_INVESTMENT_SCREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
