"""Selected pure delta/operator controls; no execution until root chooses a run.

Real selected codecs, delta, operator, typed locator and ledger; scripted child
ownership and HTTP exchange. No actual Node/Lean/native process, database, HTTP
listener or application network. READY is deliberately interrupted so no service
sleep or natural-expiry claim is manufactured by these controls.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace as NS
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
FIXTURE = ROOT/"experiments/v5-local-checks/contribution-bundle-controls01/checks/bundle-completion"
MANIFEST_SHA = "0bd22da5351f0f46ee9ac51ed6b856e8f909a2ed9a00a2c80b50a987b60907c9"
APPEND_SHA = "09dafc9677fde2266536714481140d81feb9df0e818a9757298c07e0f206a4ad"
DELTA_SHA = "6c67a896bfe97256125dc417bbc97b2e8feb41ac2da89074f471a8dfbc02cd34"
START, CPU = time.monotonic(), time.process_time()
MIB = 1024**2
CASES, FORBIDDEN = [], []


def need(ok, code):
    if not ok:
        raise AssertionError("EXPORT_OPERATOR_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 90 and time.process_time()-CPU < 45, "ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, pin=None, maximum=2*MIB):
    check()
    need(path.is_absolute() and path.is_file() and not path.is_symlink(), "INPUT")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum and (pin is None or sha(raw) == pin), "INPUT_PIN")
    return raw


def forbidden(*args, **kwargs):
    FORBIDDEN.append("EXTERNAL_EFFECT")
    raise AssertionError("EXPORT_OPERATOR_CONTROL_EXTERNAL_EFFECT")


def passed(name, **facts):
    check()
    CASES.append(dict(name=name, status="PASS", **facts))


def refused(call, fragment):
    try:
        call()
    except Exception as error:
        need(fragment in str(error), "WRONG_REFUSAL:"+str(error))
        return
    raise AssertionError("EXPORT_OPERATOR_CONTROL_MISSING_REFUSAL:"+fragment)


def load(args):
    package = Path(args.package)
    need(package.is_absolute() and package.resolve(strict=True) == package, "PACKAGE")
    raw = read(package/"SOURCES.json", args.profile_sha256)
    profile = json.loads(raw)
    source = read(package/"operator_support.py")
    pin = profile["files"]["_support"]
    need(pin["path"] == "operator_support.py" and pin["bytes"] == len(source)
         and pin["sha256"] == sha(source), "SUPPORT_PIN")
    name = "_export_operator_control_support"
    spec = importlib.util.spec_from_file_location(name, package/"operator_support.py")
    module = importlib.util.module_from_spec(spec)
    need(name not in sys.modules, "PRELOADED")
    sys.modules[name] = module
    exec(compile(source, str(package/"operator_support.py"), "exec"), module.__dict__)
    bound = module.bind(package, args.profile_sha256, args.python_runtime, check)
    need(sha(bound.raws["advertisement_delta"]) == DELTA_SHA, "DELTA_PIN")
    support = module.load_support(bound, check)
    core = module.load_source("_export_operator_control_core", bound.paths["_core"], bound.raws["_core"])
    return support, core


def fixture(s):
    raw = read(FIXTURE/"manifest.json", MANIFEST_SHA)
    append = s.F.strict(read(FIXTURE/"append.json", APPEND_SHA), 2*MIB)
    held = s.Delta.manifest(raw, MANIFEST_SHA, check_budget=check)
    units = [read(FIXTURE/entry.relative_path, entry.raw_sha256, entry.raw_bytes)
             for batch in held.batches for entry in batch]
    need(len(units) == 3 and sum(map(len, units)) == 10700, "RETAINED_CENSUS")
    rows = []
    for unit in units:
        parsed = s.PE.read_evidence(unit)
        for declaration in parsed.document["unit"][2]:
            rows.append(dict(semantic_id=s.semantic_id, unit_id=parsed.unit_id,
                export_id=s.S.export_id(s.semantic_id, parsed.unit_id, declaration[0]),
                name=declaration[0]))
    target_ids = {row["export_id"] for row in append["targets"]}
    need(len(target_ids) == 1 and len(rows) > len(target_ids), "SUPPORT_FIXTURE")
    return NS(raw=raw, units=units, rows=rows, targets=target_ids)


def delta_controls(s, f):
    calls = 0
    original = s.PE.read_evidence
    def counted(raw):
        nonlocal calls
        calls += 1
        return original(raw)
    with patch.object(s.PE, "read_evidence", counted):
        raw = s.Delta.prepare(f.raw, MANIFEST_SHA, f.units, check_budget=check)
    doc = s.F.strict(raw, s.Delta.MAX_PROPOSAL_BYTES)
    need(calls == 3 and doc["proposals"] == f.rows and doc["total_output_count"] == len(f.rows)
         and doc["omitted_output_count"] == 0 and doc["custody_checked"] is False
         and doc["published"] is False and doc["mathematical_acceptance"] is False, "ALL_OUTPUTS")
    need(any(row["export_id"] not in f.targets for row in doc["proposals"]), "SUPPORT_ONLY")
    passed("real-three-unit-all-output-includes-support", parsed_units=calls, exports=len(f.rows))

    support = next(row for row in f.rows if row["export_id"] not in f.targets)
    selected = s.F.strict(s.Delta.prepare(f.raw, MANIFEST_SHA, f.units,
        selected_export_ids=[support["export_id"]], check_budget=check), s.Delta.MAX_PROPOSAL_BYTES)
    need(selected["proposals"] == [support] and selected["omitted_output_count"] == len(f.rows)-1,
         "EXPLICIT_SUPPORT_SUBSET")
    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, f.units,
        selected_export_ids=["0"*64]), "SELECTED_EXPORT_NOT_IN_BUNDLE")
    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, f.units,
        selected_export_ids=[support["export_id"]]*2), "DUPLICATE_SELECTION")
    passed("explicit-subset-and-missing-or-duplicate-selection")

    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, list(reversed(f.units))), "UNIT_RAW_PIN")
    damaged = list(f.units); damaged[0] = bytes([damaged[0][0]^1])+damaged[0][1:]
    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, damaged), "UNIT_RAW_PIN")
    refused(lambda: s.Delta.prepare(f.raw, "0"*64, f.units), "BASELINE_MANIFEST_HASH")
    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, f.units[:-1]), "EXACT_UNIT_COUNT")
    def spent():
        raise ValueError("CONTROL_BUDGET_SPENT")
    refused(lambda: s.Delta.prepare(f.raw, MANIFEST_SHA, f.units, check_budget=spent), "CONTROL_BUDGET_SPENT")
    passed("raw-pins-order-census-and-budget-refusals")


class ReadyStop(RuntimeError):
    """Intentional control stop after all publication reads, before service wait."""


class FakeAdoption:
    def __init__(self, *args, **kwargs):
        pass


class FakeProcess:
    instances = []
    def __init__(self, adoption, configuration, evidence, *, mode, deadline, service_deadline):
        self.config = deepcopy(configuration)
        self.deadline, self.service_deadline = deadline, service_deadline
        self.process = None
        self.closed = self.channel_failed = self.forced_termination = False
        self.events = []; self.started = 0
        FakeProcess.instances.append(self)
    async def start(self):
        self.started += 1; self.events.append(("start",))
        self.process = NS(returncode=None)
        return dict(role=self.config["role"], semantic_id=self.config["semantic_id"])
    async def command(self, name, payload, *, until=None):
        need(time.monotonic() < until <= self.deadline, "FAKE_ORIGINAL_CUTOFF")
        self.events.append((name, deepcopy(payload)))
        return dict(status="SCRIPTED_OWNERSHIP_ONLY", mathematical_acceptance=False)
    async def close(self):
        self.closed = True
        if self.process is not None:
            self.process.returncode = 0
        self.events.append(("close",))
    def report(self):
        return dict(closed=self.closed, channel_failed=self.channel_failed,
                    mathematical_acceptance=False, scripted=True)


def configuration(s, area, f):
    endpoint = dict(host="127.0.0.1", port=43111, tls=False, server_name=None)
    return dict(schema="DMKN_ORDINARY_EXPORT_OPERATOR_OPERATION_V1",
        node=dict(schema="DMKN_V5_ORDINARY_EXPORT_OPERATOR_V1", role="custodian",
            state=str(area/"state"), semantic_id=s.semantic_id,
            egress=dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                        test_endpoints=[dict(host="127.0.0.1", port=43111)]),
            endpoints=[endpoint], listen=[], announce=[], bootstrap=[],
            limits=dict(service_ms=10000)), gateway=None, withdraw_exports=[],
        publication=dict(bundle_directory=str(FIXTURE),
            manifest=dict(path=str(FIXTURE/"manifest.json"), sha256=MANIFEST_SHA),
            selected_export_ids=None, requests=32, reply_bytes=MIB, attempt_timeout_ms=1000))


async def operator_case(s, core, f, area, *, corrupt_at=None, mutate=None):
    area.mkdir(); output = area/"output"; output.mkdir()
    runtime = area/"unused-runtime"; runtime.mkdir()
    cfg = configuration(s, area, f)
    if mutate is not None:
        mutate(cfg)
    reads, ready_calls = [], []
    expected = {row["export_id"]: s.F.compact(dict(schema=s.PP.LOCATOR_SCHEMA,
        semantic_id=s.semantic_id, unit_id=row["unit_id"], export_name=row["name"])) for row in f.rows}
    async def exchange(endpoint, route, request, maximum, timeout_ms, *, absolute_deadline):
        check()
        need(route == s.O.LOCATOR_ROUTE and endpoint.host == "127.0.0.1" and endpoint.port == 43111,
             "EXACT_OWN_READ")
        channel = FakeProcess.instances[-1]
        need(channel.started == 1 and absolute_deadline <= channel.service_deadline,
             "READ_SERVICE_HORIZON")
        identity = request["export_id"]
        raw = expected[identity]
        need(maximum == len(raw), "READ_EXACT_CAP")
        reads.append(identity); channel.events.append(("read", identity))
        if corrupt_at == len(reads):
            changed = s.F.strict(raw, MIB); changed["unit_id"] = "0"*64
            raw = s.F.compact(changed)
        return dict(status=200, raw=raw, request_bytes=len(s.F.compact(request)),
                    reply_bytes=len(raw), header_bytes=0)
    def ready(value):
        ready_calls.append(value)
        raise ReadyStop("SCRIPTED_STOP_AFTER_READY")
    allowance = NS(deadline=time.monotonic()+60, check=check)
    FakeProcess.instances.clear()
    with ExitStack() as stack:
        stack.enter_context(patch.object(s.L, "AdoptedLocationRuntime", FakeAdoption))
        stack.enter_context(patch.object(s.L, "OrdinaryLocationProcess", FakeProcess))
        stack.enter_context(patch.object(s.X, "exchange", exchange))
        try:
            await core.operate(s, cfg, allowance, node_runtime_root=runtime,
                workspace=area, mode="create", output=output, ready=ready)
        except Exception as error:
            return NS(error=error, channels=list(FakeProcess.instances), reads=reads, ready=ready_calls,
                      report=getattr(error, "report", None))
    raise AssertionError("EXPORT_OPERATOR_CONTROL_EXPECTED_SCRIPTED_STOP")


async def operator_controls(s, core, f, output):
    result = await operator_case(s, core, f, output/"paired-read-publish")
    need(type(result.error) is core.OperationFailure and result.report["error"]["type"] == "ReadyStop",
         "INTENTIONAL_READY_STOP")
    events = result.channels[0].events
    effect = [event for event in events if event[0] in ("read", "publish")]
    expected = []
    for row in f.rows:
        expected.extend([("read", row["export_id"]),
            ("publish", dict(semantic_id=s.semantic_id, export_id=row["export_id"]))])
    need(effect == expected and len(result.ready) == 1 and result.report["eligibility_budget"]["closed"] is True,
         "READ_BEFORE_EACH_PUBLISH")
    passed("all-output-exact-readback-before-each-scripted-publish", publications=len(f.rows),
           natural_service_test=False)

    for position in (1, 2):
        result = await operator_case(s, core, f, output/("bad-readback-"+str(position)), corrupt_at=position)
        need(type(result.error) is core.OperationFailure and "ORDINARY_LOCATOR_EXACT_EXPORT" in
             result.report["error"]["message"], "EXACT_READBACK_REFUSAL")
        pubs = [e for e in result.channels[0].events if e[0] == "publish"]
        need(len(pubs) == position-1 and not result.ready and result.channels[0].closed and
             result.report["eligibility_budget"]["requests"] == position and
             result.report["eligibility_budget"]["pending_requests"] == 0 and
             result.report["eligibility_budget"]["closed"] is True and
             result.report["eligibility_acquisition"]["http"]["failed_attempts"] == 1,
             "READBACK_FAILURE_PREFIX_AND_CHARGES")
    passed("failed-readback-no-publication-and-preserved-prefix", failed_positions=[1, 2])

    def invalid_attempt(cfg):
        cfg["withdraw_exports"] = [f.rows[0]["export_id"]]
        cfg["publication"]["attempt_timeout_ms"] = 0
    def invalid_gateway(cfg):
        cfg["node"]["role"] = "gateway"; cfg["node"]["endpoints"] = []
        cfg["publication"] = None
        cfg["gateway"] = dict(listener=dict(host="127.0.0.1", port=-1, tls=None), limits={},
            provider=dict(max_connections=1, max_requests=1, max_reply_bytes=1024, operation_ms=1000))
    for label, mutate, fragment in (("attempt", invalid_attempt, "PUBLICATION_ATTEMPT_MS"),
                                    ("listener", invalid_gateway, "LISTENER_PORT")):
        result = await operator_case(s, core, f, output/("invalid-"+label), mutate=mutate)
        need(fragment in str(result.error) and not result.reads and not result.ready and
             all(channel.started == 0 and not channel.events for channel in result.channels), "PRE_EFFECT_REFUSAL")
    passed("invalid-publication-or-gateway-config-before-effects")


async def execute(s, core, f, output):
    loop = asyncio.get_running_loop()
    errors = []
    loop.set_exception_handler(lambda _loop, context: errors.append(str(context.get("message"))))
    with ExitStack() as stack:
        # Do not replace socket.socket: Windows Proactor uses its type internally.
        stack.enter_context(patch.object(loop, "sock_connect", forbidden))
        stack.enter_context(patch.object(socket, "create_connection", forbidden))
        stack.enter_context(patch.object(subprocess, "Popen", forbidden))
        stack.enter_context(patch.object(asyncio, "create_subprocess_exec", forbidden))
        stack.enter_context(patch.object(sqlite3, "connect", forbidden))
        stack.enter_context(patch.object(s.H.Provider, "start", forbidden))
        delta_controls(s, f)
        await operator_controls(s, core, f, output)
    need(not errors and not FORBIDDEN, "UNEXPECTED_EFFECT_OR_LOOP_ERROR")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "python-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(output.is_absolute() and output.resolve() == output and output.is_relative_to(ROOT/"experiments")
         and not output.exists() and output.parent.is_dir(), "FRESH_CANONICAL_OUTPUT")
    s, core = load(args)
    f = fixture(s)
    output.mkdir()
    asyncio.run(execute(s, core, f, output))
    s.verify(); check()
    report = dict(status="PASS", groups=CASES, forbidden_effects=FORBIDDEN,
        scope="REAL_PURE_CODECS_OPERATOR_AND_TYPED_LOCATOR;SCRIPTED_NODE_AND_HTTP;NO_RUNTIME_QUALIFICATION",
        fixture_manifest_sha256=MANIFEST_SHA, fixture_append_sha256=APPEND_SHA,
        profile_sha256=args.profile_sha256, delta_sha256=DELTA_SHA,
        elapsed_wall_seconds=time.monotonic()-START, process_cpu_seconds=time.process_time()-CPU,
        mathematical_acceptance=False)
    raw = json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    need(len(raw) <= MIB, "REPORT_BOUND")
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode("utf-8"), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
