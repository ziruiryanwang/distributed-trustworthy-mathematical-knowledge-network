"""Build module-public authoring support from exact selected existing sources.

Mechanical header-only generation keeps the old admission relation/artifacts
untouched. Lean rejects importing legacy helpers into a modern `module`, so
all four helper dependencies receive the same explicit public header. No Lean
runtime/Std rebuild, basis check, proof campaign or peer input is involved.
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
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"
MODULES = ("OriginalExpr", "OriginalDecl", "CheckedExtension", "BootstrapSupport")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def public_source(raw):
    """Change only a contiguous initial import block; preserve all body bytes."""
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    end = 0
    while end < len(lines) and lines[end].startswith("import "):
        end += 1
    if end == 0 or end >= len(lines) or lines[end].strip():
        raise ValueError("EXACT_LEGACY_IMPORT_HEADER_REQUIRED")
    imports = "".join("public " + line for line in lines[:end])
    transformed = ("module\n\n" + imports + "\npublic section\n" + "".join(lines[end:])).encode("utf-8")
    body = "".join(lines[end:]).encode("utf-8")
    if not transformed.endswith(body):
        raise ValueError("UNCHANGED_SUPPORT_BODY_REQUIRED")
    return transformed, body


def main():
    source, output = Path(__file__).resolve().parent, Path(sys.argv[1])
    if Path.cwd() != ROOT or not source.is_relative_to(LOCAL) or source.parents[2] != output / "sources":
        raise ValueError("SELECTED_SNAPSHOT_REQUIRED")
    first_sync = sys.argv[2:] == ["--first-sync"]
    remaining_sync = len(sys.argv) == 4 and sys.argv[2] == "--remaining-sync"
    if sys.argv[2:] and not (first_sync or remaining_sync):
        raise ValueError("SELECTED_BUILD_MODE")
    compiled_modules = (("OriginalExpr",) if first_sync else
                        (*MODULES[1:], "OwnerRebind") if remaining_sync else (*MODULES, "OwnerRebind"))
    inputs, build = output / "public-source", output / "lean-build"
    inputs.mkdir()
    build.mkdir()
    rows = []
    for module in (*MODULES, "OwnerRebind"):
        raw = (source / (module + ".lean")).read_bytes()
        if module == "OwnerRebind":
            generated, body = raw, raw
        else:
            generated, body = public_source(raw)
        with (inputs / (module + ".lean")).open("xb") as stream:
            stream.write(generated)
        rows.append({"module": module, "original_sha256": sha(raw),
                     "generated_sha256": sha(generated), "body_sha256": sha(body)})
    with (output / "PUBLIC-SOURCE-MAP.json").open("x", encoding="utf-8") as stream:
        json.dump(rows, stream, indent=2)
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(build)
    if remaining_sync:
        previous = Path(sys.argv[3])
        if not previous.is_absolute() or not previous.is_relative_to(LOCAL) or not previous.is_dir():
            raise ValueError("SELECTED_PREVIOUS_PUBLIC_BUILD")
        if ((previous.parent / "public-source/OriginalExpr.lean").read_bytes() !=
                (inputs / "OriginalExpr.lean").read_bytes()):
            raise ValueError("CHANGED_REUSED_PUBLIC_EXPRESSION_SOURCE")
        env["LEAN_PATH"] += os.pathsep + str(previous)
    steps = []
    for module in compiled_modules:
        argv = [str(LEAN), *(["-DElab.async=false"] if first_sync or remaining_sync else []),
                "-R", str(inputs), "-o", str(build / (module + ".olean")),
                str(inputs / (module + ".lean"))]
        start = time.monotonic()
        with (output / (module + ".stdout.txt")).open("xb") as out, \
             (output / (module + ".stderr.txt")).open("xb") as err:
            result = subprocess.run(argv, cwd=ROOT, env=env, stdout=out, stderr=err, timeout=45)
        step = {"module": module, "argv": argv, "exit_code": result.returncode,
                "wall_seconds": time.monotonic() - start}
        print(json.dumps(step), flush=True)
        if result.returncode:
            raise RuntimeError("PUBLIC_SUPPORT_COMPILE_FAILED:" + module)
        steps.append(step)
    result = {"status": "PASS_PUBLIC_HELPER_COMPILATION", "steps": steps,
              "mode": ("FIRST_MODULE_SYNCHRONOUS_ONLY" if first_sync else
                       "REMAINING_SYNCHRONOUS_REUSING_FIRST" if remaining_sync else "HELPER_CHAIN"),
              "claims": "AUTHORING_SUPPORT_COMPILE_NOT_CHANGED_RECEIVER_OR_OWNER_REUSE"}
    with (output / "COMPILE-RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
