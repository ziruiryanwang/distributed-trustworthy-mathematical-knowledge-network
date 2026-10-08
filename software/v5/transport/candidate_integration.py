"""Actual unknown-SID offer -> positive-only candidates over retained index bytes.

Exactly two owner-approved loopback HTTP calls; no rebuild, custody, native
checking, proof, failure campaign or mathematical admission. Sender wire-body
and provider dispatch requests are recorded separately because the latter may
have a shorter local timeout. Neither observer changes production behavior.
"""
from pathlib import Path
import argparse
import asyncio
from copy import deepcopy
import hashlib
import json
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query
from discovery.search_session import SearchSession
from transport.http_provider import Provider, OFFER_ROUTE, CANDIDATE_ROUTE
from transport.clients import SearchClient
from transport.summary_integration import read_pin, save

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OFFER_BYTES = 8192
CANDIDATE_LIMITS = dict(scanned=32, matches=8, bytes=131072, timeout_ms=1000,
    record_probes=256, node_reads=32768, hash_calls=200000, sql_vm_steps=1000000)
SESSION_LIMITS = dict(providers=1, snapshots=1, requests=2, pages=1,
    examined=32, candidates=8, bytes=139264, wall_ms=15000, inflight=1)
# Exact expected export from retained offer-public-integration-01 evidence.
# These values are assertions on a returned positive, NEVER inputs to planning.
EXPECTED_OBJECT = "5cddd219401f57b4fb91fca36baab0e071fbb6c8619f2fd974f1a03cc082807b"
EXPECTED_LOCATOR = {
    "schema": "DMKN_MODULE_EXPORT_LOCATOR_V1",
    "module_id": "4b09f9821e27c9edcc7528e3db5b91e0d21c3637a012951361ef6260802ae293",
    "descriptor_id": "ded120293391ffad606936a24bc8d76548a32d82de03b9ecce441edbe056b0b9",
    "group_index": 0, "relative_name": [["s", "CommonsV5"], ["s", "fusion"]]}


class RecordingClient(SearchClient):
    def __init__(self, session, endpoints, evidence):
        super().__init__(session, endpoints)
        self.evidence, self.sent = evidence, []

    async def _send(self, provider, ticket, route):
        raw = F.compact(ticket["request"])
        ordinal = len(self.sent)
        F.need(ordinal < 2 and route == (OFFER_ROUTE if ordinal == 0 else CANDIDATE_ROUTE),
               "EXACT_TWO_SENT_CALLS")
        with (self.evidence / f"request-{ordinal}.json").open("xb") as stream:
            stream.write(raw)
        self.sent.append({"route": route, "bytes": len(raw),
                          "sha256": hashlib.sha256(raw).hexdigest(),
                          "request": deepcopy(ticket["request"])})
        return await super()._send(provider, ticket, route)


class RecordingProvider(Provider):
    def __init__(self, index, evidence):
        super().__init__(index=index, max_requests=2, max_reply_bytes=SESSION_LIMITS["bytes"])
        self.evidence, self.calls, self.dispatched = evidence, [], []

    def dispatch(self, route, request, *, check_budget=None):
        ordinal = len(self.calls)
        F.need(ordinal < 2 and route == (OFFER_ROUTE if ordinal == 0 else CANDIDATE_ROUTE),
               "EXACT_TWO_DISPATCH_CALLS")
        if ordinal == 0:
            F.need("snapshot_id" not in request, "OFFER_HAS_NO_PRESELECTED_SNAPSHOT")
        self.dispatched.append(deepcopy(request))
        save(self.evidence / f"dispatch-request-{ordinal}.json", request)
        started_cpu, started_wall = time.process_time(), time.monotonic()
        result = super().dispatch(route, request, check_budget=check_budget)
        raw = result if type(result) is bytes else F.compact(result)
        with (self.evidence / f"response-{ordinal}.json").open("xb") as stream:
            stream.write(raw)
        self.calls.append({"route": route, "reply_bytes": len(raw),
            "reply_sha256": hashlib.sha256(raw).hexdigest(),
            "dispatch_cpu_seconds": time.process_time() - started_cpu,
            "dispatch_wall_seconds": time.monotonic() - started_wall})
        return result


async def run(args, out, report):
    original = read_pin(args.database, args.database_sha, 64 * 1024**2)
    bundle = C.parse_json(read_pin(args.bundle, args.bundle_sha, 2**20))
    F.need(C.module_id(bundle["spec"]) == bundle["module"], "BUNDLE_MODULE_IDENTITY")
    adapter = ModuleExportAdapter(C, bundle["spec"]["foundation"], bundle["spec"]["policy"])
    features = compile_query(adapter.namespace, [
        {"tag": "declaration-kind", "value": "theorem"},
        {"tag": "result-head", "head": {"tag": "const", "symbol": {"kind": "foundation-name",
         "name_hash": C.hash_value("foundation-symbol", [["s", "Eq"]])}}}])
    target = out / "reopened-index"
    target.mkdir()
    database = target / "discovery.sqlite"
    with database.open("xb") as stream:
        stream.write(original)
    del original
    db = sqlite3.connect(database.as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        cfg = F.strict(bytes(db.execute("SELECT cfg FROM meta WHERE id=1").fetchone()[0]), 16384)
    finally:
        db.close()
    index = Store(target, adapter, cfg["limits"])
    provider, client = RecordingProvider(index, out), None
    try:
        endpoint = await provider.start()
        session = SearchSession(adapter.namespace, features, SESSION_LIMITS)
        client = RecordingClient(session, {"contact": endpoint}, out)
        initial = client.report()
        F.need(not session.summaries and not session.attempted_snapshots and not session.offer_hints
               and not session.seen_candidates and not session.last_advisory and not session.last_verified
               and initial["session"]["snapshot_budget"]
               == {"charged_attempt_slots": 0, "known_snapshot_ids": 0, "limit": 1},
               "CLIENT_STARTS_WITH_NO_SNAPSHOT_ID_PLAN_OR_CANDIDATE")
        save(out / "consumer-initial.json", initial)
        offered = await client.offer("contact", OFFER_BYTES,
            max_expanded_bytes=1048576, max_age_ms=60000)
        F.need(offered["status"] == "OFFERED"
               and offered["assurance"] == "AUTHENTICATED_PROVIDER_SELECTED_METADATA_ONLY"
               and offered["global_complete"] is False and offered["mathematical_acceptance"] is False,
               "AUTHENTICATED_OFFER_ONLY")
        save(out / "consumer-offer.json", offered)
        after_offer = client.report()
        save(out / "consumer-after-offer.json", after_offer)
        # Sole source of SID/partition/anchor: the actual authenticated offer.
        selected = next((row for row in offered["partitions"] if row["anchor_count"] > 0), None)
        F.need(selected is not None and selected["committed_empty"] is False,
               "OFFER_HAS_NONEMPTY_PARTITION")
        sid = offered["snapshot_id"]
        page = await client.candidates("contact", sid, selected["partition"], 0, CANDIDATE_LIMITS)
        F.need(page["status"] == "VERIFIED_CANDIDATES" and page["snapshot_id"] == sid
               and page["assurance"] == "VERIFIED_POSITIVE_COMMITTED_RECORDS_ONLY"
               and page["verified_scan_coverage"] is False and page["global_complete"] is False
               and page["mathematical_acceptance"] is False, "ACTUAL_VERIFIED_POSITIVE_ONLY")
        F.need(len(page["matches"]) == 1 and page["matches"][0]["object_id"] == EXPECTED_OBJECT
               and page["matches"][0]["locator"] == EXPECTED_LOCATOR,
               "EXACT_RETAINED_FUSION_EXPORT")
        F.need(page["new_matches"] == page["matches"] and page["duplicate_matches"] == 0
               and page["metadata_conflicts"] == [], "FIRST_EXACT_CLAIM_IS_NEW")
        record = page["matches"][0]
        rid = F.record_id(record)
        F.need(session.seen_candidates == {(record["object_id"], rid): True}
               and session.candidate_first == {record["object_id"]: rid}, "EXACT_DEDUP_PAIR_STATE")
        save(out / "consumer-candidates.json", page)
        metrics = client.report()
        F.need(metrics["session"]["coverage"] == after_offer["session"]["coverage"]
               and metrics["session"]["last_verified"] == after_offer["session"]["last_verified"] == {},
               "NO_VERIFIED_COVERAGE_OR_CURSOR_PROMOTION")
        F.need(metrics["session"]["last_advisory"] == {sid: {selected["partition"]: {
                   "provider": endpoint.label, "next_cursor": page["advisory_next"],
                   "provider_termination": page["provider_termination"], "verified_scan_coverage": False}}},
               "ONLY_ADVISORY_CONTINUATION_STORED")
        F.need(metrics["session"]["status"] == "ACTIVE"
               and metrics["session"]["used"]["requests"] == 2
               and metrics["session"]["used"]["pages"] == 1
               and metrics["session"]["used"]["providers"] == 1
               and metrics["session"]["snapshot_budget"]
               == {"charged_attempt_slots": 1, "known_snapshot_ids": 1, "limit": 1},
               "ONE_SHARED_FINITE_SESSION")
        F.need(metrics["http"]["completed_requests"] == 2 and metrics["http"]["failed_requests"] == 0
               and len(provider.calls) == len(client.sent) == 2, "EXACTLY_TWO_PUBLIC_HTTP_CALLS")
        F.need(metrics["session"]["used"]["bytes"] == metrics["http"]["actual_reply_bytes"]
               == sum(row["reply_bytes"] for row in provider.calls), "EXACT_REPLY_BYTE_CHARGE")
        F.need(metrics["session"]["used"]["request_bytes"] == metrics["http"]["actual_request_bytes"]
               == sum(row["bytes"] for row in client.sent), "EXACT_SENT_REQUEST_BYTE_ACCOUNTING")
        F.need(metrics["session"]["used"]["examined"] == CANDIDATE_LIMITS["scanned"]
               and metrics["session"]["used"]["candidates"] == 1
               and metrics["session"]["candidate_search"] == {
                   "charged_scan_allowances": CANDIDATE_LIMITS["scanned"], "unique_verified_records": 1,
                   "duplicate_verified_hits": 0, "alternative_metadata_claims": 0,
                   "duplicates_still_charged": True}, "FULL_SCAN_AND_ACTUAL_HIT_CHARGES")
        F.need(metrics["session"]["pending_requests"] == 0
               and all(value == 0 for value in metrics["session"]["reserved"].values()),
               "NO_CLIENT_RESERVATION_LEAK")
        F.need(client.sent[0]["request"] == provider.dispatched[0], "OFFER_DISPATCH_UNCHANGED")
        sent, dispatched = client.sent[1]["request"], deepcopy(provider.dispatched[1])
        F.need(sent["snapshot_id"] == sid and sent["partition"] == selected["partition"]
               and sent["anchor"] == selected["anchor"] and sent["start"] == 0,
               "CANDIDATE_REQUEST_BOUND_TO_RETURNED_PLAN")
        dispatched_timeout = dispatched["limits"]["timeout_ms"]
        F.need(1 <= dispatched_timeout <= sent["limits"]["timeout_ms"], "ONLY_TIMEOUT_MAY_TIGHTEN")
        dispatched["limits"]["timeout_ms"] = sent["limits"]["timeout_ms"]
        F.need(dispatched == sent, "OTHER_DISPATCH_REQUEST_FIELDS_UNCHANGED")
        report.update(snapshot_id=sid, first_nonempty_partition=selected, candidate_count=1,
            candidate_object_ids=[record["object_id"]], candidate_record_ids=[rid],
            public_requests=2, index_rebuilds=0, initial_snapshot_ids=[],
            snapshot_origin="ACTUAL_AUTHENTICATED_OFFER_ONLY", verified_scan_coverage=False,
            coverage_unchanged=True, verified_cursor_unchanged=True,
            session_limits=SESSION_LIMITS, candidate_limits=CANDIDATE_LIMITS,
            dispatched_timeout_ms=dispatched_timeout)
    finally:
        try:
            await provider.stop()
        finally:
            report["provider_final_status"] = provider.status()
            report["calls"] = provider.calls
            if client is not None:
                report["sent"] = [{key: value for key, value in row.items() if key != "request"}
                                  for row in client.sent]
                report["accounting"] = client.report()
            index.close()
    final, metrics = report["provider_final_status"], report["accounting"]
    F.need(final["active"] == final["reserved_reply_bytes"] == final["failures"] == final["refused"] == 0
           and final["requests"] == 2 and provider.server is None and not provider.tasks,
           "PROVIDER_CLEAN_TWO_CALL_CLOSE")
    F.need(final["reply_bytes"] == metrics["http"]["actual_reply_bytes"]
           and final["request_bytes"] == metrics["http"]["actual_request_bytes"]
           and final["header_bytes"] == metrics["http"]["header_bytes"], "MATCHED_PROVIDER_CLIENT_COSTS")
    read_pin(args.database, args.database_sha, 64 * 1024**2)
    read_pin(args.bundle, args.bundle_sha, 2**20)
    report["status"] = "PASS"


def main():
    F.need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
           and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_INVOCATION")
    parser = argparse.ArgumentParser()
    for name in ("database", "database-sha", "bundle", "bundle-sha", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    out = Path(args.output)
    F.need(out.is_absolute() and out.resolve() == out
           and out.is_relative_to(ROOT / "experiments/v5-local-checks") and not out.exists(),
           "FRESH_CANONICAL_OUTPUT")
    out.mkdir()
    report = {"status": "FAIL", "schema": "DMKN_PUBLIC_UNKNOWN_SNAPSHOT_CANDIDATES_V1",
              "mathematical_acceptance": False, "global_complete": False,
              "hosting": "SAME_HOST_LOOPBACK_ONLY", "guest_executions": 0, "proof_calls": 0}
    try:
        asyncio.run(run(args, out, report))
    except BaseException as error:
        report.update(status="FAIL", error={"type": type(error).__name__, "message": str(error)[:1000]})
    save(out / "RESULT.json", report)
    print(json.dumps({key: report.get(key) for key in
                    ("status", "snapshot_id", "candidate_count", "public_requests", "error")}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
