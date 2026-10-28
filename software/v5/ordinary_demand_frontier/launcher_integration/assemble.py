"""Exact file-only launcher overlay; no product imports, compiler or state."""
import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
BASE = LOCAL / "demand-frontier-package01/distribution/package"
BASE_RECEIPT = "6ada680868401735ea4abd2fb04b43c064b67d78da7eb46db1032c0b590517a8"
BASE_PROFILE = "6af0c3dee0a08d0ba0ec9f126dc6510481fc99569535c41b4ecb56c4bf3c3735"
INSTALLATION = "9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27"
HELPER = "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
PREFIX = "software/v5/ordinary_demand_frontier/"
PAYLOADS = {
    "run.py": ("run_frontier.py", "63f70a8f27645e4e3e3f2ae85296f9c43bc2f0337b4534744dbd5eb0411029dd"),
    "LAUNCHER.md": ("launcher_integration/LAUNCHER.md", "66b58b9512df12b2e4bed0b18fd81f1343e406293a3ac68ef135eaa41cc3173a"),
}


def main():
    start, cpu = time.monotonic(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[4]
    if not (Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
            sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and
            Path(sys.executable).resolve() == Path(r"D:\Python314\python.exe") and
            source.name == "sources" and source.parent.parent == LOCAL and
            Path(__file__).resolve() == source / PREFIX / "launcher_integration/assemble.py"):
        raise ValueError("LAUNCHER_ASSEMBLY_SELECTED_PROCESS")
    helper_path = source / HELPER
    raw = helper_path.read_bytes()
    if len(raw) > 2 * 1024**2 or hashlib.sha256(raw).hexdigest() != HELPER_SHA:
        raise ValueError("LAUNCHER_ASSEMBLY_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_launcher_file_helpers", helper_path)
    H = importlib.util.module_from_spec(spec)
    if spec.name in sys.modules:
        raise ValueError("LAUNCHER_ASSEMBLY_PRELOADED_HELPER")
    sys.modules[spec.name] = H
    exec(compile(raw, str(helper_path), "exec"), H.__dict__)

    def check():
        H.need(time.monotonic() - start < 60 and time.process_time() - cpu < 30,
               "LAUNCHER_ASSEMBLY_ALLOWANCE")

    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    H.need(output == source.parent / "distribution", "LAUNCHER_OUTPUT_SCOPE")
    receipt, _ = H.read_json(BASE.parent / "ASSEMBLY.json", BASE_RECEIPT, check)
    profile, profile_pin = H.read_json(BASE / "PROFILE.json", BASE_PROFILE, check)
    baseline = receipt["files"]
    H.need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and receipt["package"] == str(BASE) and
           receipt["profile_sha256"] == BASE_PROFILE and
           receipt["installation_manifest_sha256"] == profile["installation_manifest_sha256"] == INSTALLATION and
           baseline["PROFILE.json"] == profile_pin and len(baseline) == 154 and
           len(profile["files"]) == 117 and
           all(baseline.get(n) == p for n, p in profile["files"].items()), "LAUNCHER_EXACT_BASE")
    H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.relative(name); H.pin_shape(pin)
        H.need(H.pin(BASE / name, check) == pin, "LAUNCHER_BASE_PIN")
    selected = {n: BASE / n for n in baseline if n != "PROFILE.json"}
    expected = dict(baseline)
    for name, (relative, digest) in PAYLOADS.items():
        path = source / PREFIX / relative
        pin = H.pin(path, check, 2 * H.MIB)
        H.need(pin["sha256"] == digest and pin != baseline[name], "LAUNCHER_REPLACEMENT_PIN")
        selected[name], expected[name] = path, pin
    new_profile = H.canonical(dict(profile, files=dict(profile["files"], **{"run.py": expected["run.py"]})))
    expected["PROFILE.json"] = {"bytes": len(new_profile), "sha256": H.digest(new_profile)}
    changed = sorted(n for n in expected if expected[n] != baseline[n])
    H.need(changed == ["LAUNCHER.md", "PROFILE.json", "run.py"] and
           sum(p["bytes"] for p in expected.values()) <= 256 * H.MIB, "LAUNCHER_EXACT_DELTA")
    output.mkdir(); package = output / "package"; package.mkdir()
    for name, origin in sorted(selected.items()):
        check(); target = package / H.relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        H.ordinary(target.parent, directory=True)
        with H.ordinary(origin).open("rb") as incoming, H.ordinary(target, fresh=True).open("xb") as outgoing:
            shutil.copyfileobj(incoming, outgoing, H.MIB)
            outgoing.flush(); os.fsync(outgoing.fileno())
        H.need(H.pin(target, check) == expected[name], "LAUNCHER_COPY_READBACK")
    H.census(package, selected, check); H.census(BASE, baseline, check)
    for name, pin in baseline.items():
        H.need(H.pin(BASE / name, check) == pin, "LAUNCHER_BASE_CHANGED")
    for name, origin in selected.items():
        H.need(H.pin(origin, check) == expected[name] and H.pin(package / name, check) == expected[name],
               "LAUNCHER_SOURCE_OR_OUTPUT_CHANGED")
    H.need(H.pin(helper_path, check)["sha256"] == HELPER_SHA, "LAUNCHER_HELPER_CHANGED")
    H.fresh_bytes(package / "PROFILE.json", new_profile)
    H.census(package, expected, check)
    H.need(H.pin(package / "PROFILE.json", check) == expected["PROFILE.json"], "LAUNCHER_FINAL_PROFILE")
    report = {"status": "ASSEMBLED_NOT_ADOPTED", "package": str(package), "files": expected,
        "base_receipt_sha256": BASE_RECEIPT, "base_profile_sha256": BASE_PROFILE,
        "profile_sha256": expected["PROFILE.json"]["sha256"], "installation_manifest_sha256": INSTALLATION,
        "implementation_id": receipt["implementation_id"], "changed_files": changed,
        "unchanged_files": len(expected) - len(changed), "native_calls": 0, "owner_opened": False,
        "wall_seconds": time.monotonic() - start, "cpu_seconds": time.process_time() - cpu,
        "claim": "LAUNCHER_FILE_OVERLAY_NOT_RUNTIME_OR_MATHEMATICAL_ACCEPTANCE"}
    H.fresh_bytes(output / "ASSEMBLY.json", H.canonical(report)); check()
    print(H.canonical(report).decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()
