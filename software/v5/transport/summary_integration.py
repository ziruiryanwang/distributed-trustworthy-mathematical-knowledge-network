"""Two public summary encodings over ONE retained index, with no rebuilding.

Owner-controlled loopback test. Copies exact pinned closed SQLite bytes to fresh
state, then uses the actual Store/Provider/SearchClient path. No pages, custody,
Lean, proof generation, failover campaign or mathematical admission is repeated.
"""
from pathlib import Path
import argparse
import asyncio
import hashlib
import json
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery import summary_wire as W
from discovery.discovery_store import Store
from discovery.module_export_adapter import ModuleExportAdapter, compile_query
from discovery.search_session import SearchSession
from transport.http_provider import Provider
from transport.clients import SearchClient

LIMITS = dict(providers=1, snapshots=1, requests=1, pages=1, examined=1,
              candidates=1, bytes=1048576, wall_ms=15000, inflight=1)


def read_pin(path, digest, maximum):
    path = Path(path)
    F.need(path.is_absolute() and path.is_file() and 0 < path.stat().st_size <= maximum, "PINNED_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    F.need(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == digest, "PINNED_FILE_HASH")
    return raw


def save(path, value):
    with path.open("xb") as stream:
        stream.write(F.compact(value))


class RecordingProvider(Provider):
    """Logging only: neither alter nor replace the actual dispatch result."""
    def __init__(self, index, evidence):
        super().__init__(index=index, max_requests=2, max_reply_bytes=2**20)
        self.evidence, self.encoded = evidence, {}

    def dispatch(self, route, request, *, check_budget=None):
        result = super().dispatch(route, request, check_budget=check_budget)
        raw = result if type(result) is bytes else F.compact(result)
        label = "compact" if route.endswith("summary-compact") else "expanded"
        F.need(label not in self.encoded, "NO_REPEATED_SUMMARY")
        with (self.evidence / (label + ".response.json")).open("xb") as stream:
            stream.write(raw)
        self.encoded[label] = raw
        return result


async def run(args, out, report):
    original = read_pin(args.database, args.database_sha, 64 * 1024**2)
    bundle = C.parse_json(read_pin(args.bundle, args.bundle_sha, 2**20))
    reference = json.loads(read_pin(args.reference, args.reference_sha, 2**20))
    F.need(reference["status"] == "PASS", "PASSED_REFERENCE_REQUIRED")
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
    provider = RecordingProvider(index, out)
    clients = {}
    try:
        sid = index.status()["latest"]
        F.need(sid == reference["snapshot_ids"][-1], "EXACT_RETAINED_SNAPSHOT")
        endpoint = await provider.start()
        for label, encoding, byte_cap in (("expanded", "expanded-v1", 1048576),
                                          ("compact", "compact-v1", 8192)):
            client = SearchClient(SearchSession(adapter.namespace, features, LIMITS), {"index": endpoint})
            result = await client.summary("index", sid, byte_cap, encoding=encoding,
                                          max_expanded_bytes=1048576)
            F.need(result["status"] == "VERIFIED_SUMMARY", "ACTUAL_PUBLIC_VERIFICATION")
            clients[label] = client
        expanded, compact = provider.encoded["expanded"], provider.encoded["compact"]
        F.need(len(expanded) == reference["compatibility"]["summary_bytes"]
               and hashlib.sha256(expanded).hexdigest() == reference["compatibility"]["summary_sha256"],
               "EXACT_PREVIOUSLY_CHECKED_EXPANDED_SUMMARY")
        restored = W.decode_summary(compact, sid, adapter.namespace, features, max_wire_bytes=8192)
        F.need(F.compact(restored) == expanded, "EXACT_WIRE_RECONSTRUCTION")
        F.need(clients["expanded"].session.summaries[sid] == clients["compact"].session.summaries[sid],
               "SAME_VERIFIED_SUMMARY")
        F.need(len(compact) * 5 <= len(expanded), "PROSPECTIVE_EIGHTY_PERCENT_WIRE_REDUCTION")
        accounting = {}
        for label, client in clients.items():
            metrics = client.report()
            F.need(metrics["session"]["used"]["bytes"] == metrics["http"]["actual_reply_bytes"]
                   == len(provider.encoded[label]), "ACTUAL_WIRE_BYTE_CHARGE")
            F.need(metrics["session"]["pending_requests"] == 0
                   and all(n == 0 for n in metrics["session"]["reserved"].values()), "NO_RESERVATION_LEAK")
            F.need(metrics["http"]["completed_requests"] == 1 and metrics["http"]["failed_requests"] == 0,
                   "ONE_PUBLIC_SUMMARY_PER_ENCODING")
            accounting[label] = {"session_used": metrics["session"]["used"], "http": metrics["http"]}
        report.update(status="PASS", snapshot_id=sid, index_rebuilds=0, public_requests=2,
                      expanded_bytes=len(expanded), compact_bytes=len(compact),
                      wire_reduction_fraction=1-len(compact)/len(expanded), accounting=accounting)
    finally:
        await provider.stop()
        report["provider_final_status"] = provider.status()
        index.close()
    F.need(report["provider_final_status"]["active"] == 0
           and report["provider_final_status"]["reserved_reply_bytes"] == 0, "PROVIDER_CLEAN_CLOSE")
    read_pin(args.database, args.database_sha, 64 * 1024**2)


def main():
    parser = argparse.ArgumentParser()
    for name in ("database", "database-sha", "bundle", "bundle-sha", "reference", "reference-sha", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    out = Path(args.output)
    F.need(out.is_absolute() and not out.exists(), "FRESH_OUTPUT")
    out.mkdir()
    report = {"status": "FAIL", "schema": "DMKN_PUBLIC_SUMMARY_WIRE_COMPARISON_V1",
              "mathematical_acceptance": False, "hosting": "SAME_HOST_LOOPBACK_ONLY"}
    try:
        asyncio.run(run(args, out, report))
    except BaseException as error:
        report.update(status="FAIL", error={"type": type(error).__name__, "message": str(error)[:1000]})
    save(out / "RESULT.json", report)
    print(json.dumps({key: report.get(key) for key in
                    ("status", "expanded_bytes", "compact_bytes", "wire_reduction_fraction", "error")}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
