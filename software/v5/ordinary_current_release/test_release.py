"""One current source/prebuilt handoff check; no native or owner operation.

The root selects exact reviewed sources before execution. All small invalid
fixtures and partial results are retained. This does not qualify mathematics.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import zipfile

MIB = 1024**2
PREFIX = "software/v5/ordinary_current_release/"
PROFILE = "dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
BINDER = "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6"
DOCUMENTS = {"README.md", "LAUNCHER.md", "PRODUCER.md", "RECEIVE-POLICY.md",
             "CONTACTS.md", "SPARSE-SEARCH.md", "BOUNDED-TRANSPORT.md", "EXECUTION-TRUST.md"}


def need(ok, code):
    if not ok:
        raise AssertionError("CURRENT_TEST_" + code)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def pin(path):
    with path.open("rb") as stream:
        return {"bytes": path.stat().st_size,
                "sha256": hashlib.file_digest(stream, "sha256").hexdigest()}


def load(name, path):
    need(name not in sys.modules, "MODULE_COLLISION")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "package", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--release-sha256", required=True)
    args = p.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    need(all(path.is_absolute() for path in (args.source_root, args.package, args.output)) and
         not args.output.exists() and args.output.parent.is_dir(), "FRESH_ABSOLUTE_OUTPUT")
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 150 and time.process_time()-cpu < 75, "ALLOWANCE")

    release_path = args.source_root/PREFIX/"release.json"
    need(pin(release_path)["sha256"] == args.release_sha256, "RELEASE_PIN")
    mapping = json.loads(release_path.read_bytes())
    snapshot_root = Path(__file__).absolute().parents[3]
    support_pins = {source: pin(snapshot_root/source)
                   for kind in ("source", "prebuilt")
                   for source in mapping["release_support"][kind].values()}
    bundle = load("_current_release_file_check", Path(__file__).parent/"bundle.py")
    # Independent current package expectation from actual selected metadata.
    profile_path, installation_path = (args.package/"PROFILE.json",
                                      args.package/"installation/INSTALLATION.json")
    need(pin(profile_path)["sha256"] == PROFILE and
         pin(installation_path)["sha256"] == INSTALLATION, "CURRENT_IDENTITIES")
    profile = json.loads(profile_path.read_bytes())
    installation = json.loads(installation_path.read_bytes())
    expected = dict(profile["files"])
    expected.update({"installation/"+name: value for name, value in installation["files"].items()
                     if not name.startswith(("python_runtime/", "lean_runtime/"))})
    expected.update({name: pin(args.package/name) for name in DOCUMENTS})
    expected.update({"PROFILE.json": pin(profile_path),
                     "installation/INSTALLATION.json": pin(installation_path)})
    need(len(expected) == 154 and len(profile["files"]) == 117 and
         expected["reference/baseline_bundle.py"]["sha256"] == BINDER,
         "CURRENT_EXACT_ROLE_MAP")
    need(mapping["prebuilt"]["files"] == expected, "RELEASE_PREBUILT_MAP")
    for name, value in expected.items():
        check(); need(pin(args.package/name) == value, "ORIGINAL_PACKAGE:"+name)
    args.output.mkdir()
    reports, cases = {}, ["exact-current-package-map"]
    for kind in ("source", "prebuilt"):
        check()
        out = args.output/kind
        report = bundle.pack(args.source_root, out, kind=kind,
                             package=args.package if kind == "prebuilt" else None, check=check)
        saved = json.loads((out/"RECEIPT.json").read_bytes())
        need(saved == report and report["kind"] == kind, "PACK_RECEIPT:"+kind)
        for destination, source in mapping["release_support"][kind].items():
            need(report["files"][destination] == support_pins[source],
                 "REVIEWED_SUPPORT_SNAPSHOT:"+destination)
        relocated = out/"relocated"
        archive = out/report["archive_file"]
        manifest_name = report["manifest_file"]
        manifest_path = relocated/manifest_name
        need(pin(archive) == report["archive"] and pin(manifest_path) == report["manifest"],
             "PACK_TERMINAL_PINS:"+kind)
        expected_archive = dict(report["files"], **{manifest_name: report["manifest"]})
        # Independent ZIP stream readback: no second full extraction.
        with zipfile.ZipFile(archive) as z:
            rows = z.infolist()
            need(z.comment == b"" and [row.filename for row in rows] == sorted(expected_archive),
                 "ZIP_EXACT_NAMES:"+kind)
            for row in rows:
                check(); value = expected_archive[row.filename]
                need(not row.is_dir() and row.date_time == (1980, 1, 1, 0, 0, 0) and
                     row.create_system == 3 and row.external_attr == 0o100644 << 16 and
                     row.compress_type == zipfile.ZIP_STORED and row.flag_bits == 0 and
                     row.extra == row.comment == b"" and
                     row.file_size == row.compress_size == value["bytes"], "ZIP_METADATA")
                count, digest = 0, hashlib.sha256()
                with z.open(row) as stream:
                    while block := stream.read(MIB):
                        check(); count += len(block); digest.update(block)
                        need(count <= value["bytes"], "ZIP_STREAM_BOUND")
                need({"bytes": count, "sha256": digest.hexdigest()} == value, "ZIP_PAYLOAD")
                need(pin(relocated/row.filename) == value, "RELOCATED_BYTES")
        relocated_verifier = load("_current_release_verifier_"+kind, relocated/PREFIX/"bundle.py")
        verified = relocated_verifier.verify(relocated, report["manifest"]["sha256"], check=check)
        reports[kind] = {"pack": report, "verify": verified}
        cases.append(kind+"-pack-relocation-verification")

    refusals = []
    def refuses(label, expected_code, call):
        check()
        try:
            call()
        except ValueError as error:
            need(str(error) == expected_code, "WRONG_REFUSAL:"+label+":"+str(error))
            refusals.append({"case": label, "error": str(error)})
        else:
            raise AssertionError("CURRENT_TEST_MISSING_REFUSAL:"+label)

    refuses("existing-output", "SOURCE_BUNDLE_OUTPUT_EXISTS", lambda: bundle.pack(args.source_root, args.output/"source",
                                                    kind="source", check=check))
    refuses("unapproved-manifest", "CURRENT_BUNDLE_MANIFEST_PIN", lambda: bundle.verify(args.output/"source/relocated",
                                                         "0"*64, check=check))
    tiny = {"item.txt": {"bytes": 8, "sha256": hashlib.sha256(b"original").hexdigest()}}
    changed = args.output/"changed-payload"
    write(changed/"item.txt", b"modified")
    refuses("same-length-changed-payload", "CURRENT_BUNDLE_TREE_PAYLOAD:item.txt",
            lambda: bundle.check_tree(changed, tiny, check))
    extra = args.output/"extra-directory"
    write(extra/"item.txt", b"original")
    (extra/"unexpected").mkdir()
    refuses("extra-empty-directory", "SOURCE_BUNDLE_EXTRA_OR_ALIASED_DIRECTORY",
            lambda: bundle.check_tree(extra, tiny, check))
    linked = args.output/"linked-file"
    write(linked/"item.txt", b"original")
    os.link(linked/"item.txt", args.output/"retained-hardlink.txt")
    refuses("hardlinked-payload", "SOURCE_BUNDLE_SINGLE_FILE", lambda: bundle.check_tree(linked, tiny, check))
    alias_zip = args.output/"aliased-member.zip"
    with alias_zip.open("xb") as stream, zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as z:
        item = zipfile.ZipInfo("ITEM.txt", date_time=(1980, 1, 1, 0, 0, 0))
        item.create_system = 3
        item.external_attr = 0o100644 << 16
        z.writestr(item, b"original")
    refuses("case-changed-zip-member", "CURRENT_BUNDLE_ZIP_CENSUS",
            lambda: bundle.inspect_archive(alias_zip, tiny, check))
    cases.append("six-retained-file-refusals")

    relocated = args.output/"prebuilt/relocated"
    package = relocated/"package"
    selector = load("_current_release_relocated_preparer", relocated/PREFIX/"prepare_selected.py")
    # The helper's approved code is inert and its exact bytes are in the manifest.
    kit = load("_current_release_prepare_expected", relocated/
               "software/v5/ordinary_multi_source_package/prepare.py")
    selector.known_layout(kit, profile, mapping)
    native_variant = deepcopy(profile)
    native_variant["installation_manifest_sha256"] = "f"*64
    for name in mapping["build"]["native_roles"]:
        native_variant["files"][name] = {"bytes": 123, "sha256": "e"*64}
    selector.known_layout(kit, native_variant, mapping)
    cases.append("rebuilt-native-layout-is-not-native-approval")
    for label, code, mutate in (
        ("unknown-interface", "KIT_SELECT_UNKNOWN_INTERFACE", lambda d: d["files"]["reference/baseline_bundle.py"].update(sha256="0"*64)),
        ("extra-profile-role", "KIT_SELECT_UNKNOWN_INTERFACE", lambda d: d["files"].update({"extra.py": {"bytes": 1, "sha256": "0"*64}})),
        ("boolean-native-length", "KIT_INTEGER", lambda d: d["files"][mapping["build"]["native_roles"][0]].update(bytes=True)),
        ("unknown-profile-schema", "KIT_SELECT_PROFILE_LAYOUT", lambda d: d.update(schema="UNKNOWN")),
    ):
        invalid = deepcopy(profile)
        mutate(invalid)
        refuses(label, code, lambda doc=invalid: selector.known_layout(kit, doc, mapping))
    request = {"action": "init", "state": {"catalog": str(args.output/"future-catalog"),
        "custody": str(args.output/"future-custody"), "store_id": "1"*64},
        "custody_limits": {"objects": 100, "exports": 1000,
                           "logical_bytes": MIB, "db_pages": 256}}
    request_path = args.output/"init-request.json"
    write(request_path, canonical(request))
    preparation = selector.prepare_selected(relocated, package, PROFILE, request_path,
                                             args.output/"prepared")
    need(preparation["known_noncompiled_roles"] == 45 and
         preparation["preparation"]["profile_sha256"] == PROFILE and
         preparation["preparation"]["commands_executed"] == 0 and
         preparation["native_artifacts_checked"] is False and
         preparation["mathematical_acceptance"] is False and
         not (args.output/"future-catalog").exists() and
         not (args.output/"future-custody").exists(), "ACTUAL_INERT_PREPARATION")
    reports["preparation"] = preparation
    prepared = args.output/"prepared"
    receipt = preparation["preparation"]
    need(json.loads((prepared/"RECEIPT.json").read_bytes()) == receipt and
         set(receipt["files"]) == {"arguments.json", "custody-limits.json"} and
         receipt["protected_state_opened"] is False, "PREPARED_RECEIPT")
    for name, value in receipt["files"].items():
        need(pin(prepared/name) == value, "PREPARED_OUTPUT_PIN:"+name)
    arguments = json.loads((prepared/"arguments.json").read_bytes())
    need(arguments == {"entry": "owner", "arguments": ["init",
         "--catalog", request["state"]["catalog"], "--custody", request["state"]["custody"],
         "--store-id", request["state"]["store_id"], "--custody-limits", str(prepared/"custody-limits.json")],
         "profile_sha256": PROFILE, "requires_launcher": True, "mathematical_acceptance": False,
         "authority": "INERT_LOCAL_PREPARATION_PRODUCT_RECHECKS_STATE_AND_MATHEMATICS"} and
         json.loads((prepared/"custody-limits.json").read_bytes()) == request["custody_limits"],
         "EXACT_USABLE_INIT_ARGUMENTS")
    cases.append("relocated-actual-inert-preparation")
    refused_output = args.output/"refused-preparation"
    refuses("wrong-selected-profile", "KIT_SELECT_PROFILE_PIN", lambda: selector.prepare_selected(
        relocated, package, "0"*64, request_path, refused_output))
    need(not refused_output.exists(), "PROFILE_REFUSAL_BEFORE_WRITE")

    # Actual package codec loading crosses the one changed export-helper pin.
    # No native artifacts, owner database, custody or acceptance are involved.
    exporter = load("_current_release_relocated_export", relocated/
                    "software/v5/ordinary_selected_export/export.py")
    launcher = load("_current_release_export_file_support", package/"run.py")
    codecs, inventory = exporter.load_codecs(SimpleNamespace(R=launcher, check=check,
        package=package, bound={"profile_sha256": PROFILE,
                               "installation_manifest_sha256": INSTALLATION}))
    need(Path(codecs.B.__file__) == package/"reference/baseline_bundle.py" and
         pin(Path(codecs.B.__file__))["sha256"] == BINDER and
         hashlib.sha256(inventory).hexdigest() == exporter.INVENTORY_SHA and
         callable(codecs.B.bind_writer), "ACTUAL_NEW_BINDER_EXPORT_LOAD")
    cases.append("relocated-export-new-binder-codecs-load")

    for kind in ("source", "prebuilt"):
        reports[kind]["post_use_verify"] = bundle.verify(args.output/kind/"relocated",
            reports[kind]["pack"]["manifest"]["sha256"], check=check)
    for name, value in expected.items():
        check(); need(pin(args.package/name) == value, "UNCHANGED_ORIGINAL:"+name)
    need(pin(release_path)["sha256"] == args.release_sha256, "UNCHANGED_RELEASE")
    for source, value in support_pins.items():
        need(pin(args.source_root/source) == value and pin(snapshot_root/source) == value,
             "UNCHANGED_REVIEWED_SUPPORT:"+source)
    result = {"status": "PASS_SELECTED_RELEASE_FILE_GATE", "cases": cases, "refusals": refusals,
              "reports": reports, "native_execution": False, "owner_operation": False,
              "mathematical_acceptance": False, "cpu_seconds": time.process_time()-cpu,
              "wall_seconds": time.monotonic()-started}
    write(args.output/"RESULT.json", canonical(result))
    print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()
