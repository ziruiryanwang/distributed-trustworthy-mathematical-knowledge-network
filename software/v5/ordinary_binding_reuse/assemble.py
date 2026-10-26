"""One reviewed binder overlay; file-only, fresh output, no product imports."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
BASE_PROFILE = "ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67"
BASE_RECEIPT = "ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c"
BASE_INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
TARGET = "reference/baseline_bundle.py"
OLD_BINDER = "d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce"
SUCCESSOR = "software/v5/ordinary_binding_reuse/baseline_bundle.py"
SUCCESSOR_SHA = "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6"
DOCUMENTS = {"README.md", "LAUNCHER.md", "PRODUCER.md", "RECEIVE-POLICY.md",
             "CONTACTS.md", "SPARSE-SEARCH.md", "BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("BINDING_ASSEMBLY_ISOLATED_WINDOWS")
    root = Path(args.source_root)
    if not root.is_absolute() or not (1 <= args.wall_seconds <= 600 and 1 <= args.cpu_seconds <= 600):
        raise ValueError("BINDING_ASSEMBLY_SELECTION")
    helper_path = root / HELPER
    with helper_path.open("rb") as stream:
        raw = stream.read(2 * 1024**2 + 1)
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("BINDING_ASSEMBLY_HELPER_PIN")
    name = "_binding_overlay_files"
    if name in sys.modules:
        raise ValueError("BINDING_ASSEMBLY_HELPER_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, helper_path)
    H = importlib.util.module_from_spec(spec)
    sys.modules[name] = H
    exec(compile(raw, str(helper_path), "exec"), H.__dict__)

    def check():
        H.need(time.monotonic()-started < args.wall_seconds and
               time.process_time()-cpu < args.cpu_seconds, "BINDING_ALLOWANCE")

    root = H.ordinary(root, directory=True)
    helper_pin = H.pin(helper_path, check, 2*H.MIB)
    H.need(helper_pin["sha256"] == HELPER_SHA, "BINDING_HELPER_CHANGED")
    base = H.ordinary(Path(args.base_package), directory=True)
    receipt_path = H.ordinary(Path(args.base_assembly))
    successor = H.ordinary(Path(args.successor) if args.successor is not None else root/SUCCESSOR)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(not root.is_relative_to(output), "BINDING_OUTPUT_ROOT_OVERLAP")
    for selected in (base, receipt_path, successor, helper_path, Path(__file__).absolute().parent):
        H.need(not output.is_relative_to(selected) and not selected.is_relative_to(output),
               "BINDING_OUTPUT_OVERLAP")
    old, old_pin = H.read_json(base/"PROFILE.json", BASE_PROFILE, check)
    receipt, receipt_pin = H.read_json(receipt_path, BASE_RECEIPT, check)
    H.need(old["installation_manifest_sha256"] == BASE_INSTALLATION and
           receipt["profile_sha256"] == BASE_PROFILE and receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
           receipt["installation_manifest_sha256"] == BASE_INSTALLATION and
           receipt["auxiliary_files"] == 117 and receipt["files_excluding_profile"] == 153 and
           set(receipt["documentation_files"]) == DOCUMENTS, "BINDING_BASE_LAYOUT")
    installation, install_pin = H.read_json(base/"installation/INSTALLATION.json", BASE_INSTALLATION, check)
    H.need(set(installation["files"]) == H.INST_FILES | H.RUNTIME_FILES and
           len(old["files"]) == 117, "BINDING_BASE_ROLES")
    baseline = {path: H.pin_shape(pin) for path, pin in old["files"].items()}
    baseline.update({"installation/"+path: H.pin_shape(pin)
                     for path, pin in installation["files"].items() if path in H.INST_FILES})
    baseline.update({path: H.pin_shape(pin) for path, pin in receipt["documentation_files"].items()})
    baseline.update({"PROFILE.json": old_pin, "installation/INSTALLATION.json": install_pin})
    H.need(len(baseline) == 154 and baseline[TARGET]["sha256"] == OLD_BINDER and
           sum(pin["bytes"] for pin in baseline.values()) <= 768*H.MIB, "BINDING_BASE_MAP")
    H.census(base, baseline, check)
    for path, pin in baseline.items():
        H.relative(path)
        H.need(H.pin(base/path, check) == pin, "BINDING_BASE_PIN")
    new_pin = H.pin(successor, check, 2*H.MIB)
    H.need(new_pin["sha256"] == H.hexid(args.successor_sha256) == SUCCESSOR_SHA and
           new_pin != baseline[TARGET],
           "BINDING_SUCCESSOR_PIN")
    own_pin = H.pin(Path(__file__).absolute(), check, 2*H.MIB)
    files = dict(old["files"], **{TARGET: new_pin})
    profile_raw = H.canonical(dict(old, files=files))
    profile_pin = {"bytes": len(profile_raw), "sha256": H.digest(profile_raw)}
    final_map = dict(baseline, **{TARGET: new_pin, "PROFILE.json": profile_pin})
    H.need({path for path in baseline if baseline[path] != final_map[path]} ==
           {TARGET, "PROFILE.json"}, "BINDING_EXACT_DELTA")
    output.mkdir()
    package, phase = output/"package", "COPY"
    try:
        package.mkdir()
        for path in sorted(set(baseline)-{"PROFILE.json"}):
            check()
            source = successor if path == TARGET else base/path
            target = package/H.relative(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            copied = 0
            with H.ordinary(source).open("rb") as inp, H.ordinary(target, fresh=True).open("xb") as out:
                while block := inp.read(H.MIB):
                    check(); copied += len(block)
                    H.need(copied <= final_map[path]["bytes"], "BINDING_SOURCE_GREW")
                    out.write(block)
                out.flush(); os.fsync(out.fileno())
            H.need(H.pin(target, check) == final_map[path], "BINDING_COPY_PIN")
        phase = "FINAL_MAP"
        H.census(base, baseline, check)
        H.census(package, set(baseline)-{"PROFILE.json"}, check)
        for path, pin in baseline.items():
            H.need(H.pin(base/path, check) == pin, "BINDING_BASE_CHANGED")
        for path in set(baseline)-{"PROFILE.json"}:
            H.need(H.pin(package/path, check) == final_map[path], "BINDING_OUTPUT_CHANGED")
        for path, pin in ((receipt_path, receipt_pin), (successor, new_pin),
                          (helper_path, helper_pin), (Path(__file__).absolute(), own_pin)):
            H.need(H.pin(path, check) == pin, "BINDING_SELECTED_INPUT_CHANGED")
        phase = "PROFILE_COMMIT"
        pending = package/".PROFILE.pending"
        H.fresh_bytes(pending, profile_raw)
        H.need(H.pin(pending, check) == profile_pin, "BINDING_PENDING_PROFILE")
        check(); H.ordinary(package/"PROFILE.json", fresh=True)
        pending.rename(package/"PROFILE.json")
        H.census(package, final_map, check)
        H.need(H.pin(package/"PROFILE.json", check) == profile_pin, "BINDING_PROFILE_PIN")
        result = {"schema": "DMKN_ORDINARY_BINDING_OVERLAY_RECEIPT_V1",
            "status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": final_map,
            "base_profile_sha256": BASE_PROFILE, "base_receipt": receipt_pin,
            "profile_sha256": profile_pin["sha256"], "installation_manifest_sha256": BASE_INSTALLATION,
            "successor": new_pin, "assembler": own_pin, "helper": helper_pin,
            "changed_files": ["PROFILE.json", TARGET], "unchanged_files": 152,
            "wall_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu,
            "claim": "FILE_ONLY_NO_NATIVE_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        H.fresh_bytes(output/"ASSEMBLY.json", H.canonical(result))
        H.read_json(output/"ASSEMBLY.json", H.digest(H.canonical(result)), check)
        return result
    except BaseException as error:
        try:
            H.fresh_bytes(output/"ASSEMBLY-FAILURE.json", H.canonical({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:1000],
                "retention": "PRESERVED_NO_AUTOMATIC_RETRY"}))
        except Exception:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "base-package", "base-assembly", "output"):
        parser.add_argument("--"+key, required=True)
    parser.add_argument("--successor", help="Optional exact reviewed source path; default is below source-root")
    parser.add_argument("--successor-sha256", default=SUCCESSOR_SHA)
    for key in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+key, type=int, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True))
