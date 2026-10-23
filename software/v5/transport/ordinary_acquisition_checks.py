"""Focused ordinary acquisition controls; root selects execution separately.

Actual loopback Provider/exchange and cold SQLite custody plus explicitly mocked
hostile replies/failures. Fixtures are synthetic unproved syntax, never kernel
mathematics. All retained output is under required fresh absolute --store-root.
No external hosts, Lean, index/TLS suite repeats, certificate or catalog admission.
"""
from pathlib import Path
import argparse
import asyncio
from copy import deepcopy
import sys
import time
from unittest.mock import patch

sys.dont_write_bytecode = True
V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V5))
sys.path.insert(0, str(V5 / "ordinary_lean"))
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from discovery.ordinary_export_adapter import OrdinaryExportAdapter
from transport import ordinary_acquisition as O
from transport import http_provider as H
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_preview as P
import semantic_identity_checks as Fixtures


LIMITS = {"objects": 16, "exports": 32, "logical_bytes": 2*1024*1024, "db_pages": 1024}


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(marker, action):
    try:
        action()
    except ValueError as exc:
        ensure(marker == str(exc), "WRONG_REFUSAL:"+str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:"+marker)


async def refuses_async(marker, action):
    try:
        await action()
    except ValueError as exc:
        ensure(marker == str(exc), "WRONG_REFUSAL:"+str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:"+marker)


def report(label):
    print("ORDINARY_ACQUISITION_CHECK "+label+" PASS mathematical_acceptance=false", flush=True)


def save(root, name, raw):
    path = ordinary(root / name, fresh=True, directory=False)
    with path.open("xb") as stream:
        stream.write(raw)


def group_fixture(semantic):
    """Two-output inductive-shaped inert syntax, not a checked inductive type."""
    own, ctor = Fixtures.name("SyntheticAcquisitionType"), Fixtures.name("SyntheticAcquisitionConstructor")
    sort = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    target = [E.EXPR_FORMAT, [], [[2, own, []]], 0]
    descriptor = [3, [], 0, [[own, sort, [[ctor, target]]]]]
    inventory = [[own, 4, [], sort, [0, 0, [own], [ctor], 0, 0, 0, 0]],
                 [ctor, 5, [], target, [own, 0, 0, 0, 0]]]
    return E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
        "imports": [], "unit": [E.UNIT_FORMAT, descriptor, inventory]})


def fixtures(root):
    semantic = S.semantic_id()
    raw = Fixtures.evidence(semantic)
    alias = E.strict_json(raw)
    one = [E.EXPR_FORMAT, [], [[7, {"$bytes": [1]}]], 0]
    alias["unit"][1][4] = one
    alias["unit"][2][0][4][0] = one
    alias_raw = E.canonical_json(alias)
    group = group_fixture(semantic)
    own = Fixtures.name("SyntheticIdentityDeclaration")
    preview = P.preview_from_evidence(raw, own)
    # This initial pure parse is fixture validation, not mathematical acceptance.
    for data in (raw, alias_raw, group):
        PE.read_evidence(data)
    for label, data in (("evidence.json", raw), ("same-name-other-unit.json", alias_raw),
                        ("multi-output-unit.json", group), ("preview.json", preview)):
        save(root, label, data)
    return semantic, raw, alias_raw, group, own, preview


def atomic_controls(root, semantic, raw, alias, group, guard):
    store = O.OrdinaryStore(root / "atomic", semantic, LIMITS, create=True)
    try:
        store.put_evidence(raw, before_commit=guard)
        before = deepcopy(store.status())
        duplicate = store.put_evidence(raw, before_commit=guard)
        ensure(not duplicate["new"] and store.status() == before, "DUPLICATE_CHARGED_OR_CHANGED")
        store.put_evidence(alias, before_commit=guard)
        store.put_evidence(group, before_commit=guard)
        identities = []
        for data in (raw, alias, group):
            parsed = PE.read_evidence(data)
            for output in parsed.document["unit"][2]:
                export = PE.export_id(semantic, parsed.unit_id, output[0])
                identities.append(export)
                locator = P.read_locator(E.strict_json(store.get_locator(semantic, export, 4096)))
                ensure(locator["unit_id"] == parsed.unit_id and locator["export_name"] == output[0],
                       "MISSING_OR_ALIASED_OUTPUT_LOCATOR")
            ensure(store.get_evidence(semantic, parsed.unit_id, len(data)) == data, "EXACT_STORED_BYTES")
        counts = store.status()["counts"]
        ensure(counts["objects"] == 3 and counts["exports"] == 4 and len(set(identities)) == 4,
               "SAME_NAME_OR_MULTI_OUTPUT_COLLAPSED")
    finally:
        store.close()

    for label, limits, callback_failure in (("export-quota", {**LIMITS, "exports": 1}, False),
                                            ("rollback-after-first-locator", LIMITS, True)):
        failed = O.OrdinaryStore(root / label, semantic, limits, create=True)
        try:
            def callback():
                guard()
                if failed.db.in_transaction and failed.db.execute("SELECT count(*) FROM exports").fetchone()[0] > 0:
                    raise ValueError("SYNTHETIC_CALLBACK_AFTER_PARTIAL_PROJECTION")
            marker = "SYNTHETIC_CALLBACK_AFTER_PARTIAL_PROJECTION" if callback_failure else "ORDINARY_CUSTODY_QUOTA"
            refuses(marker, lambda: failed.put_evidence(group, before_commit=callback if callback_failure else guard))
            ensure(failed.status()["counts"] == {"objects": 0, "exports": 0, "logical_bytes": 0},
                   "PARTIAL_UNIT_OR_LOCATORS_SURVIVED")
            parsed = PE.read_evidence(group)
            for row in parsed.document["unit"][2]:
                export = PE.export_id(semantic, parsed.unit_id, row[0])
                refuses("ORDINARY_EXPORT_LOCALLY_UNAVAILABLE", lambda: failed.get_locator(semantic, export, 4096))
            refuses("ORDINARY_OBJECT_UNAVAILABLE", lambda: failed.get_evidence(semantic, parsed.unit_id, len(group)))
        finally:
            failed.close()
    report("atomic_all_outputs_aliases_idempotence_quota_and_callback_rollback")


async def loopback_controls(root, semantic, raw, own, preview, deadline, guard):
    adapter = OrdinaryExportAdapter(semantic)
    record = adapter.extract(preview)
    unit = PE.read_evidence(raw).unit_id
    source = O.OrdinaryStore(root / "supplier", semantic, LIMITS, create=True)
    receiver = O.OrdinaryStore(root / "receiver", semantic, LIMITS, create=True)
    providers = []
    restarted = None
    budget = O.OrdinaryBudget(deadline=deadline, requests=8, reply_bytes=65536)
    try:
        source.put_evidence(raw, before_commit=guard)
        source.put_preview(preview, before_commit=guard)
        first = H.Provider(ordinary=source, max_requests=8, max_reply_bytes=65536, operation_ms=2000)
        providers.append(first)
        endpoint = await first.start()
        client = O.OrdinaryAcquisition(adapter, {"first": endpoint}, budget, local_custody=receiver)
        fetched_preview = await client.preview("first", record)
        found = await client.locator("first", semantic, record["object_id"], 4096, expected_name=own)
        fetched = await client.evidence("first", semantic, found["locator"]["unit_id"], 4096,
            expected_export_id=record["object_id"], expected_export_name=own)
        ensure(fetched["raw"] == raw and fetched_preview["raw"] == preview and
               found["locator"]["unit_id"] == unit and not P.resolve(preview, raw)["mathematical_acceptance"],
               "ACTUAL_TYPED_FETCH_BINDING")
        ensure(budget.report()["requests"] == 3 and budget.report()["pending_requests"] == 0 and
               first.status()["requests"] == 3, "ACTUAL_ROUTE_ACCOUNTING")
        report("actual_loopback_preview_export_locator_and_exact_evidence")

        await first.stop(); source.close(); receiver.close()
        restarted = O.OrdinaryStore(root / "receiver", semantic, LIMITS)
        replacement = H.Provider(ordinary=restarted, max_requests=8, max_reply_bytes=65536, operation_ms=2000)
        providers.append(replacement)
        replacement_endpoint = await replacement.start()
        cold = O.OrdinaryAcquisition(adapter, {"replacement": replacement_endpoint}, budget)
        ensure(cold.budget is client.budget and cold.budget.deadline == deadline, "BUDGET_RENEWED_AT_PROVIDER_CHANGE")
        cold_preview = await cold.preview("replacement", record)
        cold_locator = await cold.locator("replacement", semantic, record["object_id"], 4096, expected_name=own)
        cold_evidence = await cold.evidence("replacement", semantic, cold_locator["locator"]["unit_id"], 4096,
            expected_export_id=record["object_id"], expected_export_name=own)
        ensure(cold_preview["raw"] == preview and cold_evidence["raw"] == raw and
               first.server is None and not first.tasks and budget.report()["requests"] == 6,
               "COLD_CUSTODY_NOT_INDEPENDENT_OF_ORIGINAL_PROVIDER")
        before = budget.report()["charged_reply_bytes"]
        try:
            await cold.evidence("replacement", semantic, "0"*64, 4096)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        else:
            raise AssertionError("MISSING_ACTUAL_PROVIDER_UNAVAILABLE_FAILURE")
        ensure(budget.report()["requests"] == 7 and budget.report()["charged_reply_bytes"] == before+4096 and
               budget.report()["pending_requests"] == 0 and cold.report()["http"]["failed_attempts"] == 1 and
               replacement.status()["failures"] == 1, "ACTUAL_FAILURE_NOT_CHARGED")
        save(root, "loopback-report.json", F.compact({"first": client.report(), "replacement": cold.report(),
             "original_provider": first.status(), "replacement_provider": replacement.status()}))
        report("cold_reopen_reserves_same_budget_and_actual_missing_route_charged")
    finally:
        for provider in reversed(providers):
            await provider.stop()
        for store in (source, receiver, restarted):
            if store is not None:
                store.close()


async def mutant_controls(root, semantic, raw, own, deadline):
    adapter = OrdinaryExportAdapter(semantic)
    unit = PE.read_evidence(raw).unit_id
    export = PE.export_id(semantic, unit, own)
    locator = {"schema": P.LOCATOR_SCHEMA, "semantic_id": semantic, "unit_id": unit, "export_name": own}
    budget = O.OrdinaryBudget(deadline=deadline, requests=10, reply_bytes=65536)
    client = O.OrdinaryAcquisition(adapter, {"mock": H.Endpoint("127.0.0.1", 1)}, budget)
    returned = [b""]
    calls = []
    async def synthetic_reply(endpoint, route, request, maximum, timeout_ms):
        calls.append(route)
        ensure(len(returned[0]) <= maximum, "MUTANT_EXCEEDS_TEST_RESPONSE_CAP")
        return {"status": 200, "raw": returned[0], "request_bytes": len(F.compact(request)),
                "reply_bytes": len(returned[0]), "header_bytes": 0, "elapsed_ms": 0}
    cases = [("malformed", {}, "PORTABLE_LOCATOR_FIELDS", own),
             ("wrong-semantic", {**locator, "semantic_id": "0"*64}, "ORDINARY_LOCATOR_EXACT_EXPORT", own),
             ("wrong-unit", {**locator, "unit_id": "1"*64}, "ORDINARY_LOCATOR_EXACT_EXPORT", own),
             ("wrong-name", locator, "ORDINARY_LOCATOR_EXPECTED_NAME", Fixtures.name("NotThatName"))]
    with patch.object(H, "exchange", synthetic_reply):
        for label, value, marker, expected_name in cases:
            returned[0] = E.canonical_json(value)
            save(root, label+"-locator.json", returned[0])
            before = budget.report()["charged_reply_bytes"]
            await refuses_async(marker, lambda: client.locator("mock", semantic, export, 4096,
                                                                 expected_name=expected_name))
            ensure(budget.report()["charged_reply_bytes"] == before+4096 and
                   budget.report()["pending_requests"] == 0, "MUTANT_NOT_CHARGED")
        omitted = Fixtures.name("SyntheticAbsentOutput")
        claimed_export = PE.export_id(semantic, unit, omitted)
        returned[0] = E.canonical_json({**locator, "export_name": omitted})
        save(root, "self-consistent-but-absent-output-locator.json", returned[0])
        claim = await client.locator("mock", semantic, claimed_export, 4096, expected_name=omitted)
        ensure(not claim["mathematical_acceptance"], "LOCATOR_BECAME_ACCEPTANCE")
        returned[0] = raw
        before = budget.report()["charged_reply_bytes"]
        await refuses_async("ORDINARY_EVIDENCE_EXPORT_OMISSION", lambda: client.evidence("mock", semantic, unit,
            4096, expected_export_id=claimed_export, expected_export_name=omitted))
        ensure(budget.report()["charged_reply_bytes"] == before+4096 and
               client.report()["http"]["failed_attempts"] == 5 and len(calls) == 6,
               "OMITTED_OUTPUT_NOT_CHARGED")
    save(root, "mocked-binding-report.json", F.compact(client.report()))
    report("mocked_locator_mismatch_and_actual_output_omission_refused_charged")


async def aggregate_controls(root, semantic, raw, deadline):
    adapter, unit = OrdinaryExportAdapter(semantic), PE.read_evidence(raw).unit_id
    calls = []
    async def synthetic_failure(endpoint, route, request, maximum, timeout_ms):
        calls.append(endpoint.port)
        raise OSError("SYNTHETIC_TRANSPORT_FAILURE")
    endpoints = {"a": H.Endpoint("127.0.0.1", 1), "b": H.Endpoint("127.0.0.1", 2)}
    async def fail(client, provider):
        try:
            await client.evidence(provider, semantic, unit, 4096)
        except OSError as exc:
            ensure(str(exc) == "SYNTHETIC_TRANSPORT_FAILURE", "WRONG_TEST_FAILURE")
        else:
            raise AssertionError("MISSING_TEST_FAILURE")
    with patch.object(H, "exchange", synthetic_failure):
        budget = O.OrdinaryBudget(deadline=deadline, requests=3, reply_bytes=16384)
        budget.charge_external("earlier-search", 1, 128)
        client = O.OrdinaryAcquisition(adapter, endpoints, budget)
        await fail(client, "a"); await fail(client, "b")
        await refuses_async("ORDINARY_AGGREGATE_BUDGET", lambda: client.evidence("a", semantic, unit, 4096))
        ensure(budget.report()["requests"] == 3 and budget.report()["charged_reply_bytes"] == 8320 and
               len(calls) == 2 and budget.deadline == deadline, "REQUEST_LIMIT_OR_PREPAY_RENEWED")

        byte_budget = O.OrdinaryBudget(deadline=deadline, requests=3, reply_bytes=4096)
        byte_client = O.OrdinaryAcquisition(adapter, endpoints, byte_budget)
        await fail(byte_client, "a")
        await refuses_async("ORDINARY_AGGREGATE_BUDGET", lambda: byte_client.evidence("b", semantic, unit, 4096))
        ensure(len(calls) == 3 and byte_budget.report()["requests"] == 1 and
               byte_budget.report()["charged_reply_bytes"] == 4096, "BYTE_LIMIT_RENEWED")

        expiry = O.OrdinaryBudget(deadline=deadline, requests=3, reply_bytes=8192)
        expiring_client = O.OrdinaryAcquisition(adapter, endpoints, expiry)
        with patch.object(O.time, "monotonic", return_value=deadline+1):
            await refuses_async("ORDINARY_BUDGET_CLOSED_OR_EXPIRED",
                                lambda: expiring_client.evidence("b", semantic, unit, 4096))
        ensure(len(calls) == 3 and expiry.report()["requests"] == 0 and expiry.deadline == deadline,
               "EXPIRED_ORIGINAL_DEADLINE_DIALED_OR_RENEWED")
    save(root, "mocked-budget-report.json", F.compact({"requests": client.report(),
        "bytes": byte_client.report(), "deadline": expiring_client.report()}))
    report("shared_prepaid_requests_bytes_and_nonrenewing_deadline")


async def run(root):
    deadline = time.monotonic()+30
    def guard():
        ensure(time.monotonic() < deadline, "CONTROL_PARENT_DEADLINE")
    semantic, raw, alias, group, own, preview = fixtures(root)
    atomic_controls(root, semantic, raw, alias, group, guard)
    await loopback_controls(root, semantic, raw, own, preview, deadline, guard)
    await mutant_controls(root, semantic, raw, own, deadline)
    await aggregate_controls(root, semantic, raw, deadline)
    print("ORDINARY_ACQUISITION_ALL_PASS groups=5 mathematical_acceptance=false external_network=false", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-root", required=True)
    args = parser.parse_args()
    root = ordinary(Path(args.store_root), fresh=True)
    root.mkdir()
    asyncio.run(run(root))


if __name__ == "__main__":
    main()
