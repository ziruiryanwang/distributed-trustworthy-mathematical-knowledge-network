"""One selected public-CLI reciprocal boundary check; not a package entrypoint.

Run once only under an outer Windows Job 240 wall /160 CPU /2048 MiB /10
processes. This harness has an original 210-second lifetime, 190-second work
window and 145-second accounted CPU allowance; all child grants derive from it.
No imports of product APIs, retries, state copying, old basis replay or rebuild.
Public commands own acceptance. The outer Job owns final process-tree closure.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import stat
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = LOCAL/"ordinary-package-lifecycle-01"
CONTINUATION = LOCAL/"ordinary-package-lifecycle-continuation-01"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
A_STORE = "7becc8b2d689d7240c791c44f22599bb22cee92bf6da097c2a028b535c5a0b5c"
A_ROOT = "b5632acbab2d88f5e66436bc9bd7e4a47578ab6f41e35ecb20f9b2e00c0fb334"
A_UNIT = "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e"
A_EXPORT = "bb47ce4786c4f5c22505952133e5220c0650452fb0006c83a395de131fee1355"
A_DEF_UNIT = "25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3"
A_DEF_EXPORT = "b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02"
CONTINUATION_SHA = "81b70c4894fe218dc7daf890c37cf4a51810a7517294d9881a2884b9c90066e7"
INDEX_LIMITS = {"max_objects": 32, "max_postings": 4096, "max_features": 512,
                "max_snapshots": 33, "max_logical_bytes": 16*MIB, "max_db_pages": 4096}
CUSTODY_LIMITS = {"objects": 512, "exports": 4096, "logical_bytes": 128*MIB, "db_pages": 16384}
BODY = b"""universe u

namespace CommonsPeerExample

theorem applyFour_eq {a : Type u} (f : a -> a) (x : a) :
    CommonsPackageExample.applyTwice f (CommonsPackageExample.applyTwice f x) =
      f (f (f (f x))) :=
  Eq.trans
    (@CommonsPackageExample.applyTwice_eq a f (CommonsPackageExample.applyTwice f x))
    (congrArg (fun y : a => f (f y)) (@CommonsPackageExample.applyTwice_eq a f x))

end CommonsPeerExample
"""


def need(ok, code):
    if not ok: raise ValueError(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=16*MIB):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not stat.S_ISLNK(info.st_mode)
         and not getattr(info, "st_file_attributes", 0) & 0x400
         and info.st_nlink == 1 and 0 <= info.st_size <= maximum, "RECIPROCAL_FILE_BOUND")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) == info.st_size, "RECIPROCAL_FILE_CHANGED")
    return raw


def save(path, value):
    raw = value if type(value) is bytes else json.dumps(value, sort_keys=True,
        ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    need(len(raw) <= 32*MIB, "RECIPROCAL_OUTPUT_BOUND")
    with path.open("xb") as stream: stream.write(raw)
    return digest(raw)


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def retained_input_paths():
    """File-only selection helper; no product import or state open."""
    fixed = [CONTINUATION/"CONTINUATION-RESULT.json", CONTINUATION/"CallerExposedBody.lean",
             OLD/"LIFECYCLE-RESULT.json", OLD/"CallerBody.lean", OLD/"custody-limits.json"]
    for root in (OLD/"catalog", OLD/"custody", CONTINUATION/"contribution/evidence",
                 CONTINUATION/"contribution/previews"):
        need(root.is_dir(), "RECIPROCAL_RETAINED_DIRECTORY")
        for current, directories, files in os.walk(root, followlinks=False):
            for entry in [Path(current), *(Path(current)/part for part in directories)]:
                info = entry.lstat()
                need(not stat.S_ISLNK(info.st_mode) and not
                     getattr(info, "st_file_attributes", 0) & 0x400, "RECIPROCAL_RETAINED_REDIRECT")
            fixed.extend(Path(current)/part for part in files)
    need(len(fixed) <= 96 and len(set(fixed)) == len(fixed), "RECIPROCAL_RETAINED_COUNT")
    return sorted(fixed)


def retained_map():
    result, total = {}, 0
    for path in retained_input_paths():
        raw = read(path, 32*MIB); total += len(raw)
        need(total <= 64*MIB, "RECIPROCAL_RETAINED_TOTAL")
        result[str(path)] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


class Run:
    def __init__(self, package, profile, output):
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.deadline, self.cleanup_deadline = self.started+190, self.started+210
        self.package, self.profile, self.output = package, profile, output
        self.live, self.calls, self.cleanup = {}, [], []
        self.charged_cpu = 0.0

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.charged_cpu < 145, "RECIPROCAL_ORIGINAL_ALLOWANCE")
        for row in self.live.values():
            for path, maximum in ((row["stdout"], 16*MIB), (row["stderr"], MIB)):
                need(path.stat().st_size <= maximum, "RECIPROCAL_LIVE_LOG_BOUND")

    def start(self, label, entry, operation, state=None, *, config=None, extra=(), wall=45, cpu=12, memory=512):
        self.check()
        need(label not in self.live and all(row["label"] != label for row in self.calls), "RECIPROCAL_NO_RETRY")
        wall = min(wall, math.floor(self.deadline-time.monotonic())-5)
        reserved = sum(row["cpu_cap"] for row in self.live.values())
        cpu = min(cpu, math.floor(145-(time.process_time()-self.cpu_started)-self.charged_cpu-reserved)-1)
        need(wall >= 35 and cpu >= 4, "RECIPROCAL_REMAINING_CHILD_GRANT")
        argv = [str(PYTHON), "-I", "-S", "-B", str(self.package/entry), operation,
            "--profile-sha256", self.profile, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(LEAN), "--wall-seconds", str(wall),
            "--cpu-seconds", str(cpu), "--memory-mib", str(memory)]
        if state is not None:
            catalog, custody, store, limits = state
            argv.extend(("--catalog", str(catalog), "--custody", str(custody),
                         "--store-id", store, "--custody-limits", str(limits)))
        if config is not None:
            config_path = self.output/(label+".config.json")
            pin = save(config_path, config)
            argv.extend(("--config", str(config_path), "--config-sha256", pin,
                         "--output", str(self.output/(label+"-operation"))))
        argv.extend(extra)
        save(self.output/(label+".command.json"), {"argv": argv,
            "parent_seconds_remaining": self.deadline-time.monotonic(),
            "cpu_cap": cpu, "wall_cap": wall, "memory_mib": memory})
        stdout_path, stderr_path = self.output/(label+".stdout"), self.output/(label+".stderr")
        stdout, stderr = stdout_path.open("xb"), stderr_path.open("xb")
        try:
            process = subprocess.Popen(argv, cwd=self.output, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        except BaseException:
            stdout.close(); stderr.close(); raise
        self.live[label] = {"process": process, "handles": (stdout, stderr), "cpu_cap": cpu,
            "stdout": stdout_path, "stderr": stderr_path, "deadline": time.monotonic()+wall,
            "entry": entry, "operation": operation, "started": time.monotonic()}
        return label

    def collect(self, label, *, validate=True):
        row = self.live[label]
        need(row["process"].poll() is not None, "RECIPROCAL_CHILD_STILL_LIVE")
        row["process"].wait()
        for handle in row["handles"]: handle.close()
        del self.live[label]
        event = {"label": label, "entry": row["entry"], "operation": row["operation"],
            "returncode": row["process"].returncode, "wall_seconds": time.monotonic()-row["started"],
            "charged_cpu": row["cpu_cap"], "result": None}
        self.calls.append(event)
        charge = row["cpu_cap"]
        try:
            raw, errors = read(row["stdout"]), read(row["stderr"], MIB)
            event.update(stdout_sha256=digest(raw), stderr_sha256=digest(errors))
            result = json.loads(raw)
            event["result"] = result
            cost = result["cost"]
            values = (cost["controller_cpu_seconds"], cost["worker_cpu_seconds"])
            need(all(type(value) in (float, int) and math.isfinite(value) and value >= 0
                     for value in values), "RECIPROCAL_CHILD_COST")
            if result["ok"] is True and row["process"].returncode == 0 and not errors:
                charge = sum(values)
            if validate:
                need(not errors and row["process"].returncode == 0 and result["ok"] is True,
                     "RECIPROCAL_PUBLIC_COMMAND:"+label)
                need(result["implementation_id"] == IMPLEMENTATION and result.get("semantic_id", SEMANTIC) == SEMANTIC,
                     "RECIPROCAL_INSTALLED_CORE")
            return result
        finally:
            event["charged_cpu"] = charge
            self.charged_cpu += charge

    def wait(self, label):
        row = self.live[label]
        while row["process"].poll() is None:
            self.check()
            need(time.monotonic() < row["deadline"]+1, "RECIPROCAL_CHILD_DEADLINE")
            time.sleep(0.05)
        result = self.collect(label)
        self.check()
        return result

    def call(self, *args, **kwargs):
        return self.wait(self.start(*args, **kwargs))

    def ready(self, label):
        path, until = self.output/(label+"-operation")/"READY.json", time.monotonic()+15
        while time.monotonic() < until:
            self.check()
            if self.live[label]["process"].poll() is not None:
                self.collect(label)
                raise ValueError("RECIPROCAL_SERVICE_EXIT_BEFORE_READY")
            if path.exists():
                raw = read(path, 65536)
                try: ready = json.loads(raw)
                except json.JSONDecodeError: ready = None  # Writer may still be flushing.
                if ready is not None:
                    need(ready["status"] == "READY" and ready["host"] == "127.0.0.1"
                         and ready["tls"] is False and type(ready["port"]) is int
                         and 1 <= ready["port"] <= 65535 and ready["mathematical_acceptance"] is False,
                         "RECIPROCAL_SERVICE_READY")
                    return ready
            time.sleep(0.05)
        raise ValueError("RECIPROCAL_SERVICE_START_DEADLINE")

    def close(self):
        # Only these exact launched processes may be terminated. A forced close
        # is failure; the enclosing selected Job must settle the entire tree.
        for label, row in list(self.live.items()):
            process = row["process"]
            try:
                if process.poll() is None:
                    process.terminate()
                    self.cleanup.append({"label": label, "action": "TERMINATED_EXACT_CHILD"})
                process.wait(timeout=max(0.1, min(5, self.cleanup_deadline-time.monotonic())))
                self.collect(label, validate=False)
            except BaseException as error:
                self.cleanup.append({"label": label, "error_type": type(error).__name__, "error": str(error)})
                if process.poll() is None: process.kill()
                for handle in row["handles"]: handle.close()


def query(ready):
    return {"contacts": {"selected": {"host": "127.0.0.1", "port": ready["port"],
        "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}},
        "providers": ["selected"], "specs": [
            {"tag": "object-kind", "value": "ordinary-lean-export-v2"},
            {"tag": "declaration-kind", "value": "theorem"}],
        "limits": {"providers": 1, "snapshots": 1, "requests": 4, "pages": 2,
            "examined": 32, "candidates": 8, "bytes": MIB, "wall_ms": 10000, "inflight": 1},
        "offer": {"max_bytes": 16384, "max_expanded_bytes": MIB, "max_age_ms": 10000},
        "page": {"scanned": 16, "matches": 8, "bytes": 131072, "timeout_ms": 1000,
            "record_probes": 256, "node_reads": 100000, "hash_calls": 2000000, "sql_vm_steps": 1000000}}


def publication(index, context, targets):
    return {"index": {"path": str(index), "limits": INDEX_LIMITS, "create": True},
            "context_root": context, "targets": targets, "max_unit_bytes": MIB, "max_total_bytes": 4*MIB}


def service(index, lease):
    return {"index": {"path": str(index), "limits": INDEX_LIMITS, "create": False},
        "host": "127.0.0.1", "port": 0, "tls": None, "lease_seconds": lease, "cleanup_seconds": 10,
        "limits": {"max_connections": 2, "max_requests": 24, "max_reply_bytes": 8*MIB, "operation_ms": 5000},
        "share_all_custody": True, "exclusive": True}


def selected(result, expected):
    result = result["result"]
    need(result["status"] == "INCOMPLETE_SEARCH" and result["global_complete"] is False
         and result["mathematical_acceptance"] is False and len(result["matches"]) == 1,
         "RECIPROCAL_SELECTED_INERT_MATCH")
    match = result["matches"][0]
    need(match["record"]["object_id"] == expected, "RECIPROCAL_MATCH_ID_AFTER_DISCOVERY")
    return match


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("package", "profile-sha256", "output"): parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    package, output = Path(args.package), Path(args.output)
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and Path(sys.executable) == PYTHON, "RECIPROCAL_PYTHON")
    need(package.is_absolute() and output.is_absolute() and package.is_dir() and output.is_dir()
         and output.is_relative_to(LOCAL) and not output.is_relative_to(package)
         and not package.is_relative_to(output) and all(not output.is_relative_to(old)
         and not old.is_relative_to(output) for old in (OLD, CONTINUATION)), "RECIPROCAL_PATHS")
    run = Run(package, args.profile_sha256, output)
    report = {"status": "FAILED", "phase": "INPUTS", "calls": run.calls,
        "claim": "PUBLIC_CLI_RECIPROCAL_OPERABILITY_NOT_GROWTH_OR_INDEPENDENT_HOSTS",
        "outer_job_required_for_final_tree_quiescence": True}
    preserved = None
    try:
        profile_raw = read(package/"PROFILE.json", 2*MIB)
        need(digest(profile_raw) == args.profile_sha256, "RECIPROCAL_PROFILE_PIN")
        previous_raw = read(CONTINUATION/"CONTINUATION-RESULT.json")
        need(digest(previous_raw) == CONTINUATION_SHA, "RECIPROCAL_RETAINED_OUTCOME_PIN")
        previous = json.loads(previous_raw)
        need(previous["status"] == "PASS_CORRECTED_CALLER_AND_PERSISTENT_REOPEN"
             and previous["local_root"] == A_ROOT, "RECIPROCAL_RETAINED_OWNER")
        need(digest(read(CONTINUATION/"CallerExposedBody.lean", MIB)) == previous["caller_source_sha256"],
             "RECIPROCAL_RETAINED_SOURCE_PIN")
        previous_call = previous["calls"][0]["result"]
        need(previous_call["implementation_id"] == IMPLEMENTATION and previous_call["store_id"] == A_STORE
             and previous_call["catalog"] == str(OLD/"catalog")
             and previous_call["custody"] == str(OLD/"custody"), "RECIPROCAL_RETAINED_STATE_SELECTION")
        for row in [*previous_call["result"]["units"], *previous_call["result"]["previews"]]:
            path = Path(row["file"])
            need(path.is_relative_to(CONTINUATION/"contribution"), "RECIPROCAL_RETAINED_PUBLICATION_PATH")
            raw = read(path, MIB)
            need(len(raw) == row["bytes"] and digest(raw) == row["sha256"], "RECIPROCAL_RETAINED_PUBLICATION_PIN")
        inventory = json.loads(read(package/"installation/foundation/inventory.json", MIB))
        need(all(any(row[0] == name(symbol) for row in inventory) for symbol in ("Eq.trans", "congrArg")),
             "RECIPROCAL_PROOF_BASIS_SUPPORT")
        a_target = {"name": name("CommonsPackageExample.applyTwice_eq"), "unit_id": A_UNIT, "export_id": A_EXPORT}
        need(a_target in previous["targets"], "RECIPROCAL_RETAINED_TARGET")
        retained = json.loads(read(CONTINUATION/"contribution/evidence"/(A_UNIT+".json"), MIB))
        need(any(row[1] == A_DEF_EXPORT for row in retained["imports"]), "RECIPROCAL_REAL_MISSING_DEFINITION")
        preserved = retained_map()
        save(output/"A-PRESERVED-BEFORE.json", preserved)
        a_state = (OLD/"catalog", OLD/"custody", A_STORE, OLD/"custody-limits.json")
        b_limits = output/"B-custody-limits.json"; save(b_limits, CUSTODY_LIMITS)
        b_state = (output/"B-catalog", output/"B-custody", digest(b"ordinary-public-peer-B-01"), b_limits)
        a_index, b_index = output/"A-index", output/"B-index"
        report["phase"] = "A_PUBLISH"
        run.call("A-publish", "peer.py", "publish", a_state, config=publication(a_index, A_ROOT, [a_target]))
        report["phase"] = "NEW_B_INITIALIZE"
        initialized = run.call("B-init", "owner.py", "init", b_state, wall=85, cpu=60, memory=1536)
        basis = initialized["result"]["basis"]
        need(basis["status"] == "CHECKED", "RECIPROCAL_NEW_B_BASIS")
        report["phase"] = "A_SERVE_B_FIND_RECEIVE"
        run.start("A-serve", "peer.py", "serve", a_state, config=service(a_index, 45), wall=65, cpu=8, memory=256)
        a_ready = run.ready("A-serve")
        find_config = query(a_ready)
        match = selected(run.call("B-find", "peer.py", "find", config=find_config, cpu=8, memory=256), A_EXPORT)
        receive_config = {"contacts": find_config["contacts"], "selection": match, "parent_root": basis["local_root"],
            "limits": {"requests": 12, "reply_bytes": 4*MIB, "units": 4, "unit_bytes": MIB,
                "total_bytes": 4*MIB, "missing": 4, "preflights": 4, "locator_bytes": 4096}}
        received = run.call("B-receive", "peer.py", "receive", b_state, config=receive_config,
                            wall=65, cpu=45, memory=1536)["result"]
        need(received["status"] == "CHECKED" and received["admission"]["units_checked"] == 2
             and set(received["unit_ids"]) == {A_UNIT, A_DEF_UNIT}
             and received["frontier"][0]["missing_count"] == 1
             and received["frontier"][-1]["status"] == "READY", "RECIPROCAL_ACTUAL_CLOSURE_ADMISSION")
        served = run.wait("A-serve")["result"]
        need(served["status"] == "LEASE_FINISHED" and served["quiescent"] is True
             and served["cleanup_errors"] == [], "RECIPROCAL_A_QUIESCENT")
        report["phase"] = "B_CONTRIBUTE_WITH_A_OFFLINE"
        source, acquired, outputs = output/"CallerBody.lean", output/"acquired.json", output/"outputs.json"
        save(source, BODY); save(acquired, [received["target"]])
        successor_name = name("CommonsPeerExample.applyFour_eq"); save(outputs, [successor_name])
        contribution = run.call("B-contribute", "owner.py", "contribute", b_state,
            extra=("--parent-root", received["admission"]["local_root"], "--source", str(source),
                "--acquired-targets", str(acquired), "--output-names", str(outputs),
                "--output", str(output/"B-contribution")), wall=70, cpu=50, memory=1536)["result"]
        need(contribution["admission"]["status"] == "CHECKED" and contribution["admission"]["units_checked"] == 1
             and len(contribution["targets"]) == 1 and contribution["targets"][0]["name"] == successor_name,
             "RECIPROCAL_NEW_CALLER_THEOREM")
        evidence_path = Path(contribution["units"][0]["file"])
        need(evidence_path.is_relative_to(output/"B-contribution"), "RECIPROCAL_NEW_EVIDENCE_PATH")
        evidence = read(evidence_path, MIB)
        need(digest(evidence) == contribution["units"][0]["sha256"]
             and any(row[1] == A_EXPORT for row in json.loads(evidence)["imports"]), "RECIPROCAL_CHECKED_ACQUIRED_USE")
        report["phase"] = "B_PUBLISH_SERVE_C_FIND"
        run.call("B-publish", "peer.py", "publish", b_state,
                 config=publication(b_index, contribution["local_root"], contribution["targets"]))
        run.start("B-serve", "peer.py", "serve", b_state, config=service(b_index, 15), wall=40, cpu=8, memory=256)
        cold = selected(run.call("C-find", "peer.py", "find", config=query(run.ready("B-serve")),
                                cpu=8, memory=256), contribution["targets"][0]["export_id"])
        served = run.wait("B-serve")["result"]
        need(served["status"] == "LEASE_FINISHED" and served["quiescent"] is True
             and served["cleanup_errors"] == [], "RECIPROCAL_B_QUIESCENT")
        need(read(package/"PROFILE.json", 2*MIB) == profile_raw, "RECIPROCAL_PACKAGE_UNCHANGED")
        report.update(status="PASS_PUBLIC_CLI_RECIPROCAL_SEAM", phase="COMPLETE", B_basis=basis["local_root"],
            B_received=received["admission"]["local_root"], B_contributed=contribution["local_root"],
            returned_export=cold["record"]["object_id"], source_sha256=digest(BODY),
            C_endpoint="UNKNOWN_ID_DISCOVERY_ONLY_NO_C_CUSTODY_OR_NATIVE_ACCEPTANCE")
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
    finally:
        run.close()
        if run.cleanup or run.live:
            report["status"] = "FAILED"
        report["cleanup"] = run.cleanup
        if preserved is not None:
            try:
                after = retained_map(); save(output/"A-PRESERVED-AFTER.json", after)
                need(after == preserved, "RECIPROCAL_A_SOURCE_EVIDENCE_STATE_CHANGED")
                report["A_preserved"] = True
            except BaseException as error:
                report.update(status="FAILED", preservation_error=str(error))
        report.update(wall_seconds=time.monotonic()-run.started, known_child_cpu_seconds=run.charged_cpu,
            harness_cpu_seconds=time.process_time()-run.cpu_started,
            cost_scope="Outer Job is aggregate authority; child controller+worker receipts are not added twice")
        if report["wall_seconds"] >= 210 or report["known_child_cpu_seconds"]+report["harness_cpu_seconds"] >= 145:
            report.update(status="FAILED", final_budget_error="RECIPROCAL_ORIGINAL_ALLOWANCE")
        save(output/"RECIPROCAL-RESULT.json", report)
        print(json.dumps({"status": report["status"], "calls": len(run.calls), "wall_seconds": report["wall_seconds"]}), flush=True)
    return 0 if report["status"] == "PASS_PUBLIC_CLI_RECIPROCAL_SEAM" else 1


if __name__ == "__main__":
    raise SystemExit(main())
