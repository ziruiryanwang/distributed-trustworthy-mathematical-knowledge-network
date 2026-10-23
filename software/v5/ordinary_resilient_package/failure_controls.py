"""One native-free, table-driven known-provider-failure boundary control.

One pinned package load; real SearchClient, SearchSession and reply verifiers.
Only exchange is replaced for the normal path. A constructor spy and explicitly
named fault injections observe identity or force global stop conditions. Inert
in-memory metadata is not a theorem, native acceptance or real-network evidence.
Root must separately select this source and a finite outer process envelope.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import ssl
import stat
import subprocess
import sys
from unittest.mock import patch

MIB = 1024**2


def need(value, code):
    if not value:
        raise AssertionError(code)


class Allowance:
    deadline = START_WALL+50

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU < 30,
             "FAILURE_CONTROL_ORIGINAL_ALLOWANCE")

    def operation(self, _):
        raise AssertionError("FAILURE_CONTROL_UNEXPECTED_NATIVE_ALLOCATION")


def forbidden(*_, **__):
    raise AssertionError("FAILURE_CONTROL_FORBIDDEN_STATE_NATIVE_OR_NETWORK")


def read(path, maximum=2*MIB):
    need(path.is_absolute() and ".." not in path.parts, "FAILURE_CONTROL_ABSOLUTE_PATH")
    for item in (*reversed(path.parents), path):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "FAILURE_CONTROL_REDIRECT")
        need(stat.S_ISDIR(info.st_mode) if item != path else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "FAILURE_CONTROL_REGULAR_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "FAILURE_CONTROL_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "FAILURE_CONTROL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                     separators=(",", ":")).encode("ascii")
    need(0 < len(raw) <= MIB, "FAILURE_CONTROL_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


def selected_package(args, allowance):
    root = Path(args.package)
    raw = read(root/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "FAILURE_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    entry = read(root/"peer.py")
    pin = descriptor["files"]["peer.py"]
    need(len(entry) == pin["bytes"] and hashlib.sha256(entry).hexdigest() == pin["sha256"],
         "FAILURE_CONTROL_ENTRY_PIN")
    name = "_dmkn_failure_controls_entry"
    need(name not in sys.modules, "FAILURE_CONTROL_PRELOADED_ENTRY")
    spec = importlib.util.spec_from_file_location(name, root/"peer.py")
    peer = importlib.util.module_from_spec(spec)
    sys.modules[name] = peer
    exec(compile(entry, str(root/"peer.py"), "exec"), peer.__dict__)
    owner = peer.bootstrap_owner(root, args.profile_sha256, allowance.check)
    loader = owner.bootstrap(root, args.profile_sha256, allowance.check)
    loaded = loader.load(root, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        allowance.deadline, check_parent=allowance.check)
    need(loaded.peer_api.A is loaded.A and loaded.peer_api.O is loaded.O,
         "FAILURE_CONTROL_SHARED_CORE")
    return loaded


def classification(api):
    codes = """REMOTE_HTTP_ERROR_CONSERVATIVELY_CHARGED HTTP_HEADER_BYTES HTTP_HEADER_LINES
        HTTP_HEADER_SHAPE HTTP_HEADER_NAME HTTP_HEADER_DUPLICATE_OR_CONTROL HTTP_UNSUPPORTED_HEADER
        HTTP_CONTENT_LENGTH HTTP_MESSAGE_PROFILE HTTP_STATUS HTTP_RESPONSE_BOUND HTTP_TRAILING_RESPONSE
        JSON_BYTE_LIMIT JSON_DEPTH_LIMIT JSON_DUPLICATE_KEY JSON_NONINTEGER NONCANONICAL_JSON
        SESSION_OFFER_QUERY_BINDING SESSION_OFFER_ASSURANCE SESSION_OFFER_STATUS SESSION_OFFER_NO_SUMMARY
        SESSION_OFFER_SUMMARY SESSION_OFFER_EXPIRED CANDIDATE_PAGE_SCHEMA CANDIDATE_ASSURANCE
        CANDIDATE_CURSOR_BINDING""".split()
    accepted = [kind("CONTROL") for kind in (ConnectionRefusedError, ConnectionResetError,
        ConnectionAbortedError, BrokenPipeError, TimeoutError, ssl.SSLCertVerificationError)]
    accepted += [asyncio.IncompleteReadError(b"", 1), asyncio.LimitOverrunError("CONTROL", 1),
        json.JSONDecodeError("CONTROL", "{", 1), UnicodeDecodeError("utf-8", b"\xff", 0, 1, "CONTROL")]
    accepted += [ValueError(code) for code in codes]
    class RefusedSubclass(ConnectionRefusedError):
        pass
    class ValueSubclass(ValueError):
        pass
    rejected = [OSError("CONTROL"), ssl.SSLError("CONTROL"), RuntimeError("CONTROL"),
        RefusedSubclass("CONTROL"), ValueSubclass(codes[0]), asyncio.CancelledError(),
        SystemExit(), KeyboardInterrupt()]
    rejected += [ValueError(code) for code in ("EXACT_FIELDS", "HASH_ENCODING", "SESSION_BUDGET:requests",
        "SESSION_QUERY_CHANGED", "SESSION_TICKET_NOT_PENDING", "SESSION_TRANSPORT_BYTE_VIOLATION",
        "PEER_FILE_PIN", "JSON_BYTE_LIMIT:extra", "HTTP_UNKNOWN", "CONTROL_UNEXPECTED")]
    need(all(api._provider_error(error) for error in accepted), "FAILURE_CONTROL_ALLOWLIST_MISSING")
    need(not any(api._provider_error(error) for error in rejected), "FAILURE_CONTROL_ALLOWLIST_TOO_BROAD")
    return {"accepted": len(accepted), "rejected": len(rejected)}


class Fixture:
    """Small authenticated V1 metadata only; no ordinary evidence/owner state."""
    def __init__(self, api, label, counts, namespace, feature):
        F, A, W = api.F, api.CQ.A, sys.modules["discovery.summary_wire"]
        class Memory:
            def __init__(self): self.nodes = {}
            def put_node(self, node):
                digest = A.node_hash(node); self.nodes[digest] = deepcopy(node); return digest
            def get_node(self, digest): return deepcopy(self.nodes[digest])
        self.io, self.records, self.trees = Memory(), {}, {}
        self.namespace, self.feature = namespace, feature
        digest = lambda value: hashlib.sha256(value.encode("ascii")).hexdigest()
        descriptors = [A.empty_descriptor(namespace, feature, p) for p in range(256)]
        for partition, count in counts.items():
            ctx = A.context(namespace, feature, partition)
            tree, records = A.vector_empty(ctx), []
            for ordinal in range(count):
                key = label+":"+str(partition)+":"+str(ordinal)
                record = {"schema": F.RECORD_SCHEMA, "namespace": namespace, "kind": "inert-failure-control",
                    "object_id": format(partition, "02x")+digest("object:"+key)[2:],
                    "object_sha256": digest("raw:"+key), "object_bytes": 1, "features": [feature]}
                tree = A.append_vector(self.io, ctx, ordinal, tree, F.record_id(record))
                records.append(record)
            self.records[partition], self.trees[partition] = records, tree
            descriptors[partition] = {"partition": partition, "count": count, "tree_root": tree}
        feature_root = A.feature_root(namespace, feature, descriptors)
        map_root = A.map_set(self.io, namespace, A.map_empty(namespace)[0], feature, feature_root)
        snapshot = {"schema": "DMKN_FORMAL_INDEX_SNAPSHOT_V1", "namespace": namespace,
            "feature_schema": F.SCHEMA, "partition_bits": 8, "feature_map_root": map_root,
            "local_cut": sum(counts.values()), "previous_snapshot": None,
            "coverage_claim": "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS"}
        self.sid = A.snapshot_id(snapshot)
        siblings = A.map_get(self.io, namespace, map_root, feature)[1]
        summary = {"schema": "DMKN_FORMAL_QUERY_SUMMARY_V1", "namespace": namespace,
            "snapshot_id": self.sid, "snapshot": snapshot, "features": [feature],
            "rows": [{"feature_id": feature, "partitions": descriptors, "siblings": siblings}],
            "coverage": "COMMITTED_METADATA_NOT_SOURCE_CORPUS", "mathematical_acceptance": False}
        wire = W.encode_summary(summary, self.sid, namespace, [feature],
                                max_wire_bytes=16384, max_expanded_bytes=65536)
        self.offer = F.compact({"schema": "DMKN_DISCOVERY_OFFER_V1", "namespace": namespace,
            "features": [feature], "status": "OFFERED", "reason": "SNAPSHOT_SELECTED",
            "summary": json.loads(wire), "global_complete": False, "mathematical_acceptance": False})
        need(len(self.offer) <= 16384, "FAILURE_CONTROL_OFFER_BOUND")

    def page(self, api, request):
        partition, start = request["partition"], request["start"]
        records = self.records[partition]
        count, next_position = len(records), start+1
        query = api.CQ.Q.query_id(self.namespace, [self.feature])
        siblings = api.CQ.A.vector_get(self.io, api.CQ.A.context(self.namespace, self.feature, partition),
                                      count, self.trees[partition], start)[1]
        return api.F.compact({"schema": "DMKN_FORMAL_CANDIDATE_PAGE_V1", "namespace": self.namespace,
            "snapshot_id": self.sid, "query_id": query, "partition": partition, "anchor": self.feature,
            "start": start, "next": next_position, "anchor_count": count,
            "hits": [{"ordinal": start, "record": records[start], "siblings": siblings}],
            "next_cursor": None if next_position == count else api.CQ.cursor(request, query, next_position),
            "termination": "anchor_boundary" if next_position == count else "scanned_exhausted",
            "charged": {"scanned": 1, "record_probes": 1, "node_reads": 1, "hash_calls": 1,
                        "sql_vm_steps": 100, "record_loads": 1, "proofs": 1},
            "coverage": api.CQ.CLAIM, "global_complete": False, "mathematical_acceptance": False})


async def scenario(loaded, allowance, fixtures, case):
    api = loaded.peer_api
    clients = sys.modules[api.SearchClient.__module__]
    calls, instances, charged_bytes, triggers = [], [], [], set()
    limits = dict(providers=3, snapshots=3, requests=4 if case == "request-cap" else 6,
        pages=4, examined=8, candidates=8, bytes=131072, wall_ms=30000, inflight=1)
    config = {"contacts": {label: {"host": "127.0.0.1", "port": 41001+i, "tls": False,
            "server_name": None, "ca_file": None, "ca_sha256": None} for i, label in enumerate(("p0", "p1", "p2"))},
        "providers": ["p0", "p1", "p2"], "specs": [{"tag": "declaration-kind", "value": "theorem"}],
        "limits": limits, "offer": {"max_bytes": 16384, "max_expanded_bytes": 65536, "max_age_ms": 30000},
        "page": dict(scanned=1, matches=2, bytes=8192, timeout_ms=1000,
            record_probes=1, node_reads=1, hash_calls=1, sql_vm_steps=100)}
    ledger = loaded.O.OrdinaryBudget(deadline=allowance.deadline-5,
        requests=limits["requests"], reply_bytes=limits["bytes"])
    original_deadline = ledger.deadline
    class LocalAllowance:
        deadline = allowance.deadline
        def check(self):
            allowance.check()
            if "allowance" in triggers: raise ValueError("CONTROL_ALLOWANCE_CLOSED")
    local = LocalAllowance()
    actual_init, actual_repin = api.SearchClient.__init__, api._repin
    def observe(client, *args, **kwargs):
        actual_init(client, *args, **kwargs)
        instances.append((client, client.session, client.session.deadline))
    def repin(pins, check):
        if "pin" in triggers: raise ValueError("PEER_FILE_PIN")
        return actual_repin(pins, check)
    async def exchange(endpoint, route, request, maximum, timeout):
        need(len(instances) == 1, "FAILURE_CONTROL_NEW_CLIENT")
        client, session, deadline = instances[0]
        need(client.session is session and session.deadline == deadline,
             "FAILURE_CONTROL_SESSION_OR_DEADLINE_REPLACED")
        need(ledger.deadline == original_deadline and ledger.requests == limits["requests"]
             and ledger.reply_bytes == limits["bytes"] and len(ledger.external) == 1,
             "FAILURE_CONTROL_GRANT_RENEWED_OR_NOT_PREPAID")
        provider = "p"+str(endpoint.port-41001)
        phase = "offer" if route == api.H.OFFER_ROUTE else "candidates"
        need(route in (api.H.OFFER_ROUTE, api.H.CANDIDATE_ROUTE), "FAILURE_CONTROL_UNEXPECTED_ROUTE")
        calls.append({"provider": provider, "phase": phase, "partition": request.get("partition"),
                      "start": request.get("start"), "request_bytes": len(api.F.compact(request))})
        if provider == "p1":
            charged_bytes.append(maximum)
            raise ConnectionRefusedError("CONTROL_CONTACT_REFUSED")
        if provider == "p0" and phase == "candidates" and request["start"] == 1:
            if case in ("continue", "request-cap"):
                raw = b"{"
            elif case == "transport-bound":
                raw = b"x"*(maximum+1)
            else:
                charged_bytes.append(maximum)
                if case == "cancel": raise asyncio.CancelledError("CONTROL_CANCELLED")
                if case == "unexpected": raise ValueError("CONTROL_UNEXPECTED")
                if case == "session-deadline": session.clock = lambda: session.deadline
                elif case == "ledger-deadline": ledger.deadline = time.monotonic()-1
                elif case in ("allowance", "pin"): triggers.add(case)
                elif case == "query": session.features = []
                elif case == "pending": session.pending[-1] = {"control": "foreign-unsettled-ticket"}
                else: raise AssertionError("FAILURE_CONTROL_UNKNOWN_CASE")
                raise TimeoutError("CONTROL_TIMEOUT")
        else:
            fixture = fixtures[provider]
            raw = fixture.offer if phase == "offer" else fixture.page(api, request)
        charged_bytes.append(len(raw))
        return {"status": 200, "raw": raw, "request_bytes": len(api.F.compact(request)),
                "reply_bytes": len(raw), "header_bytes": 0}
    try:
        with patch.object(api.SearchClient, "__init__", observe), patch.object(api, "_repin", repin), \
                patch.object(clients, "exchange", exchange):
            try:
                report = await api.find(loaded, config, local, network_budget=ledger)
            except api.PeerFailure as error:
                report = error.report
        need(len(instances) == 1, "FAILURE_CONTROL_CLIENT_COUNT")
        client, session, deadline = instances[0]
        need(client.session is session and session.deadline == deadline, "FAILURE_CONTROL_FINAL_IDENTITY")
        need(ledger.deadline == original_deadline or case == "ledger-deadline" and ledger.deadline < original_deadline,
             "FAILURE_CONTROL_LEDGER_DEADLINE_RENEWED")
        need(ledger.external == [{"label": "peer-find", "requests": limits["requests"], "reply_bytes": limits["bytes"]}]
             and ledger.requests == limits["requests"] and ledger.reply_bytes == limits["bytes"]
             and ledger.pending is None and not ledger.closed, "FAILURE_CONTROL_ONE_SHARED_PREPAYMENT")
        need(all(not report[key] for key in ("global_complete", "verified_scan_coverage", "mathematical_acceptance")),
             "FAILURE_CONTROL_FALSE_ASSURANCE")
        need(not report["cleanup_errors"], "FAILURE_CONTROL_CLEANUP")
        need(session.used["requests"] == len(calls) and session.used["bytes"] == sum(charged_bytes)
             and session.used["request_bytes"] == sum(row["request_bytes"] for row in calls),
             "FAILURE_CONTROL_EXACT_REQUEST_BYTE_CHARGES")
        pages = sum(row["phase"] == "candidates" for row in calls)
        need(session.used["pages"] == pages and session.used["examined"] == pages
             and not any(session.reserved.values()), "FAILURE_CONTROL_FULL_SCAN_CHARGE")
        need(len(session.pending) == (1 if case == "pending" else 0), "FAILURE_CONTROL_PENDING_SETTLEMENT")
        want_later = case == "continue"
        expected = [("p0", fixtures["p0"].records[7][0])]
        if want_later: expected.append(("p2", fixtures["p2"].records[7][0]))
        need([(row["provider"], row["record"]) for row in report["matches"]] == expected,
             "FAILURE_CONTROL_PRIOR_AND_LATER_EXACT_MATCHES")
        need(report["offers"] == [{"provider": provider, "status": "OFFERED",
             "snapshot_id": fixtures[provider].sid} for provider, _ in expected],
             "FAILURE_CONTROL_PRIOR_AND_LATER_EXACT_OFFERS")
        need(len(session.summaries) == len(expected) and len(session.seen_candidates) == len(expected),
             "FAILURE_CONTROL_VERIFIED_STATE_NOT_RESET_OR_FAILED_PAGE_ADOPTED")
        expected_providers = 3 if want_later else 2 if case == "request-cap" else 1
        need(len(session.providers) == expected_providers and session.snapshot_slots == expected_providers
             and len(session.attempted_snapshots) == len(expected), "FAILURE_CONTROL_ATTEMPT_CHARGES")
        need(all(row["partition"] != 8 for row in calls), "FAILURE_CONTROL_FAILED_PROVIDER_REVISITED")
        need(session.used["candidates"] == len(expected)+2, "FAILURE_CONTROL_FAILED_PAGE_FULL_ROW_CHARGE")
        if case in ("continue", "request-cap"):
            need(report["status"] == "INCOMPLETE_SEARCH" and len(report["provider_errors"]) == 2,
                 "FAILURE_CONTROL_RECOVERY_REPORT")
            need(report["provider_errors"] == [
                 {"provider": "p0", "phase": "candidates", "error": {"type": "JSONDecodeError", "code": "PEER_OPERATION_FAILED"}},
                 {"provider": "p1", "phase": "offer", "error": {"type": "ConnectionRefusedError", "code": "CONTROL_CONTACT_REFUSED"}}],
                 "FAILURE_CONTROL_ORDERED_SANITIZED_ERRORS")
            need(report["termination"] == ("SELECTED_CONTACTS_FINISHED_WITH_PROVIDER_ERRORS_NO_COMPLETENESS_CLAIM"
                if want_later else "SESSION_BUDGET:requests"), "FAILURE_CONTROL_TERMINATION")
            need([row["provider"] for row in calls] == (["p0"]*3+["p1"]+["p2"]*2 if want_later
                 else ["p0"]*3+["p1"]), "FAILURE_CONTROL_CONTACT_ORDER_NO_RETRY")
            need(client.http["completed_requests"] == len(calls)-1 and client.http["failed_requests"] == 1,
                 "FAILURE_CONTROL_HTTP_COUNTER_MEANING")
        else:
            codes = {"cancel": "CONTROL_CANCELLED", "unexpected": "CONTROL_UNEXPECTED",
                "session-deadline": "SESSION_DEADLINE_EXHAUSTED", "ledger-deadline": "ORDINARY_BUDGET_CLOSED_OR_EXPIRED",
                "allowance": "CONTROL_ALLOWANCE_CLOSED", "pin": "PEER_FILE_PIN", "query": "SESSION_QUERY_CHANGED",
                "pending": "PEER_FIND_PENDING_REQUEST", "transport-bound": "SESSION_TRANSPORT_BYTE_VIOLATION"}
            need(report["status"] == "FAILED" and report["error"]["code"] == codes[case]
                 and not report["provider_errors"] and [row["provider"] for row in calls] == ["p0"]*3,
                 "FAILURE_CONTROL_GLOBAL_STOP:"+case)
        return {"case": case, "ok": True, "status": report["status"], "termination": report["termination"],
            "error": report.get("error"), "calls": calls, "provider_errors": report["provider_errors"],
            "match_ids": [row["record"]["object_id"] for row in report["matches"]],
            "used": dict(session.used), "reserved": dict(session.reserved), "pending": len(session.pending),
            "http": dict(client.http), "network": report["network"]}
    finally:
        ledger.close()


async def matrix(loaded, allowance):
    api = loaded.peer_api
    namespace = api.OrdinaryExportAdapter(loaded.installation.semantic_id).namespace
    feature, = api.compile_query(namespace, [{"tag": "declaration-kind", "value": "theorem"}])
    fixtures = {"p0": Fixture(api, "p0", {7: 2, 8: 1}, namespace, feature),
                "p2": Fixture(api, "p2", {7: 1}, namespace, feature)}
    rows = []
    for case in ("continue", "request-cap", "cancel", "unexpected", "session-deadline",
                 "ledger-deadline", "allowance", "pin", "query", "pending", "transport-bound"):
        allowance.check()
        try:
            rows.append(await scenario(loaded, allowance, fixtures, case))
        except BaseException as error:
            rows.append({"case": case, "ok": False, "error_type": type(error).__name__, "error": str(error)[:1000]})
    return rows


def main(args):
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "FAILURE_CONTROL_PYTHON")
    allowance = Allowance()
    with ExitStack() as guards:
        guards.enter_context(patch.object(sqlite3, "connect", forbidden))
        guards.enter_context(patch.object(subprocess, "Popen", forbidden))
        loaded = selected_package(args, allowance)
        api = loaded.peer_api
        guards.enter_context(patch.object(api.H, "exchange", forbidden))
        guards.enter_context(patch.object(api.H.Provider, "start", forbidden))
        guards.enter_context(patch.object(sys.modules[api.SearchClient.__module__], "exchange", forbidden))
        guards.enter_context(patch.object(asyncio, "open_connection", forbidden))
        guards.enter_context(patch.object(asyncio, "start_server", forbidden))
        guards.enter_context(patch.object(loaded.O, "OrdinaryStore", forbidden))
        guards.enter_context(patch.object(loaded.A.OrdinaryAdmission, "open", forbidden))
        output = loaded.A.C.ordinary(Path(args.output), directory=True)
        for protected in (loaded.root, *loaded.installation.runtime_roots.values()):
            need(not output.is_relative_to(protected) and not protected.is_relative_to(output),
                 "FAILURE_CONTROL_OUTPUT_OVERLAP")
        classes = classification(api)
        rows = asyncio.run(matrix(loaded, allowance))
        allowance.check()
    report = {"ok": len(rows) == 11 and all(row["ok"] for row in rows), "classification": classes,
        "cases": rows, "profile_sha256": args.profile_sha256,
        "implementation_id": loaded.installation.implementation_id,
        "wall_seconds": time.monotonic()-START_WALL, "controller_cpu_seconds": time.process_time()-START_CPU,
        "native_operations": 0, "owner_opens": 0, "peer_connections": 0,
        "claim": "FAKE_EXCHANGE_REAL_METADATA_VERIFIERS_NOT_MATHEMATICAL_OR_NETWORK_QUALIFICATION"}
    save(output/"FAILURE-CONTROLS.json", report)
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+name, required=True)
    raise SystemExit(main(parser.parse_args()))
