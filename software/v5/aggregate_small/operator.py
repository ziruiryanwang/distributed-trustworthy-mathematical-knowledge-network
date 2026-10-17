"""Pinned local-owner preflight or one finite production attempt, never admission.

Run with the selected isolated Python (-I -S -B). The enclosing owner must bound
startup, imports, constructor, refusal and finalization. There is no automatic
continuation, allowance renewal, native preflight, or fixture-specific setup.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import sys
import time

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT))
from aggregate_small import producer as S
from production import producer as P

REPORT_LIMIT = P.MIB
SENTINEL_LIMIT = 64*1024


def ordinary(value, *, fresh=False):
    path = Path(value)
    P.require(path.is_absolute() and path.resolve(strict=not fresh) == path,
              "OPERATOR_ABSOLUTE_ORDINARY_PATH")
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            info = part.lstat()
            P.require(not stat.S_ISLNK(info.st_mode)
                      and not (getattr(info, "st_file_attributes", 0) & 0x400),
                      "OPERATOR_REPARSE_PATH")
    if fresh:
        P.require(not path.exists() and not path.is_symlink() and path.parent.is_dir(),
                  "OPERATOR_FRESH_FILE_PARENT")
    else:
        P.require(path.is_file(), "OPERATOR_ORDINARY_FILE")
    return path


def document(value, expected):
    P.digest(expected)
    path = ordinary(value)
    size = path.stat().st_size
    P.require(0 < size <= P.MIB, "OPERATOR_DOCUMENT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(P.MIB+1)
    P.require(len(raw) == size and P.hash_bytes(raw) == expected, "OPERATOR_DOCUMENT_PIN")
    decoded = P.parse(raw)
    P.require(type(decoded) is dict, "OPERATOR_DOCUMENT_OBJECT")
    return decoded, {"path": str(path), "bytes": size, "sha256": expected}


def declared_pins(*documents):
    """Collect only pins; the retained owner validates their actual schemas."""
    pending, result, visited = list(documents), {}, 0
    while pending:
        value = pending.pop(); visited += 1
        P.require(visited <= 100000, "OPERATOR_DOCUMENT_STRUCTURE_BOUND")
        if type(value) is dict:
            if set(value) == {"path", "bytes", "sha256"}:
                path = P.pin_fields(value)
                P.require(str(path) not in result or result[str(path)] == value,
                          "OPERATOR_CONFLICTING_PIN")
                result[str(path)] = dict(value)
            else:
                pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
    return result


def rebind(pins):
    for value in pins.values():
        path = ordinary(value["path"])
        P.require(P.file_pin(path) == value, "OPERATOR_PIN_CHANGED:"+str(path))


def separate(outputs, protected):
    for output in outputs:
        for value in protected:
            path = Path(value)
            P.require(not (output.is_relative_to(path) or path.is_relative_to(output)),
                      "OPERATOR_REPORT_OVERLAP")


def save_new(path, value, maximum):
    raw = P.encoded(value)
    P.require(0 < len(raw) <= maximum, "OPERATOR_REPORT_BOUND")
    ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return {"path": str(path), "bytes": len(raw), "sha256": P.hash_bytes(raw)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "run"))
    parser.add_argument("--profile", required=True)
    parser.add_argument("--profile-sha256", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--owner-report", required=True)
    args = parser.parse_args(argv)
    started, cpu = time.monotonic(), time.process_time()
    owner, output, report_path, sentinel = None, None, None, None
    report_safe, preflight_only, inputs = False, args.command == "preflight", {}
    pins, documents, protected, outcome = {}, {}, [], None
    report = {"schema": "DMKN_SMALL_AGGREGATE_OPERATOR_RESULT_V1", "status": "FAIL",
              "command": args.command, "error": None, "close_error": None,
              "final_binding_error": None, "owner_closed": False,
              "run_calls_attempted": 0, "preflight_request_calls": 0,
              "host_calls_attempted": 0 if preflight_only else None,
              "proof_calls": 0 if preflight_only else None,
              "mathematical_admission": False, "production_result": None,
              "preflight": None, "owner_observation": None,
              "final_binding_validated": False,
              "authority": "LOCAL_OWNER_REPORT_NOT_MATHEMATICAL_OR_FUNDING_AUTHORITY",
              "accounting": "PRE_FINAL_REPORT_PROCESS_CPU_AND_WALL;ENCLOSING_OWNER_MUST_BOUND_STARTUP_IMPORTS_REFUSAL_AND_EXIT"}
    try:
        for name, relative in (("aggregate_small", "aggregate_small/__init__.py"),
                               ("aggregate_small.producer", "aggregate_small/producer.py"),
                               ("production", "production/__init__.py"),
                               ("production.producer", "production/producer.py")):
            module = sys.modules[name]
            P.require(Path(module.__file__).resolve() == SOURCE_ROOT/relative,
                      "OPERATOR_SOURCE_ORIGIN")
        own = P.file_pin(ordinary(__file__))
        pins[own["path"]] = own
        profile, profile_pin = document(args.profile, args.profile_sha256)
        request, request_pin = document(args.request, args.request_sha256)
        documents = {profile_pin["path"]: profile_pin, request_pin["path"]: request_pin}
        P.require(len(documents) == 2, "OPERATOR_DISTINCT_OWNER_DOCUMENTS")
        pins.update(documents)
        declared = declared_pins(profile, request)
        inputs = declared
        output = Path(request["output_directory"])
        P.require(output.is_absolute() and output.resolve(strict=False) == output,
                  "OPERATOR_ABSOLUTE_PRODUCTION_OUTPUT")
        installation = ordinary(P.pin_fields(
            profile["support_profile"]["supervisor_manifest"], 8*P.MIB)).parent
        report_path = ordinary(args.owner_report, fresh=True)
        sentinel = ordinary(report_path.with_name(report_path.name+".FINALIZATION-FAILED.json"), fresh=True)
        protected = [SOURCE_ROOT, installation, output, *pins, *declared]
        separate((report_path, sentinel), protected)
        report_safe = True
        report.update(profile_document=profile_pin, request_document=request_pin, entry_source=own,
                      production_output=str(output), owner_report=str(report_path))
        owner = S.AggregateProducer(profile)
        separate((report_path, sentinel), [owner._install, *owner._pins])
        pins.update(owner._pins)
        if preflight_only:
            report["preflight_request_calls"] = 1
            sid, inputs, inventory, nodes, chosen, prior, envelope = owner._request(request)
            P.require(chosen == output and not output.exists(), "OPERATOR_PREFLIGHT_OUTPUT_UNCREATED")
            separate((report_path, sentinel), inputs)
            report["preflight"] = {
                "profile_id": owner.profile_id, "session_id": sid,
                "segments": request["session"]["segments"], "assumptions": request["session"]["assumptions"],
                "selected_stages": [{"key": key, "dependencies": list(deps)} for key, deps in nodes],
                "retained_checkpoint_count": len(inventory), "prior_allowance_charges": prior,
                "full_path_envelope": envelope,
                "installation_pin_bytes": sum(pin["bytes"] for pin in owner._pins.values()),
                "request_input_bytes": sum(pin["bytes"] for pin in inputs.values()),
                "scope": "VALIDATED_REQUEST_AND_CAP_QUOTE_NOT_FUNDING_MEMORY_SUFFICIENCY_OR_PROOF_COMPLETION"}
            outcome = "PASS_REQUEST_PREFLIGHT_ONLY"
        else:
            # This is the only dispatch entry. Exactly one finite requested prefix.
            report["run_calls_attempted"] = 1
            result = owner.run(request)
            report["production_result"] = P.file_pin(ordinary(output/"RESULT.json"))
            result_raw = P.encoded(result)
            P.require(report["production_result"]["bytes"] == len(result_raw)
                      and report["production_result"]["sha256"] == P.hash_bytes(result_raw),
                      "OPERATOR_EXACT_PRODUCTION_RESULT")
            report["production_status"] = result["status"]
            report["host_calls_attempted"] = result["host_calls_attempted"]
            report["proof_calls"] = result["reported_proof_stage_calls"]
            outcome = ("PASS_ONE_FINITE_ATTEMPT" if result["status"] in
                       ("PASS_SELECTED_PREFIX_ONLY", "PASS_FINISHED_RECEIPT_ARTIFACT") else "FAIL")
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    finally:
        if owner is not None:
            try:
                owner.close()
                report["owner_observation"] = owner.report()
                report["owner_closed"] = report["owner_observation"]["closed"] is True
                P.require(report["owner_closed"], "OPERATOR_OWNER_NOT_CLOSED")
            except BaseException as error:
                report["close_error"] = type(error).__name__+": "+str(error)[:2000]
        try:
            rebind(pins); rebind(inputs)
            if preflight_only and output is not None:
                P.require(not output.exists(), "OPERATOR_PREFLIGHT_OUTPUT_CREATED")
            report["final_binding_validated"] = True
        except BaseException as error:
            report["final_binding_error"] = type(error).__name__+": "+str(error)[:2000]
    if (outcome is not None and report["error"] is None and report["close_error"] is None
            and report["owner_closed"] and report["final_binding_validated"]):
        report["status"] = outcome
    report.update(controller_cpu_seconds_before_report=time.process_time()-cpu,
                  wall_seconds_before_report=time.monotonic()-started)
    try:
        P.require(report_safe, "OPERATOR_NO_SAFE_OWNER_REPORT_PATH")
        separate((report_path, sentinel), [*protected, *pins, *inputs])
        written = save_new(report_path, report, REPORT_LIMIT)
        rebind(pins); rebind(inputs); rebind({written["path"]: written})
        if preflight_only:
            P.require(not output.exists(), "OPERATOR_LATE_PREFLIGHT_OUTPUT_CREATED")
    except BaseException as error:
        report.update(status="FAIL", final_binding_validated=False,
                      final_binding_error=type(error).__name__+": "+str(error)[:2000])
        if report_safe:
            try:
                save_new(sentinel, {"status": "FINALIZATION_FAILED", "overrides_owner_report": True,
                                    "owner_report": str(report_path), "error": report["final_binding_error"]},
                         SENTINEL_LIMIT)
            except BaseException as late:
                report["sentinel_error"] = type(late).__name__+": "+str(late)[:2000]
    print(P.encoded(report).decode("utf-8"), end="", flush=True)
    return 0 if report["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
