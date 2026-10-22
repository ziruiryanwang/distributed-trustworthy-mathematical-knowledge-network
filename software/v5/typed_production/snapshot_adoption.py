"""Narrow adoption of the audited general36 arm, not of failed runs in general.

Exact retained record digests select one already audited execution. Structural
checks explain its usable session and keep the failed optimization screen failed.
Neither these records nor the execution capsule constitute a receipt or admission.
Later arbitrary typed snapshots use aggregate_lifecycle.snapshot, not this grammar.
"""
from pathlib import Path

from production import producer as P
from aggregate_small import producer as S
from aggregate_claims import bindings as B
from .image_adoption import IMAGE_ID

RUN_NAME = "restricted-support-matched-execution-01"
RESULT_SCHEMA = "DMKN_RC_SUPPORT_MATCHED_EXECUTION_RESULT_V1"
# Relative to the actual original outer run directory. All evidence values are
# file pins, because the inherited session identity hashes every value as a pin.
RECORDS = {
    "result": ("pair/RESULT.json", 14872, "07e8840f423f322dda398deb7c83bd9b1eb975935f7547be26ec0c2708144451"),
    "outer": ("RESULT.json", 2293, "a05b2a58bbb3d88eeffa43858e4ad02749b35e904c37e0b4ee5081d460ee6209"),
    "selection": ("selection.json", 16406, "83c64d369149cdc1e2fc840925b215a54ee094ea778810b29e96fb1b543b9235"),
    "configuration": ("../restricted-support-matched-execution-01-configuration.json", 12085,
                      "6afff33289b12bc8d11cd172c50cdc823d1612ee0eac8602d2617ef233687bf4"),
    "derivation": ("pair/derivation.json", 5492, "3156948f6cf3925363b55136f48708c52674b9dc82e8e4d0fe5df84050dd9986"),
    "arm": ("pair/general/arm-result.json", 4061, "a7324dc88040b14bd2797c6ac2b1ce955d52fb7e4affefcea4852b52f40d247b"),
    "command": ("pair/general/command/command.json", 1415, "c969a78647b360130224f4f449c8b8e56d145b971ec1bd5e53416f8adabdcc4a"),
    "job": ("pair/general/host-job.json", 2426, "15317a585ec3343123ab6e087daf7661eac4748903d471d806a16d6b806dc99f"),
    "diagnostic": ("pair/general/diagnostic.json", 10324, "cba882b3f5ec8d60db90794f610500f442fbfce05bda892cbc63cade181041ae"),
    "stdout": ("pair/general/command/stdout.txt", 1411, "a9277c23b92389d89d3381600af057cdc1b66b1b2ea27a4a6f7fc17471cd6211")}
EVIDENCE_FIELDS = tuple(RECORDS)
SESSION_ARTIFACTS = {
    "wire": ("wire.bin", 35720, "478a2b4966fe0fcd3d76901a319a07c3fc1d5f9365b8f772e2d6c9f45915624c"),
    "expected": ("header.bin", 192, "2df5af1a7ded10f5693fb9bff07a7849a67e2a22eaaca39475bf85f96546cd15"),
    "capsule": ("aggregate.snapshot", 6803834, "adaee31aec796ca62c884a747e8617d06a49b702de5d3793496470d26fb36872")}


def evidence_pins(run_directory):
    """Construct fixed expected pins; does not read, create or validate files."""
    run = Path(run_directory)
    P.require(run.is_absolute() and run.name == RUN_NAME, "TYPED_RETAINED_RUN_PATH")
    result = {}
    for role, (relative, size, sha) in RECORDS.items():
        path = run.parent/(RUN_NAME+"-configuration.json") if role == "configuration" else run/relative
        result[role] = {"path": str(path), "bytes": size, "sha256": sha}
    return result


def _bound_records(owner, pins, inputs):
    P.fields(pins, EVIDENCE_FIELDS)
    run = P.pin_fields(pins["outer"], 2*P.MIB).parent
    P.require(P.encoded(pins) == P.encoded(evidence_pins(run)), "TYPED_EXACT_RETAINED_RECORD_PINS")
    records = owner._records(pins, EVIDENCE_FIELDS, inputs)
    P.require(records["result"]["schema"] == RESULT_SCHEMA, "TYPED_RETAINED_RESULT_SCHEMA")
    return run, records


def _session(owner, run, records):
    actual = records["stdout"]
    result = {"image": owner._image, "parents": [records["configuration"]["receipt"]],
        "session_binding": actual["session_binding"], "capsule_binding": actual["capsule_binding"],
        "cycles": 1 << 26, "po2": 18, "segments": 36, "assumptions": 1}
    for role, (name, size, sha) in SESSION_ARTIFACTS.items():
        result[role] = {"path": str(run/"pair/general"/name), "bytes": size, "sha256": sha}
    return P.parse(P.encoded(result))


def session_from_evidence(owner, pins, inputs):
    """Read fixed records to form a request; preflight must still adopt it fully."""
    run, records = _bound_records(owner, pins, inputs)
    return _session(owner, run, records)


def _screen_and_outer(records, pins, run):
    pair, outer, selection = (records[k] for k in ("result", "outer", "selection"))
    P.require(pair["status"] == "FAIL_RC_INVESTMENT_SCREEN" and pair["errors"] == []
              and pair["screen"] == {"no_cpu_regression": True,
                  "padded_rows_at_most_three_quarters": False, "restricted_at_most_64_po18_segments": True}
              and pair["order"] == ["general", "restricted"]
              and pair["proof_calls"] == 0 and type(pair["proof_calls"]) is int
              and all(pair[k] is False for k in ("mathematical_admission", "full_cost_growth_claim", "full_v5_release")),
              "TYPED_INTENTIONAL_INVESTMENT_FAILURE_ONLY")
    P.fields(outer, ("authority", "result", "runtime_scope", "schema", "selection_sha256",
                     "wall_seconds", "wrapper_cpu_seconds"))
    P.fields(selection, ("schema", "name", "sources", "runtime_pins", "argv", "limits"))
    process = outer["result"]
    P.require(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1"
              and selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1" and selection["name"] == RUN_NAME
              and outer["selection_sha256"] == pins["selection"]["sha256"]
              and P.closure_known(process) and process["status"] == "COMMAND_FAILED"
              and type(process["child_exit_code"]) is int and process["child_exit_code"] == 1
              and process["termination_requested"] is False
              and process["final_job"]["terminated_processes"] == 0,
              "TYPED_SCREEN_EXIT1_CLEAN_CLOSURE")
    P.require(process["limits"] == selection["limits"] == {
        "cpu_seconds": 420, "wall_seconds": 600, "memory_mib": 4096,
        "active_processes": 3, "stdout_bytes": P.MIB, "stderr_bytes": P.MIB},
        "TYPED_SCREEN_SELECTED_LIMITS")
    argv = selection["argv"]
    P.require(type(argv) is list and len(argv) == 11 and all(type(x) is str for x in argv)
              and argv[1:4] == ["-I", "-S", "-B"]
              and argv[4] == r"{snapshot}\software\v5\restricted_support_guest\matched_pair.py"
              and argv[5:9] == ["--input", pins["configuration"]["path"], "--input-sha", pins["configuration"]["sha256"]]
              and argv[9:] == ["--output", r"{output}\pair"], "TYPED_SCREEN_EXACT_SELECTED_COMMAND")
    selected = [x.replace("{snapshot}", str(run/"sources")).replace("{output}", str(run)) for x in argv]
    P.require(process["argv"] == selected, "TYPED_SCREEN_ACTUAL_ARGV")
    P.require(P.number(process["final_job"]["cpu_seconds"]) <= selection["limits"]["cpu_seconds"]
              and P.number(outer["wall_seconds"]) <= selection["limits"]["wall_seconds"],
              "TYPED_SCREEN_ACTUAL_LIMITS")
    P.number(outer["wrapper_cpu_seconds"])


def _lineage(owner, records, pins, run, inputs):
    cfg, selection = records["configuration"], records["selection"]
    P.fields(cfg, ("schema", "fixture", "controls", "receipt", "general", "restricted"))
    P.require(cfg["schema"] == "DMKN_RC_SUPPORT_MATCHED_EXECUTION_INPUT_V1"
              and cfg["general"]["host_build"] == owner._snapshot_build_pins,
              "TYPED_RETAINED_SNAPSHOT_HOST_LINEAGE")
    image_roles = {"result": "result", "outer": "outer", "guest_result": "guest_build",
                   "guest_attempt": "guest_attempt"}
    P.require(cfg["general"]["assembly"] == {
        role: owner.profile["image_adoption"][target] for role,target in image_roles.items()},
        "TYPED_RETAINED_IMAGE_LINEAGE")
    runtime = selection["runtime_pins"]
    P.require(type(runtime) is dict and 1 <= len(runtime) <= 256, "TYPED_RETAINED_RUNTIME_MAP")
    originals = [pins["configuration"], cfg["fixture"], cfg["receipt"], owner._snapshot_host, owner._image,
                 *cfg["controls"].values(), *cfg["general"]["host_build"].values(),
                 *cfg["general"]["assembly"].values()]
    for pin in originals:
        P.require(runtime.get(pin["path"]) == pin["sha256"], "TYPED_ORIGINAL_SELECTED_INPUT")
        owner._add(inputs, pin)
    sources = selection["sources"]
    P.require(type(sources) is dict and len(sources) == 17, "TYPED_RETAINED_SOURCE_MAP")
    for relative, sha in sources.items():
        # Source map bytes are fixed by RECORDS; still enforce ordinary local
        # descendants and individual sizes before reading their retained copy.
        P.require(type(relative) is str and not Path(relative).is_absolute()
                  and ".." not in Path(relative).parts, "TYPED_RETAINED_SOURCE_PATH")
        path = owner._A.absolute(run/"sources"/relative)
        P.require(0 < path.stat().st_size <= P.MIB, "TYPED_RETAINED_SOURCE_BYTES")
        pin = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha}
        owner._add(inputs, pin, P.MIB)
    owner._no_override(originals)


def adopt(owner, session, expected, inputs):
    pins = session["snapshot_evidence"]
    run, records = _bound_records(owner, pins, inputs)
    _screen_and_outer(records, pins, run)
    _lineage(owner, records, pins, run, inputs)
    actual_session = _session(owner, run, records)
    P.require(P.encoded({k:v for k,v in session.items() if k != "snapshot_evidence"})
              == P.encoded(actual_session), "TYPED_EXACT_RETAINED_SESSION")
    pair, arm, diagnostic, actual, derivation = (
        records[k] for k in ("result", "arm", "diagnostic", "stdout", "derivation"))
    P.require(type(pair["arms"]) is list and len(pair["arms"]) == 2
              and [row["role"] for row in pair["arms"]] == ["general", "restricted"]
              and P.encoded({k:v for k,v in pair["arms"][0].items()
                             if k != "standalone_known_cpu_with_full_shared_prep"}) == P.encoded(arm)
              and pair["derivation"] == derivation, "TYPED_GENERAL_ARM_RECORD_CHAIN")
    P.require(arm["role"] == "general" and arm["status"] == "PASS_EXACT_EXECUTION_NOT_CERTIFICATE"
              and all(type(arm[k]) is int and arm[k] == v for k,v in {
                  "host_attempts": 1, "guest_execute_calls": 1, "proof_calls": 0}.items())
              and arm["capsule"] == session["capsule"] and arm["diagnostic"] == pins["diagnostic"]
              and arm["header"] == list(expected) and arm["job"] == records["job"],
              "TYPED_COMPLETE_GENERAL_ARM")
    result_expected = {"schema": "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1",
        "status": "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED", "aggregate_image": IMAGE_ID,
        "header": list(expected), "capsule_path": session["capsule"]["path"],
        "capsule_bytes": session["capsule"]["bytes"], "capsule_sha256": session["capsule"]["sha256"],
        "capsule_binding": session["capsule_binding"], "session_binding": session["session_binding"],
        "segments": 36, "assumptions": 1, "mathematical_admission": False,
        "proof_calls": 0, "guest_execute_calls": 1}
    P.fields(actual, result_expected)
    P.require(owner.support["image_id"] == IMAGE_ID and all(type(actual[k]) is type(v)
              and actual[k] == v for k,v in result_expected.items())
              and all(type(x) is int for x in actual["header"]), "TYPED_EXACT_NATIVE_RESULT")
    P.require(diagnostic["schema"] == "DMKN_SMALL_AGGREGATE_EXECUTION_DIAGNOSTIC_V1"
              and diagnostic["status"] == "CAPSULE_RETAINED_NOT_CERTIFICATE" and diagnostic["error"] is None
              and diagnostic["result"] == actual and diagnostic["aggregate_image"] == IMAGE_ID
              and diagnostic["header"] == list(expected)
              and diagnostic["elf_sha256"] == session["image"]["sha256"]
              and diagnostic["wire_bytes"] == session["wire"]["bytes"]
              and diagnostic["wire_sha256"] == session["wire"]["sha256"]
              and diagnostic["cycles_cap"] == session["cycles"] and diagnostic["segment_po2"] == 18
              and diagnostic["guest_execute_calls"] == 1 and diagnostic["proof_calls"] == 0
              and diagnostic["mathematical_admission"] is False, "TYPED_EXACT_EXECUTION_DIAGNOSTIC")
    general = derivation["arms"]["general"]
    P.require(derivation["schema"] == "DMKN_RC_SAME_TARGET_PREPARATION_V1"
              and general == {"image": IMAGE_ID, "wire_bytes": session["wire"]["bytes"],
                  "wire_sha256": session["wire"]["sha256"], "header": list(expected),
                  "header_sha256": session["expected"]["sha256"]}
              and diagnostic["parents"] == [{**session["parents"][0], "image": B.RELATION_IMAGE,
                  "journal_sha256": P.hash_bytes(bytes(derivation["parent_journal"]))}]
              and derivation["parent_receipt_bytes"] == session["parents"][0]["bytes"]
              and derivation["parent_receipt_sha256"] == session["parents"][0]["sha256"],
              "TYPED_EXACT_HEADER_AND_PARENT_DERIVATION")
    stats, segments = diagnostic["session_stats"], diagnostic["retained_segments"]
    P.require(stats == {"instruction_count": 10202450, "padding_row_count": 872949,
                       "row_count": 9240576, "segment_count": 36}
              and len(segments) == 36 and [s["index"] for s in segments] == list(range(36))
              and [s["po2"] for s in segments] == [18]*35+[16]
              and sum(s["rows"] for s in segments) == stats["row_count"]
              and sum(s["bytes"] for s in segments) == diagnostic["retained_segment_bytes"] == 6803397,
              "TYPED_COMPLETE_GENERAL36_GEOMETRY")
    command, process = records["command"], records["job"]
    P.fields(command, ("argv", "cwd", "limits"))
    argv = [owner._snapshot_host["path"], "snapshot", IMAGE_ID, session["image"]["path"],
        session["wire"]["path"], session["expected"]["path"], str(1 << 26), "18", "stats",
        session["capsule"]["path"], pins["diagnostic"]["path"], "1", session["parents"][0]["path"]]
    P.require(command["argv"] == argv and command["limits"] == {
        "cpu_seconds": 180, "wall_seconds": 120, "memory_mib": 3072,
        "active_processes": 2, "stdout_bytes": P.MIB, "stderr_bytes": P.MIB}
        and P.clean(process) and P.encoded(command) == P.encoded({k:process[k] for k in command})
        and command["cwd"] == records["outer"]["result"]["cwd"], "TYPED_ACTUAL_GENERAL_COMMAND")
    P.require(P.number(process["final_job"]["cpu_seconds"]) <= command["limits"]["cpu_seconds"]
              and P.number(arm["wall_seconds"]) <= command["limits"]["wall_seconds"],
              "TYPED_GENERAL_ACTUAL_LIMITS")
    # Segment custody files are not inputs to resumed stage production: the
    # complete exact capsule already embeds every retained segment.
    for role, maximum in (("wire", 16*P.MIB), ("expected", 192), ("capsule", S.CAPSULE_LIMIT)):
        owner._add(inputs, session[role], maximum)
    for parent in session["parents"]:
        owner._add(inputs, parent, S.PARENT_LIMIT)
    empties = (run/"command/stderr.txt", run/"pair/general/command/stderr.txt")
    for path in empties:
        owner._A.absolute(path)
        P.require(path.stat().st_size == 0, "TYPED_RETAINED_EMPTY_STDERR")
    owner._refinement_empty_evidence = tuple(dict.fromkeys(
        (*getattr(owner, "_refinement_empty_evidence", ()), *empties)))
    owner._check(inputs)
    owner._no_override(pins.values())
    owner._no_override(owner._snapshot_build_pins.values())
