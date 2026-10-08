"""Additive read-only inspection of a historically accepted local definition.

No native launch, source execution, state initialization or new acceptance.
Root alone executes after this extension and its separate allocation are frozen.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import sqlite3
import sys
import time

from node import load_config
from domains import Domains
from storage import ControlStore, Refusal, decode, digest, encode, read, require

HERE = Path(__file__).resolve().parent
MIB = 1024 * 1024
MAX_REFERENCES = 256


class ReadOnlyControl(ControlStore):
    """Reuse frozen keyed readers without invoking its writable constructor."""
    def __init__(self, root, config_id, event):
        self.root = Path(root).resolve(strict=True)
        self.config_id, self.event = config_id, event
        self.readonly, self._uncertain, self._tier = True, False, None
        self.db_path = (self.root / "control.sqlite3").resolve(strict=True)
        require(self.root.is_dir() and self.db_path.is_file()
                and self.db_path.is_relative_to(self.root), "STATE_DATABASE_REQUIRED")
        require(sqlite3.sqlite_version == "3.50.4", "SQLITE_VERSION")
        for suffix in ("-journal", "-wal", "-shm"):
            path = Path(str(self.db_path) + suffix)
            require(not path.exists() or path.stat().st_size == 0, "UNEXPECTED_SQLITE_AUXILIARY")
        with self.db_path.open("rb") as stream:
            header = stream.read(100)
        require(len(header) == 100 and header[:16] == b"SQLite format 3\x00"
                and header[18] == 1 and header[19] == 1, "SQLITE_READ_ONLY_PROFILE")
        # mode=ro prevents creation even if the checked file disappears before open.
        self.db = sqlite3.connect(self.db_path.as_uri() + "?mode=ro", uri=True,
                                  timeout=0, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 3 * MIB)
        self.db.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 16384)
        self.db.set_progress_handler(self._progress, 1)
        self.event["sql_opened"] = True
        try:
            # Connection-local read restriction, not persistent profile mutation.
            self.db.execute("PRAGMA query_only=ON")
            require(self.db.execute("PRAGMA query_only").fetchone()[0] == 1, "READ_ONLY_REQUIRED")
            require(self.db.execute("PRAGMA user_version").fetchone()[0] == 3, "SQLITE_SCHEMA_VERSION")
            require(self.db.execute("PRAGMA journal_mode").fetchone()[0] == "delete", "SQLITE_READ_ONLY_PROFILE")
            self.db.execute("BEGIN")
            self.authorization_state()
            meta = self.meta()
            require(meta["config"] == self.config_id, "CONFIG_CHANGED")
            require(meta["initialized"] == 1, "NOT_INITIALIZED")
            require(meta["active"] is None, "PENDING_EXECUTION")
        except BaseException:
            self.db.close()
            raise

    def exec(self, name, statement, values=()):
        require(statement.lstrip().upper().startswith("SELECT "), "READ_ONLY_QUERY_REQUIRED")
        return self.db.execute(statement, values)

    def close(self):
        self.db.rollback()
        self.db.close()


def request(raw, clients):
    require(len(raw) <= 16384, "REQUEST_LIMIT")
    value = decode(raw)
    require(type(value) is dict and set(value) == {"client", "context", "reference", "max_bytes"}, "INVALID_FIELDS")
    require(type(value["client"]) is str and value["client"] in clients, "UNKNOWN_CLIENT")
    require(type(value["context"]) is str and len(value["context"]) <= 96, "HANDLE_KIND")
    require(type(value["max_bytes"]) is int and 1024 <= value["max_bytes"] <= MIB, "RESPONSE_BYTE_LIMIT")
    ref = value["reference"]
    require(type(ref) is list and len(ref) == 2 and type(ref[0]) is int, "INVALID_REFERENCE")
    require(ref[0] == 1, "UNSUPPORTED_REFERENCE_KIND")
    return value


def load_checker(config, event):
    pin = config["files"]["checking"]
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "CHECKER_PIN")
    path = Path(pin["path"]).resolve(strict=True)
    require(path == HERE / "checking.py", "CHECKER_PATH")
    raw = read(path, 2 * MIB)
    require(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"].lower(), "CHECKER_PIN")
    spec = importlib.util.spec_from_file_location("selected_readonly_inspection_checker", path)
    require(spec is not None and spec.loader is not None, "CHECKER_LOADER")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    event["checker_loaded"] = True
    return module


def lean_name(S, ref, seed):
    """Exact receiver naming, not body interpretation or pretty-printing."""
    if ref[0] == 0:
        require(type(ref[1]) is int and 0 <= ref[1] < len(seed[2]), "DIRECT_REFERENCE_BINDING")
        name = seed[2][ref[1]]
        # Quoted string components avoid treating a seed name as a keyword.
        parts = []
        for part in name:
            if part[0] != 0:
                return name, None
            text = part[1].decode("utf-8", errors="strict")
            if any(character in text for character in ("«", "»", "\r", "\n")):
                return name, None
            parts.append("«" + text + "»")
        return name, ".".join(parts)
    name = S.native_name(ref)
    parts = []
    for part in name:
        require(part[0] == 0, "RECEIVING_NAME_COMPONENT")
        text = part[1].decode("utf-8", errors="strict")
        require(not any(character in text for character in ("«", "»", "\r", "\n")), "RECEIVING_NAME_COMPONENT")
        parts.append(text if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text) else "«" + text + "»")
    return name, ".".join(parts)


def direct_references(checker, plan, type_dag, value_dag):
    S, result, seen = checker.S, [], set()
    available = {S.C.dumps(value) for value in
                 (S.C.from_projection(item) for item in checker.installed_references(plan))}
    for dag in (type_dag, value_dag):
        for node in dag[1]:
            if node[0] not in (2, 8):
                continue
            ref = node[1]
            key = S.C.dumps(ref)
            require(key in available, "DIRECT_REFERENCE_NOT_INSTALLED")
            if key in seen:
                continue
            require(len(result) < MAX_REFERENCES, "DIRECT_REFERENCE_LIMIT")
            seen.add(key)
            name, text = lean_name(S, ref, checker.seed)
            if ref[0] == 3:
                kind = {0: "inductive", 1: "constructor", 2: "recursor"}.get(ref[2][0])
                require(kind is not None, "DIRECT_REFERENCE_KIND")
            else:
                kind = {0: "seed", 1: "definition", 2: "judgment_alias", 4: "opaque", 7: "proof_instance"}.get(ref[0])
                require(kind is not None, "DIRECT_REFERENCE_KIND")
            result.append({"reference": S.C.to_projection(ref), "name": S.C.to_projection(name),
                           "leanName": text, "kind": kind})
    return result


def inspect(checker, context, selected, event):
    checker.checkpoint()
    store, roots, plan = checker.context(context)
    checker.checkpoint()
    evidence = context["evidence"]
    require(type(evidence) is list and len(evidence) == 1, "HISTORICAL_DESCRIBE_EVIDENCE_REQUIRED")
    directory = Path(evidence[0]["directory"]).resolve(strict=True)
    stage_plan = decode(read(directory / "plan.json", MIB))
    expected_step = checker.native_step(["--describe", "$RUN/input/plan.json", "--inventory",
        "$RUN/input/inventory.json", "--requests", "$RUN/input/refs.json"])
    require(stage_plan["steps"] == [expected_step], "HISTORICAL_DESCRIBE_COMMAND_BINDING")
    for key, snapshot in (("agent_client", "native/AgentClient.lean"), ("core_olean", "lib/AgentReplayCore.olean"),
                          ("bootstrap_olean", "lib/BootstrapSupport.olean"), ("inventory", "inventory.json")):
        pins = [pin for pin in stage_plan["inputs"] if pin["as"] == snapshot]
        expected = checker.files[key]
        require(len(pins) == 1 and pins[0]["bytes"] == expected["bytes"]
                and pins[0]["sha256"].lower() == expected["sha256"].lower()
                and Path(pins[0]["path"]).resolve() == Path(expected["path"]).resolve(), "HISTORICAL_NATIVE_TOOL_BINDING")
    require(checker.S.same(decode(read(directory / "input/plan.json", 64 * MIB)), plan), "HISTORICAL_DESCRIBE_PLAN_BINDING")
    refs = [row["reference"] for row in context["description"]["rows"]]
    require(checker.S.same(decode(read(directory / "input/refs.json", MIB)), refs), "HISTORICAL_DESCRIBE_REQUEST_BINDING")
    description = checker.verify_native(directory, 0, store, roots, plan, refs)
    require(checker.S.same(description, context["description"]), "HISTORICAL_DESCRIPTION_BINDING")
    checker.checkpoint()
    S = checker.S
    try:
        ref = S.C.from_projection(selected["reference"])
        S.array(ref, 2)
        S.typed(ref[1], 0x11, 2)
    except (ValueError, TypeError, KeyError, IndexError) as error:
        raise Refusal("INVALID_REFERENCE", type(error).__name__) from error
    rows = [row for row in plan["batch"] if S.same(row["id"], selected["reference"][1])]
    require(len(rows) == 1, "REFERENCE_NOT_ADMITTED")
    row = rows[0]
    require(type(row["kind"]) is int and row["kind"] == 0, "DECLARATION_KIND_MISMATCH")
    declaration = S.array(store.get(ref[1], 0x11, 2), 4)
    arity = S.uint(declaration[1], 64)
    require(S.same(declaration[:2], [store.foundation, arity])
            and type(row["u"]) is int and row["u"] == arity, "DECLARATION_FOUNDATION_ARITY")
    dags = []
    for field, identifier in (("type", declaration[2]), ("value", declaration[3])):
        S.typed(identifier, 0x10, 2)
        term = S.array(store.get(identifier, 0x10, 2), 5)
        dag = term[2:]
        require(S.same(term[:2], [store.foundation, arity])
                and S.same(S.C.to_projection(dag), row[field]), "CANONICAL_TERM_BINDING")
        require(len(S.array(dag[0])) <= 4096 and 0 < len(S.array(dag[1])) <= 65536, "RETURNED_DAG_LIMIT")
        dags.append(dag)
    name, text = lean_name(S, ref, checker.seed)
    mapping = direct_references(checker, plan, dags[0], dags[1])
    checker.checkpoint()
    event["historical_evidence"] = {"stage": evidence[0]["stage"],
                                     "receipt_sha256": evidence[0]["receipt"]["sha256"],
                                     "plan_sha256": evidence[0]["plan"]["sha256"]}
    return {"status": "OK", "kind": "historical_context_definition", "client": selected["client"],
            "context": selected["context"], "foundation": plan["foundation"], "replays": plan["replays"],
            "reference": selected["reference"], "name": S.C.to_projection(name), "leanName": text,
            "kindOfDeclaration": "definition", "u": arity,
            "universeNames": S.C.to_projection([S.C.name_path("u" + str(index)) for index in range(arity)]),
            "type": row["type"], "value": row["value"],
            "typeTermID": S.C.to_projection(declaration[2]), "bodyTermID": S.C.to_projection(declaration[3]),
            "directReferences": mapping, "historical_not_fresh_native": True, "native_stages": 0,
            "mathematicalAcceptance": False, "basis": "REAUTHENTICATED_PRIOR_LOCAL_CONTEXT",
            "kernelHints": None, "reducibilityStatus": None,
            "metadataAuthority": "NOT_OBSERVED_BY_THIS_OPERATION", "valueText": None,
            "valueTextError": "PRESENTATION_NOT_PROVIDED", "request_sha256": event["request_sha256"]}


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    event = {"checker_loaded": False, "checker_metrics": {}, "sql_opened": False,
             "sql_vm_steps": 0, "sql_vm_steps_upper": 0, "sql_progress_interval": 1, "sql_rows": {},
             "native_stages": 0, "stages_allocated": 0, "stage_allocator_calls": 0,
             "historical_not_fresh_native": True, "readonly": True,
             "request_sha256": None, "response_sha256": None}
    store, checker, module = None, None, None
    cap = 1024
    domains = None
    try:
        require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
                and sys.flags.no_user_site, "PYTHON_STARTUP_PROFILE")
        config = load_config(args.config)
        domains = Domains.from_config(config)
        domains.require_state(args.state)
        state = args.state.resolve()
        event_path = args.event.resolve()
        require(event_path.parent.is_dir() and event_path.is_relative_to(domains.scratch)
                and not event_path.is_relative_to(state) and not event_path.exists(), "NEW_EXTERNAL_EVENT_REQUIRED")
        scratch = event_path.parent / "scratch"
        require(not scratch.exists() and not scratch.resolve().is_relative_to(state), "NEW_EXTERNAL_SCRATCH_REQUIRED")
        raw = read(args.request, 16384)
        event["request_sha256"] = digest(raw)
        selected = request(raw, config["clients"])
        cap = selected["max_bytes"]
        store = ReadOnlyControl(state, config["config_id"], event)
        context = store.record(selected["context"], "context", selected["client"])
        require(store.head(selected["client"]) == selected["context"], "STALE_CONTEXT")
        module = load_checker(config, event)
        def forbid_stage(_purpose):
            event["stage_allocator_calls"] += 1
            raise Refusal("NATIVE_EXECUTION_FORBIDDEN")
        scratch.mkdir(exist_ok=False)
        checker = module.Checker(config, scratch, forbid_stage)
        result = inspect(checker, context, selected, event)
        require(event["stage_allocator_calls"] == 0 and checker.metrics["stage_allocations"] == 0
                and checker.metrics["pipeline_children"] == 0, "NATIVE_EXECUTION_FORBIDDEN")
        reply = encode(result)
        require(len(reply) <= cap, "RESPONSE_TOO_LARGE")
    except Refusal as error:
        reply = encode({"status": "REFUSED", "code": error.code, "request_sha256": event["request_sha256"]})
        event["failure_detail"] = str(error)[:512]
    except Exception as error:
        checking = module is not None and isinstance(error, module.CheckingFailure)
        code = "SELECTED_CONTEXT_REFUSED" if checking or isinstance(error, OSError) else "INSPECTION_CORRESPONDENCE_REFUSED"
        reply = encode({"status": "REFUSED", "code": code, "request_sha256": event["request_sha256"]})
        event["failure_detail"] = (type(error).__name__ + ": " + str(error))[:512]
    finally:
        if checker is not None:
            event["checker_metrics"] = dict(checker.metrics)
        if store is not None:
            store.close()
    require(len(reply) <= cap, "REFUSAL_RESPONSE_BOUND")
    event["sql_vm_steps_upper"] = event["sql_vm_steps"]
    event["response_sha256"] = digest(reply)
    event["elapsed_seconds"] = time.monotonic() - started
    event_raw = encode(event)
    require(len(event_raw) <= 65536, "EVENT_BYTE_LIMIT")
    # Revalidate the event domain even on an early refusal; never write state.
    state = args.state.resolve()
    event_path = args.event.resolve()
    require(domains is not None and event_path.parent.is_dir() and event_path.is_relative_to(domains.scratch)
            and not event_path.is_relative_to(state) and not event_path.exists(), "NEW_EXTERNAL_EVENT_REQUIRED")
    with event_path.open("xb") as stream:
        stream.write(event_raw)
        stream.flush()
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
