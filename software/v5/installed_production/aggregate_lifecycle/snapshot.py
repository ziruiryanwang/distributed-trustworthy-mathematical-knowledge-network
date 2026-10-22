"""Generic snapshot staging/execution/adoption, never mathematical admission.

Original packet/profile/configuration are selected input pins. Wire, header and
ordered receipts are newly staged data bound by a manifest, NOT fictitious prior
outer runtime pins. Actual native receipt checking and guest execution are unchanged.
"""
from __future__ import annotations

from dataclasses import asdict
import math
import os
from pathlib import Path
import subprocess
import time

from aggregate_small import producer as S
from production import producer as P
from aggregate_claims.prepare_mixed import PreparedSeal, prepare_mixed_seal
from mixed_claims.packet import Envelope

CONFIG_SCHEMA = "DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_REQUEST_V1"
RESULT_SCHEMA = "DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_RESULT_V1"
STAGING_SCHEMA = "DMKN_AGGREGATE_LIFECYCLE_STAGING_V1"
COMMAND_SCHEMA = "DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_COMMAND_V1"
PASS = "PASS_ONE_GENERIC_EXECUTION_CAPSULE_ONLY"
EVIDENCE_FIELDS = ("result", "outer", "selection", "configuration", "command")
CEILINGS = {"worker_cpu_seconds": 180, "controller_cpu_seconds": 60, "wall_seconds": 240,
    "memory_mib": 3072, "active_processes": 2, "stdout_bytes": P.MIB, "stderr_bytes": P.MIB,
    "output_bytes": 208*P.MIB, "output_entries": 288}
REPORT_FIELDS = ("schema", "status", "profile_id", "configuration", "selection", "staging",
    "command", "actual_result", "session", "diagnostic", "process", "worker_cpu_charge",
    "closure_accounting_known", "host_calls_attempted", "proof_calls", "mathematical_admission",
    "final_binding_validated", "error", "final_binding_error", "controller_cpu_seconds",
    "wall_seconds", "output_census", "authority", "accounting")
SESSION_FIELDS = ("image", "wire", "expected", "capsule", "parents", "session_binding",
                  "capsule_binding", "cycles", "po2", "segments", "assumptions")


def _doc(owner, pin, maximum=P.MIB):
    return P.parse(owner._read(pin, maximum))


def _save(owner, path, raw, maximum):
    P.require(type(raw) is bytes and 0 < len(raw) <= maximum, "LIFECYCLE_SAVED_BYTES")
    owner._A.absolute(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    pin = P.file_pin(path)
    P.require(pin["bytes"] == len(raw) and pin["sha256"] == P.hash_bytes(raw), "LIFECYCLE_SAVE_PIN")
    return pin


def _config(owner, pin, table):
    owner._add(table, pin, P.MIB)
    value = _doc(owner, pin)
    P.fields(value, ("schema", "profile_id", "profile_document", "packet", "target_journal",
                     "envelope", "cycles", "po2", "diagnostic_mode", "limits", "output_directory"))
    P.require(value["schema"] == CONFIG_SCHEMA and value["profile_id"] == owner.profile_id,
              "LIFECYCLE_SNAPSHOT_CONFIGURATION")
    owner._add(table, value["profile_document"], P.MIB)
    P.require(P.encoded(_doc(owner, value["profile_document"])) == owner._lifecycle_raw,
              "LIFECYCLE_EXACT_PROFILE_DOCUMENT")
    P.fields(value["envelope"], asdict(Envelope()))
    envelope = Envelope(**value["envelope"]); envelope.validate()
    target = value["target_journal"]
    P.require(type(target) is str and len(target) == 368
              and all(c in "0123456789abcdef" for c in target), "LIFECYCLE_TARGET_HEX")
    P.uint(value["cycles"], 1 << 26, 1)
    P.require(type(value["po2"]) is int and value["po2"] == 18
              and value["diagnostic_mode"] == "stats", "LIFECYCLE_FIXED_GEOMETRY_AND_MODE")
    P.fields(value["limits"], CEILINGS)
    for key, cap in CEILINGS.items():
        P.uint(value["limits"][key], cap, 1)
    owner._add(table, value["packet"], envelope.packet_bytes)
    raw = owner._read(value["packet"], envelope.packet_bytes)
    prepared = prepare_mixed_seal(raw, bytes.fromhex(target),
        adopted_image=owner.support["image_id"], envelope=envelope)
    P.require(prepared.census.maximum_parent_receipt_bytes <= S.PARENT_LIMIT
              and prepared.census.claims <= S.ASSUMPTION_LIMIT
              and prepared.census.wire_bytes <= 16*P.MIB, "LIFECYCLE_PRODUCER_INPUT_BOUNDS")
    output = Path(value["output_directory"])
    P.require(output.is_absolute() and output.resolve(strict=False) == output, "LIFECYCLE_OUTPUT_PATH")
    return value, prepared, output


def _selection(owner, pin, configuration, cfg, table):
    owner._add(table, pin, P.MIB)
    value = _doc(owner, pin)
    P.fields(value, ("schema", "name", "sources", "runtime_pins", "argv", "limits"))
    P.require(value["schema"] == "DMKN_V5_LOCAL_CHECK_V1", "LIFECYCLE_OUTER_SELECTION")
    runtime = value["runtime_pins"]
    P.require(type(runtime) is dict and 1 <= len(runtime) <= 256, "LIFECYCLE_RUNTIME_PIN_MAP")
    for item in [configuration, cfg["profile_document"], cfg["packet"], *owner._pins.values()]:
        P.require(runtime.get(item["path"]) == item["sha256"], "LIFECYCLE_SELECTED_ORIGINAL_INPUT")
    P.require(type(value["argv"]) is list and all(type(x) is str for x in value["argv"]),
              "LIFECYCLE_OUTER_ARGV")
    return value


def staging(prepared, profile_id, cfg_pin, selection_pin, output, image):
    """Expected data-only staged manifest; file contents are independently checked."""
    def future(name, raw):
        return {"path": str(output/name), "bytes": len(raw), "sha256": P.hash_bytes(raw)}
    return {"schema": STAGING_SCHEMA, "profile_id": profile_id,
        "configuration": cfg_pin, "selection": selection_pin,
        "packet": {"bytes": prepared.input_bytes, "sha256": prepared.input_sha256},
        "target_journal": prepared.target_journal.hex(), "image": image,
        "wire": future("wire.bin", prepared.wire), "expected": future("header.bin", prepared.expected_header),
        "parents": [{"tag": parent.tag, "statement": parent.statement.hex(),
            "file": future("parent-"+str(index)+".bin", parent.receipt)}
            for index,parent in enumerate(prepared.parents)],
        "members": [member.hex() for member in prepared.members], "target_index": prepared.target_index,
        "target_siblings": [s.hex() for s in prepared.target_siblings],
        "selected_claim_indices": list(prepared.selected_claim_indices),
        "selected_frontier_indices": list(prepared.selected_frontier_indices),
        "selected_delta_indices": list(prepared.selected_delta_indices),
        "census": asdict(prepared.census), "mathematical_admission": False}


def _staged_pins(manifest):
    return [manifest["wire"], manifest["expected"], *[p["file"] for p in manifest["parents"]]]


def _command(owner, cfg, manifest, staging_pin, output, limits):
    argv = [owner._snapshot_host["path"], "snapshot", owner.support["image_id"],
        owner._image["path"], manifest["wire"]["path"], manifest["expected"]["path"],
        str(cfg["cycles"]), "18", "stats", str(output/"aggregate.snapshot"),
        str(output/"diagnostic.json"), str(len(manifest["parents"])),
        *[p["file"]["path"] for p in manifest["parents"]]]
    P.require(len(argv) == 12+len(manifest["parents"])
              and all(type(x) is str and "\0" not in x for x in argv)
              and len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2+1 <= 32767,
              "LIFECYCLE_SNAPSHOT_ARGV")
    return {"schema": COMMAND_SCHEMA, "argv": argv, "cwd": str(owner._install),
            "limits": limits, "staging": staging_pin, "authority": "ONE_LAYOUT_NO_PROOF_OR_ADMISSION"}


def _host_limits(cfg, wall):
    limits = cfg["limits"]
    P.uint(wall, limits["wall_seconds"], 1)
    return {"cpu_seconds": limits["worker_cpu_seconds"], "wall_seconds": wall,
        **{k:limits[k] for k in ("memory_mib", "active_processes", "stdout_bytes", "stderr_bytes")}}


def _actual(value, owner, cfg, manifest, capsule, output):
    P.fields(value, ("schema", "status", "aggregate_image", "header", "capsule_path", "capsule_bytes",
        "capsule_sha256", "capsule_binding", "session_binding", "segments", "assumptions",
        "mathematical_admission", "proof_calls", "guest_execute_calls"))
    expected = {"schema": "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1",
        "status": "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED",
        "aggregate_image": owner.support["image_id"],
        "header": list(owner._read(manifest["expected"], 192)),
        "capsule_path": str(output/"aggregate.snapshot"), "capsule_bytes": capsule["bytes"],
        "capsule_sha256": capsule["sha256"], "assumptions": len(manifest["parents"]),
        "mathematical_admission": False, "proof_calls": 0, "guest_execute_calls": 1}
    P.require(all(type(value[k]) is type(v) and value[k] == v for k,v in expected.items())
              and all(type(x) is int for x in value["header"]), "LIFECYCLE_EXACT_NATIVE_RESULT")
    P.uint(value["segments"], S.SEGMENT_LIMIT, 1)
    P.digest(value["capsule_binding"]); P.digest(value["session_binding"])
    P.require(P.pin_fields(capsule, S.CAPSULE_LIMIT) == output/"aggregate.snapshot",
              "LIFECYCLE_EXACT_CAPSULE_PATH")
    return {"image": owner._image, "wire": manifest["wire"], "expected": manifest["expected"],
        "capsule": capsule, "parents": [p["file"] for p in manifest["parents"]],
        "session_binding": value["session_binding"], "capsule_binding": value["capsule_binding"],
        "cycles": cfg["cycles"], "po2": 18, "segments": value["segments"], "assumptions": value["assumptions"]}


def _census(owner, output, limits, reserve=0, entries=0):
    size, count = 0, 0
    for directory, dirs, files in os.walk(output, followlinks=False):
        for name in dirs+files:
            path = Path(directory)/name
            owner._A.absolute(path, directory=name in dirs)
            count += 1
            if name in files: size += path.stat().st_size
            P.require(size+reserve <= limits["output_bytes"] and count+entries <= limits["output_entries"],
                      "LIFECYCLE_OUTPUT_CENSUS")
    P.require(size+reserve <= limits["output_bytes"] and count+entries <= limits["output_entries"],
              "LIFECYCLE_OUTPUT_RESERVE")
    return {"bytes": size+reserve, "entries": count+entries,
            "scope": "SAMPLED_CENSUS_WITH_RESERVED_FINAL_REPORT_NOT_FILESYSTEM_QUOTA"}


def _fixed_bound(owner, pins, generated):
    # Reserve 8MiB diagnostics, 1MiB result, 2MiB outer, 1MiB staging,
    # plus bounded command/native-stdout records before layout. Config, selection,
    # original packet and profile document are already in pins.
    total = dict(pins)
    total[owner._image["path"]] = owner._image
    for pin in generated: total[pin["path"]] = pin
    P.require(sum(p["bytes"] for p in total.values())+14*P.MIB <= S.FIXED_INPUT_LIMIT,
              "LIFECYCLE_FIXED_SESSION_INPUT_RESERVE")


def execute(owner, prepared, configuration, selection, started, cpu):
    inputs = {}
    owner._check(owner._pins)
    cfg, derived, output = _config(owner, configuration, inputs)
    P.require(type(prepared) is PreparedSeal and prepared == derived, "LIFECYCLE_EXACT_PREPARATION")
    owner._snapshot_selection(selection, configuration, cfg, inputs)
    owner._A.absolute(output, directory=True, fresh=True)
    P.require(output.parent.is_dir(), "LIFECYCLE_OUTPUT_PARENT")
    for path in [owner._install, *map(Path, owner._pins), *map(Path, inputs)]:
        P.require(not owner._A.overlap(output, path), "LIFECYCLE_OUTPUT_OVERLAP")
    manifest = staging(derived, owner.profile_id, configuration, selection, output, owner._image)
    generated = _staged_pins(manifest)
    _fixed_bound(owner, inputs, generated)
    limits = cfg["limits"]
    # Both segment custody and complete capsule have independent 96MiB ceilings.
    reserve = 2*S.CAPSULE_LIMIT+8*P.MIB+sum(p["bytes"] for p in generated)+2*P.MIB
    reserve += limits["stdout_bytes"]+limits["stderr_bytes"]
    P.require(reserve <= limits["output_bytes"] and 276+len(derived.parents) <= limits["output_entries"],
              "LIFECYCLE_WORST_CASE_OUTPUT_RESERVE")
    deadline = started+limits["wall_seconds"]
    report = {"schema": RESULT_SCHEMA, "status": "FAIL", "profile_id": owner.profile_id,
        "configuration": configuration, "selection": selection, "staging": None, "command": None,
        "actual_result": None, "session": None, "diagnostic": None, "process": None,
        "worker_cpu_charge": 0, "closure_accounting_known": True, "host_calls_attempted": 0,
        "proof_calls": 0, "mathematical_admission": False, "final_binding_validated": False,
        "error": None, "final_binding_error": None, "controller_cpu_seconds": 0, "wall_seconds": 0,
        "output_census": None, "authority": "LOCAL_OWNER_CAPSULE_NOT_CERTIFICATE_OR_FUNDING",
        "accounting": "INCLUSIVE_WORKER_PLUS_PRE_REPORT_CONTROLLER;ENCLOSING_OWNER_BOUNDS_ALL_TAILS"}

    def active():
        P.require(time.monotonic() <= deadline and time.process_time()-cpu <= limits["controller_cpu_seconds"],
                  "LIFECYCLE_SNAPSHOT_TIME_LIMIT")

    def rebind():
        active(); owner._check(owner._pins); owner._check(inputs)
        owner._no_override(owner.profile["host_build"].values())
        owner._no_override(owner.profile["image_adoption"].values()); active()

    rebind(); output.mkdir(); owner._attempt_open = True
    try:
        for item, raw in [(manifest["wire"], derived.wire), (manifest["expected"], derived.expected_header),
                          *[(row["file"], parent.receipt) for row,parent in zip(manifest["parents"],derived.parents)]]:
            P.require(_save(owner, Path(item["path"]), raw, 16*P.MIB) == item, "LIFECYCLE_STAGED_EXACT_BYTES")
            owner._add(inputs, item, 16*P.MIB)
        report["staging"] = _save(owner, output/"staging.json", P.encoded(manifest), P.MIB)
        owner._add(inputs, report["staging"], P.MIB)
        host_limits = _host_limits(cfg, math.floor(deadline-time.monotonic()))
        command = _command(owner, cfg, manifest, report["staging"], output, host_limits)
        report["command"] = _save(owner, output/"COMMAND.json", P.encoded(command), 64*1024)
        owner._add(inputs, report["command"], 64*1024)
        rebind(); _census(owner, output, limits, 2*P.MIB, 2)
        report["worker_cpu_charge"] = host_limits["cpu_seconds"]
        report["host_calls_attempted"] = 1
        try:
            process = owner._A.supervise(command["argv"], owner._install, output/"command", host_limits, owner._Job)
        except BaseException:
            report["closure_accounting_known"] = False; owner._closed = True
            raise
        report["process"] = process
        known = P.closure_known(process)
        if known:
            try:
                actual_cpu = P.number(process["final_job"]["cpu_seconds"])
            except (KeyError, ValueError, TypeError):
                known = False
        report["closure_accounting_known"] = known
        if known:
            report["worker_cpu_charge"] = actual_cpu
        else:
            owner._closed = True
        P.require(known and P.clean(process) and process["argv"] == command["argv"]
                  and process["cwd"] == command["cwd"] and process["limits"] == host_limits,
                  "LIFECYCLE_SNAPSHOT_CLEAN_EXACT_COMMAND")
        P.require(actual_cpu <= host_limits["cpu_seconds"], "LIFECYCLE_SNAPSHOT_WORKER_CPU")
        stdout = owner._A.bounded_read(output/"command/stdout.txt", host_limits["stdout_bytes"])
        capsule = P.file_pin(owner._A.absolute(output/"aggregate.snapshot"))
        actual = P.parse(stdout)
        owner._add(inputs, P.file_pin(output/"command/stdout.txt"), host_limits["stdout_bytes"])
        invocation = P.file_pin(output/"command/command.json")
        P.require(P.encoded(_doc(owner, invocation, 64*1024)) ==
                  P.encoded({k: command[k] for k in ("argv", "cwd", "limits")}),
                  "LIFECYCLE_ACTUAL_SAVED_INVOCATION")
        owner._add(inputs, invocation, 64*1024)
        report["session"] = _actual(actual, owner, cfg, manifest, capsule, output)
        report["actual_result"] = actual
        report["diagnostic"] = P.file_pin(owner._A.absolute(output/"diagnostic.json"))
        P.pin_fields(report["diagnostic"], 8*P.MIB)
        owner._add(inputs, capsule, S.CAPSULE_LIMIT)
        owner._add(inputs, report["diagnostic"], 8*P.MIB)
        rebind(); _census(owner, output, limits, 2*P.MIB, 2)
        report["status"] = PASS
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    try:
        rebind()
        report["output_census"] = _census(owner, output, limits, 2*P.MIB, 2)
        report["final_binding_validated"] = True
    except BaseException as error:
        report.update(status="FAIL", final_binding_error=type(error).__name__+": "+str(error)[:2000])
    report.update(controller_cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-started)
    P.fields(report, REPORT_FIELDS)
    try:
        saved = _save(owner, output/"RESULT.json", P.encoded(report), P.MIB)
        rebind(); owner._check({saved["path"]: saved}); _census(owner, output, limits)
    except BaseException as error:
        owner._closed = True
        _save(owner, output/"FINALIZATION-FAILED.json", P.encoded({"status": "FINALIZATION_FAILED",
            "overrides_result": True, "error": type(error).__name__+": "+str(error)[:2000]}), 64*1024)
        raise
    owner._attempt_open = False
    return P.parse(P.encoded(report))


def result_shape(result, profile_id):
    P.fields(result, REPORT_FIELDS)
    P.require(result["schema"] == RESULT_SCHEMA and result["status"] == PASS
              and result["profile_id"] == profile_id and result["final_binding_validated"] is True
              and result["closure_accounting_known"] is True
              and type(result["host_calls_attempted"]) is int and result["host_calls_attempted"] == 1
              and type(result["proof_calls"]) is int and result["proof_calls"] == 0
              and result["mathematical_admission"] is False
              and result["error"] is None and result["final_binding_error"] is None,
              "LIFECYCLE_COMPLETED_SNAPSHOT_ONLY")
    P.fields(result["session"], SESSION_FIELDS)


def adopt(owner, session, expected, inputs):
    pins = session["snapshot_evidence"]
    P.fields(pins, EVIDENCE_FIELDS)
    for role, maximum in (("result", P.MIB), ("outer", 2*P.MIB), ("selection", P.MIB),
                          ("configuration", P.MIB), ("command", 64*1024)):
        P.pin_fields(pins[role], maximum)
    records = owner._records(pins, EVIDENCE_FIELDS, inputs)
    result = records["result"]
    result_shape(result, owner.profile_id)
    cfg, prepared, output = _config(owner, pins["configuration"], inputs)
    owner._snapshot_selection(pins["selection"], pins["configuration"], cfg, inputs)
    owner._local_outer(records["outer"], records["selection"], pins["selection"], pins["outer"])
    P.require(result["configuration"] == pins["configuration"] and result["selection"] == pins["selection"]
              and result["command"] == pins["command"] and Path(pins["result"]["path"]) == output/"RESULT.json"
              and Path(pins["command"]["path"]) == output/"COMMAND.json", "LIFECYCLE_EVIDENCE_PATHS")
    owner._A.absolute(output, directory=True)
    owner._add(inputs, result["staging"], P.MIB)
    P.require(Path(result["staging"]["path"]) == output/"staging.json", "LIFECYCLE_STAGING_PATH")
    manifest = _doc(owner, result["staging"])
    P.require(P.encoded(manifest) == P.encoded(staging(prepared, owner.profile_id,
        pins["configuration"], pins["selection"], output, owner._image)), "LIFECYCLE_EXACT_STAGING_MANIFEST")
    for pin in _staged_pins(manifest): owner._add(inputs, pin, 16*P.MIB)
    P.require(expected == prepared.expected_header, "LIFECYCLE_EXPECTED_TARGET_HEADER")
    process, command = result["process"], records["command"]
    P.require(type(process) is dict and P.clean(process), "LIFECYCLE_SNAPSHOT_PROCESS_CLOSURE")
    limits = command.get("limits", {})
    P.fields(limits, ("cpu_seconds", "wall_seconds", "memory_mib", "active_processes", "stdout_bytes", "stderr_bytes"))
    P.require(P.encoded(limits) == P.encoded(_host_limits(cfg, limits["wall_seconds"]))
              and P.encoded(command) == P.encoded(_command(owner, cfg, manifest, result["staging"], output, limits))
              and process["argv"] == command["argv"] and process["cwd"] == command["cwd"]
              and P.encoded(process["limits"]) == P.encoded(limits), "LIFECYCLE_EXACT_STAGED_COMMAND")
    capsule = session["capsule"]
    actual_session = _actual(result["actual_result"], owner, cfg, manifest, capsule, output)
    P.require(P.encoded(actual_session) == P.encoded(result["session"])
              and P.encoded({k:v for k,v in session.items() if k != "snapshot_evidence"}) == P.encoded(actual_session),
              "LIFECYCLE_EXACT_COMPLETED_SESSION")
    stdout = owner._A.bounded_read(output/"command/stdout.txt", limits["stdout_bytes"])
    P.require(P.encoded(P.parse(stdout)) == P.encoded(result["actual_result"]), "LIFECYCLE_ACTUAL_STDOUT")
    owner._add(inputs, P.file_pin(output/"command/stdout.txt"), limits["stdout_bytes"])
    invocation = P.file_pin(output/"command/command.json")
    P.require(P.encoded(_doc(owner, invocation, 64*1024)) ==
              P.encoded({k: command[k] for k in ("argv", "cwd", "limits")}),
              "LIFECYCLE_ACTUAL_SAVED_INVOCATION")
    owner._add(inputs, invocation, 64*1024)
    owner._add(inputs, result["diagnostic"], 8*P.MIB)
    P.require(Path(result["diagnostic"]["path"]) == output/"diagnostic.json", "LIFECYCLE_DIAGNOSTIC_PATH")
    for key in ("worker_cpu_charge", "controller_cpu_seconds", "wall_seconds"):
        P.number(result[key])
    P.require(result["worker_cpu_charge"] == process["final_job"]["cpu_seconds"]
              and result["worker_cpu_charge"] <= cfg["limits"]["worker_cpu_seconds"]
              and result["controller_cpu_seconds"] <= cfg["limits"]["controller_cpu_seconds"]
              and result["wall_seconds"] <= cfg["limits"]["wall_seconds"], "LIFECYCLE_ACTUAL_COST_LIMITS")
    observed = _census(owner, output, cfg["limits"])
    census = result["output_census"]
    P.fields(census, ("bytes", "entries", "scope"))
    P.uint(census["bytes"], cfg["limits"]["output_bytes"])
    P.uint(census["entries"], cfg["limits"]["output_entries"])
    P.require(census["scope"] == observed["scope"] and observed["bytes"] <= census["bytes"]
              and observed["entries"] <= census["entries"], "LIFECYCLE_FINAL_CENSUS_RESERVE")
    owner._check(inputs)
    owner._no_override(pins.values())
    owner._no_override((result["staging"],))
