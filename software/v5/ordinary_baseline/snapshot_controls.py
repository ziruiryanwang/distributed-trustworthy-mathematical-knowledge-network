"""Focused exact-snapshot controls with synthetic, never imported artifacts.

Real bounded path/graph/hash/copy/metadata code and installed codecs operate on
small fresh ordinary files. All .olean/.ir contents and the installation/runtime
map are explicit test fixtures. No Lean binary import, source build, native
operation, owner/catalog/database or network access is allowed. These cases do
not qualify the native collector's actual graph or Lean import semantics.
"""
from pathlib import Path
import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PROFILE = "ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f"
MIB = 1024**2
PART_SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir")
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 25,
         "SNAPSHOT_CONTROLS_ORIGINAL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def read(path, maximum=2*MIB):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum, "SNAPSHOT_CONTROLS_READ_BOUND")
    return raw


def write(path, raw, *, mutate=False):
    check()
    need(type(raw) is bytes and len(raw) <= MIB, "SNAPSHOT_CONTROLS_FIXTURE_BOUND")
    with path.open("wb" if mutate else "xb") as stream:
        stream.write(raw)


def module(name, path, expected=None):
    raw = read(path)
    need(expected is None or sha(raw) == expected, "SNAPSHOT_CONTROLS_SOURCE_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    exec(compile(raw, str(path), "exec"), value.__dict__)
    return value


def name(*parts):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in parts]


def import_row(module_name, *, private=0, exported=1, meta=0):
    return {"module": module_name, "import_all": private,
            "is_exported": exported, "is_meta": meta}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "SNAPSHOT_CONTROLS_PROCESS")
    package, output = Path(args.package), Path(args.output)
    need(output.is_absolute() and output.resolve().is_relative_to(LOCAL) and
         output.parent.is_dir() and not os.path.lexists(output), "SNAPSHOT_CONTROLS_OUTPUT")
    profile_raw = read(package/"PROFILE.json")
    need(sha(profile_raw) == PROFILE, "SNAPSHOT_CONTROLS_PROFILE")
    descriptor = json.loads(profile_raw)
    base = module("_snapshot_controls_owner", package/"owner.py",
                  descriptor["files"]["owner.py"]["sha256"])
    loader = base.bootstrap(package, PROFILE, check)
    loaded = loader.load(package, PROFILE, {"python_runtime": Path(r"D:\Python314"),
        "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"},
        START+45, check_parent=check)
    source = Path(__file__).resolve().parent
    S = module("_baseline_snapshot_controls_subject", source/"baseline_snapshot.py")
    A, O = S.A, loaded.O
    need(A is loaded.A and S.X is loaded.library_extraction, "SNAPSHOT_CONTROLS_SHARED_CODECS")
    need(S.SUFFIXES == PART_SUFFIXES and S.METADATA_RESERVATION == 64*MIB,
         "SNAPSHOT_CONTROLS_SELECTED_PART_AND_RESERVATION_CONTRACT")
    output.mkdir()
    cases_directory = output/"cases"
    cases_directory.mkdir()
    cases, forbidden_calls = [], []

    def forbidden(*_, **__):
        forbidden_calls.append("FORBIDDEN")
        raise AssertionError("SNAPSHOT_CONTROLS_FORBIDDEN_EXTERNAL_OPERATION")

    def fixture(label):
        directory = cases_directory/label
        directory.mkdir()
        runtime, support = directory/"runtime", directory/"support"
        first, second = directory/"first-project", directory/"second-project"
        for path in (runtime/"lib/lean", support, first, second):
            path.mkdir(parents=True)
        installation = A.NativeInstallation.__new__(A.NativeInstallation)
        installation.root = support
        installation.runtime_roots = {"lean_runtime": runtime}
        installation.manifest_sha256 = "a"*64
        original_bytes = {}

        def artifact(root, components, imports, phase):
            selected_name = name(*components)
            base_path = root.joinpath(*components).with_suffix(".olean")
            base_path.parent.mkdir(parents=True, exist_ok=True)
            paths, sizes = [], []
            for suffix in PART_SUFFIXES:
                path = base_path.with_suffix(suffix)
                raw = ("INERT_NEVER_IMPORTED:"+".".join(components)+":"+suffix+"\n").encode("ascii")
                write(path, raw)
                original_bytes[path] = raw
                paths.append(str(path)); sizes.append(len(raw))
            return {"module": selected_name, "is_module": 1, "imports": imports,
                "effective": {"import_all": 1, "is_exported": 1, "is_meta": 0,
                              "has_data": 1, "ir_phases": phase},
                "parts": [paths[:3], paths[3:]], "part_bytes": [sizes[:3], sizes[3:]]}

        core = artifact(runtime/"lib/lean", ("Core", "Base"), [], "runtime")
        leaf = artifact(first, ("Demo", "Leaf"), [import_row(core["module"], private=1)], "all")
        tools = artifact(second, ("Extra", "Tools"),
                         [import_row(core["module"], exported=0, meta=1)], "comptime")
        top = artifact(first, ("Demo", "Root"),
                       [import_row(leaf["module"]), import_row(tools["module"], meta=1)], "all")
        report = {"schema": S.REPORT_SCHEMA,
            "assurance": "INERT_ARTIFACT_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE", "mode": "collect",
            "roots": [import_row(top["module"])], "modules": [top, leaf, core, tools]}
        project_raw = A.E.canonical_json({"schema": "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
            "project_search_paths": [str(first), str(second)], "modules": [top["module"]]})
        return {"directory": directory, "installation": installation, "first": first,
                "second": second, "runtime": runtime, "project_raw": project_raw,
                "report": report, "original_bytes": original_bytes, "artifact": artifact,
                "output": directory/"prepared"}

    def census(report):
        rows = report["modules"]
        report.update(module_count=len(rows), part_count=5*len(rows),
                      direct_import_edges=sum(len(row["imports"]) for row in rows),
                      artifact_bytes=sum(sum(row["part_bytes"][0])+sum(row["part_bytes"][1])
                                         for row in rows))

    def invoke(data, *, spool=None):
        report = data["report"]
        census(report)
        raw = encoded(report)
        return S.prepare_snapshot(data["installation"],
            project_selection_raw=data["project_raw"], project_selection_sha256=sha(data["project_raw"]),
            report_raw=raw, report_sha256=sha(raw), output_directory=data["output"],
            spool_bytes=report["artifact_bytes"]+S.METADATA_RESERVATION if spool is None else spool,
            check_budget=check)

    def unchanged(data):
        need(all(read(path) == raw for path, raw in data["original_bytes"].items()),
             "SNAPSHOT_CONTROLS_UNEXPECTED_SOURCE_MUTATION")

    def reject(label, data, code, *, spool=None, source_unchanged=True):
        check()
        try:
            invoke(data, spool=spool)
        except ValueError as error:
            need(code in str(error), "SNAPSHOT_CONTROLS_WRONG_REFUSAL:"+label+":"+str(error))
        else:
            raise AssertionError("SNAPSHOT_CONTROLS_MISSING_REFUSAL:"+label)
        need(not data["output"].exists(), "SNAPSHOT_CONTROLS_PREFLIGHT_CREATED_OUTPUT:"+label)
        if source_unchanged:
            unchanged(data)
        cases.append({"case": label, "expected_refusal": code, "snapshot_created": False})

    with ExitStack() as stack:
        for obj, attribute in ((sqlite3, "connect"), (subprocess, "Popen"), (socket, "socket"),
                (A.OrdinaryAdmission, "open"), (A.OrdinaryAdmission, "_execute"),
                (A.P.PortableCatalog, "open"), (A.P.PortableCatalog, "_commit_checked"),
                (O.OrdinaryStore, "__init__"), (O.OrdinaryStore, "put_evidence")):
            stack.enter_context(patch.object(obj, attribute, forbidden))
        data = fixture("exact-multimodule-snapshot")
        metadata_writes = []
        original_write = S._write

        def observed_write(path, raw, maximum, checker):
            original_write(path, raw, maximum, checker)
            metadata_writes.append(Path(path).name)

        with patch.object(S, "_write", observed_write):
            result = invoke(data)
        unchanged(data)
        manifest = A.E.strict_json(result.manifest_raw, A.E.Limits(max_bytes=S.MAX_MANIFEST))
        replay = A.E.strict_json(result.replay_request_raw, A.E.Limits(max_bytes=S.MAX_REQUEST))
        need(manifest["schema"] == S.SNAPSHOT_SCHEMA and
             manifest["status"] == "PREPARED_NOT_REPLAYED_OR_REGISTERED" and
             manifest["mathematical_acceptance"] == 0 and
             manifest["installation_manifest_sha256"] == data["installation"].manifest_sha256 and
             manifest["project_selection_sha256"] == sha(data["project_raw"]) and
             manifest["source_report_sha256"] == sha(encoded(data["report"])) and
             manifest["replay_request_sha256"] == sha(result.replay_request_raw) and
             result.manifest_sha256 == sha(result.manifest_raw), "SNAPSHOT_CONTROLS_EXACT_METADATA_PINS")
        need(replay["schema"] == S.REQUEST_SCHEMA and replay["mode"] == "replay" and
             replay["modules"] == [data["report"]["modules"][0]["module"]] and
             len(replay["artifacts"]) == len(manifest["modules"]) == 4 and
             manifest["module_count"] == 4 and manifest["part_count"] == 20,
             "SNAPSHOT_CONTROLS_EXACT_REPLAY_CENSUS")
        rows = {A.E.name_key(row["module"]): row for row in data["report"]["modules"]}
        seen, actual_bytes = set(), 0
        for saved, mapped in zip(manifest["modules"], replay["artifacts"]):
            key = A.E.name_key(saved["module"])
            original = rows[key]
            need(key not in seen and {A.E.name_key(row["module"]) for row in original["imports"]} <= seen,
                 "SNAPSHOT_CONTROLS_TOPOLOGICAL_COPY")
            seen.add(key)
            need(saved["imports"] == original["imports"] and saved["effective"] == original["effective"] and
                 mapped == {"module": saved["module"], "parts": saved["parts"]},
                 "SNAPSHOT_CONTROLS_FLAGS_AND_REPLAY_MATRIX")
            for suffix, target, pin, origin in zip(PART_SUFFIXES, S._matrix(saved["parts"]),
                    S._matrix(saved["pins"]), S._matrix(original["parts"])):
                destination = data["output"]/"modules"/sha(key)/("module"+suffix)
                raw = data["original_bytes"][Path(origin)]
                need(Path(target) == destination and read(destination) == raw and
                     pin == {"bytes": len(raw), "sha256": sha(raw)}, "SNAPSHOT_CONTROLS_EXACT_PART_COPY")
                actual_bytes += len(raw)
        need(seen == rows.keys() and result.artifact_bytes == actual_bytes == manifest["artifact_bytes"] and
             result.total_bytes == actual_bytes+len(encoded(data["report"]))+
                                   len(result.manifest_raw)+len(result.replay_request_raw),
             "SNAPSHOT_CONTROLS_TOTAL_ACCOUNTING")
        need(metadata_writes == ["source-report.json", "replay-request.json", "prepared-manifest.json"] and
             read(data["output"]/"source-report.json") == encoded(data["report"]) and
             read(data["output"]/"replay-request.json") == result.replay_request_raw and
             read(data["output"]/"prepared-manifest.json") == result.manifest_raw,
             "SNAPSHOT_CONTROLS_PREPARED_MANIFEST_LAST")
        cases.append({"case": "exact-multimodule-snapshot-replay-matrix", "modules": 4,
            "parts": 20, "artifact_bytes": actual_bytes, "total_bytes": result.total_bytes,
            "prepared_manifest_sha256": result.manifest_sha256, "mathematical_acceptance": False})

        data = fixture("prefix-shadow-missing-child")
        (data["first"]/"Extra").mkdir()
        reject("first-package-prefix-shadows-later-complete-child", data, "CATALOG_MISSING_PATH")

        data = fixture("source-length-changed")
        path = next(iter(data["original_bytes"]))
        write(path, data["original_bytes"][path]+b"!", mutate=True)
        reject("source-byte-length-changed", data, "BASELINE_SNAPSHOT_SOURCE_SIZE", source_unchanged=False)

        data = fixture("unapproved-part-location")
        row = data["report"]["modules"][0]
        unapproved = data["directory"]/"unapproved"
        unapproved.mkdir()
        external = unapproved/"Root.olean"
        write(external, data["original_bytes"][Path(row["parts"][0][0])])
        row["parts"][0][0] = str(external)
        reject("existing-but-unapproved-part-location", data, "BASELINE_SNAPSHOT_APPROVED_RESOLUTION")

        data = fixture("dot-component-report-path")
        row = data["report"]["modules"][0]
        path = Path(row["parts"][0][0])
        row["parts"][0][0] = str(path.parent)+"\\..\\Demo\\"+path.name
        reject("dot-components-rejected-before-normalization", data, "BASELINE_SNAPSHOT_PATH_COMPONENTS")

        data = fixture("missing-import-dependency")
        data["report"]["modules"][0]["imports"].append(import_row(name("Missing", "Lemma")))
        reject("complete-graph-required", data, "BASELINE_SNAPSHOT_MISSING_DEPENDENCY")

        data = fixture("unreachable-extra-module")
        extra = data["artifact"](data["second"], ("Unused", "Extra"), [], "all")
        data["report"]["modules"].append(extra)
        reject("extra-unreachable-module-refuses", data, "BASELINE_SNAPSHOT_UNUSED_MODULE")

        data = fixture("import-cycle")
        data["report"]["modules"][2]["imports"] = [import_row(data["report"]["modules"][0]["module"])]
        reject("dependency-cycle-refuses", data, "BASELINE_SNAPSHOT_IMPORT_CYCLE")

        data = fixture("spool-too-small")
        census(data["report"])
        reject("metadata-reservation-before-snapshot-writes", data, "BASELINE_SNAPSHOT_SPOOL_RESERVATION",
               spool=data["report"]["artifact_bytes"]+S.METADATA_RESERVATION-1)

        data = fixture("copy-time-same-length-source-mutation")
        original_hash, mutations = S._hash_exact, []

        def hash_then_mutate(path, size, checker):
            digest = original_hash(path, size, checker)
            if not mutations:
                original = read(path)
                changed = bytes([original[0] ^ 1])+original[1:]
                write(path, changed, mutate=True)
                mutations.append({"path": str(path), "bytes": size,
                                  "before": digest, "after": sha(changed)})
            return digest

        with patch.object(S, "_hash_exact", hash_then_mutate):
            try:
                invoke(data)
            except ValueError as error:
                need("BASELINE_SNAPSHOT_COPY_CHANGED" in str(error), "SNAPSHOT_CONTROLS_COPY_MUTATION_REFUSAL")
            else:
                raise AssertionError("SNAPSHOT_CONTROLS_COPY_MUTATION_NOT_DETECTED")
        partial = list((data["output"]/"modules").glob("*/module.olean"))
        need(len(mutations) == 1 and len(partial) == 1 and partial[0].is_file() and
             all(not (data["output"]/filename).exists() for filename in
                 ("source-report.json", "replay-request.json", "prepared-manifest.json")),
             "SNAPSHOT_CONTROLS_PARTIAL_COPY_PRESERVED_WITHOUT_MANIFEST")
        cases.append({"case": "copy-time-source-mutation-preserves-partial-no-manifest",
                      "expected_refusal": "BASELINE_SNAPSHOT_COPY_CHANGED", "mutation": mutations[0],
                      "partial_copy": str(partial[0]), "prepared_manifest_created": False})
        need(not forbidden_calls, "SNAPSHOT_CONTROLS_NO_FORBIDDEN_OPERATION")
    check()
    report = {"status": "PASS_REAL_SNAPSHOT_PATH_GRAPH_HASH_COPY_SYNTHETIC_ARTIFACTS",
        "cases": cases, "case_count": len(cases), "forbidden_calls": forbidden_calls,
        "profile_sha256": PROFILE, "mathematical_acceptance": False,
        "scope": "INERT_FIXTURE_FILES_NOT_BINARY_IMPORT_COLLECTOR_OR_CORRESPONDENCE",
        "wall_seconds": time.monotonic()-START, "controller_cpu_seconds": time.process_time()-CPU}
    raw = encoded(report)
    need(len(raw) <= MIB, "SNAPSHOT_CONTROLS_REPORT_BOUND")
    write(output/"RESULT.json", raw)
    print(json.dumps({"status": report["status"], "case_count": len(cases)}), flush=True)


if __name__ == "__main__":
    main()
