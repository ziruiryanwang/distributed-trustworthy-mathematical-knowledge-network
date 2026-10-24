"""Saved mixed-theorem native discriminator, not public-facade qualification.

SOURCE ONLY until root selects one finite enclosing Job. Reuse the exact saved
request and fixed inventory, no owner open/init/admission/extraction or rebuild.
Three worker operations and one ordinary consumer share one original allowance.
Two negative requests are adversarial native-boundary controls, not warrants.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
SAVED = LOCAL/"ordinary-module-native-03/collision-refusal"
REQUEST_SHA = "0070f06dc523bf03194c7a5a4b015d9e908e5ccb26ae6a68078cf429ec188032"
INVENTORY_SHA = "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
SOURCE_PINS = {
    "OrdinaryModule.lean": {"bytes": 27346, "sha256":
        "62269b34626ead7cd33fd2a492da66a34a1f1ca3cae7bc3e1f3d984d904ea525"},
    "module_worker.py": {"bytes": 8370, "sha256":
        "3872864a27e9fbb12e56eaa2ebabd9299d97a336c5e58840648a86b5c371df18"},
}
MIB = 1024**2
PARTS = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")


def need(ok, code):
    if not ok:
        raise ValueError(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def diagnostic_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "MATCHING_CHECK_DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def number(text):
        value = float(text)
        need(math.isfinite(value), "MATCHING_CHECK_NONFINITE_JSON_NUMBER")
        return value
    def reject(_):
        raise ValueError("MATCHING_CHECK_JSON_CONSTANT")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=reject)


def relative(value):
    need(type(value) is str and value and "\\" not in value, "MATCHING_CHECK_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(path.as_posix() == value and not path.is_absolute() and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts), "MATCHING_CHECK_RELATIVE_PATH")
    return path


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and path != Path(path.anchor) and len(path.drive) == 2 and
         path.drive[1] == ":" and len(str(path)) <= 32768 and ".." not in path.parts,
         "MATCHING_CHECK_ABSOLUTE_LOCAL_PATH")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "MATCHING_CHECK_MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "MATCHING_CHECK_REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "MATCHING_CHECK_PATH_KIND")
    need(not fresh, "MATCHING_CHECK_FRESH_REQUIRED")
    return path


def read(path, maximum=4*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "MATCHING_CHECK_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "MATCHING_CHECK_READ_CHANGED")
    return raw


def save(path, value):
    ordinary(path.parent, directory=True); ordinary(path, fresh=True)
    raw = value if type(value) is bytes else canonical(value)
    need(len(raw) <= 16*MIB, "MATCHING_CHECK_SAVE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return {"bytes": len(raw), "sha256": sha(raw)}


def pin(path, check, maximum=128*MIB):
    check(); path = ordinary(path)
    size, total, digest = path.stat().st_size, 0, hashlib.sha256()
    need(0 <= size <= maximum, "MATCHING_CHECK_PIN_BOUND")
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); total += len(block); digest.update(block)
            need(total <= size, "MATCHING_CHECK_PIN_GREW")
    need(total == size and path.stat().st_size == size, "MATCHING_CHECK_PIN_SIZE_CHANGED")
    return {"bytes": size, "sha256": digest.hexdigest()}


def clean(record, *, exit_code=0):
    final = record.get("final_job")
    expected_status = "COMMAND_EXITED_ZERO_AND_CLOSED" if exit_code == 0 else "COMMAND_FAILED"
    need(record.get("status") == expected_status and record.get("child_exit_code") == exit_code and
         record.get("direct_child_reaped") is True and record.get("job_closed") is True and
         record.get("cleanup_errors") == [] and record.get("termination_requested") is False and
         type(final) is dict and final.get("active_processes") == 0 and
         final.get("terminated_processes") == 0 and type(final.get("total_processes")) is int and
         final["total_processes"] >= 1, "MATCHING_CHECK_UNCLEAN_PROCESS_TREE")
    cpu = final.get("cpu_seconds")
    need(type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0, "MATCHING_CHECK_UNKNOWN_CPU")
    limits, logs = record.get("limits"), record.get("observed_logs")
    need(type(limits) is dict and type(logs) is dict, "MATCHING_CHECK_FINAL_RESOURCE_RECORD")
    for key, value in (("cpu_seconds", cpu),
                       ("wall_seconds", record.get("wall_seconds_through_cleanup"))):
        cap = limits.get(key)
        need(type(value) in (int, float) and math.isfinite(value) and value >= 0 and
             type(cap) in (int, float) and math.isfinite(cap) and 0 < cap and value <= cap,
             "MATCHING_CHECK_FINAL_RESOURCE_LIMIT:"+key)
    for key in ("stdout_bytes", "stderr_bytes"):
        value, cap = logs.get(key), limits.get(key)
        need(type(value) is int and type(cap) is int and 0 <= value <= cap,
             "MATCHING_CHECK_FINAL_LOG_LIMIT:"+key)
    return cpu


def load_exact(path, module_name, expected, check):
    need(pin(path, check, 2*MIB) == expected and module_name not in sys.modules, "MATCHING_CHECK_HELPER_PIN")
    raw = read(path, 2*MIB)
    need(sha(raw) == expected["sha256"], "MATCHING_CHECK_HELPER_CHANGED")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def consumer_source(module):
    need(re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", module), "MATCHING_CHECK_MODULE_NAME")
    return ("module\n\npublic import Init\npublic import "+module+"\n\npublic section\n\n"
        "theorem MatchingConsumer.useNew (n : Nat) : Nat.add n Nat.zero = n :=\n"
        "  CommonsLibraryExample.add_zero n\n").encode("ascii")


def consumer_child(arguments):
    need(len(arguments) == 3 and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "MATCHING_CHECK_CONSUMER_PROFILE")
    runtime, modules, source = map(Path, arguments)
    ordinary(runtime, directory=True); ordinary(modules, directory=True); ordinary(source)
    lean, output = ordinary(runtime/"bin/lean.exe"), source.with_suffix(".olean")
    need(source.name == "Consumer.lean", "MATCHING_CHECK_CONSUMER_NAME"); ordinary(output, fresh=True)
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join((str(runtime/"lib/lean"), str(modules)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    return subprocess.call([str(lean), "-DElab.async=false", "-R", str(source.parent),
        "-o", str(output), str(source)], cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW)


class Check:
    def __init__(self, args):
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.args, self.charged, self.cpu_complete = args, 0.0, True
        self.deadline = self.started+args.wall_seconds
        self.held, self.calls = {}, []
        self.output_created = False
        self.report = {"status": "FAILED", "phase": "INPUTS", "calls": self.calls,
            "new_catalog_acceptance": False,
            "claim": "DIRECT_NATIVE_MATCHING_AND_CONSUMER_NOT_PUBLIC_CONTROLLER_OR_PACKAGE_QUALIFICATION"}

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.charged < self.args.cpu_seconds,
             "MATCHING_CHECK_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None, maximum=128*MIB):
        actual = pin(path, self.check, maximum)
        need(expected is None or actual == expected, "MATCHING_CHECK_PIN:"+str(path))
        need(self.held.setdefault(str(path), actual) == actual, "MATCHING_CHECK_IMMUTABLE_CHANGED")
        return actual

    def tree(self, root):
        found, todo, entries = set(), [ordinary(root, directory=True)], 0
        while todo:
            with os.scandir(todo.pop()) as listing:
                for entry in listing:
                    self.check(); entries += 1
                    need(entries <= 1024, "MATCHING_CHECK_TREE_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        need(len(path.relative_to(root).parts) <= 8, "MATCHING_CHECK_TREE_DEPTH")
                        todo.append(ordinary(path, directory=True))
                    else:
                        ordinary(path); found.add(path.relative_to(root).as_posix())
        return found

    def prepare(self):
        self.package = ordinary(self.args.package, directory=True)
        self.output = ordinary(self.args.output, directory=True, fresh=True)
        self.script = ordinary(Path(__file__).resolve())
        roots = [self.package, self.output, PYTHON, LEAN, SAVED]
        need(self.output.is_relative_to(LOCAL) and self.package.is_relative_to(LOCAL) and
             all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "MATCHING_CHECK_DISJOINT")
        need(Path(sys.executable).resolve() == PYTHON/"python.exe" and
             self.script.name == "native_check.py", "MATCHING_CHECK_RUNNING_SOURCE")
        self.hold(self.script, maximum=2*MIB)
        for filename, expected in SOURCE_PINS.items():
            self.hold(self.script.parent/filename, expected, 2*MIB)
        raw = read(self.package/"PROFILE.json", 2*MIB)
        need(re.fullmatch(r"[0-9a-f]{64}", self.args.profile_sha256) and
             sha(raw) == self.args.profile_sha256, "MATCHING_CHECK_PROFILE_PIN")
        profile = diagnostic_json(raw)
        need(set(profile) == {"schema", "files", "installation_manifest_sha256", "helper_paths", "author_worker"}
             and profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             profile["helper_paths"] == ["authoring/helpers"] and profile["author_worker"] == "author_worker.py"
             and len(profile["files"]) == 98, "MATCHING_CHECK_CURRENT_PROFILE")
        manifest_raw = read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(sha(manifest_raw) == profile["installation_manifest_sha256"], "MATCHING_CHECK_MANIFEST_PIN")
        manifest = diagnostic_json(manifest_raw)
        need(manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1", "MATCHING_CHECK_MANIFEST_SCHEMA")
        self.payload = dict(profile["files"])
        runtimes = {"python_runtime": PYTHON, "lean_runtime": LEAN}
        for logical, expected in manifest["files"].items():
            parts = relative(logical).parts
            if parts[0] in runtimes:
                self.hold(runtimes[parts[0]].joinpath(*parts[1:]), expected)
            else:
                self.payload["installation/"+logical] = expected
        self.payload["PROFILE.json"] = {"bytes": len(raw), "sha256": sha(raw)}
        self.payload["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": sha(manifest_raw)}
        need(len(self.payload) == 127 and len({p.casefold() for p in self.payload}) == 127 and
             sum(p["bytes"] for p in self.payload.values()) <= 768*MIB, "MATCHING_CHECK_PAYLOAD_CENSUS")
        for logical, expected in self.payload.items():
            self.hold(self.package/relative(logical), expected)
        need(self.tree(self.package) == set(self.payload), "MATCHING_CHECK_PACKAGE_TREE")
        self.request_raw = read(SAVED/"request.json")
        self.inventory_raw = read(SAVED/"inventory.json", MIB)
        need(sha(self.request_raw) == REQUEST_SHA and sha(self.inventory_raw) == INVENTORY_SHA and
             self.inventory_raw == read(self.package/"installation/foundation/inventory.json", MIB),
             "MATCHING_CHECK_SAVED_INPUTS")
        self.hold(SAVED/"request.json"); self.hold(SAVED/"inventory.json")
        self.request = diagnostic_json(self.request_raw)
        need(canonical(self.request) == self.request_raw and len(self.request["units"]) == 2 and
             len(self.request["unit_ids"]) == 2 and self.request["targets"] == [name("CommonsLibraryExample.add_zero")] and
             self.request["units"][0][1][1] == name("Nat.add_zero") and
             self.request["units"][1][1][1] == name("CommonsLibraryExample.add_zero"),
             "MATCHING_CHECK_EXACT_MIXED_FIXTURE")
        self.module = bytes(self.request["module_name"][0][1]["$bytes"]).decode("ascii")
        need(self.request["module_name"] == name(self.module) and
             re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", self.module), "MATCHING_CHECK_FIXED_MODULE")
        def helper(role, module_name):
            logical = manifest["roles"][role]
            need(logical.startswith("supervisor/"), "MATCHING_CHECK_SUPERVISOR_ROLE")
            return load_exact(self.package/"installation"/relative(logical), module_name,
                              manifest["files"][logical], self.check)
        self.supervisor = helper("supervisor", "_matching_check_supervisor")
        helper("domains", "domains")
        self.jobs = helper("job", "_matching_check_job")
        self.output.mkdir()
        self.output_created = True
        self.hold(self.output/"inventory.json", save(self.output/"inventory.json", self.inventory_raw))
        save(self.output/"INPUTS.json", {"pins": self.held, "profile_sha256": self.args.profile_sha256,
            "request_sha256": REQUEST_SHA, "identity_scope": "SAVED_LABELS_NO_NEW_CONTROLLER_WARRANT",
            "original_allowance": {"wall_seconds": self.args.wall_seconds,
                "cpu_seconds": self.args.cpu_seconds, "memory_mib": self.args.memory_mib}})

    def command(self, label, directory, argv, exit_code=0, stderr=b""):
        self.check()
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(100, math.floor(self.deadline-time.monotonic())-25),
            "cpu_seconds": min(42, math.floor(self.args.cpu_seconds-self.charged-
                (time.process_time()-self.cpu_started))-62),
            "memory_mib": self.args.memory_mib, "active_processes": 4,
            "stdout_bytes": MIB, "stderr_bytes": MIB})
        need(grant["wall_seconds"] >= 30 and grant["cpu_seconds"] >= 2,
             "MATCHING_CHECK_REMAINING_GRANT")
        event = {"label": label, "argv": argv, "limits": grant,
                 "charged_cpu_seconds": grant["cpu_seconds"], "cpu_complete": False}
        self.calls.append(event); self.charged += grant["cpu_seconds"]; self.cpu_complete = False
        supervision = self.supervisor.supervise(argv, directory, directory/"supervision", grant, self.jobs.Job)
        event["supervision"] = supervision
        final = supervision.get("final_job")
        cpu = final.get("cpu_seconds") if type(final) is dict else None
        known = type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0
        if known:
            self.charged += cpu-grant["cpu_seconds"]; self.cpu_complete = True
            event.update(charged_cpu_seconds=cpu, cpu_complete=True)
        save(directory/"SUPERVISION.json", event)
        need(known, "MATCHING_CHECK_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        clean(supervision, exit_code=exit_code)
        need(read(directory/"supervision/stdout.txt", MIB) == b"" and
             read(directory/"supervision/stderr.txt", MIB).splitlines() == stderr.splitlines(),
             "MATCHING_CHECK_EXACT_DIAGNOSTIC:"+label)
        self.check()
        return event

    def worker(self, label, raw, diagnostic=None):
        directory = self.output/label
        directory.mkdir(); (directory/"modules").mkdir()
        self.hold(directory/"request.json", save(directory/"request.json", raw))
        report_path = directory/"native-report.json"
        artifact = directory/"modules"/(self.module+".olean")
        argv = [str(PYTHON/"python.exe"), "-I", "-S", "-B", str(self.script.parent/"module_worker.py"),
            str(LEAN/"bin/lean.exe"), str(self.script.parent/"OrdinaryModule.lean"),
            str(self.package/"authoring/helpers"), str(LEAN), str(self.output/"inventory.json"),
            str(directory/"request.json"), str(artifact), str(report_path)]
        event = self.command(label, directory, argv, 1 if diagnostic else 0, diagnostic or b"")
        trace_path = report_path.with_name(report_path.name+".phases.jsonl")
        trace = [diagnostic_json(line) for line in read(trace_path, 65536).splitlines()]
        phases = ("build",) if diagnostic else ("build", "reread-private", "reread-exported")
        expected_trace = [{"schema": "DMKN_ORDINARY_MODULE_PHASE_TRACE_V1", "phase": phase,
            "event": state, "exit_code": None if state == "STARTED" else 1 if diagnostic else 0}
            for phase in phases for state in ("STARTED", "EXITED")]
        need(trace == expected_trace, "MATCHING_CHECK_PHASE_ORDER")
        self.hold(trace_path)
        if diagnostic:
            need(not self.tree(directory/"modules") and not os.path.lexists(report_path) and
                 not os.path.lexists(str(report_path)+".pending") and
                 not os.path.lexists(directory/"MODULE.json"), "MATCHING_CHECK_REFUSAL_BEFORE_WRITING")
            event["native_boundary_refusal"] = diagnostic.decode("ascii")
            event["input_authority"] = "ADVERSARIAL_NATIVE_BOUNDARY_CONTROL_NOT_WARRANTED_EVIDENCE"
            return
        native = diagnostic_json(read(report_path, 8*MIB))
        event["native_result"] = native  # Preserve actual success before assertions.
        request = diagnostic_json(raw)
        rows = [row for unit in request["units"] for row in unit[2]]
        paths = [directory/"modules"/(self.module+suffix) for suffix in PARTS]
        parts, total = [], 0
        for path in paths:
            expected = self.hold(path, maximum=64*MIB)
            need(expected["bytes"] > 0, "MATCHING_CHECK_EMPTY_MODULE_PART")
            total += expected["bytes"]; parts.append({"path": str(path), "bytes": expected["bytes"]})
        need(total <= 64*MIB and self.tree(directory/"modules") == {p.name for p in paths},
             "MATCHING_CHECK_MODULE_CENSUS")
        expected = {field: request[field] for field in
            ("semantic_id", "context_root", "foundation_id", "module_name", "targets", "unit_ids")}
        expected.update(schema="DMKN_ORDINARY_MODULE_OUTPUT_V2",
            assurance="LOCAL_CHECKED_MODULE_WITH_MATCHES_CONTROLLER_BOUND_IDENTITIES",
            names=[row[0] for row in rows], inventories=rows,
            matched_unit_indices=[0], matched_names=[name("Nat.add_zero")],
            matched_inventories=request["units"][0][2],
            added_names=[name("CommonsLibraryExample.add_zero")],
            added_inventories=request["units"][1][2], units_checked=1, units_matched=1,
            checking_passes=2, basis_rows=581, artifact_parts=parts)
        need(native == expected, "MATCHING_CHECK_EXACT_MATCHED_ADDED_REPORT")
        pending = diagnostic_json(read(Path(str(report_path)+".pending"), 8*MIB))
        need(pending == dict(expected, schema="DMKN_ORDINARY_MODULE_PENDING_V2",
            assurance="LOCAL_CHECKED_MODULE_WITH_MATCHES_PENDING_REREADS"), "MATCHING_CHECK_PENDING_REPORT")
        self.hold(report_path); self.hold(Path(str(report_path)+".pending"))
        self.report["mixed_result"] = {"module": self.module, "units_matched": 1, "units_checked": 1,
            "checking_passes": 2, "fresh_rereads": ["private", "exported"],
            "artifact_pins": {path.name: self.held[str(path)] for path in paths}}

    def consumer(self):
        directory = self.output/"normal-consumer"
        directory.mkdir()
        source = directory/"Consumer.lean"
        self.hold(source, save(source, consumer_source(self.module)))
        self.command("normal-consumer", directory, [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            str(self.script), "--consumer-child", str(LEAN), str(self.output/"mixed/modules"), str(source)])
        parts = {}
        for suffix in PARTS:
            path = directory/("Consumer"+suffix)
            if os.path.lexists(path):
                parts[path.name] = self.hold(path, maximum=16*MIB)
                need(parts[path.name]["bytes"] > 0, "MATCHING_CHECK_EMPTY_CONSUMER_PART")
        need({"Consumer.olean", "Consumer.olean.private", "Consumer.olean.server"} <= set(parts),
             "MATCHING_CHECK_CONSUMER_PARTS")
        self.report["ordinary_consumer"] = {"parts": parts, "uses_new_theorem": True,
            "search_path": "ONLY_PINNED_RUNTIME_AND_NEW_MODULE_DIRECTORY"}

    def run(self):
        self.prepare()
        self.report["phase"] = "MIXED_NATIVE"
        self.worker("mixed", self.request_raw)
        self.report["phase"] = "NORMAL_CONSUMER"
        self.consumer()
        self.report["phase"] = "PROOF_IDENTITY_REFUSAL"
        changed = deepcopy(self.request)
        proof = changed["units"][0][1][4]
        need(proof[3] == 23 and len(proof[2]) == 24 and
             proof[2][-1] == [4, name("n"), 0, 0, 22], "MATCHING_CHECK_FIXED_PROOF_BINDER")
        # Alpha-renaming is a valid same-statement proof change, but not the
        # exact installed inventory. Update BOTH copies; do not test malformed
        # descriptor/inventory disagreement. Labels are not new warrants.
        proof[2][-1][1] = name("native_control_n")
        changed["units"][0][2][0][4][0] = deepcopy(proof)
        self.worker("proof-mismatch", canonical(changed),
                    b"ORDINARY_MODULE VISIBLE_INVENTORY_MISMATCH name=Nat.add_zero")
        self.report["phase"] = "ALL_MATCHED_REFUSAL"
        changed = deepcopy(self.request)
        changed.update(units=changed["units"][:1], unit_ids=changed["unit_ids"][:1],
                       targets=[name("Nat.add_zero")])
        self.worker("all-matched", canonical(changed), b"ORDINARY_MODULE NO_NEW_MODULE_DECLARATIONS")
        self.report["phase"] = "FINAL_VERIFY"
        for path, expected in self.held.items():
            need(pin(Path(path), self.check) == expected, "MATCHING_CHECK_FINAL_PIN")
        need(self.tree(self.package) == set(self.payload), "MATCHING_CHECK_FINAL_PACKAGE_TREE")
        need(len(self.calls) == 4 and self.cpu_complete, "MATCHING_CHECK_EXACT_CALL_COUNT")
        self.check()
        self.report.update(status="PASS_DIRECT_MIXED_THEOREM_NATIVE_AND_CONSUMER", phase="COMPLETE",
                           final_pins_unchanged=True)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "MATCHING_CHECK_PYTHON")
    if sys.argv[1:2] == ["--consumer-child"]:
        return consumer_child(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "output"):
        parser.add_argument("--"+name, required=True)
    for name in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+name, type=int, required=True)
    args = parser.parse_args()
    need(120 <= args.wall_seconds <= 600 and 100 <= args.cpu_seconds <= 600 and
         256 <= args.memory_mib <= 2048, "MATCHING_CHECK_FINITE_ALLOWANCE")
    run = Check(args)
    try:
        run.run()
    except BaseException as error:
        run.report.update(error_type=type(error).__name__, error=str(error)[:2000])
    run.report.update(wall_seconds=time.monotonic()-run.started,
        controller_cpu_seconds=time.process_time()-run.cpu_started,
        charged_inclusive_child_cpu_seconds=run.charged, cpu_complete=run.cpu_complete,
        retention="ALL_PARTIAL_OUTPUTS_RETAINED_NO_RETRY",
        cost_scope="EACH_COMPLETE_CHILD_JOB_ONCE_OUTER_JOB_AGGREGATE_AUTHORITATIVE")
    try:
        run.check()
    except BaseException:
        run.report.update(status="FAILED", budget_error="MATCHING_CHECK_ORIGINAL_ALLOWANCE")
    if run.output_created:
        save(run.output/"NATIVE-MATCHING-RESULT.json", run.report)
    print(json.dumps({"status": run.report["status"], "phase": run.report["phase"]}), flush=True)
    return 0 if run.report["status"] == "PASS_DIRECT_MIXED_THEOREM_NATIVE_AND_CONSUMER" else 1


if __name__ == "__main__":
    raise SystemExit(main())
