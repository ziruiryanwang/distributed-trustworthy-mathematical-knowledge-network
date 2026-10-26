"""Selected assembled CLI: exact kit preparation and unfinished-client shutdown.

No native checking, owner DB, source authoring or external network. Root must
select a fresh exact package and finite outer Job before this can run.
"""
from __future__ import annotations

import time
START = time.monotonic()
CPU = time.process_time()
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
DEADLINE = START + 55
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 15,
         "TRANSPORT_PUBLIC_ORIGINAL_ENVELOPE")


def read(path):
    check()
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB, "TRANSPORT_PUBLIC_INPUT_BOUND")
    return raw


def document(path):
    return json.loads(read(path))


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "TRANSPORT_PUBLIC_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)


async def scenario(args, output, report):
    package, checkout = Path(args.package), Path(args.source_root)
    need(hashlib.sha256(read(package/"PROFILE.json")).hexdigest() == args.profile_sha256,
         "TRANSPORT_PUBLIC_PROFILE_PIN")
    request = dict(action="directory-serve", entries=[dict(
        specs=[dict(tag="declaration-kind", value="theorem")],
        endpoints=[dict(host="127.0.0.1", port=38191, tls=False, server_name=None)])],
        host="127.0.0.1", port=0, tls=None, lease_seconds=2, cleanup_seconds=10,
        limits=dict(max_connections=1, max_requests=4, max_reply_bytes=MIB,
                    operation_ms=60000), operation_output=str(output/"public"))
    request_path = output/"request.json"
    save(request_path, request)
    report["scope"] = "REAL_OFFLINE_PREPARATION_AND_PUBLIC_LEASE_NO_MATHEMATICS"
    children, files, writer, errors = {}, [], None, []
    try:
        for label, wrapper, expected in (
            ("prepare", checkout/"software/v5/ordinary_bounded_transport/prepare_selected.py", 0),
            ("old-wrapper-refusal", checkout/"software/v5/ordinary_network_kit/prepare_selected.py", 1),
        ):
            check()
            stdout = (output/(label+".stdout")).open("xb")
            stderr = (output/(label+".stderr")).open("xb")
            files.extend((stdout, stderr))
            argv = [sys.executable, "-I", "-S", "-B", str(wrapper), "--package", str(package),
                    "--profile-sha256", args.profile_sha256, "--request", str(request_path),
                    "--output", str(output/label)]
            child = await asyncio.create_subprocess_exec(*argv, cwd=ROOT,
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW)
            children[label] = child
            async with asyncio.timeout_at(DEADLINE-10):
                code = await child.wait()
            need(code == expected, "TRANSPORT_PUBLIC_PREPARATION_EXIT:"+label)
            stdout.flush(); stderr.flush()
        need(not (output/"old-wrapper-refusal").exists() and
             b"SELECT_UNKNOWN_INTERFACE" in read(output/"old-wrapper-refusal.stderr"),
             "TRANSPORT_PUBLIC_OLD_WRAPPER_FAIL_CLOSED")
        receipt = document(output/"prepare/RECEIPT.json")
        arguments = document(output/"prepare/arguments.json")
        need(arguments.get("entry") == "peer" and
             arguments.get("profile_sha256") == args.profile_sha256,
             "TRANSPORT_PUBLIC_ARGUMENT_BINDING")
        tokens = arguments["arguments"]
        need(type(tokens) is list and tokens[0] == "directory-serve" and
             all(type(token) is str for token in tokens), "TRANSPORT_PUBLIC_ARGUMENT_TOKENS")
        diagnostics = output/"diagnostics"
        argv = [sys.executable, "-I", "-S", "-B", str(package/"run.py"),
                "--profile-sha256", args.profile_sha256,
                "--python-runtime", args.python_runtime, "--lean-runtime", args.lean_runtime,
                "--diagnostics", str(diagnostics), "--wall-seconds", "35", "--cpu-seconds", "15",
                "--memory-mib", "768", "--active-processes", "4",
                "--stdout-bytes", str(MIB), "--stderr-bytes", str(MIB), "peer", "--", *tokens]
        stdout = (output/"service.stdout").open("xb")
        stderr = (output/"service.stderr").open("xb")
        files.extend((stdout, stderr))
        save(output/"SERVICE-COMMAND.json", dict(argv=argv, cwd=str(ROOT), attempts=1))
        child = await asyncio.create_subprocess_exec(*argv, cwd=ROOT,
            stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW)
        children["service"] = child
        ready_path = output/"public/READY.json"
        ready, partial = None, 0
        async with asyncio.timeout_at(DEADLINE-12):
            while ready is None:
                need(child.returncode is None, "TRANSPORT_PUBLIC_SERVICE_EARLY_EXIT")
                if ready_path.exists():
                    with ready_path.open("rb") as stream:
                        raw = stream.read(65537)
                    need(len(raw) <= 65536, "TRANSPORT_PUBLIC_READY_BOUND")
                    try:
                        ready = json.loads(raw)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        partial += 1
                    else:
                        break
                check(); await asyncio.sleep(0.01)
        need(ready["host"] == "127.0.0.1" and ready["tls"] is False and
             type(ready["port"]) is int and 0 < ready["port"] <= 65535,
             "TRANSPORT_PUBLIC_READY_ENDPOINT")
        connected = time.monotonic()
        async with asyncio.timeout_at(DEADLINE-8):
            reader, writer = await asyncio.open_connection(ready["host"], ready["port"])
            # Deliberately incomplete headers: neither dispatch nor body parsing
            # can finish before shutdown. This client is kept live until EOF.
            writer.write(b"POST /v5/ordinary/contacts HTTP/1.1\r\nHost: localhost\r\n")
            await writer.drain()
            try:
                need(await reader.read(1) == b"", "TRANSPORT_PUBLIC_STALLED_CLIENT_EOF")
                client_close = "EOF"
            except ConnectionError as error:
                client_close = type(error).__name__
            code = await child.wait()
        need(code == 0, "TRANSPORT_PUBLIC_SERVICE_EXIT")
        elapsed = time.monotonic()-connected
        need(elapsed < 8, "TRANSPORT_PUBLIC_CLEANUP_NOT_OPERATION_TIMEOUT")
        public, launch = document(output/"public/RESULT.json"), document(diagnostics/"RUN.json")
        supervision = document(diagnostics/"SUPERVISION.json")
        need(public.get("ok") is True and public.get("operation") == "directory-serve" and
             public.get("profile_sha256") == args.profile_sha256 and
             public.get("config_sha256") == hashlib.sha256(read(output/"prepare/config.json")).hexdigest() and
             public.get("catalog") is None and public.get("custody") is None and
             public.get("store_id") is None and
             not public.get("close_errors") and not public.get("final_budget_error"),
             "TRANSPORT_PUBLIC_OPERATION_REPORT")
        result = public["result"]
        status = result["provider"]
        need(result["status"] == "LEASE_FINISHED" and result["quiescent"] is True and
             result["cleanup_errors"] == [] and status["requests"] == 1 and
             status["active"] == 0 and status["reserved_reply_bytes"] == 0 and
             status["mathematical_acceptance"] is False,
             "TRANSPORT_PUBLIC_SERVICE_QUIESCENCE")
        need(launch.get("ok") is True and launch.get("profile_sha256") == args.profile_sha256 and
             supervision.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED" and
             supervision.get("direct_child_reaped") is True and
             supervision.get("job_closed") is True and supervision.get("cleanup_errors") == [] and
             supervision["final_job"]["active_processes"] == 0,
             "TRANSPORT_PUBLIC_LAUNCHER_CLOSED")
        report.update(preparation_receipt=receipt, ready=ready, public=public,
                      launcher=launch, supervision=supervision, ready_partial_observations=partial,
                      stalled_client_seconds=elapsed, client_close=client_close,
                      old_wrapper_refused=True, assertions_passed=True)
    finally:
        if writer is not None:
            writer.close()
            try:
                async with asyncio.timeout_at(DEADLINE):
                    await writer.wait_closed()
            except ConnectionError:
                pass  # A reset is an expected outcome of aborting this client.
            except BaseException as error:
                errors.append("client:"+type(error).__name__)
        for label, child in children.items():
            if child.returncode is None:
                try:
                    child.kill()
                    async with asyncio.timeout_at(DEADLINE):
                        await child.wait()
                except BaseException as error:
                    errors.append(label+":"+type(error).__name__)
        for stream in files:
            stream.close()
        report["children_reaped"] = {label: child.returncode is not None
                                     for label, child in children.items()}
        report["cleanup_errors"] = errors
    need(not errors and all(report["children_reaped"].values()), "TRANSPORT_PUBLIC_FINAL_CLOSURE")


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and Path.cwd() == ROOT, "TRANSPORT_PUBLIC_PROFILE")
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("source-root", "package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(output.is_absolute() and output.parent.is_dir() and not output.exists(),
         "TRANSPORT_PUBLIC_FRESH_OUTPUT")
    output.mkdir()
    report = {"status": "RUNNING", "mathematical_acceptance": False}
    try:
        asyncio.run(scenario(args, output, report))
        check(); report["status"] = "PASS"
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
