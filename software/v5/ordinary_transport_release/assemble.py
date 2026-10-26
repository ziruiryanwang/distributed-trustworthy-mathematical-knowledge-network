"""File-only transport overlay for an explicitly approved supported sparse build.

Stable source/runtime/layout bindings are fixed; generated native identities are
selected by the owner. No product import, compilation, state or network access.
Immutable owner-controlled inputs are a premise. Output is fresh, retained on
failure and PROFILE-last. Run on supported Windows Python using -I -S -B.
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
PREFIX = "software/v5/ordinary_transport_release/"
TRANSPORT = "software/v5/ordinary_bounded_transport/"
COMPATIBILITY = "software/v5/ordinary_network_kit/compatibility.json"
COMPATIBILITY_SHA = "feb7e1582f22e8f1f9642ff504053d08513be5c5818667053b63d5c9721cb5c4"
SOURCE_MAP = "software/v5/ordinary_bounded_operations/source-map.json"
SOURCE_MAP_SHA = "e9b7a873c8e509651833de51e5bd6beda130c74fdf7391859a8661c08426396a"
PAYLOADS = {
    "support/transport/http_provider.py": TRANSPORT + "http_provider.py",
    "BOUNDED-TRANSPORT.md": PREFIX + "README.md",
    "EXECUTION-TRUST.md": TRANSPORT + "EXECUTION-TRUST.md",
}
BASE_ASSEMBLER = {"bytes": 10828,
    "sha256": "3c2a197e0ca159a9472ad3535897d7bd2098399cd43efc104871d63abcb10b71"}
BASE_OVERLAY = {"bytes": 1483,
    "sha256": "e8c14ecee1ba1a95c5ff195e00346d4682e244820dc10300711fe3cc13c8987f"}
BASE_CHANGED = {
    "peer.py", "peer_api.py", "profile.py", "README.md", "SPARSE-SEARCH.md",
    "support/transport/http_provider.py", "support/transport/fair_exchange.py",
    "support/discovery/fair_search.py", "support/discovery/search_session.py",
    "support/discovery/discovery_store.py", "support/discovery/candidate_query.py",
    "support/discovery/pair_access.py",
}
BASE_DOCUMENT_UPDATES = {
    "README.md": {"bytes": 9660, "sha256": "f8726c4ea578f8d0bc6ece890762dcf13ed1cb74da67f9b5f1d0a8e496661a42"},
    "CONTACTS.md": {"bytes": 7722, "sha256": "33e80a998926ed51b6348e6c308571a0e880a0ec69bad97129434a6720608bc2"},
    "SPARSE-SEARCH.md": {"bytes": 4868, "sha256": "fe5e3c823a418e7d63da9d9741fc7175197641d22b52e81fd4ec48fa504a9cef"},
}
# Same nine named-runtime pins as the pinned ordinary_package/build.py in the
# bounded source map. These are not the map's fourteen compiler/linker inputs.
RUNTIME_PINS = {
    "python_runtime/python.exe": {"bytes": 106208, "sha256": "03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38"},
    "python_runtime/python314.dll": {"bytes": 6778592, "sha256": "fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0"},
    "python_runtime/python3.dll": {"bytes": 73952, "sha256": "22c6e46d8bd563cdb072650901461ef68be2ea6cb1e80af859559d9395a27e39"},
    "lean_runtime/bin/lean.exe": {"bytes": 83456, "sha256": "a8040e2cab341c12116ab591fed9f761816f5f6b08554f6cc1680e86dfbba0a2"},
    "lean_runtime/bin/libInit_shared.dll": {"bytes": 28345856, "sha256": "841b87dfdfb81be44d03720039d123cac50e9b3e2461ff50753f77ba2c7a0b8f"},
    "lean_runtime/bin/libc++.dll": {"bytes": 1659392, "sha256": "8a9deaac6d2f4d2de468a544d1f35cd0dd4bcde03cda3cfb76fb9674749828d4"},
    "lean_runtime/bin/libleanshared.dll": {"bytes": 70414848, "sha256": "002995f741bab9497ff7ecd18be469ddd5dd7d0833037d6f434084d36138f2cd"},
    "lean_runtime/bin/libleanshared_1.dll": {"bytes": 52662272, "sha256": "15d171f935fc65a394049af4b027818891fa271821c3a5524a2fdc7688ecfa45"},
    "lean_runtime/bin/libleanshared_2.dll": {"bytes": 59422720, "sha256": "bdbb5b6c62d4530c296a05828f1a9a0c9f52ad7da5d17efd2b1cba505468355b"},
}
ROLES = {
    "python": "python_runtime/python.exe", "python_dll": "python_runtime/python314.dll",
    "python_stable_dll": "python_runtime/python3.dll", "lean": "lean_runtime/bin/lean.exe",
    "worker": "lean-src/OrdinaryWorkflowWorker.lean", "seed": "foundation/seed.json",
    "inventory": "foundation/inventory.json", "supervisor": "supervisor/commons.py",
    "job": "supervisor/run_stage.py", "domains": "supervisor/domains.py",
    "core": "py/ordinary_admission.py", "evidence": "py/ordinary_evidence.py",
    "semantics": "py/ordinary_semantics.py", "portable_evidence": "py/portable_evidence.py",
    "catalog": "py/portable_catalog.py", "legacy_catalog": "py/local_catalog.py",
}
IMPLEMENTATION_FIXED = {
    "schema": "DMKN_ORDINARY_IMPLEMENTATION_CLAIM_V1",
    "semantic_id": "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7",
    "platform": {"os": "windows", "architecture": "x86_64", "word_bits": 64, "byte_order": "little"},
    "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
    "support_scope": "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN",
}


def helper(root):
    # Approved source root and immutable owner-controlled filesystem are premises.
    path = root / HELPER
    with path.open("rb") as stream:
        raw = stream.read(2 * 1024**2 + 1)
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("TRANSPORT_RELEASE_HELPER_PIN")
    name = "_transport_release_assembly_files"
    if name in sys.modules:
        raise ValueError("TRANSPORT_RELEASE_PRELOADED_HELPER")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def validate_base_interface(H, profile, receipt, installation, compatibility,
                            source_map, *, profile_sha256):
    """Pure metadata compatibility, not compilation or mathematical acceptance.

    Caller must first pin/read actual profile/receipt/installation bytes and the
    two exact companion maps. Generated identities remain owner-approved claims.
    No runtime is read or executed; even coherent synthetic native pins prove
    only this metadata predicate. H is the selected frozen file-helper module.
    """
    H.hexid(profile_sha256)
    H.need(type(compatibility) is dict and
           set(compatibility) == {"schema", "sparse_noncompiled", "native_roles"} and
           compatibility["schema"] == "DMKN_OPERATOR_KIT_KNOWN_NETWORK_INTERFACE_V1" and
           type(compatibility["sparse_noncompiled"]) is dict and
           type(compatibility["native_roles"]) is list and
           all(type(n) is str for n in compatibility["native_roles"]),
           "TRANSPORT_COMPATIBILITY_LAYOUT")
    stable, native = compatibility["sparse_noncompiled"], set(compatibility["native_roles"])
    expected_aux = H.BASE_AUX | {"support/transport/fair_exchange.py", "support/discovery/fair_search.py",
        "support/transport/contact_directory.py", "support/discovery/pair_access.py"}
    H.need(len(stable) == 45 and len(native) == len(compatibility["native_roles"]) == 72 and
           not set(stable) & native and set(stable) | native == expected_aux,
           "TRANSPORT_COMPATIBILITY_ROLES")
    H.need(type(profile) is dict and set(profile) == {
        "schema", "installation_manifest_sha256", "helper_paths", "author_worker", "files"} and
        profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
        profile["helper_paths"] == ["authoring/helpers"] and
        profile["author_worker"] == "author_worker.py" and
        type(profile["files"]) is dict and set(profile["files"]) == expected_aux,
        "TRANSPORT_BASE_LAYOUT")
    H.hexid(profile["installation_manifest_sha256"])
    auxiliary = {name: H.pin_shape(pin) for name, pin in profile["files"].items()}
    H.need(all(auxiliary[name] == H.pin_shape(pin) for name, pin in stable.items()),
           "TRANSPORT_STABLE_AUXILIARY_PIN")
    documents = dict(H.DOCUMENTS)
    documents.update(BASE_DOCUMENT_UPDATES)
    expected_changed = {name: (documents[name] if name.endswith(".md") else stable[name])
                        for name in BASE_CHANGED}
    H.need(type(receipt) is dict and receipt.get("status") == "ASSEMBLED_NOT_ADOPTED" and
           receipt.get("profile_sha256") == profile_sha256 and
           receipt.get("installation_manifest_sha256") == profile["installation_manifest_sha256"] and
           receipt.get("assembler") == BASE_ASSEMBLER and receipt.get("overlay") == BASE_OVERLAY and
           type(receipt.get("files_excluding_profile")) is int and receipt["files_excluding_profile"] == 151 and
           type(receipt.get("auxiliary_files")) is int and receipt["auxiliary_files"] == 117 and
           type(receipt.get("unchanged_payloads")) is int and receipt["unchanged_payloads"] == 139 and
           receipt.get("documentation_files") == documents and
           receipt.get("changed_or_added") == expected_changed and
           receipt.get("claim") == "FILE_ONLY_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE",
           "TRANSPORT_BASE_RECEIPT")
    H.hexid(receipt.get("base_profile_sha256"))
    H.pin_shape(receipt.get("base_receipt"))
    H.need(type(source_map) is dict and
           source_map.get("schema") == "DMKN_ORDINARY_DISTRIBUTION_SOURCE_MAP_V1" and
           type(source_map.get("copies")) is dict and type(source_map.get("sources")) is dict,
           "TRANSPORT_SOURCE_MAP_LAYOUT")
    copied = {}
    for name, source in source_map["copies"].items():
        H.need(type(name) is str, "TRANSPORT_SOURCE_MAP_NAME")
        if name.startswith("installation/"):
            H.need(type(source) is str and source in source_map["sources"], "TRANSPORT_SOURCE_MAP_PIN")
            copied[name.removeprefix("installation/")] = H.pin_shape(source_map["sources"][source])
    compiled = {"lean-lib/" + name + ".olean" for name in H.INST_NATIVE}
    H.need(len(copied) == 19 and len(compiled) == 8 and not set(copied) & compiled and
           set(copied) | compiled == H.INST_FILES and set(RUNTIME_PINS) == H.RUNTIME_FILES,
           "TRANSPORT_INSTALLATION_ROLE_PARTITION")
    H.need(type(installation) is dict and set(installation) == {
        "schema", "implementation", "roles", "compiled_dirs", "support_groups", "files"} and
        installation["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
        type(installation["files"]) is dict and
        set(installation["files"]) == H.INST_FILES | H.RUNTIME_FILES,
        "TRANSPORT_INSTALLATION_LAYOUT")
    installed = {name: H.pin_shape(pin) for name, pin in installation["files"].items()}
    H.need(all(installed[name] == pin for name, pin in copied.items()), "TRANSPORT_INSTALLATION_SOURCE_PIN")
    H.need(all(installed[name] == pin for name, pin in RUNTIME_PINS.items()), "TRANSPORT_RUNTIME_PIN")
    compiled_dirs = {"lean-lib": sorted(name + ".olean" for name in H.INST_NATIVE)}
    groups = {
        "kernel_support": sorted(name for name in RUNTIME_PINS if name.startswith("lean_runtime/")),
        "adapter_support": sorted(name for name in H.INST_FILES if name.startswith(("lean-lib/", "lean-src/"))),
        "basis_receiver_support": sorted({"foundation/seed.json", "foundation/inventory.json"} |
            {folder + name + suffix for folder, suffix in (("lean-src/", ".lean"), ("lean-lib/", ".olean"))
             for name in ("BootstrapSupport", "BasisSnapshot")}),
        "snapshot_support": ["lean-lib/LocalSnapshot.olean", "lean-src/LocalSnapshot.lean"],
        "controller_support": sorted(name for name in installed if name.startswith(("py/", "supervisor/", "python_runtime/"))),
    }
    H.need(installation["roles"] == ROLES and installation["compiled_dirs"] == compiled_dirs and
           installation["support_groups"] == groups, "TRANSPORT_INSTALLATION_BINDINGS")
    implementation = installation["implementation"]
    H.need(type(implementation) is dict and set(implementation) == set(IMPLEMENTATION_FIXED) | set(groups) and
           all(implementation[key] == value for key, value in IMPLEMENTATION_FIXED.items()) and
           type(implementation["platform"]["word_bits"]) is int,
           "TRANSPORT_IMPLEMENTATION_LAYOUT")
    for field, names in groups.items():
        value = {"field": field, "files": {name: installed[name] for name in names}}
        if field == "controller_support":
            value.update(roles=ROLES, compiled_dirs=compiled_dirs)
        expected = H.digest(b"DMKN-ORDINARY-INSTALLED-SUPPORT-V1\0" + H.canonical(value))
        H.need(implementation[field] == expected, "TRANSPORT_IMPLEMENTATION_SUPPORT")
    implementation_id = H.digest(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0" + H.canonical(implementation))
    return {"auxiliary": auxiliary,
            "installation_files": {name: installed[name] for name in H.INST_FILES},
            "documents": documents, "implementation_id": implementation_id}


def assemble(args):
    start, cpu = time.monotonic(), time.process_time()
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
            sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("TRANSPORT_RELEASE_ISOLATED_WINDOWS_PROFILE")
    root = Path(args.source_root)
    if not root.is_absolute() or not (1 <= args.wall_seconds <= 600 and 1 <= args.cpu_seconds <= 600):
        raise ValueError("TRANSPORT_RELEASE_SELECTION")
    H = helper(root)
    def check():
        H.need(time.monotonic() - start < args.wall_seconds and
               time.process_time() - cpu < args.cpu_seconds, "TRANSPORT_ORIGINAL_ALLOWANCE")
    root = H.ordinary(root, directory=True)
    H.need(H.pin(root / HELPER, check)["sha256"] == HELPER_SHA, "HELPER_PATH_PIN")
    base = H.ordinary(Path(args.base_package), directory=True)
    receipt_path = H.ordinary(Path(args.base_receipt))
    selection_path = H.ordinary(Path(args.overlay))
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(not output.is_relative_to(base) and not base.is_relative_to(output) and
           not root.is_relative_to(output) and not output.is_relative_to(root / PREFIX) and
           not output.is_relative_to(root / TRANSPORT) and
           not receipt_path.is_relative_to(output) and not selection_path.is_relative_to(output),
           "TRANSPORT_OUTPUT_OVERLAP")
    old, old_pin = H.read_json(base / "PROFILE.json", args.base_profile_sha256, check)
    receipt, receipt_pin = H.read_json(receipt_path, args.base_receipt_sha256, check)
    selection, selection_pin = H.read_json(selection_path, args.overlay_sha256, check)
    compatibility, compatibility_pin = H.read_json(root / COMPATIBILITY, COMPATIBILITY_SHA, check)
    source_map, source_map_pin = H.read_json(root / SOURCE_MAP, SOURCE_MAP_SHA, check)
    H.need(type(old.get("installation_manifest_sha256")) is str, "TRANSPORT_INSTALLATION_SELECTION")
    installation, install_pin = H.read_json(base / "installation/INSTALLATION.json",
                                           old["installation_manifest_sha256"], check)
    validated = validate_base_interface(H, old, receipt, installation, compatibility,
                                        source_map, profile_sha256=args.base_profile_sha256)
    baseline = dict(validated["auxiliary"])
    baseline.update({"installation/" + name: pin for name, pin in validated["installation_files"].items()})
    documents = validated["documents"]
    baseline.update(documents)
    baseline.update({"PROFILE.json": old_pin, "installation/INSTALLATION.json": install_pin})
    H.need(len(baseline) == 152 and sum(H.pin_shape(p)["bytes"] for p in baseline.values())
           <= 768 * H.MIB, "TRANSPORT_BASE_BOUND")
    H.census(base, baseline, check)
    for name, expected in baseline.items():
        H.need(H.pin(base / name, check) == expected, "TRANSPORT_BASE_PIN")
    H.need(set(selection) == {"schema", "files"} and
           selection["schema"] == "DMKN_ORDINARY_BOUNDED_TRANSPORT_OVERLAY_V1" and
           type(selection["files"]) is dict and set(selection["files"]) == set(PAYLOADS),
           "TRANSPORT_OVERLAY_LAYOUT")
    chosen = {name: (base / name, pin) for name, pin in baseline.items() if name != "PROFILE.json"}
    for logical, source_name in PAYLOADS.items():
        pin = H.pin_shape(selection["files"][logical])
        source = root / source_name
        H.need(H.pin(source, check, 2 * H.MIB) == pin, "TRANSPORT_OVERLAY_PIN")
        chosen[logical] = (source, pin)
    auxiliary = dict(validated["auxiliary"])
    auxiliary.update({name: chosen[name][1] for name in PAYLOADS if not name.endswith(".md")})
    descriptor = dict(old, files=auxiliary)
    raw_profile = H.canonical(descriptor)
    own_pin = H.pin(Path(__file__).absolute(), check, 2 * H.MIB)
    H.need(H.pin(root / PREFIX / "assemble.py", check, 2 * H.MIB) == own_pin, "TRANSPORT_RUNNING_SOURCE")
    H.need(len(chosen) == 153 and len(auxiliary) == 117 and
           sum(pin["bytes"] for _, pin in chosen.values()) <= 768 * H.MIB, "TRANSPORT_OUTPUT_BOUND")
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
                    H.need(count <= expected["bytes"], "TRANSPORT_SOURCE_GREW")
                    digest.update(block); out.write(block)
                out.flush(); os.fsync(out.fileno())
            H.need(count == expected["bytes"] and digest.hexdigest() == expected["sha256"], "TRANSPORT_COPY_PIN")
        phase = "FINAL_MAP"
        H.census(base, baseline, check)
        for name, pin in baseline.items():
            H.need(H.pin(base / name, check) == pin, "TRANSPORT_BASE_CHANGED")
        for name, (source, pin) in chosen.items():
            H.need(H.pin(source, check) == pin and H.pin(package / name, check) == pin, "TRANSPORT_FINAL_PIN")
        H.need(H.pin(receipt_path, check) == receipt_pin and H.pin(selection_path, check) == selection_pin and
               H.pin(Path(__file__).absolute(), check) == own_pin and
               H.pin(root / HELPER, check)["sha256"] == HELPER_SHA and
               H.pin(root / COMPATIBILITY, check) == compatibility_pin and
               H.pin(root / SOURCE_MAP, check) == source_map_pin, "TRANSPORT_SELECTION_CHANGED")
        H.census(package, chosen, check)
        phase = "PROFILE_COMMIT"
        H.fresh_bytes(package / ".PROFILE.pending", raw_profile)
        check(); H.ordinary(package / "PROFILE.json", fresh=True)
        (package / ".PROFILE.pending").rename(package / "PROFILE.json")
        H.census(package, set(chosen) | {"PROFILE.json"}, check)
        H.need(H.pin(package / "PROFILE.json", check) ==
               {"bytes": len(raw_profile), "sha256": H.digest(raw_profile)}, "TRANSPORT_PROFILE_PIN")
        result = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package),
            "base_profile_sha256": args.base_profile_sha256, "base_receipt": receipt_pin,
            "overlay": selection_pin, "assembler": own_pin,
            "profile_sha256": H.digest(raw_profile),
            "installation_manifest_sha256": old["installation_manifest_sha256"],
            "implementation_id": validated["implementation_id"],
            "files_excluding_profile": len(chosen), "auxiliary_files": len(auxiliary),
            "changed_or_added": selection["files"],
            "documentation_files": {name: chosen[name][1] for name in set(documents) | {"BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}},
            "unchanged_payloads": sum(name not in PAYLOADS for name in baseline if name != "PROFILE.json"),
            "wall_seconds": time.monotonic() - start, "cpu_seconds": time.process_time() - cpu,
            "claim": "FILE_ONLY_NO_NATIVE_BUILD_STATE_OR_MATHEMATICAL_ACCEPTANCE"}
        H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(result))
        check()
        return result
    except BaseException as error:
        try:
            H.fresh_bytes(output / "ASSEMBLY-FAILURE.json", H.canonical({"phase": phase,
                "error_type": type(error).__name__, "error": str(error)[:1000],
                "retention": "PRESERVED_NO_AUTOMATIC_RETRY"}))
        except BaseException:
            pass  # Preserve the original failure even when diagnostics cannot be saved.
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("source-root", "base-package", "base-profile-sha256", "base-receipt",
                "base-receipt-sha256", "overlay", "overlay-sha256", "output"):
        parser.add_argument("--" + key, required=True)
    for key in ("wall-seconds", "cpu-seconds"):
        parser.add_argument("--" + key, type=int, required=True)
    print(json.dumps(assemble(parser.parse_args()), sort_keys=True))
