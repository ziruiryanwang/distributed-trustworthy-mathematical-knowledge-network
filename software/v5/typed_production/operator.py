"""Pinned typed-owner preflight or one finite attempt; never mathematical admission.

Explicit successor of aggregate_small.operator, reusing its unchanged ordinary
document, pin, separation and durable-report helpers. No owner replacement,
automatic continuation, allowance renewal, build or guest-layout execution.
An enclosing owner bounds startup/imports, construction, refusals and exit.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT))
from aggregate_small import operator as O
from production import producer as P
from typed_production import producer as T


def entry_sources():
    """The full producer closure plus these two command-entry source files."""
    result = list(T.source_paths())
    for module, relative in ((O, "aggregate_small/operator.py"),
                             (sys.modules[__name__], "typed_production/operator.py")):
        expected = SOURCE_ROOT/relative
        P.require(Path(module.__file__).resolve() == expected, "TYPED_OPERATOR_SOURCE_ORIGIN")
        result.append(expected)
    P.require(len(result) == len(set(result)), "TYPED_OPERATOR_DISTINCT_SOURCES")
    return tuple(result)


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
    owner = output = report_path = sentinel = None
    report_safe, preflight_only, inputs = False, args.command == "preflight", {}
    pins, protected, outcome = {}, [], None
    report = {
        "schema": "DMKN_TYPED_AGGREGATE_OPERATOR_RESULT_V1", "status": "FAIL",
        "command": args.command, "error": None, "close_error": None,
        "final_binding_error": None, "owner_closed": False,
        "run_calls_attempted": 0, "preflight_request_calls": 0,
        "host_calls_attempted": 0 if preflight_only else None,
        "proof_calls": 0 if preflight_only else None,
        "mathematical_admission": False, "production_result": None,
        "preflight": None, "owner_observation": None, "final_binding_validated": False,
        "authority": "LOCAL_OWNER_REPORT_NOT_MATHEMATICAL_OR_FUNDING_AUTHORITY",
        "accounting": "PRE_FINAL_REPORT_PROCESS_CPU_AND_WALL;ENCLOSING_OWNER_MUST_BOUND_STARTUP_IMPORTS_REFUSAL_AND_EXIT"}
    try:
        for source in entry_sources():
            pin = P.file_pin(O.ordinary(source))
            pins[pin["path"]] = pin
        own = pins[str(Path(__file__).resolve())]
        profile, profile_pin = O.document(args.profile, args.profile_sha256)
        request, request_pin = O.document(args.request, args.request_sha256)
        documents = {profile_pin["path"]: profile_pin, request_pin["path"]: request_pin}
        P.require(len(documents) == 2, "OPERATOR_DISTINCT_OWNER_DOCUMENTS")
        pins.update(documents)
        declared = O.declared_pins(profile, request)
        inputs = declared
        output = Path(request["output_directory"])
        P.require(output.is_absolute() and output.resolve(strict=False) == output,
                  "OPERATOR_ABSOLUTE_PRODUCTION_OUTPUT")
        support = profile["base_profile"]["support_profile"]
        installation = O.ordinary(P.pin_fields(support["supervisor_manifest"], 8*P.MIB)).parent
        report_path = O.ordinary(args.owner_report, fresh=True)
        sentinel = O.ordinary(report_path.with_name(report_path.name+".FINALIZATION-FAILED.json"), fresh=True)
        protected = [SOURCE_ROOT, installation, output, *pins, *declared]
        O.separate((report_path, sentinel), protected)
        report_safe = True
        report.update(profile_document=profile_pin, request_document=request_pin,
                      entry_source=own, production_output=str(output), owner_report=str(report_path))
        runtime = {str(P.pin_fields(pin)): pin for pin in support["runtime_pins"]}
        P.require(len(runtime) == len(support["runtime_pins"]), "TYPED_OPERATOR_DUPLICATE_RUNTIME")
        for source in entry_sources():
            P.require(runtime.get(str(source)) == pins[str(source)],
                      "TYPED_OPERATOR_SELECTED_SOURCE:"+str(source))
        owner = T.TypedLifecycleProducer(profile)
        O.separate((report_path, sentinel), [owner._install, *owner._pins])
        pins.update(owner._pins)
        if preflight_only:
            report["preflight_request_calls"] = 1
            sid, inputs, inventory, nodes, chosen, prior, envelope = owner._request(request)
            P.require(chosen == output and not output.exists(), "OPERATOR_PREFLIGHT_OUTPUT_UNCREATED")
            O.separate((report_path, sentinel), inputs)
            report["preflight"] = {
                "profile_id": owner.profile_id, "session_id": sid,
                "segments": request["session"]["segments"],
                "assumptions": request["session"]["assumptions"],
                "selected_stages": [{"key": key, "dependencies": list(deps)} for key, deps in nodes],
                "retained_checkpoint_count": len(inventory), "prior_allowance_charges": prior,
                "full_path_envelope": envelope,
                "installation_pin_bytes": sum(pin["bytes"] for pin in owner._pins.values()),
                "request_input_bytes": sum(pin["bytes"] for pin in inputs.values()),
                "scope": "VALIDATED_REQUEST_AND_CAP_QUOTE_NOT_FUNDING_MEMORY_SUFFICIENCY_OR_PROOF_COMPLETION"}
            outcome = "PASS_REQUEST_PREFLIGHT_ONLY"
        else:
            report["run_calls_attempted"] = 1
            result = owner.run(request)
            report["production_result"] = P.file_pin(O.ordinary(output/"RESULT.json"))
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
            O.rebind(pins); O.rebind(inputs)
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
        O.separate((report_path, sentinel), [*protected, *pins, *inputs])
        written = O.save_new(report_path, report, O.REPORT_LIMIT)
        O.rebind(pins); O.rebind(inputs); O.rebind({written["path"]: written})
        if preflight_only:
            P.require(not output.exists(), "OPERATOR_LATE_PREFLIGHT_OUTPUT_CREATED")
    except BaseException as error:
        report.update(status="FAIL", final_binding_validated=False,
                      final_binding_error=type(error).__name__+": "+str(error)[:2000])
        if report_safe:
            try:
                O.save_new(sentinel, {"status": "FINALIZATION_FAILED", "overrides_owner_report": True,
                                      "owner_report": str(report_path), "error": report["final_binding_error"]},
                           O.SENTINEL_LIMIT)
            except BaseException as late:
                report["sentinel_error"] = type(late).__name__+": "+str(late)[:2000]
    print(P.encoded(report).decode("utf-8"), end="", flush=True)
    return 0 if report["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
