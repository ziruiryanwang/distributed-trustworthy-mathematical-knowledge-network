"""Changed endpoint: ordinary two-use composition over a real accepted delta.

One source export and one complete onward packet; no guest, snapshot, sealer,
network or checker implementation. A new cold receiver accepts only after every
origin handle/session/preparation owner is closed. Root selects exact runtime.
"""
from pathlib import Path
import argparse
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.bindings import journal
from admission.verifier import ReceiptVerifier
from authoring.receipt_integration import named, references, FOUNDATION_SHA
from authoring.source import NATIVE_NAME_LIMITS
from delta.actual import (ROOT, BASE, TARGET as FIRST, IMAGE, FOUNDATION, POLICY,
                          FIXTURES, read_pin, save, sha, expect_refusal)
from delta.authoring import DeltaImportSession, DeltaSourceOperation, DeltaOwnerPreparation
from delta.packet import SCHEMA as PACKET_SCHEMA, DeltaError
from delta.receiver import DeltaVerifier
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source
from production.producer import encoded, parse, fields, require, uint, digest, pin_fields, file_pin, MIB

SCHEMA = "DMKN_V5_ACTUAL_DELTA_AUTHOR_RETURN_V1"
INPUTS = ("preparation_profile", "child_input", "expected_journal", "receipt", "bundle",
          "foundation", "source", "roots")
CONFIG = ("schema", *INPUTS, "native_executable", "runtime_pins", "output_directory",
          "wall_seconds", "call_limits", "author_limits", "owner_allowance")
SOURCE_SHA = "a4e2d897f929e2e63c43c70f274a8f270d9bb783180a6677366ae50ad73df153"
ROOTS_SHA = "7882f5358514ab6fbe98c212868e267cd9d0dc4a20561b2702d66530a868b2e9"
SECOND_ROOT = named("OwnerV5", "fold_map_twice_received")


def count_first_references(expression):
    pending, count, visits = [expression], 0, 0
    children = {"sort": (), "bvar": (), "const": (), "app": (1,2),
                "lam": (2,3), "forall": (2,3), "let": (1,2,3), "proj": (3,)}
    target = ["external",FIRST,named("OwnerV5","fold_map_received")]
    while pending:
        node = pending.pop(); visits += 1
        require(visits <= C.DEFAULT_LIMITS.max_nodes, "AUTHOR_REFERENCE_VISITS")
        if node[0] == "const" and node[1] == target: count += 1
        pending.extend(node[i] for i in children[node[0]])
    return count


def inspect_reuse(export_raw, request_raw, child):
    """Inspect actual exported proof closure, not just source text spelling."""
    exported, request = C.parse_json(export_raw), C.parse_json(request_raw)
    context = request["context"]
    require(exported["roots"] == request["roots"] == [SECOND_ROOT], "AUTHOR_EXACT_ROOT")
    external = [{"source_name":C.relocated_name(item["owner"],d["name"]),
                 "module":item["owner"],"relative_name":d["name"]}
                for item in context["imports"] for d in item["group"]["declarations"]]
    environment = decode_source(exported["rows"],exported["local_names"],
        context["foundation_view"]["names"],FOUNDATION,POLICY,external,NATIVE_NAME_LIMITS)
    packet = C.parse_json(child["packet"]); witness = packet["deltas"][-1]
    require(environment.spec == witness["local_spec"] and environment.module == child["local_module"],
            "AUTHOR_ACTUAL_PACKET_SPEC")
    descriptors = {C.name_key(d["name"]):d for group in environment.spec["groups"]
                   for d in group["declarations"]}
    root_key = C.name_key(SECOND_ROOT); declaration = descriptors[root_key]
    require(declaration["kind"] == "theorem" and declaration["universes"] == 4,
            "AUTHOR_POLYMORPHIC_THEOREM")
    require({("external",BASE,C.name_key(named("CommonsV5",name))) for name in ("Tree","fold","map")}
            <= references(declaration["type"]), "AUTHOR_IMPORTED_STATEMENT_STRUCTURE")
    pending, seen, proof_refs, first_uses, root_proof = [root_key], set(), set(), 0, None
    while pending:
        key = pending.pop()
        if key in seen: continue
        require(key in descriptors and len(seen) < 4096, "AUTHOR_LOCAL_PROOF_CLOSURE")
        seen.add(key); item = descriptors[key]
        if item["kind"] not in ("theorem","definition","opaque"): continue
        commitment = (environment.local_proofs[Address.of(environment.module,item["name"])]
                      if item["kind"] == "theorem" else item["value_hash"])
        raw = environment.bodies[item["universes"],commitment]
        if key == root_key: root_proof = raw
        expression = C.parse_json(raw); refs = references(expression)
        proof_refs.update(refs); first_uses += count_first_references(expression)
        pending.extend(ref[2] for ref in refs if ref[0] == "local")
    require(root_proof is not None and first_uses >= 2, "AUTHOR_TWO_ACTUAL_PRIOR_THEOREM_USES")
    return {"local_module":environment.module,"local_groups":len(environment.spec["groups"]),
        "native_export_rows":len(exported["rows"]),"new_relation_rows":len(witness["rows"]),
        "first_delta_reference_occurrences":first_uses,"root_proof_sha256":sha(root_proof),
        "root_type_sha256":sha(C.canonical(declaration["type"])),
        "local_proof_value_closure":[C.parse_json(key) for key in sorted(seen)],
        "external_proof_references":[{"module":r[1],"name":C.parse_json(r[2])}
                                     for r in sorted(proof_refs) if r[0] == "external"],
        "frontend_imported_theorem_proof_bytes":0,
        "onward_packet_retains_first_delta_proof":True,
        "scope":"ACTUAL_SOURCE_EXPORT_REFERENCE_EVIDENCE_NOT_MATHEMATICAL_AUTHORITY"}


def run(config_path, config_sha256):
    started, cpu_started = time.monotonic(), time.process_time()
    digest(config_sha256); config_path = Path(config_path)
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
            "AUTHOR_ACTUAL_OWNER_INVOCATION")
    require(config_path.is_absolute() and config_path.resolve() == config_path
            and config_path.is_file() and 0 < config_path.stat().st_size <= MIB,
            "AUTHOR_ACTUAL_CONFIG_PATH")
    with config_path.open("rb") as stream: config_raw = stream.read(MIB+1)
    require(len(config_raw) <= MIB and sha(config_raw) == config_sha256, "AUTHOR_ACTUAL_CONFIG_PIN")
    config = parse(config_raw); fields(config,CONFIG)
    require(config["schema"] == SCHEMA, "AUTHOR_ACTUAL_CONFIG_SCHEMA")
    uint(config["wall_seconds"],1800,1); deadline = started+config["wall_seconds"]
    limits = config["call_limits"]
    fields(limits,("native_cpu_seconds","receipt_cpu_seconds","wall_seconds","memory_mib"))
    for key in ("native_cpu_seconds","receipt_cpu_seconds","wall_seconds"): uint(limits[key],600,1)
    uint(limits["memory_mib"],4096,64)
    author_limits = config["author_limits"]
    fields(author_limits,("cpu_seconds","wall_seconds","memory_mib"))
    uint(author_limits["cpu_seconds"],1200,1); uint(author_limits["wall_seconds"],600,1)
    uint(author_limits["memory_mib"],4096,64)
    allowance = config["owner_allowance"]
    fields(allowance,("allowance_id","operations","worker_cpu_seconds","controller_cpu_seconds",
                      "wall_seconds","output_bytes","output_entries"))
    digest(allowance["allowance_id"])
    for key,low,high in (("operations",1,1),("worker_cpu_seconds",author_limits["cpu_seconds"],3600),
            ("controller_cpu_seconds",1,600),("wall_seconds",1,1800),
            ("output_bytes",128*MIB,1024*MIB),("output_entries",32,4096)):
        uint(allowance[key],high,low)

    def remaining():
        value = math.floor(deadline-time.monotonic())
        require(value >= 1,"AUTHOR_ACTUAL_ORIGINAL_WALL"); return value

    inputs = {name:read_pin(config[name]) for name in INPUTS}
    for name,(size,pin) in FIXTURES.items():
        require(len(inputs[name]) == size and sha(inputs[name]) == pin,"AUTHOR_RETAINED_FIXTURE:"+name)
    require(sha(inputs["bundle"]) == "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"
            and sha(inputs["foundation"]) == FOUNDATION_SHA and sha(inputs["source"]) == SOURCE_SHA
            and sha(inputs["roots"]) == ROOTS_SHA,"AUTHOR_EXACT_SEMANTIC_FIXTURES")
    profile = parse(inputs["preparation_profile"]); producer = profile["producer"]
    require((producer["image_id"],producer["foundation"],producer["policy"])
            == (IMAGE,FOUNDATION,POLICY),"AUTHOR_CURRENT_PROFILE")
    require(file_pin(Path(__file__).resolve()) in profile["source_pins"],"AUTHOR_HARNESS_PROFILE_PIN")
    runtime_rows = config["runtime_pins"]
    require(type(runtime_rows) is list and 1 <= len(runtime_rows) <= 128,"AUTHOR_RUNTIME_ROWS")
    runtime = {}
    for row in runtime_rows:
        path = pin_fields(row)
        require(path.resolve() == path and str(path) not in runtime and file_pin(path) == row,
                "AUTHOR_DISTINCT_ACTUAL_RUNTIME_PIN")
        runtime[str(path)] = {key:row[key] for key in ("bytes","sha256")}
    required_sources = {Path(__file__).resolve(),Path(__file__).parent/"actual.py",
                        Path(__file__).resolve().parents[1]/"authoring/receipt_integration.py"}
    require(required_sources <= {pin_fields(row) for row in runtime_rows}
            and required_sources <= {pin_fields(row) for row in profile["source_pins"]}
            and config["native_executable"] in runtime_rows,"AUTHOR_HELPER_AND_NATIVE_PINS")
    native = pin_fields(config["native_executable"])
    bundle = C.parse_json(inputs["bundle"]); first = C.parse_json(inputs["child_input"])
    base_summary, first_summary = C.summarize(bundle["spec"]),C.summarize(first["local_spec"])
    require(C.summary_id(base_summary) == BASE and C.summary_id(first_summary) == FIRST
            and journal(inputs["expected_journal"])["summary"] == first_summary,"AUTHOR_BASE_FIRST_BINDING")
    roots = C.parse_json(inputs["roots"]); require(roots == [SECOND_ROOT],"AUTHOR_SELECTED_ROOT")
    packet = C.canonical({"schema":PACKET_SCHEMA,
        "frontiers":[{"receipt_hex":inputs["receipt"].hex(),"summary":base_summary}],"deltas":[first]})
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "AUTHOR_FRESH_OUTPUT")
    protected = [config_path,Path(__file__).resolve().parents[1],Path(profile["lean_root"]),
                 Path(producer["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(config[name]) for name in INPUTS)
    protected.extend(pin_fields(row) for row in runtime_rows+profile["source_pins"]+profile["lean_runtime_pins"])
    protected.extend(pin_fields(row) for row in (profile["worker"],profile["image"],profile["native_executable"],
        producer["host"],producer["python"],producer["python_dll"],*producer["source_pins"],*producer["runtime_pins"]))
    require(all(not output.is_relative_to(path) and not path.is_relative_to(output) for path in protected),
            "AUTHOR_OUTPUT_OVERLAP")
    remaining(); output.mkdir(); save(output/"configuration.json",config)
    result = {"schema":SCHEMA,"status":"FAIL","configuration_sha256":config_sha256,
        "input_pins":{name:config[name] for name in INPUTS},"first_admitted":False,
        "second_admitted_cold":False,"author_calls":0,"proof_calls":0,"guest_calls":0,"network_calls":0,
        "error":None,"authority":"LOCAL_OPERATION_EVIDENCE_NOT_TRANSFERABLE_MATHEMATICAL_AUTHORITY"}
    receivers, frontiers, closers = [], [], []
    preparation = session = operation = None
    try:
        preparation = DeltaOwnerPreparation(profile,
            {**allowance,"wall_seconds":min(allowance["wall_seconds"],remaining())},output/"preparation")
        closers.append(("preparation",preparation))

        def cold_receiver(name, delta_count, size):
            receipt_runtime = {row["path"]:{key:row[key] for key in ("bytes","sha256")}
                for row in (producer["host"],producer["python"],producer["python_dll"],*producer["runtime_pins"])}
            frontier = ReceiptVerifier(supervisor_manifest=producer["supervisor_manifest"]["path"],
                supervisor_manifest_sha256=producer["supervisor_manifest"]["sha256"],
                executable=producer["host"]["path"],runtime_pins=receipt_runtime,image_id=IMAGE,
                foundation=FOUNDATION,policy=POLICY,operations=1,submitted_bytes=len(inputs["receipt"]),
                reserved_cpu_seconds=limits["receipt_cpu_seconds"],wall_seconds=remaining())
            frontiers.append((name,frontier)); closers.append((name+"-frontier",frontier))
            receiver = DeltaVerifier(frontier,native_executable=str(native),runtime_pins=runtime,
                output_directory=output/name,operations=1,submitted_bytes=size,
                reserved_cpu_seconds=limits["receipt_cpu_seconds"]+delta_count*limits["native_cpu_seconds"],
                controller_cpu_seconds=120,wall_seconds=remaining(),output_bytes=64*MIB,output_entries=256)
            receivers.append((name,receiver)); closers.append((name+"-delta",receiver))
            return receiver

        def receive(receiver, raw, summary):
            return receiver.receive(raw,summary,**{**limits,"wall_seconds":min(limits["wall_seconds"],remaining())})

        origin = cold_receiver("origin",1,len(packet)); first_handle = receive(origin,packet,first_summary)
        require(origin.describe(first_handle)["journal"] == inputs["expected_journal"],"AUTHOR_ACTUAL_FIRST_JOURNAL")
        result["first_admitted"] = True
        session = DeltaImportSession(origin,max_handles=1,max_members=2,max_calls=4096,
            packet_bytes=len(packet),data_bytes=16*MIB,wall_seconds=remaining())
        closers.append(("session",session)); require(session.use_handle(first_handle) == FIRST,"AUTHOR_FIRST_HANDLE")
        opened = set()
        for opening in bundle["openings"]:
            require(session.open_group(BASE,opening) == bundle["spec"]["groups"][opening["index"]]
                    and opening["index"] not in opened,"AUTHOR_EXACT_BASE_OPENING")
            opened.add(opening["index"])
        require(opened == set(range(base_summary["group_count"])),"AUTHOR_BASE_OPENING_CENSUS")
        for body in bundle["bodies"]:
            require(session.supply_body(BASE,body["universes"],body["expression"]) == body["digest"],
                    "AUTHOR_EXACT_BASE_SEMANTICS")
        require(session.open_group(FIRST,C.group_opening(first["local_spec"],0))
                == first["local_spec"]["groups"][0],"AUTHOR_FIRST_DELTA_INTERFACE")
        operation = DeltaSourceOperation(session,inputs["foundation"],FOUNDATION_SHA,
            inputs["source"].decode("utf-8"),roots)
        closers.append(("operation",operation)); ready = operation.prepare()
        require(ready["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
                "AUTHOR_CONTEXT_NOT_READY")
        result["author_calls"] += 1
        authored = preparation.author(operation,"author",**{**author_limits,
            "wall_seconds":min(author_limits["wall_seconds"],remaining())})
        require(authored["status"] == "UNTRUSTED_DELTA_PACKET_PREPARED"
                and authored["mathematical_acceptance"] is False,"AUTHOR_UNTRUSTED_RETURN_REQUIRED")
        child = authored["child"]; onward = read_pin(authored["packet"])
        require(onward == child["packet"] and sha(onward) == child["packet_sha256"],"AUTHOR_ONWARD_EXACT_BYTES")
        parsed = C.parse_json(onward)
        require(parsed["frontiers"] == C.parse_json(packet)["frontiers"]
                and len(parsed["deltas"]) == 2 and C.canonical(parsed["deltas"][0]) == C.canonical(first),
                "AUTHOR_COMPLETE_TWO_DELTA_REAL_FRONTIER_PACKET")
        second = parsed["deltas"][1]
        require(second["rank"] == 2 and child["local_module"] not in (BASE,FIRST)
                and {journal(bytes(item["journal"]))["module"] for item in second["parents"]} == {BASE,FIRST},
                "AUTHOR_ACTUAL_SECOND_PARENT_CLOSURE")
        exported = read_pin(authored["export"])
        request = read_pin(file_pin(Path(authored["evidence"])/"source-request.json"))
        require(request == ready["request"],"AUTHOR_SAME_PREPARED_SOURCE_REQUEST")
        result["reuse"] = inspect_reuse(exported,request,child)
        result["prepared"] = {"packet":authored["packet"],"export":authored["export"],
            "module":child["local_module"],"summary":child["summary"],"census":child["census"],
            "mathematical_acceptance":False}
        save(output/"source-reuse.json",result["reuse"])

        # No live originating mathematical authority survives into cold receiving.
        for name,value in reversed(closers): value.close()
        result["origin_close_refusal"] = expect_refusal("origin_closed_before_return",lambda: origin.describe(first_handle),
            DeltaError,"DELTA_CLOSED_OR_CHANGED_FRONTIER_OWNER","INVALID_OR_UNBOUND")
        require(all(value.report()["closed"] for unused,value in receivers+frontiers)
                and preparation.report()["closed"],"AUTHOR_ORIGIN_CLOSED")
        onward = read_pin(authored["packet"])
        recipient = cold_receiver("cold-recipient",2,len(onward))
        second_handle = receive(recipient,onward,child["summary"])
        live = recipient.describe(second_handle)
        require(live["module"] == child["local_module"] and journal(live["journal"])["rank"] == 2,
                "AUTHOR_COLD_COMPUTED_SECOND_JOURNAL")
        require({item["module"] for item in recipient.members(second_handle)} == {BASE,FIRST,child["local_module"]},
                "AUTHOR_COLD_COMPLETE_MEMBERS")
        require(recipient.open_group(second_handle,C.group_opening(second["local_spec"],0))
                == second["local_spec"]["groups"][0]
                and recipient.export_packet(second_handle) == onward,"AUTHOR_COLD_OPEN_EXPORT")
        result["second_admitted_cold"] = True
        result["cold_conclusion"] = {"module":live["module"],"journal":list(live["journal"]),
            "profile_id":live["profile_id"],"packet_sha256":sha(onward),"persisted_handle":False}
        require(sum(value.report()["attempts"] for unused,value in frontiers) == 2,
                "AUTHOR_TWO_REAL_COLD_FRONTIER_CALLS")
        for name in INPUTS: require(read_pin(config[name]) == inputs[name],"AUTHOR_INPUT_CHANGED")
        for row in runtime_rows: require(file_pin(Path(row["path"])) == row,"AUTHOR_RUNTIME_CHANGED")
        require(config_path.read_bytes() == config_raw,"AUTHOR_CONFIG_CHANGED")
        remaining(); result["status"] = "PASS_ORDINARY_DELTA_COMPOSITION_AND_FRESH_COMPLETE_PACKET_ADMISSION"
    except BaseException as error:
        result["error"] = {"type":type(error).__name__,"message":str(error)[:4000]}
    finally:
        errors = []
        for name,value in reversed(closers):
            try: value.close()
            except BaseException as error: errors.append({"component":name,"error":str(error)[:1000]})
        result["cleanup_errors"] = errors
        result["receivers"] = {name:value.report() for name,value in receivers}
        result["frontiers"] = {name:value.report() for name,value in frontiers}
        result["preparation"] = None if preparation is None else preparation.report()
        result["owner_process_cpu_seconds"] = time.process_time()-cpu_started
        result["wall_seconds_before_final_report"] = time.monotonic()-started
        result["accounting_scope"] = ("TWO_CRYPTO_THREE_NATIVE_ONE_LEAN_AUTHOR_WORKERS_AT_MOST;"
            "SUM_DISJOINT_WORKER_JOB_CPU_PLUS_SINGLE_OWNER_PROCESS_CPU;"
            "DO_NOT_ADD_INCLUSIVE_NESTED_CONTROLLER_TIMES_OR_ENCLOSING_JOB_AGAIN;"
            "FAILED_UNOBSERVED_WORK_RETAINS_RESERVATIONS;FINAL_WRITE_EXIT_TAILS_EXCLUDED")
        if errors or time.monotonic() >= deadline: result["status"] = "FAIL"
        try: save(output/"RESULT.json",result); remaining()
        except BaseException as error:
            result.update(status="FAIL",finalization_error={"type":type(error).__name__,"message":str(error)[:2000]})
            save(output/"FINALIZATION-FAILED.json",result)
    return result


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--config",required=True); parser.add_argument("--config-sha256",required=True)
    args = parser.parse_args()
    try:
        result = run(args.config,args.config_sha256)
        print(encoded({key:result.get(key) for key in ("status","first_admitted","second_admitted_cold","error")}).decode(),end="")
        return 0 if result["status"].startswith("PASS_") else 1
    except BaseException as error:
        print(encoded({"status":"FAIL_CONFIGURATION_OR_REPORT","type":type(error).__name__,
                       "message":str(error)[:4000]}).decode(),end="",file=sys.stderr)
        return 1


if __name__ == "__main__": raise SystemExit(main())
