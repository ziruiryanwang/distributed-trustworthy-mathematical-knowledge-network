"""File-only bounded-transport overlay; no product import, native build or state.

Reuse the frozen fair assembler's bounded file helpers under an exact source pin.
The baseline/receipt/overlay selection is owner-approved, not a downloaded trust
root. Output is fresh, failure is retained, and PROFILE commits last.
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
PREFIX = "software/v5/ordinary_bounded_transport/"
PAYLOADS = {
    "support/transport/http_provider.py": "http_provider.py",
    "BOUNDED-TRANSPORT.md": "README.md",
    "EXECUTION-TRUST.md": "EXECUTION-TRUST.md",
}
BASE_ASSEMBLER_SHA = "3c2a197e0ca159a9472ad3535897d7bd2098399cd43efc104871d63abcb10b71"
BASE_PROFILE_SHA = "97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834"
BASE_INSTALLATION_SHA = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
BASE_RECEIPT_SHA = "b138a6402a921ea1b7690a805cdab5d6bef2a3484659ff970eb4726dc90ba1a8"
BASE_DOCUMENTS = {"README.md", "PRODUCER.md", "LAUNCHER.md",
                  "RECEIVE-POLICY.md", "CONTACTS.md", "SPARSE-SEARCH.md"}



def helper(root):
    # Approved source root and immutable owner-controlled filesystem are premises.
    path = root/HELPER
    with path.open("rb") as stream:
        raw = stream.read(2*1024**2+1)
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("TRANSPORT_ASSEMBLY_HELPER_PIN")
    name = "_bounded_transport_assembly_files"
    if name in sys.modules:
        raise ValueError("TRANSPORT_ASSEMBLY_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def assemble(args):
    start, cpu = time.monotonic(), time.process_time()
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("TRANSPORT_ASSEMBLY_ISOLATED_WINDOWS_PROFILE")
    root = Path(args.source_root)
    if not root.is_absolute() or not (1 <= args.wall_seconds <= 600 and 1 <= args.cpu_seconds <= 600):
        raise ValueError("TRANSPORT_ASSEMBLY_SELECTION")
    if args.base_profile_sha256 != BASE_PROFILE_SHA or args.base_receipt_sha256 != BASE_RECEIPT_SHA:
        raise ValueError("TRANSPORT_EXACT_SPARSE_BASE_REQUIRED")
    H = helper(root)
    def check():
        H.need(time.monotonic()-start < args.wall_seconds and
               time.process_time()-cpu < args.cpu_seconds, "TRANSPORT_ORIGINAL_ALLOWANCE")
    root = H.ordinary(root, directory=True)
    H.need(H.pin(root/HELPER, check)["sha256"] == HELPER_SHA, "HELPER_PATH_PIN")
    base = H.ordinary(Path(args.base_package), directory=True)
    receipt_path = H.ordinary(Path(args.base_receipt))
    selection_path = H.ordinary(Path(args.overlay))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(not output.is_relative_to(base) and not base.is_relative_to(output) and
           not root.is_relative_to(output) and not output.is_relative_to(root/PREFIX) and
           not receipt_path.is_relative_to(output) and not selection_path.is_relative_to(output),
           "TRANSPORT_OUTPUT_OVERLAP")
    old, old_pin = H.read_json(base/"PROFILE.json", args.base_profile_sha256, check)
    receipt, receipt_pin = H.read_json(receipt_path, args.base_receipt_sha256, check)
    selection, selection_pin = H.read_json(selection_path, args.overlay_sha256, check)
    expected_aux = H.BASE_AUX | {"support/transport/fair_exchange.py", "support/discovery/fair_search.py",
                                 "support/transport/contact_directory.py",
                                 "support/discovery/pair_access.py"}
    H.need(set(old) == {"schema", "installation_manifest_sha256", "helper_paths", "author_worker", "files"}
           and old["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
           old["helper_paths"] == ["authoring/helpers"] and old["author_worker"] == "author_worker.py" and
           type(old["files"]) is dict and set(old["files"]) == expected_aux and
           len(expected_aux) == 117 and old["installation_manifest_sha256"] == BASE_INSTALLATION_SHA, "TRANSPORT_BASE_LAYOUT")
    H.need(receipt.get("status") == "ASSEMBLED_NOT_ADOPTED" and
           receipt.get("profile_sha256") == args.base_profile_sha256 and
           receipt.get("installation_manifest_sha256") == old["installation_manifest_sha256"] and
           receipt.get("assembler", {}).get("sha256") == BASE_ASSEMBLER_SHA and
           receipt.get("files_excluding_profile") == 151 and receipt.get("auxiliary_files") == 117 and
           type(receipt.get("documentation_files")) is dict and
           set(receipt["documentation_files"]) == BASE_DOCUMENTS, "TRANSPORT_BASE_RECEIPT")
    installation, install_pin = H.read_json(base/"installation/INSTALLATION.json",
                                           old["installation_manifest_sha256"], check)
    H.need(installation.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
           type(installation.get("files")) is dict and
           set(installation["files"]) == H.INST_FILES | H.RUNTIME_FILES,
           "TRANSPORT_INSTALLATION_LAYOUT")
    for pin in installation["files"].values():
        H.pin_shape(pin)  # External runtime pins stay inert; no runtime is opened.
    baseline = dict(old["files"])
    baseline.update({"installation/"+name: pin for name, pin in installation["files"].items()
                     if name in H.INST_FILES})
    documents = {name: H.pin_shape(pin) for name, pin in receipt["documentation_files"].items()}
    baseline.update(documents)
    baseline.update({"PROFILE.json": old_pin, "installation/INSTALLATION.json": install_pin})
    H.need(len(baseline) == 152 and sum(H.pin_shape(p)["bytes"] for p in baseline.values())
           <= 768*H.MIB, "TRANSPORT_BASE_BOUND")
    H.census(base, baseline, check)
    for name, expected in baseline.items():
        H.need(H.pin(base/name, check) == expected, "TRANSPORT_BASE_PIN")
    H.need(set(selection) == {"schema", "files"} and
           selection["schema"] == "DMKN_ORDINARY_BOUNDED_TRANSPORT_OVERLAY_V1" and
           set(selection["files"]) == set(PAYLOADS), "TRANSPORT_OVERLAY_LAYOUT")
    chosen = {name: (base/name, pin) for name, pin in baseline.items() if name != "PROFILE.json"}
    for logical, filename in PAYLOADS.items():
        pin = H.pin_shape(selection["files"][logical])
        source = root/PREFIX/filename
        H.need(H.pin(source, check, 2*H.MIB) == pin, "TRANSPORT_OVERLAY_PIN")
        chosen[logical] = (source, pin)
    auxiliary = dict(old["files"])
    auxiliary.update({name: chosen[name][1] for name in PAYLOADS if not name.endswith(".md")})
    descriptor = dict(old, files=auxiliary)
    raw_profile = H.canonical(descriptor)
    own_pin = H.pin(Path(__file__).absolute(), check, 2*H.MIB)
    H.need(H.pin(root/PREFIX/"assemble.py", check, 2*H.MIB) == own_pin,
           "TRANSPORT_RUNNING_SOURCE")
    H.need(len(chosen) == 153 and len(auxiliary) == 117 and
           sum(pin["bytes"] for _, pin in chosen.values()) <= 768*H.MIB, "TRANSPORT_OUTPUT_BOUND")
    output.mkdir()
    package, phase = output/"package", "COPY"
    try:
        package.mkdir()
        for name, (source, expected) in sorted(chosen.items()):
            check(); target = package/H.relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            H.ordinary(target.parent, directory=True)
            count, digest = 0, hashlib.sha256()
            with H.ordinary(source).open("rb") as inp, H.ordinary(target, fresh=True).open("xb") as out:
                while block := inp.read(H.MIB):
                    check(); count += len(block)
                    H.need(count <= expected["bytes"], "TRANSPORT_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            H.need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                   "TRANSPORT_COPY_PIN")
        phase = "FINAL_MAP"
        H.census(base, baseline, check)
        for name, pin in baseline.items():
            H.need(H.pin(base/name, check) == pin, "TRANSPORT_BASE_CHANGED")
        for name, (source, pin) in chosen.items():
            H.need(H.pin(source, check) == pin and H.pin(package/name, check) == pin,
                   "TRANSPORT_FINAL_PIN")
        H.need(H.pin(receipt_path, check) == receipt_pin and
               H.pin(selection_path, check) == selection_pin and
               H.pin(Path(__file__).absolute(), check) == own_pin and
               H.pin(root/HELPER, check)["sha256"] == HELPER_SHA, "TRANSPORT_SELECTION_CHANGED")
        H.census(package, chosen, check)
        phase = "PROFILE_COMMIT"
        H.fresh_bytes(package/".PROFILE.pending", raw_profile)
        check(); H.ordinary(package/"PROFILE.json", fresh=True)
        (package/".PROFILE.pending").rename(package/"PROFILE.json")
        H.census(package, set(chosen)|{"PROFILE.json"}, check)
        H.need(H.pin(package/"PROFILE.json", check) ==
               {"bytes": len(raw_profile), "sha256": H.digest(raw_profile)}, "TRANSPORT_PROFILE_PIN")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package),
            "base_profile_sha256": args.base_profile_sha256, "base_receipt": receipt_pin,
            "overlay": selection_pin, "assembler": own_pin,
            "profile_sha256": H.digest(raw_profile),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "files_excluding_profile": len(chosen), "auxiliary_files": len(auxiliary),
            "changed_or_added": selection["files"],
            "documentation_files": {name: chosen[name][1] for name in set(documents)|{"BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}},
            "unchanged_payloads": sum(name not in PAYLOADS for name in baseline if name != "PROFILE.json"),
            "wall_seconds": time.monotonic()-start, "cpu_seconds": time.process_time()-cpu,
            "claim": "FILE_ONLY_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        H.fresh_bytes(output/"ASSEMBLY.json", H.canonical(result))
        check()
        return result
    except BaseException as error:
        try:
            H.fresh_bytes(output/"ASSEMBLY-FAILURE.json", H.canonical({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:1000],
                "retention": "PRESERVED_NO_AUTOMATIC_RETRY"}))
        except BaseException:
            pass  # Preserve the original failure, even if diagnostics cannot be saved.
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "base-package", "base-profile-sha256", "base-receipt",
                "base-receipt-sha256", "overlay", "overlay-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--"+key, type=int, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True))
