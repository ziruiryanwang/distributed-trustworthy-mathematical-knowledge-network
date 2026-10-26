"""File-only multi-source overlay of an explicitly approved exact-module package.

No product imports, compiler, state or network. The owner selects the existing
package/profile/receipt and new source overlay. Generated native identities are
preserved, not authenticated by this operation. Fresh output, PROFILE committed
last, failures retained. Immutable owner-controlled input storage is a premise.
"""
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
BASE_MAP = "software/v5/ordinary_investigator_bundle/compatibility.json"
BASE_MAP_SHA = "de4937bdcac4d9ed5550d4da9c59d4f4af4551275dcaaf9d36bc85affbddd1f0"
BASE_ASSEMBLER = {"bytes": 12326,
    "sha256": "f7d5f3496d010c591a4de3872f47ff169c30413354c2576bf670b7b30c77a82b"}
PREFIX = "software/v5/ordinary_multi_source/"
PAYLOADS = {"support/transport/http_provider.py": "http_provider.py",
            "support/transport/ordinary_acquisition.py": "ordinary_acquisition.py",
            "peer_api.py": "peer_api.py"}
DOCUMENT_NAMES = {"README.md", "LAUNCHER.md", "PRODUCER.md", "RECEIVE-POLICY.md",
                  "CONTACTS.md", "SPARSE-SEARCH.md", "BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}


def helper(root):
    path = root / HELPER
    with path.open("rb") as stream:
        raw = stream.read(2 * 1024**2 + 1)
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("MULTI_SOURCE_ASSEMBLY_HELPER_PIN")
    name = "_multi_source_assembly_files"
    if name in sys.modules:
        raise ValueError("MULTI_SOURCE_ASSEMBLY_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def base_map(H, profile, receipt, installation, compatibility, profile_sha):
    """Bound an owner-selected package map; no native correctness assertion."""
    H.need(set(profile) == {"schema", "installation_manifest_sha256", "helper_paths",
                           "author_worker", "files"} and
           profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
           profile["helper_paths"] == ["authoring/helpers"] and
           profile["author_worker"] == "author_worker.py", "MULTI_SOURCE_BASE_LAYOUT")
    H.need(set(compatibility) == {"schema", "sparse_noncompiled", "native_roles"} and
           compatibility["schema"] == "DMKN_OPERATOR_KIT_KNOWN_NETWORK_INTERFACE_V1",
           "MULTI_SOURCE_BASE_COMPATIBILITY")
    stable, native = compatibility["sparse_noncompiled"], compatibility["native_roles"]
    H.need(type(stable) is dict and len(stable) == 45 and type(native) is list and
           len(native) == len(set(native)) == 72 and not set(stable) & set(native),
           "MULTI_SOURCE_ROLE_PARTITION")
    auxiliary = profile["files"]
    H.need(type(auxiliary) is dict and set(auxiliary) == set(stable) | set(native) and
           all(auxiliary[name] == pin for name, pin in stable.items()),
           "MULTI_SOURCE_BASE_SOURCE_INTERFACE")
    H.need(installation.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
           type(installation.get("files")) is dict and
           set(installation["files"]) == H.INST_FILES | H.RUNTIME_FILES,
           "MULTI_SOURCE_INSTALLATION_LAYOUT")
    H.need(receipt.get("status") == "ASSEMBLED_NOT_ADOPTED" and
           receipt.get("assembler") == BASE_ASSEMBLER and
           receipt.get("profile_sha256") == profile_sha and
           receipt.get("installation_manifest_sha256") == profile["installation_manifest_sha256"] and
           receipt.get("auxiliary_files") == 117 and receipt.get("files_excluding_profile") == 153 and
           type(receipt.get("documentation_files")) is dict and
           set(receipt["documentation_files"]) == DOCUMENT_NAMES,
           "MULTI_SOURCE_BASE_RECEIPT")
    selected = {name: H.pin_shape(pin) for name, pin in auxiliary.items()}
    selected.update({"installation/" + name: H.pin_shape(pin)
                     for name, pin in installation["files"].items() if name in H.INST_FILES})
    selected.update({name: H.pin_shape(pin) for name, pin in receipt["documentation_files"].items()})
    H.need(len(selected) == 152, "MULTI_SOURCE_BASE_FILE_COUNT")
    for name in selected:
        H.relative(name)
    return selected


def assemble(args):
    started, cpu = time.monotonic(), time.process_time()
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("MULTI_SOURCE_ASSEMBLY_ISOLATED_WINDOWS")
    root = Path(args.source_root)
    if not root.is_absolute() or not (1 <= args.wall_seconds <= 600 and 1 <= args.cpu_seconds <= 600):
        raise ValueError("MULTI_SOURCE_ASSEMBLY_SELECTION")
    H = helper(root)
    def check():
        H.need(time.monotonic() - started < args.wall_seconds and
               time.process_time() - cpu < args.cpu_seconds, "MULTI_SOURCE_ASSEMBLY_ALLOWANCE")
    root = H.ordinary(root, directory=True)
    H.need(H.pin(root / HELPER, check)["sha256"] == HELPER_SHA, "MULTI_SOURCE_HELPER_PATH")
    base = H.ordinary(Path(args.base_package), directory=True)
    receipt_path = H.ordinary(Path(args.base_receipt))
    selection_path = H.ordinary(Path(args.overlay))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(not root.is_relative_to(output) and not output.is_relative_to(root / PREFIX) and
           not output.is_relative_to(Path(__file__).absolute().parent),
           "MULTI_SOURCE_SOURCE_OUTPUT_OVERLAP")
    for path in (base, receipt_path, selection_path):
        H.need(not output.is_relative_to(path) and not path.is_relative_to(output),
               "MULTI_SOURCE_OUTPUT_OVERLAP")
    old, old_pin = H.read_json(base / "PROFILE.json", args.base_profile_sha256, check)
    receipt, receipt_pin = H.read_json(receipt_path, args.base_receipt_sha256, check)
    selection, selection_pin = H.read_json(selection_path, args.overlay_sha256, check)
    compatibility, compatibility_pin = H.read_json(root / BASE_MAP, BASE_MAP_SHA, check)
    installation, install_pin = H.read_json(base / "installation/INSTALLATION.json",
                                            old["installation_manifest_sha256"], check)
    baseline = base_map(H, old, receipt, installation, compatibility, args.base_profile_sha256)
    baseline.update({"PROFILE.json": old_pin, "installation/INSTALLATION.json": install_pin})
    H.need(sum(pin["bytes"] for pin in baseline.values()) <= 768 * H.MIB, "MULTI_SOURCE_BASE_BYTES")
    H.census(base, baseline, check)
    for name, pin in baseline.items():
        H.need(H.pin(base / name, check) == pin, "MULTI_SOURCE_BASE_PIN")
    H.need(set(selection) == {"schema", "files"} and
           selection["schema"] == "DMKN_ORDINARY_MULTI_SOURCE_OVERLAY_V1" and
           type(selection["files"]) is dict and set(selection["files"]) == set(PAYLOADS),
           "MULTI_SOURCE_OVERLAY_LAYOUT")
    chosen = {name: (base / name, pin) for name, pin in baseline.items() if name != "PROFILE.json"}
    for logical, filename in PAYLOADS.items():
        pin = H.pin_shape(selection["files"][logical])
        source = root / PREFIX / filename
        H.need(H.pin(source, check, 2 * H.MIB) == pin, "MULTI_SOURCE_OVERLAY_PIN")
        H.need(pin != baseline[logical], "MULTI_SOURCE_OVERLAY_UNCHANGED")
        chosen[logical] = (source, pin)
    auxiliary = dict(old["files"])
    auxiliary.update({name: chosen[name][1] for name in PAYLOADS})
    descriptor = dict(old, files=auxiliary)
    raw_profile = H.canonical(descriptor)
    own_pin = H.pin(Path(__file__).absolute(), check, 2 * H.MIB)
    H.need(len(chosen) == 153 and len(auxiliary) == 117 and
           sum(pin["bytes"] for _, pin in chosen.values()) <= 768 * H.MIB,
           "MULTI_SOURCE_OUTPUT_BOUND")
    output.mkdir()
    package, phase = output / "package", "COPY"
    try:
        package.mkdir()
        for name, (source, expected) in sorted(chosen.items()):
            check(); target = package / H.relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            count, digest = 0, hashlib.sha256()
            with H.ordinary(source).open("rb") as inp, H.ordinary(target, fresh=True).open("xb") as out:
                while block := inp.read(H.MIB):
                    check(); count += len(block)
                    H.need(count <= expected["bytes"], "MULTI_SOURCE_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            H.need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                   "MULTI_SOURCE_COPY_PIN")
        phase = "FINAL_MAP"
        H.census(base, baseline, check)
        for name, pin in baseline.items():
            H.need(H.pin(base / name, check) == pin, "MULTI_SOURCE_BASE_CHANGED")
        for name, (source, pin) in chosen.items():
            H.need(H.pin(source, check) == pin and H.pin(package / name, check) == pin,
                   "MULTI_SOURCE_FINAL_PIN")
        for path, pin in ((receipt_path, receipt_pin), (selection_path, selection_pin),
                          (root / BASE_MAP, compatibility_pin), (Path(__file__).absolute(), own_pin)):
            H.need(H.pin(path, check) == pin, "MULTI_SOURCE_SELECTION_CHANGED")
        H.need(H.pin(root / HELPER, check)["sha256"] == HELPER_SHA, "MULTI_SOURCE_HELPER_CHANGED")
        H.census(package, chosen, check)
        phase = "PROFILE_COMMIT"
        H.fresh_bytes(package / ".PROFILE.pending", raw_profile)
        check(); H.ordinary(package / "PROFILE.json", fresh=True)
        (package / ".PROFILE.pending").rename(package / "PROFILE.json")
        H.census(package, set(chosen) | {"PROFILE.json"}, check)
        H.need(H.pin(package / "PROFILE.json", check) ==
               {"bytes": len(raw_profile), "sha256": H.digest(raw_profile)}, "MULTI_SOURCE_PROFILE_PIN")
        documents = dict(receipt["documentation_files"])
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package),
            "base_profile_sha256": args.base_profile_sha256, "base_receipt": receipt_pin,
            "overlay": selection_pin, "assembler": own_pin, "profile_sha256": H.digest(raw_profile),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "files_excluding_profile": len(chosen), "auxiliary_files": len(auxiliary),
            "changed_or_added": selection["files"], "documentation_files": documents,
            "unchanged_payloads": sum(name not in PAYLOADS for name in baseline if name != "PROFILE.json"),
            "wall_seconds": time.monotonic() - started, "cpu_seconds": time.process_time() - cpu,
            "claim": "FILE_ONLY_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        result_raw = H.canonical(result)
        pending = output / ".ASSEMBLY.pending"
        H.fresh_bytes(pending, result_raw)
        H.need(H.pin(pending, check, 2 * H.MIB) ==
               {"bytes": len(result_raw), "sha256": H.digest(result_raw)},
               "MULTI_SOURCE_RECEIPT_READBACK")
        check()
        H.ordinary(output / "ASSEMBLY.json", fresh=True)
        pending.rename(output / "ASSEMBLY.json")
        return result
    except BaseException as error:
        try:
            H.fresh_bytes(output / "ASSEMBLY-FAILURE.json", H.canonical({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:1000],
                "retention": "PRESERVED_NO_AUTOMATIC_RETRY"}))
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "base-package", "base-profile-sha256", "base-receipt",
                "base-receipt-sha256", "overlay", "overlay-sha256", "output"):
        parser.add_argument("--" + key, required=True)
    for key in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--" + key, type=int, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True))
