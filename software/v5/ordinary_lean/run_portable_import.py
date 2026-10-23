"""Selected metadata-only local cutover; no Lean process or native loading."""
from pathlib import Path
import hashlib
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import ordinary_semantics as S
import local_catalog as C
import portable_catalog as P
import legacy_catalog_import as I

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")


def main():
    started = time.monotonic()
    deadline = started + 155
    C.need(Path.cwd() == ROOT and len(sys.argv) == 3 and sys.flags.isolated and
           sys.flags.no_site and sys.dont_write_bytecode, "SELECTED_OWNER_INVOCATION")
    output, inputs = map(Path, sys.argv[1:])
    C.need(output.parent == ROOT / "experiments/v5-local-checks" and
           inputs.parent == output.parent and Path(__file__).resolve().parents[4] == output,
           "SELECTED_OUTPUT_SNAPSHOT")
    selection = json.loads(C.read_bounded(output / "selection.json", 1024**2))
    snapshot = output / "sources"
    for relative, expected in selection["sources"].items():
        C.need(hashlib.sha256(C.read_bounded(snapshot / relative, 2*1024**2)).hexdigest() == expected,
               "SELECTED_CONTROLLER_SOURCE")

    def selected(filename):
        path = inputs / filename
        raw = C.read_bounded(path, 16*1024**2)
        C.need(selection["runtime_pins"].get(str(path)) == hashlib.sha256(raw).hexdigest(),
               "SELECTED_MANIFEST_PIN")
        return raw

    manifest_raw = selected("SOURCE.json")
    implementation_raw = selected("IMPLEMENTATION.json")
    correspondence_raw = selected("CORRESPONDENCE.json")
    manifest = E.strict_json(manifest_raw, E.Limits(max_bytes=16*1024**2))
    implementation = S.read_implementation(implementation_raw)
    C.need(implementation["controller_support"] ==
           C.digest("ordinary-portable-controller-support-v1", selection["sources"]),
           "IMPLEMENTATION_ACTUAL_CONTROLLER")
    store_id = C.digest("ordinary-portable-local-store-v1", [selection["name"],
        manifest["store_id"], manifest["selected_root"], S.implementation_id(implementation_raw)])
    destination = output / "portable-catalog"
    result = I.import_legacy(I.ELIGIBLE_SOURCE, manifest_raw, destination,
        implementation_raw, store_id, correspondence_raw, parent_deadline=deadline,
        limits=I.ImportLimits(max_file_bytes=128*1024**2))
    C.need(result["roots"] == 5 and result["names"] == 3629 and
           result["source_root"] == manifest["selected_root"], "COMPLETE_SELECTED_IMPORT")
    catalog = P.PortableCatalog.open(destination, implementation_raw, store_id)
    try:
        context = catalog.context(result["local_root"])
        plan, bindings = context["modules"], context["bindings"]
        C.need(len(plan) == 5 and len(bindings) == 3629, "REOPEN_IMPORTED_CONTEXT")
        C.need([row["module_name"] for row in plan] ==
               [C.module_name(row["root"]) for row in manifest["roots"]], "UNCHANGED_NATIVE_MODULES")
    finally:
        catalog.close()
    C.need(time.monotonic() < deadline, "IMPORT_PARENT_DEADLINE")
    result.update(schema="DMKN_ORDINARY_PORTABLE_IMPORT_RESULT_V1",
        status="PASS_LOCAL_TRANSLATION_AND_ACTIVE_REOPEN_NO_NATIVE_REPLAY",
        store_id=store_id, source_manifest_sha256=hashlib.sha256(manifest_raw).hexdigest(),
        wall_seconds=time.monotonic()-started,
        claims="OWNER_LOCAL_METADATA_CUTOVER_NOT_PEER_ADOPTION_DISCOVERY_OR_RELEASE")
    with (output / "IMPORT-RESULT.json").open("xb") as stream:
        stream.write((json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
