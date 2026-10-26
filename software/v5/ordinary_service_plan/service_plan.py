"""Finite prepaid serving through the unchanged approved ordinary public CLI.

No mathematical admission, publication, automatic retries or indefinite service.
Use approved Python -I -S -B; only the three documented CLI options are accepted.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import ipaddress
import json
import math
import os
from pathlib import Path
import stat
import sys
import time

MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_SERVICE_PLAN_V1"
RESULT_SCHEMA = "DMKN_ORDINARY_SERVICE_PLAN_RESULT_V1"
LAUNCHER_SHA = "47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39"
SOURCES = {
    "run.py": LAUNCHER_SHA,
    "owner.py": "56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a",
    "peer.py": "968d13e4c926b1520cba00502f3e98a87ffda7bdfefa0ec3fcf362c2d3efb655",
    "peer_api.py": "48ec02f0ecf76f44d7ab64e6e029bdfb4f7ccb3aba8513711dd6b07952c917e9",
    "profile.py": "1f40fb7a663c10d8f09132375ac8ab7899dea5830fff4979e0dda66b668003f8",
    "support/transport/http_provider.py": "9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7",
}
SUPPORT = {
    "supervisor": "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9",
    "domains": "651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a",
    "job": "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028",
}
LIMITS = {"wall_seconds": (35, 3600), "cpu_seconds": (4, 200000),
          "memory_mib": (1, 8192), "active_processes": (2, 8),
          "stdout_bytes": (65536, 8*MIB), "stderr_bytes": (65536, 8*MIB)}
INDEX_LIMITS = {"max_objects": (1, 1000000), "max_postings": (1, 128000000),
                "max_features": (1, 1048576), "max_snapshots": (1, 1000001),
                "max_logical_bytes": (1024, 2**40), "max_db_pages": (256, 268435456)}
CUSTODY_LIMITS = {"objects": (1, 1000000), "exports": (1, 16000000),
                  "logical_bytes": (1024, 2**40), "db_pages": (256, 268435456)}
PROVIDER_LIMITS = {"max_connections": (1, 8), "max_requests": (1, 1000000),
                   "max_reply_bytes": (1024, 2**40), "operation_ms": (1, 60000)}


def need(condition, code):
    if not condition:
        raise ValueError("SERVICE_PLAN_"+code)


def fields(value, keys, code):
    need(type(value) is dict and set(value) == set(keys), code)


def integer(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def number(value, code):
    need(type(value) in (int, float) and math.isfinite(value) and value >= 0, code)
    return value


def hexid(value):
    need(type(value) is str and len(value) == 64 and
         all(c in "0123456789abcdef" for c in value), "SHA256")
    return value


def text(value):
    need(type(value) is str and 0 < len(value) <= 32767 and
         all(ord(c) >= 32 for c in value), "TEXT")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def parse(raw, *, reports=False):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(value):
        raise ValueError("SERVICE_PLAN_NONINTEGER_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=float if reports else reject, parse_constant=reject)


def bounds(value, limits, code):
    fields(value, limits, code)
    for key, (low, high) in limits.items():
        integer(value[key], low, high, code+":"+key)


def reference(value):
    fields(value, ("path", "sha256"), "FILE_REFERENCE")
    text(value["path"]); hexid(value["sha256"])


def validate_service(config):
    required = {"index", "host", "port", "tls", "lease_seconds", "cleanup_seconds",
                "limits", "share_all_custody", "exclusive"}
    fields(config, required | ({"authoring_offers"} if "authoring_offers" in config else set()),
           "SERVICE_FIELDS")
    need(config["share_all_custody"] is True and config["exclusive"] is True, "DISCLOSURE_APPROVAL")
    address = ipaddress.ip_address(text(config["host"]))
    need(len(config["host"]) <= 64 and not address.is_unspecified and not address.is_multicast,
         "BIND_ADDRESS")
    integer(config["port"], 1, 65535, "STABLE_NONZERO_PORT")
    integer(config["lease_seconds"], 1, 3600, "LEASE")
    integer(config["cleanup_seconds"], 10, 60, "CLEANUP")
    bounds(config["limits"], PROVIDER_LIMITS, "PROVIDER_LIMITS")
    selected = config["index"]
    fields(selected, {"path", "limits", "create"} |
           ({"access_pairs"} if type(selected) is dict and "access_pairs" in selected else set()), "INDEX_FIELDS")
    text(selected["path"]); need(selected["create"] is False, "EXISTING_INDEX")
    bounds(selected["limits"], INDEX_LIMITS, "INDEX_LIMITS")
    if "access_pairs" in selected:
        pair_config = selected["access_pairs"]
        fields(pair_config, ("pairs", "limits"), "PAIR_FIELDS")
        pairs = pair_config["pairs"]
        need(type(pairs) is list and 1 <= len(pairs) <= 8, "PAIR_COUNT")
        for pair in pairs:
            need(type(pair) is list and len(pair) == 2, "PAIR_SHAPE")
            need(hexid(pair[0]) < hexid(pair[1]), "PAIR_ORDER")
        need(pairs == [list(pair) for pair in sorted(set(map(tuple, pairs)))], "PAIR_ORDER")
        bounds(pair_config["limits"], {"max_rows": (1, 16000000),
               "max_logical_bytes": (1024, 2**40)}, "PAIR_LIMITS")
    if config["tls"] is None:
        need(address.is_loopback, "REMOTE_TLS_REQUIRED")
    else:
        fields(config["tls"], ("cert_file", "cert_sha256", "key_file", "key_sha256"), "TLS_FIELDS")
        for prefix in ("cert", "key"):
            text(config["tls"][prefix+"_file"]); hexid(config["tls"][prefix+"_sha256"])
    if "authoring_offers" in config:
        reference(config["authoring_offers"])
    return deepcopy(config)


def validate_plan(doc, config):
    fields(doc, ("schema", "package", "profile_sha256", "python_runtime", "lean_runtime",
        "catalog", "custody", "store_id", "custody_limits", "config", "leases",
        "horizon_seconds", "runner_cpu_seconds", "operation_limits", "epoch_limits", "aggregate"), "FIELDS")
    need(doc["schema"] == SCHEMA, "SCHEMA")
    for key in ("package", "python_runtime", "lean_runtime", "catalog", "custody"):
        text(doc[key])
    hexid(doc["profile_sha256"]); hexid(doc["store_id"])
    reference(doc["custody_limits"]); reference(doc["config"])
    n = integer(doc["leases"], 1, 96, "LEASE_COUNT")
    integer(doc["horizon_seconds"], 1, 604800, "HORIZON")
    integer(doc["runner_cpu_seconds"], 60, 6000, "RUNNER_CPU")
    bounds(doc["operation_limits"], LIMITS, "OPERATION_LIMITS")
    outer_bounds = dict(LIMITS, wall_seconds=(50, 3660))
    bounds(doc["epoch_limits"], outer_bounds, "EPOCH_LIMITS")
    inner, outer = doc["operation_limits"], doc["epoch_limits"]
    for key, overhead in (("wall_seconds", 15), ("cpu_seconds", 60),
                          ("memory_mib", 128), ("active_processes", 1)):
        need(outer[key] >= inner[key]+overhead, "NESTED_RESERVE:"+key)
    service = validate_service(config)
    need(service["lease_seconds"]+service["cleanup_seconds"]+15 < inner["wall_seconds"],
         "SERVICE_BOOTSTRAP_RESERVE")
    need(doc["horizon_seconds"] >= n*outer["wall_seconds"]+60, "HORIZON_RESERVATION")
    per_logs = inner["stdout_bytes"]+inner["stderr_bytes"]+outer["stdout_bytes"]+outer["stderr_bytes"]+16*MIB
    reserved = {"cpu_seconds": n*outer["cpu_seconds"]+doc["runner_cpu_seconds"],
                "accepted_attempts": n*service["limits"]["max_requests"],
                "reply_bytes": n*service["limits"]["max_reply_bytes"],
                "log_bytes": n*per_logs+4*MIB}
    fields(doc["aggregate"], reserved, "AGGREGATE_FIELDS")
    for key, minimum in reserved.items():
        integer(doc["aggregate"][key], minimum, 2**53-1, "AGGREGATE_RESERVATION:"+key)
    return reserved


def ordinary(value, *, directory=False, fresh=False):
    path = Path(text(str(value)))
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":" and
         path != Path(path.anchor) and len(path.parts) <= 128, "ABSOLUTE_NONROOT_PATH")
    need(all(part not in (".", "..") and not part.endswith((".", " ")) and
             not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts[1:]), "PATH_COMPONENT")
    for parent in reversed(path.parents):
        info = parent.lstat()
        need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "PATH_ANCESTRY")
    if fresh:
        need(not path.exists() and not path.is_symlink(), "FRESH_PATH")
    else:
        info = path.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "REDIRECTED_PATH")
        need(stat.S_ISDIR(info.st_mode) if directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    return path


def read(path, maximum=2*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size and path.stat().st_size == size, "FILE_CHANGED")
    return raw


def pinned(ref, maximum=2*MIB):
    reference(ref)
    raw = read(ref["path"], maximum)
    need(hashlib.sha256(raw).hexdigest() == ref["sha256"], "FILE_PIN")
    return raw


def report_agreement(first, second):
    a, b = parse(first, reports=True), parse(second, reports=True)
    need(canonical(a) == canonical(b), "REPORT_AGREEMENT")
    return a


def selected_identities(manifest):
    """Reproduce the published ordinary implementation-claim identity encoding."""
    need(type(manifest) is dict and manifest.get("schema") == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1",
         "INSTALLATION_SCHEMA")
    claim = manifest.get("implementation")
    fields(claim, ("schema", "semantic_id", "platform", "kernel_support", "adapter_support",
        "basis_receiver_support", "controller_support", "snapshot_support", "snapshot_format", "support_scope"),
        "IMPLEMENTATION_FIELDS")
    need(claim["schema"] == "DMKN_ORDINARY_IMPLEMENTATION_CLAIM_V1", "IMPLEMENTATION_SCHEMA")
    semantic = hexid(claim["semantic_id"])
    for key in ("kernel_support", "adapter_support", "basis_receiver_support", "controller_support", "snapshot_support"):
        hexid(claim[key])
    raw = json.dumps(claim, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return {"semantic_id": semantic,
            "implementation_id": hashlib.sha256(b"DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1\0"+raw).hexdigest()}


def validate_paths(plan, config, plan_path, output, own_directory):
    """Filesystem-only preflight, including indirect TLS/offer input paths."""
    def overlaps(a, b):
        return a.is_relative_to(b) or b.is_relative_to(a)
    output = ordinary(output, directory=True, fresh=True)
    supports = [ordinary(plan[key], directory=True) for key in ("package", "python_runtime", "lean_runtime")]
    state = [ordinary(plan[key], directory=True) for key in ("catalog", "custody")]
    state.append(ordinary(config["index"]["path"], directory=True))
    directories = [output, *supports, *state, ordinary(own_directory, directory=True)]
    for i, left in enumerate(directories):
        need(all(not overlaps(left, right) for right in directories[i+1:]), "PATH_OVERLAP")
    controls = [ordinary(plan_path), ordinary(plan["config"]["path"]), ordinary(plan["custody_limits"]["path"])]
    indirect = []
    if config["tls"] is not None:
        indirect.extend({"path": config["tls"][prefix+"_file"], "sha256": config["tls"][prefix+"_sha256"]}
                        for prefix in ("cert", "key"))
    if "authoring_offers" in config:
        indirect.append(config["authoring_offers"])
    for ref in indirect:
        controls.append(ordinary(ref["path"])); pinned(ref, MIB)
    for path in controls:
        need(all(not overlaps(path, target) for target in [output, *state]), "INPUT_STATE_OUTPUT_OVERLAP")
    return {"output": output, "supports": supports, "state": state, "indirect": indirect}


def clean_supervision(report, limits):
    need(type(report) is dict and report.get("schema") == "DMKN_V4_OWNER_COMMAND_REPORT_V1" and
         report.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and "error" not in report and
         report.get("child_exit_code") == 0 and type(report.get("child_exit_code")) is int and
         report.get("direct_child_reaped") is True and report.get("job_closed") is True and
         report.get("termination_requested") is False and report.get("cleanup_errors") == [], "UNCLEAN_SUPERVISION")
    need(canonical(report.get("limits")) == canonical(limits), "SUPERVISION_LIMIT_BINDING")
    job = report.get("final_job")
    need(type(job) is dict, "FINAL_JOB")
    for key in ("active_processes", "terminated_processes"):
        integer(job.get(key), 0, 0, "UNSETTLED_JOB:"+key)
    cpu = number(job.get("cpu_seconds"), "JOB_CPU")
    need(cpu <= limits["cpu_seconds"], "OBSERVED_CPU")
    need(number(report.get("wall_seconds_through_cleanup"), "OBSERVED_WALL") <= limits["wall_seconds"],
         "OBSERVED_WALL")
    logs = report.get("observed_logs")
    fields(logs, ("stdout_bytes", "stderr_bytes"), "OBSERVED_LOGS")
    for key in logs:
        integer(logs[key], 0, limits[key], "OBSERVED_LOG:"+key)
    return cpu


def validate_epoch(outer, run_report, inner, peer_report, expected):
    """Pure checks; caller separately binds actual stdout/files and raw sizes."""
    plan, config = expected["plan"], expected["config"]
    cpu = clean_supervision(outer, plan["epoch_limits"])
    clean_supervision(inner, plan["operation_limits"])
    need(type(run_report) is dict and run_report.get("schema") == "DMKN_ORDINARY_BOUNDED_OPERATION_V1" and
         run_report.get("ok") is True and run_report.get("status") == "CLI_EXITED_ZERO" and
         run_report.get("tool") == "peer" and run_report.get("child_exit_code") == 0 and
         type(run_report.get("child_exit_code")) is int and
         run_report.get("child_supervision_status") == "COMMAND_EXITED_ZERO_AND_CLOSED", "RUN_REPORT")
    for key in ("error", "report_error"):
        need(key not in run_report, "RUN_ERROR")
    need(run_report.get("profile_sha256") == plan["profile_sha256"] and
         run_report.get("installation_manifest_sha256") == expected["installation_manifest_sha256"] and
         run_report.get("diagnostics") == expected["diagnostics"] and
         canonical(run_report.get("limits")) == canonical(plan["operation_limits"]), "RUN_BINDING")
    need(type(peer_report) is dict and peer_report.get("ok") is True and
         peer_report.get("operation") == "serve", "PEER_REPORT")
    for key in ("error", "close_errors", "final_budget_error", "report_write_error", "serialization_error"):
        need(key not in peer_report, "PEER_ERROR")
    for key in ("profile_sha256", "store_id", "catalog", "custody"):
        need(peer_report.get(key) == plan[key], "PEER_BINDING:"+key)
    need(peer_report.get("config_sha256") == plan["config"]["sha256"], "PEER_CONFIG_BINDING")
    for key in ("implementation_id", "semantic_id"):
        need(hexid(peer_report.get(key)) == expected[key], "PEER_IDENTITY_BINDING:"+key)
    result = peer_report.get("result")
    need(type(result) is dict and result.get("operation") == "serve" and
         result.get("status") == "LEASE_FINISHED" and result.get("quiescent") is True and
         result.get("cleanup_errors") == [] and result.get("mathematical_acceptance") is False, "LEASE_RESULT")
    ready = result.get("ready")
    need(type(ready) is dict and ready.get("status") == "READY" and
         ready.get("host") == config["host"] and ready.get("port") == config["port"] and
         type(ready.get("port")) is int and ready.get("tls") is (config["tls"] is not None) and
         ready.get("lease_seconds") == config["lease_seconds"] and type(ready.get("lease_seconds")) is int and
         ready.get("shared_custody") == plan["custody"] and ready.get("index") == config["index"]["path"] and
         ready.get("mathematical_acceptance") is False, "READY_BINDING")
    if "authoring_offers" in config:
        need(result.get("authoring_map_sha256") == config["authoring_offers"]["sha256"], "OFFER_BINDING")
    p = result.get("provider")
    counter_keys = {"requests", "request_bytes", "reply_bytes", "header_bytes", "reserved_reply_bytes",
                    "active", "accepted_attempts", "handshakes", "handshake_failures", "accept_failures",
                    "cleanup_pending", "cleanup_failures", "failures", "refused"}
    fields(p, counter_keys | {"accepting", "admission_exhausted", "mathematical_acceptance"}, "PROVIDER_FIELDS")
    for key in counter_keys:
        integer(p[key], 0, 2**53-1, "PROVIDER_COUNTER:"+key)
    need(all(p[key] == 0 for key in ("reserved_reply_bytes", "active", "handshakes", "cleanup_pending",
                                    "accept_failures", "cleanup_failures")) and
         p["accepting"] is False and p["mathematical_acceptance"] is False, "PROVIDER_CLOSURE")
    cap = config["limits"]
    need(p["requests"] <= p["accepted_attempts"] <= cap["max_requests"] and
         p["handshake_failures"] <= p["accepted_attempts"] and
         p["handshake_failures"] <= p["failures"] and p["refused"] <= p["accepted_attempts"] and
         p["reply_bytes"] <= cap["max_reply_bytes"] and
         p["admission_exhausted"] is (p["accepted_attempts"] >= cap["max_requests"]), "PROVIDER_ACCOUNTING")
    return {"outer_job_cpu_seconds": cpu, "accepted_attempts": p["accepted_attempts"],
            "reply_bytes": p["reply_bytes"], "provider": deepcopy(p),
            "inner_logs_bytes": sum(inner["observed_logs"].values()),
            "outer_logs_bytes": sum(outer["observed_logs"].values())}


def _sequence(plan, invoke, record, check_inputs, clock, cpu, *, origins=None):
    """Internal injection seam for deterministic tests; never a public hook."""
    begun, cpu_begun = (clock(), cpu()) if origins is None else origins
    result = {"schema": RESULT_SCHEMA, "ok": False, "status": "STOPPED", "finished": 0,
              "epochs": [], "observed_outer_job_cpu_seconds": 0,
              "observed_accepted_attempts": 0, "observed_reply_bytes": 0,
              "observed_stream_log_bytes": 0, "mathematical_acceptance": False,
              "epoch_accounting_scope": "VALIDATED_COMPLETED_EPOCHS_ONLY;ALL_ATTEMPT_CPU_REPORTED_SEPARATELY"}
    def eligible():
        need(clock()-begun+plan["epoch_limits"]["wall_seconds"]+25 < plan["horizon_seconds"], "ORIGINAL_HORIZON")
        need(cpu()-cpu_begun < plan["runner_cpu_seconds"], "RUNNER_CPU_EXHAUSTED")
    try:
        for position in range(plan["leases"]):
            # Existing supervisor failure cleanup may wait 10+10 seconds outside
            # its sampled wall limit. Never spend that reserve on another epoch.
            eligible()
            check_inputs()
            record("intent", position, {"epoch": position+1, "operation": "serve",
                "profile_sha256": plan["profile_sha256"], "config_sha256": plan["config"]["sha256"],
                "epoch_limits": plan["epoch_limits"], "operation_limits": plan["operation_limits"]})
            eligible()  # Input validation and durable intent did not renew time.
            row = invoke(position)
            result["epochs"].append(row); result["finished"] += 1
            result["observed_outer_job_cpu_seconds"] += row["outer_job_cpu_seconds"]
            result["observed_accepted_attempts"] += row["accepted_attempts"]
            result["observed_reply_bytes"] += row["reply_bytes"]
            result["observed_stream_log_bytes"] += row["inner_logs_bytes"]+row["outer_logs_bytes"]
            record("complete", position, row)
            need(clock()-begun < plan["horizon_seconds"] and cpu()-cpu_begun < plan["runner_cpu_seconds"],
                 "ORIGINAL_ALLOWANCE_EXHAUSTED")
            for actual, key in ((result["observed_outer_job_cpu_seconds"]+cpu()-cpu_begun, "cpu_seconds"),
                                (result["observed_accepted_attempts"], "accepted_attempts"),
                                (result["observed_reply_bytes"], "reply_bytes"),
                                (result["observed_stream_log_bytes"], "log_bytes")):
                need(actual <= plan["aggregate"][key], "OBSERVED_AGGREGATE:"+key)
        result.update(ok=True, status="FINITE_PLAN_FINISHED")
    except BaseException as error:
        result.update(error_type=type(error).__name__, error=str(error)[:500],
                      state_disposition="PRESERVED_NO_RESUME_OR_AUTOMATIC_RETRY")
    result.update(wall_seconds=clock()-begun, runner_cpu_seconds=cpu()-cpu_begun)
    return result


def _load_launcher(package):
    path = ordinary(package/"run.py")
    raw = read(path)
    need(hashlib.sha256(raw).hexdigest() == LAUNCHER_SHA, "KNOWN_LAUNCHER_PIN")
    spec = importlib.util.spec_from_file_location("_service_plan_checked_launcher", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def execute(plan_path, plan_sha256, output):
    started, started_cpu = time.monotonic(), time.process_time()
    output_path = None
    attempted = []
    result = {"schema": RESULT_SCHEMA, "ok": False, "status": "NO_EPOCH_LAUNCHED", "finished": 0,
              "mathematical_acceptance": False}
    try:
        need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
             sys.dont_write_bytecode and not sys.flags.optimize, "APPROVED_PYTHON_PROFILE")
        plan_path = ordinary(plan_path)
        plan_raw = pinned({"path": str(plan_path), "sha256": hexid(plan_sha256)}, 65536)
        plan = parse(plan_raw)
        need(type(plan) is dict and "config" in plan, "PLAN_OBJECT")
        config_raw = pinned(plan["config"])
        config = parse(config_raw)
        reservations = validate_plan(plan, config)
        paths = validate_paths(plan, config, plan_path, output, Path(__file__).absolute().parent)
        output = paths["output"]
        package = ordinary(plan["package"], directory=True)
        launcher = _load_launcher(package)
        def bootstrap_check():
            need(time.monotonic()-started < 60 and time.process_time()-started_cpu < 60, "PREFLIGHT_LIMIT")
        bound = launcher.bind_support(package, plan["profile_sha256"], Path(plan["python_runtime"]), bootstrap_check)
        for role, digest in SUPPORT.items():
            need(hashlib.sha256(bound["support"][role][1]).hexdigest() == digest, "KNOWN_SUPERVISOR:"+role)
        profile = parse(read(package/"PROFILE.json"))
        manifest_raw = read(package/"installation"/"INSTALLATION.json")
        need(hashlib.sha256(manifest_raw).hexdigest() == bound["installation_manifest_sha256"], "INSTALLATION_PIN")
        identities = selected_identities(parse(manifest_raw))
        pins = [{"path": str(plan_path), "sha256": plan_sha256}, plan["config"], plan["custody_limits"],
                {"path": str(package/"PROFILE.json"), "sha256": plan["profile_sha256"]}]
        for name, digest in SOURCES.items():
            need(profile["files"][name]["sha256"] == digest, "KNOWN_INTERFACE:"+name)
            pins.append({"path": str(package/name), "sha256": digest})
        bounds(parse(pinned(plan["custody_limits"], 65536)), CUSTODY_LIMITS, "CUSTODY_LIMITS")
        pins.extend(paths["indirect"])
        def check_inputs():
            need(time.monotonic()-started < plan["horizon_seconds"] and
                 time.process_time()-started_cpu < plan["runner_cpu_seconds"], "ORIGINAL_ALLOWANCE")
            for ref in pins:
                pinned(ref)
            current = launcher.bind_support(package, plan["profile_sha256"], Path(plan["python_runtime"]), lambda: None)
            need(current["installation_manifest_sha256"] == bound["installation_manifest_sha256"], "INSTALLATION_CHANGED")
            for role, digest in SUPPORT.items():
                need(hashlib.sha256(current["support"][role][1]).hexdigest() == digest, "SUPERVISOR_CHANGED")
            for path in [*paths["supports"], *paths["state"]]:
                ordinary(path, directory=True)
        check_inputs(); bootstrap_check()
        supervisor, job_class = launcher.load_supervision(bound)
        supervisor.limits_checked(plan["epoch_limits"])
        original_environment = supervisor.child_environment
        def environment(cwd):
            env = original_environment(cwd)
            py = Path(plan["python_runtime"])
            env["PATH"] = os.pathsep.join(map(str, (py, py/"DLLs", Path(plan["lean_runtime"])/"bin")))
            return env
        supervisor.child_environment = environment
        output.mkdir()  # Atomic claim. Nothing resumes or reuses this directory.
        output_path = output
        supervisor.save_new(output/"PLAN.json", {"plan_sha256": plan_sha256, "plan": plan,
            "reservations": reservations, "installation_manifest_sha256": bound["installation_manifest_sha256"]})
        def record(kind, position, value):
            epoch = output/('epoch-%04d' % (position+1))
            if kind == "intent":
                epoch.mkdir()
            supervisor.save_new(epoch/(kind.upper()+".json"), value)
        def invoke(position):
            epoch = output/('epoch-%04d' % (position+1))
            inner_path, service_path = epoch/"inner", epoch/"service"
            argv = [str(Path(plan["python_runtime"])/"python.exe"), "-I", "-S", "-B", str(package/"run.py"),
                    "--profile-sha256", plan["profile_sha256"], "--python-runtime", plan["python_runtime"],
                    "--lean-runtime", plan["lean_runtime"], "--diagnostics", str(inner_path)]
            for key, value in plan["operation_limits"].items():
                argv.extend(("--"+key.replace("_", "-"), str(value)))
            argv.extend(("peer", "--", "serve", "--catalog", plan["catalog"], "--custody", plan["custody"],
                         "--store-id", plan["store_id"], "--custody-limits", plan["custody_limits"]["path"],
                         "--config", plan["config"]["path"], "--config-sha256", plan["config"]["sha256"],
                         "--output", str(service_path)))
            attempt = {"epoch": position+1, "outer_job_cpu_seconds": None, "outcome": "UNKNOWN"}
            need(time.monotonic()-started+plan["epoch_limits"]["wall_seconds"]+25 < plan["horizon_seconds"],
                 "ORIGINAL_HORIZON_BEFORE_LAUNCH")
            need(time.process_time()-started_cpu < plan["runner_cpu_seconds"], "RUNNER_CPU_BEFORE_LAUNCH")
            attempted.append(attempt)
            outer = supervisor.supervise(argv, epoch, epoch/"outer", plan["epoch_limits"], job_class)
            attempt["outcome"] = outer.get("status", "UNKNOWN")
            final_job = outer.get("final_job")
            if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float) and math.isfinite(final_job["cpu_seconds"]) and final_job["cpu_seconds"] >= 0:
                attempt["outer_job_cpu_seconds"] = final_job["cpu_seconds"]
            supervisor.save_new(epoch/"OUTER.json", outer)
            clean_supervision(outer, plan["epoch_limits"])
            run_report = report_agreement(read(inner_path/"RUN.json"),
                read(epoch/"outer"/"stdout.txt", plan["epoch_limits"]["stdout_bytes"]))
            inner = parse(read(inner_path/"SUPERVISION.json"), reports=True)
            peer_report = report_agreement(read(service_path/"RESULT.json"),
                read(inner_path/"child"/"stdout.txt", plan["operation_limits"]["stdout_bytes"]))
            expected = {"plan": plan, "config": config, "diagnostics": str(inner_path),
                        "installation_manifest_sha256": bound["installation_manifest_sha256"], **identities}
            accounting = validate_epoch(outer, run_report, inner, peer_report, expected)
            ready = parse(read(service_path/"READY.json"), reports=True)
            need(canonical(ready) == canonical(peer_report["result"]["ready"]), "READY_FILE_AGREEMENT")
            check_inputs()
            return dict(epoch=position+1, **accounting)
        # Clock/CPU origins include preflight rather than renewing at sequence entry.
        result = _sequence(plan, invoke, record, check_inputs,
                           lambda: time.monotonic()-started, lambda: time.process_time()-started_cpu,
                           origins=(0, 0))
        result.update(plan_sha256=plan_sha256, profile_sha256=plan["profile_sha256"], reservations=reservations,
                      installation_manifest_sha256=bound["installation_manifest_sha256"],
                      boundary="FINITE_PREPAID_SERVICE_NOT_CONTINUOUS_AVAILABILITY_OR_FINAL_V5")
    except BaseException as error:
        result.update(ok=False, error_type=type(error).__name__, error=str(error)[:500],
                      state_disposition="PRESERVED_NO_RESUME_OR_AUTOMATIC_RETRY")
    result["wall_seconds_before_final_report"] = time.monotonic()-started
    result["runner_cpu_seconds_before_final_report"] = time.process_time()-started_cpu
    result["attempts"] = attempted
    result["known_attempt_job_cpu_seconds"] = sum(row["outer_job_cpu_seconds"] or 0 for row in attempted)
    result["attempt_cpu_accounting_complete"] = all(row["outer_job_cpu_seconds"] is not None for row in attempted)
    result["cost_scope"] = "KNOWN_ATTEMPT_JOB_CPU_PLUS_RUNNER_CPU_BEFORE_FINAL_REPORT;FINAL_WRITE_PRINT_EXCLUDED;INNER_JOB_INCLUDED;UNKNOWN_COST_NOT_ZERO"
    if output_path is not None:
        try:
            raw = canonical(result)+b"\n"
            need(len(raw) <= MIB, "RESULT_BOUND")
            with (output_path/"RESULT.json").open("xb") as stream:
                stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        except BaseException as error:
            result.update(ok=False, status="RESULT_WRITE_FAILED", report_error=type(error).__name__)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("plan", "plan-sha256", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    result = execute(args.plan, args.plan_sha256, args.output)
    print(canonical(result).decode("utf-8"), flush=True)
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
