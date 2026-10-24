"""Two packaged preview calls over a bounded loopback static responder.

Source-only until selected. Real public CLI/HTTP, one exact reply and one
same-length tampered reply; no provider/index, owner/custody, native compiler,
proof acquisition or mathematical acceptance. An outer finite Windows Job owns
the harness and descendants. All prior inputs and partial outputs are preserved.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import threading

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PACKAGE = LOCAL/"ordinary-preview-assembly-01/package"
OUTPUT = LOCAL/"ordinary-preview-public-01/public"
FIXTURE = LOCAL/("ordinary-project-extraction-public-01/project/completion/previews/"
    "d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a.json")
FIXTURE_PIN = {"bytes": 1351,
    "sha256": "362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c"}
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_PIN = {"bytes": 38940,
    "sha256": "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"}
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(HELPER_PIN["bytes"]+1)
    need(len(raw) == HELPER_PIN["bytes"] and hashlib.sha256(raw).hexdigest() ==
         HELPER_PIN["sha256"], "PREVIEW_PUBLIC_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_preview_public_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)
    module.ordinary(HELPER)
    return module


class StaticPreview:
    """At most two loopback connections; no path ever resolves to a file.

    HTTPServer is deliberately not threaded per request. One bounded background
    thread lets the main thread supervise the actual public processes. Socket
    reads time out, and stop/join/server_close are explicit even on failure.
    """
    def __init__(self, raw, request, until, h):
        self.raw, self.request, self.until, self.h = raw, request, until, h
        self.rows, self.errors, self.connections = [], [], 0
        self.stop = threading.Event()
        outer = self

        class Server(HTTPServer):
            allow_reuse_address = False

            def get_request(self):
                connection, address = super().get_request()
                outer.connections += 1
                connection.settimeout(1.0)
                return connection, address

            def handle_error(self, request, address):
                outer.errors.append("STATIC_HANDLER_FAILURE")

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):
                pass

            def do_POST(self):
                self.close_connection = True
                row = {"path": self.path, "mode": None, "request_valid": False}
                outer.rows.append(row)
                try:
                    need(len(outer.rows) <= 2 and self.path == "/v5/ordinary/preview"
                         and self.request_version == "HTTP/1.1", "STATIC_PREVIEW_ONLY_ROUTE")
                    headers = list(self.headers.items())
                    lower = {key.lower(): value for key, value in headers}
                    need(len(headers) == 4 and len(lower) == 4 and set(lower) == {
                        "host", "content-length", "content-type", "connection"} and
                        lower["host"] == "127.0.0.1:"+str(outer.server.server_port) and
                        lower["content-type"] == "application/json" and
                        lower["connection"].lower() == "close", "STATIC_PREVIEW_HEADERS")
                    expected = outer.h.canonical(outer.request)
                    need(lower["content-length"] == str(len(expected)) and
                         len(expected) <= 1024, "STATIC_PREVIEW_REQUEST_BOUND")
                    received = self.rfile.read(len(expected))
                    need(received == expected, "STATIC_PREVIEW_EXACT_REQUEST")
                    number = len(outer.rows)
                    response = outer.raw if number == 1 else outer.raw[:-1]+b"!"
                    row.update(request_valid=True, request=outer.request.copy(),
                        request_bytes=len(received), mode="exact" if number == 1 else "tampered",
                        response_bytes=len(response), response_sha256=outer.h.sha(response))
                    # send_response() would add Date/Server, which the product's
                    # intentionally strict transport does not permit.
                    self.send_response_only(200)
                    self.send_header("Content-Length", str(len(response)))
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(response)
                    self.wfile.flush()
                    row["response_written"] = True
                except BaseException as error:
                    row.update(error_type=type(error).__name__, error=str(error)[:500])
                    outer.errors.append("STATIC_PREVIEW_REQUEST_FAILURE")

            def do_GET(self):
                self.close_connection = True
                outer.errors.append("STATIC_UNEXPECTED_GET")

        self.server = Server(("127.0.0.1", 0), Handler)
        self.server.timeout = 0.2
        self.thread = threading.Thread(target=self.loop, name="preview-static-two-replies", daemon=True)
        self.started, self.closed = False, False

    def loop(self):
        try:
            while not self.stop.is_set() and time.monotonic() < self.until and self.connections < 2:
                self.server.handle_request()
        except BaseException as error:
            self.errors.append("STATIC_LOOP_"+type(error).__name__)

    def start(self):
        self.thread.start()
        self.started = True
        return self.server.server_port

    def close(self, cleanup_until):
        self.stop.set()
        if self.started:
            self.thread.join(max(0, min(3, cleanup_until-time.monotonic())))
        self.server.server_close()
        self.closed = True
        need(not self.thread.is_alive(), "STATIC_PREVIEW_THREAD_NOT_CLOSED")

    def report(self):
        return {"connections": self.connections, "requests": self.rows, "errors": self.errors,
            "thread_alive": self.thread.is_alive(), "server_closed": self.closed,
            "scope": "STATIC_LOOPBACK_METADATA_RESPONDER_NOT_INDEX_OR_CUSTODY_PROVIDER"}


class Check:
    def __init__(self, args, h):
        self.args, self.h, self.deadline = args, h, START_WALL+args.wall_seconds
        self.charged, self.cpu_complete = 0.0, True
        self.calls, self.held, self.output_created, self.server = [], {}, False, None

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-START_CPU+self.charged
             < self.args.cpu_seconds, "PREVIEW_PUBLIC_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None):
        value = self.h.pin(path, self.check)
        need(expected is None or value == expected, "PREVIEW_PUBLIC_EXACT_PIN:"+str(path))
        need(self.held.setdefault(str(path), value) == value, "PREVIEW_PUBLIC_INPUT_CHANGED")
        return value

    def tree(self, root):
        return self.h.Smoke.capture_tree(self, root)

    def document(self, path, maximum=4*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def prepare(self):
        h = self.h
        self.package = h.ordinary(self.args.package, directory=True)
        self.output = h.ordinary(self.args.output, directory=True, fresh=True)
        need(self.package == PACKAGE and self.output == OUTPUT, "PREVIEW_PUBLIC_SELECTED_PATHS")
        for digest in (self.args.profile_sha256, self.args.assembly_sha256):
            need(re.fullmatch(r"[0-9a-f]{64}", digest), "PREVIEW_PUBLIC_HASH")
        roots = [self.package, self.output, PYTHON.parent, LEAN]
        need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "PREVIEW_PUBLIC_DISJOINT")
        self.hold(Path(__file__).resolve()); self.hold(HELPER, HELPER_PIN)
        self.hold(FIXTURE, FIXTURE_PIN)
        self.raw = h.read(FIXTURE, MIB)
        need(h.sha(self.raw) == FIXTURE_PIN["sha256"] and len(self.raw) == 1351,
             "PREVIEW_PUBLIC_RETAINED_FIXTURE")
        self.preview_doc = h.diagnostic_json(self.raw)
        profile_raw = h.read(self.package/"PROFILE.json", 2*MIB)
        need(h.sha(profile_raw) == self.args.profile_sha256, "PREVIEW_PUBLIC_PROFILE_PIN")
        profile = h.diagnostic_json(profile_raw)
        need(profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             profile["installation_manifest_sha256"] == INSTALLATION, "PREVIEW_PUBLIC_PROFILE")
        manifest_raw = h.read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(h.sha(manifest_raw) == INSTALLATION, "PREVIEW_PUBLIC_INSTALLATION_PIN")
        manifest = h.diagnostic_json(manifest_raw)
        need(manifest["implementation"]["semantic_id"] == SEMANTIC and
             h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(manifest["implementation"]))
             == IMPLEMENTATION, "PREVIEW_PUBLIC_IMPLEMENTATION")
        payload = dict(profile["files"])
        runtimes = {"python_runtime": PYTHON.parent, "lean_runtime": LEAN}
        for name, pin in manifest["files"].items():
            parts = h.relative(name).parts
            if parts[0] in runtimes:
                self.hold(runtimes[parts[0]].joinpath(*parts[1:]), pin)
            else:
                payload["installation/"+name] = pin
        payload["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": INSTALLATION}
        need(len(payload) == 134, "PREVIEW_PUBLIC_PAYLOAD_CENSUS")
        receipt_raw = h.read(self.package/"ASSEMBLY.json", 2*MIB)
        need(h.sha(receipt_raw) == self.args.assembly_sha256, "PREVIEW_PUBLIC_ASSEMBLY_PIN")
        receipt = h.diagnostic_json(receipt_raw)
        changed = {"peer.py", "peer_api.py"}
        need(receipt["status"] == "ASSEMBLED_NOT_ADOPTED" and
             receipt["profile_sha256"] == self.args.profile_sha256 and
             receipt["installation_manifest_sha256"] == INSTALLATION and
             receipt["implementation_id"] == IMPLEMENTATION and receipt["files_excluding_profile"] == 134
             and receipt["added"] == [] and set(receipt["changed"]) == changed and
             receipt["changed_or_added"] == {name: payload[name] for name in changed},
             "PREVIEW_PUBLIC_REVIEWED_ASSEMBLY")
        payload["PROFILE.json"] = {"bytes": len(profile_raw), "sha256": self.args.profile_sha256}
        payload["ASSEMBLY.json"] = {"bytes": len(receipt_raw), "sha256": self.args.assembly_sha256}
        for name, pin in payload.items():
            self.hold(self.package/h.relative(name), pin)
        need(self.tree(self.package) == set(payload), "PREVIEW_PUBLIC_PACKAGE_CENSUS")
        self.package_files = set(payload)
        # Load selected pure support only. No method below opens an owner/store.
        base = h.load_exact(self.package/"owner.py", "_preview_public_owner",
                            profile["files"]["owner.py"], self.check)
        loader = base.bootstrap(self.package, self.args.profile_sha256, self.check)
        loaded = loader.load(self.package, self.args.profile_sha256, runtimes,
                             self.deadline, check_parent=self.check)
        adapter = loaded.peer_api.OrdinaryExportAdapter(SEMANTIC)
        self.record = adapter.extract(self.raw)
        self.namespace = adapter.namespace
        self.selection = {"provider": "static-preview", "snapshot_id": "1"*64, "record": self.record}
        need(self.record["object_id"] == FIXTURE.stem and self.record["object_bytes"] == 1351 and
             self.record["object_sha256"] == FIXTURE_PIN["sha256"], "PREVIEW_PUBLIC_FIXTURE_RECORD")
        # NativeInstallation.open already verifies/loads these support modules,
        # but does not run a native checker or create a mathematical owner.
        # Reuse its exact modules; a second domains load would collide.
        self.supervisor, self.jobs = loaded.installation._supervisor, loaded.installation._job_module
        for role, module in (("supervisor", self.supervisor), ("job", self.jobs)):
            need(Path(module.__file__).resolve() == loaded.installation.path(role),
                 "PREVIEW_PUBLIC_SUPERVISOR_ROLE")
        self.output.mkdir(); self.output_created = True
        (self.output/"calls").mkdir()
        h.save(self.output/"INPUTS.json", {"pins": self.held.copy(), "selection": self.selection,
            "snapshot_label": "SYNTHETIC_NOT_SEARCH_MEMBERSHIP_EVIDENCE", "original_allowance": {
                "wall_seconds": self.args.wall_seconds, "cpu_seconds": self.args.cpu_seconds,
                "memory_mib": self.args.memory_mib}})

    def command(self, label, config, expected_exit):
        self.check()
        need(label in ("01-exact", "02-tampered") and len(self.calls) < 2 and
             not any(row["label"] == label for row in self.calls), "PREVIEW_PUBLIC_TWO_CALLS")
        config_path = self.output/(label+"-CONFIG.json")
        config_pin = self.h.save(config_path, config); self.hold(config_path, config_pin)
        output = self.output/(label+"-output")
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(40, math.floor(self.deadline-time.monotonic())-10),
            "cpu_seconds": min(12, math.floor(self.args.cpu_seconds-self.charged-
                (time.process_time()-START_CPU))-3), "memory_mib": self.args.memory_mib,
            "active_processes": 2, "stdout_bytes": 4*MIB, "stderr_bytes": MIB})
        need(grant["wall_seconds"] >= 40 and grant["cpu_seconds"] >= 5,
             "PREVIEW_PUBLIC_REMAINING_GRANT")
        argv = [str(PYTHON), "-I", "-S", "-B", str(self.package/"peer.py"), "preview",
            "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(LEAN), "--config", str(config_path),
            "--config-sha256", config_pin["sha256"], "--output", str(output),
            "--wall-seconds", str(grant["wall_seconds"]-5),
            "--cpu-seconds", str(grant["cpu_seconds"]-1), "--memory-mib", str(self.args.memory_mib)]
        event = {"label": label, "argv": argv, "limits": grant, "expected_exit": expected_exit,
            "public_result": None, "cpu_complete": False, "charged_cpu_seconds": grant["cpu_seconds"]}
        self.calls.append(event)
        self.charged += grant["cpu_seconds"]
        known = False
        supervision = None
        try:
            supervision = self.supervisor.supervise(argv, self.output, self.output/"calls"/label,
                                                   grant, self.jobs.Job)
            event["supervision"] = supervision
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            observed = final.get("cpu_seconds") if type(final) is dict else None
            known = type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
            if known:
                self.charged += observed-grant["cpu_seconds"]
            self.cpu_complete = self.cpu_complete and known
            event.update(cpu_complete=known, charged_cpu_seconds=observed if known else grant["cpu_seconds"])
            self.h.save(self.output/"calls"/(label+"-SUPERVISION.json"), event)
        raw = self.h.read(self.output/"calls"/label/"stdout.txt", 4*MIB)
        if raw:
            event["public_result"] = self.h.diagnostic_json(raw)
        need(known, "PREVIEW_PUBLIC_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        self.h.clean(supervision, exit_code=expected_exit)
        need(self.h.read(self.output/"calls"/label/"stderr.txt", MIB) == b"", "PREVIEW_PUBLIC_STDERR")
        result = event["public_result"]
        need(type(result) is dict and result.get("ok") is (expected_exit == 0) and
             result.get("operation") == "preview" and not result.get("close_errors") and
             result == self.document(output/"RESULT.json"), "PREVIEW_PUBLIC_RESULT")
        need(self.tree(output) == {"RESULT.json"}, "PREVIEW_PUBLIC_NO_STATE_OUTPUTS")
        self.check()
        return result

    def run(self, report):
        self.check()
        request = {"schema": "DMKN_ORDINARY_PREVIEW_REQUEST_V1",
                   "object_sha256": FIXTURE_PIN["sha256"], "object_bytes": 1351}
        self.server = StaticPreview(self.raw, request, self.deadline-6, self.h)
        port = self.server.start()
        config = {"contacts": {"static-preview": {"host": "127.0.0.1", "port": port,
            "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}},
            "selection": self.selection, "limits": {"requests": 1, "reply_bytes": 1351}}
        report["phase"] = "PUBLIC_EXACT_PREVIEW"
        good = self.command("01-exact", config, 0)
        need(good["profile_sha256"] == self.args.profile_sha256 and
             good["implementation_id"] == IMPLEMENTATION and good["semantic_id"] == SEMANTIC and
             good["store_id"] is None and good["catalog"] is None and good["custody"] is None,
             "PREVIEW_PUBLIC_NO_SELECTED_STATE")
        success = good["result"]
        need(success["status"] == "PREVIEW_BOUND_NOT_ACCEPTED" and
             success["selection"] == self.selection and success["namespace"] == self.namespace and
             success["preview"] == self.preview_doc and self.h.canonical(success["preview"]) == self.raw and
             success["preview_sha256"] == FIXTURE_PIN["sha256"] and success["preview_bytes"] == 1351,
             "PREVIEW_PUBLIC_EXACT_PREVIEW")
        report["phase"] = "PUBLIC_TAMPER_REFUSAL"
        refused = self.command("02-tampered", config, 1)
        failure = refused.get("detail", {})
        need(refused.get("phase") == "PREVIEW" and refused.get("result") is None and
             failure.get("status") == "FAILED" and failure.get("selection") == self.selection and
             failure.get("error", {}).get("code") == "ORDINARY_PREVIEW_EXACT_BYTES" and
             failure.get("preview") is None, "PREVIEW_PUBLIC_EXACT_REFUSAL")
        for item, failed in ((success, False), (failure, True)):
            need(item["mathematical_acceptance"] is False and item["evidence_bound"] is False and
                 item["snapshot_membership_reverified"] is False and item["cleanup_errors"] == [],
                 "PREVIEW_PUBLIC_FALSE_AUTHORITY")
            network, acquisition = item["network"], item["acquisition"]
            need(network["requests"] == 1 and network["charged_reply_bytes"] == 1351 and
                 network["closed"] is True and network["pending_requests"] == 0 and
                 network["reserved_reply_bytes"] == 0 and network["external_prepaid"] == [],
                 "PREVIEW_PUBLIC_ONE_CHARGED_REQUEST")
            need(acquisition["http"]["failed_attempts"] == int(failed) and
                 acquisition["http"]["completed_responses"] == 1 and
                 acquisition["http"]["actual_reply_bytes"] == 1351,
                 "PREVIEW_PUBLIC_ACTUAL_HTTP_ACCOUNTING")
        self.server.close(self.deadline)
        observed = self.server.report()
        need(observed["connections"] == 2 and len(observed["requests"]) == 2 and
             not observed["errors"] and not observed["thread_alive"] and observed["server_closed"] and
             all(row["request_valid"] and row.get("response_written") is True for row in observed["requests"])
             and [row["mode"] for row in observed["requests"]] == ["exact", "tampered"],
             "PREVIEW_PUBLIC_RESPONDER_CLOSURE")
        self.h.save(self.output/"SERVER.json", observed)
        report["phase"] = "PRESERVATION"
        for path, pin in tuple(self.held.items()):
            self.hold(Path(path), pin)
        need(self.tree(self.package) == self.package_files, "PREVIEW_PUBLIC_PACKAGE_UNCHANGED")
        self.h.save(self.output/"IMMUTABLE-FILES.json", self.held.copy())
        need(len(self.calls) == 2 and self.cpu_complete, "PREVIEW_PUBLIC_TWO_CLOSED_CALLS")
        report.update(status="PASS_PUBLIC_PREVIEW_AND_TAMPER_REFUSAL", phase="COMPLETE",
            original_preview=FIXTURE_PIN, preview_export_id=self.record["object_id"],
            no_owner_or_custody_arguments=True, no_native_or_evidence_operation=True,
            server=observed, mathematical_acceptance=False)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON, "PREVIEW_PUBLIC_RUNTIME")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "assembly-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    args = parser.parse_args()
    need(args.wall_seconds == 75 and args.cpu_seconds == 32 and args.memory_mib == 512,
         "PREVIEW_PUBLIC_FINITE_ENVELOPE")
    check = Check(args, helpers())
    report = {"status": "FAILED", "phase": "PREFLIGHT", "calls": check.calls,
        "claim": "TWO_LOCAL_PUBLIC_METADATA_CALLS_NOT_INDEX_COVERAGE_MATH_OR_GLOBAL_DEPLOYMENT",
        "retention": "ALL_PRIOR_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
    try:
        check.prepare(); check.run(report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000],
            preservation="POST_FAILURE_INPUT_AUDIT_REQUIRED_NO_RENEWED_ALLOWANCE")
    finally:
        if check.server is not None:
            try:
                check.server.close(check.deadline)
            except BaseException as error:
                report.update(status="FAILED", cleanup_error=type(error).__name__+":"+str(error)[:500])
            report["server"] = check.server.report()
        report.update(wall_seconds=time.monotonic()-START_WALL,
            controller_cpu_seconds=time.process_time()-START_CPU,
            inclusive_child_job_cpu_charged=check.charged, child_cpu_complete=check.cpu_complete,
            accounting="INCLUSIVE_CHILD_CPU_ONCE_UNKNOWN_FULL_GRANT_THEN_STOP_OUTER_COUNTS_FINAL_REPORT")
        if (not check.cpu_complete or report["wall_seconds"] >= args.wall_seconds or
                report["controller_cpu_seconds"]+check.charged >= args.cpu_seconds):
            report.update(status="FAILED", budget_error="PREVIEW_PUBLIC_ORIGINAL_ALLOWANCE")
        if check.output_created:
            check.h.save(check.output/"PUBLIC-CHECK-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_PUBLIC_PREVIEW_AND_TAMPER_REFUSAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
