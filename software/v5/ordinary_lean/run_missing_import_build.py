"""Build only the changed exporter and new native missing-library entry point.

Four unchanged lower object/interface pairs are reused. This local build is
not mathematical acceptance and does not rebuild the installed Lean library.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
BIN = ROOT / "software/runtime/lean-4.34.0-windows/bin"
PRIOR = LOCAL / "ordinary-native-export-build-01/native-build"
LOWER = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport")


def need(ok, code):
    if not ok:
        raise ValueError(code)


def legacy_view(raw):
    """Only inverse public-module wrapping; all remaining body bytes retained."""
    lines = raw.splitlines(keepends=True)
    need(lines[0].strip() == b"module", "EXPECTED_MODULE_HEADER")
    output, sections, imports = [], 0, 0
    for line in lines[1:]:
        if line.strip() == b"public section":
            sections += 1
        elif line.startswith(b"public import "):
            output.append(line[len(b"public "):])
            imports += 1
        else:
            output.append(line)
    need(sections == 1 and imports == 3, "EXACT_PUBLIC_HEADER_TRANSFORM")
    return b"".join(output)


def main():
    source, output = Path(__file__).resolve().parent, Path(sys.argv[1])
    need(Path.cwd() == ROOT and source == output / "sources/software/v5/ordinary_lean"
         and output.is_absolute() and output.is_relative_to(LOCAL), "SELECTED_BUILD_REQUIRED")
    build = output / "native-build"
    view = output / "legacy-source"
    build.mkdir(); view.mkdir()
    selected = json.loads((output / "selection.json").read_bytes())
    for module in LOWER:
        for suffix in (".o", ".olean"):
            path = PRIOR / (module + suffix)
            raw = path.read_bytes()
            need(hashlib.sha256(raw).hexdigest() == selected["runtime_pins"][str(path)], "LOWER_PIN")
            if suffix == ".olean":
                with (build / path.name).open("xb") as stream:
                    stream.write(raw)
    transformed = legacy_view((source / "OrdinaryExport.lean").read_bytes())
    with (view / "OrdinaryExport.lean").open("xb") as stream:
        stream.write(transformed)
    with (view / "MissingImportExporter.lean").open("xb") as stream:
        stream.write((source / "MissingImportExporter.lean").read_bytes())
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("LEAN", "PYTHON"))}
    env["LEAN_PATH"] = str(build)
    env["PATH"] = str(BIN) + os.pathsep + env.get("PATH", "")
    deadline, steps = time.monotonic() + 130, []

    def run(label, argv):
        remaining = deadline - time.monotonic()
        need(remaining > 0, "BUILD_DEADLINE")
        with (output / (label + ".stdout.txt")).open("xb") as stdout, \
                (output / (label + ".stderr.txt")).open("xb") as stderr:
            result = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, timeout=remaining)
        steps.append({"phase": label, "exit_code": result.returncode})
        print(json.dumps(steps[-1]), flush=True)
        need(result.returncode == 0, "MISSING_IMPORT_BUILD_FAILED:" + label)

    for module in ("OrdinaryExport", "MissingImportExporter"):
        run(module + "-codegen", [str(BIN / "lean.exe"), "-R", str(view),
            "-o", str(build / (module + ".olean")), "-c", str(build / (module + ".c")),
            str(view / (module + ".lean"))])
        run(module + "-object", [str(BIN / "leanc.exe"), "-c", "-O0",
            str(build / (module + ".c")), "-o", str(build / (module + ".o"))])
    executable = build / "MissingImportExporter.exe"
    run("native-link", [str(BIN / "leanc.exe"), "-leanshared",
        *[str(PRIOR / (module + ".o")) for module in LOWER],
        str(build / "OrdinaryExport.o"), str(build / "MissingImportExporter.o"), "-o", str(executable)])
    raw = executable.read_bytes()
    result = {"status": "PASS_MISSING_IMPORT_BUILD_ONLY", "steps": steps,
        "legacy_export_view_sha256": hashlib.sha256(transformed).hexdigest(),
        "executable_bytes": len(raw), "executable_sha256": hashlib.sha256(raw).hexdigest(),
        "claims": "NATIVE_BUILD_NOT_EXPORT_OR_ADMISSION"}
    with (output / "BUILD-RESULT.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
