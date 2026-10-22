"""Closed installed producer launch/profile contract; stdlib-only bootstrap.

Local operational records are not mathematical or funding authority. Prior
outer evidence is checked one level deep, never recursively replayed.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
from types import SimpleNamespace

MIB = 1024**2
PUBLIC_ENTRY_REPORT_LIMIT = 64*1024
SELECTION_SCHEMA = "DMKN_RELEASE_PRODUCER_LAUNCH_V1"
RESULT_SCHEMA = "DMKN_RELEASE_PRODUCER_LAUNCH_RESULT_V1"
PROFILE_SCHEMA = "DMKN_INSTALLED_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1"
PROFILE_DOMAIN = b"DMKN-INSTALLED-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1\0"
TEMPLATE_SCHEMA = "DMKN_RELEASE_PRODUCER_PROFILE_TEMPLATE_V1"
MANIFEST_SCHEMA = "DMKN_V5_DIRECTORY_RELEASE_V4"
DESCRIPTOR_SCHEMA = "DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1"
SELECTION_FIELDS = ("schema", "name", "action", "release", "profile", "input", "entry",
    "run_directory", "runtime_pins", "limits", "output_limits", "prior_launches", "input_launch")
RESULT_FIELDS = ("schema", "status", "selection", "worker_report", "result", "final_error",
    "observed_output", "bootstrap_cpu_seconds", "wrapper_cpu_seconds", "wall_seconds",
    "pre_clock_interpreter_startup", "bootstrap_containment", "authority")
ACTIONS = ("snapshot", "request", "preflight", "run")
LIMITS = {"cpu_seconds": 86400, "wall_seconds": 3600, "memory_mib": 4096,
    "active_processes": 2, "stdout_bytes": MIB, "stderr_bytes": MIB}
OUTER_METADATA_BYTES = 64*MIB
SOURCE_MODULES = (
    "aggregate_lifecycle", "aggregate_lifecycle.producer", "aggregate_lifecycle.snapshot",
    "aggregate_small", "aggregate_small.producer", "production", "production.producer",
    "aggregate_claims", "aggregate_claims.bindings", "aggregate_claims.input",
    "aggregate_claims.prepare_mixed", "mixed_claims", "mixed_claims.packet",
    "delta", "delta.packet", "delta.receiver", "delta_claims", "delta_claims.claims",
    "delta_claims.receiver", "admission", "admission.bindings", "admission.verifier",
    "modules", "modules.codec", "release_production", "release_production.producer",
    "release_production.adoption", "admission.pin_phase", "admission.trust",
    "admission.clean_refusal", "release_production.launch_contract")
PYTHON_RUNTIME_NAMES = ("python3.dll", "vcruntime140.dll", "vcruntime140_1.dll",
    "DLLs/_asyncio.pyd", "DLLs/_overlapped.pyd", "DLLs/_socket.pyd", "DLLs/select.pyd",
    "DLLs/_ssl.pyd", "DLLs/libssl-3.dll", "DLLs/libcrypto-3.dll", "DLLs/_hashlib.pyd",
    "DLLs/_sqlite3.pyd", "DLLs/sqlite3.dll", "DLLs/_queue.pyd", "DLLs/_ctypes.pyd", "DLLs/libffi-8.dll")
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
RELATION = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
IMAGE = "9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865"
ARTIFACTS = {
    "stage_host": ("stage_host.exe", 68039168, "263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c"),
    "snapshot_host": ("snapshot_host.exe", 6630400, "a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05"),
    "guest_image": ("aggregate_image.bin", 1868700, "0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46")}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def fields(value, names):
    need(type(value) is dict and set(value) == set(names), "PUBLIC_EXACT_FIELDS")


def uint(value, maximum, minimum=0):
    need(type(value) is int and minimum <= value <= maximum, "PUBLIC_INTEGER_BOUND")
    return value


def number(value):
    need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
         "PUBLIC_FINITE_COST")
    return value


def digest(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "PUBLIC_DIGEST")
    return value


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, "PUBLIC_DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(unused):
        raise ValueError("PUBLIC_NONFINITE_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject)


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value, "PUBLIC_RELATIVE_PATH")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value
         and len(path.parts) <= 32, "PUBLIC_RELATIVE_SHAPE")
    for part in path.parts:
        need(part not in (".", "..") and not part.endswith((".", " "))
             and not os.path.isreserved(part)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part), "PUBLIC_PATH_COMPONENT")
    return path.parts


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor) and str(path.resolve(strict=not fresh)) == str(path),
         "PUBLIC_CANONICAL_PATH")
    for part in path.parts[1:]:
        relative(part)
    for parent in path.parents:
        info = parent.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "PUBLIC_ORDINARY_PARENT")
    if fresh:
        need(not path.exists() and not path.is_symlink() and not path.is_junction(), "PUBLIC_FRESH_PATH")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
             "PUBLIC_ORDINARY_TARGET")
    return path


def overlap(left, right):
    left, right = Path(left), Path(right)
    return left.is_relative_to(right) or right.is_relative_to(left)


def pin_shape(pin, maximum=128*MIB):
    fields(pin, ("path", "bytes", "sha256"))
    need(type(pin["path"]) is str and Path(pin["path"]).is_absolute(), "PUBLIC_PIN_PATH")
    uint(pin["bytes"], maximum, 1); digest(pin["sha256"])
    return Path(pin["path"])


def read_pin(pin, maximum=128*MIB):
    path = ordinary(pin_shape(pin, maximum))
    need(path.stat().st_size == pin["bytes"], "PUBLIC_PIN_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(pin["bytes"]+1)
    need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
         "PUBLIC_PIN_CHANGED")
    return raw


def document(pin, maximum=MIB):
    value = parse(read_pin(pin, maximum))
    need(type(value) is dict, "PUBLIC_DOCUMENT_OBJECT")
    return value


def read_selection(path, expected):
    path = ordinary(path); digest(expected)
    pin = {"path": str(path), "bytes": path.stat().st_size, "sha256": expected}
    return document(pin), pin


def _remember(table, pin, maximum=128*MIB):
    pin_shape(pin, maximum)
    need(pin["path"] not in table or table[pin["path"]] == pin, "PUBLIC_CONFLICTING_PIN")
    table[pin["path"]] = dict(pin)


def _shape(selection):
    fields(selection, SELECTION_FIELDS)
    need(selection["schema"] == SELECTION_SCHEMA and selection["action"] in ACTIONS,
         "PUBLIC_LAUNCH_SCHEMA_ACTION")
    need(type(selection["name"]) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", selection["name"]),
         "PUBLIC_OPERATION_NAME")
    fields(selection["release"], ("root", "manifest", "descriptor"))
    for key in ("profile", "input", "entry"):
        pin_shape(selection[key], PUBLIC_ENTRY_REPORT_LIMIT if key == "entry" else MIB)
    pin_shape(selection["release"]["manifest"], 8*MIB)
    pin_shape(selection["release"]["descriptor"], MIB)
    run = Path(selection["run_directory"])
    need(type(selection["run_directory"]) is str and run.is_absolute()
         and run.name == selection["name"], "PUBLIC_RUN_NAME")
    fields(selection["limits"], LIMITS)
    for key, cap in LIMITS.items():
        uint(selection["limits"][key], cap, 1)
    fields(selection["output_limits"], ("bytes", "entries"))
    uint(selection["output_limits"]["bytes"], 1024**3, MIB)
    uint(selection["output_limits"]["entries"], 16384, 8)
    runtime = selection["runtime_pins"]
    need(type(runtime) is dict and 1 <= len(runtime) <= 256, "PUBLIC_RUNTIME_COUNT")
    for path, sha in runtime.items():
        need(type(path) is str and Path(path).is_absolute(), "PUBLIC_RUNTIME_PATH")
        digest(sha)
    prior = selection["prior_launches"]
    need(type(prior) is list and len(prior) <= 16, "PUBLIC_PRIOR_COUNT")
    for pin in prior:
        pin_shape(pin, 2*MIB)
    if selection["action"] in ("run", "preflight"):
        pin_shape(selection["input_launch"], 2*MIB)
    else:
        need(selection["input_launch"] is None, "PUBLIC_UNEXPECTED_INPUT_LAUNCH")
    return run


def command(selection, selection_pin):
    run = _shape(selection)
    need(Path(selection_pin["path"]) == run/"selection.json", "PUBLIC_SELECTION_COPY_LOCATION")
    root = Path(selection["release"]["root"])
    profile = document(selection["profile"])
    python = profile["base_profile"]["support_profile"]["python"]["path"]
    return [python, "-I", "-S", "-B", str(run/"entry.py"), selection["action"],
        "--source-root", str(root/"sdk/v5"), "--entry-sha256", selection["entry"]["sha256"],
        "--profile", selection["profile"]["path"], "--profile-sha256", selection["profile"]["sha256"],
        "--input", selection["input"]["path"], "--input-sha256", selection["input"]["sha256"],
        "--owner-report", str(run/"OWNER-RESULT.json"), "--outer-selection", selection_pin["path"],
        "--outer-selection-sha256", selection_pin["sha256"]]


def _override(run, action_output, action, *, completed=False):
    markers = [run/"FINALIZATION-FAILED.json", run/"OWNER-RESULT.json.FINALIZATION-FAILED.json"]
    if completed:
        markers.append(run/"FINALIZATION-PENDING.json")
    if action in ("snapshot", "run"):
        markers.append(action_output/"FINALIZATION-FAILED.json")
    need(not any(path.exists() for path in markers), "PUBLIC_FINALIZATION_OVERRIDE")


def validate_worker_report(selection, selection_pin, worker_pin):
    run = _shape(selection)
    need(Path(selection_pin["path"]) == run/"selection.json"
         and document(selection_pin) == selection, "PUBLIC_WORKER_SELECTION")
    profile, value = document(selection["profile"]), document(selection["input"])
    need(profile["schema"] == PROFILE_SCHEMA and profile["release"] == selection["release"],
         "PUBLIC_OUTER_PROFILE_RELEASE")
    operation = Path(value["output_directory"])
    _override(run, operation, selection["action"])
    need(Path(worker_pin["path"]) == run/"OWNER-RESULT.json", "PUBLIC_WORKER_REPORT_LOCATION")
    worker = document(worker_pin, PUBLIC_ENTRY_REPORT_LIMIT)
    expected_status = {"snapshot": "PASS_ONE_SNAPSHOT", "request": "PASS_REQUEST_CONSTRUCTION_ONLY",
        "preflight": "PASS_REQUEST_PREFLIGHT_ONLY", "run": "PASS_ONE_FINITE_ATTEMPT"}[selection["action"]]
    need(worker.get("schema") == "DMKN_RELEASE_LIFECYCLE_OPERATOR_RESULT_V1"
         and worker.get("status") == expected_status and worker.get("action") == selection["action"]
         and worker.get("profile_document") == selection["profile"]
         and worker.get("input_document") == selection["input"]
         and worker.get("outer_selection") == selection_pin
         and worker.get("profile_id") == hashlib.sha256(PROFILE_DOMAIN+encoded(profile)).hexdigest()
         and worker.get("source_root") == str(Path(selection["release"]["root"])/"sdk/v5")
         and worker.get("owner_report") == str(run/"OWNER-RESULT.json")
         and worker.get("output_directory") == str(operation)
         and worker.get("owner_created") is True and worker.get("owner_closed") is True
         and worker.get("final_binding_validated") is True
         and all(worker.get(key) is None for key in ("error", "close_error", "final_binding_error")),
         "PUBLIC_EXACT_WORKER_COMPLETION")
    entry_pin = worker.get("entry_source")
    pin_shape(entry_pin, PUBLIC_ENTRY_REPORT_LIMIT)
    need(Path(entry_pin["path"]) == run/"entry.py"
         and all(entry_pin[key] == selection["entry"][key] for key in ("bytes", "sha256")),
         "PUBLIC_EXECUTED_ENTRY_IDENTITY")
    read_pin(entry_pin, PUBLIC_ENTRY_REPORT_LIMIT)
    produced_key = {"snapshot":"snapshot_result", "request":"request", "run":"production_result"}.get(selection["action"])
    if produced_key:
        produced = worker.get(produced_key)
        expected_path = run/"request.json" if selection["action"] == "request" else operation/"RESULT.json"
        need(pin_shape(produced, MIB) == expected_path, "PUBLIC_PRODUCED_REPORT_LOCATION")
        read_pin(produced, MIB)
    return worker


def completed_outer(outer_pin, *, pins=None):
    """Validate this operation only; never follow its prior_launches recursively."""
    table = {} if pins is None else pins
    _remember(table, outer_pin, 2*MIB)
    outer = document(outer_pin, 2*MIB); fields(outer, RESULT_FIELDS)
    need(outer["schema"] == RESULT_SCHEMA and outer["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
         and outer["final_error"] is None, "PUBLIC_COMPLETED_OUTER")
    _remember(table, outer["selection"], MIB)
    selection = document(outer["selection"]); run = _shape(selection)
    need(Path(outer_pin["path"]) == run/"RESULT.json"
         and Path(outer["selection"]["path"]) == run/"selection.json", "PUBLIC_OUTER_PATH_BINDING")
    _remember(table, selection["profile"], MIB); _remember(table, selection["input"], MIB)
    _remember(table, outer["worker_report"], PUBLIC_ENTRY_REPORT_LIMIT)
    profile, value = document(selection["profile"]), document(selection["input"])
    operation = Path(value["output_directory"])
    worker = validate_worker_report(selection, outer["selection"], outer["worker_report"])
    _remember(table, worker["entry_source"], PUBLIC_ENTRY_REPORT_LIMIT)
    produced_key = {"snapshot":"snapshot_result", "request":"request", "run":"production_result"}.get(selection["action"])
    if produced_key:
        _remember(table, worker[produced_key], MIB)
    _override(run, operation, selection["action"], completed=True)
    process = outer["result"]
    need(type(process) is dict and process.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
         and type(process.get("child_exit_code")) is int and process["child_exit_code"] == 0
         and process.get("direct_child_reaped") is True and process.get("job_closed") is True
         and process.get("cleanup_errors") == [] and process.get("termination_requested") is False
         and type(process.get("final_job")) is dict
         and process["final_job"].get("active_processes") == 0
         and process["final_job"].get("terminated_processes") == 0
         and process.get("argv") == command(selection, outer["selection"])
         and process.get("cwd") == selection["release"]["root"]
         and process.get("limits") == selection["limits"], "PUBLIC_EXACT_CLEAN_COMMAND")
    need(number(process["final_job"]["cpu_seconds"]) <= selection["limits"]["cpu_seconds"]
         and number(outer["wall_seconds"]) <= selection["limits"]["wall_seconds"]
         and number(outer["bootstrap_cpu_seconds"]) <= 30
         and number(outer["wrapper_cpu_seconds"]) <= 60, "PUBLIC_OUTER_COST_LIMIT")
    census = outer["observed_output"]; fields(census, ("bytes", "entries", "scope"))
    need(census["scope"] == "DISJOINT_OPERATION_AND_SELECTED_ACTION_OUTPUT_ROOTS", "PUBLIC_OUTPUT_SCOPE")
    for key in ("bytes", "entries"):
        uint(census[key], selection["output_limits"][key])
    return SimpleNamespace(outer=outer, selection=selection, worker=worker, profile=profile,
                           input=value, run=run, action_output=operation, pins=table)


def _lineage(selection, profile, value, pins):
    prior = value.get("prior_attempts", [])
    need(type(prior) is list and len(prior) == len(selection["prior_launches"]), "PUBLIC_EXACT_PRIOR_LINEAGE")
    for inner, outer_pin in zip(prior, selection["prior_launches"]):
        old = completed_outer(outer_pin, pins=pins)
        need(old.selection["action"] == "run" and encoded(old.profile) == encoded(profile)
             and old.input.get("allowance_id") == value.get("allowance_id")
             and old.worker.get("production_result") == inner, "PUBLIC_PRIOR_ATTEMPT_BINDING")
        _remember(pins, inner, MIB)
        report = document(inner)
        need(report.get("allowance_id") == value.get("allowance_id")
             and report.get("profile_id") == old.worker["profile_id"], "PUBLIC_PRIOR_INNER_IDENTITY")
    if selection["input_launch"] is not None:
        origin = completed_outer(selection["input_launch"], pins=pins)
        need(origin.selection["action"] == "request" and encoded(origin.profile) == encoded(profile)
             and origin.worker.get("request") == selection["input"], "PUBLIC_GENERATED_REQUEST_ORIGIN")
    need(len(pins) <= 256 and sum(pin["bytes"] for pin in pins.values()) <= OUTER_METADATA_BYTES,
         "PUBLIC_OUTER_METADATA_BOUND")


def validate_selection(selection, selection_pin, *, fresh_run):
    run = _shape(selection)
    root = ordinary(selection["release"]["root"], directory=True)
    ordinary(run, directory=True, fresh=fresh_run)
    need(not overlap(root, run), "PUBLIC_OUTPUT_INSTALLATION_OVERLAP")
    manifest = document(selection["release"]["manifest"], 8*MIB)
    need(Path(selection["release"]["manifest"]["path"]) == root/"V5-RELEASE.json"
         and manifest.get("schema") == MANIFEST_SCHEMA and type(manifest.get("files")) is dict,
         "PUBLIC_RELEASE_MANIFEST")
    descriptor = document(selection["release"]["descriptor"])
    need(descriptor.get("schema") == DESCRIPTOR_SCHEMA, "PUBLIC_RELEASE_DESCRIPTOR")
    profile, value = document(selection["profile"]), document(selection["input"])
    need(profile.get("schema") == PROFILE_SCHEMA and profile.get("release") == selection["release"],
         "PUBLIC_EXACT_PROFILE_RELEASE")
    template_row = manifest["production"]["profile_template"]
    template_pin = {**template_row, "path": str(root.joinpath(*relative(template_row["path"])))}
    template = document(template_pin)
    expected_profile = materialize_profile(root, selection["release"]["manifest"],
                                          selection["release"]["descriptor"], template)
    need(encoded(profile) == encoded(expected_profile), "PUBLIC_PROFILE_EQUALS_RELEASE_TEMPLATE")
    need(Path(selection["entry"]["path"]) == root/"sdk/v5/release_production/operator.py",
         "PUBLIC_INSTALLED_ENTRY_ROLE")
    pins = {}
    for pin in (selection["profile"], selection["input"], selection["entry"],
                selection["release"]["manifest"], selection["release"]["descriptor"], template_pin):
        _remember(pins, pin)
    for pin in (selection["entry"], selection["release"]["descriptor"]):
        path = ordinary(pin["path"])
        need(path.is_relative_to(root) and manifest["files"].get(path.relative_to(root).as_posix()) ==
             {key:pin[key] for key in ("bytes", "sha256")}, "PUBLIC_RELEASE_ROLE_PIN")
        read_pin(pin)
    operation = Path(value["output_directory"])
    ordinary(operation, directory=True, fresh=fresh_run or not operation.exists())
    need(not overlap(operation, root) and not overlap(operation, run), "PUBLIC_DISJOINT_ACTION_OUTPUT")
    for pin in pins.values():
        need(not overlap(run, pin["path"]) and not overlap(operation, pin["path"]), "PUBLIC_OUTPUT_INPUT_OVERLAP")
    runtime = {}
    for path, sha in selection["runtime_pins"].items():
        original = ordinary(path)
        pin = {"path": path, "bytes": original.stat().st_size, "sha256": sha}
        pin_shape(pin); runtime[path] = pin
        need(not overlap(run, path) and not overlap(operation, path), "PUBLIC_OUTPUT_RUNTIME_OVERLAP")
    need(sum(pin["bytes"] for pin in runtime.values()) <= 512*MIB, "PUBLIC_RUNTIME_BYTE_BOUND")
    for pin in (selection["profile"], selection["input"], selection["entry"]):
        need(runtime.get(pin["path"]) == pin, "PUBLIC_SELECTED_DIRECT_INPUT")
    request_output = None
    if selection["action"] == "request":
        request_output = run/"request.json"
        need(value.get("request_output") == str(request_output), "PUBLIC_REQUEST_OUTPUT_LOCATION")
    if selection["action"] == "snapshot":
        need(value.get("profile_document") == selection["profile"], "PUBLIC_SNAPSHOT_PROFILE_DOCUMENT")
        packet = value.get("packet"); pin_shape(packet)
        need(runtime.get(packet["path"]) == packet, "PUBLIC_SELECTED_PACKET")
    _lineage(selection, profile, value, pins)
    for pin in pins.values():
        need(not overlap(run, pin["path"]) and not overlap(operation, pin["path"]), "PUBLIC_OUTPUT_EVIDENCE_OVERLAP")
    result = SimpleNamespace(selection=selection, selection_pin=selection_pin, root=root, run=run,
        profile=profile, input=value, action_output=operation, runtime_pins=runtime, pins=pins,
        entry=selection["entry"], release=selection["release"], request_output=request_output,
        owner_report=run/"OWNER-RESULT.json")
    rebind_selection(result)
    return result


def rebind_selection(selected):
    # Callers check clocks around this bounded operation; it creates no state.
    for path in set(selected.pins).intersection(selected.runtime_pins):
        need(selected.pins[path] == selected.runtime_pins[path], "PUBLIC_CONFLICTING_RUNTIME_PIN")
    for pin in {**selected.pins, **selected.runtime_pins}.values():
        read_pin(pin)
    _lineage(selected.selection, selected.profile, selected.input, {})


def selection_for_owner(owner, pin, configuration, cfg, table):
    owner._add(table, pin, MIB)
    selection = document(pin)
    _shape(selection)
    need(selection["action"] == "snapshot" and selection["input"] == configuration
         and selection["profile"] == cfg["profile_document"]
         and selection["release"] == owner._lifecycle_profile["release"], "PUBLIC_SNAPSHOT_SELECTION_BINDING")
    for original in (configuration, cfg["profile_document"], cfg["packet"], *owner._pins.values()):
        need(selection["runtime_pins"].get(original["path"]) == original["sha256"],
             "PUBLIC_SELECTED_OWNER_INPUT")
    return selection


def outer_for_owner(owner, outer, selection, selection_pin, outer_pin):
    # Public evidence is shallowly re-read under its own finite envelope, not
    # silently appended to the immutable fixed-session pin set. The entry and
    # worker add at most128KiB to the historical13.125MiB future reserve;
    #13.25MiB fits the unchanged14MiB reservation in snapshot._fixed_bound.
    # This is a distinct-byte bound, not a claim that repeated I/O reads total
    #14MiB or that the final fixed-session table lists every public read.
    completed = completed_outer(outer_pin)
    need(completed.outer == outer and completed.selection == selection
         and outer["selection"] == selection_pin and selection["action"] == "snapshot"
         and encoded(completed.profile) == owner._lifecycle_raw
         and completed.worker.get("snapshot_result", {}).get("path") ==
             str(completed.action_output/"RESULT.json"), "PUBLIC_EXACT_SNAPSHOT_OUTER")


def validate_production_metadata(manifest, descriptor, template):
    """Pure exact producer metadata checks; no filesystem or owner construction."""
    need(type(manifest) is dict and manifest.get("schema") == MANIFEST_SCHEMA
         and type(manifest.get("files")) is dict, "PUBLIC_METADATA_MANIFEST")
    files = manifest["files"]
    def role(row, path=None):
        fields(row, ("path", "bytes", "sha256"))
        relative(row["path"]); uint(row["bytes"], 128*MIB, 1); digest(row["sha256"])
        need((path is None or row["path"] == path)
             and files.get(row["path"]) == {key:row[key] for key in ("bytes", "sha256")},
             "PUBLIC_METADATA_FILE_ROLE")
        return row
    fields(manifest["production"], ("descriptor", "profile_template"))
    role(manifest["production"]["descriptor"], "production/ARTIFACTS.json")
    role(manifest["production"]["profile_template"], "production/PROFILE-TEMPLATE.json")
    fields(descriptor, ("schema", "foundation", "policy", "relation_image", "aggregate_image", "roles", "sources"))
    need((descriptor["schema"],descriptor["foundation"],descriptor["policy"],descriptor["relation_image"],descriptor["aggregate_image"])
         == (DESCRIPTOR_SCHEMA,FOUNDATION,POLICY,RELATION,IMAGE), "PUBLIC_METADATA_MATHEMATICS")
    fields(descriptor["roles"], ARTIFACTS)
    for name,(filename,size,sha) in ARTIFACTS.items():
        item = role(descriptor["roles"][name], "assets/producer/"+filename)
        need(item["bytes"] == size and item["sha256"] == sha, "PUBLIC_METADATA_ARTIFACT")
    fields(descriptor["sources"], SOURCE_MODULES)
    for name,item in descriptor["sources"].items():
        suffix = name.replace(".", "/")+(".py" if "." in name else "/__init__.py")
        role(item, "sdk/v5/"+suffix)
    fields(template, ("schema", "support_profile", "source_pins", "base_source_pins", "stage_memory_ceiling_mib"))
    need(template["schema"] == TEMPLATE_SCHEMA, "PUBLIC_TEMPLATE_SCHEMA")
    def exact_rows(rows, paths):
        need(type(rows) is list and len(rows) == len(paths), "PUBLIC_METADATA_LIST_LENGTH")
        selected = {}
        for item in rows:
            role(item); need(item["path"] not in selected, "PUBLIC_METADATA_DUPLICATE_PIN")
            selected[item["path"]] = item
        need(set(selected) == set(paths), "PUBLIC_METADATA_EXACT_PIN_PATHS")
        return selected
    core = exact_rows(template["source_pins"], [item["path"] for item in descriptor["sources"].values()])
    need(core == {item["path"]:item for item in descriptor["sources"].values()}, "PUBLIC_METADATA_SOURCE_BINDING")
    exact_rows(template["base_source_pins"], ("sdk/v5/aggregate_small/__init__.py", "sdk/v5/aggregate_small/producer.py"))
    support = template["support_profile"]
    fields(support, ("schema", "supervisor_manifest", "host", "python", "python_dll",
        "source_pins", "runtime_pins", "image_id", "foundation", "policy"))
    need((support["schema"],support["image_id"],support["foundation"],support["policy"])
         == ("DMKN_V5_PRODUCER_PROFILE_V1",IMAGE,FOUNDATION,POLICY)
         and support["host"] == descriptor["roles"]["stage_host"], "PUBLIC_METADATA_SUPPORT")
    role(support["supervisor_manifest"], "base/RELEASE-MANIFEST.json")
    role(support["host"])
    role(support["python"], "base/receiver/runtime/python/python.exe")
    role(support["python_dll"], "base/receiver/runtime/python/python314.dll")
    exact_rows(support["source_pins"], ("sdk/v5/production/__init__.py", "sdk/v5/production/producer.py"))
    exact_rows(support["runtime_pins"], (*core, "sdk/v5/aggregate_small/operator.py",
        "sdk/v5/release_production/operator.py", *("base/receiver/runtime/python/"+name for name in PYTHON_RUNTIME_NAMES)))
    uint(template["stage_memory_ceiling_mib"], 8192, 1)


def materialize_profile(root, manifest_pin, descriptor_pin, template):
    """Derive profile data from an adopted complete release; writes nothing."""
    root = ordinary(root, directory=True)
    manifest = document(manifest_pin, 8*MIB)
    need(Path(manifest_pin["path"]) == root/"V5-RELEASE.json"
         and manifest.get("schema") == MANIFEST_SCHEMA, "PUBLIC_TEMPLATE_RELEASE")
    descriptor = document(descriptor_pin)
    validate_production_metadata(manifest, descriptor, template)
    expected_descriptor = manifest["production"]["descriptor"]
    need(descriptor_pin == {**expected_descriptor,
         "path": str(root.joinpath(*relative(expected_descriptor["path"])))},
         "PUBLIC_MATERIALIZED_DESCRIPTOR_ROLE")
    template_row = manifest["production"]["profile_template"]
    template_pin = {**template_row, "path": str(root.joinpath(*relative(template_row["path"])))}
    need(document(template_pin) == template, "PUBLIC_MATERIALIZED_TEMPLATE_ROLE")
    def materialize(value):
        if type(value) is dict:
            if "path" in value:
                fields(value, ("path", "bytes", "sha256"))
                path = "/".join(relative(value["path"]))
                uint(value["bytes"], 128*MIB, 1); digest(value["sha256"])
                need(manifest["files"].get(path) == {key:value[key] for key in ("bytes", "sha256")},
                     "PUBLIC_TEMPLATE_FILE_ROLE")
                return {**value, "path": str(root.joinpath(*relative(path)))}
            return {key:materialize(item) for key,item in value.items()}
        if type(value) is list:
            need(len(value) <= 128, "PUBLIC_TEMPLATE_LIST_BOUND")
            return [materialize(item) for item in value]
        return value
    selected = materialize(template)
    roles = {name:materialize(pin) for name,pin in descriptor["roles"].items()}
    fields(roles, ("stage_host", "snapshot_host", "guest_image"))
    sources = {materialize(pin)["path"]: materialize(pin) for pin in descriptor["sources"].values()}
    need(type(selected["source_pins"]) is list and len(selected["source_pins"]) == 31
         and len(sources) == 31 and {pin["path"]:pin for pin in selected["source_pins"]} == sources,
         "PUBLIC_TEMPLATE_CORE_CLOSURE")
    support = selected["support_profile"]
    fields(support, ("schema", "supervisor_manifest", "host", "python", "python_dll",
        "source_pins", "runtime_pins", "image_id", "foundation", "policy"))
    need(support["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1" and support["host"] == roles["stage_host"]
         and support["image_id"] == descriptor["aggregate_image"]
         and support["foundation"] == descriptor["foundation"] and support["policy"] == descriptor["policy"],
         "PUBLIC_TEMPLATE_SUPPORT_BINDING")
    uint(selected["stage_memory_ceiling_mib"], 8192, 1)
    common = {"release": dict(manifest_pin), "descriptor": dict(descriptor_pin)}
    profile = {"schema": PROFILE_SCHEMA, "source_pins": selected["source_pins"],
        "release": {"root": str(root), "manifest": dict(manifest_pin), "descriptor": dict(descriptor_pin)},
        "snapshot_host_build": {**common, "snapshot_host": roles["snapshot_host"]},
        "base_profile": {"schema": "DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1", "support_profile": support,
            "source_pins": selected["base_source_pins"], "relation_image": descriptor["relation_image"],
            "host_build": {**common, "stage_host": roles["stage_host"]},
            "image_adoption": {**common, "guest_image": roles["guest_image"]},
            "stage_memory_ceiling_mib": selected["stage_memory_ceiling_mib"]}}
    need(len(encoded(profile)) <= MIB, "PUBLIC_MATERIALIZED_PROFILE_BOUND")
    return profile
