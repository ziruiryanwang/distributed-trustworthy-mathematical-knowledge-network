"""One public unknown-snapshot offer, then one authenticated candidate page.

Owner-selected loopback integration over a fresh copy of exact retained closed
index bytes. The consumer knows its namespace/features and an approved contact,
but obtains its snapshot ID and partition plan ONLY from the actual offer.
No index rebuild, provider failover, Lean/proof call or mathematical admission.
"""
from pathlib import Path
import argparse
import asyncio
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
from transport.http_provider import Provider, OFFER_ROUTE
from transport.clients import SearchClient
from transport.summary_integration import read_pin, save

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OFFER_BYTES = 8192
PAGE_LIMITS = dict(examined=32, matches=8, bytes=131072,
                   timeout_ms=1000, node_reads=32768)
SESSION_LIMITS = dict(providers=1, snapshots=1, requests=2, pages=1,
                      examined=32, candidates=8, bytes=139264,
                      wall_ms=15000, inflight=1)


class RecordingProvider(Provider):
    """Record actual request/reply bytes without changing dispatch results."""
    def __init__(self, index, evidence):
        # The unchanged page route reserves its 1-MiB route ceiling, distinct
        # from the tighter client page cap. Fund that advertised server cost.
        super().__init__(index=index, max_requests=2, max_reply_bytes=2**21)
        self.evidence, self.calls = evidence, []

    def dispatch(self, route, request, *, check_budget=None):
        ordinal = len(self.calls)
        F.need(ordinal < 2 and route == (OFFER_ROUTE if ordinal == 0
                                        else "/v5/discovery/page"), "EXACT_TWO_CALL_SEQUENCE")
        if ordinal == 0:
            F.need("snapshot_id" not in request, "OFFER_HAS_NO_PRESELECTED_SNAPSHOT")
        request_raw = F.compact(request)
        with (self.evidence / f"request-{ordinal}.json").open("xb") as stream:
            stream.write(request_raw)
        started_cpu, started_wall = time.process_time(), time.monotonic()
        result = super().dispatch(route, request, check_budget=check_budget)
        raw = result if type(result) is bytes else F.compact(result)
        with (self.evidence / f"response-{ordinal}.json").open("xb") as stream:
            stream.write(raw)
        self.calls.append({"route": route, "request_bytes": len(request_raw),
            "reply_bytes": len(raw), "request_sha256": hashlib.sha256(request_raw).hexdigest(),
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
        client = SearchClient(session, {"contact": endpoint})
        initial = client.report()
        F.need(not session.summaries and not session.attempted_snapshots
               and not session.offer_hints and initial["session"]["snapshot_budget"]
               == {"charged_attempt_slots": 0, "known_snapshot_ids": 0, "limit": 1},
               "CLIENT_STARTS_WITH_NO_SNAPSHOT_ID_OR_PLAN")
        save(out / "consumer-initial.json", initial)
        offered = await client.offer("contact", OFFER_BYTES,
            max_expanded_bytes=1048576, max_age_ms=60000)
        F.need(offered["status"] == "OFFERED"
               and offered["assurance"] == "AUTHENTICATED_PROVIDER_SELECTED_METADATA_ONLY"
               and offered["global_complete"] is False
               and offered["mathematical_acceptance"] is False, "AUTHENTICATED_OFFER_ONLY")
        save(out / "consumer-offer.json", offered)
        # This is the sole source of the SID and selected partition. In
        # particular, no index.status(), reference SID or direct summary call.
        selected = next((row for row in offered["partitions"] if row["anchor_count"] > 0), None)
        F.need(selected is not None and selected["committed_empty"] is False,
               "OFFER_HAS_NONEMPTY_PARTITION")
        sid = offered["snapshot_id"]
        page = await client.page("contact", sid, selected["partition"], 0, PAGE_LIMITS)
        F.need(page["status"] == "VERIFIED_PAGE" and page["snapshot_id"] == sid
               and page["partition"] == selected["partition"]
               and page["anchor"] == selected["anchor"] and page["start"] == 0
               and page["assurance"] == "VERIFIED_COMMITTED_INTERVAL"
               and page["mathematical_acceptance"] is False, "ACTUAL_AUTHENTICATED_PAGE")
        F.need(1 <= len(page["matches"]) <= PAGE_LIMITS["matches"],
               "FIRST_NONEMPTY_PARTITION_RETURNS_ACTUAL_CANDIDATE")
        save(out / "consumer-page.json", page)
        metrics = client.report()
        F.need(metrics["session"]["status"] == "ACTIVE"
               and metrics["session"]["used"]["requests"] == 2
               and metrics["session"]["used"]["pages"] == 1
               and metrics["session"]["used"]["providers"] == 1
               and metrics["session"]["snapshot_budget"]
               == {"charged_attempt_slots": 1, "known_snapshot_ids": 1, "limit": 1},
               "ONE_SHARED_FINITE_SESSION")
        F.need(metrics["http"]["completed_requests"] == 2
               and metrics["http"]["failed_requests"] == 0
               and len(provider.calls) == 2, "EXACTLY_TWO_PUBLIC_HTTP_CALLS")
        F.need(metrics["session"]["used"]["bytes"] == metrics["http"]["actual_reply_bytes"]
               == sum(row["reply_bytes"] for row in provider.calls), "EXACT_REPLY_BYTE_CHARGE")
        F.need(metrics["session"]["used"]["request_bytes"] == metrics["http"]["actual_request_bytes"]
               == sum(row["request_bytes"] for row in provider.calls), "EXACT_REQUEST_BYTE_ACCOUNTING")
        F.need(metrics["session"]["used"]["examined"] == page["next"]
               and metrics["session"]["used"]["candidates"] == len(page["matches"]),
               "EXACT_EXAMINED_AND_CANDIDATE_CHARGE")
        F.need(metrics["session"]["pending_requests"] == 0
               and all(value == 0 for value in metrics["session"]["reserved"].values()),
               "NO_CLIENT_RESERVATION_LEAK")
        report.update(snapshot_id=sid, first_nonempty_partition=selected,
            candidate_count=len(page["matches"]), candidate_object_ids=[row["object_id"] for row in page["matches"]],
            public_requests=2, index_rebuilds=0, initial_snapshot_ids=[],
            snapshot_origin="ACTUAL_AUTHENTICATED_OFFER_ONLY",
            session_limits=SESSION_LIMITS, page_limits=PAGE_LIMITS)
    finally:
        try:
            await provider.stop()
        finally:
            report["provider_final_status"] = provider.status()
            report["calls"] = provider.calls
            if client is not None:
                report["accounting"] = client.report()
            index.close()
    final, metrics = report["provider_final_status"], report["accounting"]
    F.need(final["active"] == final["reserved_reply_bytes"] == final["failures"] == final["refused"] == 0
           and final["requests"] == 2, "PROVIDER_CLEAN_TWO_CALL_CLOSE")
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
           and out.is_relative_to(ROOT / "experiments/v5-local-checks")
           and not out.exists(), "FRESH_CANONICAL_OUTPUT")
    out.mkdir()
    report = {"status": "FAIL", "schema": "DMKN_PUBLIC_UNKNOWN_SNAPSHOT_OFFER_V1",
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
