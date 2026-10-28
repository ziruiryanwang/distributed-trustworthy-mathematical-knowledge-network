"""Create one exact exchange selection from saved results; never launch/open state."""
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
IMPLEMENTATION = "86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea"
PYTHON = Path(r"D:\Python314")
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
B = (LOCAL / "refinement-recipient-catalog01", LOCAL / "refinement-recipient-custody01",
     hashlib.sha256(b"DMKN_REFINEMENT_RECIPIENT_OWNER_V1:recipient01").hexdigest())
A = (LOCAL / "std-kernel-catalog01", LOCAL / "std-kernel-custody01",
     "fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7")
INDEX = LOCAL / "refinement-recipient-index01"
STEPS = ("serve-a", "receive-b", "contribute-b", "publish-b", "serve-b", "receive-a")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(doc):
    return json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def fresh(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def clean(doc):
    need(doc["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and doc["child_exit_code"] == 0
         and doc["direct_child_reaped"] and doc["job_closed"]
         and not doc["termination_requested"] and not doc["cleanup_errors"]
         and doc["final_job"]["active_processes"] == 0
         and doc["final_job"]["terminated_processes"] == 0, "PREDECESSOR_NOT_CLEAN")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("step", choices=STEPS)
    step = parser.parse_args().step
    need(Path.cwd() == ROOT and Path(__file__).resolve() == ROOT / HERE / "select_exchange.py"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "CANONICAL_ISOLATED_SELECTOR")
    name = "refinement-recipient-" + step + "01"
    destination = LOCAL / (name + "-selection.json")
    config_path = LOCAL / (name + "-config.json")
    need(not destination.exists() and not config_path.exists() and not (LOCAL / name).exists(),
         "FRESH_OPERATION_REQUIRED")
    pins = {}

    def read(path):
        raw = path.read_bytes()
        pins[str(path)] = sha(raw)
        return json.loads(raw)

    # Copy exact already-used package/runtime pins; Run-V5-Check verifies current
    # bytes before launch. No historical outcome pins or fresh owner logic copied.
    ground_selection = read(LOCAL / "refinement-recipient-part-b01/selection.json")
    for path, pin in ground_selection["runtime_pins"].items():
        p = Path(path)
        if (p.is_relative_to(PACKAGE) or p.is_relative_to(PYTHON) or
                p.is_relative_to(LEAN) or p == PACKAGE.parent / "ASSEMBLY.json"):
            pins[path] = pin
    need(len(pins) == 179 and pins[str(PACKAGE / "PROFILE.json")] == PROFILE,
         "EXACT_178_PACKAGE_RUNTIME_PINS")

    def completed(operation, owner):
        run = LOCAL / ("refinement-recipient-" + operation + "01")
        clean(read(run / "RESULT.json")["result"])
        clean(read(run / "public-launch/SUPERVISION.json"))
        launcher = read(run / "public-launch/RUN.json")
        doc = read(run / "public-launch/child/stdout.txt")
        read(run / "selection.json")
        need(launcher["ok"] and launcher["status"] == "CLI_EXITED_ZERO" and
             launcher["profile_sha256"] == PROFILE and doc["ok"] and
             doc["profile_sha256"] == PROFILE and doc["implementation_id"] == IMPLEMENTATION and
             doc["catalog"] == str(owner[0]) and doc["custody"] == str(owner[1]) and
             doc["store_id"] == owner[2] and not doc.get("close_errors", []),
             "ACTUAL_OWNER_PREDECESSOR")
        result = doc["result"]
        need(not result.get("cleanup_errors", []), "PREDECESSOR_CLEANUP")
        return result

    std = completed("part-b", B)
    need(std["status"] == "BASELINE_INTAKE_COMPLETE" and
         [b["units_checked"] for b in std["batches"]] == [429, 174] and
         all(b["status"] == "CHECKED" for b in std["batches"]), "ACTUAL_B_STD_ROOT")
    std_root = std["local_root"]
    source_files = ["tools/Run-V5-Check.py", HERE + "select_exchange.py",
                    "software/v5/ordinary_std_intake/custody_limits.json"]

    def template(filename):
        source_files.append(HERE + filename)
        return read(ROOT / HERE / filename)

    def endpoint(operation, owner):
        run = LOCAL / ("refinement-recipient-" + operation + "01")
        selection = read(run / "selection.json")
        need(selection["name"] == run.name and not (run / "RESULT.json").exists(),
             "EXPECTED_LIVE_SERVICE")
        ready = read(run / "peer/READY.json")
        need(ready["status"] == "READY" and ready["host"] == "127.0.0.1" and
             type(ready["port"]) is int and 1 <= ready["port"] <= 65535 and
             ready["tls"] is False and ready["shared_custody"] == str(owner[1]),
             "ACTUAL_LOCAL_READY")
        return dict(host=ready["host"], port=ready["port"], tls=False,
                    server_name=None, ca_file=None, ca_sha256=None)

    owner = A if step in ("serve-a", "receive-a") else B
    public = [150, 90, 1536, 6]
    outer = [180, 110, 2048, 8]
    config = None
    if step == "serve-a":
        config = template("a-serve.json")
        public, outer = [210, 60, 1536, 3], [240, 90, 1792, 4]
        read(LOCAL / "finite-map-refinement-publication01/publication/RESULT.json")
    elif step == "receive-b":
        config = template("b-receive-template.json")
        config["contacts"]["a"] = endpoint("serve-a", A)
        config["parent_root"] = std_root
        publication = read(LOCAL / "finite-map-refinement-publication01/publication/RESULT.json")
        need(any(config["selection"]["record"] == p["record"] and
                 config["selection"]["snapshot_id"] == p["snapshot_id"]
                 for p in publication["result"]["publications"]), "ACTUAL_A_PUBLICATION")
    elif step == "contribute-b":
        served = completed("serve-a", A)
        need(served["status"] == "LEASE_FINISHED" and served["quiescent"], "A_OFFLINE")
        received = completed("receive-b", B)
        acquired = template("acquired-targets.json")
        need(received["status"] == "CHECKED" and received["local_acceptance_available"] and
             received["admission"]["status"] == "CHECKED" and
             received["admission"]["units_checked"] == 37 and
             received["parent_root"] == std_root and received["target"] == acquired[0],
             "ACTUAL_CHECKED_RECEIVED_THEORY")
        parent = received["admission"]["local_root"]
        source_files += [HERE + f for f in ("Body.lean", "output-names.json", "project-authoring.json")]
        prior = read(LOCAL / "finite-map-refinement-contribution02/selection.json")
        std_pins = {p: h for p, h in prior["runtime_pins"].items()
                    if Path(p).parent == LEAN / "lib/lean/Std/Data/HashMap"}
        need(len(std_pins) == 5, "EXACT_INSTALLED_IMPORT_PINS")
        pins.update(std_pins)
    else:
        contribution = completed("contribute-b", B)
        need(contribution["status"] == "CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES" and
             contribution["admission"]["status"] == "CHECKED" and
             len(contribution["units"]) == len(contribution["targets"]) == 1 and
             contribution["units"][0]["bytes"] <= 1048576,
             "ACTUAL_ONE_UNIT_RETURN_REQUIRED")
        if step == "publish-b":
            need(not INDEX.exists(), "FRESH_B_INDEX")
            config = template("b-publish-template.json")
            config.update(context_root=contribution["local_root"], targets=contribution["targets"])
            config["index"]["path"] = str(INDEX)
            public, outer = [60, 30, 768, 3], [90, 45, 1024, 4]
        else:
            publication = completed("publish-b", B)
            need(publication["status"] == "INDEXED_LOCAL_TARGETS" and
                 publication["local_context"] == contribution["local_root"] and
                 len(publication["publications"]) == 1, "ACTUAL_B_PUBLICATION")
            if step == "serve-b":
                config = template("b-serve-template.json")
                config["index"]["path"] = str(INDEX)
                public, outer = [120, 30, 768, 3], [150, 45, 1024, 4]
            else:
                config = template("a-receive-template.json")
                config["contacts"]["b"] = endpoint("serve-b", B)
                p = publication["publications"][0]
                config["selection"] = dict(provider="b", snapshot_id=p["snapshot_id"], record=p["record"])

    argv = [str(PYTHON / "python.exe"), "-I", "-S", "-B", str(PACKAGE / "run.py"),
            "--profile-sha256", PROFILE, "--python-runtime", str(PYTHON), "--lean-runtime", str(LEAN),
            "--diagnostics", "{output}/public-launch"]
    for flag, value in zip(("wall-seconds", "cpu-seconds", "memory-mib", "active-processes"), public):
        argv += ["--" + flag, str(value)]
    argv += ["--stdout-bytes", "1048576", "--stderr-bytes", "1048576"]
    argv += ["owner" if step == "contribute-b" else "peer", "--", step.split("-")[0]]
    argv += ["--catalog", str(owner[0]), "--custody", str(owner[1]), "--store-id", owner[2],
             "--custody-limits", "{snapshot}/software/v5/ordinary_std_intake/custody_limits.json"]
    if config is not None:
        raw = encode(config)
        need(b"__" not in raw, "UNRESOLVED_DYNAMIC_CONFIG")
        fresh(config_path, raw)
        pins[str(config_path)] = sha(raw)
        argv += ["--config", str(config_path), "--config-sha256", sha(raw), "--output", "{output}/peer"]
    else:
        argv += ["--parent-root", parent, "--authoring-frontier-root", std_root]
        for flag, file in (("source", "Body.lean"), ("acquired-targets", "acquired-targets.json"),
                           ("output-names", "output-names.json"), ("project-authoring", "project-authoring.json")):
            argv += ["--" + flag, "{snapshot}/" + HERE + file]
        argv += ["--project-authoring-sha256", sha((ROOT / HERE / "project-authoring.json").read_bytes()),
                 "--output", "{output}/contribution"]
    sources = {f: sha((ROOT / f).read_bytes()) for f in source_files}
    need(len(pins) <= 256, "EXTERNAL_PIN_CAP")
    limits = dict(zip(("wall_seconds", "cpu_seconds", "memory_mib", "active_processes"), outer))
    limits.update(stdout_bytes=4194304, stderr_bytes=1048576)
    raw = encode(dict(schema="DMKN_V5_LOCAL_CHECK_V1", name=name, sources=sources,
                      runtime_pins=pins, argv=argv, limits=limits))
    fresh(destination, raw)
    print(json.dumps(dict(selection=str(destination), sha256=sha(raw), external_pins=len(pins),
                          source_count=len(sources), b_std_root=std_root)))


if __name__ == "__main__":
    main()
