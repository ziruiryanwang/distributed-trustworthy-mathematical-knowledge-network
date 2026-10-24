"""One real-owner context query using saved metadata; no native/search rerun.

Uses the existing protected synthetic owner in place. Opening may settle old
RESERVED operations as INTERRUPTED; this is not a database-read-only claim.
Root schedules this after other owner operations and selects the exact package.
No admission, source compilation, extraction, peer request or retry is performed.
"""
from __future__ import annotations

import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import msvcrt
import os
from pathlib import Path
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
SAVED = LOCAL/"ordinary-current-relocated-smoke-01/smoke"
PUBLIC = LOCAL/"ordinary-query-public-01/public"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_PIN = {"bytes": 38940, "sha256": "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"}
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
FOUNDATION = "884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282"
CONTEXT = "94827b21912710d45d0a459d089b741d39a15caf9b60847b5f0553be7457cece"
STORE = "c60f943f157cccf4c4be478cc2b600b609f79e81084fda3eca691ef0ccbddfeb"
QUERY_SHA = "449b5fea77f4c19cfbde47346ea255ae1277a1cf53e3030a6baa9de3f8659af6"
PINS = {
    PUBLIC/"IMMUTABLE-FILES.json": "9952b07e2ef0dea7a3cb8513971e19b524aa198f4aed6fb89ec8024774ffd319",
    PUBLIC/"query-local/native-type.json": "226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480",
    PUBLIC/"fixtures/known-bindings.json": "0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f",
    PUBLIC/"query-prepared/QUERY.json": "eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a",
    PUBLIC/"query-prepared/SPECS.json": "7c707bb2b3f5cc2628eef4fcb933c7944156ead940ad02465fa42084049dc72d",
    PUBLIC/"query-prepared/RESULT.json": "a7dbe7e1ff6e028eee87adfc1492e479a2abd50b57169503889bcd11428c14a8",
    SAVED/"catalog/ADOPTION.json": "6a1cbaf4edb1e74e1a27c34def157d64249c5a91eb822274c3bf5d4f11d399db",
    SAVED/"fixtures/custody-limits.json": "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe",
    SAVED/"completion/RESULT.json": "60cf12bd8b954a2a61a7d8a2aeb006e4ea9bdee087a8846de3eec1e39224bf79",
}
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(HELPER_PIN["bytes"]+1)
    need(len(raw) == HELPER_PIN["bytes"] and hashlib.sha256(raw).hexdigest() == HELPER_PIN["sha256"],
         "CONTEXT_INTEGRATION_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_context_integration_helpers", HELPER)
    h = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), h.__dict__)
    h.ordinary(HELPER)
    return h


def prepare(c, h, args):
    package, output = h.ordinary(args.package, directory=True), h.ordinary(args.output, directory=True, fresh=True)
    need(package.is_relative_to(LOCAL) and output == LOCAL/"ordinary-context-query-integration-01/integration",
         "CONTEXT_INTEGRATION_SELECTED_PATHS")
    c.package, c.output = package, output
    roots = [package, output, SAVED, PUBLIC, PYTHON.parent, LEAN]
    need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
             for i, a in enumerate(roots) for b in roots[i+1:]), "CONTEXT_INTEGRATION_DISJOINT_PATHS")
    c.hold(Path(__file__).resolve()); c.hold(HELPER, HELPER_PIN)
    for digest in (args.profile_sha256, args.assembly_sha256):
        need(re.fullmatch(r"[0-9a-f]{64}", digest), "CONTEXT_INTEGRATION_DESCRIPTOR_HASH")
    need(c.hold(package/"PROFILE.json")["sha256"] == args.profile_sha256,
         "CONTEXT_INTEGRATION_PROFILE_PIN")
    profile = c.document(package/"PROFILE.json", 2*MIB)
    need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         profile["installation_manifest_sha256"] == INSTALLATION and
         profile["files"]["query.py"]["sha256"] == QUERY_SHA, "CONTEXT_INTEGRATION_QUERY_PROFILE")
    need(c.hold(package/"installation/INSTALLATION.json")["sha256"] == INSTALLATION,
         "CONTEXT_INTEGRATION_INSTALLATION_PIN")
    manifest = c.document(package/"installation/INSTALLATION.json", 2*MIB)
    need(h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(manifest["implementation"])) ==
         IMPLEMENTATION and manifest["implementation"]["semantic_id"] == SEMANTIC,
         "CONTEXT_INTEGRATION_IMPLEMENTATION")
    expected_files = set(profile["files"]) | {"PROFILE.json", "ASSEMBLY.json", "installation/INSTALLATION.json"}
    for logical, expected in profile["files"].items():
        c.hold(package/h.relative(logical), expected)
    runtimes = {"python_runtime": PYTHON.parent, "lean_runtime": LEAN}
    for logical, expected in manifest["files"].items():
        parts = h.relative(logical).parts
        if parts[0] in runtimes:
            path = runtimes[parts[0]].joinpath(*parts[1:])
        else:
            path = package/"installation"/logical
            expected_files.add("installation/"+logical)
        c.hold(path, expected)
    need(c.hold(package/"ASSEMBLY.json")["sha256"] == args.assembly_sha256,
         "CONTEXT_INTEGRATION_ASSEMBLY_PIN")
    assembly = c.document(package/"ASSEMBLY.json", 2*MIB)
    need(assembly["status"] == "ASSEMBLED_NOT_ADOPTED" and
         assembly["profile_sha256"] == args.profile_sha256 and
         assembly["installation_manifest_sha256"] == INSTALLATION and
         assembly["implementation_id"] == IMPLEMENTATION and
         assembly["files_excluding_profile"] == 134 and assembly["added"] == [] and
         set(assembly["changed"]) in ({"module/OrdinaryModule.lean"}, {"module/OrdinaryModule.lean", "query.py"}) and
         assembly["changed_or_added"] == {key: profile["files"][key] for key in assembly["changed"]},
         "CONTEXT_INTEGRATION_ASSEMBLY_BINDING")
    need(c.capture_tree(package) == expected_files, "CONTEXT_INTEGRATION_PACKAGE_CENSUS")
    for path, digest in PINS.items():
        need(c.hold(path)["sha256"] == digest, "CONTEXT_INTEGRATION_SAVED_PIN:"+str(path))
    retained = c.document(PUBLIC/"IMMUTABLE-FILES.json")
    need(type(retained) is dict and len(retained) == 463, "CONTEXT_INTEGRATION_PRIOR_MAP_CENSUS")
    for path, expected in retained.items():
        c.hold(h.ordinary(path), expected)
    adoption = c.document(SAVED/"catalog/ADOPTION.json")
    need(adoption["store_id"] == STORE and adoption["implementation"] == manifest["implementation"] and
         c.document(SAVED/"completion/RESULT.json")["local_root"] == CONTEXT,
         "CONTEXT_INTEGRATION_EXISTING_OWNER")
    def helper(role, module, digest):
        logical = manifest["roles"][role]
        expected = manifest["files"][logical]
        need(logical.startswith("supervisor/") and expected["sha256"] == digest,
             "CONTEXT_INTEGRATION_SUPERVISOR_PIN")
        return h.load_exact(package/"installation"/h.relative(logical), module, expected, c.check)
    c.supervisor = helper("supervisor", "_context_query_supervisor",
        "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9")
    helper("domains", "domains", "651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a")
    c.jobs = helper("job", "_context_query_job",
        "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028")
    output.mkdir()
    c.output_created = True
    h.save(output/"SELECTION.json", {"package": str(package), "profile_sha256": args.profile_sha256,
        "assembly_sha256": args.assembly_sha256, "store_id": STORE, "context_root": CONTEXT,
        "original_allowance": vars(args), "calls_selected": 1,
        "scope": "EXISTING_OWNER_QUERY_REOPEN_MAY_SETTLE_RESERVED_NO_NATIVE_OR_ADMISSION"})


def run(c, h, args, report):
    c.check()
    grant = c.supervisor.limits_checked({"wall_seconds": min(45, math.floor(c.deadline-time.monotonic())-20),
        "cpu_seconds": min(15, math.floor(args.cpu_seconds-(time.process_time()-c.cpu_started))-5),
        "memory_mib": args.memory_mib, "active_processes": 1, "stdout_bytes": MIB, "stderr_bytes": MIB})
    need(grant["wall_seconds"] >= 40 and grant["cpu_seconds"] >= 5, "CONTEXT_INTEGRATION_REMAINING_GRANT")
    argv = [str(PYTHON), "-I", "-S", "-B", str(c.package/"query.py"),
        "--profile-sha256", args.profile_sha256, "--python-runtime", str(PYTHON.parent),
        "--lean-runtime", str(LEAN), "--wall-seconds", str(grant["wall_seconds"]-5),
        "--cpu-seconds", str(grant["cpu_seconds"]-1), "--memory-mib", str(args.memory_mib),
        "--context-root", CONTEXT, "--catalog", str(SAVED/"catalog"), "--custody", str(SAVED/"custody"),
        "--store-id", STORE, "--custody-limits", str(SAVED/"fixtures/custody-limits.json"),
        "--native-type", str(PUBLIC/"query-local/native-type.json"), "--output", str(c.output/"query")]
    event = {"label": "context-query", "argv": argv, "limits": grant, "cpu_complete": False,
             "charged_cpu_seconds": grant["cpu_seconds"]}
    c.calls.append(event)
    c.charged, c.complete = grant["cpu_seconds"], False
    report["phase"] = "PUBLIC_CONTEXT_QUERY"
    supervision = None
    try:
        supervision = c.supervisor.supervise(argv, c.output, c.output/"call", grant, c.jobs.Job)
        event["supervision"] = supervision
    except BaseException as error:
        event["supervision_exception"] = {"type": type(error).__name__, "error": str(error)[:2000]}
        raise
    finally:
        final = supervision.get("final_job") if type(supervision) is dict else None
        cpu = final.get("cpu_seconds") if type(final) is dict else None
        known = type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0
        c.charged, c.complete = (cpu if known else grant["cpu_seconds"]), known
        event.update(cpu_complete=known, charged_cpu_seconds=c.charged)
        h.save(c.output/"CALL-SUPERVISION.json", event)
    need(c.complete, "CONTEXT_INTEGRATION_UNKNOWN_CPU_FULL_GRANT_CHARGED")
    h.clean(supervision)
    need(supervision["final_job"]["total_processes"] == 1 and
         h.read(c.output/"call/stderr.txt", MIB) == b"", "CONTEXT_INTEGRATION_NO_CHILD_WORKERS")
    result = c.document(c.output/"call/stdout.txt", MIB)
    saved_raw = h.read(c.output/"query/RESULT.json", MIB)
    need(h.read(c.output/"call/stdout.txt", MIB) == saved_raw+b"\n" and
         result["ok"] is True and result["operation"] == "prepare-query" and not result.get("close_errors") and
         result["mathematical_acceptance"] is False and result["profile_sha256"] == args.profile_sha256 and
         result["binding_mode"] == "selected-local-context" and
         result["interpretation"] == "SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE" and
         result["context_selection"] == {"context_root": CONTEXT, "store_id": STORE,
             "semantic_id": SEMANTIC, "foundation_id": FOUNDATION, "implementation_id": IMPLEMENTATION,
             "reference_count": 4} and result["cost"]["worker_cpu_seconds"] == 0,
         "CONTEXT_INTEGRATION_CONTEXT_REPLY")
    for actual, prior in (("BINDINGS.json", "fixtures/known-bindings.json"),
                          ("QUERY.json", "query-prepared/QUERY.json"), ("SPECS.json", "query-prepared/SPECS.json")):
        need(h.read(c.output/"query"/actual, MIB) == h.read(PUBLIC/prior, MIB),
             "CONTEXT_INTEGRATION_SAVED_BYTE_AGREEMENT:"+actual)
    baseline = c.document(PUBLIC/"query-prepared/RESULT.json", MIB)
    for key in ("bindings_sha256", "native_type_sha256", "query_sha256", "features", "specs", "namespace", "key_profile"):
        need(result[key] == baseline[key], "CONTEXT_INTEGRATION_SAVED_FIELD_AGREEMENT:"+key)
    need(c.capture_tree(c.output/"query") == {"BINDINGS.json", "QUERY.json", "SPECS.json", "RESULT.json"},
         "CONTEXT_INTEGRATION_QUERY_CENSUS")
    # No second owner reopening. The result is published after both real closes;
    # the closed one-process Job also releases SQLite handles. Observe the sole
    # catalog owner lock directly; custody has no corresponding owner.lock file.
    lock_path = h.ordinary(SAVED/"catalog/owner.lock")
    need(h.read(lock_path, 1) == b"\0", "CONTEXT_INTEGRATION_LOCK_BYTES")
    with lock_path.open("r+b") as lock:
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            report["catalog_owner_lock_reacquired"] = True
        finally:
            lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
    report["phase"] = "FINAL_PRESERVATION"
    for path, expected in tuple(c.held.items()):
        c.hold(Path(path), expected)
    c.check()
    h.save(c.output/"IMMUTABLE-FILES.json", c.held)
    report.update(status="PASS_SELECTED_REAL_CONTEXT_QUERY_REUSE", phase="COMPLETE",
        immutable_files=len(c.held), prior_immutable_files=463, public_query_calls=1,
        native_calls=0, query_output_equal_to_saved_manual=True,
        owner_closure_observation="POST_FINALLY_SUCCESS_MARKER_CLOSED_SINGLE_PROCESS_JOB_AND_RELEASED_CATALOG_LOCK")


def main():
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON,
         "CONTEXT_INTEGRATION_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for field in ("package", "profile-sha256", "assembly-sha256", "output"):
        parser.add_argument("--"+field, required=True)
    for field in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+field, required=True, type=int)
    args = parser.parse_args()
    need(args.wall_seconds == 90 and args.cpu_seconds == 45 and args.memory_mib == 512,
         "CONTEXT_INTEGRATION_FINITE_ENVELOPE")
    h = helpers()
    # Reuse only pure pin/tree/budget utilities, never Smoke.prepare/run/command.
    c = h.Smoke(args)
    c.started, c.cpu_started, c.deadline = BOOT_WALL, BOOT_CPU, BOOT_WALL+args.wall_seconds
    c.output_created = False
    report = {"status": "FAILED", "phase": "PREFLIGHT", "calls": c.calls,
        "mathematical_acceptance": False, "claim": "SELECTED_CONTEXT_QUERY_USABILITY_NOT_SEARCH_RECALL_GROWTH_OR_FINAL_V5",
        "retention": "ALL_PRIOR_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY",
        "state_scope": "EXISTING_OWNER_REOPEN_MAY_SETTLE_RESERVED_OPERATIONS_NOT_DATABASE_READ_ONLY"}
    try:
        prepare(c, h, args); run(c, h, args, report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000],
            immutable_preservation="POST_FAILURE_SAVED_FILE_AUDIT_REQUIRED_NO_RENEWED_ALLOWANCE")
    finally:
        report.update(wall_seconds=time.monotonic()-c.started,
            controller_cpu_seconds=time.process_time()-c.cpu_started,
            inclusive_child_job_cpu_charged=c.charged, child_cpu_complete=c.complete,
            accounting="CHILD_JOB_CPU_ONCE_UNKNOWN_FULL_GRANT_THEN_STOP_OUTER_JOB_AUTHORITATIVE")
        if not c.complete or report["wall_seconds"] >= args.wall_seconds or (
                report["controller_cpu_seconds"]+c.charged >= args.cpu_seconds):
            report.update(status="FAILED", budget_or_cleanup_error="CONTEXT_INTEGRATION_ORIGINAL_ALLOWANCE_OR_CLOSURE")
        if c.output_created:
            h.save(c.output/"INTEGRATION-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_SELECTED_REAL_CONTEXT_QUERY_REUSE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
