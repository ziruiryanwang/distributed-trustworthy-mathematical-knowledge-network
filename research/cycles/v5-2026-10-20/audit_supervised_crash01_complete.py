"""Independent saved-evidence audit only; no product imports or live APIs."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUT = ROOT / "experiments/v5-local-checks/supervised-generations-crash-01"


def read(path):
    assert path.is_file() and not path.is_symlink() and not path.is_junction()
    return path.read_bytes()


def digest(raw):
    return sha256(raw).hexdigest()


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def doc(path):
    return json.loads(read(path))


selection_path = OUT.with_name(OUT.name + "-selection.json")
input_path = OUT.with_name(OUT.name + "-input.json")
selection = doc(selection_path)
outer = doc(OUT / "RESULT.json")
inner = doc(OUT / "crash-result.json")
before = doc(OUT / "worker-before-crash.json")
worker_input = doc(OUT / "worker-input.json")
assert selection["name"] == OUT.name
assert read(selection_path) == read(OUT / "selection.json")
assert outer["selection_sha256"] == digest(read(selection_path))
assert len(selection["sources"]) == 5 and len(selection["runtime_pins"]) == 147
for relative, expected in selection["sources"].items():
    assert digest(read(ROOT / relative)) == expected
    assert digest(read(OUT / "sources" / relative)) == expected
for path, expected in selection["runtime_pins"].items():
    assert digest(read(Path(path))) == expected
assert len(inner["selected_sources"]) == 124
paths = set()
for row in inner["selected_sources"].values():
    raw = read(Path(row["path"]))
    assert len(raw) == row["bytes"] and digest(raw) == row["sha256"]
    paths.add(row["path"])
assert set(before["origins"].values()) <= paths
assert len(before["origins"]) == 17
assert "origins" not in inner
assert inner["status"] == "FAIL" and inner["error_code"] == "CRASH_ACTUAL_TREE_CLOSURE"
assert inner["stage"] == "supervise-real-crash"
assert not {"after_reopen", "restart_refusal", "retired", "before_crash"} & set(inner)
result = outer["result"]
nested = inner["supervisor"]
assert result["status"] == "COMMAND_FAILED" and result["child_exit_code"] == 1
assert nested["status"] == "COMMAND_FAILED" and nested["child_exit_code"] == 23
for report in (result, nested):
    assert report["direct_child_reaped"] and report["job_closed"]
    assert report["cleanup_errors"] == [] and report["final_job"]["active_processes"] == 0
    assert report["final_job"]["terminated_processes"] == 0
assert nested["termination_requested"] and not result["termination_requested"]
assert nested["final_job"]["total_processes"] == 4
assert result["final_job"]["total_processes"] == 6
assert nested["session_recovery"] == dict(status="QUIESCED", unclean_slots=[0],
                                         orderly_close_claim=False, mathematical_acceptance=False)
assert before["worker"] == before["joined"]["worker"] == before["session"]["worker"]
assert before["descendant"] == doc(OUT / "descendant-ready.json")
assert before["descendant"]["parent_pid"] == before["worker"]["pid"]
assert before["deliberate_exit_code"] == 23 and not before["orderly_close_attempted"]
assert doc(OUT / "crashed-worker/command.json") == {
    key: nested[key] for key in ("argv", "cwd", "limits")}
assert nested["argv"][-1] == digest(read(OUT / "worker-input.json"))
assert before["session"]["command_sha256"] == digest(compact({
    "argv": nested["argv"], "cwd": nested["cwd"], "evidence": str(OUT / "crashed-worker"),
    "stdin_sha256": None, "serve_seconds": None}))
assert before["session"]["profile_sha256"] == worker_input["profile_sha256"] == inner["profile_sha256"]
assert before["session"]["recovery_deadline_ns"] - before["session"]["run_deadline_ns"] == 25 * 10**9
assert before["session"]["limits"] == nested["limits"]
assert before["record"]["session"]["session_sha256"] == digest(compact({
    key: value for key, value in before["session"].items() if key not in ("state", "worker")}))
profile = dict(adapter_sha256=selection["sources"]["software/v5/supervised_generations/crash_smoke.py"],
               sources=inner["selected_sources"],
               operator_manifest_sha256="a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed",
               worker="FIXED_CRASH_WITH_ONE_IDLE_DESCENDANT_V1")
assert digest(compact(profile)) == inner["profile_sha256"]
dbpath = OUT / "managed/generations.sqlite"
db_before = read(dbpath)
db = sqlite3.connect(dbpath.as_uri() + "?mode=ro&immutable=1", uri=True)
try:
    assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
    meta = db.execute("SELECT id,config,sequence,retired_floor,last_horizon,session_sequence,session FROM meta").fetchall()
    slots = db.execute("SELECT id,record FROM slots ORDER BY id").fetchall()
    assert len(meta) == 1 and meta[0][0] == 1 and [row[0] for row in slots] == [0, 1]
    unused, cfg, sequence, floor, horizon, count, raw_session = meta[0]
    record = json.loads(slots[0][1])
    expected = deepcopy(before["record"])
    expected.update(run_state="QUIESCED_UNCLEAN", quiescence={
        "schema": "DMKN_V5_EXACT_JOB_QUIESCENCE_V1",
        "session_sha256": expected["session"]["session_sha256"],
        "nonce": before["session"]["nonce"], "worker": before["worker"]})
    assert record == expected and bytes(slots[0][1]) == compact(expected)
    assert slots[1][1] is None and sequence == count == 1 and floor == 0
    assert horizon == before["record"]["config"]["placement"]["retention_not_after_ms"]
    assert json.loads(cfg) == worker_input["config"] == inner["manager_config"]
    expected_session = {**before["session"], "state": "QUIESCED"}
    assert json.loads(raw_session) == expected_session and bytes(raw_session) == compact(expected_session)
    assert record["phase"] == "PROVISIONING" and record["retirement_lower_ms"] is None
    assert record["runs"] == 1 and record["failure"] is None and "closure_sha256" not in record
finally:
    db.close()
assert read(dbpath) == db_before
generation = OUT / "managed/slot-0/g00000000000000000001"
assert generation.is_dir() and not (generation / "workspace").exists()
assert sorted(path.name for path in generation.iterdir()) == ["generation.json"]
assert list((OUT / "managed/slot-1").iterdir()) == []
marker = read(OUT / "managed/manager.json")
assert digest(marker) == before["session"]["binding"]["marker_sha256"]
assert digest(compact(worker_input["config"])) == before["session"]["binding"]["config_sha256"]
seed = dict(manager=digest(marker), sequence=1, slot=0, config=worker_input["generation"])
assert digest(b"DMKN-V5-TWO-SLOT-GENERATION-V1\0" + compact(seed)) == record["generation"]
files = [selection_path, input_path, OUT / "RESULT.json", OUT / "crash-result.json",
         OUT / "worker-before-crash.json", OUT / "worker-input.json", OUT / "descendant-ready.json", dbpath]
print(json.dumps(dict(
    audit="PASS_PRESERVED_FAILED_CRASH_EVIDENCE_WITH_QUIESCENCE_NOT_RETIREMENT",
    hashes={str(path.relative_to(ROOT)): digest(read(path)) for path in files},
    snapshot_sources=5, runtime_pins=147, logical_sources=124, worker_origins=17,
    parent_final_rebind_reached=False, worker=before["worker"], descendant=before["descendant"],
    durable=dict(phase=record["phase"], run_state=record["run_state"], sequence=sequence,
                 runs=record["runs"], session_charge=count, retired_floor=floor, horizon=horizon,
                 session_state=expected_session["state"], database_bytes=len(db_before)),
    raw_outer=result["status"], raw_inner=inner["status"], raw_nested=nested["status"],
    outer_cpu=result["final_job"]["cpu_seconds"], wrapper_cpu=outer["wrapper_cpu_seconds"],
    inclusive_known_cpu=result["final_job"]["cpu_seconds"] + outer["wrapper_cpu_seconds"],
    outer_wall=outer["wall_seconds"], managed_reclamation=False, retired=False), indent=2))
