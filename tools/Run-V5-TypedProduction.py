"""One explicit typed-production attempt under the unchanged finite supervisor.

Narrow successor of Run-V5-Production.py: separate schema/entry and complete
typed source closure. No compilation, retries, automatic continuation or funding.
Selections are trusted owner decisions, never downloaded peer instructions.
"""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
SOURCE_MODULES = (
    "aggregate_lifecycle", "aggregate_lifecycle.producer", "aggregate_lifecycle.snapshot",
    "aggregate_small", "aggregate_small.producer", "production", "production.producer",
    "aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
    "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec", "typed_production", "typed_production.producer",
    "typed_production.snapshot_adoption", "typed_production.host_adoption",
    "typed_production.image_adoption", "aggregate_small.operator", "typed_production.operator")


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, relative, files):
    path = BASE / relative
    raw = path.read_bytes()
    need({"sha256": sha(raw), "bytes": len(raw)} == files[relative], "SUPERVISOR_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def main():
    wall, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_OWNER_INVOCATION")
    need(len(sys.argv) == 3, "SELECTION_AND_SHA_REQUIRED")
    manifest_raw = (BASE / "RELEASE-MANIFEST.json").read_bytes()
    need(sha(manifest_raw) == MANIFEST_SHA, "FROZEN_SUPERVISOR_MANIFEST")
    files = json.loads(manifest_raw)["files"]
    A = load("_v5_supervisor", "operator/commons.py", files)
    load("domains", "receiver/helpers/domains.py", files)
    J = load("_v5_job", "receiver/helpers/run_stage.py", files)
    path = A.absolute(sys.argv[1])
    need(path.is_relative_to(ROOT / "experiments"), "LOCAL_SELECTION")
    raw = A.bounded_read(path, 1024**2)
    need(sha(raw) == sys.argv[2], "SELECTION_PIN")
    s = A.strict(raw)
    need(set(s) == {"schema", "name", "sources", "runtime_pins", "argv", "limits"}
         and s["schema"] == "DMKN_V5_TYPED_PRODUCTION_V1", "SELECTION_SCHEMA")
    need(type(s["name"]) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", s["name"]), "RUN_NAME")
    limits = A.limits_checked(s["limits"])
    relative_sources = tuple(name.replace(".", "/") + (".py" if "." in name else "/__init__.py")
                             for name in SOURCE_MODULES)
    own = Path(__file__).resolve().relative_to(ROOT).as_posix()
    expected_sources = {"software/v5/"+relative for relative in relative_sources} | {own}
    need(type(s["sources"]) is dict and len(expected_sources) == 32
         and set(s["sources"]) == expected_sources, "EXACT_TYPED_PRODUCTION_SOURCE_SET")
    selected = {}
    for rel, expected in s["sources"].items():
        source = A.absolute(ROOT.joinpath(*A.safe_relative(rel)))
        contents = A.bounded_read(source, 2*1024**2)
        need(sha(contents) == expected, "SOURCE_PIN:" + rel)
        selected[rel] = contents
    need(sum(map(len, selected.values())) <= 16*1024**2, "SOURCE_TOTAL_BOUND")
    need(type(s["runtime_pins"]) is dict and 1 <= len(s["runtime_pins"]) <= 256, "RUNTIME_COUNT")

    def verify_runtime():
        for name, expected in s["runtime_pins"].items():
            runtime_path = A.absolute(name)
            size = runtime_path.stat().st_size
            need(size <= 512*1024**2, "RUNTIME_FILE_BOUND")
            with runtime_path.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
            need(runtime_path.stat().st_size == size and actual == expected, "RUNTIME_PIN:" + name)

    verify_runtime()
    argv = s["argv"]
    need(type(argv) is list and len(argv) == 16
         and all(type(x) is str and len(x) <= 4096 and "\0" not in x for x in argv)
         and argv[1:4] == ["-I", "-S", "-B"] and argv[5] == "run"
         and argv[6::2] == ["--profile", "--profile-sha256", "--request",
                            "--request-sha256", "--owner-report"],
         "EXACT_FINITE_TYPED_OPERATOR_COMMAND")
    # Stable installation is retained across attempts. A snapshot is evidence,
    # not a new owner installation that silently changes profile/allowance ID.
    operator = A.absolute(argv[4])
    need(operator.is_relative_to(ROOT / "experiments/v5-local-checks")
         and operator.parts[-4:] == ("software", "v5", "typed_production", "operator.py"),
         "RETAINED_TYPED_PRODUCTION_OPERATOR")
    source_root = operator.parents[1]
    for relative in relative_sources:
        actual = A.absolute(source_root.joinpath(*PurePosixPath(relative).parts))
        selected_relative = "software/v5/"+relative
        need(str(actual) in s["runtime_pins"]
             and s["runtime_pins"][str(actual)] == sha(selected[selected_relative])
             and A.bounded_read(actual, 2*1024**2) == selected[selected_relative],
             "EXACT_RETAINED_TYPED_SOURCE:"+relative)
    output = ROOT / "experiments/v5-local-checks" / s["name"]
    A.absolute(output, directory=True, fresh=True)
    need(not source_root.is_relative_to(output) and not output.is_relative_to(source_root),
         "STABLE_INSTALLATION_DISJOINT_FROM_ATTEMPT")
    output.mkdir()
    snapshot = output / "sources"
    snapshot.mkdir()
    for rel, contents in selected.items():
        target = snapshot.joinpath(*PurePosixPath(rel).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(contents)
    with (output / "selection.json").open("xb") as stream:
        stream.write(raw)
    argv = [x.replace("{snapshot}", str(snapshot)).replace("{output}", str(output)) for x in argv]
    need(argv[4] == str(operator), "EXECUTED_OPERATOR_IS_CHECKED_OPERATOR")
    need(argv[0] in s["runtime_pins"], "PINNED_COMMAND")
    result = A.supervise(argv, ROOT, output / "command", limits, J.Job, started=wall)
    try:
        verify_runtime()
        need(path.read_bytes() == raw, "SELECTION_CHANGED")
        for rel, contents in selected.items():
            need(snapshot.joinpath(*PurePosixPath(rel).parts).read_bytes() == contents,
                 "SNAPSHOT_CHANGED:" + rel)
    except BaseException as error:
        result.update(status="FINAL_BINDING_FAILED", binding_error=str(error))
    report = {"schema": "DMKN_V5_TYPED_PRODUCTION_RESULT_V1", "selection_sha256": sha(raw),
              "result": result, "wrapper_cpu_seconds": time.process_time()-cpu,
              "wall_seconds": time.monotonic()-wall,
              "authority": "LOCAL_PRODUCTION_EVIDENCE_NOT_MODULE_CERTIFICATION",
              "runtime_scope": "EXPLICIT_RUNTIME_PINS_NOT_HERMETIC_TOOLCHAIN_PROOF"}
    A.save_new(output / "RESULT.json", report)
    print(json.dumps(report), flush=True)
    return 0 if result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
