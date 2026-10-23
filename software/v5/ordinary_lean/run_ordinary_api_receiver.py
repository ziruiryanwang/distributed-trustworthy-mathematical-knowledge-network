"""Selected ordinary B workflow, using real installed admission and HTTP APIs.

The owner-selected publisher manifest contains inert source evidence only. B's
query is structural and fixed before that manifest is read. No publisher ID,
snapshot, artifact, catalog or success report authorizes B mathematics. This
is an integration caller, not a new checker or a public hostile-source runner.
"""
from pathlib import Path
import argparse
import asyncio
import hashlib
import math
import sys
import time

MIB = 1024*1024
CUSTODY = dict(objects=32, exports=64, logical_bytes=8*MIB, db_pages=4096)
INDEX = dict(max_objects=16, max_postings=4096, max_features=4096,
             max_snapshots=32, max_logical_bytes=16*MIB, max_db_pages=8192)
QUERY = [{"tag": "declaration-kind", "value": "theorem"},
         {"tag": "binder-domain-head", "head": {"tag": "forallE"}}]


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("output", "installation", "manifest-sha256", "python-runtime",
                 "lean-runtime", "support-root", "publisher-manifest", "publisher-sha256",
                 "store-id", "helper-paths", "successor-template", "author-worker-script"):
        p.add_argument("--"+name, required=True)
    p.add_argument("--wall-seconds", type=int, default=180)
    p.add_argument("--cpu-seconds", type=int, default=120)
    p.add_argument("--memory-mib", type=int, default=1536)
    return p.parse_args()


async def run(args):
    started, cpu_start = time.monotonic(), time.process_time()
    deadline, charged_workers = started+args.wall_seconds, 0.0
    support, installed = Path(args.support_root), Path(args.installation)
    # Installed modules win and must match the manifest on open. Auxiliary
    # custody/discovery/request helpers are root-selected snapshots, not peers.
    sys.path[:0] = [str(installed/"py"), str(support/"ordinary_lean"), str(support)]
    import ordinary_admission as A
    import ordinary_evidence as E
    import portable_evidence as PE
    import portable_preview as PP
    from discovery import formal_features as F
    from discovery.ordinary_export_adapter import OrdinaryExportAdapter, compile_query
    from discovery.discovery_store import Store
    from discovery.search_session import SearchSession
    from transport.clients import SearchClient
    from transport.http_provider import Provider
    from transport.ordinary_acquisition import OrdinaryStore, OrdinaryAcquisition, OrdinaryBudget
    from ordinary_successor_authoring import author_successor
    A.need(60 <= args.wall_seconds <= 480 and 10 <= args.cpu_seconds <= 300
           and 256 <= args.memory_mib <= 2048, "RECEIVER_SELECTED_LIMITS")
    output = A.C.ordinary(Path(args.output), directory=True)

    def guard():
        A.need(time.monotonic() < deadline and
               time.process_time()-cpu_start+charged_workers < args.cpu_seconds,
               "RECEIVER_PARENT_BUDGET")

    def save(name, value):
        guard()
        A.P.PortableCatalog._write_fresh(output/name, F.compact(value))

    def budget():
        guard()
        wall = math.floor(deadline-time.monotonic())-5
        cpu = math.floor(args.cpu_seconds-(time.process_time()-cpu_start)-charged_workers)-1
        A.need(wall >= 30 and cpu >= 2, "RECEIVER_REMAINING_BUDGET")
        result = A.OperationBudget(wall, cpu, args.memory_mib, output_bytes=16*MIB)
        result.deadline = min(result.deadline, deadline)
        return result

    def account_worker_cpu(seconds):
        nonlocal charged_workers
        A.need(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
               "RECEIVER_WORKER_CPU_CHARGE")
        charged_workers += seconds

    manifest_raw = A.C.read_bounded(A.C.ordinary(installed/"INSTALLATION.json"), 2*MIB)
    installation = A.NativeInstallation.open(installed, manifest_raw, args.manifest_sha256,
        runtime_roots={"python_runtime": Path(args.python_runtime), "lean_runtime": Path(args.lean_runtime)})
    adapter = OrdinaryExportAdapter(installation.semantic_id)
    features = compile_query(adapter.namespace, QUERY)
    # Fixed before any target IDs or publisher index data enter this process.
    save("QUERY.json", {"specs": QUERY, "features": features, "target_id": None, "snapshot_id": None})
    publisher_raw = A.C.read_bounded(A.C.ordinary(Path(args.publisher_manifest)), MIB)
    A.need(hashlib.sha256(publisher_raw).hexdigest() == args.publisher_sha256, "PUBLISHER_SELECTION_PIN")
    # This exact-hash-selected local owner instruction may be readable JSON.
    # Use the bounded duplicate-rejecting writer reader, not the canonical
    # network-record reader. All actual peer responses still use strict codecs.
    publisher = A._writer_json(publisher_raw, MIB)
    F.fields(publisher, ("schema", "semantic_id", "units", "target_name"))
    A.need(publisher["schema"] == "DMKN_ORDINARY_SELECTED_PUBLICATION_V1" and
           publisher["semantic_id"] == installation.semantic_id and
           type(publisher["units"]) is list and 1 <= len(publisher["units"]) <= 8,
           "PUBLISHER_FINITE_INPUT")
    target_key = E.name_key(publisher["target_name"])
    source = received = owner = index = reopened = None
    servers = []
    try:
        source = OrdinaryStore(output/"publisher-custody", installation.semantic_id, CUSTODY, create=True)
        index = Store(output/"publisher-index", adapter, INDEX, create=True)
        target_raw, source_bytes, unit_ids = None, 0, set()
        for row in publisher["units"]:
            guard(); F.fields(row, ("path", "sha256"))
            raw = A.C.read_bounded(A.C.ordinary(Path(row["path"])), 4*MIB)
            source_bytes += len(raw)
            A.need(source_bytes <= 4*MIB and A.sha(raw) == row["sha256"], "PUBLISHER_UNIT_PIN_OR_BYTES")
            evidence = PE.read_evidence(raw)
            A.need(evidence.unit_id not in unit_ids, "PUBLISHER_DUPLICATE_UNIT")
            unit_ids.add(evidence.unit_id)
            source.put_evidence(raw, before_commit=guard)
            if any(E.name_key(r[0]) == target_key for r in evidence.document["unit"][2]):
                A.need(target_raw is None, "PUBLISHER_TARGET_AMBIGUOUS")
                target_raw = raw
        A.need(target_raw is not None, "PUBLISHER_TARGET_ABSENT")
        preview = PP.preview_from_evidence(target_raw, publisher["target_name"])
        source.put_preview(preview, before_commit=guard)
        publication = index.admit(preview); guard()
        save("PUBLICATION.json", publication)
        # B starts with only its own freshly checked foundation.
        received = OrdinaryStore(output/"custody", installation.semantic_id, CUSTODY, create=True)
        owner = A.OrdinaryAdmission.open(installation, output/"catalog", args.store_id, received, create=True)
        initialize_budget = budget()
        basis = owner.initialize(initialize_budget)
        charged_workers += initialize_budget.worker_cpu
        save("BASIS.json", basis)
        receive_budget = budget()  # Created BEFORE search, shared through admission.
        acquisition_budget = OrdinaryBudget(deadline=receive_budget.deadline, requests=24, reply_bytes=8*MIB)
        acquisition_budget.charge_external("formal-search", 2, 8192+131072)
        acquisition_budget.charge_external("successor-formal-search", 2, 8192+131072)
        provider = Provider(index=index, ordinary=source, max_requests=24,
                            max_reply_bytes=8*MIB, operation_ms=10000)
        servers.append(provider)
        endpoint = await provider.start()

        async def discover_and_acquire():
            remaining_ms = max(1, math.floor((receive_budget.deadline-time.monotonic())*1000))
            search = SearchClient(SearchSession(adapter.namespace, features,
                dict(providers=1, snapshots=1, requests=2, pages=1, examined=32,
                     candidates=8, bytes=8192+131072, wall_ms=remaining_ms, inflight=1)), {"a": endpoint})
            A.need(not search.session.summaries and not search.session.attempted_snapshots,
                   "RECEIVER_NO_PRIOR_SNAPSHOT")
            offer = await search.offer("a", 8192, max_expanded_bytes=MIB)
            save("OFFER.json", offer)
            A.need(offer["status"] == "OFFERED", "RECEIVER_NO_OFFER")
            part = next((r for r in offer["partitions"] if r["anchor_count"] > 0), None)
            A.need(part is not None, "RECEIVER_NO_NONEMPTY_PARTITION")
            page = await search.candidates("a", offer["snapshot_id"], part["partition"], 0,
                dict(scanned=32, matches=8, bytes=131072, timeout_ms=1000,
                     record_probes=256, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000))
            save("CANDIDATES.json", page)
            A.need(page["status"] == "VERIFIED_CANDIDATES" and len(page["matches"]) == 1,
                   "RECEIVER_SINGLE_SELECTED_CANDIDATE")
            record = page["matches"][0]  # Only the authenticated returned record chooses IDs.
            client = OrdinaryAcquisition(adapter, {"a": endpoint}, acquisition_budget, local_custody=received)
            selected_preview = await client.preview("a", record)
            loc = record["locator"]
            selected = await client.evidence("a", installation.semantic_id, loc["unit_id"], MIB,
                expected_export_id=record["object_id"], expected_export_name=loc["export_name"])
            PP.resolve(selected_preview["raw"], selected["raw"])
            units = {PE.read_evidence(selected["raw"]).unit_id: selected["raw"]}
            frontier, requested = [], set()
            while True:
                receive_budget.check(); guard()
                A.need(len(units) <= 8 and sum(map(len, units.values())) <= 4*MIB, "RECEIVER_FINITE_CLOSURE")
                plan = owner.preflight(basis["local_root"], list(units.values()), budget=receive_budget)
                frontier.append({"status": plan.status, "missing": [[E.strict_json(n), i] for n, i in plan.missing]})
                if plan.status == "READY":
                    break
                for encoded_name, identity in plan.missing:
                    A.need(identity not in requested and len(requested) < 8, "RECEIVER_NO_PROGRESS_OR_FRONTIER_CAP")
                    requested.add(identity)
                    name = E.strict_json(encoded_name)
                    found = await client.locator("a", installation.semantic_id, identity, 4096, expected_name=name)
                    uid = found["locator"]["unit_id"]
                    if uid not in units:
                        fetched = await client.evidence("a", installation.semantic_id, uid, MIB,
                            expected_export_id=identity, expected_export_name=name)
                        units[uid] = fetched["raw"]
            save("ACQUISITION.json", {"frontier": frontier, "search": search.report(),
                                     "acquisition": client.report(), "unit_ids": sorted(units)})
            return record, selected_preview["raw"], units, plan, client

        async with asyncio.timeout_at(receive_budget.deadline):
            record, selected_preview, units, plan, client = await discover_and_acquire()
        accepted = owner.admit(basis["local_root"], plan, receive_budget)
        charged_workers += receive_budget.worker_cpu
        save("ADMISSION.json", accepted)
        await provider.stop()
        A.need(provider.server is None and not provider.tasks, "PUBLISHER_STILL_LIVE")
        source.close(); source = None
        index.close(); index = None
        # A is offline. B now uses the exact discovered, independently checked
        # method in a new source contribution. No A native artifact is imported.
        discovered_target = {"name": record["locator"]["export_name"],
            "unit_id": record["locator"]["unit_id"], "export_id": record["object_id"]}
        successor = author_successor(owner, accepted["local_root"], discovered_target,
            output_directory=output/"successor", template_path=Path(args.successor_template),
            helper_paths=[Path(p) for p in args.helper_paths.split(";")],
            author_worker_script=Path(args.author_worker_script), parent_deadline=deadline,
            make_budget=budget, account_worker_cpu=account_worker_cpu, check_parent=guard)
        for row in successor["units"]:
            raw = received.get_evidence(installation.semantic_id, row["unit_id"], MIB, check_budget=guard)
            A.need(len(raw) == row["bytes"] and A.sha(raw) == row["sha256"], "SUCCESSOR_DURABLE_BYTES")
            units[row["unit_id"]] = raw
        successor_preview = received.get_preview(successor["preview"]["sha256"],
                                                 successor["preview"]["bytes"], check_budget=guard)
        index = Store(output/"successor-index", adapter, INDEX, create=True)
        save("SUCCESSOR-PUBLICATION.json", index.admit(successor_preview))
        guard()
        owner.close(); owner = None
        received.close(); received = None
        # C starts without the new target ID or snapshot. It obtains the new
        # contribution and its exact nonfoundation closure from cold B custody.
        # This endpoint establishes byte availability, not C kernel acceptance.
        reopened = OrdinaryStore(output/"custody", installation.semantic_id, CUSTODY)
        rehost = Provider(index=index, ordinary=reopened, max_requests=16, max_reply_bytes=8*MIB)
        servers.append(rehost)
        replacement = await rehost.start()
        cold = OrdinaryAcquisition(adapter, {"b": replacement}, acquisition_budget)
        async with asyncio.timeout_at(receive_budget.deadline):
            remaining_ms = max(1, math.floor((receive_budget.deadline-time.monotonic())*1000))
            cold_search = SearchClient(SearchSession(adapter.namespace, features,
                dict(providers=1, snapshots=1, requests=2, pages=1, examined=32,
                     candidates=8, bytes=8192+131072, wall_ms=remaining_ms, inflight=1)), {"b": replacement})
            offered = await cold_search.offer("b", 8192, max_expanded_bytes=MIB)
            A.need(offered["status"] == "OFFERED", "COLD_SUCCESSOR_NO_OFFER")
            part = next((r for r in offered["partitions"] if r["anchor_count"] > 0), None)
            A.need(part is not None, "COLD_SUCCESSOR_NO_PARTITION")
            page = await cold_search.candidates("b", offered["snapshot_id"], part["partition"], 0,
                dict(scanned=32, matches=8, bytes=131072, timeout_ms=1000,
                     record_probes=256, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000))
            A.need(page["status"] == "VERIFIED_CANDIDATES" and len(page["matches"]) == 1,
                   "COLD_SUCCESSOR_CANDIDATE")
            cold_record = page["matches"][0]
            cold_preview = await cold.preview("b", cold_record)
            loc = cold_record["locator"]
            first = await cold.evidence("b", installation.semantic_id, loc["unit_id"], MIB,
                expected_export_id=cold_record["object_id"], expected_export_name=loc["export_name"])
            PP.resolve(cold_preview["raw"], first["raw"])
            fetched = {loc["unit_id"]: first["raw"]}
            inventory = A._writer_json(installation.read("inventory", MIB), MIB)
            base = {E.name_key(row[0]): A.S.basis_symbol_id(installation.semantic_id,
                     A.S.foundation_id(), row[0]) for row in inventory}
            requested = set()
            while True:
                guard(); acquisition_budget.active()
                A.need(len(fetched) <= 8 and sum(map(len, fetched.values())) <= 4*MIB,
                       "COLD_FINITE_CLOSURE")
                parsed = [PE.read_evidence(raw) for raw in fetched.values()]
                known = dict(base)
                for item in parsed:
                    for row in item.document["unit"][2]:
                        key = E.name_key(row[0])
                        identity = A.S.export_id(installation.semantic_id, item.unit_id, row[0])
                        A.need(key not in known or known[key] == identity, "COLD_NAME_CONFLICT")
                        known[key] = identity
                missing = {}
                for item in parsed:
                    for name, identity in item.document["imports"]:
                        key = E.name_key(name)
                        if key in known:
                            A.need(known[key] == identity, "COLD_IMPORT_CONFLICT")
                        else:
                            A.need(key not in missing or missing[key][1] == identity, "COLD_MISSING_CONFLICT")
                            missing[key] = (name, identity)
                if not missing:
                    break
                for name, identity in missing.values():
                    A.need(identity not in requested and len(requested) < 8, "COLD_NO_PROGRESS_OR_CAP")
                    requested.add(identity)
                    found = await cold.locator("b", installation.semantic_id, identity, 4096, expected_name=name)
                    uid = found["locator"]["unit_id"]
                    if uid not in fetched:
                        response = await cold.evidence("b", installation.semantic_id, uid, MIB,
                            expected_export_id=identity, expected_export_name=name)
                        fetched[uid] = response["raw"]
            # These expected-output assertions happen only after discovery and
            # closure acquisition; they do not choose any C fetch identifier.
            A.need(cold_preview["raw"] == successor_preview and fetched == units,
                   "COLD_SUCCESSOR_COMPLETE_BYTE_CORRESPONDENCE")
            save("COLD-SUCCESSOR.json", {"offer": offered, "page": page,
                "search": cold_search.report(), "unit_ids": sorted(fetched),
                "mathematical_acceptance": False})
        result = {"status": "PASS_INSTALLED_RECIPROCAL_CONTRIBUTION_AND_COLD_SUCCESSOR_DISCOVERY",
            "semantic_id": installation.semantic_id, "implementation_id": installation.implementation_id,
            "store_id": args.store_id, "received_root": accepted["local_root"],
            "local_root": successor["local_root"], "successor": successor,
            "discovered_export_id": record["object_id"], "discovered_export_name": record["locator"]["export_name"],
            "custody_directory": str(output/"custody"), "catalog_directory": str(output/"catalog"),
            "custody_limits": CUSTODY, "units_checked": accepted["units_checked"],
            "original_provider_stopped": True, "rehost": cold.report(),
            "provider": provider.status(), "replacement_provider": rehost.status(),
            "known_native_cpu_seconds": charged_workers,
            "controller_cpu_seconds": time.process_time()-cpu_start,
            "wall_seconds": time.monotonic()-started,
            "claim": "LOCAL_RECIPROCAL_WORKFLOW_AND_COLD_AVAILABILITY_NOT_C_ACCEPTANCE_GROWTH_OR_GLOBAL_RELEASE"}
        save("RECEIVER-RESULT.json", result)
        print(F.compact(result).decode("utf-8"), flush=True)
    finally:
        for server in reversed(servers):
            await server.stop()
        for item in (owner, reopened, received, index, source):
            if item is not None:
                item.close()


if __name__ == "__main__":
    asyncio.run(run(arguments()))
