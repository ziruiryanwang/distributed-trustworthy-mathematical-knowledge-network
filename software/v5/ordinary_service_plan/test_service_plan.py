"""Focused finite-service orchestration controls; root selects execution.

Synthetic reports below test validation only. The optional real path creates
empty stores through current constructors, never mathematical accepted roots.
No native initialization, publication, build or historical state is used.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START_WALL + 220


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-START_CPU < 60,
         "SERVICE_TEST_ORIGINAL_ENVELOPE")


def read(path, maximum=4*MIB):
    check()
    with Path(path).open("rb") as stream:
        raw = stream.read(maximum+1)
    need(0 < len(raw) <= maximum, "SERVICE_TEST_READ_BOUND")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 4*MIB, "SERVICE_TEST_WRITE_BOUND")
    with Path(path).open("xb") as stream:
        stream.write(raw+b"\n")


def sha(path):
    return hashlib.sha256(read(path)).hexdigest()


def load_source(path, digest, name):
    raw = read(path)
    need(hashlib.sha256(raw).hexdigest() == digest, "SERVICE_TEST_SOURCE_PIN")
    need(name not in sys.modules, "SERVICE_TEST_MODULE_PRELOADED")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def refuses(call, label):
    check()
    try:
        call()
    except (ValueError, TypeError, KeyError, OSError) as error:
        return dict(case=label, error_type=type(error).__name__, error=str(error)[:250])
    raise AssertionError("SERVICE_TEST_UNEXPECTED_ACCEPTANCE:"+label)


def fixture_config(base, port=38194):
    return dict(index=dict(path=str(base/"index"), create=False,
        limits=dict(max_objects=1, max_postings=16, max_features=16,
                    max_snapshots=2, max_logical_bytes=MIB, max_db_pages=256)),
        host="127.0.0.1", port=port, tls=None, lease_seconds=1, cleanup_seconds=10,
        limits=dict(max_connections=1, max_requests=4, max_reply_bytes=MIB,
                    operation_ms=1000), share_all_custody=True, exclusive=True)


def fixture_plan(base, args=None):
    operation = dict(wall_seconds=35, cpu_seconds=20, memory_mib=512,
                     active_processes=3, stdout_bytes=MIB, stderr_bytes=MIB)
    epoch = dict(wall_seconds=50, cpu_seconds=80, memory_mib=640,
                 active_processes=4, stdout_bytes=MIB, stderr_bytes=MIB)
    return dict(schema="DMKN_ORDINARY_SERVICE_PLAN_V1",
        package=str(base/"package") if args is None else args.package,
        profile_sha256="1"*64 if args is None else args.profile_sha256,
        python_runtime=str(base/"python") if args is None else args.python_runtime,
        lean_runtime=str(base/"lean") if args is None else args.lean_runtime,
        catalog=str(base/"catalog"), custody=str(base/"custody"), store_id="a"*64,
        custody_limits=dict(path=str(base/"custody-limits.json"), sha256="2"*64),
        config=dict(path=str(base/"config.json"), sha256="3"*64),
        leases=2, horizon_seconds=160, runner_cpu_seconds=60,
        operation_limits=operation, epoch_limits=epoch,
        aggregate=dict(cpu_seconds=220, accepted_attempts=8, reply_bytes=2*MIB,
                       log_bytes=44*MIB))


def plan_controls(helper, base):
    config, plan = fixture_config(base), fixture_plan(base)
    reservation = helper.validate_plan(deepcopy(plan), deepcopy(config))
    refusals = []
    for key, value in (("leases", True), ("leases", 0), ("leases", 97),
                       ("horizon_seconds", 159), ("runner_cpu_seconds", 59),
                       ("profile_sha256", "g"*64), ("store_id", 7),
                       ("schema", "unknown")):
        changed = deepcopy(plan); changed[key] = value
        refusals.append(refuses(lambda: helper.validate_plan(changed, config), "plan:"+key+":"+str(value)))
    for key in plan:
        changed = deepcopy(plan); del changed[key]
        refusals.append(refuses(lambda: helper.validate_plan(changed, config), "missing:"+key))
    changed = deepcopy(plan); changed["command"] = ["arbitrary.exe"]
    refusals.append(refuses(lambda: helper.validate_plan(changed, config), "arbitrary-command"))
    for key in ("cpu_seconds", "accepted_attempts", "reply_bytes", "log_bytes"):
        changed = deepcopy(plan); changed["aggregate"][key] -= 1
        refusals.append(refuses(lambda: helper.validate_plan(changed, config), "aggregate:"+key))
        changed = deepcopy(plan); changed["aggregate"][key] = True
        refusals.append(refuses(lambda: helper.validate_plan(changed, config), "aggregate-bool:"+key))
    for key in ("wall_seconds", "cpu_seconds", "memory_mib", "active_processes"):
        changed = deepcopy(plan); changed["epoch_limits"][key] -= 1
        refusals.append(refuses(lambda: helper.validate_plan(changed, config), "nested-reserve:"+key))
    for key, value in (("port", 0), ("port", True), ("share_all_custody", False),
                       ("exclusive", 1), ("host", "0.0.0.0"),
                       ("host", "192.0.2.1"), ("lease_seconds", True)):
        changed = deepcopy(config); changed[key] = value
        refusals.append(refuses(lambda: helper.validate_service(changed), "service:"+key+":"+str(value)))
    changed = deepcopy(config); changed["index"]["create"] = True
    refusals.append(refuses(lambda: helper.validate_service(changed), "create-index"))
    changed = deepcopy(config); changed["index"]["unknown"] = None
    refusals.append(refuses(lambda: helper.validate_service(changed), "extra-index-field"))
    changed = deepcopy(config); changed["unknown"] = None
    refusals.append(refuses(lambda: helper.validate_service(changed), "extra-service-field"))
    for raw in (b'{"key":1,"key":2}', b'{"x":NaN}', b'{"x":1.25}', b'{', b'[] trailing'):
        refusals.append(refuses(lambda: helper.parse(raw), "strict-json:"+repr(raw)))
    return dict(group="strict_inputs_and_upfront_reservations", reservation=reservation,
                refusals=refusals, mathematical_acceptance=False)


def report_fixture(plan, config, base):
    def supervision(limits, cpu):
        return dict(schema="DMKN_V4_OWNER_COMMAND_REPORT_V1",
            status="COMMAND_EXITED_ZERO_AND_CLOSED", child_exit_code=0,
            direct_child_reaped=True, job_closed=True, termination_requested=False,
            cleanup_errors=[], limits=deepcopy(limits),
            final_job=dict(active_processes=0, terminated_processes=0, cpu_seconds=cpu),
            wall_seconds_through_cleanup=2.0, observed_logs=dict(stdout_bytes=100, stderr_bytes=0))
    expected = dict(plan=deepcopy(plan), config=deepcopy(config),
        diagnostics=str(base/"inner"), installation_manifest_sha256="4"*64,
        implementation_id="5"*64, semantic_id="6"*64)
    run = dict(schema="DMKN_ORDINARY_BOUNDED_OPERATION_V1", ok=True,
        status="CLI_EXITED_ZERO", tool="peer", child_exit_code=0,
        child_supervision_status="COMMAND_EXITED_ZERO_AND_CLOSED",
        profile_sha256=plan["profile_sha256"], installation_manifest_sha256="4"*64,
        diagnostics=expected["diagnostics"], limits=deepcopy(plan["operation_limits"]))
    provider = {key: 0 for key in ("requests", "request_bytes", "reply_bytes", "header_bytes",
        "reserved_reply_bytes", "active", "accepted_attempts", "handshakes", "handshake_failures",
        "accept_failures", "cleanup_pending", "cleanup_failures", "failures", "refused")}
    provider.update(accepting=False, admission_exhausted=False, mathematical_acceptance=False)
    ready = dict(status="READY", host=config["host"], port=config["port"], tls=False,
        lease_seconds=config["lease_seconds"], shared_custody=plan["custody"],
        index=config["index"]["path"], mathematical_acceptance=False)
    peer = dict(ok=True, operation="serve", profile_sha256=plan["profile_sha256"],
        store_id=plan["store_id"], catalog=plan["catalog"], custody=plan["custody"],
        config_sha256=plan["config"]["sha256"], implementation_id="5"*64, semantic_id="6"*64,
        result=dict(operation="serve", status="LEASE_FINISHED", quiescent=True,
                    cleanup_errors=[], mathematical_acceptance=False, ready=ready, provider=provider))
    return [supervision(plan["epoch_limits"], 2.0), run,
            supervision(plan["operation_limits"], 1.5), peer, expected]


def epoch_controls(helper, base):
    plan, config = fixture_plan(base), fixture_config(base)
    good = report_fixture(plan, config, base)
    row = helper.validate_epoch(*deepcopy(good))
    need(row["outer_job_cpu_seconds"] == 2.0 and row["inner_logs_bytes"] == 100 and
         row["outer_logs_bytes"] == 100, "SERVICE_TEST_NO_DOUBLE_CPU_ACCOUNTING")
    cases = []

    def mutation(label, index, keys, value, *, delete=False):
        changed = deepcopy(good)
        cursor = changed[index]
        for key in keys[:-1]:
            cursor = cursor[key]
        if delete:
            del cursor[keys[-1]]
        else:
            cursor[keys[-1]] = value
        cases.append(refuses(lambda: helper.validate_epoch(*changed), label))

    for index, label in ((0, "outer"), (2, "inner")):
        for key, value in (("termination_requested", True), ("job_closed", False),
                           ("direct_child_reaped", False), ("child_exit_code", True),
                           ("cleanup_errors", ["uncertain"]), ("status", "READY"),
                           ("schema", "WRONG_SCHEMA"), ("error", "contradictory")):
            mutation(label+":"+key, index, [key], value)
        mutation(label+":missing-schema", index, ["schema"], None, delete=True)
        for key in ("active_processes", "terminated_processes"):
            mutation(label+":"+key, index, ["final_job", key], 1)
        mutation(label+":missing-final-job", index, ["final_job"], None, delete=True)
        mutation(label+":cpu-over-cap", index, ["final_job", "cpu_seconds"], 1000)
        mutation(label+":log-over-cap", index, ["observed_logs", "stdout_bytes"], 9*MIB)
    for key, value in (("profile_sha256", "f"*64), ("diagnostics", "wrong"),
                       ("installation_manifest_sha256", "f"*64), ("ok", False),
                       ("report_error", "lost")):
        mutation("run:"+key, 1, [key], value)
    for key, value in (("profile_sha256", "f"*64), ("catalog", "wrong"), ("custody", "wrong"),
                       ("store_id", "f"*64), ("config_sha256", "f"*64),
                       ("implementation_id", "f"*64), ("semantic_id", "f"*64),
                       ("report_write_error", "lost"), ("close_errors", []), ("final_budget_error", {})):
        mutation("peer:"+key, 3, [key], value)
    for key, value in (("quiescent", False), ("status", "READY"), ("cleanup_errors", ["lost"])):
        mutation("result:"+key, 3, ["result", key], value)
    mutation("ready:port", 3, ["result", "ready", "port"], 0)
    mutation("ready:index", 3, ["result", "ready", "index"], "wrong")
    for key, value in (("accept_failures", 1), ("cleanup_failures", 1), ("active", 1),
                       ("reserved_reply_bytes", 1), ("requests", True),
                       ("accepted_attempts", 5), ("requests", 1), ("reply_bytes", MIB+1),
                       ("admission_exhausted", True), ("handshake_failures", 1)):
        mutation("provider:"+key, 3, ["result", "provider", key], value)
    for index, label in ((0, "outer"), (1, "run"), (2, "inner"), (3, "peer")):
        changed = deepcopy(good); changed[index] = None
        cases.append(refuses(lambda: helper.validate_epoch(*changed), "missing:"+label))

    tolerated = deepcopy(good)
    tolerated[3]["result"]["provider"].update(requests=4, accepted_attempts=4,
        failures=4, reply_bytes=MIB, admission_exhausted=True)
    tolerant_row = helper.validate_epoch(*tolerated)
    need(tolerant_row["accepted_attempts"] == 4 and tolerant_row["reply_bytes"] == MIB,
         "SERVICE_TEST_CLEAN_PREPAID_EXHAUSTION")
    return dict(group="clean_report_binding_and_prepaid_client_failure", synthetic=True,
        positive=row, clean_quota_exhaustion=tolerant_row, refusals=cases), row, tolerant_row


def sequence_controls(helper, base, row, exhausted):
    plan = fixture_plan(base)
    outcomes = []

    def scenario(label, *, returned=None, invoke_failure=False, input_failure_after=None,
                 wall_after=None, cpu_after=None, initial_wall=0, initial_cpu=0,
                 record_failure=False, input_wall=0, intent_wall=0):
        clock = SimpleNamespace(wall=initial_wall, cpu=initial_cpu)
        calls, records, input_calls = [], [], []

        def inputs():
            input_calls.append(len(input_calls))
            clock.wall += input_wall
            if input_failure_after is not None and len(input_calls) > input_failure_after:
                raise ValueError("SYNTHETIC_INPUT_CHANGED")

        def invoke(position):
            calls.append(position)
            if invoke_failure:
                raise ValueError("SYNTHETIC_MISSING_OR_UNCLEAN_REPORT")
            clock.wall += 2 if wall_after is None else wall_after
            clock.cpu += 0.25 if cpu_after is None else cpu_after
            return dict(epoch=position+1, **deepcopy(row if returned is None else returned))

        def record(kind, position, value):
            records.append((kind, position))
            if kind == "intent":
                clock.wall += intent_wall
            if record_failure and kind == "complete":
                raise OSError("SYNTHETIC_COMPLETE_RECORD_FAILED")

        result = helper._sequence(deepcopy(plan), invoke, record, inputs,
                                  lambda: clock.wall, lambda: clock.cpu, origins=(0, 0))
        outcomes.append(dict(case=label, calls=calls, records=records, result=result))
        return result, calls, records

    result, calls, records = scenario("two-clean")
    need(result["ok"] is True and result["finished"] == 2 and calls == [0, 1] and
         records == [("intent", 0), ("complete", 0), ("intent", 1), ("complete", 1)] and
         result["observed_outer_job_cpu_seconds"] == 4.0,
         "SERVICE_TEST_TWO_EPOCHS_ORDER_AND_CPU")
    result, calls, _ = scenario("two-prepaid-exhausted", returned=exhausted)
    need(result["ok"] is True and calls == [0, 1] and
         result["observed_accepted_attempts"] == plan["aggregate"]["accepted_attempts"] and
         result["observed_reply_bytes"] == plan["aggregate"]["reply_bytes"],
         "SERVICE_TEST_PREPAID_ONLY_NO_RENEWAL")
    for label, kwargs, expected_calls in (
        ("missing-unclean-first", dict(invoke_failure=True), [0]),
        ("inputs-changed-before-first", dict(input_failure_after=0), []),
        ("inputs-changed-between", dict(input_failure_after=1), [0]),
        ("horizon-insufficient-next", dict(wall_after=90), [0]),
        ("preflight-horizon-not-rebased", dict(initial_wall=90), []),
        ("preflight-cpu-not-rebased", dict(initial_cpu=60), []),
        ("input-validation-spent-horizon", dict(input_wall=90), []),
        ("durable-intent-spent-horizon", dict(intent_wall=90), []),
        ("runner-cpu-exhausted", dict(cpu_after=61), [0]),
        ("complete-record-uncertain", dict(record_failure=True), [0]),
        ("observed-aggregate-exceeded", dict(returned={**row, "accepted_attempts": 9}), [0]),
    ):
        result, calls, _ = scenario(label, **kwargs)
        need(result["ok"] is False and calls == expected_calls,
             "SERVICE_TEST_STOP_NO_RETRY:"+label)
    return dict(group="finite_sequence_original_allowance_no_retry", synthetic=True, outcomes=outcomes)


def path_controls(helper, base):
    base.mkdir()
    for leaf in ("package", "python", "lean", "catalog", "custody", "index", "companion"):
        (base/leaf).mkdir()
    plan, config = fixture_plan(base), fixture_config(base)
    plan_path, output = base/"plan.json", base/"fresh-output"
    save(base/"config.json", config)
    save(base/"custody-limits.json", dict(objects=1, exports=1, logical_bytes=MIB, db_pages=256))
    plan["config"]["sha256"] = sha(base/"config.json")
    plan["custody_limits"]["sha256"] = sha(base/"custody-limits.json")
    save(plan_path, plan)
    checked = helper.validate_paths(plan, config, plan_path, output, base/"companion")
    need(checked["output"] == output and not output.exists(), "SERVICE_TEST_PREFLIGHT_NO_WRITES")
    need(helper.pinned(plan["config"]) == read(base/"config.json"), "SERVICE_TEST_PIN_POSITIVE")
    bad_ref = dict(plan["config"], sha256="f"*64)
    cases = [refuses(lambda: helper.pinned(bad_ref), "stale-config-pin")]
    changed = deepcopy(config); changed["index"]["path"] = plan["catalog"]
    cases.append(refuses(lambda: helper.validate_paths(plan, changed, plan_path, output,
                                                      base/"companion"), "index-catalog-overlap"))
    cases.append(refuses(lambda: helper.validate_paths(plan, config, plan_path,
        base/"custody"/"new-output", base/"companion"), "output-custody-overlap"))
    cases.append(refuses(lambda: helper.validate_paths(plan, config, plan_path,
        base/"package"/"new-output", base/"companion"), "output-package-overlap"))
    save(base/"catalog"/"config.json", config)
    changed_plan = deepcopy(plan); changed_plan["config"]["path"] = str(base/"catalog"/"config.json")
    cases.append(refuses(lambda: helper.validate_paths(changed_plan, config, plan_path, output,
        base/"companion"), "config-inside-catalog"))
    cert, key = base/"catalog"/"cert.pem", base/"key.pem"
    save(cert, {"inert": "not-a-certificate"}); save(key, {"inert": "not-a-key"})
    changed = deepcopy(config); changed["tls"] = dict(cert_file=str(cert), cert_sha256=sha(cert),
                                                       key_file=str(key), key_sha256=sha(key))
    cases.append(refuses(lambda: helper.validate_paths(plan, changed, plan_path, output,
        base/"companion"), "nested-tls-inside-catalog"))
    offer = base/"custody"/"offers.json"; save(offer, {"inert": True})
    changed = deepcopy(config); changed["authoring_offers"] = dict(path=str(offer), sha256=sha(offer))
    cases.append(refuses(lambda: helper.validate_paths(plan, changed, plan_path, output,
        base/"companion"), "nested-offer-inside-custody"))
    for path in (Path("relative.json"), Path(base.anchor)):
        cases.append(refuses(lambda: helper.ordinary(path), "nonordinary:"+str(path)))
    original, linked = base/"hardlink-original.json", base/"hardlink.json"
    save(original, {"inert": True}); os.link(original, linked)
    cases.append(refuses(lambda: helper.ordinary(linked), "hardlink-file"))
    output.mkdir()
    cases.append(refuses(lambda: helper.validate_paths(plan, config, plan_path, output,
        base/"companion"), "existing-output-no-resume"))
    good = b'{"ok":true,"counter":2}'
    need(helper.report_agreement(good, b'{ "counter":2, "ok":true }\n') ==
         {"ok": True, "counter": 2}, "SERVICE_TEST_EQUIVALENT_REPORT_JSON")
    cases.append(refuses(lambda: helper.report_agreement(good, b'{"ok":false,"counter":2}'),
                         "stdout-result-disagreement"))
    cases.append(refuses(lambda: helper.report_agreement(good, b'{"ok":true,"ok":true,"counter":2}'),
                         "duplicate-report-field"))
    return dict(group="ordinary_paths_freshness_pins_and_report_agreement", refusals=cases,
                preflight_created_output=False, synthetic=True)


def load_package(args):
    package = Path(args.package)
    raw = read(package/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256, "SERVICE_TEST_PROFILE_PIN")
    pin = json.loads(raw)["files"]["profile.py"]
    loader = load_source(package/"profile.py", pin["sha256"], "_service_test_profile")
    return loader.load(package, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)


def empty_state(args, base, helper):
    """Ordinary constructors only; no roots/evidence/publications are invented."""
    loaded = load_package(args)
    A, O, api = loaded.A, loaded.O, loaded.peer_api
    custody_limits = dict(objects=1, exports=1, logical_bytes=MIB, db_pages=256)
    custody = owner = index = None
    try:
        custody = O.OrdinaryStore(base/"custody", loaded.installation.semantic_id,
                                 custody_limits, create=True)
        owner = A.OrdinaryAdmission.open(loaded.installation, base/"catalog", "a"*64,
                                        custody, create=True, limits=A.P.Limits())
        config = fixture_config(base, args.port)
        index = api.DS.Store(base/"index", api.OrdinaryExportAdapter(loaded.installation.semantic_id),
                             config["index"]["limits"], create=True)
        # Evidence is the genuine empty stores. Direct SELECT inspects them; no
        # state table is edited and no saved report is granted event authority.
        need(owner.catalog._db.execute("SELECT COUNT(*) FROM roots").fetchone() == (0,),
             "SERVICE_TEST_NO_ACCEPTED_ROOT")
        need(custody.db.execute("SELECT COUNT(*) FROM objects").fetchone() == (0,),
             "SERVICE_TEST_NO_CUSTODY_OBJECT")
        need(index.db.execute("SELECT COUNT(*) FROM objects").fetchone() == (0,),
             "SERVICE_TEST_NO_INDEX_OBJECT")
        identity = dict(implementation_id=loaded.installation.implementation_id,
                        semantic_id=loaded.installation.semantic_id,
                        installation_manifest_sha256=hashlib.sha256(loaded.installation.manifest_raw).hexdigest())
        need(helper.selected_identities(loaded.installation.doc) ==
             {key: identity[key] for key in ("implementation_id", "semantic_id")},
             "SERVICE_TEST_IDENTITY_ENCODING_CORRESPONDENCE")
    finally:
        for resource in (index, owner, custody):
            if resource is not None:
                resource.close()
    save(base/"custody-limits.json", custody_limits)
    save(base/"config.json", config)
    plan = fixture_plan(base, args)
    plan["custody_limits"]["sha256"] = sha(base/"custody-limits.json")
    plan["config"]["sha256"] = sha(base/"config.json")
    return plan, config, identity


def public_controls(helper, args, base):
    base.mkdir()
    plan, config, identity = empty_state(args, base, helper)
    helper.validate_plan(plan, config)
    plan_path, service_output = base/"plan.json", base/"service-plan"
    save(plan_path, plan)
    command = [sys.executable, "-I", "-S", "-B", args.source,
               "--plan", str(plan_path), "--plan-sha256", sha(plan_path),
               "--output", str(service_output)]
    save(base/"COMMAND.json", dict(argv=command, cwd=str(ROOT),
        scope="TWO_PREPAID_LEASES_THEN_EXISTING_OUTPUT_REFUSAL", native_calls=0,
        mathematical_acceptance=False))

    def invoke(label):
        check()
        with (base/(label+".stdout")).open("xb") as stdout, \
                (base/(label+".stderr")).open("xb") as stderr:
            child = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
            try:
                code = child.wait(timeout=max(1, min(180, DEADLINE-time.monotonic()-10)))
            except BaseException:
                if child.poll() is None:
                    child.kill(); child.wait(timeout=8)
                raise
        report = helper.parse(read(base/(label+".stdout")), reports=True)
        return code, report

    code, report = invoke("actual")
    need(code == 0 and report.get("ok") is True and report.get("finished") == 2 and
         report.get("status") == "FINITE_PLAN_FINISHED" and report.get("mathematical_acceptance") is False,
         "SERVICE_TEST_ACTUAL_TWO_LEASES")
    saved = helper.report_agreement(read(service_output/"RESULT.json"), read(base/"actual.stdout"))
    need(saved["profile_sha256"] == args.profile_sha256 and saved["plan_sha256"] == sha(plan_path) and
         saved["installation_manifest_sha256"] == identity["installation_manifest_sha256"],
         "SERVICE_TEST_ACTUAL_PLAN_BINDINGS")
    expected_epochs = [service_output/"epoch-0001", service_output/"epoch-0002"]
    need(sorted(path.name for path in service_output.glob("epoch-*")) ==
         [path.name for path in expected_epochs], "SERVICE_TEST_NO_EXTRA_EPOCH")
    audited = []
    for epoch in expected_epochs:
        outer = helper.parse(read(epoch/"OUTER.json"), reports=True)
        run = helper.parse(read(epoch/"inner"/"RUN.json"), reports=True)
        inner = helper.parse(read(epoch/"inner"/"SUPERVISION.json"), reports=True)
        peer = helper.parse(read(epoch/"service"/"RESULT.json"), reports=True)
        accounting = helper.validate_epoch(outer, run, inner, peer, dict(plan=plan, config=config,
            diagnostics=str(epoch/"inner"), **identity))
        need(peer["implementation_id"] == identity["implementation_id"] and
             peer["semantic_id"] == identity["semantic_id"] and peer["cost"]["worker_cpu_seconds"] == 0 and
             accounting["accepted_attempts"] == 0 and accounting["reply_bytes"] == 0,
             "SERVICE_TEST_EMPTY_INERT_NO_NATIVE_OR_CLIENTS")
        helper.report_agreement(read(epoch/"outer"/"stdout.txt"), read(epoch/"inner"/"RUN.json"))
        helper.report_agreement(read(epoch/"inner"/"child"/"stdout.txt"), read(epoch/"service"/"RESULT.json"))
        audited.append(dict(epoch=epoch.name, accounting=accounting))
    need(saved["observed_outer_job_cpu_seconds"] == sum(item["accounting"]["outer_job_cpu_seconds"]
        for item in audited), "SERVICE_TEST_ACTUAL_CPU_ONCE")
    before = sha(service_output/"RESULT.json")
    code, refusal = invoke("resume-refusal")
    need(code == 1 and refusal.get("ok") is False and refusal.get("finished") == 0 and
         refusal.get("status") == "NO_EPOCH_LAUNCHED" and "FRESH_PATH" in refusal.get("error", "") and
         sha(service_output/"RESULT.json") == before and
         sorted(path.name for path in service_output.glob("epoch-*")) == [path.name for path in expected_epochs],
         "SERVICE_TEST_PUBLIC_NO_RESUME_OR_OVERWRITE")
    with sqlite3.connect((base/"catalog"/"catalog.sqlite").as_uri()+"?mode=ro", uri=True) as db:
        need(db.execute("SELECT COUNT(*) FROM roots").fetchone() == (0,), "SERVICE_TEST_FINAL_NO_ACCEPTANCE")
        need(db.execute("SELECT COUNT(*) FROM operations").fetchone() == (0,), "SERVICE_TEST_FINAL_NO_NATIVE_OPERATIONS")
    return dict(group="real_public_two_lease_empty_inert_service", helper_report=saved,
                epoch_audits=audited, resume_refusal=refusal, mathematical_acceptance=False)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and Path.cwd() == ROOT,
         "SERVICE_TEST_PROFILE")
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("source", "source-sha256", "package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(output.is_absolute() and output.parent.is_dir() and not output.exists(), "SERVICE_TEST_FRESH_OUTPUT")
    need(1 <= args.port <= 65535, "SERVICE_TEST_FIXED_NONZERO_PORT")
    output.mkdir()
    report = dict(status="RUNNING", groups=[], mathematical_acceptance=False,
                  scope="FINITE_LOCAL_ORCHESTRATION_NOT_MATH_GROWTH_OR_INDEPENDENT_HOSTING")
    try:
        helper = load_source(Path(args.source), args.source_sha256, "_service_plan_test_subject")
        report["groups"].append(plan_controls(helper, output/"synthetic"))
        group, row, exhausted = epoch_controls(helper, output/"synthetic")
        report["groups"].append(group)
        report["groups"].append(sequence_controls(helper, output/"synthetic", row, exhausted))
        report["groups"].append(path_controls(helper, output/"paths"))
        report["groups"].append(public_controls(helper, args, output/"public"))
        check(); report["status"] = "PASS"
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:1500])
    report.update(wall_seconds=time.monotonic()-START_WALL,
                  controller_cpu_seconds=time.process_time()-START_CPU)
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
