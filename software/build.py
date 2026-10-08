"""Rebuild installed Lean support from source under a bounded local stage.

Python -B -E -s -S build.py --lean-runtime ABS_RUNTIME --work ABS_NEW_WORK.
No prepared experimental .olean is consumed. This is an owner build operation,
not mathematical acceptance, a remote endpoint, or a hostile-source sandbox.
"""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time

INSTALL = Path(__file__).resolve().parent
sys.path.insert(0, str(INSTALL / "py"))

from domains import Domains
from storage import decode, encode, read, require
import run_stage

MIB = 1048576


def pin(path):
    path = Path(path).resolve(strict=True)
    raw = read(path, 16*MIB)
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def save_new(path, value):
    raw = encode(value)
    require(len(raw) <= MIB, "BUILD_RECORD_LIMIT")
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return pin(path)


def read_record(path):
    """Execution records include finite timing floats, unlike public requests."""
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_RECORD_KEY")
            value[key] = item
        return value
    def bad(_):
        raise ValueError("NONFINITE_RECORD_NUMBER")
    def finite(token):
        value = float(token)
        require(math.isfinite(value), "NONFINITE_RECORD_NUMBER")
        return value
    return json.loads(read(path, MIB), object_pairs_hook=pairs, parse_constant=bad, parse_float=finite)


def assets():
    lock = decode(read(INSTALL / "assets-lock.json", MIB))
    require(lock["schema"] == 1 and type(lock["files"]) is list and 1 <= len(lock["files"]) <= 256,
            "ASSET_LOCK_PROFILE")
    seen = set()
    for row in lock["files"]:
        require(set(row) == {"path", "bytes", "sha256"} and type(row["path"]) is str, "ASSET_LOCK_ROW")
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts and row["path"] not in seen,
                "ASSET_LOCK_PATH")
        seen.add(row["path"])
        path = (INSTALL / relative).resolve(strict=True)
        require(path.is_relative_to(INSTALL), "ASSET_DOMAIN")
        actual = pin(path)
        require(actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"], "ASSET_CHANGED")
    require({"native/BootstrapSupport.lean", "native/AgentReplayCore.lean", "native/AgentClient.lean",
             "py/codec.py", "py/source_codec.py", "py/symbol_index.py"} <= seen, "INCOMPLETE_ASSET_LOCK")
    return pin(INSTALL / "assets-lock.json")


def build(args):
    started = time.monotonic()
    work, runtime = args.work.resolve(), args.lean_runtime.resolve(strict=True)
    target = INSTALL / "build"
    require(not work.exists() and not target.exists(), "FRESH_BUILD_REQUIRED")
    policy = {"schema": 2, "domains": {"install": str(INSTALL), "state": str(work / "reserved-state"),
        "scratch": str(work / "scratch"), "lean_runtime": str(runtime)}}
    domains = Domains.from_stage_plan(policy)
    require(work != Path(work.anchor) and not work.is_relative_to(INSTALL)
            and not INSTALL.is_relative_to(work) and not runtime.is_relative_to(work)
            and not work.is_relative_to(runtime), "BUILD_WORK_DOMAIN")
    asset_pin = assets()
    lean, python = pin(runtime / "bin/lean.exe"), pin(sys.executable)
    domain_pin, runner_pin = pin(INSTALL / "py/domains.py"), pin(INSTALL / "py/run_stage.py")
    sources = {name: pin(INSTALL / "native" / (name + ".lean"))
               for name in ("BootstrapSupport", "AgentReplayCore", "AgentClient")}
    request = domains.scratch / "support-build"
    stage = request / "stage-build"
    request.mkdir(parents=True, exist_ok=False)
    plan = {"schema": 2, "domains": domains.as_dict(), "domains_source": domain_pin,
        "request_directory": str(request), "stage_directory": str(stage), "stage": "support-build",
        "expected_runner_sha256": runner_pin["sha256"], "lean": lean, "python": python,
        "seconds": 300, "memory_mib": 4096, "bytes": 128*MIB,
        "inputs": [{**domain_pin, "as": "domains.py"}, *[
            {**value, "as": "native/" + name + ".lean"} for name, value in sources.items()]],
        "output_directories": ["lib"], "steps": [
            {"kind": "lean", "label": "build-" + name, "cwd": "$RUN/input/native",
             "lean_path": ["$RUN/out/lib"], "expected_exit": 0,
             "argv": ["-R", "$RUN/input/native", "-o", "$RUN/out/lib/" + name + ".olean",
                      "$RUN/input/native/" + name + ".lean"]}
            for name in ("BootstrapSupport", "AgentReplayCore")]}
    plan_path = request / "build-plan.json"
    plan_pin = save_new(plan_path, plan)
    with redirect_stdout(sys.stderr):
        exit_code = run_stage.execute(plan_path, stage, "support-build", plan_pin["sha256"])
    require(exit_code == 0, "SUPPORT_BUILD_FAILED")
    receipt = read_record(stage / "stage.json")
    require(receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
            and len(receipt["steps"]) == 2 and all(item["exit_code"] == 0 for item in receipt["steps"])
            and receipt["execution_endpoint"]["children_quiescent"] is True
            and receipt["final_job"]["active_processes"] == 0,
            "BUILD_RECEIPT_STATUS")
    # The runner already authenticates all commands and confirms child cleanup.
    # Binding copied outputs to its immutable output list prevents promotion of
    # an unrelated operator file as the result of this build.
    outputs = {}
    for key, name in (("bootstrap_olean", "BootstrapSupport"), ("core_olean", "AgentReplayCore")):
        source = stage / "out/lib" / (name + ".olean")
        source_pin = pin(source)
        require(source_pin in receipt["outputs"], "BUILD_OUTPUT_RECEIPT_BINDING")
        outputs[key] = source_pin
    (target / "lib").mkdir(parents=True, exist_ok=False)
    for key, source_pin in list(outputs.items()):
        destination = target / "lib" / Path(source_pin["path"]).name
        shutil.copyfile(source_pin["path"], destination)
        output = pin(destination)
        require(output["bytes"] == source_pin["bytes"] and output["sha256"] == source_pin["sha256"], "BUILD_COPY_CHANGED")
        outputs[key] = output
    result = {"status": "LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE", "lean": lean,
        "python": python, "sources": sources, "assets_lock": asset_pin,
        "runner": runner_pin, "domains_source": domain_pin, "plan": plan_pin,
        "stage_receipt": pin(stage / "stage.json"), "outputs": outputs,
        "elapsed_seconds_before_final_receipt": time.monotonic()-started,
        "mathematicalAcceptance": False, "scope": "two local source compilations; receiving bootstrap still required"}
    result_pin = save_new(target / "build-receipt.json", result)
    return {"status": result["status"], "receipt": result_pin}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean-runtime", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    args = parser.parse_args()
    require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
            and sys.flags.no_user_site, "RUN_PYTHON_WITH_B_E_s_S")
    try:
        result = build(args)
    except Exception as error:
        result = {"status": "BUILD_FAILED", "code": getattr(error, "code", type(error).__name__),
            "detail": str(error)[:1024], "mathematicalAcceptance": False}
        sys.stdout.buffer.write(encode(result))
        return 1
    sys.stdout.buffer.write(encode(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
