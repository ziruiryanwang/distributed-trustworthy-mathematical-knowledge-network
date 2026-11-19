"""Read-only saved-evidence audit. Never imports or executes project code."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CYCLE = ROOT / "research/cycles/v5-2026-10-20"
RUN = ROOT / "experiments/v5-local-checks/managed-operator-lifecycle-01"
INSTALL = ROOT / "product-local/v5-distribution-managed-owner-01/Mathematical Commons v5"
COUNT = {"outer_snapshots": 0, "runtime_pins": 0, "boot_sources": 0, "artifacts": 0}


def raw(path):
    p = Path(path)
    assert p.is_absolute() and p.is_file() and not p.is_symlink() and not p.is_junction(), p
    return p.read_bytes()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def compact(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def domain(name, value):
    return sha(name.encode("ascii") + b"\0" + compact(value))


def parse(value):
    def pairs(items):
        result = {}
        for key, item in items:
            assert key not in result
            result[key] = item
        return result
    return json.loads(value, object_pairs_hook=pairs)


def load(path):
    return parse(raw(path))


def pin(path, digest, size=None):
    value = raw(path)
    assert sha(value) == digest, path
    if size is not None:
        assert len(value) == size, path
    return value


def clean(value, evidence):
    assert value["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
    assert value["child_exit_code"] == 0 and value["direct_child_reaped"] is True
    assert value["job_closed"] is True and value["cleanup_errors"] == []
    assert value["termination_requested"] is False
    assert value["final_job"]["active_processes"] == value["final_job"]["terminated_processes"] == 0
    command = load(evidence / "command.json")
    assert command == {key: value[key] for key in ("argv", "cwd", "limits")}
    for name in ("stdout", "stderr"):
        assert len(raw(evidence / (name + ".txt"))) == value["observed_logs"][name + "_bytes"]
    assert value["final_job"]["cpu_seconds"] <= value["limits"]["cpu_seconds"]


selection_path = RUN.parent / "managed-operator-lifecycle-01-selection.json"
selection_raw = pin(selection_path, "aac5291b234e237e19f75e934fbb8ecf39971027743b85c206035f2f837b4007", 43164)
assert raw(RUN / "selection.json") == selection_raw
selection = parse(selection_raw)
outer = parse(pin(RUN / "RESULT.json", "ddfe5243753d66539c7b0325e039b6c29ee6694d1010a7cf4c853d88d39944f2", 2300))
inner = parse(pin(RUN / "managed-operator-lifecycle-01-result.json", "c0640cda6b4976703dea1b577e30846cb8564ef6959bc17d64f4cda6b0c0d686", 26055))
input_path = RUN.parent / "managed-operator-lifecycle-01-input.json"
supplied = parse(pin(input_path, "4aa1ae631f776021736711a5d6477aba5b68e665cd1b3440bb247e8e2a4ae5d8", 705))
assert outer["selection_sha256"] == sha(selection_raw)
assert inner["input_sha256"] == sha(raw(input_path)) and inner["status"] == "PASS" and inner["stage"] == "complete"
assert inner["error"] if "error" in inner else True
assert "error" not in inner
assert [op["name"] for op in inner["operations"]] == ["serve", "status", "retire", "reclaim"]
assert len(selection["sources"]) == 2 and len(selection["runtime_pins"]) == 155
for relative, digest in selection["sources"].items():
    pin(ROOT / relative, digest)
    pin(RUN / "sources" / relative, digest)
    COUNT["outer_snapshots"] += 1
for filename, digest in selection["runtime_pins"].items():
    pin(filename, digest)
    COUNT["runtime_pins"] += 1
clean(outer["result"], RUN / "command")
assert outer["result"]["limits"] == selection["limits"]
expected_argv = [arg.replace("{snapshot}", str(RUN / "sources")).replace("{output}", str(RUN)) for arg in selection["argv"]]
assert outer["result"]["argv"] == expected_argv
assert parse(raw(RUN / "command/stdout.txt")) == {"status": "PASS", "stage": "complete", "wall_seconds": inner["wall_seconds"]}
assert raw(RUN / "command/stderr.txt") == b""
release_raw = pin(INSTALL / "V5-RELEASE.json", "8fcf2c971029c8ad0787ec8da0891be178a95b80999f8bccc262e077009701a2")
release = parse(release_raw)
assert supplied["release_sha256"] == inner["release_sha256"] == sha(release_raw)
assert supplied["installation_root"] == str(INSTALL)
build = load(RUN.parent / "distribution-managed-owner-01-input.json")
assert release["build_input_sha256"] == sha(raw(RUN.parent / "distribution-managed-owner-01-input.json"))
sdk = {logical: release["files"][relative] for logical, relative in release["sdk_sources"].items()}
assert len(sdk) == len(build["sdk_sources"]) == 126
for logical, row in sdk.items():
    assert row == {key: build["sdk_sources"][logical][key] for key in ("bytes", "sha256")}
base_raw = pin(INSTALL / "base/RELEASE-MANIFEST.json", "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed")
base = parse(base_raw)
helpers = {name: base["files"][name] for name in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py")}
profile = domain("DMKN-V5-INSTALLED-MANAGED-WORKER-V1", {
    "release_sha256": sha(release_raw), "base_manifest_sha256": sha(base_raw), "sources": sdk,
    "owner_entry": "managed_owner.py", "helpers": helpers, "role": "DMKN_V5_MANAGED_OWNER_WORKER_V1",
    "ownership": "PRIVATE_FIXED_WORKER_NO_EXTERNAL_WRITERS_OR_OUT_OF_JOB_LAUNCHERS_V1"})
assert profile == inner["profile_sha256"]
selected = {**sdk, "owner/managed_owner.py": sdk["v5/client/managed_owner.py"]}


def bootcheck(run, plan, boot):
    assert plan["sources"] == selected and boot["source_files"] == 127
    assert boot["source_bytes"] == sum(row["bytes"] for row in selected.values()) == 1661192
    assert boot["status"] == "OWNER_EXITED_ZERO" and boot["plan_sha256"] == sha(raw(run / "plan.json"))
    assert boot["job_membership"] == "OS_CONFIRMED_MEMBERSHIP_LIMITS_AND_CLOSURE_REPORTED_BY_PARENT"
    for logical, row in selected.items():
        pin(run / "sources" / logical, row["sha256"], row["bytes"])
        COUNT["boot_sources"] += 1
    for logical in boot["imported_origins"].values():
        assert logical.replace("\\", "/") in selected
    for module in ("placement.lifecycle", "placement.sessions", "placement.reclaim", "client.serve_generations"):
        assert boot["imported_origins"][module].replace("\\", "/") == "v5/" + module.replace(".", "/") + ".py"
    assert not (run / "BOOT-FAILED.json").exists()


results, plans, origin_counts = {}, {}, {}
for operation in inner["operations"]:
    name = operation["name"]
    run = RUN / "operations" / name
    values = {}
    for kind, row in operation["artifacts"].items():
        values[kind] = parse(pin(row["path"], row["sha256"], row["bytes"]))
        COUNT["artifacts"] += 1
    request_raw = pin(RUN / "inputs" / (name + ".json"), operation["request_sha256"])
    assert request_raw == raw(RUN / "operations" / (name + "-request") / "request.json")
    request = parse(request_raw)
    parameters = request["parameters"]
    assert parameters["manager_config"] == inner["manager_config"] and parameters["manager_root"] == inner["manager_root"]
    assert parameters["operation"] == name and request["runtime_mode"] == "atomic"
    assert request["owner"] == {"root": str(INSTALL / "sdk/v5/client"), "entry": "managed_owner.py", "sources": {"managed_owner.py": sdk["v5/client/managed_owner.py"]}}
    plan, boot, launch, result = (values[key] for key in ("plan", "boot", "launch", "owner"))
    assert raw(run / "plan.json") == raw(RUN / "operations" / (name + "-request") / "launch.json")
    assert plan["parameters"] == parameters and plan["limits"] == request["limits"]
    assert plan["installation_root"] == str(INSTALL / "base")
    assert plan["source_roots"] == {key: str(INSTALL / "sdk" / path) for key, path in (("owner", "v5/client"), ("portable", "portable"), ("v5", "v5"))}
    bootcheck(run, plan, boot)
    origin_counts[name] = len(boot["imported_origins"])
    assert launch["final_error"] is None and launch["plan_sha256"] == sha(raw(run / "plan.json"))
    clean(launch["result"], run / "command")
    clean(operation["supervision"], RUN / "public-commands" / name)
    assert operation["supervision"] == load(RUN / "public-commands" / (name + "-result.json"))
    assert parse(raw(RUN / "public-commands" / name / "stdout.txt")) == launch
    assert operation["supervision"]["argv"] == [str(INSTALL / "base/receiver/runtime/python/python.exe"), "-I", "-S", "-B", str(INSTALL / "distribution.py"), "launch", sha(release_raw), "run", str(RUN / "inputs" / (name + ".json")), sha(request_raw)]
    assert result["status"] == "COMPLETE" and result["operation"] == name and result["profile_sha256"] == profile
    assert all(result[key] is False for key in ("mathematical_acceptance", "global_complete", "public_deployment_qualified"))
    results[name], plans[name] = result, plan

serve = results["serve"]
worker_run = RUN / "operations/serve/work/managed-worker"
worker = load(worker_run / "work/managed-result.json")
worker_plan, worker_boot = load(worker_run / "plan.json"), load(worker_run / "BOOT-RESULT.json")
bootcheck(worker_run, worker_plan, worker_boot)
origin_counts["worker"] = len(worker_boot["imported_origins"])
assert serve["worker"] == worker and serve["worker_boot"] == worker_boot
assert worker_plan["parameters"] == {"schema": "DMKN_V5_MANAGED_OWNER_WORKER_V1", "request": plans["serve"]["parameters"], "profile_sha256": profile}
assert worker_plan["source_roots"] == {key: str(RUN / "operations/serve/sources" / key) for key in ("owner", "portable", "v5")}
assert worker_plan["limits"] == plans["serve"]["parameters"]["inner_limits"]
assert serve["worker_plan_sha256"] == sha(raw(worker_run / "plan.json"))
nested = serve["supervision"]
clean(nested, RUN / "operations/serve/work/managed-supervisor")
assert nested["session_recovery"] == {"status": "QUIESCED", "unclean_slots": [], "orderly_close_claim": False, "mathematical_acceptance": False}
assert worker["status"] == "COMPLETE" and not worker.get("close_errors")
assert worker["profile_sha256"] == profile and worker["restored"] == []
record = worker["manager"]["slots"][0]
generation = inner["generation"]
assert generation == serve["generation"] == worker["generation"] == record["generation"]
assert record["run_state"] == "CLOSED" and record["phase"] == "SEALED_SERVING"
assert record["runs"] == record["sequence"] == 1 and record["slot"] == 0
assert record["failure"] is None and "quiescence" not in record
assert worker["manager"]["slots"][1] is None and worker["allocation"]["runs"] == 0
assert worker["sealed"]["phase"] == "SEALED_SERVING" and worker["sealed"]["run_state"] == "LIVE"
assert len(worker["closures"]) == 1
closure = worker["closures"][0]
assert closure["status"] == "CLOSED" and closure["cleanup"]["errors"] == []
assert all(closure["cleanup"][key] is True for key in ("intake_closed", "retained_closed", "location_closed", "read_closed", "journal_closed", "controller_closed", "workspace_closed"))
assert sha(compact(closure)) == record["closure_sha256"] == inner["closure_sha256"]
location = closure["observed"]["location"]
assert location["closed"] is True and location["returncode"] == 0
assert location["forced_termination"] is False and location["channel_failed"] is False
assert location["role_pre"] == location["role_post"]
for relative, row in location["role_pre"].items():
    assert row == sdk["portable/location/" + relative]
assert closure["observed"]["intake"]["used"]["requests"] == closure["observed"]["read"]["requests"] == 0
assert closure["observed"]["intake"]["active_connections"] == closure["observed"]["read"]["active"] == 0
session = worker["manager"]["session"]
assert session["number"] == 1 and session["state"] == "BOUND" and session["profile_sha256"] == profile
assert worker["join"] == {"number": 1, "nonce": session["nonce"], "worker": session["worker"], "mathematical_acceptance": False}
assert record["session"]["session_sha256"] == sha(compact({key: value for key, value in session.items() if key not in ("state", "worker")}))
assert record["session"]["worker"] == session["worker"]
command_bound = {"argv": nested["argv"], "cwd": nested["cwd"], "evidence": str(RUN / "operations/serve/work/managed-supervisor"), "stdin_sha256": None, "serve_seconds": None}
assert session["command_sha256"] == sha(compact(command_bound))
assert session["recovery_deadline_ns"] - session["run_deadline_ns"] == 25_000_000_000
assert int(nested["argv"][-1]) - int(nested["argv"][-2]) == 80_000_000_000
assert int(nested["argv"][-1]) <= session["run_deadline_ns"]
expected_status = deepcopy(worker["manager"])
expected_status["session"]["state"] = "QUIESCED"
assert results["status"]["manager"] == expected_status
manager = RUN / "managed"
marker_raw = raw(manager / "manager.json")
config = inner["manager_config"]
assert parse(marker_raw) == {"schema": config["schema"], "root": str(manager), "config_sha256": sha(compact(config))}
assert session["binding"]["root"] == str(manager) and session["binding"]["marker_sha256"] == sha(marker_raw)
assert session["binding"]["config_sha256"] == sha(compact(config))
assert generation == domain("DMKN-V5-TWO-SLOT-GENERATION-V1", {"manager": sha(marker_raw), "sequence": 1, "slot": 0, "config": inner["generation_config"]})
expected_config = deepcopy(inner["generation_config"])
expected_config["placement"]["generation"] = generation
assert record["config"] == expected_config
assert (record["config"]["placement"]["admission_close_ms"], record["config"]["placement"]["retention_not_after_ms"]) == (1577836798000, 1577836799000)
clock = plans["retire"]["parameters"]["clock"]
assert clock == {"lower_utc_ms": 1577836800000, "valid_for_ms": 60000, "rate_error_ppm": 0, "model_id": config["clock_model_id"]}
retired = results["retire"]["retired"]
expected_record = deepcopy(record)
expected_record.update(phase="RETIRED", retirement_lower_ms=1577836800010)
assert retired == expected_record and results["retire"]["retirement_intent"]["retirement_lower_ms"] == 1577836800001
expected_retired = deepcopy(expected_status)
expected_retired.update(retired_floor=1, slots=[retired, None])
assert results["retire"]["manager"] == expected_retired
reclaim = results["reclaim"]
facet = reclaim["enrollment"]["reclaim"]
assert {key: value for key, value in reclaim["enrollment"].items() if key not in ("reclaim", "phase")} == {key: value for key, value in retired.items() if key != "phase"}
target = manager / "slot-0/g00000000000000000001"
assert facet["root"] == inner["exact_reclaimed_root"] == str(target) and not target.exists()
assert facet["profile"] == plans["reclaim"]["parameters"]["reclamation_profile"]
assert facet["calls"] == facet["cursor"] == facet["window_end"] == 0 and facet["failure"] is None
assert facet["entry_count"] == 29 and facet["presence"] == "abeafe1f"
assert facet["binding_sha256"] == domain("DMKN-V5-RECLAIM-BINDING-V1", {key: facet[key] for key in ("schema", "root", "identities", "marker_sha256", "entry_count", "presence", "profile")})
generation_marker = {"schema": "DMKN_V5_MANAGED_GENERATION_V1", "epoch": config["epoch"], "slot": 0, "sequence": 1, "generation": generation, "config_sha256": sha(compact(record["config"]))}
assert facet["marker_sha256"] == sha(compact(generation_marker))
assert reclaim["reclamation"] == {"charged_reclaim_calls": 1, "generation": generation, "mathematical_acceptance": False, "physical_envelope_adopted": False, "sequence": 1, "slot": 0, "status": "FREE"}
expected_free = deepcopy(expected_retired)
expected_free["slots"] = [None, None]
assert inner["final_state"] == reclaim["manager"] == expected_free
assert sorted(path.name for path in manager.iterdir()) == ["generations.sqlite", "manager.json", "owner.lock", "slot-0", "slot-1"]
for slot in (manager / "slot-0", manager / "slot-1"):
    assert slot.is_dir() and list(slot.iterdir()) == []
for name in ("serve", "status", "retire", "reclaim"):
    assert (RUN / "operations" / name).is_dir() and (RUN / "operations" / (name + "-request")).is_dir()
    assert (RUN / "public-commands" / name).is_dir()
db = manager / "generations.sqlite"
db_before = raw(db)
with sqlite3.connect(db.as_uri() + "?mode=ro&immutable=1", uri=True) as connection:
    assert connection.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
    meta = connection.execute("SELECT id,config,sequence,retired_floor,last_horizon,session_sequence,session FROM meta").fetchall()
    assert len(meta) == 1
    ident, dbconfig, sequence, floor, horizon, session_seq, dbsession = meta[0]
    assert (ident, sequence, floor, horizon, session_seq) == (1, 1, 1, 1577836799000, 1)
    assert parse(dbconfig) == config and parse(dbsession) == expected_free["session"]
    assert connection.execute("SELECT id,record FROM slots ORDER BY id").fetchall() == [(0, None), (1, None)]
assert raw(db) == db_before
assert all(not (manager / ("generations.sqlite" + suffix)).exists() for suffix in ("-journal", "-wal", "-shm"))
assert all(inner[key] is False for key in ("full_v5_release", "mathematical_acceptance", "global_complete", "public_deployment_qualified", "independent_hosts", "unclean_recovery_retirement_tested", "physical_envelope_adopted"))
assert all(inner[key] == 0 for key in ("proof_calls", "native_calls", "verifier_calls", "trust_adoptions"))
print(json.dumps({"audit": "PASS_SAVED_PUBLIC_LIFECYCLE", "counts": COUNT, "origin_counts": origin_counts,
    "generation": generation, "profile": profile, "closure": sha(compact(closure)), "database_sha256": sha(db_before),
    "database_bytes": len(db_before), "sqlite_integrity": "ok", "final_sequence": 1, "retired_floor": 1,
    "last_horizon": horizon, "session_sequence": 1, "session_state": "QUIESCED", "slots": [None, None],
    "reclamation_layout_entries": 29, "present_entries": sum(byte.bit_count() for byte in bytes.fromhex(facet["presence"])),
    "node_stderr_bytes": location["stderr_bytes"], "known_cpu_seconds": outer["result"]["final_job"]["cpu_seconds"] + outer["wrapper_cpu_seconds"],
    "outer_wall_seconds": outer["wall_seconds"]}, sort_keys=True))
