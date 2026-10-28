"""Focused controller controls with inert compiler outputs; root selects execution.

No Lean, native binary, child process, database, owner or network operation.
Synthetic installation/profile files are fixture data, never build qualification.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

BUILD_SHA = "d14f2910003b8f8bc36dacc50796b37f87befbc60de76fb9cb575e30e8ce9ef1"
MAP_SHA = "65fde356b8ce6146b07ab49fad40a859af5bf0ce32e8d7beea76e32da60a9c9e"
HELPER_SHA = "49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5"
PREFIX = "software/v5/ordinary_current_distribution/"
CORE = ("ordinary_evidence", "ordinary_semantics", "portable_evidence",
        "local_catalog", "portable_catalog", "ordinary_admission")
RECEIVER = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "LocalSnapshot",
            "BootstrapSupport", "OrdinaryExport", "BasisSnapshot", "OrdinaryWorkflowWorker")
AUTHORING = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
             "OwnerRebind", "OwnerConstruction", "OwnerUseCommand", "OrdinaryExport",
             "SuccessorExport", "SuccessorExportCommand", "PortableOwnerConstructCommand",
             "PortableConstructExportCommand", "PortableContributionExportCommand")
EXTRACTOR = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport",
             "OrdinaryExport", "MissingImportExporter", "BaselineExporter")
PARTS = (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise AssertionError("CURRENT_CONTROL_"+code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def pin(raw):
    return {"bytes": len(raw), "sha256": digest(raw)}


def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def load(path, expected, name):
    raw = path.read_bytes()
    need(digest(raw) == expected and name not in sys.modules, "SELECTED_SOURCE")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def refuses(fn, expected):
    try:
        fn()
    except (ValueError, AssertionError) as error:
        need(str(error) == expected, "WRONG_REFUSAL:"+str(error))
    else:
        raise AssertionError("CURRENT_CONTROL_EXPECTED_REFUSAL:"+expected)


@contextmanager
def isolated_core_names():
    names = (*CORE, "_dmkn_distribution_installer", "_dmkn_distribution_supervisor",
             "_dmkn_distribution_job", "domains")
    need(not any(name in sys.modules for name in names), "PRELOADED_CORE")
    previous = list(sys.path)
    try:
        yield
    finally:
        for name in names:
            sys.modules.pop(name, None)
        sys.path[:] = previous


def forbidden(*args, **kwargs):
    raise AssertionError("CURRENT_CONTROL_CHILD_OR_DATABASE_FORBIDDEN")


class SyntheticCase:
    """Exercise the real controller with inert artifacts and observed stage grants."""

    def __init__(self, candidate, helper, source, mapping, output, mode):
        self.C, self.B, self.mode = candidate, helper, mode
        self.root = output/mode
        need(not self.root.exists(), "FRESH_CASE")
        self.root.mkdir()
        self.source = self.root/"source"
        self.python, self.lean = self.root/"python", self.root/"lean"
        self.output = self.root/"synthetic-build"
        self.mapping = deepcopy(mapping)
        self.calls, self.imports, self.runtime_pins = [], {}, {}
        self.original_load = helper.load_module
        for name in mapping["sources"]:
            write(self.source/name, (source/name).read_bytes())
        write(self.source/PREFIX/"build.py", (source/PREFIX/"build.py").read_bytes())
        all_runtime = set(helper.RUNTIME_PINS) | set(mapping["native_runtime_pins"])
        for name in sorted(all_runtime):
            kind, suffix = name.split("/", 1)
            raw = ("SYNTHETIC-NOT-EXECUTABLE:"+name).encode("ascii")
            write((self.python if kind == "python_runtime" else self.lean)/suffix, raw)
            if name in helper.RUNTIME_PINS:
                self.runtime_pins[name] = (len(raw), digest(raw))
            else:
                self.mapping["native_runtime_pins"][name] = pin(raw)
        self.map_raw = canonical(self.mapping)
        write(self.source/PREFIX/"source-map.json", self.map_raw)
        write(self.root/"SYNTHETIC-FIXTURE.json", canonical({
            "claim": "MOCK_COMPILER_OUTPUTS_NOT_A_BUILD_OR_MATHEMATICAL_ACCEPTANCE",
            "mode": mode, "runtime_bytes": "NONEXECUTABLE_MARKERS"}))

    def load_module(self, name, path):
        if name == "_dmkn_distribution_supervisor":
            return SimpleNamespace(limits_checked=lambda grant: dict(grant), supervise=self.supervise)
        if name == "domains":
            return SimpleNamespace()
        if name == "_dmkn_distribution_job":
            return SimpleNamespace(Job=object)
        module = self.original_load(name, path)
        if name in CORE:
            self.imports[name] = str(Path(module.__file__).resolve())
            if self.mode == "wrong-core-origin" and name == "ordinary_admission":
                module.__file__ = str(self.source/"software/v5/ordinary_lean/ordinary_admission.py")
        if name == "_dmkn_distribution_installer":
            need(all(self.imports[n] == str(self.output/"_build/selected-core"/(n+".py"))
                     for n in CORE), "INSTALLER_SELECTED_IMPORTS")
        return module

    def supervise(self, argv, cwd, log, grant, job):
        need(job is object and not log.exists(), "MOCK_JOB_BOUNDARY")
        need(grant["memory_mib"] == 256 and grant["active_processes"] == 8 and
             grant["stdout_bytes"] == grant["stderr_bytes"] == 8*MIB and
             0 < grant["wall_seconds"] < 120 and 0 < grant["cpu_seconds"] < 300,
             "AGGREGATE_GRANT_SHAPE")
        need(not self.calls or grant["wall_seconds"] <= self.calls[-1]["grant"]["wall_seconds"] and
             grant["cpu_seconds"] <= self.calls[-1]["grant"]["cpu_seconds"], "GRANT_NOT_RENEWED")
        self.calls.append({"argv": list(argv), "grant": dict(grant)})
        log.mkdir(); write(log/"stdout.txt", b""); write(log/"stderr.txt", b"")
        command = argv[5]

        def emit(directory, modules, suffixes):
            need(not any(directory.iterdir()), "FRESH_MOCK_OBJECT_LANE")
            for module in modules:
                for suffix in suffixes:
                    write(directory/(module+suffix),
                          ("SYNTHETIC-NONNATIVE:"+command+":"+module+suffix).encode("ascii"))

        if command == "--compile-worker":
            need(len(self.calls) == 1 and len(argv) == 12, "RECEIVER_AUTHORING_STAGE")
            receiver_source, receiver_objects, author_source, author_objects = map(Path, argv[7:11])
            need(receiver_source != author_source and receiver_objects != author_objects,
                 "SEPARATE_COMPILE_LANES")
            receiver = (receiver_source/"CheckedExtension.lean").read_bytes()
            author = (author_source/"CheckedExtension.lean").read_bytes()
            need(digest(receiver) == self.mapping["sources"][
                "software/v5/ordinary_kernel_admission/CheckedExtension.lean"]["sha256"] and
                 digest(author) == self.B.PUBLIC_HASHES["CheckedExtension"] and receiver != author,
                 "ACTUAL_STAGED_LANE_SEPARATION")
            emit(receiver_objects, RECEIVER, (".olean",))
            emit(author_objects, AUTHORING, PARTS)
        elif command == "--extractor-worker":
            need(len(self.calls) == 2 and len(argv) == 10, "EXTRACTOR_STAGE")
            source, objects = map(Path, argv[7:9])
            need(digest((source/"CheckedExtension.lean").read_bytes()) == self.mapping["sources"][
                "software/v5/ordinary_lean/CheckedExtension.lean"]["sha256"], "LEGACY_EXTRACTOR_SUPPORT")
            emit(objects, EXTRACTOR, (".olean", ".c", ".o"))
            for name in ("MissingImportExporter", "BaselineExporter"):
                write(objects/(name+".exe"), ("SYNTHETIC-NOT-EXECUTABLE:"+name).encode("ascii"))
        elif command == "--query-worker":
            need(len(self.calls) == 3 and len(argv) == 11 and
                 Path(argv[8]) == self.output/"_build/authoring-objects", "QUERY_CURRENT_HELPERS")
            emit(Path(argv[9]), ("OwnerQueryCommand",), PARTS)
        else:
            raise AssertionError("CURRENT_CONTROL_UNEXPECTED_WORKER:"+command)
        final = {"active_processes": 0, "terminated_processes": 0}
        if self.mode != "unknown-child-cpu":
            final["cpu_seconds"] = 0.25
        return {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
                "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
                "termination_requested": False, "final_job": final}

    def run(self):
        args = SimpleNamespace(source_root=str(self.source), python_runtime=str(self.python),
            lean_runtime=str(self.lean), output=str(self.output), wall_seconds=120,
            cpu_seconds=300, memory_mib=256)
        with isolated_core_names(), patch.object(self.C, "bootstrap", return_value=self.B), \
                patch.object(self.C, "MAP_SHA", digest(self.map_raw)), \
                patch.object(self.B, "RUNTIME_PINS", self.runtime_pins), \
                patch.object(self.B, "load_module", side_effect=self.load_module), \
                patch.object(sys, "executable", str(self.python/"python.exe")), \
                patch.object(subprocess, "Popen", forbidden), patch.object(subprocess, "call", forbidden), \
                patch.object(sqlite3, "connect", forbidden):
            if self.mode == "wrong-map-pin":
                with patch.object(self.C, "MAP_SHA", "0"*64):
                    refuses(lambda: self.C.build(args), "DISTRIBUTION_SOURCE_MAP_PIN")
                need(not self.output.exists() and not self.calls, "BAD_MAP_PREOUTPUT")
                return {"mode": self.mode, "refused_before_output": True}
            if self.mode == "wrong-core-origin":
                refuses(lambda: self.C.build(args), "DISTRIBUTION_CORE_IMPORT_PATH")
                need(not self.calls and not (self.output/"package").exists(), "BAD_CORE_PRECOMPILE")
                return {"mode": self.mode, "refused_before_compile": True}
            if self.mode == "unknown-child-cpu":
                refuses(lambda: self.C.build(args),
                        "DISTRIBUTION_CHILD_NOT_CLEAN:receiver-authoring-job")
                failure = json.loads((self.output/"_build/BUILD-FAILURE.json").read_bytes())
                need(len(self.calls) == 1 and failure["child_cpu_complete"] is False and
                     failure["inclusive_child_cpu_charged"] == self.calls[0]["grant"]["cpu_seconds"] and
                     not (self.output/"package/PROFILE.json").exists(), "UNKNOWN_CPU_CHARGED_AND_STOPPED")
                return {"mode": self.mode, "full_grant_charged": failure["inclusive_child_cpu_charged"]}
            result = self.C.build(args)
            package = self.output/"package"
            actual = {p.relative_to(package).as_posix(): pin(p.read_bytes())
                      for p in package.rglob("*") if p.is_file()}
            profile = json.loads((package/"PROFILE.json").read_bytes())
            installed = json.loads((package/"installation/INSTALLATION.json").read_bytes())
            need(len(actual) == 154 and result["files"] == actual and len(profile["files"]) == 117 and
                 len(result["documentation_files"]) == 8, "FULL_ROLE_CENSUS")
            for logical, source in self.mapping["copies"].items():
                need((package/logical).read_bytes() == (self.source/source).read_bytes(),
                     "EXACT_SELECTED_COPY:"+logical)
            need(installed["files"]["py/ordinary_admission.py"] == self.mapping["sources"][
                "software/v5/ordinary_parse_reuse/ordinary_admission.py"] and
                 profile["installation_manifest_sha256"] == result["installation_manifest_sha256"] and
                 len(self.calls) == 3 and result["inclusive_child_job_cpu_seconds"] == 0.75 and
                 result["child_cpu_complete"] is True, "CURRENT_CORE_AND_SINGLE_CPU_CHARGE")
            return {"mode": self.mode, "files": len(actual), "auxiliary": len(profile["files"]),
                    "documents": 8, "synthetic_child_cpu_seconds": 0.75,
                    "claim": "MOCK_COMPOSITION_NOT_NATIVE_BUILD_QUALIFICATION"}


def main():
    need(sys.platform == "win32" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_WINDOWS_PROCESS")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source, output = Path(args.source_root), Path(args.output)
    need(source.is_absolute() and source.is_dir() and output.is_absolute() and
         output.parent.is_dir() and not output.exists() and not source.is_relative_to(output),
         "FRESH_SELECTED_PATHS")
    started = time.monotonic()
    candidate = load(source/PREFIX/"build.py", BUILD_SHA, "_current_candidate_controls")
    helper = load(source/"software/v5/ordinary_package/build.py", HELPER_SHA, "_current_helper_controls")
    raw = (source/PREFIX/"source-map.json").read_bytes()
    need(digest(raw) == MAP_SHA, "MAP_PIN")
    mapping = json.loads(raw)
    candidate.validate_mapping(mapping, helper)
    passed = ["selected_map_and_exact_closure"]
    for name, expected in mapping["sources"].items():
        need(pin((source/name).read_bytes()) == expected, "SOURCE_BYTES:"+name)
    for lane, rows in mapping["lanes"].items():
        for row in rows:
            body = (source/row["source"]).read_bytes()
            view, record = candidate.transform_source(helper, row, body, mapping["sources"])
            need(digest(view) == row["transformed_sha256"] and
                 record["original_sha256"] == digest(body), "SELECTED_TRANSFORM:"+lane)
            refuses(lambda: candidate.transform_source(helper, row, body+b"\n", mapping["sources"]),
                    "DISTRIBUTION_TRANSFORM_INPUT")
    passed.append("all_selected_lane_transforms_and_changed_byte_refusal")
    bad = deepcopy(mapping); bad["counts"]["auxiliary_payloads"] = 113
    refuses(lambda: candidate.validate_mapping(bad, helper), "DISTRIBUTION_SOURCE_MAP_SCHEMA")
    bad = deepcopy(mapping); bad["copies"].pop("CONTACTS.md")
    refuses(lambda: candidate.validate_mapping(bad, helper), "DISTRIBUTION_SOURCE_CENSUS")
    bad = deepcopy(mapping)
    row = next(r for r in bad["lanes"]["receiver"] if r["module"] == "CheckedExtension")
    row["source"] = "software/v5/ordinary_lean/CheckedExtension.lean"
    row["transformed_sha256"] = bad["sources"][row["source"]]["sha256"]
    refuses(lambda: candidate.validate_mapping(bad, helper), "DISTRIBUTION_CHECKED_EXTENSION_LANE")
    passed.append("stale_census_missing_role_and_wrong_receiver_lane_refused")
    output.mkdir()
    outcomes = []
    for mode in ("positive", "wrong-map-pin", "wrong-core-origin", "unknown-child-cpu"):
        need(time.monotonic()-started < 60, "ORIGINAL_CONTROL_DEADLINE")
        case = SyntheticCase(candidate, helper, source, mapping, output, mode)
        outcomes.append(case.run())
        passed.append("synthetic_"+mode)
    result = {"status": "FOCUSED_CURRENT_DISTRIBUTION_CONTROLS_PASSED", "groups": passed,
              "builder_sha256": BUILD_SHA, "map_sha256": MAP_SHA, "outcomes": outcomes,
              "native_calls": 0, "child_launches": 0, "database_operations": 0,
              "claim": "SOURCE_AND_MOCK_CONTROLLER_ONLY_NOT_A_NATIVE_BUILD_OR_MATHEMATICAL_ACCEPTANCE"}
    write(output/"RESULT.json", canonical(result))
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
