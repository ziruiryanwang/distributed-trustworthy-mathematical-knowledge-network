"""One matched source-known M build/sharing observation; not a peer API.

Run only through the selected enclosing Job. Serial child Jobs account for each
arm's descendants. No proof production, retries, V/W work or optimality claim.
"""
import argparse
import asyncio
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import time
from types import SimpleNamespace

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = Path(__file__).resolve().parents[1]
MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
METHOD = "bbf0845d2622374699a93a9d8ccc6e565dd1c985e72441ec0eeae41bb03fc0c5"
NAME = [["s", "OwnerV5"], ["s", "evaluator_unique"]]
MAP = (2805479, "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0")
PACKET = (498641, "efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b")
REPLACEMENTS = {
    "v5/admission/pin_phase.py": ("standalone_validation/admission/pin_phase.py",
        "ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881"),
    "v5/mixed_claims/imports_atomic.py": ("continuing_context/mixed_claims/imports_atomic.py",
        "45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad"),
    "v5/mixed_claims/receiver.py": ("incremental_native/mixed_claims/receiver.py",
        "5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b"),
    "v5/client/workspace_atomic.py": ("continuing_context/client/workspace_atomic.py",
        "32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773"),
}
SEARCH = dict(providers=1, snapshots=1, requests=3, pages=2, examined=8,
              candidates=4, bytes=384*1024, inflight=1, wall_ms=90000)
ADMISSION = dict(native_cpu_seconds=10, receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)
AUTHOR = dict(cpu_seconds=45, wall_seconds=90, memory_mib=768)
JOB = dict(cpu_seconds=120, wall_seconds=240, memory_mib=1024,
           active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB)
OPERATION = dict(wall_seconds=180, controller_cpu_seconds=90, calls=96,
    input_bytes=32*MIB, worker_cpu_seconds=75, output_bytes=128*MIB, output_entries=1024,
    acquisition=dict(requests=16, reply_bytes=4*MIB, verify_attempts=2,
        verification_input_bytes=16*MIB, worker_cpu_seconds=30),
    imports=dict(max_sources=2, max_members=8, max_receipts=1, max_calls=8192,
                 submitted_bytes=32*MIB, data_bytes=8*MIB))


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(value, directory=False):
    path = Path(value)
    need(path.is_absolute() and path.is_relative_to(PROJECT) and ".." not in path.parts,
         "CANONICAL_PATH")
    for part in (*reversed(path.parents), path):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not
             getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
    need(path.is_dir() if directory else path.is_file(), "ORDINARY_PATH_KIND")
    return path


def read(path, limit=2*MIB):
    path = ordinary(path)
    need(0 < path.stat().st_size <= limit, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(limit+1)
    need(0 < len(raw) <= limit, "READ_BOUND")
    return raw


def pinned(row, limit=128*MIB):
    need(type(row) is dict and set(row) == {"path", "bytes", "sha256"}, "PIN_SHAPE")
    raw = read(row["path"], limit)
    need((len(raw), sha(raw)) == (row["bytes"], row["sha256"]), "PIN_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n"
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())


def load_source(name, path, expected=None):
    raw = read(path)
    if expected is not None:
        need(sha(raw) == expected, "HELPER_PIN")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def stage(output, row):
    need((row["bytes"], row["sha256"]) == MAP, "CURRENT_SDK_BASIS")
    basis = json.loads(pinned(row, 3*MIB))["sdk_sources"]
    need(len(basis) == 114 and set(REPLACEMENTS) <= set(basis), "SDK_CENSUS")
    code = output/"selected-code"; code.mkdir()
    selected = {}
    for logical, old in sorted(basis.items()):
        relative = PurePosixPath(logical)
        need(not relative.is_absolute() and relative.as_posix() == logical and
             all(part not in ("", ".", "..") and "\\" not in part for part in relative.parts),
             "LOGICAL_SOURCE_PATH")
        if logical in REPLACEMENTS:
            physical, expected = REPLACEMENTS[logical]
            raw = read(SOURCE/physical)
        else:
            physical = Path(old["path"]).relative_to(PROJECT/"software/v5")
            expected = old["sha256"]; raw = read(SOURCE/physical)
            need(len(raw) == old["bytes"], "SOURCE_SIZE")
        need(sha(raw) == expected, "SOURCE_PIN:"+logical)
        target = code.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            need(stream.write(raw) == len(raw), "STAGE_WRITE")
        need(read(target) == raw, "STAGE_READBACK")
        selected[logical] = dict(path=str(target), bytes=len(raw), sha256=expected)
    save(output/"sources.json", selected)
    return selected


def initial_selection(C, permitted_hashes, bundle):
    need(bundle["module"] == C.module_id(bundle["spec"]) == BASE, "EXACT_I_BASIS")
    openings = [dict(module=BASE, opening=C.group_opening(bundle["spec"], i)) for i in (0, 10)]
    need(all(row["opening"] == bundle["openings"][row["opening"]["index"]]
             for row in openings), "I_OPENINGS")
    bodies = []
    for row in openings:
        for declaration in row["opening"]["group"]["declarations"]:
            if declaration["kind"] != "recursor":
                continue
            for digest in sorted(permitted_hashes(declaration)):
                values = [value for value in bundle["bodies"] if value["digest"] == digest
                          and value["universes"] == declaration["universes"]]
                need(len(values) == 1 and C.body_id(values[0]["expression"], values[0]["universes"])
                     == digest, "I_RULE_BODY")
                bodies.append(dict(module=BASE, universes=values[0]["universes"],
                                   expression=values[0]["expression"]))
    need(len(bodies) == 2, "EXACT_TWO_RULE_BODIES")
    return C.summarize(bundle["spec"]), openings, bodies


def ready_check(result):
    need(result["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY" and result["context"] is not None
         and not result["demands"] and result["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
         "GENUINE_READY_CONTEXT")


def mathematical_endpoint(client, ready, C):
    # Read-only inspection through the actual session's checked/charged view API.
    # Never installs saved data or creates an acceptance capability.
    ready_check(ready)
    items, unused_binding = client._session.view_selection(client._selection_view)
    projection = dict(foundation=client.workspace.config["wire_profile"]["foundation"],
        policy=client.workspace.config["wire_profile"]["policy"], definition_mode="eager",
        selected=[{key: (list(item[key]) if key == "journal" else item[key])
                   for key in ("module", "journal", "summary", "openings", "bodies")} for item in items])
    need([item["module"] for item in items] == sorted((BASE, METHOD)), "EXACT_ENDPOINT_MODULES")
    need({(item["module"], opening["index"]) for item in items for opening in item["openings"]}
         == {(BASE, 0), (BASE, 10), (METHOD, 0)}, "EXACT_ENDPOINT_GROUPS")
    need(sum(len(item["bodies"]) for item in items) == 2, "EXACT_ENDPOINT_BODIES")
    return dict(projection=projection, sha256=sha(C.canonical(projection)),
                status=ready["status"], demands=ready["demands"], cost=ready["cost"])


async def query_acquire(client, endpoint, queries, detail):
    from client import direct_contacts
    from location.protocol import OwnerEgressPolicy
    policy = OwnerEgressPolicy(dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
        public_ports=[], test_endpoints=[dict(host=endpoint.host, port=endpoint.port)]))
    envelope = deepcopy(SEARCH)
    for key in ("providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes"):
        envelope[key] *= len(queries)
    envelope["generations"] = len(queries)
    detail["reservation"] = direct_contacts.reserve_queries(client, envelope, policy)
    contact = {key: getattr(endpoint, key) for key in ("host", "port", "tls", "server_name")}
    detail["queries"] = []
    for query in queries:
        row = dict(query=query, pages=[]); detail["queries"].append(row)
        row["binding"] = direct_contacts.next_query(client, {"selected": contact}, query["specs"],
            deepcopy(SEARCH), contact_lifetime_ms=90000)
        offer = await client.search_offer("selected", max_bytes=131072,
            max_expanded_bytes=262144, max_age_ms=60000, attempt_timeout_ms=5000)
        row["offer"] = offer
        need(offer["status"] == "OFFERED", "SEARCH_OFFER_REFUSED")
        partitions = [part for part in offer["partitions"] if part["anchor_count"] > 0]
        need(len(partitions) <= 2, "FINITE_PARTITIONS")
        for part in partitions:
            page = await client.search_page("selected", offer["snapshot_id"], part["partition"], 0,
                dict(examined=4, matches=2, bytes=131072, timeout_ms=1000, node_reads=50000),
                candidates_only=False, attempt_timeout_ms=5000)
            row["pages"].append(page)
            need(page["status"] == "VERIFIED_PAGE", "AUTHENTICATED_PAGE")
            if not page["matches"]:
                continue
            need(len(page["matches"]) == 1, "SINGLE_CONTRACT_CANDIDATE")
            candidate = await client.resolve("selected", page["matches"][0])
            description = client.describe_candidate(candidate)
            d = description["descriptor"]
            need(d["kind"] == "theorem" and d["universes"] == query["universes"]
                 and d["type"] == query["type"], "RETURNED_EXACT_CONTRACT")
            offered = await client.packet_offers(candidate, max_offers=1, max_bytes=4096)
            need(len(offered["packets"]) == 1, "ONE_OFFERED_PACKET")
            entry = {key: offered["packets"][0][key] for key in ("packet_sha256", "packet_bytes")}
            detail.update(description=description, offered=offered)
            need(not client.delta._cache and not client.delta._native_memo, "FIRST_M_EMPTY_PRIVATE_MEMO")
            return await client.acquire(candidate, entry, **ADMISSION)
    raise ValueError("NO_MATCH_WITHIN_ORIGINAL_ENVELOPE")


def tree_census(root):
    """Finite retained evidence/storage snapshot, not unbounded project traversal."""
    rows, total, entries = [], 0, 0
    for path in root.rglob("*"):
        entries += 1
        need(entries <= 4096 and not path.is_symlink() and not path.is_junction(), "OUTPUT_CENSUS_BOUND")
        if path.is_file():
            size = path.stat().st_size; total += size
            need(total <= 256*MIB, "OUTPUT_BYTE_BOUND")
            rows.append(dict(path=path.relative_to(root).as_posix(), bytes=size))
    return dict(files=rows, bytes=total, file_count=len(rows))


async def arm(args, request):
    code = ordinary(args.code, directory=True)
    source_rows = json.loads(read(code.parent/"sources.json"))
    need(len(source_rows) == 114, "SELECTED_SOURCE_COUNT")
    for logical, row in source_rows.items():
        need(Path(row["path"]) == code.joinpath(*PurePosixPath(logical).parts), "SOURCE_ROOT_BINDING")
        pinned(row)
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    from admission.trust import TrustDomain
    from client.runtime import RuntimeProfile
    from client.workspace_validated import Workspace
    from client.serve_workspace import _close_workspace
    from custody.module_store import permitted_hashes
    from evidence_network.transport import CompositeProvider
    from modules import codec as C
    query_helper = load_source("_sharing_method_query", SOURCE/"examples/mirror_method/method_query.py",
        "0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642")
    output = ordinary(args.output, directory=True)
    plan = json.loads(pinned(request["basis_plan"]))
    p = plan["parameters"]
    context = SimpleNamespace(installation=Path(plan["installation_root"]), sources_v5=code/"v5",
        sources_portable=code/"portable", source_sha256={key: row["sha256"] for key, row in source_rows.items()},
        deadline=args.deadline)
    def remaining():
        value = math.floor(context.deadline-time.monotonic())
        need(value >= 1, "ORIGINAL_ARM_DEADLINE")
        return value
    context.remaining_seconds = remaining
    report = dict(schema="DMKN_SHARING_MARGIN_ARM_V1", arm=args.arm, status="FAIL", errors=[],
        cleanup_errors=[], source_recipe_known=True, new_crypto_production=False,
        initial_live_warrants_restored=False, provider=None)
    workspace = client = domain = provider = provider_workspace = None
    begun = time.monotonic()
    try:
        foundation = pinned(p["foundation"])
        bundle = C.parse_json(pinned(request["bundle"]))
        recipe = pinned(request["recipe"]).decode("utf-8")
        summary, openings, bodies = initial_selection(C, permitted_hashes, bundle)
        # Answer-independent query constructed before provider packet is read.
        queries = query_helper.method_queries(C, BASE)
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        domain = TrustDomain.create(output/"trust", sha(str(output).encode()), support)
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        config = deepcopy(p["workspace_config"])
        config["packet_envelope"].update(deltas=1, edges=1)
        workspace = Workspace.open(output/"recipient", config, create=True)
        grant = workspace.reserve(deepcopy(OPERATION), outer_deadline=context.deadline-10)
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=args.arm == "L",
            foundation_bytes=foundation, foundation_sha256=p["foundation"]["sha256"])
        report["initial"] = client.report()
        need(not client.delta._cache and not client.delta._native_memo, "COLD_M_RECEIVER")
        if args.arm == "L":
            initial = client.admit_receipt(pinned(request["receipt"]), summary,
                cpu_seconds=10, wall_seconds=60, memory_mib=512)
            fact = client.describe(initial)
            need(fact["kind"] == "I" and fact["live"]["module"] == BASE, "GENUINE_I")
            ready = client.import_context([dict(warrant=initial, resolutions=None)],
                [bytes(fact["live"]["journal"])], openings, bodies, definition_mode="eager")
            ready_check(ready)
            old_context = ready["context"]
            before = dict(session=id(client._session), deadline=client._session._deadline,
                          caps=client._session._caps, calls=client._session._calls)
            prepared = client.author(old_context, recipe, [NAME], **AUTHOR)
            need(prepared["status"] == "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED", "SOURCE_PREPARED")
            raw = prepared["child"]["packet"]
            need((len(raw), sha(raw)) == PACKET and prepared["child"]["local_module"] == METHOD,
                 "EXACT_SOURCE_BUILT_METHOD")
            workspace.packets.put(METHOD, raw, before_commit=grant.remaining_seconds)
            need(not client.delta._cache and not client.delta._native_memo, "FIRST_M_EMPTY_PRIVATE_MEMO")
            warrant = client.admit_local(METHOD, PACKET[1], PACKET[0], **ADMISSION)
        else:
            publication_started = time.monotonic()
            provider_workspace = Workspace.open(output/"provider", config, create=True)
            raw = pinned(request["packet"])
            need((len(raw), sha(raw)) == PACKET, "EXACT_PROVIDER_PACKET")
            spec = C.parse_json(raw)["deltas"][0]["local_spec"]
            need(C.module_id(spec) == METHOD and len(spec["groups"]) == 1, "SINGLE_PROVIDER_METHOD")
            opening = C.group_opening(spec, 0)
            provider_workspace.modules.put_group(METHOD, opening)
            provider_workspace.packets.put(METHOD, raw)
            provider_workspace.index.admit(provider_workspace.adapter.encode_opening(METHOD, NAME, opening),
                expected_id=C.export_id(METHOD, NAME))
            report["publication"] = dict(groups=1, bodies=0, indexed=1, packet_bytes=len(raw),
                inherited_I_semantics_not_published=True, provider_mathematical_acceptance=False)
            provider = CompositeProvider(index=provider_workspace.index, custody=provider_workspace.modules,
                packets=provider_workspace.packets, max_connections=2, max_requests=16,
                max_reply_bytes=32*MIB, operation_ms=5000)
            async with asyncio.timeout_at(min(context.deadline-15, grant.deadline-5)):
                endpoint = await provider.start(host="127.0.0.1", port=0)
                report["discovery"] = {}
                warrant = await query_acquire(client, endpoint, queries, report["discovery"])
                await provider.stop()
            report["provider"] = provider.status()
            need(provider.server is None and not provider.tasks, "PROVIDER_CLOSED")
            report["publication"]["service_horizon_seconds"] = time.monotonic()-publication_started
            report["publication"]["selected_payload_bytes"] = len(raw)+len(C.canonical(opening))
            report["publication"]["selected_payload_byte_seconds_upper_bound"] = (
                report["publication"]["selected_payload_bytes"]
                * report["publication"]["service_horizon_seconds"])
            report["publication"]["storage_scope"] = (
                "SELECTED_PACKET_AND_GROUP_DURING_FINITE_SERVICE_ONLY; INDEX_DB_AND_POSTRUN_EVIDENCE_EXCLUDED")
        fact = client.describe(warrant)
        need(fact["kind"] == "mixed" and fact["live"]["module"] == METHOD
             and fact["live"]["packet_sha256"] == PACKET[1], "GENUINE_EXACT_M")
        raw = workspace.packets.get(PACKET[1], PACKET[0])
        need((len(raw), sha(raw)) == PACKET, "DURABLE_M_PACKET")
        material = client.semantic_material(warrant)
        chosen = [row for row in material["openings"] if row["module"] == METHOD]
        need(len(chosen) == 1 and chosen[0]["opening"]["index"] == 0, "ACTUAL_M_OPENING")
        client.retain_semantics(openings+chosen, [])
        held, descriptor = workspace.modules.get_group(METHOD, NAME)
        need(held == chosen[0]["opening"] and descriptor["kind"] == "theorem", "DURABLE_M_GROUP")
        journals = {item["module"]: bytes(item["journal"]) for item in fact["members"]}
        need(set(journals) == {BASE, METHOD}, "EXACT_M_MEMBERS")
        if args.arm == "L":
            ready = client.advance_context(old_context, warrants=[dict(warrant=warrant, resolutions=None)],
                selected=[journals[METHOD]], openings=chosen, bodies=[])
            need(id(client._session) == before["session"] and client._session._deadline == before["deadline"]
                 and client._session._caps == before["caps"] and client._session._calls > before["calls"]
                 and ready["context"] is not old_context, "SAME_FINITE_SESSION_ADVANCED")
        else:
            ready = client.import_context([dict(warrant=warrant, resolutions=None)],
                [journals[BASE], journals[METHOD]], openings+chosen, bodies, definition_mode="eager")
        report["endpoint"] = mathematical_endpoint(client, ready, C)
        report["before_close"] = client.report()
        counts = report["before_close"]["counts"]
        need(counts["new_import_sessions"] == 1 and counts["author_calls"] == int(args.arm == "L")
             and counts["admission_submissions"] == (2 if args.arm == "L" else 1), "EXACT_ARM_CALLS")
        report.update(status="PASS", endpoint_reached=time.monotonic())
    except BaseException as error:
        report["errors"].append(type(error).__name__+": "+str(error)[:2000])
    finally:
        if provider is not None:
            try:
                await provider.stop(); report["provider"] = provider.status()
                need(provider.server is None and not provider.tasks, "PROVIDER_FINAL_CLOSED")
            except BaseException as error:
                report["cleanup_errors"].append("provider:"+str(error)[:1000])
        if client is not None:
            try:
                report["client"] = await client.close()
                need(report["client"]["closed"], "CLIENT_CLOSED")
            except BaseException as error:
                report["cleanup_errors"].append("client:"+str(error)[:1000])
        for label, held in (("recipient", workspace), ("provider", provider_workspace)):
            if held is not None:
                report[label+"_closed"] = _close_workspace(held, report["cleanup_errors"])
        if domain is not None:
            try:
                domain.withdraw("Finite matched sharing arm complete; no future authority.")
                report["domain_withdrawn"] = (output/"trust/WITHDRAWN").is_file()
            except BaseException as error:
                report["cleanup_errors"].append("trust:"+str(error)[:1000])
        if (report["cleanup_errors"] or not report.get("recipient_closed") or not report.get("domain_withdrawn")
                or (provider_workspace is not None and not report.get("provider_closed"))):
            report["status"] = "FAIL"
        report["complete_wall_inside_child"] = time.monotonic()-begun
        report["retained_disk"] = tree_census(output)
        report["retention_horizon"] = "PROCESS_OBSERVATION_ONLY; SAVED_EVIDENCE_POSTRUN_STORAGE_UNPRICED"
        report["total_storage_byte_time"] = "NOT_FULLY_MEASURED; NO_PARETO_OR_ALL_RESOURCE_BENEFIT_CLAIM"
        if time.monotonic() >= context.deadline:
            report["status"] = "FAIL"; report["errors"].append("ORIGINAL_ARM_DEADLINE")
        save(output/"arm-result.json", report)
    return 0 if report["status"] == "PASS" else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True); parser.add_argument("--output", required=True)
    parser.add_argument("--arm", choices=("L", "S")); parser.add_argument("--code")
    parser.add_argument("--deadline", type=float)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == PROJECT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_INVOCATION")
    request = json.loads(read(args.input))
    need(type(request) is dict and set(request) == {"schema", "map", "basis_plan", "manifest",
         "recipe", "receipt", "bundle", "packet"}
         and request["schema"] == "DMKN_SHARING_MARGIN_INPUT_V1", "INPUT_SCHEMA")
    if args.arm:
        need(args.code and args.deadline is not None, "ARM_BINDING")
        return asyncio.run(arm(args, request))
    started = time.monotonic(); deadline = started+550
    output = ordinary(args.output, directory=True)
    stage(output, request["map"])
    plan = json.loads(pinned(request["basis_plan"]))
    base = ordinary(plan["installation_root"], directory=True)
    manifest = json.loads(pinned(request["manifest"], 2*MIB))
    need(Path(request["manifest"]["path"]) == base/"RELEASE-MANIFEST.json", "SUPERVISOR_ROOT")
    helpers = {}
    for name, relative in (("supervisor", "operator/commons.py"),
                           ("domains", "receiver/helpers/domains.py"),
                           ("job", "receiver/helpers/run_stage.py")):
        helpers[name] = load_source("domains" if name == "domains" else "_sharing_"+name,
            base/relative, manifest["files"][relative]["sha256"])
    result = dict(schema="DMKN_SHARING_MARGIN_RESULT_V1", status="FAIL", arms=[],
        order=["L", "S"], one_pair_not_population_bound=True, full_v5_release=False,
        claim_scope="SOURCE_KNOWN_CHECKED_BUILD_REUSE_NOT_MATHEMATICAL_DISCOVERY",
        errors=[], common_producer_creation_present_in_both_histories=True)
    try:
        for label in ("L", "S"):
            now = time.monotonic()
            need(deadline-now >= JOB["wall_seconds"]+10, "SHARED_ORIGINAL_DEADLINE_REMAINDER")
            arm_output = output/label; arm_output.mkdir()
            argv = [sys.executable, "-I", "-S", "-B", str(Path(__file__).resolve()),
                "--input", args.input, "--output", str(arm_output), "--arm", label,
                "--code", str(output/"selected-code"), "--deadline", str(min(deadline-10, now+230))]
            run = helpers["supervisor"].supervise(argv, PROJECT, output/(label+"-command"),
                deepcopy(JOB), helpers["job"].Job, started=now)
            save(output/(label+"-job.json"), run)
            observation = dict(arm=label, job=run)
            result["arms"].append(observation)
            if (arm_output/"arm-result.json").is_file():
                observation["result"] = json.loads(read(arm_output/"arm-result.json", 8*MIB))
            need(run["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and run["job_closed"]
                 and run["final_job"]["active_processes"] == 0, "ARM_JOB_FAILED:"+label)
            need(observation["result"]["status"] == "PASS", "ARM_ENDPOINT_FAILED:"+label)
            observation["known_cpu_seconds"] = (run["final_job"]["cpu_seconds"]
                + run["wrapper_supervision_cpu_seconds"])
        local, shared = result["arms"]
        need(local["result"]["endpoint"]["projection"] == shared["result"]["endpoint"]["projection"],
             "MATCHED_CANONICAL_MATHEMATICS")
        result.update(status="PASS_MATCHED_OBSERVATION_NOT_AUTOMATIC_BENEFIT",
            cpu_difference_L_minus_S=local["known_cpu_seconds"]-shared["known_cpu_seconds"],
            endpoint_sha256=local["result"]["endpoint"]["sha256"],
            common_setup_scope="SDK_STAGE_AND_HARNESS_SETUP_SHARED; NOT_AN_ARM_SPEEDUP",
            accounting="ARM_DESCENDANT_JOB_PLUS_ITS_SEPARATE_SUPERVISOR; NEVER_ADD_TO_OUTER_INCLUSIVE_JOB",
            scalar_benefit_claim=False, n_greater_than_one_claim=False)
    except BaseException as error:
        result["errors"].append(type(error).__name__+": "+str(error)[:2000])
    result["driver_wall_seconds"] = time.monotonic()-started
    save(output/"comparison-result.json", result)
    print(json.dumps({key: result[key] for key in ("status", "errors")}), flush=True)
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
