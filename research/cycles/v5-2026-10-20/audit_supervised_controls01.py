"""Saved control output and immutable SQLite only; no product imports."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUT = ROOT / "experiments/v5-local-checks/supervised-generations-controls-01"


def raw(path):
    assert path.is_file() and not path.is_symlink() and not path.is_junction()
    return path.read_bytes()


def digest(data): return sha256(data).hexdigest()
def doc(path): return json.loads(raw(path))


selection_path = OUT.with_name(OUT.name + "-selection.json")
selection = doc(selection_path)
outer = doc(OUT / "RESULT.json")
inner = doc(OUT / "supervised-generations-controls-result.json")
assert selection["name"] == OUT.name
assert raw(selection_path) == raw(OUT / "selection.json")
assert outer["selection_sha256"] == digest(raw(selection_path))
assert len(selection["sources"]) == 5 and len(selection["runtime_pins"]) == 142
for relative, expected in selection["sources"].items():
    assert digest(raw(ROOT / relative)) == expected
    assert digest(raw(OUT / "sources" / relative)) == expected
for path, expected in selection["runtime_pins"].items():
    assert digest(raw(Path(path))) == expected
assert len(inner["sources"]) == 124
paths = set()
for row in inner["sources"].values():
    value = raw(Path(row["path"]))
    assert len(value) == row["bytes"] and digest(value) == row["sha256"]
    paths.add(row["path"])
assert set(inner["origins"].values()) <= paths
tree = ast.parse(raw(OUT / "sources/software/v5/supervised_generations/tests.py"))
selected = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "SELECTED" for target in node.targets))
assert list(selected) == inner["selected"] and len(selected) == inner["tests"] == 5
assert set(selected) == set(inner["observations"])
assert inner["status"] == "PASS" and all(inner[key] == 0 for key in ("failures", "errors", "skipped"))
assert inner["forbidden_calls"] == []
assert all(not inner[key] for key in ("positive_worker_join", "positive_os_quiescence",
    "positive_actor_closure", "managed_deletions", "old_data_deleted", "old_suites_imported"))
result = outer["result"]
assert result["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and result["child_exit_code"] == 0
assert result["direct_child_reaped"] and result["job_closed"] and result["cleanup_errors"] == []
assert result["final_job"]["active_processes"] == result["final_job"]["terminated_processes"] == 0
assert not result["termination_requested"]
assert len(raw(OUT / "command/stdout.txt")) == result["observed_logs"]["stdout_bytes"] == 0
assert len(raw(OUT / "command/stderr.txt")) == result["observed_logs"]["stderr_bytes"] == 809
registry_names = ["c01/managed", "c02/managed", "c03/managed", "c04/managed",
                  "c05/before-commit", "c05/after-commit", "c05/close-failure"]
summary = {}
for name in registry_names:
    root = OUT / name
    dbpath = root / "generations.sqlite"
    initial = raw(dbpath)
    db = sqlite3.connect(dbpath.as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
        meta = db.execute("SELECT id,config,sequence,retired_floor,last_horizon,session_sequence,session FROM meta").fetchall()
        slots = db.execute("SELECT id,record FROM slots ORDER BY id").fetchall()
        assert len(meta) == 1 and meta[0][0] == 1 and [row[0] for row in slots] == [0, 1]
        unused, cfg, sequence, floor, horizon, count, session_raw = meta[0]
        cfg = json.loads(cfg)
        session = None if session_raw is None else json.loads(session_raw)
        records = [None if row[1] is None else json.loads(row[1]) for row in slots]
        assert cfg["max_sessions"] == 2 and floor == 0
        assert session is None or session["state"] != "QUIESCED"
        assert all(record is None or record["run_state"] not in ("CLOSED", "QUIESCED_UNCLEAN") for record in records)
        if name == "c01/managed":
            assert session is None and count == sequence == horizon == 0 and records == [None, None]
            assert not (OUT / "c01/old-schema").exists()
        elif name == "c02/managed":
            assert count == session["number"] == 3 and session["state"] == "BOUND"
            assert records == [None, None] and sequence == horizon == 0
        elif name == "c03/managed":
            assert count == sequence == 2 and horizon == 2000000000000
            assert [row["runs"] for row in records] == [1, 1]
            assert [row["run_state"] for row in records] == ["LIVE", "UNKNOWN"]
            assert records[0]["phase"] == "RETIRING" and records[0]["retirement_lower_ms"] == horizon
        elif name == "c04/managed":
            assert count == sequence == 1 and records[1] is None and horizon == 2000000000000
            assert records[0]["runs"] == 1 and records[0]["run_state"] == "LIVE"
        else:
            expected = "RESERVED" if name.endswith("before-commit") else "BOUND"
            assert count == 1 and session["state"] == expected and sequence == horizon == 0
            assert records == [None, None]
        summary[name] = dict(sha256=digest(initial), bytes=len(initial), session_charge=count,
            session_state=None if session is None else session["state"], sequence=sequence,
            runs=[None if row is None else row["runs"] for row in records],
            run_states=[None if row is None else row["run_state"] for row in records])
    finally:
        db.close()
    assert raw(dbpath) == initial
    for slot in ("slot-0", "slot-1"):
        assert list((root / slot).iterdir()) == []
print(json.dumps(dict(audit="PASS_EXACT_FIVE_REFUSAL_CONTROLS_NOT_POSITIVE_RECOVERY",
    hashes={str(path.relative_to(ROOT)): digest(raw(path)) for path in
        (selection_path, OUT / "RESULT.json", OUT / "supervised-generations-controls-result.json")},
    snapshot_sources=5, runtime_pins=142, logical_sources=124, origins=len(inner["origins"]),
    registries=summary, inclusive_known_cpu=result["final_job"]["cpu_seconds"] + outer["wrapper_cpu_seconds"],
    wall=outer["wall_seconds"]), indent=2))
