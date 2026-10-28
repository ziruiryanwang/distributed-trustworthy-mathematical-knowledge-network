"""Select one fresh recipient grounding step; file/JSON operations only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
HERE = "software/v5/ordinary_finite_map_refinement/fresh_recipient/"
PACKAGE = LOCAL / "frontier-launcher-package01/distribution/package"
PROFILE = "efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45"
ASSEMBLY = "d3b2ccc6f3cad7dcf5ebae1852840c6238cf555b1340de7797e910bb6b01ecf0"
IMPLEMENTATION = "86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea"
MANIFEST_SHA = "1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
CATALOG = LOCAL / "refinement-recipient-catalog01"
CUSTODY = LOCAL / "refinement-recipient-custody01"
STORE = hashlib.sha256(b"DMKN_REFINEMENT_RECIPIENT_OWNER_V1:recipient01").hexdigest()
STEPS = ["init", "prefix", "part-a", "part-b"]
COUNTS = {"prefix": [1024], "part-a": [620, 404], "part-b": [429, 174]}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read(path, expected=None):
    raw = path.read_bytes()
    need(expected is None or digest(raw) == expected, "INPUT_PIN:" + str(path))
    return json.loads(raw)


def fresh(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def clean(doc):
    need(doc["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and
         doc["child_exit_code"] == 0 and doc["direct_child_reaped"] and
         doc["job_closed"] and not doc["termination_requested"] and
         doc["cleanup_errors"] == [] and
         doc["final_job"]["active_processes"] == 0 and
         doc["final_job"]["terminated_processes"] == 0, "PREDECESSOR_NOT_CLEAN")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("step", choices=STEPS)
    step = parser.parse_args().step
    need(Path.cwd() == ROOT and Path(__file__).resolve() == ROOT / HERE / "select_grounding.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "CANONICAL_ISOLATED_SELECTOR")
    name = "refinement-recipient-" + step + "01"
    destination = LOCAL / (name + "-selection.json")
    need(not destination.exists() and not (LOCAL / name).exists(), "FRESH_OPERATION_REQUIRED")
    if step == "init":
        need(not CATALOG.exists() and not CUSTODY.exists(), "FRESH_OWNER_REQUIRED")
    pins = {}

    def retain(path, expected=None):
        actual = digest(path.read_bytes())
        need(expected is None or actual == expected, "INPUT_PIN:" + str(path))
        pins[str(path)] = actual
        return actual

    assembly_path = PACKAGE.parent / "ASSEMBLY.json"
    assembly = read(assembly_path, ASSEMBLY)
    retain(assembly_path, ASSEMBLY)
    need(assembly["implementation_id"] == IMPLEMENTATION and
         assembly["profile_sha256"] == PROFILE and len(assembly["files"]) == 154,
         "PACKAGE_IDENTITY")
    for relative, pin in assembly["files"].items():
        path = PACKAGE / relative
        need(path.stat().st_size == pin["bytes"], "PACKAGE_LENGTH")
        retain(path, pin["sha256"])
    # Reuse only actual runtime identities, not historical packages or outcomes.
    old = read(LOCAL / "std-kernel-init01.selection.json")
    for path, sha in old["runtime_pins"].items():
        p = Path(path)
        if p.is_relative_to(PYTHON) or p.is_relative_to(LEAN):
            retain(p, sha)
    need(len(pins) == 178, "PACKAGE_PLUS_RUNTIME_COUNT")
    args = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(PACKAGE / "run.py"),
            "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON),
            "--lean-runtime", str(LEAN), "--diagnostics", "{output}/public-launch",
            "--wall-seconds", "90" if step == "init" else "360",
            "--cpu-seconds", "60" if step == "init" else "300",
            "--memory-mib", "1280" if step == "init" else "1536",
            "--active-processes", "3", "--stdout-bytes", "1048576",
            "--stderr-bytes", "1048576", "owner", "--",
            "init" if step == "init" else "intake-baseline",
            "--catalog", str(CATALOG), "--custody", str(CUSTODY), "--store-id", STORE,
            "--custody-limits", "{snapshot}/software/v5/ordinary_std_intake/custody_limits.json"]
    if step != "init":
        predecessor = STEPS[STEPS.index(step)-1]
        previous = LOCAL / ("refinement-recipient-" + predecessor + "01")
        result = read(previous / "RESULT.json")
        clean(result["result"])
        clean(read(previous / "public-launch/SUPERVISION.json"))
        launch = read(previous / "public-launch/RUN.json")
        owner = read(previous / "public-launch/child/stdout.txt")
        need(launch["ok"] and launch["status"] == "CLI_EXITED_ZERO" and
             launch["profile_sha256"] == PROFILE and owner["ok"] and
             owner.get("close_errors", []) == [] and owner["profile_sha256"] == PROFILE and
             owner["implementation_id"] == IMPLEMENTATION and owner["store_id"] == STORE and
             owner["catalog"] == str(CATALOG) and owner["custody"] == str(CUSTODY),
             "ACTUAL_RECIPIENT_PREDECESSOR")
        accepted = owner["result"]
        if predecessor == "init":
            need(accepted["status"] == "INITIALIZED_LOCAL_OWNER" and
                 accepted["basis"]["status"] == "CHECKED" and
                 accepted["basis"]["units_checked"] == 456, "ACTUAL_CHECKED_BASIS")
            parent = accepted["basis"]["local_root"]
        else:
            need(accepted["status"] == "BASELINE_INTAKE_COMPLETE" and
                 [b["units_checked"] for b in accepted["batches"]] == COUNTS[predecessor] and
                 all(b["status"] == "CHECKED" for b in accepted["batches"]), "ACTUAL_CHECKED_PREFIX")
            parent = accepted["local_root"]
        for relative in ("RESULT.json", "selection.json", "public-launch/RUN.json",
                         "public-launch/SUPERVISION.json", "public-launch/child/stdout.txt"):
            retain(previous / relative)
        original_path = LOCAL / "std-reconstruct01/materialized/manifest.json"
        original = read(original_path, MANIFEST_SHA)
        retain(original_path, MANIFEST_SHA)
        if step == "prefix":
            manifest = dict(original, batches=[original["batches"][0]])
            manifest_path = LOCAL / "refinement-recipient-prefix-manifest01.json"
            fresh(manifest_path, canonical(manifest))
        else:
            manifest_path = LOCAL / ("std-kernel-suffix-inputs01/" + step + "-canonical.json")
            expected = {"part-a": "9eee85273f5fcbc0b91f9f0975c10bfad557b6cb555d334e580499fdf0fedb9c",
                        "part-b": "a0036d02cc15f0fb5a11d3b02a097870b12b81e963f10db26a9949d6b42b5c5c"}[step]
            manifest = read(manifest_path, expected)
        need([len(b) for b in manifest["batches"]] == COUNTS[step], "EXACT_WHOLE_UNIT_CUT")
        all_original = sum(original["batches"], [])
        start, end = {"prefix": (0, 1024), "part-a": (1024, 2048), "part-b": (2048, 2651)}[step]
        need(sum(manifest["batches"], []) == all_original[start:end] and
             manifest["semantic_id"] == original["semantic_id"] and
             manifest["schema"] == original["schema"], "ORIGINAL_UNITS_AND_ORDER")
        manifest_sha = retain(manifest_path)
        args += ["--parent-root", parent, "--bundle-directory", str(original_path.parent),
                 "--bundle-manifest", str(manifest_path), "--bundle-manifest-sha256", manifest_sha]
    sources = {relative: digest((ROOT / relative).read_bytes()) for relative in (
        "tools/Run-V5-Check.py", HERE + "select_grounding.py",
        "software/v5/ordinary_std_intake/custody_limits.json")}
    limits = dict(active_processes=4, cpu_seconds=90 if step == "init" else 330,
                  memory_mib=1536 if step == "init" else 1792, stderr_bytes=1048576,
                  stdout_bytes=4194304, wall_seconds=120 if step == "init" else 420)
    selection = dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=name, sources=sources,
                     runtime_pins=pins, argv=args, limits=limits)
    raw = canonical(selection)
    fresh(destination, raw)
    print(json.dumps(dict(selection=str(destination), sha256=digest(raw), store_id=STORE,
                          source_count=len(sources), external_pins=len(pins))))


if __name__ == "__main__":
    main()
