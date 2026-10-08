"""Cooperative owner-local Lean node; no network or hostile-source sandbox.

Metadata requests load only this dispatcher and its indexed control store.
The independently extracted checker is loaded on selected mathematical paths.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import re
import sys
import time

from storage import ControlStore, Refusal, decode, digest, encode, owner_lock, read, require
from domains import Domains
from capacity import initial_authorization

MIB = 1024 * 1024
SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
PEER_OPS = {"peer_find", "peer_acquire", "expose", "replica_expose"}


def keys(value, required, optional=()):
    require(type(value) is dict and set(required) <= set(value) <= set(required) | set(optional), "INVALID_FIELDS")


def bounded_int(value, low, high, code):
    require(type(value) is int and low <= value <= high, code)
    return value


def context_package_limit(value, common_count):
    """Initial working-context bound, never a change to initialized state."""
    require(type(common_count) is int and 1 <= common_count <= 16, "CONFIG_PACKAGES")
    return bounded_int(value, common_count, 16, "CONFIG_LIMIT:packages")


def request(raw, clients):
    require(len(raw) <= 131072, "REQUEST_LIMIT")
    value = decode(raw)
    keys(value, {"client", "request_id", "op", "args"})
    require(type(value["client"]) is str and value["client"] in clients + ["owner"], "UNKNOWN_CLIENT")
    require(type(value["request_id"]) is str and SAFE_ID.fullmatch(value["request_id"]), "REQUEST_ID")
    require(type(value["op"]) is str and value["op"] in {"init", "info", "find", "preview", "admit", "submit", "publish", "select_context"} | PEER_OPS, "UNKNOWN_OPERATION")
    require(type(value["args"]) is dict, "INVALID_ARGUMENTS")
    require((value["client"] == "owner") == (value["op"] == "init"), "CLIENT_OPERATION_SCOPE")
    return value


def load_config(path):
    raw = read(path, 131072)
    value = decode(raw)
    keys(value, {"schema", "files", "limits", "clients", "common", "offers", "owner_source_execution", "domains", "peers"})
    require(type(value["schema"]) is int and value["schema"] == 3, "CONFIG_PROFILE")
    clients = value["clients"]
    require(type(clients) is list and 1 <= len(clients) <= 16
            and all(type(client) is str and SAFE_ID.fullmatch(client) and client != "owner" for client in clients)
            and len(set(clients)) == len(clients), "CONFIG_CLIENTS")
    domains = Domains.from_config(value)
    require(Path(__file__).resolve() == domains.install / "py" / "node.py", "INSTALLED_NODE_REQUIRED")
    require(value["owner_source_execution"] is True, "OWNER_SOURCE_EXECUTION_NOT_ENABLED")
    keys(value["common"], {"packages"})
    require(type(value["common"]["packages"]) is list and 1 <= len(value["common"]["packages"]) <= 16, "CONFIG_PACKAGES")
    require(type(value["offers"]) is list and 0 <= len(value["offers"]) <= 8, "CONFIG_OFFERS")
    require(type(value["peers"]) is dict and len(value["peers"]) <= 2, "CONFIG_PEERS")
    for alias, endpoint in value["peers"].items():
        require(type(alias) is str and SAFE_ID.fullmatch(alias), "CONFIG_PEER_ALIAS")
        keys(endpoint, {"host", "port"})
        require(endpoint["host"] == "127.0.0.1", "CONFIG_PEER_LOOPBACK")
        bounded_int(endpoint["port"], 1, 65535, "CONFIG_PEER_PORT")
    require(type(value["files"]) is dict and {"checking", "domains", "peer_node", "peer_wire", "peer_service"} <= set(value["files"]), "CONFIG_FILES")
    for name in ("peer_node", "peer_wire", "peer_service"):
        pin = value["files"][name]
        keys(pin, {"path", "bytes", "sha256"})
        require(type(pin["path"]) is str and Path(pin["path"]).is_absolute()
                and Path(pin["path"]).resolve() == domains.install / "py" / (name + ".py"), "PEER_MODULE_PATH")
        bounded_int(pin["bytes"], 1, 2 * MIB, "PEER_MODULE_BYTES")
        require(type(pin["sha256"]) is str and re.fullmatch(r"[a-fA-F0-9]{64}", pin["sha256"]), "PEER_MODULE_PIN")
    domain_pin = value["files"]["domains"]
    keys(domain_pin, {"path", "bytes", "sha256"})
    require(Path(domain_pin["path"]).resolve() == domains.install / "py" / "domains.py", "DOMAINS_PATH")
    domain_bytes = read(domain_pin["path"], MIB)
    require(len(domain_bytes) == domain_pin["bytes"] and digest(domain_bytes) == domain_pin["sha256"].lower(), "DOMAINS_PIN")
    limits = value["limits"]
    required = {"requests", "stages", "stage_bytes", "staging_bytes", "metadata_pages", "native_seconds", "native_memory_mib", "entries", "request_bytes", "source_bytes", "peer_request_bytes", "expose_request_bytes"}
    require(type(limits) is dict and required <= set(limits), "CONFIG_LIMITS")
    context_package_limit(limits.get("packages", 16), len(value["common"]["packages"]))
    initial_authorization(limits)
    for name, low, high in (("requests", 1, 4096), ("stages", 1, 256), ("entries", 1, 8192),
                            ("native_seconds", 1, 300), ("native_memory_mib", 128, 4096),
                            ("stage_bytes", MIB, 512 * MIB), ("staging_bytes", MIB, 64 * 1024 * MIB),
                            ("request_bytes", 65536, 16 * MIB), ("source_bytes", 1, 65536)):
        bounded_int(limits[name], low, high, "CONFIG_LIMIT:" + name)
    bounded_int(limits["peer_request_bytes"], 64 * MIB, 64 * MIB, "CONFIG_LIMIT:peer_request_bytes")
    bounded_int(limits["expose_request_bytes"], 80 * MIB, 80 * MIB, "CONFIG_LIMIT:expose_request_bytes")
    value["config_id"] = digest(raw)
    return value


class Dispatcher:
    def __init__(self, config, store, event):
        self.config, self.store, self.event = config, store, event
        self.key = None
        self.math = None
        self.math_module = None
        self.peer = None
        self.operation = None
        self.work_bytes = config["limits"]["request_bytes"]
        self.quiescent = True

    def peering(self):
        if self.peer is None:
            for name in ("peer_wire", "peer_service", "peer_node"):
                pin = self.config["files"][name]
                source = read(pin["path"], 2 * MIB)
                require(len(source) == pin["bytes"] and digest(source) == pin["sha256"].lower(), "PEER_MODULE_PIN")
                require(Path(pin["path"]).resolve() == Path(__file__).resolve().parent / (name + ".py"), "PEER_MODULE_PATH")
            path = Path(self.config["files"]["peer_node"]["path"])
            spec = importlib.util.spec_from_file_location("installed_peer_operations", path)
            require(spec is not None and spec.loader is not None, "PEER_MODULE_LOADER")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            self.peer = module.PeerOperations(self)
            self.event["peer_modules_loaded"] = True
        return self.peer

    def checking(self):
        if self.math is None:
            pin = self.config["files"]["checking"]
            keys(pin, {"path", "bytes", "sha256"})
            source = read(pin["path"], 2 * MIB)
            require(len(source) == pin["bytes"] and digest(source) == pin["sha256"].lower(), "CHECKER_PIN")
            path = Path(pin["path"]).resolve()
            require(path == Path(__file__).resolve().parent / "checking.py", "CHECKER_PATH")
            spec = importlib.util.spec_from_file_location("operation_local_checker", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            self.math_module = module
            self.event["checker_loaded"] = True
            directory = self.store.root / "work" / self.key
            directory.mkdir(parents=True, exist_ok=False)
            self.math = module.Checker(self.config, directory, self.allocate)
        return self.math

    def allocate(self, purpose):
        require(self.operation not in PEER_OPS, "NATIVE_EXECUTION_FORBIDDEN")
        grant = self.store.stage(self.key, purpose)
        self.quiescent = False
        return grant

    def selected_work_bound(self):
        """Endpoint observation of this request only, excluding charged stages."""
        directory = self.store.root / "work" / self.key
        if not directory.exists():
            return
        total, files = 0, 0
        for child in directory.iterdir():
            if re.fullmatch(r"stage-[0-9]{4}", child.name):
                continue
            items = child.rglob("*") if child.is_dir() else [child]
            for item in items:
                if item.is_file():
                    files += 1
                    total += item.stat().st_size
                    ceiling = 16448 if self.operation in PEER_OPS else 16384
                    require(files <= ceiling and total <= self.work_bytes, "REQUEST_WORK_LIMIT")
        self.event["selected_request_files"] = files
        self.event["selected_request_bytes"] = total

    def check(self, method, *args):
        checker = self.checking()
        try:
            result = getattr(checker, method)(*args)
            self.quiescent = True
            self.selected_work_bound()
            return result
        except self.math_module.CheckingFailure:
            self.quiescent = True
            self.selected_work_bound()
            raise
        finally:
            self.event["checker_metrics"] = dict(getattr(checker, "metrics", {}))

    def candidate(self, client, snapshot, sequence, offer):
        data = {"snapshot": snapshot, "sequence": sequence, "descriptor_id": offer["descriptor_id"]}
        return self.store.put_record("candidate", client, data)

    def selected_candidate(self, client, handle):
        data = self.store.record(handle, "candidate", client)
        cut = self.store.cut(data["snapshot"])
        require(type(data["sequence"]) is int and 1 <= data["sequence"] <= cut["cut"], "CANDIDATE_MEMBERSHIP")
        offer = self.store.entry(cut["provider"], data["sequence"])
        require(offer["descriptor_id"] == data["descriptor_id"], "CANDIDATE_BINDING")
        return data, offer

    def selected_context(self, client, handle):
        context = self.store.record(handle, "context", client)
        require(self.store.head(client) == handle, "STALE_CONTEXT")
        return context

    def prepare(self, req):
        """Prepare selected mathematics before the short visibility transaction."""
        op, args, client = req["op"], req["args"], req["client"]
        if op == "init":
            keys(args, set())
            require(not self.store.meta()["initialized"], "ALREADY_INITIALIZED")
            context = self.check("bootstrap", self.config["common"]["packages"])
            offers = [self.check("offer", package) for package in self.config["offers"]]
            return {"context": context, "offers": offers}
        require(self.store.meta()["initialized"], "NOT_INITIALIZED")
        if op in PEER_OPS:
            return self.peering().prepare(req)
        if op == "select_context":
            keys(args, {"context", "selected"})
            self.selected_context(client, args["context"])
            self.store.record(args["selected"], "context", client)
            return None
        if op == "admit":
            keys(args, {"context", "selected"})
            require(type(args["selected"]) is list and 1 <= len(args["selected"]) <= 4 and
                    all(type(x) is str for x in args["selected"]) and len(set(args["selected"])) == len(args["selected"]), "SELECTED_LIMIT")
            context = self.selected_context(client, args["context"])
            offers = [self.selected_candidate(client, handle)[1] for handle in args["selected"]]
            return self.check("admit", context, offers)
        if op == "submit":
            keys(args, {"context", "source", "root"})
            context = self.selected_context(client, args["context"])
            require(type(args["source"]) is str and type(args["root"]) is str and 0 < len(args["root"]) <= 256, "SOURCE_INPUT")
            raw = args["source"].encode("utf-8")
            require(0 < len(raw) <= self.config["limits"]["source_bytes"], "SOURCE_LIMIT")
            return self.check("submit", context, raw, args["root"])
        if op == "publish":
            keys(args, {"artifact", "snapshot"})
            snapshot = self.store.cut(args["snapshot"])
            require(snapshot["provider"] == "P1" and self.store.current("P1")["snapshot"] == args["snapshot"], "STALE_SNAPSHOT")
            artifact = self.store.record(args["artifact"], "artifact", client)
            checked = self.check("publication", artifact)
            return self.peering().publication_offer(checked)
        return None

    def commit_operation(self, req, prepared):
        op, args, client = req["op"], req["args"], req["client"]
        s = self.store
        if op in PEER_OPS:
            return self.peering().commit(req, prepared)
        if op == "init":
            require(not s.meta()["initialized"], "ALREADY_INITIALIZED")
            contexts = {}
            for target in self.config["clients"]:
                contexts[target] = s.put_record("context", target, prepared["context"])
                s.set_head(target, contexts[target])
            snapshot = s.snapshot("P1", 0)
            for offer in prepared["offers"]:
                snapshot, _, _ = s.append("P1", offer)
            s.exec("initialized", "UPDATE meta SET initialized=1 WHERE id=1")
            return {"status": "OK", "accepted": True, "contexts": contexts, "snapshots": {"P1": snapshot},
                    "description": prepared["context"]["description"]}
        if op == "info":
            keys(args, set())
            handle = s.head(client)
            context = s.record(handle, "context", client)
            return {"status": "OK", "context": handle, "snapshots": {"P1": s.current("P1")["snapshot"]},
                    "description": context["description"], "description_historical": True}
        if op == "select_context":
            # Recheck record ownership/binding and the expected head inside the
            # visibility transaction. This selects history; no live proof check.
            self.selected_context(client, args["context"])
            s.record(args["selected"], "context", client)
            s.set_head(client, args["selected"])
            return {"status": "OK", "client": client, "previous_context": args["context"],
                    "context": args["selected"], "changed": args["context"] != args["selected"],
                    "mathematicalAcceptance": False, "context_record_authenticated": True,
                    "live_context_status": "UNCHECKED", "native_stages": 0}
        if op == "find":
            keys(args, {"provider"}, {"snapshot", "cursor", "limit", "max_bytes"})
            require(args["provider"] == "P1", "UNKNOWN_PROVIDER")
            limit = bounded_int(args.get("limit", 2), 1, 4, "PAGE_LIMIT")
            max_bytes = bounded_int(args.get("max_bytes", 16384), 1024, 16384, "PAGE_BYTE_LIMIT")
            snapshot = args.get("snapshot", s.current("P1")["snapshot"])
            cut = s.cut(snapshot)
            require(cut["provider"] == args["provider"], "SNAPSHOT_PROVIDER")
            first = 1
            if args.get("cursor") is not None:
                cursor = s.record(args["cursor"], "cursor", client)
                require(cursor["snapshot"] == snapshot and cursor["provider"] == args["provider"] and
                        cursor["limit"] == limit and cursor["max_bytes"] == max_bytes, "CURSOR_MISMATCH")
                first = cursor["next"]
            records = s.page(args["provider"], first, cut["cut"], limit)
            result = {"status": "OK", "untrusted": True, "rows": [], "snapshot": snapshot, "cursor": None, "complete": False}
            for sequence, offer in records:
                handle = self.candidate(client, snapshot, sequence, offer)
                row = {"candidate": handle, "candidate_only": True, "descriptor_id": offer["descriptor_id"], "formal_metadata": offer["formal_metadata"]}
                proposed = dict(result, rows=result["rows"] + [row])
                # Reserve enough space for the final opaque cursor and framing.
                if len(encode(proposed)) + 256 > max_bytes:
                    require(result["rows"], "ROW_EXCEEDS_REPLY_BUDGET")
                    break
                result["rows"].append(row)
                first = sequence + 1
                self.event["consumed_sequences"].append(sequence)
            result["complete"] = first > cut["cut"]
            if not result["complete"]:
                result["cursor"] = s.put_record("cursor", client, {"provider": args["provider"], "snapshot": snapshot,
                    "next": first, "limit": limit, "max_bytes": max_bytes})
            require(len(encode(result)) <= max_bytes, "PAGE_BYTE_LIMIT")
            return result
        if op == "preview":
            keys(args, {"candidate"})
            data, offer = self.selected_candidate(client, args["candidate"])
            return {"status": "OK", "untrusted": True, "candidate_only": True, "candidate": args["candidate"],
                    "snapshot": data["snapshot"], "descriptor_id": offer["descriptor_id"], "formal_metadata": offer["formal_metadata"]}
        if op == "admit":
            require(s.head(client) == args["context"], "STALE_CONTEXT")
            require(prepared["kind"] == "context", "PREPARED_KIND")
            context = s.put_record("context", client, prepared)
            s.set_head(client, context)
            return {"status": "OK", "accepted": True, "client": client, "context": context, "description": prepared["description"]}
        if op == "submit":
            require(s.head(client) == args["context"], "STALE_CONTEXT")
            require(prepared["kind"] == "artifact", "PREPARED_KIND")
            require(prepared["source_sha256"] == digest(args["source"].encode("utf-8")) and prepared["source_root"] == args["root"], "SOURCE_BINDING")
            artifact = s.put_record("artifact", client, dict(prepared, context=args["context"]))
            return {"status": "OK", "accepted": True, "client": client, "artifact": artifact, "context": args["context"],
                    "description": prepared["description"], "source_sha256": prepared["source_sha256"], "source_root": prepared["source_root"]}
        if op == "publish":
            require(s.current("P1")["snapshot"] == args["snapshot"], "STALE_SNAPSHOT")
            snapshot, sequence, existing = s.append("P1", prepared)
            publication = s.mark_published("P1", sequence, prepared["descriptor_id"])
            candidate = self.candidate(client, snapshot, sequence, prepared)
            return {"status": "OK", "untrusted": True, "candidate_only": True, "snapshot": snapshot, "candidate": candidate,
                    "descriptor_id": prepared["descriptor_id"], "existing": existing, "publication": publication}
        raise Refusal("UNKNOWN_OPERATION")

    def execute(self, req, raw):
        self.operation = req["op"]
        grant_name = {"peer_acquire": "peer_request_bytes", "expose": "expose_request_bytes",
                      "replica_expose": "expose_request_bytes"}.get(self.operation, "request_bytes")
        self.work_bytes = self.config["limits"][grant_name]
        prior = self.store.prior(req["client"], req["request_id"], raw)
        if prior is not None:
            self.event["historical"] = True
            return prior
        try:
            self.key = self.store.reserve(req["client"], req["request_id"], raw, grant=self.work_bytes)
        except Refusal:
            raise
        except Exception as error:
            return encode({"status": "BLOCKED", "code": "RESERVATION_PERSISTENCE_UNCERTAIN", "detail": type(error).__name__})
        try:
            prepared = self.prepare(req)
            self.selected_work_bound()
            with self.store.transaction():
                reply = encode(self.commit_operation(req, prepared))
                require(len(reply) <= MIB, "RESPONSE_LIMIT")
                self.store.terminal(self.key, reply)
            return reply
        except BaseException as error:
            uncertain = self.math_module is not None and isinstance(error, self.math_module.StageUncertain)
            checking_failure = self.math_module is not None and isinstance(error, self.math_module.CheckingFailure)
            if self.store._uncertain:
                return encode({"status": "BLOCKED", "code": "TRANSACTION_OUTCOME_UNKNOWN"})
            if uncertain or not self.quiescent:
                return encode({"status": "BLOCKED", "code": "PENDING_EXECUTION", "detail": str(error)[:512]})
            try:
                self.selected_work_bound()
            except Refusal as bound_error:
                error, checking_failure = bound_error, False
            except Exception as bound_error:
                error, checking_failure = Refusal("REQUEST_WORK_AUDIT_FAILED", type(bound_error).__name__), False
            if checking_failure:
                diagnostics = error.diagnostics[:64]
                # Never truncate source success into acceptance. Only diagnostic
                # presentation can be abbreviated; the complete evidence stays.
                while len(encode(diagnostics)) > 32768:
                    diagnostics.pop()
                result = {"status": "REFUSED", "code": error.code, "diagnostics": diagnostics,
                          "diagnostics_truncated": error.diagnostics_truncated or len(diagnostics) < len(error.diagnostics)}
            elif isinstance(error, Refusal):
                result = {"status": "REFUSED", "code": error.code, "detail": error.detail[:512]}
            else:
                result = {"status": "REFUSED", "code": "INTERNAL_ERROR", "detail": type(error).__name__ + ": " + str(error)[:512]}
            reply = encode(result)
            try:
                self.store.terminal_refusal(self.key, reply)
            except Exception as terminal_error:
                return encode({"status": "BLOCKED", "code": "TERMINAL_PERSISTENCE_UNCERTAIN", "detail": type(terminal_error).__name__})
            return reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--event", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    event = {"checker_loaded": False, "checker_metrics": {}, "sql_vm_steps": 0, "sql_opened": False, "sql_rows": {},
             "stages_allocated": 0, "historical": False, "fetched_sequences": [], "consumed_sequences": []}
    store = None
    try:
        require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
                and sys.flags.no_user_site, "PYTHON_STARTUP_PROFILE")
        config = load_config(args.config)
        domains = Domains.from_config(config)
        domains.require_state(args.state)
        if args.event is not None:
            event_path = args.event.resolve()
            require(event_path != domains.scratch and event_path.is_relative_to(domains.scratch)
                    and event_path.parent.is_dir() and not event_path.exists(), "EVENT_SCRATCH_DOMAIN")
            event["origin_directory"] = str(event_path.parent)
        raw = read(args.request, 131072)
        event["request_sha256"] = digest(raw)
        req = request(raw, config["clients"])
        with owner_lock(args.state):
            try:
                store = ControlStore(args.state.resolve(), config["config_id"], config["limits"], event,
                                     create=req["op"] == "init", scratch=domains.scratch)
                reply = Dispatcher(config, store, event).execute(req, raw)
            finally:
                if store is not None:
                    store.close()
                    store = None
    except Refusal as error:
        blocked = error.code in {"PENDING_EXECUTION", "TRANSACTION_OUTCOME_UNKNOWN"}
        result = {"status": "BLOCKED" if blocked else "REFUSED", "code": error.code, "detail": error.detail[:512]}
        if error.code == "TRANSACTION_OUTCOME_UNKNOWN":
            result["state_outcome"] = "UNKNOWN"
        reply = encode(result)
    except Exception as error:
        reply = encode({"status": "REFUSED", "code": "INTERNAL_ERROR", "detail": type(error).__name__ + ": " + str(error)[:512]})
    event["elapsed_seconds"] = time.monotonic() - started
    event["sql_vm_steps_upper"] = event["sql_vm_steps"]
    event["sql_progress_interval"] = 1
    event["response_sha256"] = digest(reply)
    if args.event is not None and "domains" in locals():
        event_path = args.event.resolve()
        require(event_path != domains.scratch and event_path.is_relative_to(domains.scratch)
                and event_path.parent.is_dir() and not event_path.exists(), "EVENT_SCRATCH_DOMAIN")
        with args.event.open("xb") as stream:
            stream.write(encode(event))
    sys.stdout.buffer.write(reply)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
