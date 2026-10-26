"""One retained-concept module export and persisted-tag reopen, not a growth test.

Invoked only under the root-selected bounded Job. No initialization, intake,
new proof, producer project, network or direct state mutation. The unchanged
public owner CLI may add a new module sidecar to the existing compatible owner.
All prior sidecar files are pinned before and checked after; failures retained.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
OWNER = LOCAL / "concept-recipient-init-01"
STORE = "dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09"
CONTEXT = "03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
UNIT = "52c32f0b4de89b9fed93bd099499dd7d029c6bc62e5de32bfeeaa25b08c9e3dd"
UNIT_SHA = "fe0d8a292f3532f7da7a4a74ac41de7b267457193c8f417f7210e7a33767e90f"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
HELPER = ROOT / "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic()-START < 160 and time.process_time()-CPU < 20,
         "EXACT_PUBLIC_ALLOWANCE")


def helpers():
    raw = HELPER.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "EXACT_PUBLIC_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_exact_public_files", HELPER)
    h = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), h.__dict__)
    h.ordinary(HELPER)
    return h


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "output", "custody-limits"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and Path(sys.executable) == PYTHON and
         sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize, "EXACT_PUBLIC_CONTEXT")
    H = helpers()
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    package = H.ordinary(Path(args.package), directory=True)
    need(output.is_relative_to(LOCAL) and package.is_relative_to(LOCAL) and
         not output.is_relative_to(package) and not package.is_relative_to(output),
         "EXACT_PUBLIC_PATHS")
    profile, profile_pin = H.read_json(package / "PROFILE.json", args.profile_sha256, check)
    need(profile["installation_manifest_sha256"] ==
         "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2",
         "EXACT_PUBLIC_INSTALLATION")
    for logical, pin in profile["files"].items():
        H.relative(logical)
        need(H.pin(package/logical, check) == pin, "EXACT_PUBLIC_PACKAGE_PIN")
    unit_path = LOCAL / "concept-theory-b-export-01/bundle/units" / (UNIT+".json")
    unit, _ = H.read_json(unit_path, UNIT_SHA, check)
    target_name = name("RepairTheory.ClosureBridge.AllClosure")
    need(unit["semantic_id"] == SEMANTIC and len(unit["unit"][2]) == 1 and
         unit["unit"][2][0][0] == target_name, "EXACT_PUBLIC_TARGET")
    # Use the pinned stateless identity codec, not a reimplemented domain formula.
    codec = package / "installation/py/ordinary_semantics.py"
    installation, _ = H.read_json(package / "installation/INSTALLATION.json",
                                  profile["installation_manifest_sha256"], check)
    codec_pin = installation["files"]["py/ordinary_semantics.py"]
    need(H.pin(codec, check) == codec_pin, "EXACT_PUBLIC_IDENTITY_CODEC")
    # ordinary_semantics imports ordinary_evidence; their selected imports are
    # already pinned by the installation, and no owner or state API is loaded.
    for module_name in ("ordinary_evidence", "ordinary_semantics"):
        path = package / "installation/py" / (module_name+".py")
        need(module_name not in sys.modules and H.pin(path, check) ==
             installation["files"]["py/"+module_name+".py"], "EXACT_PUBLIC_CODEC_PIN")
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    target = {"name": target_name, "unit_id": UNIT,
              "export_id": sys.modules["ordinary_semantics"].export_id(SEMANTIC, UNIT, target_name)}
    sidecar = OWNER / "catalog/module-anchors-v1"
    prior = {}
    if sidecar.exists():
        H.ordinary(sidecar, directory=True)
        for path in sidecar.rglob("*"):
            check()
            H.ordinary(path, directory=path.is_dir())
            if path.is_file():
                need(len(prior) < 2048, "EXACT_PUBLIC_PRIOR_BOUND")
                prior[path.relative_to(sidecar).as_posix()] = H.pin(path, check)
    output.mkdir()
    H.fresh_bytes(output / "PRIOR-SIDECAR.json", H.canonical(prior))
    H.fresh_bytes(output / "targets.json", H.canonical([target]))
    records = []
    try:
        for label, anchor in (("cold", ""), ("warm", None)):
            check()
            if anchor is None:
                anchor = records[0]["result"]["anchor_id"]
            argv = [str(PYTHON), "-I", "-S", "-B", str(package / "owner.py"), "export-module",
                "--profile-sha256", args.profile_sha256, "--python-runtime", str(PYTHON.parent),
                "--lean-runtime", str(LEAN), "--wall-seconds", "65", "--cpu-seconds", "35",
                "--memory-mib", "1536", "--catalog", str(OWNER / "catalog"),
                "--custody", str(OWNER / "custody"), "--store-id", STORE,
                "--custody-limits", str(H.ordinary(Path(args.custody_limits))),
                "--parent-root", CONTEXT, "--module-targets", str(output / "targets.json"),
                "--output", str(output / (label+"-module"))]
            if anchor:
                argv += ["--module-anchor", anchor]
            H.fresh_bytes(output / (label+"-COMMAND.json"), H.canonical({"argv": argv}))
            with (output/(label+"-stdout.json")).open("xb") as out, \
                    (output/(label+"-stderr.txt")).open("xb") as err:
                code = subprocess.call(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                                       stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
            need(code == 0 and (output/(label+"-stderr.txt")).stat().st_size == 0,
                 "EXACT_PUBLIC_"+label.upper()+"_FAILED")
            value, _ = H.read_json(output/(label+"-stdout.json"),
                                  H.pin(output/(label+"-stdout.json"), check, 8*MIB)["sha256"], check)
            need(value["ok"] is True and value["operation"] == "export-module" and
                 value["store_id"] == STORE and value["profile_sha256"] == args.profile_sha256,
                 "EXACT_PUBLIC_RESPONSE")
            result = value["result"]
            need(result["source_context_root"] == CONTEXT and result["targets"] == [target] and
                 result["new_catalog_acceptance"] is False, "EXACT_PUBLIC_CONTEXT_BINDING")
            if label == "cold":
                need(result["status"] == "CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR" and
                     result["units_matched"] == 4 and result["units_checked"] == 6 and
                     len(result["matched_names"]) == 9 and len(result["added_names"]) == 12 and
                     len(result["ordered_unit_ids"]) == 10 and result["native_calls"] == 1,
                     "EXACT_PUBLIC_COLD_PARTITION")
                registered = sidecar / "records" / (result["anchor_id"]+".json")
                record, _ = H.read_json(registered, H.pin(registered, check)["sha256"], check)
                tags = [unit["realization"] for unit in record["units"]]
                need(tags.count("installed-exact-nontheorem") == 4 and tags.count("added") == 6,
                     "EXACT_PUBLIC_REGISTERED_TAGS")
            else:
                need(result["status"] == "REUSED_LOCAL_MODULE_ANCHOR" and
                     result["anchor_id"] == anchor and result["native_calls"] == 0 and
                     result["fetch_calls"] == 0 and result["ordered_unit_ids"] == [],
                     "EXACT_PUBLIC_WARM_REUSE")
            records.append(value)
        need(H.pin(package / "PROFILE.json", check) == profile_pin, "EXACT_PUBLIC_PROFILE_CHANGED")
        for logical, pin in profile["files"].items():
            need(H.pin(package/logical, check) == pin, "EXACT_PUBLIC_PACKAGE_CHANGED")
        for relative, pin in prior.items():
            need(H.pin(sidecar/relative, check) == pin, "EXACT_PUBLIC_PRIOR_CHANGED")
        summary = {"status": "PASS_EXACT_MODULE_COLD_AND_REOPEN", "calls": records,
                   "prior_sidecar_files_unchanged": len(prior),
                   "wall_seconds": time.monotonic()-START,
                   "controller_cpu_seconds": time.process_time()-CPU,
                   "claim": "RETAINED_CONCEPT_MODULE_REALIZATION_NOT_QUERY_OR_GROWTH"}
        raw = H.canonical(summary)
        H.fresh_bytes(output / ".RESULT.pending", raw)
        need(H.pin(output / ".RESULT.pending", check, 8*MIB) ==
             {"bytes": len(raw), "sha256": H.digest(raw)}, "EXACT_PUBLIC_RESULT_READBACK")
        check()
        H.ordinary(output / "RESULT.json", fresh=True)
        (output / ".RESULT.pending").rename(output / "RESULT.json")
        print(json.dumps({"status": summary["status"]}), flush=True)
    except BaseException as error:
        H.fresh_bytes(output / "FAILURE.json", H.canonical({"error_type": type(error).__name__,
            "error": str(error)[:1000], "completed_calls": len(records),
            "retention": "PRESERVED_NO_RETRY"}))
        raise


if __name__ == "__main__":
    main()
