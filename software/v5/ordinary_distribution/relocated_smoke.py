"""One fresh-owner relocated smoke: six public calls and one normal consumer.

Source-only until selected. Requires an outer Job for the entire process tree.
No old owner, source checkout, package rebuild, network, certificate or retry.
Only pinned supervision helpers are imported from the relocated installation.
"""
from __future__ import annotations

import argparse
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

MIB = 1024**2
PARTS = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
MODULE_BODY = b"""namespace CommonsPackageExample

@[expose]
def applyTwice {a : Type u} (f : a -> a) (x : a) : a := f (f x)

theorem applyTwice_eq {a : Type u} (f : a -> a) (x : a) :
    applyTwice f x = f (f x) := rfl

end CommonsPackageExample
"""
LIBRARY_BODY = b"""theorem CommonsLibraryExample.add_zero (n : Nat) :
    Nat.add n Nat.zero = n := Nat.add_zero n
"""


def need(ok, code):
    if not ok:
        raise ValueError(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(domain, raw):
    return sha(domain.encode("ascii")+b"\0"+raw)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def diagnostic_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, "SMOKE_DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def number(text):
        value = float(text)
        need(math.isfinite(value), "SMOKE_NONFINITE_JSON_NUMBER")
        return value
    def reject(_):
        raise ValueError("SMOKE_JSON_CONSTANT")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=reject)


def relative(value):
    need(type(value) is str and value and "\\" not in value, "SMOKE_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(path.as_posix() == value and not path.is_absolute() and
         all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts), "SMOKE_RELATIVE_PATH")
    return path


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and path != Path(path.anchor) and len(path.drive) == 2 and
         path.drive[1] == ":" and len(str(path)) <= 32768 and ".." not in path.parts,
         "SMOKE_ABSOLUTE_LOCAL_PATH")
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            need(item == path and fresh, "SMOKE_MISSING_PATH")
            return path
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "SMOKE_REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if item != path or directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "SMOKE_PATH_KIND")
    need(not fresh, "SMOKE_FRESH_REQUIRED")
    return path


def read(path, maximum=4*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "SMOKE_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "SMOKE_READ_CHANGED")
    return raw


def save(path, value):
    ordinary(path.parent, directory=True); ordinary(path, fresh=True)
    raw = value if type(value) is bytes else canonical(value)
    need(len(raw) <= 16*MIB, "SMOKE_SAVE_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return {"bytes": len(raw), "sha256": sha(raw)}


def pin(path, check, maximum=128*MIB):
    check(); path = ordinary(path)
    size, total, digest = path.stat().st_size, 0, hashlib.sha256()
    need(0 <= size <= maximum, "SMOKE_PIN_BOUND")
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            check(); total += len(block); digest.update(block)
            need(total <= size, "SMOKE_PIN_GREW")
    need(total == size and path.stat().st_size == size, "SMOKE_PIN_SIZE_CHANGED")
    return {"bytes": size, "sha256": digest.hexdigest()}


def clean(record, *, exit_code=0, extraction=False):
    final = record.get("final_job")
    expected_status = ("EXTRACTED_AND_CLOSED" if extraction else
                       "COMMAND_EXITED_ZERO_AND_CLOSED" if exit_code == 0 else "COMMAND_FAILED")
    need(record.get("status") == expected_status and record.get("child_exit_code") == exit_code and
         record.get("direct_child_reaped") is True and record.get("job_closed") is True and
         record.get("cleanup_errors") == [] and record.get("termination_requested") is False and
         type(final) is dict and final.get("active_processes") == 0 and
         final.get("terminated_processes") == 0 and type(final.get("total_processes")) is int and
         final["total_processes"] >= 1, "SMOKE_UNCLEAN_PROCESS_TREE")
    cpu = final.get("cpu_seconds")
    need(type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0, "SMOKE_UNKNOWN_CPU")
    if extraction:
        need(record.get("threads_joined") is True and record.get("accounting_complete") is True and
             record.get("job_attach_resume_completed") is True and record.get("native_cpu_seconds") == cpu,
             "SMOKE_EXTRACTION_CLOSURE")
    else:
        limits, logs = record.get("limits"), record.get("observed_logs")
        need(type(limits) is dict and type(logs) is dict, "SMOKE_FINAL_RESOURCE_RECORD")
        for key, value in (("cpu_seconds", cpu),
                           ("wall_seconds", record.get("wall_seconds_through_cleanup"))):
            cap = limits.get(key)
            need(type(value) in (int, float) and math.isfinite(value) and value >= 0 and
                 type(cap) in (int, float) and math.isfinite(cap) and 0 < cap and value <= cap,
                 "SMOKE_FINAL_RESOURCE_LIMIT:"+key)
        for key in ("stdout_bytes", "stderr_bytes"):
            value, cap = logs.get(key), limits.get(key)
            need(type(value) is int and type(cap) is int and 0 <= value <= cap,
                 "SMOKE_FINAL_LOG_LIMIT:"+key)
    return cpu


def load_exact(path, module_name, expected, check):
    need(pin(path, check, 2*MIB) == expected and module_name not in sys.modules, "SMOKE_HELPER_PIN")
    raw = read(path, 2*MIB)
    need(sha(raw) == expected["sha256"], "SMOKE_HELPER_CHANGED")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def consumer_source(module):
    need(type(module) is str and re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", module), "SMOKE_MODULE_NAME")
    return ("module\n\npublic import Init\npublic import "+module+"\n\npublic section\n\n"
        "universe u\n\n"
        "theorem DistributionConsumer.byTheorem {a : Type u} (f : a -> a) (x : a) :\n"
        "    CommonsPackageExample.applyTwice f x = f (f x) :=\n"
        "  @CommonsPackageExample.applyTwice_eq a f x\n\n"
        "theorem DistributionConsumer.byReduction {a : Type u} (f : a -> a) (x : a) :\n"
        "    CommonsPackageExample.applyTwice f x = f (f x) := rfl\n").encode("ascii")


def consumer_worker(arguments):
    need(len(arguments) == 3 and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SMOKE_CONSUMER_PROFILE")
    runtime, modules, source = map(Path, arguments)
    ordinary(runtime, directory=True); ordinary(modules, directory=True); ordinary(source)
    lean, output = ordinary(runtime/"bin/lean.exe"), source.with_suffix(".olean")
    need(source.name == "Consumer.lean", "SMOKE_CONSUMER_NAME"); ordinary(output, fresh=True)
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join((str(runtime/"lib/lean"), str(modules)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    return subprocess.call([str(lean), "-DElab.async=false", "-R", str(source.parent),
        "-o", str(output), str(source)], cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW)


class Smoke:
    def __init__(self, args):
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.args, self.charged, self.complete = args, 0.0, True
        self.calls, self.held = [], {}
        self.deadline = self.started+args.wall_seconds

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.charged < self.args.cpu_seconds,
             "SMOKE_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None, maximum=128*MIB):
        actual = pin(path, self.check, maximum)
        need(expected is None or actual == expected, "SMOKE_EXACT_PIN:"+str(path))
        previous = self.held.setdefault(str(path), actual)
        need(previous == actual, "SMOKE_IMMUTABLE_OUTPUT_CHANGED")
        return actual

    def document(self, path, maximum=4*MIB):
        self.check()
        return diagnostic_json(read(path, maximum))

    def capture_tree(self, root):
        files, pending, entries = set(), [ordinary(root, directory=True)], 0
        while pending:
            folder = pending.pop()
            with os.scandir(folder) as listing:
                for entry in listing:
                    self.check(); entries += 1
                    need(entries <= 1024, "SMOKE_TREE_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        need(len(path.relative_to(root).parts) <= 8, "SMOKE_TREE_DEPTH")
                        pending.append(ordinary(path, directory=True))
                    else:
                        self.hold(path); files.add(path.relative_to(root).as_posix())
        return files

    def prepare(self):
        args = self.args
        self.package = ordinary(args.package, directory=True)
        self.output = ordinary(args.output, directory=True, fresh=True)
        self.runtimes = {"python_runtime": ordinary(args.python_runtime, directory=True),
                         "lean_runtime": ordinary(args.lean_runtime, directory=True)}
        roots = [self.package, self.output, *self.runtimes.values()]
        need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "SMOKE_DISJOINT_ROOTS")
        need(Path(sys.executable).resolve() == self.runtimes["python_runtime"]/"python.exe",
             "SMOKE_RUNNING_PYTHON")
        self.script = ordinary(Path(__file__).resolve()); self.hold(self.script, maximum=2*MIB)
        need(re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256), "SMOKE_PROFILE_HASH")
        profile_raw = read(self.package/"PROFILE.json", 2*MIB)
        need(sha(profile_raw) == args.profile_sha256, "SMOKE_PROFILE_PIN")
        self.profile = diagnostic_json(profile_raw)
        need(set(self.profile) == {"schema", "files", "installation_manifest_sha256", "helper_paths", "author_worker"}
             and self.profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             self.profile["helper_paths"] == ["authoring/helpers"] and
             self.profile["author_worker"] == "author_worker.py" and len(self.profile["files"]) == 98,
             "SMOKE_CURRENT_PROFILE")
        manifest_raw = read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(sha(manifest_raw) == self.profile["installation_manifest_sha256"], "SMOKE_INSTALLATION_PIN")
        self.manifest = diagnostic_json(manifest_raw)
        need(self.manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1", "SMOKE_INSTALLATION_SCHEMA")
        self.semantic = self.manifest["implementation"]["semantic_id"]
        self.implementation = identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1",
                                       canonical(self.manifest["implementation"]))
        self.package_pins = dict(self.profile["files"])
        for logical, expected in self.manifest["files"].items():
            parts = relative(logical).parts
            if parts[0] in self.runtimes:
                self.hold(self.runtimes[parts[0]].joinpath(*parts[1:]), expected)
            else:
                self.package_pins["installation/"+logical] = expected
        self.package_pins["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": sha(manifest_raw)}
        self.package_pins["PROFILE.json"] = {"bytes": len(profile_raw), "sha256": sha(profile_raw)}
        need(len(self.package_pins) == 127 and len({p.casefold() for p in self.package_pins}) == 127,
             "SMOKE_PACKAGE_CENSUS")
        for logical, expected in self.package_pins.items():
            self.hold(self.package/relative(logical), expected)
        need(self.capture_tree(self.package) == set(self.package_pins), "SMOKE_EXACT_RELOCATED_TREE")
        for suffix in PARTS:
            self.hold(self.runtimes["lean_runtime"]/("lib/lean/Std/Data/Internal/List/Defs"+suffix))
        roles = self.manifest["roles"]
        def helper(role, module):
            logical = roles[role]
            need(logical.startswith("supervisor/"), "SMOKE_SUPERVISOR_LOCATION")
            return load_exact(self.package/"installation"/relative(logical), module,
                              self.manifest["files"][logical], self.check)
        self.supervisor = helper("supervisor", "_relocated_smoke_supervisor")
        helper("domains", "domains")
        self.jobs = helper("job", "_relocated_smoke_job")
        self.output.mkdir()
        self.catalog, self.custody = self.output/"catalog", self.output/"custody"
        self.store = sha(b"ordinary-current-relocated-smoke\0"+str(self.output).encode("utf-8"))
        self.fixtures = self.output/"fixtures"; self.fixtures.mkdir()
        save(self.output/"RELOCATION.json", {"files": self.package_pins, "profile_sha256": self.args.profile_sha256,
             "installation_manifest_sha256": self.profile["installation_manifest_sha256"],
             "implementation_id": self.implementation, "semantic_id": self.semantic})
        self.fixture("custody-limits.json", {"objects": 512, "exports": 4096,
                                            "logical_bytes": 128*MIB, "db_pages": 16384})
        self.fixture("module-body.lean", MODULE_BODY); self.fixture("library-body.lean", LIBRARY_BODY)
        self.fixture("acquired.json", [])
        self.fixture("module-outputs.json", [name("CommonsPackageExample.applyTwice"), name("CommonsPackageExample.applyTwice_eq")])
        self.fixture("library-outputs.json", [name("CommonsLibraryExample.add_zero")])
        self.fixture("library-modules.json", [name("Std.Data.Internal.List.Defs")])

    def fixture(self, filename, value):
        path = self.fixtures/filename
        self.hold(path, save(path, value)); return path

    def command(self, label, argv_for_grant, *, initial=False, expected_exit=0):
        self.check()
        wall_cap, cpu_cap = (145, 92) if initial else (100, 42)
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall_cap, math.floor(self.deadline-time.monotonic())-25),
            "cpu_seconds": min(cpu_cap, math.floor(self.args.cpu_seconds-self.charged-
                (time.process_time()-self.cpu_started))-62),
            "memory_mib": self.args.memory_mib, "active_processes": 8,
            "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB})
        need(grant["wall_seconds"] >= 60 and grant["cpu_seconds"] >= 6, "SMOKE_REMAINING_CHILD_GRANT")
        argv = argv_for_grant(grant["wall_seconds"]-25, grant["cpu_seconds"]-2)
        event = {"label": label, "argv": argv, "limits": grant, "public_result": None,
                 "charged_cpu_seconds": grant["cpu_seconds"], "cpu_complete": False}
        self.calls.append(event)
        self.charged += grant["cpu_seconds"]; self.complete = False
        report = self.supervisor.supervise(argv, self.output, self.output/label, grant, self.jobs.Job)
        final = report.get("final_job")
        observed = final.get("cpu_seconds") if type(final) is dict else None
        known = type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
        if known:
            self.charged += observed-grant["cpu_seconds"]; self.complete = True
            event.update(charged_cpu_seconds=observed, cpu_complete=True)
        event["supervision"] = report
        save(self.output/(label+"-SUPERVISION.json"), event)
        # Preserve the actual reply before asserting success or expected refusal.
        raw = read(self.output/label/"stdout.txt", 8*MIB)
        if raw and label != "normal-consumer":
            event["public_result"] = diagnostic_json(raw)
        need(known, "SMOKE_UNKNOWN_CHILD_CPU_FULL_GRANT_CHARGED")
        clean(report, exit_code=expected_exit)
        need(read(self.output/label/"stderr.txt", MIB) == b"", "SMOKE_CHILD_STDERR")
        self.check()
        return event["public_result"]

    def owner(self, label, operation, extra=(), *, missing=False):
        need(label in ("init", "contribute-module", "export-module", "missing-library", "extract-std", "complete"),
             "SMOKE_FIXED_OWNER_SEQUENCE")
        def argv(wall, cpu):
            return [str(Path(sys.executable)), "-I", "-S", "-B", str(self.package/"owner.py"), operation,
                "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(self.runtimes["python_runtime"]),
                "--lean-runtime", str(self.runtimes["lean_runtime"]), "--catalog", str(self.catalog),
                "--custody", str(self.custody), "--store-id", self.store,
                "--custody-limits", str(self.fixtures/"custody-limits.json"),
                "--wall-seconds", str(wall), "--cpu-seconds", str(cpu),
                "--memory-mib", str(self.args.memory_mib), *map(str, extra)]
        result = self.command(label, argv, initial=label == "init", expected_exit=1 if missing else 0)
        need(type(result) is dict and result.get("operation") == operation and not result.get("close_errors"),
             "SMOKE_PUBLIC_REPLY")
        if missing:
            detail = result.get("detail", {})
            need(result.get("ok") is False and result.get("phase") == "CONTRIBUTE" and
                 result.get("accepted") is None and detail.get("phase") == "BINDING" and
                 detail.get("accepted") is None and detail.get("error") == "CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS" and
                 detail.get("needs_local_interpretations") == [name("Nat.add_zero")], "SMOKE_EXACT_EXPECTED_MISSING")
        else:
            need(result.get("ok") is True and result["implementation_id"] == self.implementation and
                 result["profile_sha256"] == self.args.profile_sha256 and result["store_id"] == self.store and
                 result["catalog"] == str(self.catalog) and result["custody"] == str(self.custody),
                 "SMOKE_PUBLIC_OWNER_BINDING")
        return result

    def native(self, path, *, extraction=False):
        report = self.document(path, 2*MIB)
        clean(report, extraction=extraction); self.hold(path)
        return report

    def admission(self, accepted, units, names, *, basis=False):
        unit_count = 456 if basis else len(units)
        need(accepted["status"] == "CHECKED" and accepted["units_checked"] == unit_count and
             accepted["retained_unit_ids"] == units, "SMOKE_EXACT_ADMISSION")
        operation = ordinary(Path(accepted["operation_directory"]), directory=True)
        need(operation.parent == self.catalog/"admission-calls", "SMOKE_ADMISSION_PATH")
        native = self.native(operation/"supervision-result.json")
        need(native["final_job"]["cpu_seconds"] == accepted["worker_cpu_seconds"], "SMOKE_ADMISSION_CPU")
        argv = native["argv"]
        artifact = ordinary(Path(argv[-2]))
        need(argv[-3] == accepted["local_root"] and Path(argv[-1]) == operation/"worker-report.json" and
             artifact.name == "chunk.olean" and artifact.parent.parent == self.catalog/"operations",
             "SMOKE_NATIVE_ARTIFACT_PATH")
        observed = self.document(operation/"worker-report.json", 16*MIB)
        need(observed["schema"] == "DMKN_ORDINARY_WORKER_OUTPUT_V1" and
             observed["kind"] == ("basis" if basis else "extension") and observed["names"] == names and
             observed["units_checked"] == unit_count and observed["artifact_bytes"] == artifact.stat().st_size,
             "SMOKE_NATIVE_REPORT")
        self.hold(artifact); self.capture_tree(operation)

    def publication(self, result, directory, parent, outputs):
        need(result == self.document(directory/"RESULT.json") and result["admission"] == self.document(directory/"ADMISSION.json") and
             result["parent_root"] == parent and result["local_root"] != parent and
             result["local_root"] == result["admission"]["local_root"] and result["semantic_id"] == self.semantic and
             result["implementation_id"] == self.implementation and
             [target["name"] for target in result["targets"]] == outputs and
             len(result["units"]) == 2 and len(result["previews"]) == len(outputs), "SMOKE_PUBLICATION_RESULT")
        evidence, by_name, inventory_names = {}, {}, []
        for row in result["units"]:
            path = directory/"evidence"/(row["unit_id"]+".json")
            need(row["file"] == str(path), "SMOKE_EVIDENCE_PATH")
            self.hold(path, {key: row[key] for key in ("bytes", "sha256")})
            raw = read(path); doc = diagnostic_json(raw)
            need(identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == row["unit_id"] and
                 doc["schema"] == "DMKN_LEAN_ORDINARY_EVIDENCE_V2" and
                 doc["semantic_id"] == self.semantic, "SMOKE_EVIDENCE_ID")
            evidence[row["unit_id"]] = doc
            for entry in doc["unit"][2]:
                key = canonical(entry[0]); need(key not in by_name, "SMOKE_DUPLICATE_EXPORT")
                by_name[key] = (row["unit_id"], doc, entry); inventory_names.append(entry[0])
        self.admission(result["admission"], [row["unit_id"] for row in result["units"]], inventory_names)
        for target, preview in zip(result["targets"], result["previews"]):
            need(target["export_id"] == identity("DMKN-ORDINARY-EXPORT-V2",
                 canonical([self.semantic, target["unit_id"], target["name"]])), "SMOKE_EXPORT_ID")
            unit_id, doc, entry = by_name[canonical(target["name"])]
            need(unit_id == target["unit_id"] and {key: preview[key] for key in target} == target,
                 "SMOKE_TARGET_PREVIEW_BINDING")
            path = directory/"previews"/(target["export_id"]+".json")
            need(preview["file"] == str(path), "SMOKE_PREVIEW_PATH")
            self.hold(path, {key: preview[key] for key in ("bytes", "sha256")})
            viewed = self.document(path)
            need(viewed["schema"] == "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2" and
                 viewed["semantic_id"] == self.semantic and viewed["unit_id"] == unit_id and
                 viewed["export_name"] == target["name"] and viewed["header"] == entry[1:4],
                 "SMOKE_PREVIEW_EVIDENCE_HEADER")
        return by_name

    def run(self, report):
        module_names = [name("CommonsPackageExample.applyTwice"), name("CommonsPackageExample.applyTwice_eq")]
        library_names = [name("CommonsLibraryExample.add_zero")]
        report["phase"] = "INITIALIZE"
        initial = self.owner("init", "init")["result"]
        need(initial["status"] == "INITIALIZED_LOCAL_OWNER", "SMOKE_INITIALIZED")
        basis = initial["basis"]["local_root"]; report["basis_root"] = basis
        inventory = self.document(self.package/"installation"/relative(self.manifest["roles"]["inventory"]))
        need(len(inventory) == 581, "SMOKE_FIXED_BASIS_CENSUS")
        self.admission(initial["basis"], [], [row[0] for row in inventory], basis=True)
        adoption = self.document(self.catalog/"ADOPTION.json")
        need(adoption["store_id"] == self.store and adoption["implementation"] == self.manifest["implementation"],
             "SMOKE_FRESH_ADOPTION")
        self.hold(self.catalog/"ADOPTION.json")
        contribution, exported = self.output/"module-contribution", self.output/"export"
        report["phase"] = "CONTRIBUTE_MODULE"
        first = self.owner("contribute-module", "contribute", ("--parent-root", basis,
            "--source", self.fixtures/"module-body.lean", "--acquired-targets", self.fixtures/"acquired.json",
            "--output-names", self.fixtures/"module-outputs.json", "--output", contribution))["result"]
        report["module_admission"] = first["admission"]
        need(first["status"] == "CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES", "SMOKE_CONTRIBUTION_STATUS")
        by_name = self.publication(first, contribution, basis, module_names)
        need([by_name[canonical(n)][1]["unit"][1][0] for n in module_names] == [0, 1], "SMOKE_DEFINITION_AND_THEOREM")
        author = self.native(contribution/"AUTHORING-SUPERVISION.json")
        need(author["argv"][4] == str(self.package/"author_worker.py"), "SMOKE_RELOCATED_AUTHOR_WORKER")
        request = self.document(contribution/"REQUEST.json")
        need(request["parent_root"] == basis and request["acquired_targets"] == [] and
             request["output_names"] == module_names and request["source_body_sha256"] == sha(MODULE_BODY),
             "SMOKE_MODULE_REQUEST")
        self.capture_tree(contribution)
        target = first["targets"][1]
        targets = self.fixture("module-targets.json", [target])
        report["phase"] = "EXPORT_MODULE"
        exported_result = self.owner("export-module", "export-module", ("--parent-root", first["local_root"],
            "--module-targets", targets, "--output", exported))["result"]
        report["module_export"] = exported_result
        manifest = self.document(exported/"MODULE.json")
        need({k: v for k, v in exported_result.items() if k not in ("module_directory", "manifest_path", "supported_runtime")} == manifest and
             manifest["status"] == "CHECKED_PROOF_COMPLETE_LOCAL_MODULE" and
             manifest["source_context_root"] == first["local_root"] and manifest["semantic_id"] == self.semantic and
             manifest["targets"] == [target] and manifest["new_catalog_acceptance"] is False and
             manifest["ordered_unit_ids"] == [row["unit_id"] for row in first["units"]] and
             exported_result["module_directory"] == str(exported/"modules") and
             exported_result["manifest_path"] == str(exported/"MODULE.json"), "SMOKE_MODULE_RESULT")
        runtime = exported_result["supported_runtime"]
        need(runtime["implementation_id"] == self.implementation and
             runtime["installation_manifest_sha256"] == self.profile["installation_manifest_sha256"] and
             runtime["lean_runtime"] == str(self.runtimes["lean_runtime"]) and
             runtime["lean_executable"] == str(self.runtimes["lean_runtime"]/"bin/lean.exe") and
             runtime["lean_executable_pin"] == self.manifest["files"][self.manifest["roles"]["lean"]],
             "SMOKE_MODULE_RUNTIME")
        native = self.native(exported/"SUPERVISION.json")
        need(native["argv"][4] == str(self.package/"module_worker.py") and
             native["argv"][6] == str(self.package/"module/OrdinaryModule.lean") and
             native["final_job"]["cpu_seconds"] == manifest["native_cpu_seconds"], "SMOKE_RELOCATED_MODULE_WORKER")
        native_raw = read(exported/"native-report.json", 8*MIB)
        native_report = diagnostic_json(native_raw)
        need(sha(native_raw) == manifest["report_sha256"] and native_report["units_checked"] == 2 and
             native_report["checking_passes"] == 2 and native_report["basis_rows"] == 581 and
             native_report["semantic_id"] == self.semantic and native_report["context_root"] == first["local_root"] and
             native_report["foundation_id"] == manifest["foundation_id"] and
             native_report["module_name"] == name(manifest["module_name"]) and
             native_report["targets"] == [target["name"]] and
             native_report["unit_ids"] == manifest["ordered_unit_ids"] and native_report["names"] == module_names and
             native_report["inventories"] == [by_name[canonical(n)][2] for n in module_names],
             "SMOKE_MODULE_NATIVE_REPORT")
        trace = [diagnostic_json(line) for line in read(exported/"native-report.json.phases.jsonl").splitlines()]
        need([(r["phase"], r["event"], r["exit_code"]) for r in trace] ==
             [(phase, event, code) for phase in ("build", "reread-private", "reread-exported")
              for event, code in (("STARTED", None), ("EXITED", 0))], "SMOKE_THREE_MODULE_PHASES")
        module = manifest["module_name"]
        needed = {module+suffix for suffix in PARTS}
        need(set(manifest["artifact_parts"]) == needed and {p.name for p in (exported/"modules").iterdir()} == needed,
             "SMOKE_MODULE_FIVE_PARTS")
        for filename, expected in manifest["artifact_parts"].items():
            self.hold(exported/"modules"/filename, expected)
        self.capture_tree(exported)
        report["phase"] = "NORMAL_CONSUMER"
        consumer = self.output/"consumer"; consumer.mkdir()
        source = consumer/"Consumer.lean"; self.hold(source, save(source, consumer_source(module)))
        self.command("normal-consumer", lambda wall, cpu: [str(Path(sys.executable)), "-I", "-S", "-B",
            str(self.script), "--consumer-worker", str(self.runtimes["lean_runtime"]), str(exported/"modules"), str(source)])
        need(read(self.output/"normal-consumer/stdout.txt", MIB) == b"", "SMOKE_CONSUMER_STDOUT")
        produced = {}
        for suffix in PARTS:
            path = consumer/("Consumer"+suffix)
            if path.exists():
                produced[path.name] = self.hold(path)
                need(produced[path.name]["bytes"] > 0, "SMOKE_CONSUMER_PART")
        need({"Consumer.olean", "Consumer.olean.private", "Consumer.olean.server"} <= set(produced),
             "SMOKE_REQUIRED_CONSUMER_PARTS")
        self.capture_tree(consumer)
        report["ordinary_consumer"] = {"source_sha256": sha(consumer_source(module)), "parts": produced,
                                       "theorem_application": True, "definition_reduction": True}
        missing, extraction, completion = (self.output/part for part in ("missing", "extraction", "completion"))
        report["phase"] = "MISSING_LIBRARY"
        refused = self.owner("missing-library", "contribute", ("--parent-root", basis,
            "--source", self.fixtures/"library-body.lean", "--acquired-targets", self.fixtures/"acquired.json",
            "--output-names", self.fixtures/"library-outputs.json", "--output", missing), missing=True)
        need(self.document(missing/"FAILURE.json") == refused["detail"], "SMOKE_RETAINED_REFUSAL")
        author = self.native(missing/"AUTHORING-SUPERVISION.json")
        need(author["final_job"]["cpu_seconds"] == refused["cost"]["worker_cpu_seconds"] ==
             refused["detail"]["native_cpu_seconds"], "SMOKE_REFUSAL_ACCOUNTING")
        candidate_raw, request_raw = read(missing/"candidate.json"), read(missing/"REQUEST.json")
        request = diagnostic_json(request_raw)
        need(request["parent_root"] == basis and request["source_body_sha256"] == sha(LIBRARY_BODY) and
             request["output_names"] == library_names and request["acquired_targets"] == [], "SMOKE_LIBRARY_REQUEST")
        self.capture_tree(missing)
        report["phase"] = "EXTRACTION"
        extracted = self.owner("extract-std", "extract-std", ("--parent-root", basis,
            "--retained-contribution", missing, "--retained-request-sha256", sha(request_raw),
            "--retained-candidate-sha256", sha(candidate_raw), "--library-modules", self.fixtures/"library-modules.json",
            "--output", extraction))["result"]
        need(extracted["status"] == "EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED" and
             extracted["mathematical_acceptance"] is False and extracted["parent_root"] == basis and
             extracted["missing_targets"] == [name("Nat.add_zero")] and
             extracted["supplemental_units"] == extracted["consumer_units"] == 1, "SMOKE_EXACT_EXTRACTION")
        extraction_native = self.native(extraction/"EXTRACTION-SUPERVISION.json", extraction=True)
        need(extraction_native["argv"][0] == str(self.package/"authoring/bin/MissingImportExporter.exe") and
             extracted["native_cpu_seconds"] == extraction_native["native_cpu_seconds"], "SMOKE_NEW_EXTRACTOR_PATH")
        selected = extracted["pins"]
        for key, filename in (("candidate", "candidate.json"), ("targets", "targets.json"),
                ("prepared_bindings", "prepared-bindings.json"), ("extraction_request", "request.json"),
                ("supplement", "supplement.json")):
            self.hold(extraction/filename, selected[key])
        need(read(extraction/"candidate.json") == candidate_raw and self.document(extraction/"targets.json") == library_names,
             "SMOKE_SAME_RETAINED_CANDIDATE")
        self.capture_tree(extraction)
        report["phase"] = "COMPLETION"
        completed = self.owner("complete", "complete", ("--parent-root", basis,
            "--candidate", extraction/"candidate.json", "--candidate-sha256", selected["candidate"]["sha256"],
            "--supplement", extraction/"supplement.json", "--supplement-sha256", selected["supplement"]["sha256"],
            "--prepared-bindings", extraction/"prepared-bindings.json", "--prepared-bindings-sha256", selected["prepared_bindings"]["sha256"],
            "--output-names", extraction/"targets.json", "--output", completion))["result"]
        report["completion_admission"] = completed["admission"]
        need(completed["status"] == "CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES" and
             completed["candidate_sha256"] == sha(candidate_raw) and
             completed["supplement_sha256"] == selected["supplement"]["sha256"], "SMOKE_COMPLETION_RESULT")
        units = self.publication(completed, completion, basis, library_names)
        need(set(units) == {canonical(name("Nat.add_zero")), canonical(library_names[0])}, "SMOKE_TWO_THEOREMS")
        supplier_id, supplier, _ = units[canonical(name("Nat.add_zero"))]
        consumer_id, consumer_doc, _ = units[canonical(library_names[0])]
        supplier_export = identity("DMKN-ORDINARY-EXPORT-V2", canonical([self.semantic, supplier_id, name("Nat.add_zero")]))
        need(supplier["unit"][1][0] == consumer_doc["unit"][1][0] == 1 and
             [name("Nat.add_zero"), supplier_export] in consumer_doc["imports"] and
             any(node[0] == 2 and node[1] == name("Nat.add_zero") for node in consumer_doc["unit"][1][4][2]) and
             not any(row[0] == name("Nat.add_zero") for row in supplier["imports"]), "SMOKE_ACTUAL_SUPPLIED_PROOF_USE")
        self.capture_tree(completion)
        report.update(module_root=first["local_root"], library_root=completed["local_root"],
            actual_proof_use={"supplier_unit": supplier_id, "supplier_export": supplier_export, "consumer_unit": consumer_id})
        need([row["label"] for row in self.calls] == ["init", "contribute-module", "export-module",
             "normal-consumer", "missing-library", "extract-std", "complete"], "SMOKE_EXACT_SEVEN_CALLS")
        report["phase"] = "FINAL_VERIFY"
        for path, expected in list(self.held.items()):
            self.hold(Path(path), expected)
        need(self.capture_tree(self.package) == set(self.package_pins), "SMOKE_FINAL_PACKAGE_CENSUS")
        save(self.output/"IMMUTABLE-FILES.json", self.held)
        self.check()
        report.update(status="PASS_RELOCATED_CURRENT_SOURCE_BUILD_PUBLIC_USE", phase="COMPLETE")


def main():
    if sys.argv[1:2] == ["--consumer-worker"]:
        return consumer_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "SMOKE_PYTHON_PROFILE")
    need(120 <= args.wall_seconds <= 3600 and 100 <= args.cpu_seconds <= 3600 and
         256 <= args.memory_mib <= 8192, "SMOKE_FINITE_ALLOWANCE")
    smoke = Smoke(args)
    report = {"status": "FAILED", "phase": "SUPPORT", "calls": smoke.calls,
        "claim": "SOURCE_BUILD_RELOCATED_PUBLIC_INTEROPERABILITY_NOT_GENERAL_LIBRARY_GROWTH_OR_FINAL_V5",
        "retention": "ALL_PARTIAL_OUTPUT_AND_ACCEPTANCE_PRESERVED_NO_RETRY"}
    try:
        smoke.prepare()
        report.update(profile_sha256=args.profile_sha256, implementation_id=smoke.implementation,
                      installation_manifest_sha256=smoke.profile["installation_manifest_sha256"])
        smoke.run(report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000])
    finally:
        report.update(wall_seconds=time.monotonic()-smoke.started,
            controller_cpu_seconds=time.process_time()-smoke.cpu_started,
            inclusive_child_job_cpu_charged=smoke.charged, child_cpu_complete=smoke.complete,
            accounting="COMPLETE_CHILD_JOB_ONCE_UNKNOWN_FULL_GRANT_THEN_STOP_OUTER_JOB_AUTHORITATIVE")
        if report["wall_seconds"] >= args.wall_seconds or report["controller_cpu_seconds"]+smoke.charged >= args.cpu_seconds:
            report.update(status="FAILED", budget_error="SMOKE_ORIGINAL_ALLOWANCE")
        if hasattr(smoke, "output") and smoke.output.is_dir():
            save(smoke.output/"SMOKE-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_RELOCATED_CURRENT_SOURCE_BUILD_PUBLIC_USE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
