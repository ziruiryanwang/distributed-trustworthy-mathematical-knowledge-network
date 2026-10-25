"""Native-free changed-boundary controls; execution requires root selection.

Compile the exact receive orchestration and unchanged OrdinaryBudget class from
their selected source ASTs. Owner/native, record decoding and transport are
explicit doubles; no network, protected store, Lean or package installation is
opened. These controls establish orchestration, not mathematical verification or
wire-codec correctness. Emit results to stdout for the selected outer runner.
"""
from __future__ import annotations

import ast
import asyncio
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import time
from types import SimpleNamespace as NS
from unittest.mock import patch


ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = Path(__file__).resolve().parent
ACQUISITION = ROOT / "software/v5/ordinary_authoring_offers/ordinary_acquisition.py"
ACQUISITION_SHA = "d4599471b1285650876d53763c4a618a4dd5d7a953197954249052771a9df64f"
MIB = 1024**2
SELECTED_UID, ANCESTOR_UID = "1"*64, "2"*64
SELECTED_EXPORT, PREMISE_EXPORT = "3"*64, "4"*64
PARENT, SEMANTIC, SNAPSHOT = "5"*64, "6"*64, "7"*64
NAME, PREMISE_NAME = ["selected"], ["premise"]
SELECTED_RAW, ANCESTOR_RAW = b"selected-unit", b"ancestor-unit"


def need(ok, code):
    if not ok:
        raise ValueError(code)


def uint(value, lower, upper, code="CONTROL_UINT"):
    need(type(value) is int and lower <= value <= upper, code)
    return value


def hexid(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "CONTROL_HEX")
    return value


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def selected_ast(path, names, namespace, expected=None):
    raw = path.read_bytes()
    need(0 < len(raw) <= 2*MIB, "CONTROL_SOURCE_BOUND")
    digest = hashlib.sha256(raw).hexdigest()
    need(expected is None or digest == expected, "CONTROL_DONOR_PIN")
    tree = ast.parse(raw, str(path))
    chosen = [node for node in tree.body if isinstance(node,
        (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in names]
    need({node.name for node in chosen} == set(names), "CONTROL_EXACT_DEFINITIONS")
    exec(compile(ast.Module(body=chosen, type_ignores=[]), str(path), "exec"), namespace)
    return digest


class Scenario:
    def __init__(self, api, budget_type, *, policy="selected-unit-only", ready=False):
        self.api, self.budget_type = api, budget_type
        self.calls, self.effects, self.accounts = [], [], []
        self.ready, self.ready_after_dependency = ready, True
        self.cleanup_fail = self.final_fail = self.expire_preflight = False
        self.admit_fail = self.context_fail = False
        self.accounted = False
        self.admission_status = "CHECKED"
        self.preflights, self.admits = 0, 0
        self.allowance = NS(deadline=time.monotonic()+40, check=self.check,
                            operation=self.operation, account=self.account)
        self.loaded = NS(installation=NS(semantic_id=SEMANTIC))
        self.owner = NS(catalog=NS(context=self.context), preflight=self.preflight,
                        admit=self.admit)
        self.custody = object()
        self.config = {"dependency_policy": policy, "parent_root": PARENT,
            "contacts": {"provider": {}},
            "selection": {"provider": "provider", "snapshot_id": SNAPSHOT,
                "record": {"schema": "ORDINARY", "object_id": SELECTED_EXPORT,
                    "object_bytes": 16, "locator": {"unit_id": SELECTED_UID,
                                                         "export_name": NAME}}},
            "limits": {"requests": 8, "reply_bytes": 4096, "units": 4,
                "unit_bytes": 128, "total_bytes": 512, "missing": 4,
                "preflights": 4, "locator_bytes": 128}}

    def check(self):
        need(time.monotonic() < self.allowance.deadline, "CONTROL_ALLOWANCE_EXPIRED")
        need(not (self.accounted and self.final_fail), "CONTROL_FINAL_ALLOWANCE")

    def account(self, amount):
        self.accounts.append(amount)
        self.accounted = True
        need(not self.cleanup_fail, "CONTROL_ACCOUNT_FAILURE")

    def operation(self, _):
        self.effects.append("operation")
        result = NS(deadline=self.allowance.deadline-1, worker_cpu=2.5)
        result.check = lambda: need(time.monotonic() < result.deadline,
                                    "CONTROL_OPERATION_EXPIRED")
        self.operation_value = result
        return result

    def context(self, parent):
        self.effects.append("context")
        need(parent == PARENT and not self.context_fail, "CONTROL_PARENT")

    def preflight(self, parent, units, *, limits, budget):
        self.preflights += 1
        need(parent == PARENT and units[0] == SELECTED_RAW, "CONTROL_PREFLIGHT_INPUT")
        need(budget is self.operation_value and limits.max_units == 4,
             "CONTROL_PREFLIGHT_ORIGINAL_GRANT")
        if self.expire_preflight:
            budget.deadline = time.monotonic()-1
        ready = self.ready or (self.ready_after_dependency and ANCESTOR_RAW in units)
        return NS(status="READY" if ready else "NEEDS",
                  missing=() if ready else ((compact(PREMISE_NAME), PREMISE_EXPORT),))

    def admit(self, parent, plan, budget):
        self.admits += 1
        need(parent == PARENT and plan.status == "READY" and budget is self.operation_value,
             "CONTROL_ADMIT_PRECONDITION")
        need(not self.admit_fail, "CONTROL_ADMIT_FAILURE")
        return {"status": self.admission_status, "local_root": "8"*64}

    def begin(self, loaded, config, allowance, operation):
        allowance.check()
        need(loaded is self.loaded and operation == "receive", "CONTROL_BEGIN")
        return deepcopy(config), {"operation": operation, "status": "STARTED",
            "mathematical_acceptance": False, "cleanup_errors": []}

    def state(self, *_):
        self.effects.append("state")

    def contacts(self, config, check):
        self.effects.append("contacts")
        check()
        return config, []

    def client_type(self):
        scenario = self
        class Client:
            def __init__(self, adapter, endpoints, ledger, *, local_custody):
                need(local_custody is scenario.custody, "CONTROL_CUSTODY")
                self.ledger = ledger

            async def fetch(self, kind, raw, maximum):
                ticket = self.ledger.begin(maximum)
                scenario.calls.append(kind)
                self.ledger.settle(ticket, len(raw))
                return {"raw": raw}

            async def preview(self, provider, record):
                need(provider == "provider", "CONTROL_PROVIDER")
                return await self.fetch("preview", b"preview", 16)

            async def evidence(self, provider, semantic, uid, maximum, **kwargs):
                need(provider == "provider" and semantic == SEMANTIC, "CONTROL_EVIDENCE_BINDING")
                if uid == SELECTED_UID:
                    need(kwargs == {"expected_export_id": SELECTED_EXPORT,
                         "expected_export_name": NAME}, "CONTROL_SELECTED_BINDING")
                    return await self.fetch("selected-evidence", SELECTED_RAW, maximum)
                need(uid == ANCESTOR_UID and kwargs == {"expected_export_id": PREMISE_EXPORT,
                     "expected_export_name": PREMISE_NAME}, "CONTROL_ANCESTOR_BINDING")
                return await self.fetch("ancestor-evidence", ANCESTOR_RAW, maximum)

            async def locator(self, provider, semantic, identity, maximum, **kwargs):
                need(identity == PREMISE_EXPORT and kwargs == {"expected_name": PREMISE_NAME},
                     "CONTROL_LOCATOR_BINDING")
                await self.fetch("ancestor-locator", b"locator", maximum)
                return {"locator": {"unit_id": ANCESTOR_UID}}

            def report(self):
                return {"calls": list(scenario.calls)}
        return Client

    async def run(self, *, network=None, close_failure=False):
        self.api.update(_begin=self.begin, _state=self.state, _contacts=self.contacts)
        self.api["O"].OrdinaryAcquisition = self.client_type()
        before = deepcopy(self.config)
        original_close = self.budget_type.close
        def bad_close(ledger):
            original_close(ledger)
            raise ValueError("CONTROL_LEDGER_CLOSE_FAILURE")
        with patch.object(self.budget_type, "close", bad_close if close_failure else original_close):
            try:
                report = await self.api["receive"](self.loaded, self.owner, self.custody,
                    self.config, self.allowance, network_budget=network)
                failed = False
            except self.api["PeerFailure"] as error:
                report, failed = error.report, True
        need(self.config == before, "CONTROL_CONFIG_UNCHANGED")
        need(json.loads(compact(report)) == report, "CONTROL_REPORT_SERIALIZABLE")
        return report, failed


def main():
    F = NS(need=need, uint=uint, hexid=hexid,
        validate_record=lambda record, _: record, ORDINARY_EXPORT_RECORD_SCHEMA="ORDINARY")
    namespace = {"F": F, "math": math, "time": time, "deepcopy": deepcopy,
                 "EVIDENCE_MAX": 16*MIB}
    selected_ast(ACQUISITION, {"OrdinaryBudget"}, namespace, ACQUISITION_SHA)
    Budget = namespace["OrdinaryBudget"]
    O = NS(OrdinaryBudget=Budget)
    api = {"asyncio": asyncio, "deepcopy": deepcopy, "re": re, "F": F, "O": O,
        "A": NS(need=need, E=NS(strict_json=json.loads), PreflightLimits=lambda **kw: NS(**kw)),
        "PP": NS(resolve=lambda preview, unit: need(preview == b"preview" and unit == SELECTED_RAW,
                                                    "CONTROL_PREVIEW_SELECTED_BINDING")),
        "OrdinaryExportAdapter": lambda _: NS(namespace="namespace"),
        "_repin": lambda pins, check: check(),
        "RECEIVE_LIMITS": {"requests": (1, 8192), "reply_bytes": (1, 1024*MIB),
            "units": (1, 1024), "unit_bytes": (1, 16*MIB), "total_bytes": (1, 64*MIB),
            "missing": (1, 4096), "preflights": (1, 1025), "locator_bytes": (1, MIB)}}
    api_sha = selected_ast(HERE/"peer_api.py", {"PeerFailure", "_error", "_fields",
        "_limits", "_network", "_failure", "receive"}, api)
    cases = []
    async def one(label, scenario, *, fail=False, status=None, calls=(), **kwargs):
        report, failed = await scenario.run(**kwargs)
        need(failed == fail and (status is None or report["status"] == status),
             "CONTROL_TERMINAL:"+label+":"+str(report))
        need(scenario.calls == list(calls), "CONTROL_CALLS:"+label)
        if report.get("network"):
            need(report["network"]["pending_requests"] == 0, "CONTROL_SETTLED:"+label)
        cases.append({"case": label, "status": "PASS", "reported_status": report["status"],
                      "error": report.get("error"), "calls": list(scenario.calls)})
        return report

    async def exercise():
        for label, policy in (("invalid-policy", "automatic"), ("nonstring-policy", True),
                              ("null-policy", None), ("missing-policy", "missing")):
            s = Scenario(api, Budget, policy=policy)
            if policy == "missing":
                del s.config["dependency_policy"]
            r = await one(label, s, fail=True, status="FAILED")
            need(not s.effects and not s.accounts and s.admits == 0,
                 "CONTROL_POLICY_BEFORE_IO:"+label)
            need(r["error"]["code"] == ("PEER_RECEIVE_FIELDS" if policy == "missing" else
                 "PEER_RECEIVE_DEPENDENCY_POLICY"), "CONTROL_POLICY_CODE")
        s = Scenario(api, Budget)
        r = await one("strict-missing-no-recursion", s, status="NEED_GROUNDED_PREMISES",
                      calls=("preview", "selected-evidence"))
        need(s.preflights == 1 and s.admits == 0 and s.accounts == [2.5] and
             r["admission"] is None and r["mathematical_acceptance"] is False and
             r["local_acceptance_available"] is False and r["network"]["closed"] and
             r["grounded_premises_needed"] == [{"name": PREMISE_NAME, "export_id": PREMISE_EXPORT}]
             and r["dependency_policy"] == "selected-unit-only" and r["target"] ==
             {"name": NAME, "unit_id": SELECTED_UID, "export_id": SELECTED_EXPORT},
             "CONTROL_STRICT_NONACCEPTANCE")
        for status in ("CHECKED", "REUSED"):
            s = Scenario(api, Budget, ready=True); s.admission_status = status
            r = await one("strict-ready-"+status, s,
                status="CHECKED" if status == "CHECKED" else "REUSED_LOCAL_ACCEPTANCE",
                calls=("preview", "selected-evidence"))
            need(s.admits == 1 and r["admission"]["status"] == status and
                 r["mathematical_acceptance"] == (status == "CHECKED") and
                 r["local_acceptance_available"] is True, "CONTROL_READY_ADMISSION")
        s = Scenario(api, Budget, policy="bounded-closure")
        await one("explicit-closure", s, status="CHECKED", calls=("preview", "selected-evidence",
                  "ancestor-locator", "ancestor-evidence"))
        need(s.preflights == 2 and s.admits == 1, "CONTROL_EXPLICIT_CLOSURE")
        for label, fault in (("account-failure", "cleanup_fail"), ("final-allowance", "final_fail"),
                              ("preflight-expired", "expire_preflight")):
            s = Scenario(api, Budget); setattr(s, fault, True)
            r = await one(label, s, fail=True, status="FAILED", calls=("preview", "selected-evidence"))
            need(s.admits == 0 and s.accounts == [2.5] and r["mathematical_acceptance"] is False,
                 "CONTROL_STRICT_FINAL_CHECKS")
        s = Scenario(api, Budget)
        r = await one("ledger-close-failure", s, fail=True, status="FAILED",
                      calls=("preview", "selected-evidence"), close_failure=True)
        need(r["cleanup_errors"] and s.admits == 0, "CONTROL_CLOSE_NOT_BYPASSED")
        s = Scenario(api, Budget, ready=True); s.final_fail = True
        r = await one("postadmission-failure-retains-effect", s, fail=True, status="FAILED",
                      calls=("preview", "selected-evidence"))
        need(r["admission"]["status"] == "CHECKED" and r["mathematical_acceptance"] is True,
             "CONTROL_PARTIAL_ACCEPTANCE_PRESERVED")
        s = Scenario(api, Budget); s.context_fail = True
        await one("wrong-parent-before-transport", s, fail=True, status="FAILED")
        s = Scenario(api, Budget)
        ledger = Budget(deadline=time.monotonic()+35, requests=8, reply_bytes=4096)
        ledger.charge_external("prior-search", 1, 100)
        original_deadline = ledger.deadline
        r = await one("strict-shared-original-grant", s, status="NEED_GROUNDED_PREMISES",
                      calls=("preview", "selected-evidence"), network=ledger)
        need(ledger.requests == 3 and ledger.reply_bytes == 100+7+len(SELECTED_RAW) and
             ledger.deadline <= original_deadline and not ledger.closed, "CONTROL_NO_RENEWAL")
        ledger.close()
        for label, spent_requests, spent_bytes in (("spent-requests", 8, 0),
                                                    ("spent-bytes", 0, 4096)):
            s = Scenario(api, Budget)
            ledger = Budget(deadline=time.monotonic()+35, requests=8, reply_bytes=4096)
            ledger.charge_external("prior-search", spent_requests, spent_bytes)
            r = await one(label, s, fail=True, status="FAILED", network=ledger)
            need(r["error"]["code"] == "ORDINARY_AGGREGATE_BUDGET" and s.admits == 0 and
                 not ledger.closed, "CONTROL_ORIGINAL_BUDGET_EXHAUSTED")
            ledger.close()
        s = Scenario(api, Budget)
        ledger = Budget(deadline=time.monotonic()+35, requests=8, reply_bytes=4096)
        ledger.deadline = time.monotonic()-1
        await one("expired-original-network", s, fail=True, status="FAILED", network=ledger)
        need(s.admits == 0 and not ledger.closed, "CONTROL_EXPIRED_NOT_RENEWED")
        ledger.close()
        s = Scenario(api, Budget, policy="bounded-closure")
        s.config["limits"]["preflights"] = 1
        r = await one("closure-original-preflight-cap", s, fail=True, status="FAILED",
            calls=("preview", "selected-evidence", "ancestor-locator", "ancestor-evidence"))
        need(r["error"]["code"] == "PEER_PREFLIGHT_CAP" and s.admits == 0,
             "CONTROL_PREFLIGHT_CAP_NOT_RENEWED")
    asyncio.run(exercise())
    print(json.dumps({"status": "PASS", "scope": "EXACT_RECEIVE_ORCHESTRATION_WITH_DOUBLED_OWNER_AND_IO",
        "peer_api_sha256": api_sha, "budget_source_sha256": ACQUISITION_SHA,
        "cases": cases}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
