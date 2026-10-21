"""One support RC/general execution screen, reusing frozen pair helpers.

Only the exact retained fixture may use the old RC native host. The new support
controls and actual three-crate build/assembly are independently bound. This
adapter creates no proof and does not retry a failed arm or economic screen.
"""
import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
MIB = 1024**2
HELPER_SHA = "6deb0711c94fb6baba44e17a216befcd2ff8e945ede64148f7f7d54e0e241af6"
FIXTURE_SHA = "019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a"
FIXTURE_SOURCE_SHA = "b6f2014319b97b94b04ac9a8caf4068031f7f0e4a854a00aff596d6c47b9e51d"
RETAINED_HOST_SHA = "e3f35fb15ac19ce9862796e50f01807145583307b9b607c8219411c8206271b9"


def load_helpers():
    source = Path(__file__).resolve(strict=True)
    if not (os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize
            and source.is_relative_to(HERE) and source.parents[3].name == "sources"
            and source.relative_to(source.parents[3]).as_posix() ==
                "software/v5/restricted_support_guest/matched_pair.py"):
        raise ValueError("EXACT_ISOLATED_SELECTED_SUPPORT_PAIR_SNAPSHOT")
    path = source.parents[1] / "restricted_composition/matched_pair.py"
    raw = path.read_bytes()
    if len(raw) != 26523 or hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("FROZEN_MATCHED_PAIR_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_support_frozen_pair", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return path, module


HELPER_PATH, H = load_helpers()
need, digest, ordinary, bounded, parse = H.need, H.digest, H.ordinary, H.bounded, H.parse
save, save_json, clean_job = H.save, H.save_json, H.clean_job
Inputs, supervisor, host, statistics = H.Inputs, H.supervisor, H.host, H.statistics
HOST_LIMITS, ARM_WALL, PAIR_WALL = H.HOST_LIMITS, H.ARM_WALL, H.PAIR_WALL


def support_controls(inputs, config):
    controls = config["controls"]
    need(set(controls) == {"result", "outer", "selection"}, "CONTROL_RECORD_SET")
    control_root = HERE / "restricted-support-controls-01"
    expected = {
        "result": (control_root / "command/stdout.txt", 4073,
                   "b9ac046a12a5131d67343596dbee9c48ad0c418fda51c2c20146af1610e6f081"),
        "outer": (control_root / "RESULT.json", 1890,
                  "b1ebc2538329c08fe67509f5d50ea0ead4ac8a174973506f493d160840a27da0"),
        "selection": (HERE / "restricted-support-controls-01-selection.json", 8140,
                      "6f855719615335d5bb88221e90c170a5892d5ded441be0e28e2178a3d687ab35")}
    for role, (path, size, sha) in expected.items():
        need(controls[role] == dict(path=str(path), bytes=size, sha256=sha),
             "EXACT_ADOPTED_SUPPORT_CONTROL_RECORD")
    native, outer, selection = (inputs.record(controls[key]) for key in ("result", "outer", "selection"))
    fixture_path = HERE / "restricted-composition-controls-01/evidence/fixture.json"
    need(config["fixture"] == dict(path=str(fixture_path), bytes=84727, sha256=FIXTURE_SHA)
         and outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1"
         and outer["selection_sha256"] == controls["selection"]["sha256"]
         and selection["name"] == control_root.name
         and selection["runtime_pins"][str(fixture_path)] == FIXTURE_SHA,
         "EXACT_RETAINED_NATIVE_DIFFERENTIAL_FIXTURE")
    clean_job(outer["result"])
    need(native["schema"] == "DMKN_RC_SUPPORT_CONTROLS_V1" and native["status"] == "PASS"
         and native["errors"] == [] and native["executed_count"] == len(native["executed"]) == 30
         and all(row["status"] == "PASS" for row in native["executed"])
         and len(native["expected_refusals"]) == 12
         and native["guest_calls"] == native["proof_calls"] == 0
         and native["crypto_produced"] is False
         and native["executed"][28]["name"] == "first_exact_baseline_j_parents_census"
         and native["executed"][29]["name"] == "second_exact_baseline_j_parents_census",
         "ACTUAL_30_CONTROLS_12_REFUSALS_UNCHANGED_J_AND_ORDERED_PARENTS")
    # The exact adopted stdout above is the actual comparison of full J and
    # ordered pending claims. Its work counters are not guest-row evidence.
    build_pin = dict(path=str(HERE / "restricted-support-build-01/RESULT.json"), bytes=16962,
                     sha256="e26e29de72363e5c0873b9e0c307d3efaaeca4cc5e02144821446b1a06225392")
    built = inputs.record(build_pin)
    need(selection["runtime_pins"][build_pin["path"]] == build_pin["sha256"]
         and built["schema"] == "DMKN_V5_RC_SUPPORT_BUILD_RESULT_V1"
         and built["status"] == "PASS_RC_SUPPORT_TWO_COMPILES_ONLY"
         and built["job"]["active_processes"] == built["job"]["terminated_processes"] == 0,
         "ADOPTED_SUPPORT_NATIVE_BUILD")
    inputs.no_override(HERE / "restricted-support-build-01/FINALIZATION-FAILED.json")
    return native, dict(build=build_pin, controls_outer=controls["outer"], controls_inner=controls["result"])


def image(inputs, role, records, native_adoption):
    if role == "general":
        return H.image(inputs, role, records)
    need(role == "restricted" and set(records) ==
         {"result", "outer", "guest_result", "guest_attempt"}, "SUPPORT_IMAGE_RECORD_SET")
    rows = {name: inputs.record(pin) for name, pin in records.items()}
    assembled, outer, built = rows["result"], rows["outer"], rows["guest_result"]
    assembly_root = HERE / "restricted-support-guest-image-assembly-01"
    guest_root = HERE / "restricted-support-guest-build-01"
    need(Path(records["outer"]["path"]) == assembly_root / "RESULT.json"
         and Path(records["result"]["path"]) == assembly_root / "assembly/RESULT.json"
         and Path(records["guest_result"]["path"]) == guest_root / "RESULT.json"
         and Path(records["guest_attempt"]["path"]) == HERE / (guest_root.name + "-attempt.json")
         and outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1", "EXACT_SUPPORT_IMAGE_ROOTS")
    clean_job(outer["result"])
    need(assembled["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_IMAGE_ASSEMBLY_RESULT_V1"
         and assembled["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
         and assembled["assembler_calls"] == 1
         and assembled["guest_executions"] == assembled["proof_calls"] == 0
         and assembled["mathematical_admission"] is False
         and assembled["guest_build_result"] == records["guest_result"]
         and assembled["selection_sha256"] == built["selection_sha256"]
         and assembled["image_id_origin"] == "ACTUAL_PINNED_ASSEMBLER_NOT_FILE_SHA256"
         and rows["guest_attempt"] == {"status": built["status"],
                                       "result_sha256": records["guest_result"]["sha256"]},
         "ACTUAL_SUPPORT_GUEST_ASSEMBLY")
    need(built["schema"] == "DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_RESULT_V1"
         and built["status"] == "PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY"
         and built["job"]["active_processes"] == built["job"]["terminated_processes"] == 0
         and built["compiler_calls"] == 3 and built["module_compiles"] == built["checker_compiles"] == 0
         and built["selected_source_files"] == built["production_source_closure_files"] == 12
         and len(built["outputs"]) == 5 and built["native_adoption"] == native_adoption,
         "ACTUAL_THREE_CRATE_SUPPORT_BUILD_AND_NATIVE_BINDING")
    inputs.no_override(guest_root / "FINALIZATION-FAILED.json")
    artifact = assembled["image"]
    need(Path(artifact["path"]) == assembly_root / "assembly/aggregate_image.bin", "ACTUAL_SUPPORT_IMAGE_PATH")
    inputs.read(artifact, 64*MIB)
    return assembled["image_id"], artifact


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
    from restricted_composition import prepare_execution as P, fixtures as F
    from aggregate_claims import bindings as B
    for module, relative in ((P, "restricted_composition/prepare_execution.py"),
                             (F, "restricted_composition/fixtures.py"),
                             (B, "aggregate_claims/bindings.py")):
        need(Path(module.__file__).resolve(strict=True) == source.parents[1] / relative, "SELECTED_MODULE_ORIGIN")
    inputs = Inputs()
    inputs.read(dict(path=str(HELPER_PATH), bytes=26523, sha256=HELPER_SHA))
    need(digest(bounded(Path(F.__file__), MIB)) == FIXTURE_SOURCE_SHA, "UNCHANGED_FIXTURE_DEFINITION")
    raw = bounded(args.input, 2*MIB)
    need(digest(raw) == args.input_sha, "ROOT_SELECTED_PAIR_CONFIG")
    inputs.read(dict(path=args.input, bytes=len(raw), sha256=args.input_sha))
    config = parse(raw)
    need(set(config) == {"schema", "fixture", "controls", "receipt", "general", "restricted"}
         and config["schema"] == "DMKN_RC_SUPPORT_MATCHED_EXECUTION_INPUT_V1", "PAIR_CONFIG")
    need(Path(config["receipt"]["path"]) == HERE / "module-base-production-01/finish-0/receipt.bin",
         "EXACT_RETAINED_BASE_RECEIPT_PATH")
    output = ordinary(args.output, fresh=True)
    need(output.is_relative_to(HERE) and output.parent == source.parents[4], "PAIR_OUTPUT_IN_SELECTED_RUN")
    output.mkdir()
    save(output / "configuration.json", raw)
    report = dict(schema="DMKN_RC_SUPPORT_MATCHED_EXECUTION_RESULT_V1", status="FAIL", arms=[], errors=[],
                  order=["general", "restricted"], proof_calls=0, mathematical_admission=False,
                  full_v5_release=False, full_cost_growth_claim=False, one_pair_not_timing_significance=True)
    arm_cpu = 0.0
    try:
        supervisor_api, jobs = supervisor(inputs)
        native, native_adoption = support_controls(inputs, config)
        for role in ("general", "restricted"):
            need(set(config[role]) == {"host_build", "assembly"}, "ARM_ADOPTION_FIELDS")
        endpoints = {role: dict(host=host(inputs, role, config[role]["host_build"]))
                     for role in ("general", "restricted")}
        for role in endpoints:
            endpoints[role]["image_id"], endpoints[role]["image"] = image(inputs, role, config[role]["assembly"], native_adoption)
        need(endpoints["restricted"]["host"]["sha256"] == RETAINED_HOST_SHA, "EXACT_OLD_HOST_FOR_EXACT_FIXTURE")
        fixture, receipt = inputs.read(config["fixture"], 4*MIB), inputs.read(config["receipt"], MIB)
        prepared = P.prepare_pair(fixture, fixture_sha256=config["fixture"]["sha256"], parent_receipt=receipt,
            general_image=endpoints["general"]["image_id"], restricted_image=endpoints["restricted"]["image_id"])
        need(B.member_journal(prepared["target"])["module"] == native["executed"][28]["detail"]["module"]
             and digest(prepared["target"]) == native["executed"][28]["detail"]["journal_sha256"],
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
