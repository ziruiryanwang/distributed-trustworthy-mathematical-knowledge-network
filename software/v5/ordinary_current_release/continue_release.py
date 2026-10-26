"""Finish the missed inert release boundary using one reviewed preparer repair.

The failed first gate and its two distribution receipts remain immutable. Build
one fresh source-input staging tree, repack each changed distribution once, and
require only the preparer payload to differ. No old negative suite, compiler,
native worker, protected state or network operation is run.
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
from types import SimpleNamespace

MIB = 1024**2
PREFIX = "software/v5/ordinary_current_release/"
RELEASE_SHA = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
TEST_SHA = "fc65a4da6149200f16652fe61cfba3cda82efab1f8aa542a744f44f3218f0beb"
PREPARER = PREFIX+"prepare_selected.py"
REPAIR = PREFIX+"prepare_selected02.py"


def need(ok, code):
    if not ok:
        raise AssertionError("CURRENT_CONTINUE_"+code)


def frozen_helpers(snapshot):
    path = snapshot/PREFIX/"test_release.py"
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == TEST_SHA, "FROZEN_TEST_HELPERS")
    name = "_current_continuation_frozen_helpers"
    need(name not in sys.modules, "HELPER_COLLISION")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module  # __name__ is not __main__; the old suite never runs.


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source-root", "package", "output", "prior-source-receipt", "prior-prebuilt-receipt"):
        parser.add_argument("--"+name, type=Path, required=True)
    for name in ("release-sha256", "preparer-sha256", "prior-source-receipt-sha256",
                 "prior-prebuilt-receipt-sha256"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    started, cpu = time.monotonic(), time.process_time()

    def check():
        need(time.monotonic()-started < 150 and time.process_time()-cpu < 75, "ALLOWANCE")

    snapshot = Path(__file__).absolute().parents[3]
    T = frozen_helpers(snapshot)
    bundle = T.load("_current_continuation_file_helpers", snapshot/PREFIX/"bundle.py")
    H = bundle.helper()
    root = H.ordinary(args.source_root, directory=True)
    package = H.ordinary(args.package, directory=True)
    output = H.ordinary(args.output, directory=True, fresh=True)
    H.ordinary(output.parent, directory=True)
    need(not root.is_relative_to(output) and not output.is_relative_to(package) and
         not package.is_relative_to(output) and not snapshot.is_relative_to(output) and
         not output.is_relative_to(snapshot), "OUTPUT_DISJOINT")
    need(H.hexid(args.release_sha256) == RELEASE_SHA, "APPROVED_RELEASE")
    H.hexid(args.preparer_sha256)
    release_raw = H.read(snapshot/PREFIX/"release.json", check)
    need(H.sha(release_raw) == RELEASE_SHA and
         H.read(root/PREFIX/"release.json", check) == release_raw, "RELEASE_BINDING")
    release = H.strict_json(release_raw)
    need(release["schema"] == "DMKN_ORDINARY_CURRENT_RELEASE_SELECTION_V1", "RELEASE_SCHEMA")

    prior, prior_inputs = {}, {}
    for kind in ("source", "prebuilt"):
        path = H.ordinary(getattr(args, "prior_"+kind+"_receipt"))
        expected_sha = H.hexid(getattr(args, "prior_"+kind+"_receipt_sha256"))
        raw = H.read(path, check)
        need(H.sha(raw) == expected_sha and not path.is_relative_to(output), "PRIOR_RECEIPT_PIN")
        value = H.strict_json(raw)
        need(value["schema"] == "DMKN_ORDINARY_CURRENT_RELEASE_BUNDLE_RECEIPT_V1" and
             value["status"] == "PACKED_CURRENT_DISTRIBUTION_NOT_NEW_ACCEPTANCE" and
             value["kind"] == kind and value["release_sha256"] == RELEASE_SHA,
             "PRIOR_RECEIPT_SELECTION")
        prior[kind], prior_inputs[path] = value, H.pin(raw)

    # Every staged logical input has one actual selected origin. Foundation
    # data are the only inputs intentionally external to the source snapshot.
    staged_pins, origins, originals, snapshot_pins = {}, {}, {}, {}
    for name in ("continue_release.py", "test_release.py"):
        selected_path = snapshot/PREFIX/name
        expected = H.pin(H.read(selected_path, check))
        need(H.pin(H.read(root/PREFIX/name, check)) == expected, "HARNESS_SOURCE:"+name)
        snapshot_pins[selected_path], originals[root/PREFIX/name] = expected, expected

    def select(logical, source, expected=None):
        H.relative(logical); H.relative(source)
        origin = root/source if source.startswith("software/assets/foundation/") else snapshot/source
        raw = H.read(origin, check)
        actual = H.pin(raw)
        need(expected is None or actual == expected, "SELECTED_SOURCE_PIN:"+source)
        need(logical not in staged_pins or
             (staged_pins[logical] == actual and origins[logical] == origin), "SOURCE_ALIAS")
        need(H.pin(H.read(root/source, check)) == actual, "CANONICAL_SOURCE_PIN:"+source)
        staged_pins[logical], origins[logical], originals[root/source] = actual, origin, actual
        if origin.is_relative_to(snapshot):
            snapshot_pins[origin] = actual

    for name, expected in release["build"]["sources"].items():
        select(name, name, expected)
    for row in release["companions"].values():
        select(row["source"], row["source"], {"bytes": row["bytes"], "sha256": row["sha256"]})
    for kind in ("source", "prebuilt"):
        for source in release["release_support"][kind].values():
            select(source, REPAIR if source == PREPARER else source)
    need(staged_pins[PREPARER]["sha256"] == args.preparer_sha256 and
         len(staged_pins) == 106 and sum(row["bytes"] for row in staged_pins.values()) <= 8*MIB,
         "STAGING_SELECTION")
    old_pin = H.pin(H.read(snapshot/PREPARER, check))
    need(H.pin(H.read(root/PREPARER, check)) == old_pin and
         all(value["files"][PREPARER] == old_pin for value in prior.values()) and
         old_pin != staged_pins[PREPARER], "EXACT_OLD_AND_REPAIRED_PREPARER")
    originals[root/PREPARER], snapshot_pins[snapshot/PREPARER] = old_pin, old_pin

    output.mkdir()
    staging = output/"source-inputs"
    staging.mkdir()
    for name, expected in sorted(staged_pins.items()):
        check()
        raw = H.read(origins[name], check)
        need(H.pin(raw) == expected, "STAGING_INPUT_CHANGED:"+name)
        target = staging/name
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        H.fresh_bytes(target, raw)
    bundle.check_tree(staging, staged_pins, check)

    reports, verifiers = {}, {}
    for kind in ("source", "prebuilt"):
        check()
        report = bundle.pack(staging, output/kind, kind=kind,
                             package=package if kind == "prebuilt" else None, check=check)
        need(H.strict_json(H.read(output/kind/"RECEIPT.json", check)) == report,
             "PACK_RECEIPT:"+kind)
        current, old = report["files"], prior[kind]["files"]
        need(set(current) == set(old) and
             {name for name in current if current[name] != old[name]} == {PREPARER} and
             current[PREPARER] == staged_pins[PREPARER] and
             report["manifest"] != prior[kind]["manifest"], "ONLY_PREPARER_PAYLOAD_CHANGED:"+kind)
        for destination, source in release["release_support"][kind].items():
            need(current[destination] == staged_pins[source], "REVIEWED_SUPPORT:"+destination)
        relocated = output/kind/"relocated"
        for destination, expected in current.items():
            check()
            need(H.pin(H.read(relocated/destination, check, expected["bytes"])) == expected,
                 "RELOCATED_PAYLOAD:"+destination)
        verifier = T.load("_current_continuation_verifier_"+kind, relocated/PREFIX/"bundle.py")
        reports[kind] = {"pack": report, "verify": verifier.verify(
            relocated, report["manifest"]["sha256"], check=check), "changed_payloads": [PREPARER]}
        verifiers[kind] = verifier

    relocated = output/"prebuilt/relocated"
    current_package = relocated/"package"
    selector = T.load("_current_continuation_relocated_preparer", relocated/PREPARER)
    request = {"action": "init", "state": {"catalog": str(output/"future-catalog"),
        "custody": str(output/"future-custody"), "store_id": "1"*64},
        "custody_limits": {"objects": 100, "exports": 1000, "logical_bytes": MIB, "db_pages": 256}}
    request_path, prepared = output/"init-request.json", output/"prepared"
    T.write(request_path, T.canonical(request))
    preparation = selector.prepare_selected(relocated, current_package, T.PROFILE, request_path, prepared)
    need(preparation["known_noncompiled_roles"] == 45 and
         preparation["preparation"]["profile_sha256"] == T.PROFILE and
         preparation["preparation"]["commands_executed"] == 0 and
         preparation["native_artifacts_checked"] is False and
         preparation["mathematical_acceptance"] is False and
         not (output/"future-catalog").exists() and not (output/"future-custody").exists(),
         "ACTUAL_INERT_PREPARATION")
    receipt = preparation["preparation"]
    need(H.strict_json(H.read(prepared/"RECEIPT.json", check)) == receipt and
         set(receipt["files"]) == {"arguments.json", "custody-limits.json"} and
         receipt["protected_state_opened"] is False, "PREPARED_RECEIPT")
    for name, expected in receipt["files"].items():
        need(H.pin(H.read(prepared/name, check)) == expected, "PREPARED_OUTPUT_PIN:"+name)
    arguments = H.strict_json(H.read(prepared/"arguments.json", check))
    need(arguments == {"entry": "owner", "arguments": ["init",
         "--catalog", request["state"]["catalog"], "--custody", request["state"]["custody"],
         "--store-id", request["state"]["store_id"], "--custody-limits", str(prepared/"custody-limits.json")],
         "profile_sha256": T.PROFILE, "requires_launcher": True, "mathematical_acceptance": False,
         "authority": "INERT_LOCAL_PREPARATION_PRODUCT_RECHECKS_STATE_AND_MATHEMATICS"} and
         H.strict_json(H.read(prepared/"custody-limits.json", check)) == request["custody_limits"],
         "EXACT_USABLE_INIT_ARGUMENTS")
    reports["preparation"] = preparation
    refused = output/"refused-preparation"
    try:
        selector.prepare_selected(relocated, current_package, "0"*64, request_path, refused)
    except ValueError as error:
        need(str(error) == "KIT_SELECT_PROFILE_PIN", "WRONG_PROFILE_REFUSAL_CODE")
    else:
        raise AssertionError("CURRENT_CONTINUE_MISSING_PROFILE_REFUSAL")
    need(not refused.exists(), "PROFILE_REFUSAL_BEFORE_WRITE")

    exporter = T.load("_current_continuation_relocated_export", relocated/
                      "software/v5/ordinary_selected_export/export.py")
    launcher = T.load("_current_continuation_export_support", current_package/"run.py")
    codecs, inventory = exporter.load_codecs(SimpleNamespace(R=launcher, check=check,
        package=current_package, bound={"profile_sha256": T.PROFILE,
                                        "installation_manifest_sha256": T.INSTALLATION}))
    need(Path(codecs.B.__file__) == current_package/"reference/baseline_bundle.py" and
         T.pin(Path(codecs.B.__file__))["sha256"] == T.BINDER and
         hashlib.sha256(inventory).hexdigest() == exporter.INVENTORY_SHA and
         callable(codecs.B.bind_writer), "ACTUAL_NEW_BINDER_EXPORT_LOAD")

    for kind, verifier in verifiers.items():
        reports[kind]["post_use_verify"] = verifier.verify(output/kind/"relocated",
            reports[kind]["pack"]["manifest"]["sha256"], check=check)
    bundle.check_tree(staging, staged_pins, check)
    bundle.check_tree(package, release["prebuilt"]["files"], check)
    for group in (originals, snapshot_pins, prior_inputs):
        for path, expected in group.items():
            check()
            need(H.pin(H.read(path, check)) == expected, "UNCHANGED_INPUT:"+str(path))
    check()
    result = {"status": "PASS_SELECTED_RELEASE_PREPARER_CONTINUATION",
        "reports": reports, "staged_inputs": staged_pins,
        "prior_receipts": {kind: {"path": str(getattr(args, "prior_"+kind+"_receipt")),
            "sha256": getattr(args, "prior_"+kind+"_receipt_sha256")} for kind in prior},
        "repaired_preparer": staged_pins[PREPARER],
        "cases": ["source-only-preparer-delta", "prebuilt-only-preparer-delta",
                  "relocated-actual-inert-preparation", "wrong-profile-before-write",
                  "relocated-export-new-binder-codecs-load", "unchanged-originals-and-sources"],
        "old_ten_negatives_repeated": False, "native_execution": False,
        "owner_operation": False, "mathematical_acceptance": False,
        "cpu_seconds": time.process_time()-cpu, "wall_seconds": time.monotonic()-started}
    T.write(output/"RESULT.json", T.canonical(result))
    print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()
