"""Compact owner facade; no operational reply is mathematical proof authority.

Source-only until root adopts/tests/packages. Exact release plus cooperative owner
filesystem is required. One finite process tree per call; failed state is retained.
"""
from __future__ import annotations
import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

MIB = 1024**2
HEX = r"[0-9a-f]{64}"
PROFILE_SHA = "da89c714e188a8b61da06a044e51acc2bdfd3e7972d699bac87b83e5422d15a2"
PROFILE_BYTES = 1882214
CEILINGS = {"cpu_seconds": 200000, "wall_seconds": 86400, "memory_mib": 8192,
            "active_processes": 8, "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB}
CODEC_FILES = {"fragment_peer.py", "fragment_index.py", "cert_capsule.py", "cert_bundle.py",
    "cert_fragments.py", "cert_stages.py", "assets/schema.json", "assets/registry.json",
    "helpers/peer_wire.py", "helpers/peer_service.py", "FRAGMENT-NETWORK-API.md"}
BOOTSTRAP = {"python": "runtime/python/python.exe", "python_dll": "runtime/python/python314.dll",
             "job": "helpers/run_stage.py", "domains": "helpers/domains.py"}
WORKFLOW_FILES = {"cert_workflow.py", "cert_capsule.py", "cert_bundle.py", "cert_fragments.py",
                  "cert_stages.py", "proof_compose.py", "cert_application.py", "bin/native_relation.exe", "bin/receipt_verifier.exe"}
PATH_FLAGS = {"--run", "--parent", "--local-definition", "--local-fragment", "--fragment",
              "--application-plan", "--expected-capsule"}
WORKFLOW_FLAGS = PATH_FLAGS | {"--cpu-budget-seconds", "--deadline-utc"}
OWNER_OPERATIONS = {"status", "join", "offer", "publish", "withdraw", "providers", "find", "acquire", "maintain", "stop"}

def need(ok, code):
    if not ok:
        raise ValueError(code)


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("NONINTEGER_JSON_NUMBER")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def absolute(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor), "ABSOLUTE_NONROOT_LOCAL_PATH")
    need(all(part not in (".", "..") and not part.endswith((".", " "))
             and not os.path.isreserved(part) and not any(ord(c) < 32 or c in ':*?"<>|' for c in part)
             for part in path.parts[1:]), "ORDINARY_PATH_COMPONENT")
    for ancestor in reversed(path.parents):
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "ORDINARY_PATH_ANCESTRY")
    if fresh:
        need(not path.exists() and not path.is_symlink(), "FRESH_PATH_REQUIRED")
    else:
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
             "ORDINARY_PATH_TARGET")
    need(path.resolve(strict=not fresh) == path, "CANONICAL_PATH_REQUIRED")
    return path


def safe_relative(name):
    need(type(name) is str and 0 < len(name) <= 1024 and "\\" not in name, "RELATIVE_NAME")
    p = PurePosixPath(name)
    need(p.parts and not p.is_absolute() and p.as_posix() == name
         and all(x not in (".", "..") and not x.endswith((".", " "))
                 and not os.path.isreserved(x) and not any(ord(c) < 32 or c in ':*?"<>|' for c in x)
                 for x in p.parts), "SAFE_RELATIVE_NAME")
    return p.parts


def bounded_read(path, limit):
    absolute(path)
    need(0 < path.stat().st_size <= limit, "INPUT_BYTE_LIMIT")
    with path.open("rb") as stream:
        raw = stream.read(limit+1)
    need(0 < len(raw) <= limit, "INPUT_GREW")
    return raw


def pin(path):
    absolute(path)
    size = path.stat().st_size
    need(0 <= size <= 128*MIB, "SELECTED_CODE_BYTE_LIMIT")
    h, observed = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            observed += len(block)
            need(observed <= 128*MIB, "SELECTED_CODE_GREW")
            h.update(block)
    need(observed == size, "SELECTED_CODE_CHANGED_SIZE")
    return {"bytes": observed, "sha256": h.hexdigest()}


def overlap(a, b):
    return a.is_relative_to(b) or b.is_relative_to(a)


def limits_checked(limits):
    need(type(limits) is dict and set(limits) == set(CEILINGS), "EXPLICIT_FINITE_LIMITS")
    for name, ceiling in CEILINGS.items():
        need(type(limits[name]) is int and 1 <= limits[name] <= ceiling, "LIMIT_RANGE:"+name)
    return dict(limits)


def save_new(path, value):
    raw = (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)+"\n").encode()
    need(len(raw) <= MIB, "OPERATIONAL_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def child_environment(root):
    # OS configuration (including SYSTEMROOT/TEMP) remains owner supplied.
    # Disable language/search-path injection; use only bundled executable dirs.
    result = {k: v for k, v in os.environ.items()
              if not k.upper().startswith(("PYTHON", "LEAN", "RUST", "CARGO", "RISC0", "NODE"))
              and k.upper() not in {"PATH", "VIRTUAL_ENV"}}
    result["PATH"] = os.pathsep.join(str(root / "receiver" / suffix)
        for suffix in ("bin", "runtime/python", "runtime/python/DLLs"))
    return result


def settle_after_exit(job, stdout_path, stderr_path, limits, started, wrapper_cpu,
                      record, *, clock=None, cpu=None, pause=None, max_total_processes=None):
    """Allow at most one second of natural Job settlement inside original limits."""
    clock = time.monotonic if clock is None else clock
    cpu = time.process_time if cpu is None else cpu
    pause = time.sleep if pause is None else pause
    until = min(clock()+1.0, started+limits["wall_seconds"])
    while True:
        observed = job.stats()
        lengths = {"stdout_bytes": stdout_path.stat().st_size,
                   "stderr_bytes": stderr_path.stat().st_size}
        record["last_observed_job"] = observed
        record["observed_logs"] = lengths
        current = clock()
        if (current-started > limits["wall_seconds"]
            or observed["cpu_seconds"] > limits["cpu_seconds"]
            or (max_total_processes is not None and observed["total_processes"] > max_total_processes)
            or any(lengths[k] > limits[k] for k in lengths)):
            record["status"] = "RESOURCE_LIMIT"
            raise RuntimeError("OWNER_COMMAND_RESOURCE_LIMIT")
        need(cpu()-wrapper_cpu <= 60, "WRAPPER_CONTROLLER_CPU_LIMIT")
        if observed["active_processes"] == 0 or current >= until:
            return observed
        pause(min(0.05, until-current))


def supervise(argv, cwd, evidence, limits, job_class, *, started=None, stdin_bytes=None, serve_seconds=None):
    """One child Job. Caller has adopted code/paths; no mathematical status parsing."""
    limits = limits_checked(limits)
    started = time.monotonic() if started is None else started
    wrapper_cpu = time.process_time()
    job, process = None, None
    record = {"schema": "DMKN_V4_OWNER_COMMAND_REPORT_V1", "status": "COMMAND_FAILED",
        "authority": "LOCAL_OPERATION_REPORT_NOT_MATHEMATICAL_ACCEPTANCE", "argv": argv,
        "cwd": str(cwd), "limits": limits, "child_exit_code": None, "direct_child_reaped": False,
        "final_job": None, "last_observed_job": None, "job_closed": False,
        "cleanup_errors": [], "termination_requested": False,
        "cpu_scope": "NATIVE_JOB_USER_TIME_LIMIT_AND_SAMPLED_JOB_USER_PLUS_KERNEL;WRAPPER_SEPARATE",
        "limits_scope": "WALL_TOTAL_CPU_AND_LOG_CAPS_SAMPLED_NOT_HARD_DISK_CAPS"}
    evidence.mkdir()
    save_new(evidence / "command.json", {"argv": argv, "cwd": str(cwd), "limits": limits})
    stdout_path, stderr_path = evidence / "stdout.txt", evidence / "stderr.txt"
    failure = None
    input_stream = None
    serve_stopped = False
    if stdin_bytes is not None:
        need(isinstance(stdin_bytes, bytes) and 0 < len(stdin_bytes) <= MIB, "STDIN_FILE_BOUND")
        with (evidence / "stdin.jsonl").open("xb") as stream:
            stream.write(stdin_bytes); stream.flush(); os.fsync(stream.fileno())
        input_stream = (evidence / "stdin.jsonl").open("rb")
    need(serve_seconds is None or (type(serve_seconds) is int and 1 <= serve_seconds <= limits["wall_seconds"]-15 and stdin_bytes is None),
         "FINITE_SERVICE_LEASE")
    launched = time.monotonic()
    try:
        with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            job = job_class(limits["cpu_seconds"], limits["memory_mib"], active_processes=limits["active_processes"])
            process = subprocess.Popen(argv, cwd=cwd, env=child_environment(cwd), stdin=subprocess.PIPE if serve_seconds is not None else input_stream or subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=0x4 | subprocess.CREATE_NO_WINDOW)
            job.attach_resume(process)
            while True:
                if serve_seconds is not None and not serve_stopped and time.monotonic()-launched >= serve_seconds:
                    process.stdin.write(b'{"id":"lease-stop","request":{"operation":"stop"}}\n')
                    process.stdin.flush(); process.stdin.close()
                    serve_stopped = True
                observed = job.stats()
                record["last_observed_job"] = observed
                lengths = {"stdout_bytes": stdout_path.stat().st_size, "stderr_bytes": stderr_path.stat().st_size}
                record["observed_logs"] = lengths
                if (time.monotonic()-started > limits["wall_seconds"]
                    or observed["cpu_seconds"] > limits["cpu_seconds"]
                    or any(lengths[k] > limits[k] for k in lengths)):
                    record["status"] = "RESOURCE_LIMIT"
                    raise RuntimeError("OWNER_COMMAND_RESOURCE_LIMIT")
                need(time.process_time()-wrapper_cpu <= 60, "WRAPPER_CONTROLLER_CPU_LIMIT")
                if process.poll() is not None:
                    record["child_exit_code"] = process.returncode
                    settle_after_exit(job, stdout_path, stderr_path, limits, started, wrapper_cpu, record)
                    record["status"] = "COMMAND_EXITED_ZERO_AND_CLOSED" if process.returncode == 0 else "COMMAND_FAILED"
                    break
                time.sleep(0.05)
    except BaseException as exc:
        failure = type(exc).__name__+": "+str(exc)[:2000]
        record["error"] = failure
        if record["status"] != "RESOURCE_LIMIT":
            record["status"] = "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "COMMAND_FAILED"
    finally:
        if input_stream is not None:
            input_stream.close()
        if serve_seconds is not None and process is not None and process.stdin is not None:
            try:
                process.stdin.close()
            except BaseException as exc:
                record["cleanup_errors"].append("stdin.close:"+type(exc).__name__)
        # Also kill/reap the direct suspended child when assignment never worked.
        # A successful CLI may not leave a background descendant behind.
        cleanup_needed = failure is not None
        if job is not None:
            try:
                record["final_job"] = job.stats()
                record["last_observed_job"] = record["final_job"]
                cleanup_needed = cleanup_needed or record["final_job"]["active_processes"] != 0
            except BaseException as exc:
                record["final_job"] = None
                cleanup_needed = True
                record["cleanup_errors"].append("final_job:"+type(exc).__name__)
        if cleanup_needed:
            if record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED":
                record["status"] = "DESCENDANTS_REQUIRED_TERMINATION"
            if job is not None:
                try:
                    job.kill(); record["termination_requested"] = True
                except BaseException as exc:
                    record["cleanup_errors"].append("job.kill:"+type(exc).__name__)
            if process is not None:
                try:
                    if process.poll() is None:
                        process.kill(); record["termination_requested"] = True
                except BaseException as exc:
                    record["cleanup_errors"].append("direct.kill:"+type(exc).__name__)
        if process is not None:
            try:
                process.wait(timeout=10)
                record["child_exit_code"] = process.returncode
                record["direct_child_reaped"] = True
            except BaseException as exc:
                record["cleanup_errors"].append("direct.wait:"+type(exc).__name__)
        if job is not None:
            try:
                settle = time.monotonic()+10
                while True:
                    record["final_job"] = job.stats()
                    record["last_observed_job"] = record["final_job"]
                    if record["final_job"]["active_processes"] == 0:
                        break
                    if time.monotonic() >= settle:
                        raise RuntimeError("ACTIVE_DESCENDANTS_REMAIN")
                    time.sleep(0.05)
            except BaseException as exc:
                record["final_job"] = None
                record["cleanup_errors"].append("job.quiesce:"+type(exc).__name__)
            try:
                job.close(); record["job_closed"] = True
            except BaseException as exc:
                record["cleanup_errors"].append("job.close:"+type(exc).__name__)
        if (record["cleanup_errors"] or (process is not None and not record["direct_child_reaped"])
            or (job is not None and (record["final_job"] is None
                or record["final_job"].get("active_processes") != 0 or not record["job_closed"]))):
            record["status"] = "CLEANUP_UNCERTAIN"
        record["service_orderly_stop_sent"] = serve_stopped
        record["wrapper_supervision_cpu_seconds"] = time.process_time()-wrapper_cpu
        record["wall_seconds_through_cleanup"] = time.monotonic()-started
        record["observed_logs"] = {name: path.stat().st_size if path.exists() else 0
            for name, path in (("stdout_bytes", stdout_path), ("stderr_bytes", stderr_path))}
        # Recheck after closure so a fast child cannot evade the last sample.
        if (record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
            and (record["wall_seconds_through_cleanup"] > limits["wall_seconds"]
                or record["final_job"]["cpu_seconds"] > limits["cpu_seconds"]
                or any(record["observed_logs"][k] > limits[k] for k in record["observed_logs"]))):
            record["status"] = "RESOURCE_LIMIT"
        if (record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED"
            and record["final_job"].get("terminated_processes") != 0):
            record["status"] = "JOB_REPORTED_TERMINATION_OR_UNKNOWN_COUNTER"
        if record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" and serve_seconds is not None and not serve_stopped:
            record["status"] = "SERVICE_EXITED_BEFORE_ORDERLY_LEASE_STOP"
    return record


class Release:
    def __init__(self, manifest, expected_sha):
        self.manifest = absolute(manifest)
        self.root = self.manifest.parent
        need(re.fullmatch(HEX, expected_sha or ""), "EXTERNAL_MANIFEST_PIN_REQUIRED")
        raw = bounded_read(self.manifest, 8*MIB)
        need(hashlib.sha256(raw).hexdigest() == expected_sha, "RELEASE_MANIFEST_PIN")
        value = strict(raw)
        need(type(value) is dict and set(value) == {"schema", "release", "profile", "files"}
             and value["schema"] == "DMKN_COMPACT_COMMONS_RELEASE_V1"
             and value["release"] == "v4-2026-10-06-compact" and value["profile"] == "receiver/profile.json",
             "RELEASE_MANIFEST_FIELDS")
        self.files, self.expected_sha = value["files"], expected_sha
        need(type(self.files) is dict and 1 <= len(self.files) <= 20000, "RELEASE_FILE_COUNT")
        names, total = set(), 0
        for name, row in self.files.items():
            safe_relative(name)
            need(name.casefold() not in names and name != self.manifest.name, "RELEASE_CASE_ALIAS_OR_SELF")
            names.add(name.casefold())
            need(type(row) is dict and set(row) == {"bytes", "sha256"}
                 and type(row["bytes"]) is int and 0 <= row["bytes"] <= 128*MIB
                 and type(row["sha256"]) is str and re.fullmatch(HEX, row["sha256"]), "RELEASE_FILE_PIN")
            total += row["bytes"]
        need(total <= 1024*MIB, "COMPACT_RELEASE_BYTE_BOUND")
        self.profile = self.root / "receiver/profile.json"
        need(self.files.get("receiver/profile.json") == {"bytes": PROFILE_BYTES, "sha256": PROFILE_SHA},
             "EXACT_ADOPTED_PROFILE")
        self.verify("receiver/profile.json")
        profile = strict(bounded_read(self.profile, 8*MIB))
        need(profile["schema"] == "DMKN_INSTALLED_CERTIFIED_PROFILE_V5"
             and profile["profile_id"] == "dmkn-experimental-certified-definitions-01", "PROFILE_SCHEMA")
        self.assets, self.roles = profile["assets"], profile["roles"]
        for role, name in BOOTSTRAP.items():
            need(self.roles.get(role) == name, "EXACT_BOOTSTRAP_ROLE")
        need(self.roles.get("workflow") == "cert_workflow.py", "EXACT_WORKFLOW_ROLE")
        need(self.roles.get("native_relation") == "bin/native_relation.exe", "EXACT_NATIVE_RELATION_ROLE")
        need(self.roles.get("receipt_verifier") == "bin/receipt_verifier.exe", "EXACT_RECEIPT_VERIFIER_ROLE")
        self.python = self.root / "receiver/runtime/python/python.exe"
        self.node = self.root / "runtime/node/node.exe"
        self.policy = {"profile_id": profile["profile_id"], "foundation": profile["foundation"],
                       "image_words": [int.from_bytes(bytes.fromhex(profile["image_id"])[i:i+4], "little")
                                       for i in range(0, 32, 4)],
                       "registry_sha256": self.assets["assets/registry.json"]["sha256"]}
        self.image = profile["image_id"]
        need(Path(sys.executable).resolve() == self.python, "BUNDLED_PYTHON_ORIGIN")
        need(Path(__file__).resolve() == self.root / "operator/commons.py", "PUBLIC_LAUNCHER_ORIGIN")

    def verify(self, name):
        need(name in self.files, "RELEASE_ASSET_MISSING:" + name)
        path = self.root.joinpath(*safe_relative(name))
        need(pin(path) == self.files[name], "RELEASE_ASSET_CHANGED:" + name)
        return path

    def selected(self, action):
        need(action in {"provision", "node", "workflow", "seal-request"}, "PUBLIC_ACTION")
        selected = {"operator/commons.py", "receiver/profile.json"}
        receiver = set(BOOTSTRAP.values())
        if action == "workflow":
            receiver |= WORKFLOW_FILES
        if action in {"provision", "node"}:
            receiver |= {n[len("receiver/"):] for n in self.files if n.startswith("receiver/runtime/python/")}
            actual_codec = {n[len("codec/"):] for n in self.files if n.startswith("codec/")}
            need(actual_codec == CODEC_FILES, "EXACT_FROZEN_CODEC_MAP")
            selected |= {"codec/" + n for n in CODEC_FILES}
            selected |= {n for n in self.files if n.startswith("overlay/")}
            need({"overlay/node02.mjs", "overlay/overlay02.mjs", "overlay/intent_store.mjs",
                  "overlay/fragment_bridge.py", "overlay/package.json", "overlay/package-lock.json"} <= selected,
                 "EXACT_OVERLAY_COMPONENTS")
            if action == "node":
                selected |= {n for n in self.files if n.startswith("runtime/node/")}
                need("runtime/node/node.exe" in selected, "BUNDLED_NODE_REQUIRED")
        for name in receiver:
            need(self.files.get("receiver/" + name) == self.assets.get(name) and name in self.assets,
                 "PROFILE_RELEASE_ASSET_BINDING")
            selected.add("receiver/" + name)
        for name in sorted(selected):
            self.verify(name)
        return {name: self.files[name] for name in sorted(selected)}


def uint(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def address(value, mode, *, listen=False, bootstrap=False):
    need(type(value) is str and len(value) <= 256, "ADDRESS_STRING_BOUND")
    match = re.fullmatch(r"/ip4/([0-9.]+)/tcp/([0-9]+)(?:/p2p/([A-Za-z0-9]{1,128}))?", value)
    need(match is not None, "DIRECT_IPV4_TCP_ONLY")
    ip, port, peer = match.groups()
    octets = ip.split(".")
    need(len(octets) == 4 and all(x.isdigit() and str(int(x)) == x and 0 <= int(x) <= 255 for x in octets),
         "CANONICAL_IPV4")
    need(str(int(port)) == port and (0 if listen else 1) <= int(port) <= 65535
         and (not listen or peer is None) and (not bootstrap or peer is not None), "ADDRESS_PORT_OR_PEER")
    a, b, c, _ = map(int, octets)
    public = not (a in (0, 10, 127) or a >= 224 or (a == 100 and 64 <= b <= 127)
        or (a == 169 and b == 254) or (a == 172 and 16 <= b <= 31)
        or (a == 192 and (b in (168, 0) or (b == 88 and c == 99)))
        or (a == 198 and (b in (18, 19) or (b == 51 and c == 100)))
        or (a == 203 and b == 0 and c == 113))
    need((mode == "loopback" and ip == "127.0.0.1")
         or (mode == "public-ipv4" and (public or (listen and ip == "0.0.0.0"))), "ADDRESS_POLICY")
    return value


def provision_request(raw):
    need(isinstance(raw, bytes) and 0 < len(raw) <= 32768, "PROVISION_REQUEST_BOUND")
    value = strict(raw)
    need(type(value) is dict and set(value) == {"schema", "mode", "listen", "announce", "bootstrap", "limits", "store_limits"}
         and value["schema"] == "DMKN_COMPACT_OWNER_PROVISION_V1"
         and value["mode"] in ("loopback", "public-ipv4"), "PROVISION_SCHEMA")
    for name, low, high in (("listen", 1, 1), ("announce", 0, 4), ("bootstrap", 0, 16)):
        need(type(value[name]) is list and low <= len(value[name]) <= high, "ADDRESS_COUNT")
        for row in value[name]:
            address(row, value["mode"], listen=name == "listen", bootstrap=name == "bootstrap")
    need(value["mode"] != "public-ipv4" or value["announce"], "PUBLIC_ANNOUNCE_REQUIRED")
    limits = value["limits"]
    ranges = {"operation_ms": (1000, 60000), "query_events": (16, 4096), "provider_limit": (1, 32),
        "advertised_keys": (1, 4096), "provider_ttl_ms": (3000, 172800000),
        "reprovide_interval_ms": (500, 3600000), "maintenance_ms": (1000, 3600000),
        "io_bytes": (16781312, 1024**3)}
    need(type(limits) is dict and set(limits) == set(ranges) | {"metadata"}, "OVERLAY_LIMIT_FIELDS")
    for name, (low, high) in ranges.items():
        uint(limits[name], low, high, "OVERLAY_LIMIT:" + name)
    need(limits["reprovide_interval_ms"] * 3 <= limits["provider_ttl_ms"], "RENEWAL_MARGIN")
    metadata = limits["metadata"]
    need(type(metadata) is dict and set(metadata) == {"entries", "bytes", "valueBytes", "providersPerKey", "pages"},
         "METADATA_LIMIT_FIELDS")
    for name, low, high in (("entries", 32, 65536), ("bytes", 65536, 128*MIB), ("valueBytes", 1024, 65536),
                            ("providersPerKey", 1, 128), ("pages", 256, 65536)):
        uint(metadata[name], low, high, "METADATA_LIMIT:" + name)
    store = value["store_limits"]
    need(type(store) is dict and set(store) == {"max_entries", "max_blob_bytes", "max_db_pages"}, "STORE_LIMIT_FIELDS")
    for name, low, high in (("max_entries", 1, 10000000), ("max_blob_bytes", 1, 1024**4), ("max_db_pages", 256, 1048576)):
        uint(store[name], low, high, "STORE_LIMIT:" + name)
    return value


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned_input(path, expected, maximum):
    need(type(expected) is str and re.fullmatch(HEX, expected), "INPUT_DIGEST_REQUIRED")
    raw = bounded_read(path, maximum)
    need(digest(raw) == expected, "EXACT_INPUT_CHANGED")
    return raw


def provision_configs(release, owner, request):
    bridge = {"schema": "DMKN_FRAGMENT_BRIDGE_CONFIG_V1", "codec": {"root": str(release.root / "codec"),
        "index_sha256": release.files["codec/fragment_index.py"]["sha256"],
        "peer_sha256": release.files["codec/fragment_peer.py"]["sha256"]},
        "state": str(owner / "fragments"), "io_root": str(owner / "frames"),
        "policy": release.policy, "limits": request["store_limits"]}
    bridge_raw = (json.dumps(bridge, sort_keys=True, separators=(",", ":")) + "\n").encode()
    overlay = {"schema": "DMKN_MAINTAINED_OVERLAY_V1", "state": str(owner / "overlay"),
        **{key: request[key] for key in ("mode", "listen", "announce", "bootstrap", "limits")},
        "bridge": {"python": str(release.python), "script_sha256": release.files["overlay/fragment_bridge.py"]["sha256"],
            "config": str(owner / "bridge-config.json"), "config_sha256": digest(bridge_raw), "io_root": str(owner / "frames")}}
    return bridge, overlay, bridge_raw


def owner_commands(raw):
    # The shipped Node stdin buffer is32KiB per chunk; cap this whole finite file
    # below that boundary, not merely each line. Live stdio is the advanced API.
    need(isinstance(raw, bytes) and 0 < len(raw) <= 16384 and raw.endswith(b"\n"), "FINITE_COMMAND_FILE_BOUND")
    lines = raw[:-1].split(b"\n")
    need(1 <= len(lines) <= 128 and all(lines), "FINITE_COMMAND_COUNT")
    ids, commands = set(), []
    for line in lines:
        value = owner_line(line)
        need(type(value) is dict and set(value) == {"id", "request"}
             and type(value["id"]) is str and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", value["id"])
             and value["id"] not in ids and type(value["request"]) is dict
             and value["request"].get("operation") in OWNER_OPERATIONS, "OWNER_COMMAND_ENVELOPE")
        ids.add(value["id"])
        commands.append(value)
    need(all(row["request"]["operation"] != "stop" for row in commands[:-1]), "STOP_MUST_BE_LAST")
    return commands


def owner_line(line):
    """Conservative Unicode-scalar/safe-integer subset of JSON.stringify output."""
    value = strict(line)
    def ordered(item, depth=0):
        if type(item) in (dict, list):
            need(depth < 24, "OWNER_JSON_DEPTH")
        if type(item) is dict:
            # ECMAScript own-property order puts canonical uint32 indices first.
            indices = sorted((key for key in item if re.fullmatch(r"0|[1-9][0-9]*", key)
                              and int(key) < 2**32-1), key=int)
            others = [key for key in item if key not in indices]
            return {key: ordered(item[key], depth+1) for key in indices+others}
        if type(item) is list:
            return [ordered(member, depth+1) for member in item]
        if type(item) is int:
            need(-(2**53-1) <= item <= 2**53-1, "OWNER_JSON_SAFE_INTEGER")
        need(item is None or type(item) in (str, int, bool), "OWNER_JSON_VALUE")
        return item
    canonical = json.dumps(ordered(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    need(canonical == line, "OWNER_NODE_CANONICAL_JSON")
    return value


def owner_config(release, path, expected, evidence):
    raw = pinned_input(path, expected, 32768)
    value = strict(raw)
    need(type(value) is dict and set(value) == {"schema", "state", "mode", "listen", "announce", "bootstrap", "bridge", "limits"}
         and value["schema"] == "DMKN_MAINTAINED_OVERLAY_V1", "OWNER_CONFIG_SCHEMA")
    bridge = value["bridge"]
    need(type(bridge) is dict and set(bridge) == {"python", "script_sha256", "config", "config_sha256", "io_root"}
         and bridge["python"] == str(release.python)
         and bridge["script_sha256"] == release.files["overlay/fragment_bridge.py"]["sha256"], "ADOPTED_BRIDGE_BINDING")
    bridge_path = absolute(bridge["config"])
    bridge_raw = pinned_input(bridge_path, bridge["config_sha256"], 32768)
    config = strict(bridge_raw)
    need(type(config) is dict and set(config) == {"schema", "codec", "state", "io_root", "policy", "limits"}
         and config["schema"] == "DMKN_FRAGMENT_BRIDGE_CONFIG_V1" and config["policy"] == release.policy
         and config["codec"] == {"root": str(release.root / "codec"),
             "index_sha256": release.files["codec/fragment_index.py"]["sha256"],
             "peer_sha256": release.files["codec/fragment_peer.py"]["sha256"]}
         and config["io_root"] == bridge["io_root"], "ADOPTED_CODEC_POLICY")
    roots = [absolute(value["state"], directory=True, fresh=not Path(value["state"]).exists()),
             absolute(config["state"], directory=True), absolute(config["io_root"], directory=True)]
    for root in roots:
        need(not overlap(root, release.root) and not overlap(root, evidence), "STATE_DOMAIN_OVERLAP")
    need(all(not overlap(a, b) for i, a in enumerate(roots) for b in roots[i+1:]), "STATE_DOMAINS_DISTINCT")
    need(not overlap(path, evidence) and not overlap(bridge_path, evidence), "CONFIG_EVIDENCE_OVERLAP")
    return value, [(path, digest(raw)), (bridge_path, digest(bridge_raw))]


def workflow_command(release, arguments, evidence):
    actions = {"apply", "check-fragment", "apply-fast", "check-fast", "prepare-seal", "advance"}
    need(type(arguments) is list and 1 <= len(arguments) <= 128
         and arguments[0] in actions, "COMPACT_WORKFLOW_ACTION_ONLY")
    action = arguments[0]
    bounds = {"--run", "--cpu-budget-seconds", "--deadline-utc"}
    seal_flags = bounds | {"--fragment", "--expected-manifest-sha256", "--expected-interface"}
    allowed = ({"--run", "--max-new-stages"} if action == "advance" else
               seal_flags if action == "prepare-seal" else WORKFLOW_FLAGS)
    seen, index = {}, 1
    while index < len(arguments):
        token = arguments[index]
        need(type(token) is str and token in allowed and index + 1 < len(arguments), "EXACT_WORKFLOW_OPTION")
        value = arguments[index+1]
        need(type(value) is str and "\0" not in value and len(value) <= 32767, "WORKFLOW_VALUE_BOUND")
        seen[token] = seen.get(token, 0) + 1
        need(seen[token] == 1 or token in {"--parent", "--local-definition", "--local-fragment"}, "DUPLICATE_WORKFLOW_OPTION")
        if token in PATH_FLAGS:
            path = absolute(value, directory=token in {"--run", "--parent", "--local-fragment", "--fragment"},
                            fresh=token == "--run" and action != "advance")
            need(not overlap(path, evidence) and not overlap(path, release.root), "WORKFLOW_PATH_DOMAIN")
        elif token in {"--expected-manifest-sha256", "--expected-interface"}:
            need(re.fullmatch(HEX, value), "EXACT_SEAL_INPUT_PIN")
        elif token == "--max-new-stages":
            need(re.fullmatch(r"[1-9][0-9]{0,2}", value) and 1 <= int(value) <= 393, "FINITE_NEW_STAGE_COUNT")
        index += 2
    if action == "advance":
        need(set(seen) == {"--run", "--max-new-stages"}, "EXACT_ADVANCE_INPUTS_NO_RENEWAL")
    elif action == "prepare-seal":
        need(set(seen) == seal_flags, "EXACT_SEAL_INPUTS")
    else:
        need(bounds <= set(seen), "EXPLICIT_OPERATION_BOUND_REQUIRED")
        if action in {"apply", "apply-fast"}:
            need({"--application-plan", "--expected-capsule"} <= set(seen) and "--fragment" not in seen, "EXPLICIT_APPLICATION_INPUTS")
        else:
            need(set(seen) == bounds | {"--fragment"}, "EXACT_CHECK_INPUTS")
    return [str(release.python), "-I", "-S", "-B", str(release.root / "receiver/cert_workflow.py"),
            *arguments, "--profile", str(release.profile), "--profile-sha256", PROFILE_SHA]


def load_module(name, path):
    need(name not in sys.modules, "UNEXPECTED_HELPER_MODULE")
    raw = bounded_read(path, MIB)
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    exec(compile(raw, str(path), "exec"), result.__dict__)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--evidence", required=True, type=Path)
    for key in CEILINGS:
        parser.add_argument("--" + key.replace("_", "-"), required=True, type=int)
    commands = parser.add_subparsers(dest="action", required=True)
    provision = commands.add_parser("provision", allow_abbrev=False)
    provision.add_argument("--request", type=Path, required=True)
    provision.add_argument("--request-sha256", required=True)
    provision.add_argument("--owner", type=Path, required=True)
    node = commands.add_parser("node", allow_abbrev=False)
    node.add_argument("--config", type=Path, required=True)
    node.add_argument("--config-sha256", required=True)
    node.add_argument("--create", action="store_true")
    group = node.add_mutually_exclusive_group(required=True)
    group.add_argument("--commands", type=Path)
    group.add_argument("--serve-seconds", type=int)
    node.add_argument("--commands-sha256")
    workflow = commands.add_parser("workflow", allow_abbrev=False)
    workflow.add_argument("arguments", nargs=argparse.REMAINDER)
    seal = commands.add_parser("seal-request", allow_abbrev=False)
    seal.add_argument("--fragment", type=Path, required=True)
    seal.add_argument("--expected-manifest-sha256", required=True)
    seal.add_argument("--expected-interface", required=True)
    args = parser.parse_args(argv)
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.flags.no_user_site
         and sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
         "WINDOWS_ISOLATED_UNOPTIMIZED_PYTHON_REQUIRED")
    limits = limits_checked({key: getattr(args, key) for key in CEILINGS})
    release = Release(args.manifest, args.manifest_sha256)
    selected = release.selected(args.action)
    evidence = absolute(args.evidence, directory=True, fresh=True)
    need(not overlap(evidence, release.root), "EVIDENCE_INSTALL_OVERLAP")
    stdin_bytes, serve_seconds, auxiliary, recheck = None, None, {}, []
    if args.action == "provision":
        owner = absolute(args.owner, directory=True, fresh=True)
        need(not overlap(owner, release.root) and not overlap(owner, evidence), "OWNER_DOMAIN_OVERLAP")
        request_raw = pinned_input(args.request, args.request_sha256, 32768)
        need(not overlap(args.request, evidence) and not overlap(args.request, owner), "REQUEST_DOMAIN_OVERLAP")
        request = provision_request(request_raw)
        bridge, overlay, bridge_raw = provision_configs(release, owner, request)
        owner.mkdir(); (owner / "frames").mkdir()
        save_new(owner / "bridge-config.json", bridge)
        need((owner / "bridge-config.json").read_bytes() == bridge_raw, "GENERATED_BRIDGE_PIN")
        save_new(owner / "overlay-config.json", overlay)
        command = [str(release.python), "-I", "-S", "-B", str(release.root / "overlay/fragment_bridge.py"),
                   "--config", str(owner / "bridge-config.json"), "--config-sha256", digest(bridge_raw)]
        stdin_bytes = b'{"operation":"init"}\n'
        auxiliary = {"owner": str(owner), "overlay_config": str(owner / "overlay-config.json"),
                     "overlay_config_sha256": pin(owner / "overlay-config.json")["sha256"],
                     "bridge_config_sha256": digest(bridge_raw),
                     "next_step": "Start node with exact config pin and --create only once; failure may have committed state."}
        recheck = [(args.request, args.request_sha256), (owner / "bridge-config.json", digest(bridge_raw)),
                   (owner / "overlay-config.json", auxiliary["overlay_config_sha256"])]
    elif args.action == "node":
        config, recheck = owner_config(release, args.config, args.config_sha256, evidence)
        if args.create:
            absolute(config["state"], directory=True, fresh=True)
        else:
            absolute(config["state"], directory=True)
        command = [str(release.node), "--max-old-space-size=512", str(release.root / "overlay/node02.mjs"),
                   "--config", str(args.config), "--config-sha256", args.config_sha256]
        if args.create:
            command.append("--create")
        if args.commands is not None:
            stdin_bytes = pinned_input(args.commands, args.commands_sha256, 16384)
            owner_commands(stdin_bytes)
            need(not overlap(args.commands, evidence), "COMMAND_EVIDENCE_OVERLAP")
            recheck.append((args.commands, args.commands_sha256))
        else:
            need(args.commands_sha256 is None, "NO_COMMAND_HASH_WITH_SERVICE_LEASE")
            serve_seconds = uint(args.serve_seconds, 1, limits["wall_seconds"]-15, "FINITE_SERVICE_LEASE")
    elif args.action == "workflow":
        need(args.arguments and args.arguments[0] == "--", "WORKFLOW_SEPARATOR")
        command = workflow_command(release, args.arguments[1:], evidence)
    else:
        fragment = absolute(args.fragment, directory=True)
        need(not overlap(fragment, release.root) and not overlap(fragment, evidence), "SEAL_HANDOFF_DOMAIN")
        manifest_raw = pinned_input(fragment / "fragment.json", args.expected_manifest_sha256, 16384)
        fragment_manifest = strict(manifest_raw)
        need(fragment_manifest.get("schema") == "DMKN_BOUNDED_PROOF_FRAGMENT_V1"
             and fragment_manifest.get("image") == release.image
             and fragment_manifest.get("foundation") == release.policy["foundation"]
             and fragment_manifest.get("profile_id") == release.policy["profile_id"]
             and re.fullmatch(HEX, args.expected_interface), "SEAL_EXPECTED_POLICY")
        evidence.mkdir()
        record = {"schema": "DMKN_OWNER_SEAL_REQUEST_V1", "fragment": str(fragment),
            "expected_manifest_sha256": args.expected_manifest_sha256, "expected_interface": args.expected_interface,
            "policy": release.policy, "image": release.image, "release_manifest_sha256": release.expected_sha,
            "assurance": "OWNER_SELECTED_HANDOFF_NOT_CHECKED_NOT_CERTIFIED",
            "instructions": "Use this adopted compact installation workflow prepare-seal on the exact held proposition fragment, then funded advance under its original budget/deadline. Only completed final receipt verification certifies; this handoff does not."}
        save_new(evidence / "seal-request.json", record)
        print(json.dumps(record, sort_keys=True))
        return 0
    need(time.monotonic()-BOOT_WALL < limits["wall_seconds"] and time.process_time()-BOOT_CPU <= 60, "PREFLIGHT_RESOURCE_LIMIT")
    load_module("domains", release.root / "receiver/helpers/domains.py")
    jobs = load_module("_compact_commons_job", release.root / "receiver/helpers/run_stage.py")
    record = supervise(command, release.root, evidence, limits, jobs.Job, started=BOOT_WALL,
                       stdin_bytes=stdin_bytes, serve_seconds=serve_seconds)
    try:
        need(digest(bounded_read(release.manifest, 8*MIB)) == release.expected_sha, "FINAL_MANIFEST_CHANGED")
        for path, expected in recheck:
            need(digest(bounded_read(path, MIB)) == expected, "FINAL_OWNER_INPUT_CHANGED")
        for name in selected:
            release.verify(name)
    except Exception as error:
        record["status"] = "FINAL_INPUT_BINDING_FAILED"
        record["final_input_error"] = type(error).__name__ + ": " + str(error)[:1000]
    selected_identity = json.dumps(selected, sort_keys=True, separators=(",", ":")).encode()
    if time.monotonic()-BOOT_WALL > limits["wall_seconds"] or time.process_time()-BOOT_CPU > 60:
        record["status"] = "FINAL_WRAPPER_RESOURCE_LIMIT"
    record.update(release_manifest_sha256=release.expected_sha, action=args.action,
                  selected_code={"files": len(selected), "bytes": sum(v["bytes"] for v in selected.values()),
                                 "exact_map_sha256": digest(selected_identity), "map_source": "deterministic selected subset of adopted release manifest"},
                  profile_sha256=PROFILE_SHA, owner=auxiliary,
                  wrapper_total_cpu_seconds_before_report=time.process_time()-BOOT_CPU,
                  wrapper_total_wall_seconds_before_report=time.monotonic()-BOOT_WALL)
    save_new(evidence / "result.json", record)
    # Finite captured replies only after terminal closure; no live relay threads.
    raw_reply = bounded_read(evidence / "stdout.txt", limits["stdout_bytes"]) if (evidence / "stdout.txt").stat().st_size else b""
    if raw_reply:
        sys.stdout.buffer.write(raw_reply)
        sys.stdout.buffer.flush()
    print(json.dumps({"event": "commons-owner-terminal", "status": record["status"],
        "authority": record["authority"], "evidence": str(evidence), "owner": auxiliary}, sort_keys=True))
    return 0 if record["status"] == "COMMAND_EXITED_ZERO_AND_CLOSED" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "PUBLIC_FACADE_REFUSED_OR_REPORT_FAILED", "error": type(error).__name__ + ": " + str(error)[:2000],
                          "authority": "NOT_MATHEMATICAL_ACCEPTANCE", "failed_state_preserved": True}), file=sys.stderr)
        raise SystemExit(1)

