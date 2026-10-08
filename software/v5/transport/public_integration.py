"""Root-selected actual loopback harness over exact pinned owner workload bundles.

No fixture regeneration, certificates, native checking or mathematical admission.
The consumer receives symbolic query/relative names, never target content IDs.
"""
from pathlib import Path
import argparse
import asyncio
from copy import deepcopy
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from discovery import formal_features as F
from discovery.module_export_adapter import ModuleExportAdapter, compile_query, SLOTS
from discovery.discovery_store import Store
from discovery.search_session import SearchSession
from custody.module_store import ModuleStore, BODY_SCHEMA, permitted_hashes
from transport.http_provider import Provider
from transport.clients import SearchClient, AcquisitionClient

INDEX_LIMITS = dict(max_objects=256, max_postings=32768, max_features=8192,
                    max_snapshots=257, max_logical_bytes=134217728, max_db_pages=65536)
CUSTODY_LIMITS = dict(modules=16, groups=256, declarations=256, bodies=256,
                      logical_bytes=134217728, db_pages=65536)
SESSION_LIMITS = dict(providers=2, snapshots=1, requests=66, pages=64, examined=1024,
                     candidates=256, bytes=16777216, wall_ms=120000, inflight=1)
PAGE_LIMITS = dict(examined=16, matches=8, bytes=262144, timeout_ms=1000, node_reads=100000)


def read_pinned(path, expected, maximum):
    path = Path(path); F.need(path.is_absolute(), "PINNED_ABSOLUTE_PATH")
    F.hexid(expected); F.need(0 < path.stat().st_size <= maximum, "PINNED_INPUT_BYTES")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    F.need(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == expected, "PINNED_INPUT_HASH")
    value = C.parse_json(raw)
    # Root's human-authored selection may carry one LF; actual bundle canonical
    # bytes remain exact. Hash pins include every input byte in either case.
    return value


def save(path, value):
    raw = C.canonical(value)
    with Path(path).open("xb") as stream: stream.write(raw)


def check_bundle(value):
    F.fields(value, ("schema", "module", "spec", "openings", "bodies",
                     "mathematical_admission", "certificate_verification"))
    F.need(value["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
           and value["mathematical_admission"] is False
           and value["certificate_verification"] == "NOT_PERFORMED", "WORKLOAD_BUNDLE_ASSURANCE")
    F.need(C.module_id(value["spec"]) == value["module"], "WORKLOAD_MODULE_BINDING")
    F.need(type(value["openings"]) is list and len(value["openings"]) == len(value["spec"]["groups"]), "WORKLOAD_OPENINGS")
    for i, opening in enumerate(value["openings"]):
        F.need(opening["index"] == i and C.verify_group_opening(value["module"], opening)
               == value["spec"]["groups"][i], "WORKLOAD_GROUP_BINDING")
    F.need(type(value["bodies"]) is list and len(value["bodies"]) <= 256, "WORKLOAD_BODY_COUNT")
    for body in value["bodies"]:
        F.fields(body, ("universes", "digest", "expression"))
        F.need(C.body_id(body["expression"], body["universes"]) == body["digest"], "WORKLOAD_BODY_BINDING")


def compile_selection(adapter, selection):
    F.fields(selection, ("schema", "query_specs", "target_name", "body_name", "group_max_bytes", "body_max_bytes"))
    F.need(selection["schema"] == "DMKN_DISCOVERY_PUBLIC_USE_SELECTION_V1", "PUBLIC_SELECTION_SCHEMA")
    C.validate_name(selection["target_name"]); C.validate_name(selection["body_name"])
    F.uint(selection["group_max_bytes"], 1024, 16*1024**2); F.uint(selection["body_max_bytes"], 1024, 16*1024**2)
    F.need(type(selection["query_specs"]) is list and 1 <= len(selection["query_specs"]) <= 8, "PUBLIC_SELECTION_QUERY")
    specs = []
    for spec in selection["query_specs"]:
        if type(spec) is dict and spec.get("tag") == "result-head-foundation-name":
            F.fields(spec, ("tag", "foundation_name")); C.validate_name(spec["foundation_name"])
            specs.append({"tag": "result-head", "head": {"tag": "const", "symbol": {
                "kind": "foundation-name", "name_hash": C.hash_value("foundation-symbol", spec["foundation_name"])}}})
        else: specs.append(spec)
    return compile_query(adapter.namespace, specs)


def external_owner(descriptor, relative_name):
    found, todo = set(), [descriptor["type"]]
    expected = C.name_key(relative_name)
    while todo:
        expr = todo.pop()
        if expr[0] in ("const", "proj") and expr[1][0] == "external" and C.name_key(expr[1][2]) == expected:
            found.add(expr[1][1])
        todo.extend(expr[index] for _, index in SLOTS[expr[0]])
    F.need(len(found) == 1, "EXACT_EXTERNAL_BODY_OWNER_IN_TARGET_TYPE")
    return found.pop()


async def run(bundles, selection, evidence):
    for bundle in bundles: check_bundle(bundle)
    foundation, policy = bundles[0]["spec"]["foundation"], bundles[0]["spec"]["policy"]
    F.need(all(b["spec"]["foundation"] == foundation and b["spec"]["policy"] == policy for b in bundles), "ONE_DISCOVERY_NAMESPACE")
    adapter = ModuleExportAdapter(C, foundation, policy)
    features = compile_selection(adapter, selection)
    stores, providers, report = [], [], {"schema": "DMKN_PUBLIC_DISCOVERY_INTEGRATION_V1", "events": [],
        "mathematical_admission": False, "certificate_verification": "NOT_PERFORMED",
        "hosting": "SAME_HOST_LOOPBACK_ONLY", "candidate_foundation": foundation, "candidate_policy": policy}
    def event(kind, **values): report["events"].append({"event": kind, **values})
    try:
        index_a = Store(evidence/"index-a", adapter, INDEX_LIMITS, create=True); stores.append(index_a)
        index_b = Store(evidence/"index-b", adapter, INDEX_LIMITS, create=True); stores.append(index_b)
        custody = ModuleStore(evidence/"custodian", C, foundation, policy, CUSTODY_LIMITS, create=True); stores.append(custody)
        receiver = ModuleStore(evidence/"receiver", C, foundation, policy, CUSTODY_LIMITS, create=True); stores.append(receiver)
        published = 0
        for bundle in bundles:
            module = bundle["module"]
            body_map = {(b["universes"], b["digest"]): b["expression"] for b in bundle["bodies"]}
            for opening in bundle["openings"]:
                custody.put_group(module, opening)
                for descriptor in opening["group"]["declarations"]:
                    raw = adapter.encode_opening(module, descriptor["name"], opening)
                    index_a.admit(raw); index_b.admit(raw); published += 1
                    for digest in permitted_hashes(descriptor):
                        key = descriptor["universes"], digest
                        F.need(key in body_map, "COMMITTED_WORKLOAD_BODY_MISSING")
                        custody.put_body(module, descriptor["name"], {"schema": BODY_SCHEMA,
                            "module_id": module, "relative_name": descriptor["name"], "universes": key[0],
                            "body_hash": digest, "expression": body_map[key]})
        sid = index_a.status()["latest"]
        F.need(sid == index_b.status()["latest"], "REPLACEABLE_SNAPSHOT_BINDING")
        event("PUBLISHED_SELECTED_EXPORTS", exports=published, snapshot_id=sid)
        a, b, c = Provider(index=index_a), Provider(index=index_b), Provider(custody=custody)
        providers.extend([a, b, c])
        endpoint_a, endpoint_b, endpoint_c = await a.start(), await b.start(), await c.start()
        client = SearchClient(SearchSession(adapter.namespace, features, SESSION_LIMITS), {"a": endpoint_a, "b": endpoint_b})
        summary = await client.summary("a", sid, 1048576)
        nonempty = [p for p in summary["partitions"] if p["anchor_count"]]
        F.need(nonempty, "NO_MATCHING_SELECTED_ANCHOR")
        first_plan = nonempty[0]
        first = await client.page("a", sid, first_plan["partition"], 0, PAGE_LIMITS)
        matches = list(first["matches"])
        event("A_FIRST_VERIFIED_PAGE", partition=first_plan["partition"], start=0, next=first["next"],
              anchor_count=first["anchor_count"], next_cursor=first["next_cursor"])
        await a.stop(); event("A_STOPPED", active=a.status()["active"])
        continuation = "SAME_VECTOR_CURSOR" if first["next_cursor"] is not None else "SAME_SNAPSHOT_REMAINING_PARTITIONS"
        b_pages = 0
        for plan in nonempty:
            position = first["next"] if plan["partition"] == first_plan["partition"] else 0
            while position < plan["anchor_count"]:
                F.need(b_pages < 63, "FINITE_PUBLIC_PAGE_CEILING")
                page = await client.page("b", sid, plan["partition"], position, PAGE_LIMITS)
                F.need(page["next"] > position, "PUBLIC_PAGE_NO_PROGRESS")
                event("B_VERIFIED_PAGE", partition=plan["partition"], start=position, next=page["next"])
                matches.extend(page["matches"]); position = page["next"]; b_pages += 1
        F.need(b_pages > 0, "NO_ACTUAL_POST_LOSS_CONTINUATION")
        selected = [r for r in matches if C.name_key(r["locator"]["relative_name"]) == C.name_key(selection["target_name"])]
        F.need(len(selected) == 1, "EXACT_DISCOVERED_TARGET")
        acquisition = AcquisitionClient(adapter, {"custodian": endpoint_c}, requests=8, bytes=33554432,
                                        wall_ms=60000, local_custody=receiver)
        resolved = await acquisition.export("custodian", selected[0])
        save(evidence/"acquired-target.json", resolved)
        owner = external_owner(resolved["descriptor"], selection["body_name"])
        body_declaration = await acquisition.declaration("custodian", owner, selection["body_name"], selection["group_max_bytes"])
        digest = body_declaration["descriptor"]["value_hash"]
        F.need(body_declaration["descriptor"]["kind"] == "definition" and digest is not None, "DEMANDED_DEFINITION")
        event("TARGET_ACQUIRED_AND_BODY_ADDRESS_DERIVED", export_id=resolved["export_id"], module_id=resolved["locator"]["module_id"],
              body_owner=owner, body_hash=digest, mathematical_acceptance=False)
        await c.stop(); custody.close()
        reopened = ModuleStore(evidence/"custodian", C, foundation, policy, CUSTODY_LIMITS); stores.append(reopened)
        replacement = Provider(custody=reopened); providers.append(replacement)
        endpoint_replacement = await replacement.start()
        acquisition.endpoints["custodian"] = endpoint_replacement
        body = await acquisition.body("custodian", body_declaration, digest, selection["body_max_bytes"])
        save(evidence/"acquired-body.json", body)
        event("CUSTODIAN_RESTARTED_BODY_ACQUIRED", body_hash=body["body"]["body_hash"], mathematical_acceptance=False)
        report.update(status="PASS", continuation=continuation, discovered_matches=len(matches),
                      consumer_api_input_contains_target_content_id=False, search=client.report(), acquisition=acquisition.report(),
                      provider_status=[p.status() for p in providers], receiver=receiver.status())
    except BaseException as error:
        report.update(status="FAIL", error={"type": type(error).__name__, "message": str(error)[:1000]})
        raise
    finally:
        for provider in reversed(providers): await provider.stop()
        report["provider_final_status"] = [p.status() for p in providers]
        for store in reversed(stores): store.close()
        save(evidence/"RESULT.json", report)
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", action="append", required=True)
    p.add_argument("--bundle-sha256", action="append", required=True)
    p.add_argument("--selection", required=True); p.add_argument("--selection-sha256", required=True)
    p.add_argument("--evidence", required=True)
    args = p.parse_args(); evidence = Path(args.evidence)
    F.need(evidence.is_absolute() and not evidence.exists(), "FRESH_ABSOLUTE_EVIDENCE")
    F.need(1 <= len(args.bundle) <= 8 and len(args.bundle) == len(args.bundle_sha256), "EXPLICIT_BUNDLE_PINS")
    bundles = [read_pinned(path, pin, 16*1024**2) for path, pin in zip(args.bundle, args.bundle_sha256)]
    selection = read_pinned(args.selection, args.selection_sha256, 16384)
    evidence.mkdir(parents=True)
    report = asyncio.run(run(bundles, selection, evidence))
    print(json.dumps({"status": report["status"], "events": len(report["events"]), "mathematical_admission": False}))
    return 0


if __name__ == "__main__": raise SystemExit(main())
