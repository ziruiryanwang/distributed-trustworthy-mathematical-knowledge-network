"""Fresh file-only selection for the four changed ordinary-discovery seams."""
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
    if Path.cwd() != ROOT or len(sys.argv) != 2 or not re.fullmatch(r"ordinary-[a-z0-9-]+", sys.argv[1]):
        raise ValueError("CANONICAL_SELECTED_NAME_REQUIRED")
    name = sys.argv[1]
    prior = json.loads((LOCAL / "ordinary-owner-consumer-05/selection.json").read_bytes())
    pins = {path: prior["runtime_pins"][path] for path in (
        r"D:\Python314\python.exe", r"D:\Python314\python314.dll", r"D:\Python314\python3.dll")}
    for path, expected in pins.items():
        if sha(Path(path)) != expected:
            raise ValueError("PYTHON_RUNTIME_PIN")
    sources = ["tools/Run-V5-Check.py"]
    sources += ["software/v5/discovery/" + name for name in (
        "ordinary_export_adapter_checks.py", "select_ordinary_discovery_checks.py",
        "ordinary_export_adapter.py", "formal_features.py", "authenticated_index.py",
        "discovery_store.py", "discovery_query.py", "candidate_query.py")]
    sources += ["software/v5/ordinary_lean/" + name for name in (
        "ordinary_evidence.py", "ordinary_preview.py", "ordinary_semantics.py",
        "portable_evidence.py", "portable_preview.py")]
    value = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": name,
        "sources": {relative: sha(ROOT / relative) for relative in sources}, "runtime_pins": pins,
        "argv": [r"D:\Python314\python.exe", "-I", "-S", "-B",
                 r"{snapshot}\software\v5\discovery\ordinary_export_adapter_checks.py",
                 "--store-root", r"{output}\index-store"],
        "limits": {"cpu_seconds": 30, "wall_seconds": 60, "memory_mib": 256,
                   "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576}}
    path = LOCAL / (name + ".selection.json")
    if path.exists() or (LOCAL / name).exists():
        raise ValueError("FRESH_SELECTION_REQUIRED")
    raw = (json.dumps(value, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"selection": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "execution": "NOT_STARTED"}))


if __name__ == "__main__":
    main()
