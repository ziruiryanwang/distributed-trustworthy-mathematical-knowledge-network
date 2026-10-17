"""Selected-only offline allocation refinement: four Rust rlibs, one host link.

No execution on import. Never edit the retained SDK, invoke Cargo/build scripts,
or run the produced host. The root must select and review a finite operation.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/prover_memory"
SDK_REL = "experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8"
OLD_STAGE = HERE / "small-aggregate-stage-host-build-01"
OLD_INTEGRATION = HERE / "proof-validation-integration-build-01"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
SUPPORT = ROOT / "software/v5/modules/native/proof_validation/control.py"
SUPPORT_SHA = "91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1"
DESCRIPTOR_SHA = "c93a45a6a558718c931c39b121e9bcffa7d464ecaa1d5b0e80185efd6cace710"
PATCH_SHA = "a53940b67580e215c55c2eae1e33e12f93a410193dde5f6414f533e4517fdc6c"
PASS = "PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY"
NAMES = ("risc0_circuit_rv32im", "risc0_zkvm", "dmkn_module_relation",
         "dmkn_aggregate_relation", "small_aggregate_stage_host")
SOURCE_SET = {"software/v5/prover_memory/" + name for name in
              ("build.py", "SOURCE.json", "preflight.patch", "BUILD-RECIPE.md")}
LIMITS = {
    "worker_cpu_seconds": 240, "worker_wall_seconds": 300, "memory_mib": 3072,
    "active_processes": 6, "total_worker_cpu_seconds": 1200,
    "ordinary_controller_cpu_seconds": 120, "controller_cpu_seconds": 180,
    "total_wall_seconds": 1800, "fresh_output_bytes": 1073741824,
    "fresh_output_entries": 8192, "command_log_bytes": 1048576,
}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, "DUPLICATE_JSON_FIELD")
        result[key] = value
    return result


def read(path):
    need(path.stat().st_size <= 2 * 1024**2, "ADMIN_INPUT_BYTES")
    return json.loads(path.read_bytes(), object_pairs_hook=pairs,
                      parse_constant=lambda value: need(False, "NONFINITE_JSON"))


def save(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode())


def pin(path):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def short_pin(value):
    return {"bytes": value["bytes"], "sha256": value["sha256"]}


def checked_relative(value):
    need(type(value) is str and "\\" not in value and ":" not in value,
         "POSIX_RELATIVE_PATH")
    parts = value.split("/")
    need(parts and all(part not in ("", ".", "..") for part in parts), "RELATIVE_PARTS")
    return Path(*parts)


def check_pin(path, expected):
    need(type(expected) is dict and set(expected) == {"bytes", "sha256"}
         and type(expected["bytes"]) is int and expected["bytes"] >= 0
         and type(expected["sha256"]) is str
         and re.fullmatch(r"[0-9a-f]{64}", expected["sha256"]), "PIN_FIELDS")
    need(path.is_absolute() and path.resolve(strict=True) == path and path.is_file()
         and path.stat().st_size == expected["bytes"] and sha(path) == expected["sha256"],
         "FILE_PIN:" + str(path))


def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_exact_patch(original, patch):
    """Two exact unified hunks in memory; no fuzz, offset, shell or SDK writes."""
    need(b"\r" not in original and b"\r" not in patch
         and not original.startswith(b"\xef\xbb\xbf")
         and original.endswith(b"\n") and patch.endswith(b"\n"), "EXACT_LF_ENCODING")
    source = original.splitlines(keepends=True)
    lines = patch.splitlines(keepends=True)
    need(lines[:2] == [b"--- a/risc0/circuit/rv32im/src/prove/preflight.rs\n",
                       b"+++ b/risc0/circuit/rv32im/src/prove/preflight.rs\n"], "PATCH_TARGET")
    output, cursor, i, hunks = [], 0, 2, 0
    while i < len(lines):
        match = re.fullmatch(rb"@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n", lines[i])
        need(match is not None, "EXACT_HUNK_HEADER")
        old_start, old_count, new_start, new_count = map(int, match.groups())
        start = old_start - 1
        need(cursor <= start <= len(source), "ORDERED_HUNK")
        output.extend(source[cursor:start])
        cursor = start
        need(len(output) == new_start - 1, "EXACT_NEW_HUNK_POSITION")
        old_seen = new_seen = 0
        i += 1
        while i < len(lines) and not lines[i].startswith(b"@@ "):
            marker, body = lines[i][:1], lines[i][1:]
            need(marker in (b" ", b"-", b"+") and body.endswith(b"\n"), "HUNK_LINE")
            if marker in (b" ", b"-"):
                need(cursor < len(source) and source[cursor] == body, "EXACT_HUNK_CONTEXT")
                cursor += 1
                old_seen += 1
            if marker in (b" ", b"+"):
                output.append(body)
                new_seen += 1
            i += 1
        need((old_seen, new_seen) == (old_count, new_count), "EXACT_HUNK_COUNTS")
        hunks += 1
    need(hunks == 2, "EXACT_TWO_HUNKS")
    output.extend(source[cursor:])
    return b"".join(output)


def main():
    started, cpu = time.monotonic(), time.process_time()
    finalizing = closing_phase = False

    def envelope():
        cap = LIMITS["controller_cpu_seconds"] if finalizing else LIMITS["ordinary_controller_cpu_seconds"]
        need(time.monotonic() - started <= LIMITS["total_wall_seconds"]
             and time.process_time() - cpu <= cap, "WHOLE_BUILD_CONTROLLER_ENVELOPE")

    need(os.name == "nt" and Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and len(sys.argv) == 3, "ISOLATED_CANONICAL_BUILD")
    selection = Path(sys.argv[1]).resolve(strict=True)
    need(selection.parent == HERE and re.fullmatch(r"[0-9a-f]{64}", sys.argv[2])
         and sha(selection) == sys.argv[2], "EXACT_SELECTION")
    chosen = read(selection)
    need(set(chosen) == {"schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"}
         and chosen["schema"] == "DMKN_V5_PROVER_ALLOCATION_BUILD_V1"
         and chosen["authorizes_compile_only"] is True and chosen["limits"] == LIMITS
         and type(chosen["name"]) is str and re.fullmatch(r"prover-allocation-build-[0-9]{2}", chosen["name"]),
         "SELECTION_FIELDS")
    need(type(chosen["sources"]) is dict and set(chosen["sources"]) == SOURCE_SET, "FOUR_ADAPTER_SOURCES")
    for relative, expected in chosen["sources"].items():
        check_pin(ROOT / checked_relative(relative), expected)
    need(sha(SOURCE / "SOURCE.json") == DESCRIPTOR_SHA and sha(SOURCE / "preflight.patch") == PATCH_SHA,
         "FROZEN_DESCRIPTOR_AND_PATCH")
    descriptor = read(SOURCE / "SOURCE.json")
    need(descriptor["schema"] == "DMKN_V5_PROVER_ALLOCATION_SOURCE_V1"
         and descriptor["canonical_root"] == str(ROOT), "SOURCE_DESCRIPTOR")
    run = HERE / chosen["name"]
    attempt = HERE / (chosen["name"] + "-attempt.json")
    need(not run.exists() and not attempt.exists(), "FRESH_BUILD_AND_ATTEMPT")

    source_inputs, copies = {}, {}

    def retain(path, expected):
        expected = short_pin(expected)
        key = str(path)
        need(key not in source_inputs or source_inputs[key] == expected, "INPUT_PIN_CONFLICT")
        source_inputs[key] = expected

    def copy_plan(origin, relative, expected, *, transformed=False):
        checked_relative(relative)
        need(relative not in copies, "COPY_TARGET_COLLISION")
        retain(origin, expected)
        target_pin = short_pin(descriptor["expected_patched"]) if transformed else short_pin(expected)
        copies[relative] = {"origin": origin, "pin": target_pin, "transformed": transformed}

    for relative, expected in chosen["sources"].items():
        copy_plan(ROOT / relative, "source/adapters/" + relative, expected)
    records = {item["path"]: item for item in descriptor["retained_records"]}
    need(len(records) == 19, "NINETEEN_RETAINED_RECORDS")
    for index, item in enumerate(descriptor["retained_records"]):
        relative = item["path"]
        origin = ROOT / checked_relative(relative)
        copy_plan(origin, f"source/evidence/{index:02d}-" + origin.name, item)
        if relative.startswith(SDK_REL + "/"):
            copy_plan(origin, "source/sdk/" + relative[len(SDK_REL) + 1:], item)
    for inventory in descriptor["sdk_source_inventories"]:
        for item in inventory["files"]:
            relative = item["path"]
            origin = ROOT / SDK_REL / checked_relative(relative)
            copy_plan(origin, "source/sdk/" + relative, item,
                      transformed=str(origin) == str(ROOT / descriptor["source"]["path"]))
    need(sum(len(item["files"]) for item in descriptor["sdk_source_inventories"]) == 113,
         "EXACT_SDK_SOURCE_COUNT")
    for old, destination in ((OLD_INTEGRATION, "source/integration/"), (OLD_STAGE, "source/stage/")):
        map_path = old / "source-map.json"
        check_pin(map_path, short_pin(records[map_path.relative_to(ROOT).as_posix()]))
        for relative, expected in read(map_path).items():
            copy_plan(old / "source" / checked_relative(relative), destination + relative, expected)
    generated = [item for item in records.values() if item["path"].endswith("/out/preflight_opt_gen.rs")]
    need(len(generated) == 1, "EXACT_GENERATED_PREFLIGHT")
    copy_plan(ROOT / generated[0]["path"], "generated/rv32im/preflight_opt_gen.rs", generated[0])
    for path, expected in source_inputs.items():
        envelope()
        check_pin(Path(path), expected)

    retained_selection = read(OLD_STAGE / "selection.json")
    need(type(chosen["runtime_pins"]) is dict
         and chosen["runtime_pins"] == retained_selection["runtime_pins"]
         and len(chosen["runtime_pins"]) == 1071, "EXACT_RETAINED_RUNTIME_MAP")
    for item in descriptor["direct_extern_inputs"]:
        for entry in item["externs"]:
            need(chosen["runtime_pins"].get(entry["path"]) == entry["sha256"]
                 and Path(entry["path"]).stat().st_size == entry["bytes"], "DIRECT_EXTERN_PIN")

    h = load("allocation_support", SUPPORT, SUPPORT_SHA)
    old = h.load("allocation_prior_build", h.PREDECESSOR, h.PREDECESSOR_SHA)
    q = h.load("allocation_prior", old.PRIOR, old.PRIOR_SHA)
    a = h.load("allocation_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = h.load("allocation_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = h.load("allocation_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = h.load("allocation_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    r.LOG_LIMIT = LIMITS["command_log_bytes"]
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PINNED_CONTROLLER")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
         and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "PINNED_JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_IMPORT_ORIGINS")
    c.h = run_stage
    helper_pins = {SUPPORT: SUPPORT_SHA, h.PREDECESSOR: h.PREDECESSOR_SHA,
                   old.PRIOR: old.PRIOR_SHA, ROOT / "experiments/scale-equation-01/runtime.py": q.RUNTIME_SHA,
                   p.PYTHON: p.PYTHON_SHA, p.PYTHON.parent / "python314.dll": p.PYTHON_DLL_SHA,
                   p.HELPERS / "run_stage.py": p.HELPER_SHA, p.HELPERS / "domains.py": p.DOMAINS_SHA,
                   r.VCTIP: r.VCTIP_SHA}
    helper_pins.update({q.CRYPTO / name: digest for name, digest in q.HELPERS.items()})
    old_environment = read(OLD_STAGE / "environment-profile.json")
    for item in old_environment["host_binaries"]:
        helper_pins[Path(item["path"])] = item["sha256"]

    def check_inputs(*, full_runtime=True):
        envelope()
        need(sha(selection) == sys.argv[2], "SELECTION_CHANGED")
        for path, expected in source_inputs.items():
            envelope()
            check_pin(Path(path), expected)
        for path, digest in helper_pins.items():
            envelope()
            need(path.resolve(strict=True) == path and path.is_file() and sha(path) == digest,
                 "HELPER_CHANGED:" + str(path))
        if full_runtime:
            total = 0
            for name, digest in chosen["runtime_pins"].items():
                envelope()
                path = Path(name)
                need(type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest)
                     and path.is_absolute() and path.resolve(strict=True) == path and path.is_file()
                     and sha(path) == digest, "RETAINED_RUNTIME_CHANGED:" + name)
                total += path.stat().st_size
            need(total == 2320491997, "EXACT_RETAINED_RUNTIME_BYTES")

    def expand(value):
        need(type(value) is str, "TEMPLATE_STRING")
        result = value.replace("${RUN}", str(run))
        need("${" not in result, "UNEXPANDED_TEMPLATE")
        return result

    steps = descriptor["compiler_recipe"]["ordered_steps"]
    need(tuple(item["name"] for item in steps) == NAMES, "EXACT_FIVE_STEPS")
    commands = [{"name": item["name"], "argv": [expand(value) for value in item["argv_template"]]}
                for item in steps]
    outputs = {item["name"]: Path(expand(item["output_template"])) for item in steps}
    for row in commands:
        argv = row["argv"]
        need(argv[0] == str(RUST / "bin/rustc.exe") and argv[0] in chosen["runtime_pins"]
             and "--test" not in argv and argv.count("-o") == 1
             and argv[argv.index("-o") + 1] == str(outputs[row["name"]]), "EXACT_COMPILER_OUTPUT")
        need(outputs[row["name"]].is_relative_to(run), "OUTPUT_ROOT")
        for i, argument in enumerate(argv):
            if argument == "--extern":
                path = argv[i + 1].split("=", 1)[1]
                need(path in chosen["runtime_pins"] or Path(path) in outputs.values(), "BOUND_EXTERN")

    check_inputs()
    run.mkdir()
    phases, completed_outputs = [], {}
    source_map = {"adapters": chosen["sources"], "files": {name: row["pin"] for name, row in copies.items()}}
    result = {
        "schema": "DMKN_V5_PROVER_ALLOCATION_BUILD_RESULT_V1", "status": "FAIL",
        "selection_sha256": sys.argv[2], "descriptor_sha256": DESCRIPTOR_SHA, "patch_sha256": PATCH_SHA,
        "limits": LIMITS, "runtime_pin_count": 1071, "runtime_pin_bytes": 2320491997,
        "backend_rust_crate_rebuilds": 0, "relation_rust_crate_rebuilds": 0, "stage_host_links": 0,
        "checker_rebuilds": 0, "native_circuit_rebuilds": 0, "guest_rebuilds": 0,
        "host_calls": 0, "guest_calls": 0, "proof_calls": 0, "network_calls": 0,
        "authority": "FIVE_STEP_COMPILE_ONLY_NOT_MATHEMATICAL_ADMISSION",
        "source_map_sha256": None, "commands_sha256": None,
        "environment_sha256": None, "input_map_sha256": None, "outputs": completed_outputs,
        "executable": None,
    }

    class Budget:
        def __init__(self):
            self.current = {}
            self.peak = {"working_bytes": 0, "entries": 0}

        def refresh(self):
            envelope()
            self.current = c.census(run)
            envelope()
            need(self.current["working_bytes"] <= LIMITS["fresh_output_bytes"]
                 and self.current["entries"] <= LIMITS["fresh_output_entries"], "BUILD_OUTPUT_ENVELOPE")
            for key in self.peak:
                self.peak[key] = max(self.peak[key], self.current[key])

    budget = Budget()

    def verify_snapshot():
        actual = {"source/" + key: value for key, value in c.file_map(run / "source").items()}
        actual.update({"generated/" + key: value for key, value in c.file_map(run / "generated").items()})
        need(actual == source_map["files"], "EXACT_COMPLETE_SOURCE_SNAPSHOT")
        for item in completed_outputs.values():
            check_pin(Path(item["path"]), short_pin(item))

    def aggregate_job():
        rows = [{"name": name, "stats": getattr(phase, "final_stats", None)} for name, phase in phases]
        complete = all(row["stats"] is not None for row in rows)
        summed = ("cpu_seconds", "user_cpu_seconds", "kernel_cpu_seconds", "active_processes",
                  "total_processes", "terminated_processes")
        total = {key: sum(row["stats"][key] for row in rows) if complete else None for key in summed}
        total["peak_job_private_commit_bytes"] = (max((row["stats"]["peak_job_private_commit_bytes"]
                                                       for row in rows), default=0) if complete else None)
        total["phase_jobs"] = rows
        return total

    try:
        (run / "commands").mkdir()
        (run / "lib").mkdir()
        raw_selection = selection.read_bytes()
        need(hashlib.sha256(raw_selection).hexdigest() == sys.argv[2], "SAVED_SELECTION_BYTES")
        with (run / "selection.json").open("xb") as stream:
            stream.write(raw_selection)
        patch = (SOURCE / "preflight.patch").read_bytes()
        need(hashlib.sha256(patch).hexdigest() == PATCH_SHA, "PATCH_BYTES")
        for relative, row in copies.items():
            envelope()
            raw = row["origin"].read_bytes()
            expected_input = source_inputs[str(row["origin"])]
            need(len(raw) == expected_input["bytes"]
                 and hashlib.sha256(raw).hexdigest() == expected_input["sha256"], "COPY_INPUT_REBIND")
            if row["transformed"]:
                raw = apply_exact_patch(raw, patch)
            need(len(raw) == row["pin"]["bytes"]
                 and hashlib.sha256(raw).hexdigest() == row["pin"]["sha256"], "DERIVED_SNAPSHOT_PIN")
            target = run / checked_relative(relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(raw)
            check_pin(target, row["pin"])
        save(run / "source-map.json", source_map)
        save(run / "compile-commands.json", commands)
        result["source_map_sha256"] = sha(run / "source-map.json")
        result["commands_sha256"] = sha(run / "compile-commands.json")
        save(run / "INPUT-MAP.json", {"source_inputs": source_inputs,
             "runtime_pins": chosen["runtime_pins"], "helper_pins": {str(path): digest for path, digest in helper_pins.items()},
             "trust_boundary": "Pinned owner build/toolchain plus Windows system DLLs; not hermetic or sandboxed"})
        result["input_map_sha256"] = sha(run / "INPUT-MAP.json")
        base_env, environment = p.environment(run, RUST)
        need(environment["host_binaries"] == old_environment["host_binaries"], "RETAINED_ENVIRONMENT_TOOLS")
        base_env["VCToolsUserTelemetryOptOut"] = "1"
        base_env["CARGO_NET_OFFLINE"] = "true"
        per_step_env = {}
        for item in steps:
            env = {key: value for key, value in base_env.items()
                   if key != "OUT_DIR" and not key.startswith("CARGO_PKG_")
                   and key not in ("CARGO_MANIFEST_DIR", "CARGO_MANIFEST_PATH")}
            env.update({key: expand(value) for key, value in item["environment_overlay"].items()})
            per_step_env[item["name"]] = env
        environment.update(explicit_environment=base_env, step_environments=per_step_env,
                           environment_keys_only=sorted(base_env))
        save(run / "environment-profile.json", environment)
        result["environment_sha256"] = sha(run / "environment-profile.json")
        verify_snapshot()
        budget.refresh()

        class InclusiveJob(run_stage.Job):
            def stats(self):
                measured = super().stats()
                if not finalizing and not closing_phase:
                    need(measured["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "PHASE_WORKER_CPU")
                    previous = sum(phase.final_stats["cpu_seconds"] for _, phase in phases
                                   if phase.final_stats is not None)
                    need(previous + measured["cpu_seconds"] <= LIMITS["total_worker_cpu_seconds"],
                         "WHOLE_WORKER_CPU")
                return measured

        def exact_job(seconds, memory, active_processes):
            need((seconds, memory, active_processes) == (300, 4096, 8), "RETAINED_PHASE_CONSTRUCTOR")
            return InclusiveJob(240, 3072, active_processes=6)

        phase_type = r.phase_class(p, a)
        for row in commands:
            check_inputs(full_runtime=False)
            verify_snapshot()
            phase = phase_type("allocation-" + row["name"], run, budget,
                               per_step_env[row["name"]], exact_job, LIMITS["worker_wall_seconds"])
            phases.append((row["name"], phase))
            try:
                phase.invoke(row["name"], row["argv"], ROOT, allow_build_telemetry=True)
            finally:
                closing_phase = True
                try:
                    phase.close()
                finally:
                    closing_phase = False
            need(phase.final_stats["cpu_seconds"] <= LIMITS["worker_cpu_seconds"], "CLOSED_PHASE_CPU")
            completed_outputs[row["name"]] = pin(outputs[row["name"]])
            counter = ("backend_rust_crate_rebuilds" if row["name"] in NAMES[:2]
                       else "relation_rust_crate_rebuilds" if row["name"] in NAMES[2:4]
                       else "stage_host_links")
            result[counter] += 1
            budget.refresh()
        result.update(status=PASS, executable=completed_outputs[NAMES[-1]])
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        finalizing = True
        for _, phase in phases:
            if not phase.closed:
                try:
                    phase.close()
                except BaseException as error:
                    result.update(status="FAIL_CLEANUP", cleanup_error=str(error)[:2000])
        result["job"] = aggregate_job()
        result["commands"] = [command for _, phase in phases for command in phase.commands]
        try:
            check_inputs()
            need(sha(run / "selection.json") == sys.argv[2], "FINAL_SELECTION_COPY")
            verify_snapshot()
            need(sha(run / "source-map.json") == result["source_map_sha256"]
                 and sha(run / "compile-commands.json") == result["commands_sha256"]
                 and sha(run / "environment-profile.json") == result["environment_sha256"]
                 and sha(run / "INPUT-MAP.json") == result["input_map_sha256"], "FINAL_RECORD_PINS")
            if result["status"] == PASS:
                need(len(phases) == len(result["commands"]) == len(completed_outputs) == 5
                     and result["job"]["active_processes"] == result["job"]["terminated_processes"] == 0
                     and result["job"]["cpu_seconds"] <= LIMITS["total_worker_cpu_seconds"], "FULL_BUILD_CLOSURE")
            budget.refresh()
        except BaseException as error:
            result.update(status="FAIL_FINAL_CHECK", final_error=str(error)[:3000])
        result.update(controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, output_census=budget.current,
                      sampled_peaks=budget.peak,
                      accounting="CONTROLLER_DISJOINT_FROM_SUM_OF_SERIAL_INCLUSIVE_WORKER_JOBS;FINAL_REPORT_EXIT_TAIL_EXCLUDED")
        save(run / "RESULT.json", result)
        save(attempt, {"status": result["status"], "result_sha256": sha(run / "RESULT.json")})
        try:
            budget.refresh()
        except BaseException as error:
            result["status"] = "FAIL_FINALIZATION"
            save(run / "FINALIZATION-FAILED.json", {"status": "FAIL_FINALIZATION",
                 "overrides_result_and_attempt": True, "result_sha256": sha(run / "RESULT.json"),
                 "error": str(error)[:3000]})
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
