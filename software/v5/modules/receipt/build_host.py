"""Compile v5 module host against retained backend, with owned VCTIP cleanup.

Fresh source/selection only; no backend rebuild, image, execution or proof.
Adapted from the independently adopted collection host build supervisor.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
SOURCE = ROOT / "software/v5/modules/receipt"
HELD = ROOT / "experiments/general-checker-guest-02"
HOST = ROOT / "experiments/general-checker-host-05/build-01"
OLD = ROOT / "experiments/general-checker-guest-01"
RUN = HERE / "module-host-build-03"
ATTEMPT = HERE / "module-host-build-03-attempt.json"
INPUTS = {"src/bin/module_host.rs", "src/canonical.rs", "src/commitments.rs", "src/journal.rs",
          "src/policy.rs", "src/trace.rs", "build_host.py", "HOST-BUILD-PLAN.md"}
LIBRARIES = {"anyhow", "bincode", "risc0_zkvm", "serde", "serde_json"}
REGISTRY = HOST / "cargo-home/registry/src/index.crates.io-1949cf8c6b5b557f"
EXTERNAL_NATIVE = {
    "registry+https://github.com/rust-lang/crates.io-index#windows_x86_64_msvc@0.53.0": {
        "path": REGISTRY / "windows_x86_64_msvc-0.53.0/lib",
        "files": {"windows.0.53.0.lib": {
            "bytes": 5221340,
            "sha256": "34b8a86432177dc82c1fe0d34a941502e27a3b3f36bd7e54d6b96a70530bb285"}},
    },
    "registry+https://github.com/rust-lang/crates.io-index#windows_x86_64_msvc@0.52.6": {
        "path": REGISTRY / "windows_x86_64_msvc-0.52.6/lib",
        "files": {"windows.0.52.0.lib": {
            "bytes": 5210890,
            "sha256": "24d8cbc445955b0d48041948a3c71ce2cddb948c089b25ec7106fadd9f3efde0"}},
    },
}

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def load(name, path, digest):
    need(sha(path) == digest, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def target_file_map(a, directory):
    """Cargo may hardlink artifacts. Charge/hash each path; reject reparse paths."""
    a.regular_stat(directory, allow_hardlinks=True)
    rows = {}
    for path in directory.rglob("*"):
        a.regular_stat(path, allow_hardlinks=True)
        need(path.resolve().is_relative_to(directory), "TARGET_MAP_ESCAPE")
        if path.is_file():
            need(len(rows) < a.ENTRY_LIMIT, "TARGET_MAP_ENTRY_LIMIT")
            rows[path.relative_to(directory).as_posix()] = {"bytes": path.stat().st_size, "sha256": sha(path)}
    return rows

def main():
    started, cpu = time.monotonic(), time.process_time()
    need(Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_host.py", "CANONICAL_ROOT")
    need(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
         and sys.flags.no_site and sys.flags.no_user_site and len(sys.argv) == 3, "ISOLATED_CALL")
    cp = Path(sys.argv[1]).resolve(strict=True)
    need(cp.is_relative_to(HERE) and cp.stat().st_size <= 65536 and sha(cp) == sys.argv[2], "CLEARANCE")
    clearance = json.loads(cp.read_bytes())
    need(set(clearance) == {"authorizes_driver_compile_only_and_owned_telemetry_cleanup", "sha256",
         "worker_seconds", "wall_seconds", "worker_memory_mib", "active_processes",
         "host_result_sha256", "host_target_map_sha256"}, "EXACT_SELECTION_FIELDS")
    need(clearance["authorizes_driver_compile_only_and_owned_telemetry_cleanup"] is True
         and set(clearance["sha256"]) == INPUTS
         and clearance["worker_seconds"] == 600 and clearance["wall_seconds"] == 900
         and clearance["worker_memory_mib"] == 4096 and clearance["active_processes"] == 8,
         "EXACT_COMPILE_SCOPE")
    for name, digest in clearance["sha256"].items():
        need(sha(SOURCE / name) == digest, "AUTHORED_PIN " + name)
    need(sha(HOST / "RESULT.json") == clearance["host_result_sha256"], "ADOPTED_HOST_RESULT")
    prior = json.loads((HOST / "RESULT.json").read_bytes())
    need(prior["status"] == "PASS_LOCAL_HOST_BUILD_ONLY" and prior["proof_calls"] == 0,
         "HOST_BUILD_PASSED")
    q = load("adapter_prior", OLD / "prepare.py", "af2d128e831c0bbc3056c516c803fdeab56f69d2a96ca7355a8b22e06f8be529")
    a = load("adapter_artifacts", q.CRYPTO / "artifacts.py", q.HELPERS["artifacts.py"])
    p = load("adapter_provision", q.CRYPTO / "provision_build.py", q.HELPERS["provision_build.py"])
    c = load("adapter_census", q.CRYPTO / "continue_build03.py", q.HELPERS["continue_build03.py"])
    r = load("adapter_phase", ROOT / "experiments/scale-equation-01/runtime.py", q.RUNTIME_SHA)
    p.a, c.a, c.p, c.HERE = a, a, p, HERE
    a.DISK_LIMIT = 12 * 1024**3
    need(Path(sys.executable).resolve() == p.PYTHON and sha(p.PYTHON) == p.PYTHON_SHA
         and sha(p.PYTHON.parent / "python314.dll") == p.PYTHON_DLL_SHA, "PYTHON_PIN")
    need(sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA,
         "JOB_HELPERS")
    sys.path.insert(0, str(p.HELPERS))
    import run_stage
    import domains
    need(Path(run_stage.__file__).resolve() == p.HELPERS / "run_stage.py"
         and Path(domains.__file__).resolve() == p.HELPERS / "domains.py", "JOB_ORIGIN")
    c.h = run_stage
    target = HOST / "target"
    deps = target / "x86_64-pc-windows-msvc/release/deps"
    host_deps = target / "release/deps"
    need(host_deps.is_dir() and host_deps.resolve(strict=True) == host_deps,
         "ADOPTED_HOST_DEPENDENCY_DIRECTORY")
    logs = [row for row in prior["commands"] if row["label"] == "build-host"]
    need(len(logs) == 1 and logs[0]["exit_code"] == 0, "ACTUAL_SUCCESSFUL_BUILD")
    stdout = HOST / "commands/build-host/stdout.txt"
    need(a.pin(stdout) in logs[0]["logs"], "COMPILER_LOG_PIN")
    externs, native, external_seen = {}, set(), set()
    for line in stdout.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("reason") == "compiler-artifact" and row["target"]["name"] in LIBRARIES:
            files = [Path(x).resolve(strict=True) for x in row["filenames"] if x.endswith(".rlib")]
            files = [x for x in files if x.parent == deps]
            if files:
                need(len(files) == 1 and row["target"]["name"] not in externs, "AMBIGUOUS_RLIB")
                externs[row["target"]["name"]] = files[0]
        if row.get("reason") == "build-script-executed":
            for entry in row["linked_paths"]:
                kind, separator, value = entry.partition("=")
                need(not separator or kind in ("native", "dependency", "all"), "UNKNOWN_LINK_PATH_KIND")
                path = Path(value if separator else kind).resolve(strict=True)
                need(path.is_dir(), "NATIVE_LINK_PATH_NOT_DIRECTORY")
                if not path.is_relative_to(target):
                    package = row["package_id"]
                    need(package in EXTERNAL_NATIVE
                         and path == EXTERNAL_NATIVE[package]["path"],
                         "NATIVE_LINK_PATH_ESCAPE")
                    need(target_file_map(a, path) == EXTERNAL_NATIVE[package]["files"],
                         "EXTERNAL_NATIVE_MAP")
                    external_seen.add(package)
                native.add(str(path))
    need(set(externs) == LIBRARIES, "ALL_EXACT_DIRECT_RLIBS")
    need(external_seen == set(EXTERNAL_NATIVE), "EXACT_EXTERNAL_NATIVE_SET")
    target_manifest = HELD / "HOST-TARGET-MAP.json"
    need(sha(target_manifest) == clearance["host_target_map_sha256"], "ADOPTED_HOST_TARGET_MAP")
    target_record = json.loads(target_manifest.read_bytes())
    need(target_record["host_result_sha256"] == clearance["host_result_sha256"], "TARGET_MAP_HOST_BINDING")
    target_map = target_record["files"]
    need(target_file_map(a, target) == target_map, "ADOPTED_TARGET_BYTES")
    runtime = c.runtime_map()
    need(not RUN.exists(), "FRESH_DRIVER_ALLOCATION")
    RUN.mkdir()
    external_bytes = sum(row["bytes"] for item in EXTERNAL_NATIVE.values() for row in item["files"].values())
    external_entries = sum(1 + len(item["files"]) for item in EXTERNAL_NATIVE.values())
    reserve = sum(row["bytes"] for row in target_map.values()) + external_bytes + 3 * 1024**3

    class Budget(a.Budget):
        def refresh(self):
            self.current = {k: v for k, v in c.census(self.run).items()
                            if k in ("working_bytes", "retained_archive_bytes", "entries")}
            self.current["working_bytes"] += reserve
            self.current["retained_archive_bytes"] += 192 * 1024**2
            self.current["entries"] += len(target_map) + external_entries + 30000
            need(self.current["entries"] <= a.ENTRY_LIMIT, "ENTRY_LIMIT")
            self.check()

    budget = Budget(RUN, started + 900)
    phase = None
    sources = None
    result = {"status": "FAIL", "scope": "DRIVER_COMPILE_ONLY_REUSED_RLIBS", "started_utc": p.utc(),
              "clearance": a.pin(cp), "guest_executions": 0, "proof_calls": 0, "network_calls": 0}
    try:
        budget.refresh()
        (RUN / "commands").mkdir()
        sources = {name: {"bytes": (SOURCE / name).stat().st_size, "sha256": clearance["sha256"][name]}
                   for name in INPUTS}
        c.copy_map(SOURCE, RUN / "source", sources, budget)
        with (RUN / "selection.json").open("xb") as stream:
            stream.write(cp.read_bytes())
        env, environment = p.environment(RUN, c.OLD / "rust")
        env["VCToolsUserTelemetryOptOut"] = "1"
        environment["environment_keys_only"] = sorted(env)
        a.save(RUN / "environment-profile.json", environment)
        a.save(RUN / "LINK-INPUTS.json", {"host_result": a.pin(HOST / "RESULT.json"),
            "compiler_stdout": a.pin(stdout), "externs": {k: a.pin(v) for k, v in externs.items()},
            "native_search_paths": sorted(native),
            "dependency_search_paths": [str(deps), str(host_deps)],
            "external_native": {key: {"path": str(item["path"]), "files": item["files"]}
                                for key, item in EXTERNAL_NATIVE.items()},
            "target_map": target_map, "source_map": sources})
        executable = RUN / "module_host.exe"
        argv = [c.OLD / "rust/bin/rustc.exe", "--edition=2021", "--crate-name", "module_host",
                "--target", "x86_64-pc-windows-msvc", "--crate-type", "bin", "-C", "opt-level=3",
                "-C", "lto=fat", "-C", "embed-bitcode=yes", "-C", "overflow-checks=yes", "-C", "panic=unwind",
                "-C", "linker=" + env["CARGO_TARGET_X86_64_PC_WINDOWS_MSVC_LINKER"],
                "-L", "dependency=" + str(deps),
                "-L", "dependency=" + str(host_deps), RUN / "source/src/bin/module_host.rs", "-o", executable]
        for name, path in sorted(externs.items()):
            argv += ["--extern", name + "=" + str(path)]
        for path in sorted(native):
            argv += ["-L", "native=" + path]
        phase = r.phase_class(p, a)("module-host-compile", RUN, budget, env, run_stage.Job, 600)
        phase.invoke("compile-driver", argv, ROOT, allow_build_telemetry=True)
        need(executable.is_file(), "EXACT_DRIVER_OUTPUT")
        need(c.file_map(RUN / "source") == sources, "COPIED_DRIVER_SOURCE_CHANGED")
        result.update(status="PASS_MODULE_HOST_COMPILE_ONLY", executable=a.pin(executable))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)[:4000]
    finally:
        if phase is not None:
            try:
                phase.close()
            except BaseException as error:
                result["status"], result["cleanup_error"] = "FAIL_CLEANUP", str(error)[:2000]
            result["job"], result["commands"] = phase.final_stats, phase.commands
        try:
            need(sha(cp) == sys.argv[2], "SELECTION_CHANGED")
            if (RUN / "selection.json").exists():
                need(sha(RUN / "selection.json") == sys.argv[2], "SAVED_SELECTION_CHANGED")
            for name, digest in clearance["sha256"].items():
                need(sha(SOURCE / name) == digest, "USED_INPUT_CHANGED")
            need(sha(OLD / "prepare.py") == "af2d128e831c0bbc3056c516c803fdeab56f69d2a96ca7355a8b22e06f8be529",
                 "PRIOR_HELPER_CHANGED")
            for name, digest in q.HELPERS.items():
                need(sha(q.CRYPTO / name) == digest, "HELPER_CHANGED")
            need(sha(ROOT / "experiments/scale-equation-01/runtime.py") == q.RUNTIME_SHA
                 and sha(p.HELPERS / "run_stage.py") == p.HELPER_SHA
                 and sha(p.HELPERS / "domains.py") == p.DOMAINS_SHA, "SUPERVISOR_CHANGED")
            need(a.pin(stdout) in logs[0]["logs"], "COMPILER_LOG_CHANGED")
            if sources is not None and (RUN / "source").is_dir():
                need(c.file_map(RUN / "source") == sources, "STAGED_DRIVER_SOURCE_CHANGED")
            need(sha(HOST / "RESULT.json") == clearance["host_result_sha256"]
                 and sha(target_manifest) == clearance["host_target_map_sha256"]
                 and target_file_map(a, target) == target_map and c.runtime_map() == runtime, "HOST_LINK_INPUTS_CHANGED")
            for item in EXTERNAL_NATIVE.values():
                need(item["path"].resolve(strict=True) == item["path"]
                     and target_file_map(a, item["path"]) == item["files"],
                     "EXTERNAL_NATIVE_INPUT_CHANGED")
            budget.refresh()
            result["final_storage"] = c.census(RUN)
        except BaseException as error:
            result["status"], result["final_check_error"] = "FAIL_FINAL_CHECK", str(error)[:3000]
        result.update(controller_cpu_seconds=time.process_time() - cpu,
                      wall_seconds=time.monotonic() - started, sampled_reserved_peaks=budget.peak,
                      finished_utc=p.utc())
        if result["wall_seconds"] > 900:
            result["status"] = "FAIL_TOTAL_WALL_LIMIT"
        a.save(RUN / "RESULT.json", result)
    print(json.dumps({key: result.get(key) for key in ("status", "error", "wall_seconds")}))
    return 0 if result["status"] == "PASS_MODULE_HOST_COMPILE_ONLY" else 1

def attempt():
    """Preserve controller-only costs even when main refuses before allocation."""
    started, cpu = time.monotonic(), time.process_time()
    need(Path.cwd() == ROOT and Path(__file__).resolve() == SOURCE / "build_host.py",
         "CANONICAL_ATTEMPT_ROOT")
    need(not ATTEMPT.exists(), "FRESH_ATTEMPT_EVIDENCE")
    report = {"schema": "v5-module-host-build-attempt-02", "scope": "CONTROLLER_ONLY_NOT_WORKER_CPU",
              "allocation_preexisted": RUN.exists(), "status": "FAIL_PREALLOCATION",
              "worker_cpu_seconds": None, "worker_cost_evidence": None}
    code = 1
    try:
        code = main()
        report["status"] = "RETURNED_PASS" if code == 0 else "RETURNED_FAILURE"
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)[:4000]
        report["status"] = "FAIL_AFTER_ALLOCATION" if RUN.exists() else "FAIL_PREALLOCATION"
    finally:
        report["allocation_exists"] = RUN.exists()
        result_path = RUN / "RESULT.json"
        if not report["allocation_preexisted"] and result_path.is_file():
            report["worker_cost_evidence"] = {
                "path": str(result_path), "bytes": result_path.stat().st_size,
                "sha256": sha(result_path)}
        report.update(exit_code=code, controller_cpu_seconds=time.process_time() - cpu,
                      controller_wall_seconds=time.monotonic() - started,
                      scope_note="Outer controller times include main controller time; do not add them. "
                                 "Worker CPU, if any, is only in the referenced run result.")
        with ATTEMPT.open("xb") as stream:
            stream.write((json.dumps(report, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"attempt": str(ATTEMPT), "status": report["status"],
                      "error": report.get("error"), "exit_code": code}))
    return code

if __name__ == "__main__":
    raise SystemExit(attempt())


