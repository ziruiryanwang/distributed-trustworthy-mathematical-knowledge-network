"""Explicit release-owned snapshot/request/preflight/run commands.

Derived from the reviewed typed lifecycle entry. Each invocation performs one
selected action only. Only run dispatches finite proof stages. No action chooses
funding, retries, builds a release or constitutes mathematical acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
from importlib import import_module
import importlib.machinery
import json
import os
from pathlib import Path
import stat
import sys
import time
from types import SimpleNamespace

MIB = 1024**2
PUBLIC_ENTRY_REPORT_LIMIT = 64*1024
REQUEST_SCHEMA = "DMKN_RELEASE_LIFECYCLE_REQUEST_ENTRY_V1"
REPORT_SCHEMA = "DMKN_RELEASE_LIFECYCLE_OPERATOR_RESULT_V1"
PRODUCER_MODULES = (
    "aggregate_lifecycle", "aggregate_lifecycle.producer", "aggregate_lifecycle.snapshot",
    "aggregate_small", "aggregate_small.producer", "production", "production.producer",
    "aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
    "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec", "release_production", "release_production.producer",
    "release_production.adoption", "admission.pin_phase", "admission.trust",
    "admission.clean_refusal", "release_production.launch_contract")
IMPORT_MODULES = (*PRODUCER_MODULES, "aggregate_small.operator")


def _need(ok, reason):
    if not ok:
        raise ValueError(reason)


def _digest(value):
    _need(type(value) is str and len(value) == 64
          and all(c in "0123456789abcdef" for c in value), "LIFECYCLE_ENTRY_DIGEST")
    return value


def _ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    _need(path.is_absolute() and path.resolve(strict=not fresh) == path,
          "LIFECYCLE_ENTRY_ORDINARY_PATH")
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            info = part.lstat()
            _need(not stat.S_ISLNK(info.st_mode)
                  and not (getattr(info, "st_file_attributes", 0) & 0x400),
                  "LIFECYCLE_ENTRY_REPARSE_PATH")
    if fresh:
        _need(not path.exists() and path.parent.is_dir(), "LIFECYCLE_ENTRY_FRESH_PARENT")
    else:
        _need(path.is_dir() if directory else path.is_file(), "LIFECYCLE_ENTRY_PATH_KIND")
    return path


def _read_pin(row, maximum=MIB):
    _need(type(row) is dict and set(row) == {"path", "bytes", "sha256"},
          "LIFECYCLE_ENTRY_PIN_FIELDS")
    _digest(row["sha256"])
    _need(type(row["path"]) is str and type(row["bytes"]) is int
          and 0 < row["bytes"] <= maximum, "LIFECYCLE_ENTRY_PIN_BOUND")
    path = _ordinary(row["path"])
    _need(path.stat().st_size == row["bytes"], "LIFECYCLE_ENTRY_PIN_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(row["bytes"]+1)
    _need(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
          "LIFECYCLE_ENTRY_PIN_CHANGED")
    return raw


def _pin_document(path, expected=None, maximum=MIB):
    path = _ordinary(path)
    size = path.stat().st_size
    _need(0 < size <= maximum, "LIFECYCLE_ENTRY_DOCUMENT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    _need(len(raw) == size, "LIFECYCLE_ENTRY_DOCUMENT_CHANGED")
    actual = hashlib.sha256(raw).hexdigest()
    if expected is not None:
        _need(actual == _digest(expected), "LIFECYCLE_ENTRY_DOCUMENT_PIN")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            _need(key not in result, "LIFECYCLE_ENTRY_DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def constant(unused):
        raise ValueError("LIFECYCLE_ENTRY_NONFINITE_JSON")
    value = json.loads(raw, object_pairs_hook=unique, parse_constant=constant)
    _need(type(value) is dict, "LIFECYCLE_ENTRY_DOCUMENT_OBJECT")
    return value, dict(path=str(path), bytes=size, sha256=actual)


def _module_path(root, name):
    relative = name.replace(".", "/")
    return root/(relative+".py" if "." in name else relative+"/__init__.py")


def _bootstrap(args):
    """Stdlib pin/origin gate before any product import; explicit test seam."""
    _need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
          and sys.dont_write_bytecode and not sys.flags.optimize,
          "LIFECYCLE_ENTRY_ISOLATED_WINDOWS")
    entry = _ordinary(Path(__file__).resolve())
    own = dict(path=str(entry), bytes=entry.stat().st_size, sha256=_digest(args.entry_sha256))
    _read_pin(own, PUBLIC_ENTRY_REPORT_LIMIT)
    root = _ordinary(args.source_root, directory=True)
    profile, profile_pin = _pin_document(args.profile, args.profile_sha256)
    _need(set(profile) == {"schema", "base_profile", "source_pins", "snapshot_host_build", "release"}
          and profile["schema"] == "DMKN_INSTALLED_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1",
          "LIFECYCLE_ENTRY_RELEASE_PROFILE")
    rows = profile["source_pins"]
    _need(type(rows) is list and len(rows) == len(PRODUCER_MODULES),
          "LIFECYCLE_ENTRY_31_SOURCES")
    expected = {str(_module_path(root, name)) for name in PRODUCER_MODULES}
    pins, held = {}, {}
    for row in rows:
        held[Path(row["path"])] = _read_pin(row)
        _need(row["path"] in expected and row["path"] not in pins,
              "LIFECYCLE_ENTRY_EXACT_SOURCE_ROOT")
        pins[row["path"]] = dict(row)
    _need(set(pins) == expected, "LIFECYCLE_ENTRY_EXACT_SOURCE_CLOSURE")
    runtime = profile["base_profile"]["support_profile"]["runtime_pins"]
    _need(type(runtime) is list and len(runtime) <= 128, "LIFECYCLE_ENTRY_RUNTIME_BOUND")
    by_path = {}
    for row in runtime:
        _need(type(row) is dict and set(row) == {"path", "bytes", "sha256"}
              and type(row["path"]) is str and row["path"] not in by_path,
              "LIFECYCLE_ENTRY_RUNTIME_PIN_MAP")
        by_path[row["path"]] = row
    for path, row in pins.items():
        _need(by_path.get(path) == row, "LIFECYCLE_ENTRY_SOURCE_RUNTIME_BINDING")
    operator_path = str(_module_path(root, "aggregate_small.operator"))
    _need(operator_path in by_path, "LIFECYCLE_ENTRY_OPERATOR_PIN_REQUIRED")
    held[Path(operator_path)] = _read_pin(by_path[operator_path])
    pins[operator_path] = dict(by_path[operator_path])
    installed_entry = str(_module_path(root, "release_production.operator"))
    _need(installed_entry in by_path
          and by_path[installed_entry]["bytes"] == own["bytes"]
          and by_path[installed_entry]["sha256"] == own["sha256"],
          "LIFECYCLE_ENTRY_INSTALLED_ENTRY_BINDING")
    _read_pin(by_path[installed_entry], PUBLIC_ENTRY_REPORT_LIMIT)
    pins[installed_entry] = dict(by_path[installed_entry])
    packages = {name.split(".")[0] for name in IMPORT_MODULES}
    _need(not any(name.split(".")[0] in packages for name in sys.modules),
          "LIFECYCLE_ENTRY_PRELOADED_PRODUCT_MODULE")
    previous = list(sys.path)
    support = profile["base_profile"]["support_profile"]
    python_root = Path(support["python"]["path"]).parent
    _need(str(Path(sys.executable).resolve()) == support["python"]["path"],
          "LIFECYCLE_ENTRY_ACTUAL_PYTHON")
    manifest, manifest_pin = _pin_document(support["supervisor_manifest"]["path"],
                                         support["supervisor_manifest"]["sha256"], 8*MIB)
    _need(manifest_pin == support["supervisor_manifest"], "LIFECYCLE_ENTRY_SUPERVISOR_MANIFEST")
    support_root = Path(manifest_pin["path"]).parent
    runtime_prefix = python_root.relative_to(support_root).as_posix()+"/"
    python_rows = {support_root/name: {"path": str(support_root/name), **row}
                  for name,row in manifest["files"].items() if name.startswith(runtime_prefix)}
    _need(1 <= len(python_rows) <= 10000 and sum(row["bytes"] for row in python_rows.values()) <= 256*MIB,
          "LIFECYCLE_ENTRY_FULL_PYTHON_BOUND")
    _need(all(item and Path(item).is_absolute() and Path(item).is_relative_to(python_root)
              for item in previous), "LIFECYCLE_ENTRY_STDLIB_SEARCH_PATH")

    def python_binding():
        actual = set()
        directories = 0
        for parent, children, names in os.walk(python_root, followlinks=False):
            parent = _ordinary(parent, directory=True); directories += 1
            _need(directories <= 10000, "LIFECYCLE_ENTRY_PYTHON_DIRECTORY_BOUND")
            for name in children:
                _ordinary(parent/name, directory=True)
            for name in names:
                actual.add(_ordinary(parent/name))
                _need(len(actual) <= 10000, "LIFECYCLE_ENTRY_PYTHON_FILE_BOUND")
        _need(actual == set(python_rows), "LIFECYCLE_ENTRY_PYTHON_CENSUS")
        for row in python_rows.values():
            # The fixed runtime may contain empty data files; product source pins do not.
            path = _ordinary(row["path"])
            _need(type(row["bytes"]) is int and 0 <= row["bytes"] <= 128*MIB,
                  "LIFECYCLE_ENTRY_PYTHON_FILE_SIZE")
            with path.open("rb") as stream:
                raw = stream.read(row["bytes"]+1)
            _need(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
                  "LIFECYCLE_ENTRY_PYTHON_PIN")

    python_binding()

    class HeldLoader(importlib.machinery.SourceFileLoader):
        def get_code(self, fullname):
            path = Path(self.path)
            _need(path in held and path.suffix == ".py", "LIFECYCLE_ENTRY_UNSELECTED_SOURCE")
            return compile(held[path], str(path), "exec", dont_inherit=True)

    class Origins:
        def find_spec(self, fullname, path=None, target=None):
            spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
            if spec is None:
                return None
            _need(spec.origin is not None, "LIFECYCLE_ENTRY_NAMESPACE_IMPORT")
            origin = Path(spec.origin)
            if origin in held:
                spec.loader = HeldLoader(fullname, str(origin))
                return spec
            _need(origin in python_rows, "LIFECYCLE_ENTRY_UNSELECTED_IMPORT_ORIGIN")
            return spec

    guard = Origins()
    _need(sys.meta_path[-1] is importlib.machinery.PathFinder, "LIFECYCLE_ENTRY_FILESYSTEM_IMPORTER")
    sys.meta_path[-1] = guard
    expected_meta_path = tuple(sys.meta_path)
    try:
        sys.path.insert(0, str(root))
        O = import_module("aggregate_small.operator")
        T = import_module("release_production.producer")
        for name in IMPORT_MODULES:
            module = sys.modules.get(name)
            _need(module is not None and Path(getattr(module, "__file__", "")).resolve()
                  == _module_path(root, name), "LIFECYCLE_ENTRY_IMPORTED_ORIGIN:"+name)
        _need(tuple(T.SOURCE_MODULES) == PRODUCER_MODULES,
              "LIFECYCLE_ENTRY_DECLARED_CLOSURE_CHANGED")
        _need(tuple(sys.meta_path) == expected_meta_path
              and sys.path == [str(root), *previous], "LIFECYCLE_ENTRY_IMPORT_POLICY_CHANGED")
        for row in pins.values():
            _read_pin(row)
    finally:
        sys.path[:] = previous
    def verify_imports():
        _need(tuple(sys.meta_path) == expected_meta_path and sys.path == previous,
              "LIFECYCLE_ENTRY_IMPORT_POLICY_CHANGED")
        for name,module in tuple(sys.modules.items()):
            if name.split(".")[0] in packages:
                _need(name in IMPORT_MODULES and Path(getattr(module, "__file__", "")) == _module_path(root, name),
                      "LIFECYCLE_ENTRY_FINAL_PRODUCT_ORIGIN")
        for row in pins.values():
            _read_pin(row)
        _read_pin(manifest_pin, 8*MIB)
        python_binding()
    pins.update({own["path"]: own, profile_pin["path"]: profile_pin})
    return SimpleNamespace(O=O, P=sys.modules["production.producer"], T=T,
        N=sys.modules["aggregate_lifecycle.snapshot"],
        C=sys.modules["release_production.launch_contract"], verify_imports=verify_imports,
        Envelope=sys.modules["mixed_claims.packet"].Envelope,
        source_root=root, entry_pin=own, profile=profile, profile_pin=profile_pin,
        pins=pins, invocation=list(sys.orig_argv))


def _snapshot_selection(boot, path, configuration_pin):
    """Exact genuine public invocation; no historical local-check translation."""
    selection, pin = boot.C.read_selection(path, boot.selection_sha256)
    selected = boot.C.validate_selection(selection, pin, fresh_run=False)
    _need(selection["profile"] == boot.profile_pin and selection["input"] == configuration_pin
          and selection["action"] == boot.action and Path(boot.entry_pin["path"]) == selected.run/"entry.py"
          and boot.C.command(selection, pin) == boot.invocation, "LIFECYCLE_ENTRY_EXACT_PUBLIC_INVOCATION")
    boot.selected = selected
    return selection, pin


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("snapshot", "request", "preflight", "run"))
    for name in ("source-root", "entry-sha256", "profile", "profile-sha256", "input", "input-sha256", "owner-report"):
        parser.add_argument("--"+name, required=True)
    parser.add_argument("--outer-selection", required=True)
    parser.add_argument("--outer-selection-sha256", required=True)
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    started, cpu = time.monotonic(), time.process_time()
    boot = owner = report_path = sentinel = output = request_output = None
    O = P = None
    safe = False
    pins, inputs, protected, generated = {}, {}, [], {}
    pending_request = outcome = None
    report = dict(schema=REPORT_SCHEMA, status="FAIL", action=args.action,
        error=None, close_error=None, final_binding_error=None, owner_creation="NOT_ATTEMPTED",
        owner_created=False, owner_closed=False, owner_observation=None, final_binding_validated=False,
        prepare_calls_attempted=0, snapshot_calls_attempted=0, production_request_calls_attempted=0,
        run_calls_attempted=0, preflight_calls_attempted=0, proof_calls=0, host_calls_attempted=0,
        snapshot_result=None, request=None, production_result=None, preflight=None,
        mathematical_admission=False, funding=False,
        authority="LOCAL_OWNER_REPORT_NOT_MATHEMATICAL_OR_FUNDING_AUTHORITY",
        accounting="PRE_FINAL_REPORT_PROCESS_CPU_AND_WALL;ENCLOSING_OWNER_BOUNDS_ALL_TAILS")
    try:
        boot = _bootstrap(args)
        boot.selection_sha256, boot.action = _digest(args.outer_selection_sha256), args.action
        O, P = boot.O, boot.P
        pins.update(boot.pins)
        value, input_pin = O.document(args.input, args.input_sha256)
        _need(input_pin["path"] not in pins, "LIFECYCLE_ENTRY_DISTINCT_INPUT_DOCUMENT")
        pins[input_pin["path"]] = input_pin
        selection, selection_pin = _snapshot_selection(boot, args.outer_selection, input_pin)
        pins[selection_pin["path"]] = selection_pin
        if args.action == "snapshot":
            P.fields(value, ("schema", "profile_id", "profile_document", "packet", "target_journal",
                "envelope", "cycles", "po2", "diagnostic_mode", "limits", "output_directory"))
            P.require(value["schema"] == boot.N.CONFIG_SCHEMA
                      and value["profile_document"] == boot.profile_pin,
                      "LIFECYCLE_ENTRY_SNAPSHOT_PROFILE_DOCUMENT")
            inputs = O.declared_pins(boot.profile, value)
        elif args.action == "request":
            P.fields(value, ("schema", "snapshot_evidence", "allowance_id", "budget", "checkpoints",
                "prior_attempts", "output_directory", "stage_limit", "carried_external_costs", "request_output"))
            P.require(value["schema"] == REQUEST_SCHEMA, "LIFECYCLE_ENTRY_REQUEST_INPUT")
            P.fields(value["snapshot_evidence"], boot.N.EVIDENCE_FIELDS)
            inputs = O.declared_pins(boot.profile, value)
            request_output = O.ordinary(value["request_output"], fresh=True)
        else:
            P.fields(value, ("schema", "allowance_id", "session", "checkpoints", "output_directory",
                             "stage_limit", "budget", "prior_attempts", "carried_external_costs"))
            P.require(value["schema"] == "DMKN_V5_SMALL_AGGREGATE_PRODUCER_REQUEST_V1",
                      "LIFECYCLE_ENTRY_STAGE_REQUEST_SCHEMA")
            inputs = O.declared_pins(boot.profile, value)
        output = O.ordinary(value["output_directory"], fresh=True)
        installation = O.ordinary(P.pin_fields(
            boot.profile["base_profile"]["support_profile"]["supervisor_manifest"], 8*MIB)).parent
        release_root = _ordinary(boot.profile["release"]["root"], directory=True)
        report_path = O.ordinary(args.owner_report, fresh=True)
        sentinel = O.ordinary(str(report_path)+".FINALIZATION-FAILED.json", fresh=True)
        protected = [release_root, boot.source_root, installation, *pins, *inputs]
        outputs = [output, report_path, sentinel]+([] if request_output is None else [request_output])
        for index, path in enumerate(outputs):
            O.separate((path,), [*protected, *outputs[:index], *outputs[index+1:]])
        safe = True
        report.update(profile_document=boot.profile_pin, input_document=input_pin,
            entry_source=boot.entry_pin, source_root=str(boot.source_root),
            output_directory=str(output), owner_report=str(report_path), outer_selection=selection_pin)
        O.rebind(pins)
        O.rebind(inputs)
        report["owner_creation"] = "ATTEMPTED_UNCONFIRMED"
        owner = boot.T.ReleaseLifecycleProducer(boot.profile)
        report.update(owner_created=True, owner_creation="OPENED", profile_id=owner.profile_id)
        for path in outputs:
            O.separate((path,), [owner._install, *owner._pins])
        pins.update(owner._pins)
        for row in owner._pins.values():
            P.require(selection["runtime_pins"].get(row["path"]) == row["sha256"],
                      "LIFECYCLE_ENTRY_SELECTED_OWNER_CLOSURE")
        if args.action == "snapshot":
            target = value["target_journal"]
            P.require(type(target) is str and len(target) == 368
                      and all(c in "0123456789abcdef" for c in target), "LIFECYCLE_ENTRY_EXACT_TARGET_HEX")
            envelope = boot.Envelope(**value["envelope"])
            envelope.validate()
            raw = owner._read(value["packet"], envelope.packet_bytes)
            report["prepare_calls_attempted"] = 1
            prepared = owner.prepare(raw, bytes.fromhex(target), envelope=envelope)
            report["snapshot_calls_attempted"] = 1
            report["host_calls_attempted"] = None  # A raised call has unknown actual dispatch extent.
            actual = owner.snapshot(prepared, configuration=input_pin, selection=selection_pin)
            result_pin = P.file_pin(O.ordinary(output/"RESULT.json"))
            P.require(result_pin["bytes"] == len(P.encoded(actual))
                      and result_pin["sha256"] == P.hash_bytes(P.encoded(actual)),
                      "LIFECYCLE_ENTRY_EXACT_SNAPSHOT_REPORT")
            generated[result_pin["path"]] = result_pin
            report.update(snapshot_result=result_pin, snapshot_status=actual["status"],
                host_calls_attempted=actual["host_calls_attempted"])
            boot.N.result_shape(actual, owner.profile_id)
            report["session"] = actual["session"]
            # Rebind all generated/pinned evidence cited by the actual report,
            # not just a status or its returned Python object.
            generated.update(O.declared_pins(actual))
            outcome = "PASS_ONE_SNAPSHOT"
        elif args.action == "request":
            report["production_request_calls_attempted"] = 1
            options = {name: value[name] for name in ("allowance_id", "budget", "checkpoints", "prior_attempts",
                "output_directory", "stage_limit", "carried_external_costs")}
            pending_request = owner.production_request(value["snapshot_evidence"], **options)
            P.require(type(pending_request) is dict and pending_request["output_directory"] == str(output),
                      "LIFECYCLE_ENTRY_RETURNED_OUTPUT")
            # production_request has already called preflight. Do not call it again.
            inputs.update(O.declared_pins(pending_request))
            O.separate((request_output, report_path, sentinel, output), [*protected, *pins, *inputs])
            P.require(not output.exists(), "LIFECYCLE_ENTRY_REQUEST_DID_NOT_DISPATCH")
            outcome = "PASS_REQUEST_CONSTRUCTION_ONLY"
        elif args.action == "preflight":
            report["preflight_calls_attempted"] = 1
            report["preflight"] = owner.preflight(value)
            P.require(type(report["preflight"]) is dict
                      and report["preflight"]["status"] == "PASS_REQUEST_PREFLIGHT_ONLY"
                      and report["preflight"]["profile_id"] == owner.profile_id
                      and report["preflight"]["host_calls"] == 0
                      and report["preflight"]["proof_calls"] == 0
                      and report["preflight"]["mathematical_admission"] is False
                      and report["preflight"]["funding"] is False
                      and not output.exists(), "LIFECYCLE_ENTRY_PREFLIGHT_ONLY")
            outcome = "PASS_REQUEST_PREFLIGHT_ONLY"
        else:
            report["run_calls_attempted"] = 1
            report["host_calls_attempted"] = report["proof_calls"] = None
            actual = owner.run(value)
            result_pin = P.file_pin(O.ordinary(output/"RESULT.json"))
            P.require(result_pin["bytes"] == len(P.encoded(actual))
                      and result_pin["sha256"] == P.hash_bytes(P.encoded(actual)),
                      "LIFECYCLE_ENTRY_EXACT_PRODUCTION_REPORT")
            generated[result_pin["path"]] = result_pin
            generated.update(O.declared_pins(actual))
            report.update(production_result=result_pin, production_status=actual["status"],
                host_calls_attempted=actual["host_calls_attempted"],
                proof_calls=actual["reported_proof_stage_calls"])
            P.require(actual["profile_id"] == owner.profile_id
                      and actual["status"] in ("PASS_SELECTED_PREFIX_ONLY", "PASS_FINISHED_RECEIPT_ARTIFACT")
                      and actual["closure_accounting_known"] is True
                      and actual["final_binding_validated"] is True,
                      "LIFECYCLE_ENTRY_SUCCESSFUL_FINITE_ATTEMPT")
            outcome = "PASS_ONE_FINITE_ATTEMPT"
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    finally:
        if owner is not None:
            try:
                owner.close()
                report["owner_observation"] = owner.report()
                report["owner_closed"] = report["owner_observation"]["closed"] is True
                _need(report["owner_closed"], "LIFECYCLE_ENTRY_OWNER_NOT_CLOSED")
            except BaseException as error:
                report["close_error"] = type(error).__name__+": "+str(error)[:2000]
        if O is not None:
            try:
                boot.verify_imports()
                if hasattr(boot, "selected"):
                    boot.C.rebind_selection(boot.selected)
                O.rebind(pins)
                O.rebind(inputs)
                O.rebind(generated)
                if args.action in ("request", "preflight") and output is not None:
                    _need(not output.exists(), "LIFECYCLE_ENTRY_REQUEST_OUTPUT_CREATED")
                for path in (Path(row["path"]).parent/"FINALIZATION-FAILED.json" for row in generated.values()):
                    _need(not path.exists(), "LIFECYCLE_ENTRY_SNAPSHOT_FINALIZATION_OVERRIDE")
                report["final_binding_validated"] = True
            except BaseException as error:
                report["final_binding_error"] = type(error).__name__+": "+str(error)[:2000]
    success = (outcome is not None and report["error"] is None and report["close_error"] is None
               and report["owner_closed"] and report["final_binding_validated"])
    if success and args.action == "request":
        try:
            request_pin = O.save_new(request_output, pending_request, MIB)
            generated[request_pin["path"]] = request_pin
            O.rebind(generated)
            report["request"] = request_pin
        except BaseException as error:
            success = False
            report["final_binding_error"] = type(error).__name__+": "+str(error)[:2000]
            report["final_binding_validated"] = False
    if success:
        report["status"] = outcome
    report.update(controller_cpu_seconds_before_report=time.process_time()-cpu,
                  wall_seconds_before_report=time.monotonic()-started)
    try:
        _need(safe and O is not None, "LIFECYCLE_ENTRY_NO_SAFE_OWNER_REPORT_PATH")
        O.separate((report_path, sentinel), [*protected, *pins, *inputs, *generated,
            *([] if request_output is None else [request_output]), output])
        written = O.save_new(report_path, report, PUBLIC_ENTRY_REPORT_LIMIT)
        O.rebind(pins)
        O.rebind(inputs)
        O.rebind(generated)
        O.rebind({written["path"]: written})
        if args.action in ("request", "preflight"):
            _need(not output.exists(), "LIFECYCLE_ENTRY_LATE_REQUEST_OUTPUT_CREATED")
    except BaseException as error:
        report.update(status="FAIL", final_binding_validated=False,
            final_binding_error=type(error).__name__+": "+str(error)[:2000])
    if safe and report["final_binding_error"] is not None:
        # Also cover a partially written request or failed pre-report rebind;
        # a subsequently saved FAIL report does not erase either failure.
        try:
            O.save_new(sentinel, dict(status="FINALIZATION_FAILED", overrides_owner_report=True,
                overrides_generated_request=True, owner_report=str(report_path),
                request_output=None if request_output is None else str(request_output),
                error=report["final_binding_error"]), 65536)
        except BaseException as late:
            report["sentinel_error"] = type(late).__name__+": "+str(late)[:2000]
    # Stdlib reporting also covers refused bootstrap with no imported product code.
    print(json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False), flush=True)
    return 0 if report["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
