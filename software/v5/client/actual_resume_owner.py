"""Fresh finite reuse of actual03's retained seed; never repeat its discovery.

Trusted local launcher strategy, not mathematical authority or a benchmark.
Old reports are pinned historical costs, never live warrants. Two unchanged
consumer/cold grants require fresh actual admission; no receipt is produced.
"""
import asyncio
from copy import deepcopy
import json

from client.actual_assets_atomic import (Assets, BASE, MIB, configuration,
                                        grant_limits, need, read_pin, save)
from client.actual_owner03 import (CALL, FUSION, PROJECTION, RETENTION,
                                   inspect_author, projection_source)
from client.workspace_atomic import Workspace

SEED_MODULE = "b42957064314b6667bf05cd3eec27ce39b925491c756a69f23a739d39ebb9f94"
SEED_PACKET = (554165, "92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f")
SEED_OPERATION = "4898246455cde36d15d11631b263a7a4fe9bb8d6c18d920504e72f038ca8490b"
SEED_PUBLICATION = "1573252331936645f052074a5506189fbbd2162160d93d7617d208d4af8d3a75"
SEED_SNAPSHOT = "2b7c0199b33673fe3909489c01f71d36dc0cfcddd56ec3bc82d36b78294c65a5"
PRIOR = {
    "actual01": ("client-actual-01/RESULT.json", 2253,
        "342303c66d75ac3d7987d7ad72eae74b4640417d498f12a742d3ecf8b8bf448c"),
    "actual02": ("client-actual-02/RESULT.json", 2257,
        "f1f0de3f7043b0bf973f973861f17cde46594d16d194c0f2096583a8af38ecc6"),
    "actual02_inner": ("client-actual-02/work/actual-result.json", 3835,
        "5f9b4045cbf01d7b81ce604a610634331e4a8fe0a1461b13e3b6e84bb359259e"),
    "actual03": ("client-actual-03/RESULT.json", 2263,
        "9692606b3e530d78aa86b18e04512ae3df14912e11139a7a3fe9a0cb623b6267"),
    "actual03_inner": ("client-actual-03/work/actual-result.json", 106892,
        "f06d047dc44354bd1cedc98a86f9104a2b94323ed9cb9c952ba512c1d7184e58"),
}


def retained(context):
    """Read exact historical bytes, without opening any old mutable databases."""
    records, pins, costs = {}, {}, {}
    for name, (relative, size, digest) in PRIOR.items():
        context.remaining_seconds()
        pin = {"path": str(context.workspace_root/relative), "bytes": size, "sha256": digest}
        # Operational reports contain finite floats, unlike canonical mathematics.
        records[name] = json.loads(read_pin(pin, MIB))
        pins[name] = pin
    for name in ("actual01", "actual02", "actual03"):
        outer = records[name]; operation = outer["result"]
        need(outer["status"] == "COMMAND_FAILED" and outer["final_error"] is None
             and operation["job_closed"] and operation["direct_child_reaped"]
             and not operation["cleanup_errors"] and operation["final_job"]["active_processes"] == 0,
             "RESUME_PRIOR_TERMINAL:"+name)
        job = operation["final_job"]["cpu_seconds"]
        wrapper = outer["wrapper_cpu_seconds"]
        costs[name] = {"status": outer["status"], "job_cpu_seconds": job,
            "wrapper_cpu_seconds": wrapper, "known_cpu_seconds": job+wrapper,
            "wall_seconds": outer["wall_seconds"],
            "pre_clock_interpreter_startup": outer["pre_clock_interpreter_startup"]}
    old = records["actual03_inner"]
    need(old["status"] == "FAIL" and old["error"] == "DeltaError:MIXED_CONTROLLER_CPU",
         "RESUME_PRIOR_FAILURE_BINDING")
    seed = old["phases"]["seed"]
    publication = seed["publication"]
    need(publication["publication_id"] == SEED_PUBLICATION
         and publication["snapshot_id"] == SEED_SNAPSHOT
         and publication["phase"] == "LOCALLY_PUBLISHED"
         and publication["intent"]["module"] == SEED_MODULE
         and publication["intent"]["export_names"] == [FUSION]
         and (publication["intent"]["packet_bytes"], publication["intent"]["packet_sha256"]) == SEED_PACKET,
         "RESUME_SEED_PUBLICATION_BINDING")
    closed = seed["closed_client"]
    need(closed["closed"] and closed["status"] == "CLOSED", "RESUME_SEED_CLOSED_RECORD")
    evidence = {"pins": pins, "prior_attempt_costs": costs,
        "known_prior_attempt_cpu_seconds": sum(row["known_cpu_seconds"] for row in costs.values()),
        "prior_error02": records["actual02_inner"]["error"], "prior_error03": old["error"],
        "seed_publication": SEED_PUBLICATION, "seed_snapshot": SEED_SNAPSHOT,
        "seed_close_time_controller_cpu_seconds": closed["observed_controller_cpu_since_grant"],
        "seed_close_time_wall_seconds": closed["wall_since_grant"],
        "cost_scope": "PRIOR_ATTEMPTS_RETAINED_SEPARATELY_NOT_CHARGED_AGAIN;"
                      "SEED_CLOSE_TIME_IS_NESTED_NOT_ADDITIVE;LATE_CLIENTS_SEED_CLOCK_NOT_USED",
        "upstream_receipt_production_cost": "PREEXISTING_RETAINED_EVIDENCE_NOT_INCLUDED_IN_CLIENT_ATTEMPT_TOTAL",
        "authority": "PINNED_HISTORICAL_DATA_NOT_LIVE_MATHEMATICAL_AUTHORITY"}
    path = (context.workspace_root/"client-actual-03"/"work"/"origin"/"operations"/
            SEED_OPERATION/"preparation"/"author-1"/"mixed-packet.json")
    pin = {"path": str(path), "bytes": SEED_PACKET[0], "sha256": SEED_PACKET[1]}
    return read_pin(pin, MIB), pin, evidence


class Strategy:
    def __init__(self, context):
        self.context, self.assets = context, Assets(context)
        self.config = configuration()
        self.consumer_root = context.location_workspace/"consumer"
        self.workspaces, self.clients, self.closed_clients = [], [], {}
        self.report = {"schema": "DMKN_V5_CLIENT_RETAINED_REUSE_RESULT_V1", "status": "FAIL",
            "phases": {}, "cleanup_errors": [], "proof_calls": 0, "guest_calls": 0,
            "seed_author_calls": 0, "discovery_calls": 0,
            "cold_scope": "FRESH_CLIENT_OWNERS_SAME_PYTHON_PROCESS_AND_HOST",
            "consumer_inputs": "EXACT_RETAINED_ACTUAL03_SEED_PACKET_NO_DESERIALIZED_AUTHORITY",
            "comparison_scope": "CHANGED_BOUNDARY_CONTINUATION_NOT_A_MATCHED_SPEEDUP_BENCHMARK",
            "full_v5_release": False, "mathematical_authority": "LIVE_OWNERS_ONLY_NOT_THIS_REPORT"}

    def open(self, create=False):
        self.context.remaining_seconds()
        workspace = Workspace.open(self.consumer_root, self.config, create=create)
        self.workspaces.append(workspace)
        return workspace

    def client(self, workspace, phase):
        grant = workspace.reserve(grant_limits(phase), outer_deadline=self.context.deadline)
        self.report["phases"][phase] = {"grant": grant.identifier}
        client = self.assets.owners(workspace, grant, phase)
        self.clients.append((phase, client))
        return grant, client

    async def close_client(self, phase, client, *, success):
        if phase not in self.closed_clients:
            # Capture exactly once: a second report samples CPU from the original
            # grant again and would wrongly include the later cold phase.
            result = await client.close()
            self.closed_clients[phase] = deepcopy(result)
            self.report["phases"][phase]["closed_client"] = deepcopy(result)
        result = self.closed_clients[phase]
        need(result["closed"] and result["receipt"]["closed"] and result["mixed"]["closed"]
             and (result["preparation"] is None or result["preparation"]["closed"])
             and result["status"] not in ("CLEANUP_INCOMPLETE", "CLOSED_REPORT_UNCERTAIN"),
             "RESUME_CLIENT_CLOSE:"+phase)
        if success: need(result["status"] == "CLOSED", "RESUME_CLIENT_SUCCESS_CLOSE:"+phase)

    async def consumer(self, raw, pin):
        workspace = self.open(True)
        grant, client = self.client(workspace, "consumer")
        # Structural custody is intentionally not mathematical acceptance. The
        # next public client call must issue a fresh real receipt/native warrant.
        stored = workspace.packets.put(SEED_MODULE, raw, before_commit=self.context.remaining_seconds)
        need(stored["mathematical_acceptance"] is False
             and (stored["packet_bytes"], stored["packet_sha256"]) == SEED_PACKET
             and workspace.packets.get(pin["sha256"], pin["bytes"]) == raw,
             "RESUME_STRUCTURAL_CUSTODY")
        phase = self.report["phases"]["consumer"]
        phase.update(seed_packet_pin=pin, structural_custody=stored)
        warrant = client.admit_local(SEED_MODULE, pin["sha256"], pin["bytes"], **CALL)
        description = client.describe(warrant)
        need(description["live"]["module"] == SEED_MODULE, "RESUME_FRESH_SEED_ADMISSION")
        phase["fresh_actual_admission"] = True
        material = client.semantic_material(warrant)
        members = {row["module"]: row["journal"] for row in description["members"]}
        need(set(members) == {BASE, SEED_MODULE} and material["status"] == "AVAILABLE_PACKET_SEMANTICS",
             "RESUME_PACKET_ONLY_IMPORT_MEMBERS")
        phase["material_census"] = material["census"]
        ready = client.import_context([{"warrant": warrant, "resolutions": None}],
            [members[module] for module in sorted(members)], material["openings"], material["bodies"])
        need(ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
             and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0, "RESUME_ATOMIC_CONTEXT")
        phase["context_cost"] = ready["cost"]
        source = projection_source(SEED_MODULE)
        prepared = client.author(ready["context"], source, [PROJECTION], cpu_seconds=60, wall_seconds=120)
        phase["export"] = inspect_author(prepared, source, PROJECTION, SEED_MODULE, FUSION, grant)
        published = client.publish(prepared["child"]["packet"], [PROJECTION], retention_policy=RETENTION)
        need(published["phase"] == "LOCALLY_PUBLISHED" and published["indexed"] == 1,
             "RESUME_SUCCESSOR_PUBLICATION")
        phase.update(publication=published, semantic_origin="FRESHLY_ADMITTED_RETAINED_PACKET_ONLY")
        await self.close_client("consumer", client, success=True)
        workspace.close()
        return published

    async def cold(self, published):
        need(len(self.clients) == len(self.closed_clients) == 1
             and self.closed_clients["consumer"]["closed"], "RESUME_ORIGINAL_OWNERS_MUST_BE_CLOSED")
        workspace = self.open()
        prior = workspace.read_record("publications", published["publication_id"])
        need(prior["intent"] == published["intent"] and prior["outcome"]["phase"] == "LOCALLY_PUBLISHED",
             "RESUME_REOPEN_PUBLICATION_RECORD")
        grant, client = self.client(workspace, "cold")
        intent = prior["intent"]
        warrant = client.admit_local(intent["module"], intent["packet_sha256"], intent["packet_bytes"], **CALL)
        description = client.describe(warrant)
        need(description["live"]["module"] == intent["module"]
             and {row["module"] for row in description["members"]} == {BASE, SEED_MODULE, intent["module"]},
             "RESUME_COLD_CLIENT_ADMISSION")
        self.report["phases"]["cold"].update(module=intent["module"],
            publication_id=published["publication_id"], packet_sha256=intent["packet_sha256"],
            members=[row["module"] for row in description["members"]],
            old_report_granted_authority=False, fresh_actual_admission=True)
        await self.close_client("cold", client, success=True)
        workspace.close()

    async def cleanup(self):
        errors = []
        for phase, client in reversed(self.clients):
            if phase in self.closed_clients: continue
            try: await self.close_client(phase, client, success=False)
            except BaseException as error:
                errors.append(phase+"-close:"+str(error)[:300])
        for workspace in reversed(self.workspaces):
            try: workspace.close()
            except BaseException as error: errors.append("workspace-close:"+str(error)[:300])
        self.report["cleanup_errors"] = errors
        # Reuse close-time snapshots, never re-report a closed prior phase.
        self.report["clients"] = deepcopy(self.closed_clients)
        return not errors and len(self.closed_clients) == len(self.clients)

    async def run(self):
        try:
            raw, pin, history = retained(self.context)
            self.report["retained_evidence"] = history
            published = await self.consumer(raw, pin)
            await self.cold(published)
            reports = list(self.closed_clients.values())
            need(len(reports) == 2 and all(row["receipt"]["attempts"] == 1
                 and row["mixed"]["attempts"] == 1 and row["counts"]["admission_submissions"] == 1
                 for row in reports) and sum(row["counts"]["author_calls"] for row in reports) == 1,
                 "RESUME_EXACT_RECEIPT_AUTHOR_CALLS")
            self.context.remaining_seconds()
            self.report["status"] = "PASS_RETAINED_SEED_ATOMIC_REUSE_PUBLICATION_AND_COLD_CLIENT_READMISSION"
        except BaseException as error:
            self.report["error"] = type(error).__name__+":"+str(error)[:2000]
        finally:
            if not await self.cleanup(): self.report["status"] = "FAIL_CLEANUP"
            save(self.context.location_workspace/"actual-result.json", self.report)
        return 0 if self.report["status"].startswith("PASS_") else 1


def main(context):
    return asyncio.run(Strategy(context).run())
