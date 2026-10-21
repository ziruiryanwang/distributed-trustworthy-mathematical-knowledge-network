"""Finite trusted-owner method circulation through the installed ordinary SDK.

Two independently funded, sequential local agents; one new contribution each.
No new checker, proof production, location layer or transferable report authority.
The retained packet is provider fixture data, never a first-receiver query input.
"""
import asyncio
from copy import deepcopy
import hashlib
from importlib import import_module
from pathlib import Path
import re
import sys
import time
from types import SimpleNamespace

from admission.trust import TrustDomain
from client import direct_contacts, remote_reader
from client.runtime import RuntimeProfile, read_pin
from client.semantic_reader import SemanticReader, READY
from client.serve_workspace import _close_workspace
from client.workspace_mixed import CommonsClient as MixedClient
from client.workspace_validated import Workspace
from custody.module_store import BODY_SCHEMA, permitted_hashes
from discovery import formal_features as F
from discovery.discovery_store import ordinary
from evidence_network.transport import CompositeProvider
from location.protocol import OwnerEgressPolicy
from modules import codec as C

MIB = 1024**2
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
MIRROR = [["s", "OwnerV5"], ["s", "mirror"]]
INVOLUTION = [["s", "OwnerV5"], ["s", "mirror_involution"]]
INJECTIVE = [["s", "OwnerV5"], ["s", "mirror_injective"]]
SEARCH = dict(providers=1, snapshots=1, requests=3, pages=2, examined=8,
              candidates=4, bytes=384*1024, inflight=1, wall_ms=90000)
HTTP = dict(max_connections=2, max_requests=128, max_reply_bytes=64*MIB, operation_ms=5000)
HELPER = dict(modules=8, names=64, groups=64, bodies=64, steps=256, data_bytes=8*MIB)
AUTHOR = dict(cpu_seconds=45, wall_seconds=90, memory_mib=768)
ADMISSION = dict(native_cpu_seconds=10, receipt_cpu_seconds=10, wall_seconds=60, memory_mib=512)


def _operation_limits(phase):
    return dict(wall_seconds=210, controller_cpu_seconds=120,
        calls=192 if phase == "first" else 256, input_bytes=64*MIB,
        worker_cpu_seconds=95 if phase == "first" else 115,
        output_bytes=128*MIB, output_entries=1024,
        acquisition=dict(requests=128, reply_bytes=32*MIB, verify_attempts=2,
            verification_input_bytes=64*MIB,
            worker_cpu_seconds=50 if phase == "first" else 70),
        imports=dict(max_sources=1, max_members=8, max_receipts=1, max_calls=8192,
                     submitted_bytes=32*MIB, data_bytes=8*MIB))


def _app(function, *arguments):
    for argument in arguments:
        function = ["app", function, argument]
    return function


def _tree(a):
    return _app(["const", ["external", BASE, [["s", "CommonsV5"], ["s", "Tree"]]],
                 [["param", 0]]], a)


def _eq(a, left, right):
    return _app(["const", ["foundation", [["s", "Eq"]]], [["succ", ["param", 0]]]],
                a, left, right)


def _mirror_types():
    """Expected V descriptors before relocation: mirror references are local."""
    a, t = ["bvar", 1], ["bvar", 0]
    mirror = ["const", ["local", MIRROR], [["param", 0]]]
    result = _eq(_tree(a), _app(mirror, a, _app(mirror, a, t)), t)
    prefix = lambda body: ["forall", "implicit", ["sort", ["succ", ["param", 0]]],
                          ["forall", "default", _tree(["bvar", 0]), body]]
    return prefix(_tree(a)), prefix(result)


def _injective_type(module):
    mirror = ["const", ["external", module, MIRROR], [["param", 0]]]
    a, x, y = ["bvar", 2], ["bvar", 1], ["bvar", 0]
    hypothesis = _eq(_tree(a), _app(mirror, a, x), _app(mirror, a, y))
    conclusion = _eq(_tree(["bvar", 3]), ["bvar", 2], ["bvar", 1])
    return ["forall", "implicit", ["sort", ["succ", ["param", 0]]],
            ["forall", "default", _tree(["bvar", 0]),
             ["forall", "default", _tree(["bvar", 1]),
              ["forall", "default", hypothesis, conclusion]]]]


def _known_query(module):
    unused, expression = _mirror_types()
    C.validate_expr(expression, 1)
    key = C.hash_value("discovery-declared-type",
                      dict(universes=1, type=C.relocate_expr(expression, module, 1)))
    return [dict(universes=1, type=expression, expected_module=module,
        expected_name=INVOLUTION, specs=[dict(tag="declaration-kind", value="theorem"),
                                       dict(tag="declared-type-key", value=key)],
        mathematical_acceptance=False, global_complete=False)]


def _reference(module, name):
    """Support only ordinary string components, quoting every Lean component."""
    C.digest_string(module); C.validate_name(name)
    F.need(name and all(part[0] == "s" and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part[1])
                       for part in name), "MIRROR_UNSUPPORTED_METHOD_NAME")
    return ".".join("«"+part[1]+"»" for part in C.relocated_name(module, name))


def _write(path, raw):
    F.need(type(raw) is bytes and 0 < len(raw) <= 16*MIB, "MIRROR_EVIDENCE_BYTES")
    path = ordinary(path, fresh=True, directory=False)
    with path.open("xb") as stream:
        F.need(stream.write(raw) == len(raw), "MIRROR_EVIDENCE_SHORT_WRITE")
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def _owner_helpers(context):
    original = list(sys.path)
    try:
        sys.path.insert(0, str(context.sources_owner))
        result = []
        for name in ("contribution", "method_query"):
            path = ordinary(context.sources_owner/(name+".py"), directory=False)
            wanted = C.digest_string(context.source_sha256["owner/"+name+".py"])
            F.need(hashlib.sha256(path.read_bytes()).hexdigest() == wanted, "MIRROR_OWNER_HELPER_PIN")
            module = import_module(name)
            F.need(Path(module.__file__).resolve() == path, "MIRROR_OWNER_HELPER_ORIGIN")
            result.append(module)
        return result[0].contribute_from_context, result[1].method_queries
    finally:
        sys.path[:] = original


def _parameters(context):
    p = deepcopy(dict(context.parameters))
    F.fields(p, {"schema", "action", "runtime_adoption", "foundation", "packet",
        "workspace_config", "provider_workspace_path", "first_workspace_path", "second_workspace_path",
        "first_domain_path", "first_domain_id", "second_domain_path", "second_domain_id",
        "first_operation_limits", "second_operation_limits", "author_limits", "admission_limits",
        "first_template", "second_template"})
    F.need(p["schema"] == "DMKN_V5_MIRROR_METHOD_OWNER_V1"
           and p["action"] == "explicit-temporary-adoption-and-method-circulation", "MIRROR_EXPLICIT_ACTION")
    F.need(p["author_limits"] == AUTHOR and p["admission_limits"] == ADMISSION,
           "MIRROR_FIXED_WORKER_CAPS")
    for phase in ("first", "second"):
        F.need(p[phase+"_operation_limits"] == _operation_limits(phase), "MIRROR_FIXED_OPERATION_CAPS")
        C.digest_string(p[phase+"_domain_id"])
    F.need(p["first_domain_id"] != p["second_domain_id"], "MIRROR_SEPARATE_DOMAINS")
    paths = {}
    for field in ("provider_workspace_path", "first_workspace_path", "second_workspace_path",
                  "first_domain_path", "second_domain_path"):
        path = ordinary(p[field], fresh=True)
        for base in (context.installation, context.run, context.sources_owner,
                     context.sources_v5, context.sources_portable, *paths.values()):
            base = Path(base)
            F.need(not path.is_relative_to(base) and not base.is_relative_to(path), "MIRROR_DISJOINT_STATE")
        paths[field] = path
    work, run = ordinary(context.location_workspace), ordinary(context.run)
    F.need(work != run and work.is_relative_to(run), "MIRROR_OUTPUT_SCOPE")
    F.need(context.limits["memory_mib"] == 1024 and context.limits["active_processes"] == 4
           and context.limits["cpu_seconds"] == 300 and context.limits["wall_seconds"] == 600,
           "MIRROR_OUTER_ENVELOPE")
    F.need(p["packet"]["bytes"] == 498641 and p["packet"]["sha256"] ==
           "efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b",
           "MIRROR_RETAINED_PROVIDER_INPUT")
    F.need(p["foundation"]["bytes"] == 23313 and p["foundation"]["sha256"] ==
           "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c",
           "MIRROR_FOUNDATION_INPUT")
    envelope = p["workspace_config"]["packet_envelope"]
    F.need(envelope["deltas"] == 3 and envelope["edges"] == 8,
           "MIRROR_THREE_DELTA_ENVELOPE")
    return p, paths, work


def _seed(workspace, raw, image):
    # Pure structural extraction; this namespace is not an issuer or a client.
    extractor = SimpleNamespace(workspace=SimpleNamespace(_envelope=workspace._envelope), _aggregate_image=image)
    summary, groups, values, census = MixedClient._semantic_plan(extractor, raw)
    F.need(census["claims"] == census["frontiers"] == census["deltas"] == 1,
           "MIRROR_SEED_EVIDENCE_FORM")
    root, selected, bodies = C.summary_id(summary), [], set()
    for (owner, unused), encoded in sorted(groups.items()):
        opening = C.parse_json(encoded)
        group = C.verify_group_opening(owner, opening)
        workspace.modules.put_group(owner, opening)
        for declaration in group["declarations"]:
            if owner == root and declaration["kind"] == "theorem":
                selected.append((opening, declaration["name"]))
            for digest in sorted(permitted_hashes(declaration)):
                arity = declaration["universes"]; key = owner, arity, digest
                if key in bodies: continue
                F.need((arity, digest) in values, "MIRROR_SEED_MISSING_SEMANTICS")
                response = dict(schema=BODY_SCHEMA, module_id=owner, relative_name=declaration["name"],
                    universes=arity, body_hash=digest, expression=C.parse_json(values[arity, digest]))
                workspace.modules.put_body(owner, declaration["name"], response)
                bodies.add(key)
    F.need(len(selected) == 1, "MIRROR_SEED_SINGLE_ROOT_THEOREM")
    opening, name = selected[0]
    workspace.packets.put(root, raw)
    workspace.index.admit(workspace.adapter.encode_opening(root, name, opening),
                          expected_id=C.export_id(root, name))
    return dict(module=root, groups=len(groups), bodies=len(bodies), census=census,
                mathematical_acceptance=False)


def _contract(description, query):
    locator, descriptor = description["locator"], description["descriptor"]
    F.need(descriptor["kind"] == "theorem" and descriptor["universes"] == query["universes"]
           and descriptor["type"] == query["type"], "MIRROR_RETURNED_EXACT_CONTRACT")
    if "expected_module" in query:
        F.need(locator["module_id"] == query["expected_module"]
               and locator["relative_name"] == query["expected_name"], "MIRROR_ONWARD_EXACT_IDENTITY")


async def _acquire(client, endpoint, queries, detail):
    """No packet path, provider-private root or method name enters this receiver."""
    policy = OwnerEgressPolicy(dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test",
        public_ports=[], test_endpoints=[dict(host=endpoint.host, port=endpoint.port)]))
    envelope = deepcopy(SEARCH)
    for key in ("providers", "snapshots", "requests", "pages", "examined", "candidates", "bytes"):
        envelope[key] *= len(queries)
    envelope["generations"] = len(queries)
    detail["reservation"] = direct_contacts.reserve_queries(client, envelope, policy)
    contact = {key: getattr(endpoint, key) for key in ("host", "port", "tls", "server_name")}
    detail["queries"] = []
    for ordinal, query in enumerate(queries):
        row = dict(ordinal=ordinal, pages=[]); detail["queries"].append(row)
        row["binding"] = direct_contacts.next_query(client, {"selected": contact}, query["specs"],
            deepcopy(SEARCH), contact_lifetime_ms=90000)
        offer = await client.search_offer("selected", max_bytes=131072,
            max_expanded_bytes=262144, max_age_ms=60000, attempt_timeout_ms=5000)
        row["offer"] = offer
        F.need(offer["status"] == "OFFERED", "MIRROR_OFFER_REFUSED")
        partitions = [part for part in offer["partitions"] if part["anchor_count"] > 0]
        F.need(len(partitions) <= 2, "MIRROR_FINITE_PARTITION_SCOPE")
        for part in partitions:
            page = await client.search_page("selected", offer["snapshot_id"], part["partition"], 0,
                dict(examined=4, matches=2, bytes=131072, timeout_ms=1000, node_reads=50000),
                candidates_only=False, attempt_timeout_ms=5000)
            row["pages"].append(page)
            F.need(page["status"] == "VERIFIED_PAGE", "MIRROR_AUTHENTICATED_PAGE")
            if not page["matches"]: continue
            F.need(len(page["matches"]) == 1, "MIRROR_SINGLE_CONTRACT_CANDIDATE")
            candidate = await client.resolve("selected", page["matches"][0])
            description = client.describe_candidate(candidate)
            _contract(description, query)
            offered = await client.packet_offers(candidate, max_offers=1, max_bytes=4096)
            F.need(len(offered["packets"]) == 1, "MIRROR_ONE_OFFERED_PACKET")
            entry = {key: offered["packets"][0][key] for key in ("packet_sha256", "packet_bytes")}
            reader = SemanticReader(client, candidate, limits=deepcopy(HELPER), definition_mode="interface-only")
            try:
                staged = await reader.stage(candidate, entry)
                F.need(staged["status"] == "STAGED" and staged["module"] == description["locator"]["module_id"],
                       "MIRROR_STAGED_LOCATOR")
                detail.update(description=description, chosen_query=query, staged=staged, rounds=[])
                for round_number in range(32):
                    preview = reader.preview()
                    trace = dict(round=round_number, preview=preview, actions=[])
                    detail["rounds"].append(trace)
                    if preview["status"] == READY:
                        return reader, description
                    progressed = False
                    for demand in preview["demands"]:
                        if demand["kind"] == "NeedModuleEvidence":
                            members = [m for m in staged["members"] if m["module"] == demand["module"]]
                            F.need(len(members) == 1, "MIRROR_DEMANDED_INTERNAL_MEMBER")
                            chosen = reader.select_member(staged["module"], bytes(members[0]["journal"]))
                            trace["actions"].append(chosen)
                            progressed |= chosen["status"] == "SELECTED_MEMBER"
                        resolved = await reader.resolve(demand, max_bytes=65536)
                        trace["actions"].append(dict(kind="resolve", status=resolved["status"], demand=demand))
                        progressed |= resolved["status"] == "RESOLVED"
                        if demand["kind"] == "NeedBody":
                            fetched = await reader.fetch_body(demand, max_bytes=65536)
                            trace["actions"].append(fetched)
                            progressed |= fetched["status"] == "FETCHED"
                    F.need(progressed, "MIRROR_SEMANTIC_NO_PROGRESS")
                raise ValueError("MIRROR_SEMANTIC_ROUND_LIMIT")
            except BaseException:
                reader.close()
                raise
        row["outcome"] = "NO_CANDIDATE_IN_SELECTED_FINITE_PAGES"
    raise ValueError("MIRROR_NO_CANDIDATE_WITHIN_ORIGINAL_QUERY_ENVELOPE")


def _check_descriptor(workspace, module, name, kind, expression):
    unused, descriptor = workspace.modules.get_group(module, name)
    F.need(descriptor["name"] == name and descriptor["kind"] == kind
           and descriptor["universes"] == 1 and descriptor["type"] == expression,
           "MIRROR_ACTUAL_DESCRIPTOR")
    return dict(module=module, name=name, kind=kind, universes=1,
                type_sha256=hashlib.sha256(C.canonical(expression)).hexdigest())


async def _phase(context, p, paths, work, phase, support, foundation,
                 queries, provider_workspace, template, contribute, detail):
    workspace = client = provider = reader = domain = None
    detail.update(status="FAILED", stage="adopt", error=None, cleanup_errors=[],
                  client_closed=False, workspace_closed=False, domain_withdrawn=False, service_closed=False)
    try:
        # Second phase reaches here only after first closure; no overlapping
        # same-process controller clock or second grant reservation exists.
        domain = TrustDomain.create(paths[phase+"_domain_path"], p[phase+"_domain_id"], support)
        detail["trust"] = domain.identity()
        runtime = RuntimeProfile.from_context(context, p["runtime_adoption"], trust_domain=domain)
        workspace = Workspace.open(paths[phase+"_workspace_path"], p["workspace_config"], create=True)
        grant = workspace.reserve(p[phase+"_operation_limits"], outer_deadline=context.deadline-10)
        detail["operation_id"] = grant.identifier
        client = runtime.open_operation(workspace, grant, mode="validated", authoring=True,
            foundation_bytes=foundation, foundation_sha256=p["foundation"]["sha256"])
        provider = CompositeProvider(index=provider_workspace.index, custody=provider_workspace.modules,
                                     packets=provider_workspace.packets, **HTTP)
        service_deadline = min(grant.deadline-5, context.deadline-10, time.monotonic()+90)
        detail.update(stage="acquire", service_deadline=service_deadline)
        async with asyncio.timeout_at(service_deadline):
            endpoint = await provider.start(host="127.0.0.1", port=0)
            detail["endpoint"] = {key: getattr(endpoint, key) for key in ("host", "port", "tls", "server_name")}
            reader, description = await _acquire(client, endpoint, queries, detail)
            await provider.stop()
        detail["service"] = provider.status()
        F.need(provider.server is None and not provider.tasks, "MIRROR_HTTP_CLOSED_BEFORE_CHECKING")
        detail["service_closed"] = True
        before_network = deepcopy(client.report()["acquisition"]["used"])
        detail["stage"] = "admit-and-import"
        module = description["locator"]["module_id"]
        ready = reader.finish({module: deepcopy(ADMISSION)})
        detail["import"] = {key: ready[key] for key in ("status", "demands", "cost", "mathematical_acceptance")}
        F.need(ready["status"] == "READY" and ready["context"] is not None and not ready["demands"]
               and ready["cost"]["frontend_theorem_ancestor_proof_bytes"] == 0,
               "MIRROR_LIVE_INTERFACE_CONTEXT")
        opening, descriptor = workspace.modules.get_group(module, description["locator"]["relative_name"])
        F.need(opening == description["opening"] and descriptor == description["descriptor"],
               "MIRROR_UNCHANGED_ADMITTED_LOCATOR")
        _contract(description, detail["chosen_query"])
        if phase == "first":
            F.need(template.count("__METHOD_REF__") == 1, "MIRROR_SINGLE_TEMPLATE_REFERENCE")
            reference = _reference(module, description["locator"]["relative_name"])
            source = template.replace("__METHOD_REF__", reference)
            roots = [MIRROR, INVOLUTION]
            detail["method_reference"] = reference
        else:
            mirror_type, involution_type = _mirror_types()
            detail["imported_descriptors"] = [
                _check_descriptor(workspace, module, MIRROR, "definition", mirror_type),
                _check_descriptor(workspace, module, INVOLUTION, "theorem", involution_type)]
            C.digest_string(module)
            F.need(template.count("__MIRROR_MODULE_HEX__") == 10, "MIRROR_ONWARD_TEMPLATE_TOKENS")
            source = template.replace("__MIRROR_MODULE_HEX__", module)
            roots = [INJECTIVE]
        F.need("__METHOD_REF__" not in source and "__MIRROR_MODULE_HEX__" not in source,
               "MIRROR_NO_REMAINING_TEMPLATE_TOKEN")
        detail["source"] = _write(work/(phase+"-source.lean"), source.encode("utf-8"))
        detail["before_contribution"] = client.report()
        detail["stage"] = "author-admit-publish"
        result = contribute(client, ready["context"], source=source, roots=roots,
            export_names=roots, author_limits=deepcopy(AUTHOR), admission_limits=deepcopy(ADMISSION))
        detail["contribution"] = result
        F.need(result["status"] == "CONTRIBUTED" and result["operation_id"] == grant.identifier,
               "MIRROR_CONTRIBUTED")
        intent = result["publication"]["intent"]
        packet = workspace.packets.get(intent["packet_sha256"], intent["packet_bytes"])
        detail["packet"] = _write(work/(phase+"-published-packet.json"), packet)
        if phase == "first":
            mirror_type, involution_type = _mirror_types()
            detail["output_descriptors"] = [
                _check_descriptor(workspace, intent["module"], MIRROR, "definition", mirror_type),
                _check_descriptor(workspace, intent["module"], INVOLUTION, "theorem", involution_type)]
        else:
            detail["output_descriptors"] = [_check_descriptor(workspace, intent["module"],
                INJECTIVE, "theorem", _injective_type(module))]
        after = client.report(); detail["after_contribution"] = after
        F.need(after["counts"]["admission_submissions"] == 2
               and after["counts"]["author_calls"] == after["counts"]["new_import_sessions"] == 1
               and after["counts"]["publication_attempts"] == 1
               and after["preparation"]["calls"] == 1 and after["mixed"]["attempts"] == 2,
               "MIRROR_ONE_CONTRIBUTION_PER_FRESH_OWNER")
        F.need(all(after["acquisition"]["used"][key] == before_network[key]
                   for key in ("requests", "reply_bytes")), "MIRROR_NO_NETWORK_AFTER_SERVICE_CLOSURE")
        detail.update(status="COMPLETED", stage="done")
    except BaseException as error:
        detail["error"] = remote_reader._error(error)
        raise
    finally:
        if provider is not None and not detail["service_closed"]:
            try:
                async with asyncio.timeout_at(context.deadline-5): await provider.stop()
                detail["service"] = provider.status()
                detail["service_closed"] = provider.server is None and not provider.tasks
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="service", **remote_reader._error(error)))
        if reader is not None:
            try:
                detail["reader"] = reader.report(); reader.close()
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="reader", **remote_reader._error(error)))
        if client is not None:
            try:
                closed = await client.close(); detail["client"] = closed
                F.need(closed["closed"] and not closed["cleanup_uncertain"]
                       and all(closed[key] is not None and closed[key]["closed"]
                               for key in ("receipt", "aggregate", "mixed", "preparation")), "MIRROR_CLIENT_CLEANUP")
                if detail["status"] == "COMPLETED":
                    F.need(closed["status"] == "CLOSED" and not closed["failures"], "MIRROR_CLIENT_CLEAN_CLOSE")
                detail["client_closed"] = True
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="client", **remote_reader._error(error)))
        if workspace is not None:
            detail["workspace_closed"] = _close_workspace(workspace, detail["cleanup_errors"])
        if domain is not None:
            try:
                domain.withdraw("Explicit finite mirror-method phase completed or failed")
                marker = ordinary(paths[phase+"_domain_path"]/"WITHDRAWN", directory=False)
                F.need(marker.stat().st_size <= 16384, "MIRROR_WITHDRAWAL_BOUND")
                withdrawal = C.parse_json(marker.read_bytes(), C.Limits(max_bytes=16384))
                F.need(withdrawal["schema"] == "DMKN_LOCAL_TRUST_WITHDRAWN_V1"
                       and withdrawal["adoption"] == detail["trust"], "MIRROR_EXACT_WITHDRAWAL")
                detail.update(domain_withdrawn=True, withdrawal=withdrawal)
            except BaseException as error:
                detail["cleanup_errors"].append(dict(component="trust", **remote_reader._error(error)))
        if detail["cleanup_errors"] or not all(detail[key] for key in
                ("client_closed", "workspace_closed", "domain_withdrawn", "service_closed")):
            detail["status"] = "FAILED"
        remote_reader._save(work/(phase+"-result.json"), detail)


async def run(context):
    p, paths, work = _parameters(context)
    contribute, construct_queries = _owner_helpers(context)
    report = dict(schema="DMKN_V5_MIRROR_METHOD_RESULT_V1", status="FAILED", stage="freeze-queries",
        error=None, cleanup_errors=[], phases={}, proof_production_calls=0,
        global_complete=False, mathematical_acceptance=False, full_v5_release=False,
        authority="OPERATIONAL_COMPOSITION_REPORT_NOT_TRANSFERABLE_AUTHORITY")
    report["selected_file_pins"] = {key: deepcopy(p[key]) for key in
                                    ("first_template", "second_template", "foundation", "packet")}
    report["owner_source_sha256"] = {name: context.source_sha256["owner/"+name]
                                    for name in ("owner.py", "contribution.py", "method_query.py")}
    provider_workspace = None
    primary = None
    try:
        # This happens before reading ANY candidate/fixture packet data. Only
        # the known BASE identity and the adopted local codec feed these bytes.
        queries = construct_queries(C, BASE)
        F.need(len(queries) == 2, "MIRROR_TWO_PROSPECTIVE_ALTERNATIVES")
        report["first_queries"] = _write(work/"first-queries.json", C.canonical(queries))
        templates = {phase: read_pin(p[phase+"_template"], 65536).decode("utf-8")
                     for phase in ("first", "second")}
        support = RuntimeProfile.support_manifest(context, p["runtime_adoption"])
        foundation = read_pin(p["foundation"], MIB)
        provider_workspace = Workspace.open(paths["provider_workspace_path"], p["workspace_config"], create=True)
        raw = read_pin(p["packet"], MIB)
        report["seed"] = _seed(provider_workspace, raw, p["workspace_config"]["wire_profile"]["aggregate_image"])
        # The fixture identity is deliberately not passed into the receiver.
        report["stage"] = "first-agent"
        first = report["phases"]["first"] = {}
        await _phase(context, p, paths, work, "first", support, foundation, queries,
                     provider_workspace, templates["first"], contribute, first)
        F.need(first["status"] == "COMPLETED", "MIRROR_FIRST_PHASE_FAILED")
        F.need(_close_workspace(provider_workspace, report["cleanup_errors"]), "MIRROR_SEED_WORKSPACE_CLOSE")
        provider_workspace = None
        # The live first owner is closed and withdrawn. This opens ordinary
        # public custody only, never revives its saved context or trust domain.
        onward = first["contribution"]["publication"]["intent"]["module"]
        second_queries = _known_query(onward)
        report["second_queries"] = _write(work/"second-queries.json", C.canonical(second_queries))
        provider_workspace = Workspace.open(paths["first_workspace_path"], p["workspace_config"], create=False)
        report["stage"] = "second-agent"
        second = report["phases"]["second"] = {}
        await _phase(context, p, paths, work, "second", support, foundation, second_queries,
                     provider_workspace, templates["second"], contribute, second)
        F.need(second["status"] == "COMPLETED", "MIRROR_SECOND_PHASE_FAILED")
        report.update(status="COMPLETED", stage="done")
    except BaseException as error:
        primary = error
        report["error"] = remote_reader._error(error)
    finally:
        if provider_workspace is not None:
            report["final_provider_workspace_closed"] = _close_workspace(provider_workspace, report["cleanup_errors"])
            if not report["final_provider_workspace_closed"]: report["status"] = "FAILED"
        if report["cleanup_errors"] or time.monotonic() >= context.deadline:
            report["status"] = "FAILED"
        report["finished"] = time.monotonic()
        # Each full phase is retained separately. Do not duplicate its bounded
        # query/coverage/issuer reports into an aggregate that could exceed 1MiB.
        report["phases"] = {phase: dict(status=detail.get("status", "FAILED"),
            stage=detail.get("stage"), error=detail.get("error"),
            report_path=str(work/(phase+"-result.json")),
            operation_id=detail.get("operation_id"),
            module=((detail.get("contribution") or {}).get("publication") or {}).get("intent", {}).get("module"),
            cleanup_errors=detail.get("cleanup_errors", []))
            for phase, detail in report["phases"].items()}
        remote_reader._save(work/"mirror-method-result.json", report)
    if isinstance(primary, asyncio.CancelledError): raise primary
    return report


def main(context):
    return 0 if asyncio.run(run(context))["status"] == "COMPLETED" else 1
