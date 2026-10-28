"""Three disjoint inert CLI checks of the selected, relocated local kit."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MANIFEST = "0b027eedfc768a3dbde08c1b389b19fd316e17cf1cbe6c5b421e5cc735b86ec8"
PROFILE = "c8c8b5971e43361b7b09847b35b0e44c2645b284e59c59b90ab993136ccdb146"
REPORT = ROOT / "experiments/v5-local-checks/dedicated-host-preview01/RESULT.json"
REPORT_SHA = "77065fe33292368d3d4a177c4b836cf0bcf98128b0984a6178168734226c5113"
REQUEST = ROOT / "experiments/v5-local-checks/report-selection-controls01/controls/request-004.json"
REQUEST_SHA = "590d75c471c7de8445fa3c2830f4fa4f8aba3049baff31b0cd845820840c6917"


def need(ok, code):
    if not ok:
        raise ValueError("RELOCATED_" + code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--kit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "PYTHON")
    kit, output = Path(args.kit), Path(args.output)
    need(kit.is_absolute() and output.is_absolute() and not output.exists() and
         output.is_relative_to(ROOT / "experiments/v5-local-checks"), "PATHS")
    manifest_raw = (kit / "KIT-MANIFEST.json").read_bytes()
    need(sha(manifest_raw) == MANIFEST, "MANIFEST")
    manifest = json.loads(manifest_raw)
    for rel in ("kit.py", "file_helpers.py", "operator/prepare.py", "operator/prepare_selected.py",
                "operator/compatibility.json", "preview/view_preview.py", "preview/render.py"):
        raw = (kit / rel).read_bytes()
        need({"bytes": len(raw), "sha256": sha(raw)} == manifest["files"][rel], "SOURCE_PIN")
    need(sha(REPORT.read_bytes()) == REPORT_SHA and sha(REQUEST.read_bytes()) == REQUEST_SHA, "INPUT_PINS")
    output.mkdir()
    calls = {
        "manifest-refusal": [str(kit / "kit.py"), "verify", "--root", str(kit),
                             "--manifest-sha256", "0"*64],
        "prepare": [str(kit / "operator/prepare_selected.py"), "--package", str(kit / "package"),
                    "--profile-sha256", PROFILE, "--request", str(REQUEST), "--output", str(output / "prepared")],
        "preview": [str(kit / "preview/view_preview.py"), "--package", str(kit / "package"),
                    "--profile-sha256", PROFILE, "--report", str(REPORT), "--report-sha256", REPORT_SHA,
                    "--output", str(output / "view")],
    }

    def run(item):
        name, arguments = item
        argv = [sys.executable, "-I", "-S", "-B", *arguments]
        # These exact reviewed CLIs are finite and inert. The enclosing Job owns
        # hard resource/closure limits for this controller and all three children.
        result = subprocess.run(argv, cwd=kit, capture_output=True, timeout=45)
        need(len(result.stdout) <= 1024**2 and len(result.stderr) <= 1024**2, "LOG_BOUND")
        for suffix, raw in (("stdout.txt", result.stdout), ("stderr.txt", result.stderr)):
            with (output / (name + "." + suffix)).open("xb") as stream:
                stream.write(raw)
        if name == "manifest-refusal":
            need(result.returncode != 0 and b"KIT_MANIFEST_PIN" in result.stderr, "EXPECTED_REFUSAL")
        else:
            need(result.returncode == 0 and result.stderr == b"", "CLI_FAILED:" + name)
            json.loads(result.stdout)
        return {"name": name, "exit_code": result.returncode,
                "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, calls.items()))
    view = json.loads((output / "view/VIEW.json").read_bytes())
    need(view["status"] == "TYPE_DISPLAY_COMPLETE" and view["report_sha256"] == REPORT_SHA and
         view["selected_profile_sha256"] == PROFILE and not view["mathematical_acceptance"] and
         (output / "view/TYPE.txt").read_bytes() == view["view_text"].encode("ascii"), "PREVIEW_RESULT")
    prepared = json.loads((output / "prepared/arguments.json").read_bytes())
    need(prepared["profile_sha256"] == PROFILE and prepared["entry"] == "owner" and
         prepared["arguments"][0] == "contribute" and
         (output / "prepared/selection-disclosure.json").is_file(), "PREPARATION_RESULT")
    need((kit / "KIT-MANIFEST.json").read_bytes() == manifest_raw and
         sha(REPORT.read_bytes()) == REPORT_SHA and sha(REQUEST.read_bytes()) == REQUEST_SHA, "INPUT_CHANGED")
    summary = {"status": "PASS_RELOCATED_INERT_CLI", "commands": results, "manifest_sha256": MANIFEST,
               "profile_sha256": PROFILE, "mathematical_acceptance": False, "native_calls": 0,
               "claim": "RELOCATED_ENTRYPOINTS_NOT_NEW_MATHEMATICAL_OR_GROWTH_EVIDENCE"}
    raw = json.dumps(summary, sort_keys=True).encode("ascii")
    with (output / "RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode("ascii"))


if __name__ == "__main__":
    main()
