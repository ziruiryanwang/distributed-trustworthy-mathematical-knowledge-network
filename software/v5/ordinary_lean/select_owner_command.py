"""File-only selection of the changed producer-command route; never executes it."""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if Path.cwd() != ROOT:
        raise ValueError("CANONICAL_ROOT_REQUIRED")
    old = LOCAL / "ordinary-owner-export-01/selection.json"
    if digest(old) != "293dc9befaafc41a6324cb71903136d9eced11a21537f2086738a7c35ce115ff":
        raise ValueError("PRIOR_SELECTION_IDENTITY")
    value = json.loads(old.read_bytes())
    value["name"] = "ordinary-owner-command-02"
    value["sources"] = {rel: digest(ROOT / rel) for rel in (
        "tools/Run-V5-Check.py", "software/v5/ordinary_lean/OwnerExportCommand.lean",
        "software/v5/ordinary_lean/run_owner_command.py",
        "software/v5/ordinary_lean/select_owner_command.py")}
    # Drop only the former receiver/snapshot/CLI dependencies not imported by
    # this producer command. Preserve exact producer/compiler/exporter pins.
    unused = {"LocalSnapshot.lean", "LocalSnapshot.olean", "BasisSnapshot.lean",
              "BasisSnapshot.olean", "OrdinaryWorkflowWorker.lean", "OrdinaryWorkflowWorker.olean"}
    value["runtime_pins"] = {p: sha for p, sha in value["runtime_pins"].items()
                             if Path(p).name not in unused}
    for relative in ("lean-build/OwnerExportCommand.olean",
                     "sources/software/v5/ordinary_lean/OwnerExportCommand.lean"):
        compiled = LOCAL / "ordinary-owner-command-01" / relative
        value["runtime_pins"][str(compiled)] = digest(compiled)
    for path, sha in value["runtime_pins"].items():
        if digest(Path(path)) != sha:
            raise ValueError("CHANGED_PREREQUISITE:" + path)
    value["argv"] = [r"D:\Python314\python.exe", "-I", "-S", "-B",
                     r"{snapshot}\software\v5\ordinary_lean\run_owner_command.py", "{output}"]
    # Exactly the failed route's finite allowance, not a cap increase.
    assert value["limits"]["memory_mib"] == 1536
    target = LOCAL / "ordinary-owner-command-02-selection.json"
    raw = (json.dumps(value, indent=2) + "\n").encode()
    with target.open("xb") as stream:
        stream.write(raw)
    print(str(target))
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
