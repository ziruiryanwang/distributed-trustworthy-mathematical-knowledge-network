"""File-only selection of the adopted owner-local transition, not peer adoption."""
from pathlib import Path
import hashlib
import json
import re
import sqlite3
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ordinary_evidence as E
import ordinary_semantics as S
import local_catalog as C

PREFIX = "software/v5/ordinary_lean/"
SOURCES = ["tools/Run-V5-Check.py"] + [PREFIX + name for name in (
    "select_portable_import.py", "run_portable_import.py", "run_portable_extension.py", "ordinary_evidence.py",
    "ordinary_semantics.py", "portable_evidence.py", "local_catalog.py",
    "legacy_identity_translation.py", "portable_catalog.py", "legacy_catalog_import.py")]
CYCLE = ROOT / "research/cycles/v5-2026-10-22-native-library"
OLD = LOCAL / "ordinary-native-admission-01"
RECOVERY = LOCAL / "ordinary-native-recovery-01"
SUCCESSOR = LOCAL / "ordinary-successor-admission-01"
SOURCE = SUCCESSOR / "successor-admission/catalog"
FINAL_ROOT = "98e65adcb09061a78dd3088a4bbf966b9ac1cee9f98da6f8fbcdb410f3edf7b9"


def need(ok, code):
    if not ok:
        raise ValueError(code)


def pin(path):
    path = C.ordinary(path)
    size = path.stat().st_size
    need(size <= 128 * 1024**2, "SELECTED_FILE_BOUND")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == size, "SELECTED_FILE_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": digest}


def saved(path, expected):
    row = pin(path)
    need(row["sha256"] == expected, "ADOPTED_INPUT_CHANGED:" + str(path))
    return json.loads(path.read_bytes())


def write(path, value):
    raw = E.canonical_json(value)
    with path.open("xb") as stream:
        stream.write(raw)
    return pin(path)


def main():
    need(Path.cwd() == ROOT and len(sys.argv) == 2 and
         re.fullmatch(r"ordinary-[a-z0-9-]{1,54}", sys.argv[1]), "CANONICAL_NAME_REQUIRED")
    name = sys.argv[1]
    selected_path = LOCAL / (name + ".selection.json")
    inputs = LOCAL / (name + "-inputs")
    need(not selected_path.exists() and not inputs.exists() and not (LOCAL / name).exists(),
         "FRESH_SELECTION_REQUIRED")
    prior = saved(OLD / "selection.json", "ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f")
    result = saved(SUCCESSOR / "successor-admission/SUCCESSOR-RESULT.json",
                   "188110017e34f123f2a6b6fe9b6eb4df7dcd3d9ace888dd0beec9669a9de28a6")
    saved(SUCCESSOR / "RESULT.json", "a0273ec06eb9be9e64e0695fe8a4fbc2ed2528d4f540fabc41d2cbf6b1718726")
    need(result["root"] == FINAL_ROOT and result["units_checked"] == 7, "ADOPTED_FINAL_ROOT")
    profile_path = OLD / "native-admission/PROFILE.json"
    profile_doc = json.loads(profile_path.read_bytes())
    profile, support = profile_doc["profile"], profile_doc["support"]
    profile_id = C.digest("ordinary-native-profile-v1", profile)
    need(profile_id == result["profile_id"], "ADOPTED_PROFILE")

    # Resolve every named source/compiled/kernel support leaf to retained bytes.
    support_pins = [pin(profile_path)]
    for key in ("source", "compiled"):
        for filename, expected in support["adapter"][key].items():
            if key == "source":
                path = OLD / "sources" / PREFIX / filename
                need(prior["sources"][PREFIX + filename] == expected["sha256"], "OLD_SOURCE_SELECTION")
            else:
                matches = [Path(p) for p, digest in prior["runtime_pins"].items()
                           if Path(p).name == filename and digest == expected["sha256"]]
                need(len(matches) == 1, "EXACT_COMPILED_SUPPORT")
                path = matches[0]
            actual = pin(path)
            need({k: actual[k] for k in ("bytes", "sha256")} == expected, "ADAPTER_SUPPORT_BYTES")
            support_pins.append(actual)
    for filename, expected in support["kernel"]["files"].items():
        path = ROOT / "software/runtime/lean-4.34.0-windows/bin" / filename
        actual = pin(path)
        need(prior["runtime_pins"][str(path)] == expected["sha256"] and
             {k: actual[k] for k in ("bytes", "sha256")} == expected, "KERNEL_SUPPORT_BYTES")
        support_pins.append(actual)
    for key, domain, section in (("kernel_support", "ordinary-kernel-support-v1", "kernel"),
                                ("adapter_support", "ordinary-adapter-support-v1", "adapter"),
                                ("basis_receiver_support", "ordinary-basis-receiver-support-v1", "basis_receiver")):
        need(profile[key] == C.digest(domain, support[section]), "ORIGINAL_SUPPORT_DIGEST")

    db_pin = pin(SOURCE / "catalog.sqlite")
    need(not any(Path(str(SOURCE / "catalog.sqlite") + suffix).exists()
                 for suffix in ("-journal", "-wal", "-shm")), "SOURCE_SIDECAR")
    db = sqlite3.connect((SOURCE / "catalog.sqlite").as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        need(db.execute("SELECT count(*) FROM roots").fetchone() == (5,), "FIVE_ADOPTED_ROOTS")
        ordered, current = [], FINAL_ROOT
        while current:
            need(len(ordered) < 5, "CHAIN_BOUND")
            found = db.execute("SELECT record FROM roots WHERE id=?", (current,)).fetchone()
            need(found is not None and type(found[0]) is bytes, "ROOT_RECORD")
            raw = found[0]
            row = E.strict_json(raw, E.Limits(max_bytes=16*1024**2))
            need(row["root"] == current and row["profile_id"] == profile_id, "ROOT_PROFILE")
            ordered.append((raw, row)); current = row["parent"]
    finally:
        db.close()
    need(pin(SOURCE / "catalog.sqlite") == db_pin, "READONLY_DATABASE_CHANGED")
    ordered.reverse()
    need(len(ordered) == 5 and ordered[0][1]["root"] == result["basis_id"], "COMPLETE_CHAIN")

    # The actual clean check lineage is adopted by root; these pins retain it.
    # A future arbitrary caller cannot confer eligibility by fabricating this list.
    lineage_dirs = [OLD / "native-admission/calls/000-basis",
        OLD / "native-admission/calls/001-extension",
        RECOVERY / "native-recovery/calls/002-extension",
        RECOVERY / "native-recovery/calls/003-extension",
        SUCCESSOR / "successor-admission/call"]
    root_rows, offset = [], 0
    for index, (raw, row) in enumerate(ordered):
        count = (0, 1024, 1024, 804, 7)[index]
        evidence_dir = (SUCCESSOR / "successor-admission/evidence" if index == 4
                        else OLD / "native-admission/evidence")
        start = 0 if index == 4 else offset
        evidence = [pin(evidence_dir / f"{n:05d}.json") for n in range(start, start + count)]
        offset += count if index < 4 else 0
        lineage = [pin(lineage_dirs[index] / filename) for filename in
                   ("SUPERVISION.json", "worker-report.json", "supervision/command.json")]
        root_rows.append({"root": row["root"], "record_sha256": hashlib.sha256(raw).hexdigest(),
                          "check_lineage": lineage, "evidence": evidence})
    manifest = {"schema": "DMKN_ORDINARY_ELIGIBLE_LOCAL_SOURCE_V1", "source_directory": str(SOURCE),
        "store_id": result["store_id"], "profile_id": profile_id, "basis_id": result["basis_id"],
        "selected_root": FINAL_ROOT, "marker": pin(SOURCE / "ADOPTION.json"), "database": db_pin,
        "fixed_seed": pin(ROOT / "software/assets/foundation/seed-verified.json"),
        "fixed_inventory": pin(ROOT / "software/assets/foundation/seed-inventory-json.json"),
        "check_support": support_pins, "roots": root_rows}
    source_map = {relative: pin(ROOT / relative)["sha256"] for relative in SOURCES}
    snapshot = {kind: {module + suffix: support["adapter"][kind][module + suffix]
                for module in ("BasisSnapshot", "LocalSnapshot")}
                for kind, suffix in (("source", ".lean"), ("compiled", ".olean"))}
    implementation = {"schema": S.IMPLEMENTATION_SCHEMA, "semantic_id": S.semantic_id(),
        "platform": {"os": "windows", "architecture": "x86_64", "word_bits": 64, "byte_order": "little"},
        **{key: profile[key] for key in ("kernel_support", "adapter_support", "basis_receiver_support")},
        "controller_support": C.digest("ordinary-portable-controller-support-v1", source_map),
        "snapshot_support": C.digest("ordinary-snapshot-support-v1", snapshot),
        "snapshot_format": profile["snapshot_format"],
        "support_scope": "EXPLICIT_NAMED_SUPPORT_NOT_HERMETIC_TOOLCHAIN"}
    impl_raw = E.canonical_json(implementation)
    S.read_implementation(impl_raw)
    correspondence = {"schema": "DMKN_ORDINARY_SAME_RUNTIME_CORRESPONDENCE_V1",
        "source_profile_id": profile_id, "semantic_id": S.semantic_id(), "foundation_id": S.foundation_id(),
        "implementation_id": S.implementation_id(impl_raw),
        **{key: implementation[key] for key in ("kernel_support", "adapter_support", "basis_receiver_support",
                                              "snapshot_support", "snapshot_format", "platform")},
        "seed_sha256": S.SEED, "inventory_sha256": S.INVENTORY,
        "expression_contract_sha256": S.EXPRESSION_CONTRACT, "declaration_contract_sha256": S.DECLARATION_CONTRACT,
        "adopted_argument": pin(CYCLE / "PORTABLE-SUPPORT-CORRESPONDENCE.md")}
    need(correspondence["adopted_argument"]["sha256"] ==
         "ade45957f49d7078c46819dd020cda5c63d19d879571f4b958d6b5ede6386fba", "REVIEWED_CORRESPONDENCE")
    inputs.mkdir()
    input_pins = [write(inputs / filename, value) for filename, value in (
        ("SOURCE.json", manifest), ("IMPLEMENTATION.json", implementation),
        ("CORRESPONDENCE.json", correspondence))]
    runtime_pins = {path: prior["runtime_pins"][path] for path in
                   (r"D:\Python314\python.exe", r"D:\Python314\python314.dll", r"D:\Python314\python3.dll")}
    for path, expected in runtime_pins.items():
        need(pin(Path(path))["sha256"] == expected, "PYTHON_PIN")
    runtime_pins.update({p["path"]: p["sha256"] for p in input_pins})
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name, "sources": source_map,
        "runtime_pins": runtime_pins, "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_lean\run_portable_import.py", "{output}", str(inputs)],
        "limits": {"cpu_seconds": 120, "wall_seconds": 180, "memory_mib": 512,
                   "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    selected = write(selected_path, selection)
    print(json.dumps({"selection": str(selected_path), "sha256": selected["sha256"],
                      "evidence_units": 2859, "execution": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
