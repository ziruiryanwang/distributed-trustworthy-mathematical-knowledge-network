"""Finite file-only selection for the new portable catalog storage boundary."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if Path.cwd() != ROOT or len(sys.argv) != 2 or not re.fullmatch(r"ordinary-[a-z0-9-]{1,54}", sys.argv[1]):
        raise ValueError("CANONICAL_NAME_REQUIRED")
    name = sys.argv[1]
    path = LOCAL / (name + ".selection.json")
    if path.exists() or (LOCAL / name).exists():
        raise ValueError("FRESH_SELECTION_REQUIRED")
    prior = json.loads((LOCAL / "ordinary-owner-consumer-05/selection.json").read_bytes())
    pins = {p: prior["runtime_pins"][p] for p in
            (r"D:\Python314\python.exe", r"D:\Python314\python314.dll", r"D:\Python314\python3.dll")}
    for filename, expected in pins.items():
        if sha(Path(filename)) != expected:
            raise ValueError("PYTHON_RUNTIME_PIN")
    sources = ["tools/Run-V5-Check.py"] + ["software/v5/ordinary_lean/" + filename for filename in
        ("portable_catalog_checks.py", "select_portable_catalog_checks.py", "portable_catalog.py",
         "ordinary_semantics.py", "portable_evidence.py", "ordinary_evidence.py", "local_catalog.py",
         "semantic_identity_checks.py")]
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": {relative: sha(ROOT / relative) for relative in sources}, "runtime_pins": pins,
        "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
                 r"{snapshot}\software\v5\ordinary_lean\portable_catalog_checks.py",
                 "--store-root", r"{output}\inert-stores"],
        "limits": {"cpu_seconds": 30, "wall_seconds": 60, "memory_mib": 256,
                   "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    raw = (json.dumps(selection, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"selection": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
                      "execution": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
