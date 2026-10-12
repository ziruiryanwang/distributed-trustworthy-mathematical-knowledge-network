"""Selected actual receipt -> live ordinary source -> untrusted child capsule.

One integration harness, not another controller, sandbox, or proof authority.
Only the local owner supplies the pinned configuration. No retry, networking,
child proving, synthetic handles, or deserialization of acceptance is provided.
Run only under root's separately reviewed finite enclosing process selection.
"""
from pathlib import Path
import argparse
import hashlib
import math
import os
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission.verifier import ReceiptVerifier
from authoring.imports import ImportSession
from authoring.source import SourceOperation, NATIVE_NAME_LIMITS
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source
from preparation.owner import OwnerPreparation
from production.producer import (MIB, encoded, parse, fields, require, uint,
                                digest, pin_fields, file_pin, clean)

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MODULE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
BUNDLE_SHA = "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"
FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
SCHEMA = "DMKN_V5_RECEIPT_SOURCE_INTEGRATION_V1"
INPUT_NAMES = ("preparation_profile", "receipt", "bundle", "foundation", "source", "roots")
CONFIG_FIELDS = ("schema", *INPUT_NAMES, "output_directory", "wall_seconds",
                 "receive_limits", "session_limits", "owner_allowance",
                 "author_limits", "snapshot_limits")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_pin(pin, maximum):
    path = pin_fields(pin, maximum)
    require(path.resolve() == path and path.is_file(), "INTEGRATION_CANONICAL_INPUT")
    require(file_pin(path) == pin, "INTEGRATION_INPUT_PIN")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    require(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "INTEGRATION_READ_PIN")
    return raw


def save(path, value):
    raw = encoded(value)
    require(len(raw) <= 4*MIB, "INTEGRATION_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def named(*parts):
    return [["s", part] for part in parts]


def validate_limits(config):
    """Reject bad later-stage grants before spending the receiving allocation."""
    simple = {
        "receive_limits": {"cpu_seconds": (1, 600), "wall_seconds": (1, 600), "memory_mib": (64, 4096)},
        "author_limits": {"cpu_seconds": (1, 1200), "wall_seconds": (1, 600), "memory_mib": (64, 4096)},
        "session_limits": {"max_modules": (1, 8), "max_calls": (1, 65536),
            "receipt_bytes": (1, 1024*MIB), "data_bytes": (1, 16*MIB), "wall_seconds": (1, 3600)},
        "snapshot_limits": {"cycles": (1, 2**28), "po2": (12, 20), "prepare_cpu_seconds": (1, 60),
            "prepare_wall_seconds": (1, 600), "cpu_seconds": (1, 1200),
            "wall_seconds": (1, 600), "memory_mib": (64, 4096)},
    }
    for section, ranges in simple.items():
        fields(config[section], ranges)
        for key, (minimum, maximum) in ranges.items(): uint(config[section][key], maximum, minimum)
    allowance = config["owner_allowance"]
    ranges = {"operations": (2, 16), "worker_cpu_seconds": (1, 3600),
        "controller_cpu_seconds": (1, 600), "wall_seconds": (1, 3600),
        "output_bytes": (128*MIB, 1024*MIB), "output_entries": (32, 4096)}
    fields(allowance, ("allowance_id", *ranges)); digest(allowance["allowance_id"])
    for key, (minimum, maximum) in ranges.items(): uint(allowance[key], maximum, minimum)
    require(allowance["worker_cpu_seconds"] >= config["author_limits"]["cpu_seconds"]
            +config["snapshot_limits"]["prepare_cpu_seconds"]+config["snapshot_limits"]["cpu_seconds"],
            "INTEGRATION_EXPLICIT_STAGE_RESERVATIONS")


def references(expression):
    """Bounded references in canonical terms, keeping local and external roles."""
    pending, found, visited = [expression], set(), 0
    children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
    while pending:
        node = pending.pop(); visited += 1
        require(visited <= C.DEFAULT_LIMITS.max_nodes, "INTEGRATION_REFERENCE_VISITS")
        if node[0] in ("const", "proj"):
            ref = node[1]
            if ref[0] == "external": found.add((ref[0], ref[1], C.name_key(ref[2])))
            elif ref[0] == "local": found.add((ref[0], "", C.name_key(ref[1])))
        pending.extend(node[index] for index in children[node[0]])
    return found


def inspect_reuse(export_raw, request_raw, child):
    """Evidence check on ACTUAL exported proof, independent of source spelling."""
    exported, request = C.parse_json(export_raw), C.parse_json(request_raw)
    packet = request["context"]
    require(exported["roots"] == request["roots"] == [named("OwnerV5", "fold_map_received")],
            "INTEGRATION_ONE_ORDINARY_ROOT")
    external = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                 "module": item["owner"], "relative_name": d["name"]}
                for item in packet["imports"] for d in item["group"]["declarations"]]
    environment = decode_source(exported["rows"], exported["local_names"],
        packet["foundation_view"]["names"], FOUNDATION, POLICY, external, NATIVE_NAME_LIMITS)
    require(environment.spec == child["input"]["local_spec"]
            and environment.module == child["local_module"], "INTEGRATION_ACTUAL_CHILD_SPEC")
    descriptors = {C.name_key(d["name"]): d for group in environment.spec["groups"]
                   for d in group["declarations"]}
    root = request["roots"][0]; root_key = C.name_key(root)
    declaration = descriptors[root_key]
    require(declaration["kind"] == "theorem", "INTEGRATION_ROOT_IS_THEOREM")
    expected_type = {("external", MODULE, C.name_key(named("CommonsV5", name)))
                     for name in ("Tree", "fold", "map")}
    require(expected_type <= references(declaration["type"]), "INTEGRATION_IMPORTED_TYPE_USE")
    pending, seen, proof_refs, root_proof = [root_key], set(), set(), None
    while pending:
        key = pending.pop()
        if key in seen: continue
        require(key in descriptors and len(seen) < 4096, "INTEGRATION_LOCAL_PROOF_CLOSURE")
        seen.add(key); item = descriptors[key]
        if item["kind"] not in ("theorem", "definition", "opaque"): continue
        commitment = (environment.local_proofs[Address.of(environment.module, item["name"])]
                      if item["kind"] == "theorem" else item["value_hash"])
        raw = environment.bodies[item["universes"], commitment]
        if key == root_key: root_proof = raw
        refs = references(C.parse_json(raw)); proof_refs.update(refs)
        pending.extend(ref[2] for ref in refs if ref[0] == "local")
    require(("external", MODULE, C.name_key(named("CommonsV5", "binary_congr"))) in proof_refs,
            "INTEGRATION_IMPORTED_THEOREM_IN_PROOF_CLOSURE")
    require(root_proof is not None, "INTEGRATION_ROOT_PROOF_PRESENT")
    return {"local_module": environment.module, "local_groups": len(environment.spec["groups"]),
        "local_declarations": len(descriptors), "native_export_rows": len(exported["rows"]),
        "child_rows": len(child["input"]["rows"]), "root": root, "root_proof_sha256": sha(root_proof),
        "proof_value_closure": [C.parse_json(key) for key in sorted(seen)],
        "external_proof_references": [{"module": ref[1], "name": C.parse_json(ref[2])}
                                      for ref in sorted(proof_refs) if ref[0] == "external"],
        "imported_theorem_proof_bytes": 0, "foundation_proofs_separately_supplied": True,
        "scope": "ACTUAL_SOURCE_EXPORT_REFERENCE_EVIDENCE_NOT_CHILD_ADMISSION"}


def run(config_path, config_sha256):
    started, cpu_started = time.monotonic(), time.process_time()
    digest(config_sha256)
    config_path = Path(config_path)
    require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize, "INTEGRATION_OWNER_INVOCATION")
    require(config_path.is_absolute() and config_path.resolve() == config_path
            and config_path.is_file() and 0 < config_path.stat().st_size <= MIB,
            "INTEGRATION_CONFIGURATION_PATH")
    with config_path.open("rb") as stream: config_raw = stream.read(MIB+1)
    require(len(config_raw) <= MIB and sha(config_raw) == config_sha256, "INTEGRATION_CONFIGURATION_PIN")
    config = parse(config_raw); fields(config, CONFIG_FIELDS)
    require(config["schema"] == SCHEMA, "INTEGRATION_CONFIGURATION_SCHEMA")
    uint(config["wall_seconds"], 3600, 1); deadline = started+config["wall_seconds"]
    validate_limits(config)

    def remaining():
        value = math.floor(deadline-time.monotonic())
        require(value >= 1, "INTEGRATION_ORIGINAL_WALL")
        return value

    maxima = {"preparation_profile": MIB, "receipt": 64*MIB, "bundle": 16*MIB,
              "foundation": 16*MIB, "source": 65536, "roots": 65536}
    inputs = {name: read_pin(config[name], maxima[name]) for name in INPUT_NAMES}
    profile = parse(inputs["preparation_profile"]); producer = profile["producer"]
    require((producer["image_id"], producer["foundation"], producer["policy"])
            == (IMAGE, FOUNDATION, POLICY), "INTEGRATION_CURRENT_PROFILE")
    require(sha(inputs["bundle"]) == BUNDLE_SHA and sha(inputs["foundation"]) == FOUNDATION_SHA,
            "INTEGRATION_CURRENT_SEMANTIC_INPUTS")
    self_pin = file_pin(Path(__file__).resolve())
    require(self_pin in profile["source_pins"], "INTEGRATION_LOADED_HARNESS_PIN")
    bundle = C.parse_json(inputs["bundle"])
    C.fields(bundle, {"schema", "module", "spec", "openings", "bodies",
                      "certificate_verification", "mathematical_admission"})
    require(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
            and bundle["certificate_verification"] == "NOT_PERFORMED"
            and bundle["mathematical_admission"] is False, "INTEGRATION_UNTRUSTED_BUNDLE")
    summary = C.summarize(bundle["spec"])
    require(C.summary_id(summary) == bundle["module"] == MODULE
            and summary["foundation"] == FOUNDATION and summary["policy"] == POLICY,
            "INTEGRATION_BASE_SUMMARY")
    source = inputs["source"].decode("utf-8"); roots = C.parse_json(inputs["roots"])
    require(roots == [named("OwnerV5", "fold_map_received")], "INTEGRATION_SELECTED_ROOT")
    output = Path(config["output_directory"])
    require(output.is_absolute() and output.resolve() == output and output.parent.is_dir()
            and not output.exists() and output.is_relative_to(ROOT/"experiments/v5-local-checks"),
            "INTEGRATION_FRESH_OUTPUT")
    protected = [config_path, Path(__file__).resolve().parents[1], Path(profile["lean_root"]),
                 Path(producer["supervisor_manifest"]["path"]).parent]
    protected.extend(pin_fields(config[name]) for name in INPUT_NAMES)
    protected.extend(pin_fields(row) for row in profile["source_pins"]+profile["lean_runtime_pins"])
    protected.extend(pin_fields(profile[name]) for name in ("worker", "image", "native_executable"))
    protected.extend(pin_fields(row) for row in (producer["host"], producer["python"],
        producer["python_dll"], *producer["source_pins"], *producer["runtime_pins"]))
    require(all(not output.is_relative_to(path) and not path.is_relative_to(output)
                for path in protected), "INTEGRATION_OUTPUT_OVERLAP")
    remaining(); output.mkdir(); save(output/"configuration.json", config)
    result = {"schema": SCHEMA, "status": "FAIL", "configuration_sha256": config_sha256,
        "base_receipt_admitted": False, "child_mathematical_admission": False,
        "child_proof_calls": 0, "network_calls": 0, "authority": "LOCAL_INTEGRATION_EVIDENCE_ONLY",
        "input_pins": {name: config[name] for name in INPUT_NAMES}, "error": None}
    verifier = session = operation = owner = None
    try:
        # Validate the ACTUAL loaded source/runtime profile before cryptographic
        # work. The owner remains live over receipt/context preparation as well.
        allowance = {**config["owner_allowance"],
                     "wall_seconds": min(config["owner_allowance"]["wall_seconds"], remaining())}
        owner = OwnerPreparation(profile, allowance, output/"preparation")
        runtime = {row["path"]: {key: row[key] for key in ("bytes", "sha256")}
                   for row in (producer["host"], producer["python"], producer["python_dll"],
                               *producer["runtime_pins"])}
        verifier = ReceiptVerifier(supervisor_manifest=producer["supervisor_manifest"]["path"],
            supervisor_manifest_sha256=producer["supervisor_manifest"]["sha256"],
            executable=producer["host"]["path"], runtime_pins=runtime, image_id=IMAGE,
            foundation=FOUNDATION, policy=POLICY, operations=1, submitted_bytes=len(inputs["receipt"]),
            reserved_cpu_seconds=config["receive_limits"]["cpu_seconds"], wall_seconds=remaining())
        session_caps = {**config["session_limits"],
                        "wall_seconds": min(config["session_limits"]["wall_seconds"], remaining())}
        session = ImportSession(verifier, **session_caps)
        receive_limits = {**config["receive_limits"],
                          "wall_seconds": min(config["receive_limits"]["wall_seconds"], remaining())}
        handle = verifier.receive(inputs["receipt"], summary, output/"receive", **receive_limits)
        module = session.use_handle(handle, inputs["receipt"])
        require(module == MODULE, "INTEGRATION_LIVE_SELECTED_MODULE")
        result["base_receipt_admitted"] = True
        live = verifier.describe(handle)
        opened = set()
        for opening in bundle["openings"]:
            group = session.open_group(module, opening)
            require(group == bundle["spec"]["groups"][opening["index"]]
                    and opening["index"] not in opened, "INTEGRATION_EXACT_BUNDLE_GROUP")
            opened.add(opening["index"])
        require(opened == set(range(summary["group_count"])), "INTEGRATION_COMPLETE_SELECTED_BUNDLE")
        for body in bundle["bodies"]:
            C.fields(body, {"universes", "digest", "expression"})
            require(session.supply_body(module, body["universes"], body["expression"]) == body["digest"],
                    "INTEGRATION_COMMITTED_SEMANTIC_BODY")
        operation = SourceOperation(session, inputs["foundation"], FOUNDATION_SHA, source, roots)
        ready = operation.prepare()
        require(ready["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
                "INTEGRATION_COMPLETE_CONTEXT_REQUIRED")
        request_expected = ready["request"]
        author_limits = {**config["author_limits"],
                         "wall_seconds": min(config["author_limits"]["wall_seconds"], remaining())}
        authored = owner.author(operation, "author", **author_limits)
        require(authored["status"] == "UNTRUSTED_CHILD_REQUEST_PREPARED", "INTEGRATION_AUTHOR_READY_REQUIRED")
        child = authored["child"]
        require(len(child["parent_receipts"]) == 1
                and child["parent_receipts"][0] == {"module": MODULE, "journal": live["journal"],
                                                   "receipt": inputs["receipt"]},
                "INTEGRATION_EXACT_GENUINE_PARENT")
        export = read_pin(authored["export"], 16*MIB)
        request_path = Path(authored["evidence"])/"source-request.json"
        request = read_pin({"path": str(request_path), "bytes": len(request_expected),
                            "sha256": ready["request_sha256"]}, 16*MIB)
        require(request == request_expected, "INTEGRATION_SAME_SOURCE_REQUEST_BYTES")
        result["source_reuse"] = inspect_reuse(export, request, child)
        save(output/"source-reuse.json", result["source_reuse"])
        require(verifier.describe(handle) == live, "INTEGRATION_ORIGINAL_HANDLE_STILL_LIVE")
        snapshot_limits = {**config["snapshot_limits"],
                           "wall_seconds": min(config["snapshot_limits"]["wall_seconds"], remaining())}
        prepared = owner.snapshot(child, "snapshot", **snapshot_limits)
        require(prepared["status"] == "UNTRUSTED_PROVER_CAPSULE_PREPARED"
                and prepared["mathematical_acceptance"] is False
                and prepared["local_module"] == child["local_module"]
                and prepared["session"]["assumptions"] == 1, "INTEGRATION_ONE_PARENT_CAPSULE")
        result["prepared"] = prepared
        result["base_admission"] = {"module": MODULE, "profile_id": live["profile_id"],
            "receipt_sha256": live["receipt_sha256"], "journal_sha256": sha(live["journal"]),
            "persisted_handle": False}
        for name in INPUT_NAMES:
            require(read_pin(config[name], maxima[name]) == inputs[name], "INTEGRATION_INPUT_CHANGED")
        require(config_path.read_bytes() == config_raw, "INTEGRATION_CONFIGURATION_CHANGED")
        remaining()
        result["status"] = "PASS_GENUINE_PARENT_SOURCE_CHILD_SNAPSHOT_NOT_CHILD_CERTIFICATE"
    except BaseException as error:
        result["error"] = {"type": type(error).__name__, "message": str(error)[:4000]}
    finally:
        cleanup_errors = []
        for value, name in ((operation, "operation"), (session, "session"), (verifier, "verifier"), (owner, "owner")):
            if value is not None:
                try: value.close()
                except BaseException as error: cleanup_errors.append({"component": name, "error": str(error)[:1000]})
        result["cleanup_errors"] = cleanup_errors
        if cleanup_errors: result["status"] = "FAIL"
        try:
            if verifier is not None: result["verifier_accounting"] = verifier.report()
            if owner is not None: result["preparation_accounting"] = owner.report()
            process_path = output/"receive/process.json"
            if process_path.is_file():
                with process_path.open("rb") as stream: process_raw = stream.read(MIB+1)
                require(len(process_raw) <= MIB, "INTEGRATION_RECEIVE_REPORT_BOUND")
                process = parse(process_raw)
                result["receive_process"] = process
                result["receive_clean_closure"] = clean(process)
                if result["status"].startswith("PASS_"):
                    require(clean(process), "INTEGRATION_FINAL_RECEIVE_CLOSURE")
            elif result["status"].startswith("PASS_"):
                require(False, "INTEGRATION_MISSING_RECEIVE_PROCESS_EVIDENCE")
            total, entries = 0, 0
            for path in output.rglob("*"):
                entries += 1
                require(path.resolve() == path, "INTEGRATION_EVIDENCE_ALIAS")
                require(entries <= config["owner_allowance"]["output_entries"]+32,
                        "INTEGRATION_EVIDENCE_ENTRIES")
                if path.is_file(): total += path.stat().st_size
                require(total <= config["owner_allowance"]["output_bytes"]+len(inputs["receipt"])+8*MIB,
                        "INTEGRATION_EVIDENCE_BYTES")
            result["sampled_evidence_before_final_report"] = {"bytes": total, "entries": entries}
        except BaseException as error:
            result.update(status="FAIL", accounting_or_evidence_error={
                "type": type(error).__name__, "message": str(error)[:2000]})
        result["owner_process_cpu_seconds"] = time.process_time()-cpu_started
        result["wall_seconds_before_final_report"] = time.monotonic()-started
        result["accounting_scope"] = ("SUM_ACTUAL_RECEIVE_JOB_PLUS_PREPARATION_WORKER_JOB_PLUS_OWNER_PROCESS_CPU;"
            "DO_NOT_ADD_INCLUSIVE_NESTED_CONTROLLER_OR_ENCLOSING_JOB_AGAIN;"
            "UNKNOWN_JOBS_RETAIN_RESERVATIONS;FINAL_REPORT_AND_EXIT_TAILS_EXCLUDED")
        if time.monotonic() >= deadline: result.update(status="FAIL", late_deadline=True)
        try:
            save(output/"RESULT.json", result)
            remaining()
        except BaseException as error:
            result.update(status="FAIL", finalization_error={"type": type(error).__name__,
                          "message": str(error)[:2000]})
            # This marker overrides even a completely written candidate PASS.
            # Failure writing the marker still causes a nonzero caller exit.
            save(output/"FINALIZATION-FAILED.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--config", required=True); parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()
    try:
        result = run(args.config, args.config_sha256)
        print(encoded({key: result.get(key) for key in ("status", "base_receipt_admitted", "error")}).decode(), end="")
        return 0 if result["status"].startswith("PASS_") else 1
    except BaseException as error:
        print(encoded({"status": "FAIL_CONFIGURATION_OR_REPORT", "type": type(error).__name__,
                       "message": str(error)[:4000]}).decode(), end="", file=sys.stderr)
        return 1


if __name__ == "__main__": raise SystemExit(main())
