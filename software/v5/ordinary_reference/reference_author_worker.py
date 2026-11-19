"""One ordinary source compile over a controller-authenticated artifact map.

The caller holds the enclosing Job, protected owner and original allowance.
Source and elaboration extensions are owner-approved executable inputs, not a
hostile-source sandbox. Output is inert until independent owner admission.
The controller authenticates/revalidates original and generated library parts;
this worker binds the source/setup and fresh outputs without rescanning them.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

MIB = 1024**2
MODULE = re.compile(r"DMKNAuthor_[0-9a-f]{64}\Z")


def need(condition, code):
    if not condition:
        raise ValueError(code)


def ordinary_path(value, *, directory=False, fresh=False):
    need(type(value) is str and 0 < len(value) <= 32768 and
         re.match(r"^[A-Za-z]:[\\/]", value) is not None and
         not any(ord(c) < 32 or c == ";" for c in value) and
         not any(p in (".", "..") for p in value.replace("\\", "/").split("/")),
         "REFERENCE_AUTHOR_PATH")
    path = Path(value)
    need(path.is_absolute(), "REFERENCE_AUTHOR_ABSOLUTE_PATH")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
             "REFERENCE_AUTHOR_PATH_ANCESTOR")
    if fresh:
        need(not os.path.lexists(path), "REFERENCE_AUTHOR_FRESH_OUTPUT")
        return path
    info = path.lstat()
    need(not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT and
         (stat.S_ISDIR(info.st_mode) if directory else
          stat.S_ISREG(info.st_mode) and info.st_nlink == 1), "REFERENCE_AUTHOR_ORDINARY_PATH")
    return path


def pin(path, maximum):
    ordinary_path(str(path))
    info = path.stat()
    need(0 < info.st_size <= maximum, "REFERENCE_AUTHOR_INPUT_BOUND")
    count, digest = 0, hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(min(65536, maximum+1-count)):
            count += len(block)
            need(count <= maximum, "REFERENCE_AUTHOR_FILE_GROWTH")
            digest.update(block)
    need(count == info.st_size, "REFERENCE_AUTHOR_SIZE_CHANGED")
    return {"path": str(path), "bytes": count, "sha256": digest.hexdigest()}


def object_pairs(rows):
    result = {}
    for key, value in rows:
        need(key not in result, "REFERENCE_AUTHOR_DUPLICATE_KEY")
        result[key] = value
    return result


def parts(output):
    return (output, Path(str(output)+".server"), Path(str(output)+".private"),
            output.with_suffix(".ir.sig"), output.with_suffix(".ir"))


def run(args):
    need(len(args) == 6 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "REFERENCE_AUTHOR_WORKER_PROFILE")
    lean = ordinary_path(args[0])
    source_root = ordinary_path(args[1], directory=True)
    source = ordinary_path(args[2])
    setup = ordinary_path(args[3])
    output = ordinary_path(args[4], fresh=True)
    report = ordinary_path(args[5], fresh=True)
    need(source.parent == source_root and source.suffix == ".lean" and
         output.suffix == ".olean" and MODULE.fullmatch(source.stem) is not None and
         output.stem == source.stem and len(set((lean, source, setup, output, report))) == 5,
         "REFERENCE_AUTHOR_MODULE_PATHS")
    output_parts = parts(output)
    need(report not in output_parts and source not in output_parts and setup not in output_parts,
         "REFERENCE_AUTHOR_OUTPUT_ALIAS")
    for path in output_parts:
        ordinary_path(str(path), fresh=True)
    before_source, before_setup = pin(source, 2*MIB), pin(setup, 16*MIB)
    with setup.open("rb") as handle:
        raw = handle.read(16*MIB+1)
    need(len(raw) == before_setup["bytes"] and hashlib.sha256(raw).hexdigest() ==
         before_setup["sha256"], "REFERENCE_AUTHOR_SETUP_CHANGED")
    document = json.loads(raw.decode("utf-8"), object_pairs_hook=object_pairs)
    need(type(document) is dict and set(document) ==
         {"name", "package", "isModule", "imports", "importArts", "dynlibs", "plugins", "options"}
         and document["name"] == source.stem and document["package"] is None and
         document["isModule"] is True and document["dynlibs"] == [] and document["plugins"] == []
         and type(document["options"]) is dict and set(document["options"]) == {"Elab.async"}
         and document["options"]["Elab.async"] is False, "REFERENCE_AUTHOR_SETUP_FIELDS")
    imports, artifacts = document["imports"], document["importArts"]
    need(type(imports) is list and 1 <= len(imports) <= 16 and type(artifacts) is dict and
         1 <= len(artifacts) <= 4128 and source.stem not in artifacts,
         "REFERENCE_AUTHOR_SETUP_BOUND")
    imported = set()
    for row in imports:
        need(type(row) is dict and set(row) == {"module", "importAll", "isExported", "isMeta"}
             and type(row["module"]) is str and row["module"] in artifacts and
             row["module"] not in imported and row["importAll"] is False and
             row["isExported"] is True and row["isMeta"] is False,
             "REFERENCE_AUTHOR_SETUP_IMPORT")
        imported.add(row["module"])
    # Exact path identities, full artifact pins and transitive coverage belong to
    # the protected controller. This syntax check cannot manufacture that trust.
    for name, matrix in artifacts.items():
        need(type(name) is str and 0 < len(name) <= 4096 and type(matrix) is list and
             len(matrix) == 2 and all(type(row) is list for row in matrix) and
             [len(row) for row in matrix] == [3, 2] and
             all(type(path) is str and 0 < len(path) <= 32768 and "\x00" not in path
                 for row in matrix for path in row), "REFERENCE_AUTHOR_SETUP_ARTIFACTS")
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = ""
    env["PATH"] = str(lean.parent)
    argv = [str(lean), "--setup="+str(setup), "-DElab.async=false", "-R", str(source_root),
            "-o", str(output), str(source)]
    need(sum(len(argument)+3 for argument in argv) <= 30000, "REFERENCE_AUTHOR_ARGV_BOUND")
    code = subprocess.call(argv, cwd=source_root, env=env, stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
    need(code == 0, "REFERENCE_AUTHOR_COMPILER_EXIT")
    need(pin(source, 2*MIB) == before_source and pin(setup, 16*MIB) == before_setup,
         "REFERENCE_AUTHOR_INPUT_CHANGED")
    output_pins, total = [], 0
    for path in output_parts:
        item = pin(path, 64*MIB)
        total += item["bytes"]
        need(total <= 64*MIB, "REFERENCE_AUTHOR_OUTPUT_BYTES")
        output_pins.append(item)
    result = {"schema": "DMKN_ORDINARY_REFERENCE_AUTHOR_OUTPUT_V1",
        "assurance": "OWNER_APPROVED_SOURCE_OUTPUT_NOT_MATHEMATICAL_ACCEPTANCE",
        "module_name": source.stem, "source_root": str(source_root),
        "source": before_source, "setup": before_setup, "artifact_parts": output_pins}
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    need(0 < len(raw) <= MIB, "REFERENCE_AUTHOR_REPORT_BYTES")
    ordinary_path(str(report), fresh=True)
    with report.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
