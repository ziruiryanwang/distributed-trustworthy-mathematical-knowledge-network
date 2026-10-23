"""Bounded local pipe to obtain missing complete units, not acceptance.

Uses an exact pinned, read-only protected parent. No LocalCatalog.open, replay,
source elaboration, remote executable, trust exception or original-store write.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import queue
import sqlite3
import subprocess
import sys
import threading
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
OLD = LOCAL / "ordinary-native-admission-01/sources/software/v5/ordinary_lean"
SYSROOT = ROOT / "software/runtime/lean-4.34.0-windows"
DATABASE = LOCAL / "ordinary-native-recovery-01/native-recovery/catalog/catalog.sqlite"
DB_SHA = "bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9"
PROFILE = "fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219"
PARENT = "4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026"
BASIS = "cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299"
MIB = 1024 * 1024


def need(ok, code):
    if not ok:
        raise ValueError(code)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(name, path, pins):
    need(digest(path) == pins[str(path)], "OLD_HELPER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_parent(E, pins):
    need(pins[str(DATABASE)] == DB_SHA and digest(DATABASE) == DB_SHA, "EXACT_READ_ONLY_PARENT")
    bindings, roots, current = {}, [], PARENT
    with sqlite3.connect(DATABASE.as_uri() + "?mode=ro&immutable=1", uri=True) as db:
        while current:
            need(current not in roots and len(roots) < 4, "PARENT_CHAIN_BOUND")
            size = db.execute("SELECT length(record) FROM roots WHERE id=?", (current,)).fetchone()
            need(size is not None and 0 < size[0] <= 16 * MIB, "PARENT_RECORD_BOUND")
            raw = db.execute("SELECT record FROM roots WHERE id=?", (current,)).fetchone()[0]
            need(len(raw) == size[0], "PARENT_RECORD_SIZE")
            row = E.strict_json(raw, E.Limits(max_bytes=16 * MIB))
            need(row["root"] == current and row["profile_id"] == PROFILE, "PARENT_RECORD_CONTEXT")
            roots.append(current)
            for name, symbol in row["bindings"]:
                key = E.name_key(name)
                need(key not in bindings and len(bindings) < 65536, "PARENT_DUPLICATE_OR_BOUND")
                bindings[key] = E._hex(symbol)
            current = row["parent"]
    need(len(roots) == 4 and roots[-1] == BASIS and len(bindings) == 3622, "ADOPTED_PARENT_CENSUS")
    need(digest(DATABASE) == DB_SHA, "PARENT_CHANGED")
    return bindings


def exchange(argv, env, output, lookup, parse, name_key, *, seconds=100):
    """One nonrenewing deadline; bounded frames/queue/transcript; clean exit.

    Pipe IO uses readers and one writer so malformed or stalled children cannot
    block the controlling deadline. The outer Job owns the complete process tree.
    """
    deadline = time.monotonic() + seconds
    events, writes = queue.Queue(8), queue.Queue(1)
    stop = threading.Event()
    process = subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    threads = []

    def put(event):
        while not stop.is_set():
            try:
                events.put(event, timeout=0.1)
                return
            except queue.Full:
                pass

    def reader():
        try:
            with (output / "protocol.stdout.jsonl").open("xb") as log:
                total = 0
                while True:
                    raw = process.stdout.readline(MIB + 2)
                    if not raw:
                        break
                    total += len(raw)
                    need(total <= 32 * MIB and raw.endswith(b"\n") and 1 < len(raw) <= MIB + 1,
                         "PROTOCOL_STDOUT_BOUND")
                    log.write(raw)
                    put(("frame", raw))
            put(("stdout_eof", None))
        except BaseException as error:
            put(("error", error))

    def errors():
        try:
            with (output / "native.stderr.txt").open("xb") as log:
                total, tail = 0, b""
                while chunk := process.stderr.read(4096):
                    total += len(chunk)
                    need(total <= MIB, "NATIVE_STDERR_BOUND")
                    need(b"PANIC" not in (tail + chunk).upper(), "NEW_NATIVE_DIAGNOSTIC")
                    tail = chunk[-4:]
                    log.write(chunk)
            put(("stderr_eof", None))
        except BaseException as error:
            put(("error", error))

    def writer():
        try:
            while not stop.is_set():
                try:
                    raw = writes.get(timeout=0.1)
                except queue.Empty:
                    continue
                if raw is None:
                    process.stdin.close()
                    return
                view = memoryview(raw)
                while view:
                    count = process.stdin.write(view)
                    need(count is not None and count > 0, "PROTOCOL_PIPE_WRITE")
                    view = view[count:]
                process.stdin.flush()
        except BaseException as error:
            put(("error", error))

    for function in (reader, errors, writer):
        thread = threading.Thread(target=function, daemon=True)
        threads.append(thread); thread.start()
    done, eof, sequence, total, answers = None, set(), 0, 0, {}
    try:
        with (output / "protocol.stdin.jsonl").open("xb") as transcript:
            while len(eof) != 2:
                remaining = deadline - time.monotonic()
                need(remaining > 0, "PROTOCOL_DEADLINE")
                try:
                    kind, value = events.get(timeout=remaining)
                except queue.Empty:
                    raise ValueError("PROTOCOL_DEADLINE") from None
                if kind == "error":
                    raise value
                if kind.endswith("_eof"):
                    need(kind != "stdout_eof" or done is not None, "PREMATURE_STDOUT_EOF")
                    eof.add(kind)
                    continue
                need(done is None, "TRAILING_STDOUT_FRAME")
                total += len(value)
                need(total <= 32 * MIB, "AGGREGATE_PROTOCOL_BOUND")
                frame = parse(value[:-1], MIB)
                need(type(frame) is dict, "PROTOCOL_OBJECT")
                if frame.get("schema") == "DMKN_ORDINARY_MISSING_IMPORT_DONE_V1":
                    need(set(frame) == {"schema", "lookups", "units", "output_bytes"} and
                         type(frame["lookups"]) is int and frame["lookups"] == sequence and
                         type(frame["units"]) is int and 1 <= frame["units"] <= 1024 and
                         type(frame["output_bytes"]) is int and 0 < frame["output_bytes"] <= 64 * MIB,
                         "DONE_BINDING")
                    done = frame
                    writes.put(None, timeout=max(0.001, deadline - time.monotonic()))
                    continue
                need(set(frame) == {"schema", "seq", "name"} and
                     frame["schema"] == "DMKN_ORDINARY_PARENT_LOOKUP_V1" and
                     type(frame["seq"]) is int and frame["seq"] == sequence and sequence < 65536,
                     "LOOKUP_FRAME_BINDING")
                key = name_key(frame["name"])
                need(key not in answers, "DUPLICATE_LOOKUP")
                symbol = lookup(key)
                answers[key] = symbol
                response = {"schema": "DMKN_ORDINARY_PARENT_REPLY_V1", "seq": sequence,
                            "name": frame["name"], "status": "FOUND" if symbol is not None else "ABSENT"}
                if symbol is not None:
                    response["symbol_id"] = symbol
                raw = json.dumps(response, separators=(",", ":"), ensure_ascii=True).encode() + b"\n"
                total += len(raw)
                need(len(raw) <= MIB + 1 and total <= 32 * MIB, "REPLY_AGGREGATE_BOUND")
                transcript.write(raw)
                writes.put(raw, timeout=max(0.001, deadline - time.monotonic()))
                sequence += 1
        remaining = deadline - time.monotonic()
        need(remaining > 0 and process.wait(timeout=remaining) == 0, "NATIVE_EXIT_REQUIRED")
        return done, answers, total
    finally:
        stop.set()
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        for thread in threads:
            thread.join(timeout=2)
        for stream in (process.stdin, process.stdout, process.stderr):
            if not stream.closed:
                stream.close()
        need(all(not thread.is_alive() for thread in threads), "PROTOCOL_THREADS_UNCLOSED")


def main():
    output, executable, candidate = map(Path, sys.argv[1:4])
    source = Path(__file__).resolve()
    need(len(sys.argv) == 4 and Path.cwd() == ROOT and output.is_absolute() and output.is_relative_to(LOCAL)
         and source == output / "sources/software/v5/ordinary_lean/run_missing_import_completion.py",
         "SELECTED_COMPLETION_REQUIRED")
    selected = json.loads((output / "selection.json").read_bytes())
    pins = selected["runtime_pins"]
    for path in (executable, candidate):
        need(path.is_absolute() and path.is_relative_to(LOCAL) and digest(path) == pins[str(path)], "INPUT_PIN")
    E = load("ordinary_evidence", OLD / "ordinary_evidence.py", pins)
    G = load("missing_native_writer", OLD / "run_native_admission.py", pins)
    parent = read_parent(E, pins)
    need(0 < candidate.stat().st_size <= 64 * MIB, "CANDIDATE_SIZE")
    bundle = G.writer_json(candidate.read_bytes(), 64 * MIB)
    need(bundle["schema"] == "DMKN_ORDINARY_CANDIDATE_BUNDLE_V1" and
         bundle["profile_id"] == PROFILE and bundle["context_id"] == PARENT and bundle["basis_id"] == BASIS,
         "CANDIDATE_CONTEXT")
    unresolved = E._array(bundle["unresolved_imports"], maximum=65536)
    seen, targets = set(), []
    for name in unresolved:
        key = E.name_key(name)
        need(key not in seen, "DUPLICATE_CANDIDATE_IMPORT")
        seen.add(key)
        if key not in parent:
            targets.append(name)
    need(0 < len(targets) <= 1024, "GENUINELY_MISSING_TARGETS_REQUIRED")
    module = [[0, {"$bytes": list(part.encode())}] for part in "Std.Data.ExtHashMap.Lemmas".split(".")]
    request = {"schema": "DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1", "profile_id": PROFILE,
        "context_id": PARENT, "basis_id": BASIS, "modules": [module], "targets": targets}
    raw = E.canonical_json(request)
    need(len(raw) <= MIB, "REQUEST_BYTE_BOUND")
    request_path, bundle_path = output / "request.json", output / "supplement.json"
    with request_path.open("xb") as stream:
        stream.write(raw)
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("LEAN", "PYTHON"))}
    env["PATH"] = str(SYSROOT / "bin") + os.pathsep + env.get("PATH", "")
    done, answers, protocol_bytes = exchange([str(executable), str(SYSROOT), str(request_path), str(bundle_path)],
        env, output, parent.get, G.writer_json, E.name_key)
    need(bundle_path.stat().st_size == done["output_bytes"], "DONE_OUTPUT_SIZE")
    raw_bundle = bundle_path.read_bytes()
    supplement = G.writer_json(raw_bundle, 64 * MIB)
    need(type(supplement) is dict and set(supplement) == {"schema", "assurance", "profile_id", "context_id",
         "basis_id", "targets", "boundary_imports", "units", "stats"} and
         supplement["schema"] == "DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1" and
         supplement["assurance"] == "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE" and
         all(supplement[x] == request[x] for x in ("profile_id", "context_id", "basis_id", "targets")) and
         len(E._array(supplement["units"], maximum=1024)) == done["units"] and
         supplement["stats"]["lookup_count"] == done["lookups"], "SUPPLEMENT_BINDING")
    boundary = set()
    for row in E._array(supplement["boundary_imports"], maximum=65536):
        name, symbol = E._array(row, 2)
        key = E.name_key(name)
        need(key not in boundary and answers.get(key) == symbol and parent.get(key) == E._hex(symbol),
             "SUPPLEMENT_BOUNDARY_IDENTITY")
        boundary.add(key)
    need(all(answers.get(E.name_key(name), "not_asked") is None for name in targets), "TARGET_LOOKUP_REQUIRED")
    need(digest(DATABASE) == DB_SHA and digest(candidate) == pins[str(candidate)], "FINAL_INPUT_PIN")
    result = {"status": "PASS_MISSING_COMPLETE_UNITS_EXPORTED_NOT_ACCEPTED", "targets": targets,
        "units": done["units"], "lookups": done["lookups"], "boundary_imports": len(boundary),
        "protocol_bytes": protocol_bytes, "bundle_bytes": len(raw_bundle),
        "bundle_sha256": hashlib.sha256(raw_bundle).hexdigest(), "candidate_sha256": pins[str(candidate)],
        "request_sha256": hashlib.sha256(raw).hexdigest(), "parent_database_sha256": DB_SHA}
    with (output / "COMPLETION-RESULT.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
