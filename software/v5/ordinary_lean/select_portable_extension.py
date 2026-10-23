"""File-only selector for one changed V2-catalog/native-worker handoff."""
from pathlib import Path
import hashlib
import json
import os
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ordinary_evidence as E
import local_catalog as C

PREFIX = "software/v5/ordinary_lean/"
IMPORT = LOCAL / "ordinary-portable-import-01"
INPUTS = LOCAL / "ordinary-portable-import-01-inputs"
ORIGIN = LOCAL / "ordinary-native-admission-01"
TARGET = "DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches"


def pin(path):
    C.ordinary(path)
    size = path.stat().st_size
    C.need(size <= 128 * 1024**2, "SELECTED_FILE_BOUND")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    C.need(size == path.stat().st_size, "SELECTED_FILE_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": digest}


def main():
    C.need(Path.cwd() == ROOT and len(sys.argv) == 2 and
           re.fullmatch(r"ordinary-[a-z0-9-]{1,54}", sys.argv[1]), "CANONICAL_NAME_REQUIRED")
    name = sys.argv[1]
    selection_path = LOCAL / (name + ".selection.json")
    manifest_path = LOCAL / (name + "-parent.json")
    C.need(not any(p.exists() for p in (selection_path, manifest_path, LOCAL / name)), "FRESH_OPERATION")
    result = json.loads((IMPORT / "IMPORT-RESULT.json").read_bytes())
    outer = json.loads((IMPORT / "RESULT.json").read_bytes())
    C.need(result["status"] == "PASS_LOCAL_TRANSLATION_AND_ACTIVE_REOPEN_NO_NATIVE_REPLAY" and
           result["roots"] == 5 and result["names"] == 3629 and
           outer["result"]["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
           outer["selection_sha256"] == pin(IMPORT / "selection.json")["sha256"], "CLEAN_IMPORTED_PARENT")
    imported_selection = json.loads((IMPORT / "selection.json").read_bytes())
    source_manifest = E.strict_json((INPUTS / "SOURCE.json").read_bytes(), E.Limits(max_bytes=16*1024**2))
    source = IMPORT / "portable-catalog"
    C.ordinary(source, directory=True)
    pending, directories, files, total = [source], [], {}, 0
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as listing:
            for entry in listing:
                path = Path(entry.path)
                relative = path.relative_to(source).as_posix()
                C.need(len(directories) + len(files) < 8192, "PARENT_TREE_COUNT")
                if entry.is_dir(follow_symlinks=False):
                    C.ordinary(path, directory=True)
                    directories.append(relative); pending.append(path)
                else:
                    p = pin(path)
                    total += p["bytes"]
                    C.need(total <= 512*1024**2, "PARENT_TREE_BYTES")
                    files[relative] = {key: p[key] for key in ("bytes", "sha256")}
    audit_files = [key for key in files if key.startswith("imports/") and key.endswith("/audit.json")]
    C.need(len(audit_files) == 1, "ONE_ACTIVATED_IMPORT")
    audit = E.strict_json((source / audit_files[0]).read_bytes(), E.Limits(max_bytes=16*1024**2))
    target = [[0, {"$bytes": list(part.encode())}] for part in TARGET.split(".")]
    matches = [entry for row in audit["roots"] for entry in row["translations"]
               if any(pair[0] == target for pair in entry["portable_outputs"])]
    C.need(len(matches) == 1, "EXACT_TARGET_EVIDENCE")
    manifest = {"schema": "DMKN_ORDINARY_PORTABLE_EXTENSION_PARENT_V1",
        "source_directory": str(source), "store_id": result["store_id"], "parent_root": result["local_root"],
        "implementation": pin(INPUTS / "IMPLEMENTATION.json"), "source_manifest": pin(INPUTS / "SOURCE.json"),
        "correspondence": pin(INPUTS / "CORRESPONDENCE.json"), "import_selection": pin(IMPORT / "selection.json"),
        "directories": sorted(directories), "files": files,
        "target_evidence": matches[0]["portable_evidence"]["relative_path"]}
    C.need(manifest["target_evidence"] in files, "TARGET_IN_PARENT_TREE")
    sources = ["tools/Run-V5-Check.py", PREFIX + "select_portable_extension.py"] + [PREFIX + filename for filename in
        ("ordinary_evidence.py", "ordinary_semantics.py", "local_catalog.py", "portable_evidence.py",
         "portable_catalog.py", "run_portable_extension.py")]
    source_map = {relative: pin(ROOT / relative)["sha256"] for relative in sources}
    for relative in sources:
        if relative != PREFIX + "select_portable_extension.py":
            C.need(source_map[relative] == imported_selection["sources"][relative], "IMPORTED_CONTROLLER_CHANGED")
    old = json.loads((ORIGIN / "selection.json").read_bytes())
    runtime_pins = {p: old["runtime_pins"][p] for p in
                   (r"D:\Python314\python.exe", r"D:\Python314\python314.dll", r"D:\Python314\python3.dll")}
    for item in [manifest[key] for key in ("implementation", "source_manifest", "correspondence", "import_selection")] + source_manifest["check_support"]:
        C.need(pin(Path(item["path"])) == item, "SUPPORT_CHANGED")
        runtime_pins[item["path"]] = item["sha256"]
    for path in (ORIGIN / "selection.json", ORIGIN / "sources/tools/Run-V5-Check.py",
                 IMPORT / "IMPORT-RESULT.json", IMPORT / "RESULT.json"):
        runtime_pins[str(path)] = pin(path)["sha256"]
    raw = E.canonical_json(manifest)
    with manifest_path.open("xb") as stream:
        stream.write(raw)
    runtime_pins[str(manifest_path)] = hashlib.sha256(raw).hexdigest()
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": source_map, "runtime_pins": runtime_pins,
        "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
            r"{snapshot}\software\v5\ordinary_lean\run_portable_extension.py", "{output}", str(manifest_path)],
        "limits": {"cpu_seconds": 90, "wall_seconds": 120, "memory_mib": 1536,
                   "active_processes": 3, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    encoded = E.canonical_json(selection)
    with selection_path.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"selection": str(selection_path), "sha256": hashlib.sha256(encoded).hexdigest(),
                      "execution": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
