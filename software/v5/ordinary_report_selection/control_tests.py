"""Changed-boundary inert controls; root selects execution after source review.

Retained report bytes are fixtures, never mathematical warrants. No product
module, protected database, Lean worker, service or old test campaign is run.
"""
from __future__ import annotations

import argparse
import ast
from contextlib import ExitStack, contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
from types import ModuleType
from unittest.mock import patch


PREFIX = "software/v5/ordinary_report_selection/"
CHECKS = "experiments/v5-local-checks/"
CURRENT = "21bcb169cced5d85c3d2272265ef1f24f6848fbe2da0d2ab3f3acfe27697bba7"
POLICY = "prior-profile-extract-only-v1"
SOURCE_PINS = {
    "prepare.py": "203f6249e0659d13b58c79232b8e7a9533d0fc44d843c55a9eba03f244bb0892",
    "prepare_selected.py": "c86960216bc537bd61aa43940a62b7496bcdb2ecfd430ba28e5ed1abd35c65c2",
    "compatibility.json": "fa9fa6371e855f6ae711a866cdc31ed906ceb725274d776716d2416767fe3846",
}
FIXTURES = {
    "intake": (CHECKS + "refinement-recipient-part-b01/public-launch/child/stdout.txt", 2983,
               "e06a0ab9f171868f2d9187ba5757a3d6a7408f2d54c5b79fa52981d0e01f713e"),
    "receive": (CHECKS + "refinement-recipient-receive-b01/peer/RESULT.json", 8036,
                "99cf799a2f0e5f22be49432b46df475afe577fbf8cf512189c7bc36a7ccee6b7"),
    "find": (CHECKS + "finite-map-discovery-find02/peer/RESULT.json", 59945,
             "69ed25ff27c46d6d56a70a821d5b1589151b318da8eb11374b4973a0600b2830"),
    "preview": (CHECKS + "finite-map-discovery-preview02-01/peer/RESULT.json", 10748,
                "0e51b73aa4953a74bff6f68b787985d21bca4883f73f80fb65b90eb8e243ae20"),
    "query": (CHECKS + "received-query01/query/query/RESULT.json", 1642,
              "a578a6bff109b1db4a0d8ba60c17c414cd467b6449c8c27c393cfd1337d9e05c"),
    "source": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/Body.lean", 1077,
               "af055f8fb031383770e952fdd155bc1ef0280214d60f2724109695c62900aec0"),
    "project": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/project-authoring.json", 440,
                "578bb7bcb00531cd9e1da1811db6f1f011b23d1403c32d21a10d387e70ca2865"),
    "names": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/output-names.json", 233,
              "9287a8c97fc6a8d425d5682208991b72fcafdae60e1068b8dde6918a67018061"),
}
CUSTODY = dict(objects=4096, exports=8192, logical_bytes=134217728, db_pages=65536)
CONTACT = dict(host="127.0.0.1", port=38191, tls=False,
               server_name=None, ca_file=None, ca_sha256=None)


def need(ok, code):
    if not ok:
        raise AssertionError("SELECTION_CONTROL_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def write(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def load(path, raw, label):
    allowed = {"__future__", "argparse", "hashlib", "ipaddress", "json", "math",
               "os", "pathlib", "re", "stat", "importlib.util", "sys", "time"}
    for node in ast.walk(ast.parse(raw, filename=str(path))):
        if isinstance(node, ast.Import):
            need(all(alias.name in allowed for alias in node.names), "PRODUCT_IMPORT")
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0 and node.module in allowed, "PRODUCT_IMPORT")
    module = ModuleType(label)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def refuses(call, expected):
    try:
        call()
    except ValueError as error:
        need(str(error) == expected, "WRONG_REFUSAL:" + str(error))
    else:
        raise AssertionError("SELECTION_CONTROL_EXPECTED_REFUSAL:" + expected)


@contextmanager
def inert_boundary(allowed_reads, workspace):
    original_open = Path.open
    opened = []

    def checked_open(path, mode="r", *args, **kwargs):
        path = path.absolute()
        writing = any(flag in mode for flag in "wax+")
        if writing:
            need(path.is_relative_to(workspace) and "x" in mode and
                 not any(flag in mode for flag in "wa+"), "UNSELECTED_WRITE")
        else:
            need(path in allowed_reads or path.is_relative_to(workspace), "UNSELECTED_READ:" + str(path))
        opened.append((str(path), mode))
        return original_open(path, mode, *args, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError("SELECTION_CONTROL_FORBIDDEN_PROCESS_NETWORK_OR_DB")

    with ExitStack() as stack:
        stack.enter_context(patch.object(Path, "open", checked_open))
        for obj, attr in ((subprocess, "Popen"), (subprocess, "call"),
                          (os, "system"), (socket, "socket"),
                          (socket, "create_connection"), (sqlite3, "connect")):
            stack.enter_context(patch.object(obj, attr, forbidden))
        yield opened


class Controls:
    def __init__(self, root, output, raws, sources):
        self.root, self.output, self.raws = root, output, raws
        self.kit = load(root / PREFIX / "prepare.py", sources["prepare.py"], "_selection_test_kit")
        adapter = load(root / PREFIX / "prepare_selected.py", sources["prepare_selected.py"], "_selection_test_adapter")
        need(adapter.HELPER_SHA == SOURCE_PINS["prepare.py"] and
             adapter.MAP_SHA == SOURCE_PINS["compatibility.json"], "ADAPTER_SOURCE_PINS")
        self.kit.PROFILE = CURRENT
        self.counter, self.positives, self.negatives = 0, 0, 0
        self.groups = []

    def doc(self, label):
        return json.loads(self.raws[label])

    def ref(self, label):
        relative, _, sha = FIXTURES[label]
        return dict(path=str(self.root / relative), sha256=sha)

    def variant(self, document):
        self.counter += 1
        path = self.output / ("negative-%03d.json" % self.counter)
        raw = canonical(document)
        write(path, raw)
        return dict(path=str(path), sha256=digest(raw))

    def state(self):
        return {key: self.doc("receive")[key] for key in ("catalog", "custody", "store_id")}

    def base(self, action):
        self.counter += 1
        return dict(action=action, state=self.state(), custody_limits=deepcopy(CUSTODY),
                    operation_output=str(self.output / ("operation-%03d" % self.counter)))

    def contribute(self):
        request = self.base("contribute")
        request.update(parent_report=self.ref("receive"), source=self.ref("source"),
                       approve_local_source=True, acquired=[dict(report=self.ref("receive"), target_indices=[0])],
                       output_names=self.doc("names"), project_authoring=self.ref("project"),
                       approve_local_project=True, authoring_frontier_report=self.ref("intake"))
        return request

    def run(self, request, error=None):
        self.counter += 1
        request_path = self.output / ("request-%03d.json" % self.counter)
        prepared = self.output / ("prepared-%03d" % self.counter)
        write(request_path, canonical(request))
        call = lambda: self.kit.prepare(request_path, prepared)
        if error:
            refuses(call, error)
            need(not prepared.exists(), "REFUSAL_WROTE_OUTPUT")
            self.negatives += 1
            return
        receipt = call()
        need(json.loads((prepared / "RECEIPT.json").read_bytes()) == receipt and
             receipt["commands_executed"] == 0 and receipt["protected_state_opened"] is False and
             receipt["mathematical_acceptance"] is False, "INERT_RECEIPT")
        need(set(path.name for path in prepared.iterdir()) == set(receipt["files"]) | {"RECEIPT.json"}, "CENSUS")
        for filename, pin in receipt["files"].items():
            raw = (prepared / filename).read_bytes()
            need(pin == dict(bytes=len(raw), sha256=digest(raw)), "OUTPUT_PIN")
        for pin in receipt["inputs"]:
            raw = Path(pin["path"]).read_bytes()
            need(pin == dict(path=pin["path"], bytes=len(raw), sha256=digest(raw)), "INPUT_PIN")
        need(not Path(request["operation_output"]).exists(), "OPERATION_OUTPUT_CREATED")
        self.positives += 1
        return prepared, json.loads((prepared / "arguments.json").read_bytes())

    def group(self, label):
        self.groups.append(dict(name=label, status="PASS"))

    def execute(self):
        old = self.doc("receive")
        need(old["profile_sha256"] != CURRENT and self.doc("intake")["profile_sha256"] != CURRENT,
             "AUTHENTIC_FOREIGN_PROFILES")
        self.run(self.contribute(), "KIT_PARENT_SUCCESS")
        request = self.contribute()
        request["selection_report_policy"] = POLICY
        prepared, arguments = self.run(request)
        args = arguments["arguments"]
        def arg(key):
            need(args.count(key) == 1, "ARGUMENT_OCCURRENCE:" + key)
            return args[args.index(key)+1]
        parent = old["result"]["admission"]["local_root"]
        frontier = self.doc("intake")["result"]["local_root"]
        need(arg("--parent-root") == parent and arg("--authoring-frontier-root") == frontier and
             arg("--project-authoring-sha256") == FIXTURES["project"][2] and
             arguments["profile_sha256"] == CURRENT and arguments["mathematical_acceptance"] is False,
             "EXACT_CURRENT_ARGUMENTS")
        need((prepared / "Body.lean").read_bytes() == self.raws["source"] and
             (prepared / "project-authoring.json").read_bytes() == self.raws["project"] and
             json.loads((prepared / "acquired-targets.json").read_bytes()) == [old["result"]["target"]] and
             json.loads((prepared / "output-names.json").read_bytes()) == self.doc("names"), "EXACT_EXTRACTED_INPUTS")
        expected = []
        for label, role, selected in (
                ("receive", "parent", dict(root=parent)),
                ("receive", "acquired", dict(targets=[old["result"]["target"]])),
                ("intake", "authoring-frontier", dict(root=frontier))):
            report = self.doc(label)
            expected.append(dict(source=self.ref(label), role=role, operation=report["operation"],
                reported_profile_sha256=report["profile_sha256"], profile_matches_selected=False, selection=selected))
        disclosure = json.loads((prepared / "selection-disclosure.json").read_bytes())
        need(disclosure == dict(schema="DMKN_OPERATOR_REPORT_SELECTION_V1", policy=POLICY,
             selected_profile_sha256=CURRENT, reports=expected, mathematical_acceptance=False,
             package_compatibility_established=False, protected_state_opened=False,
             authority="UNTRUSTED_SELECTION_ONLY_CURRENT_PRODUCT_RECHECKS_STATE_AND_MATHEMATICS"),
             "EXACT_ORIGIN_DISCLOSURE")
        self.group("strict-refusal-and-opted-in-parent-acquired-frontier-selection")

        # One pure current-profile parser regression, not another old preparation.
        self.kit.PROFILE = old["profile_sha256"]
        inputs = self.kit.Inputs()
        selected = self.kit.parent(inputs, self.ref("receive"), self.state())
        need(selected == parent and inputs.selection_disclosures == [], "STRICT_CURRENT_UNCHANGED")
        self.kit.PROFILE = CURRENT
        self.group("strict-current-parser-retains-exact-root-without-disclosure")

        variants = []
        wrong_state = deepcopy(request)
        wrong_state["state"]["store_id"] = "0"*64
        variants.append((wrong_state, "KIT_REPORT_STATE_MISMATCH"))
        for error, mutate in (
                ("KIT_PARENT_SUCCESS", lambda r: r.update(ok=False)),
                ("KIT_PARENT_SUCCESS", lambda r: r.update(close_errors=["retained failure"])),
                ("KIT_IDENTIFIER", lambda r: r.update(profile_sha256="malformed")),
                ("KIT_PARENT_CHECKED_RECEIVE", lambda r: r["result"].update(status="FAILED")),
                ("KIT_IDENTIFIER", lambda r: r["result"]["admission"].update(local_root="malformed")),
                ("KIT_PARENT_OPERATION", lambda r: r.update(operation="preview"))):
            changed = deepcopy(old)
            mutate(changed)
            failed = deepcopy(request)
            failed["parent_report"] = self.variant(changed)
            variants.append((failed, error))
        for failed, error in variants:
            self.run(failed, error)
        duplicate = deepcopy(request)
        duplicate["acquired"].append(deepcopy(duplicate["acquired"][0]))
        self.run(duplicate, "KIT_DUPLICATE_TARGET_NAME")
        missing_project = deepcopy(request)
        for key in ("project_authoring", "approve_local_project"):
            del missing_project[key]
        self.run(missing_project, "KIT_FRONTIER_REQUIRES_PROJECT")
        self.group("state-result-identity-target-and-frontier-refusals")

        receive = self.base("receive")
        receive.update(selection_report_policy=POLICY, parent_report=self.ref("receive"),
            contacts={"peer-a": deepcopy(CONTACT)}, find_report=self.ref("find"), match_index=0,
            dependency_policy="bounded-closure", limits=dict(requests=128, reply_bytes=8388608,
                units=64, unit_bytes=1048576, total_bytes=4194304, missing=1024,
                preflights=65, locator_bytes=4096))
        self.run(receive, "KIT_SUCCESSFUL_SELECTED_REPORT_REQUIRED")
        # These exact unrelated-role helpers remain strict independently of policy.
        refuses(lambda: self.kit.Inputs().report(self.ref("preview"), "preview"),
                "KIT_SUCCESSFUL_SELECTED_REPORT_REQUIRED")
        refuses(lambda: self.kit.accepted_report(self.kit.Inputs(), self.ref("receive"), self.state()),
                "KIT_PARENT_SUCCESS")
        refuses(lambda: self.kit.query_specs(self.kit.Inputs(), self.ref("query")),
                "KIT_SUCCESSFUL_QUERY_REPORT_REQUIRED")
        for action in ("find", "preview", "publish", "inspect", "produce-baseline"):
            self.run(dict(action=action, selection_report_policy=POLICY,
                          parent_report=self.ref("receive")), "KIT_SELECTION_POLICY_SCOPE")
        for value in ("automatic", True, None):
            changed = deepcopy(request)
            changed["selection_report_policy"] = value
            self.run(changed, "KIT_SELECTION_POLICY")
        self.run(dict(action="prepare-symbol-query", selection_report_policy=POLICY,
                      context_root=parent), "KIT_SELECTION_POLICY_SCOPE")
        self.group("unrelated-report-roles-and-policy-scope-remain-strict")


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "ISOLATED_WINDOWS_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.source_root, args.output
    need(root.is_absolute() and output.is_absolute() and root.is_dir() and
         output.parent.is_dir() and not output.exists(), "SELECTED_FRESH_PATHS")
    started, cpu = time.monotonic(), time.process_time()
    sources, raws, selected = {}, {}, {}
    for filename, sha in SOURCE_PINS.items():
        path = root / PREFIX / filename
        raw = path.read_bytes()
        need(digest(raw) == sha, "SOURCE_PIN:" + filename)
        sources[filename] = raw
        selected[path] = dict(bytes=len(raw), sha256=sha)
    for label, (relative, size, sha) in FIXTURES.items():
        path = root / relative
        raw = path.read_bytes()
        need(len(raw) == size and digest(raw) == sha, "FIXTURE_PIN:" + label)
        raws[label] = raw
        selected[path] = dict(bytes=size, sha256=sha)
    output.mkdir()
    with inert_boundary(set(selected), output) as opened:
        controls = Controls(root, output, raws, sources)
        controls.execute()
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "COOPERATIVE_ALLOWANCE")
        for path, expected in selected.items():
            raw = path.read_bytes()
            need(expected == dict(bytes=len(raw), sha256=digest(raw)), "INPUT_CHANGED:" + str(path))
        controls.group("all-selected-input-bytes-preserved-and-no-product-side-effects")
        result = dict(schema="DMKN_OPERATOR_REPORT_SELECTION_CONTROLS_V1", ok=True,
            groups=controls.groups, positive_preparations=controls.positives,
            refused_preparations=controls.negatives, selected_input_count=len(selected),
            profile_sha256=CURRENT, commands_executed=0, protected_state_opened=False,
            product_modules_imported=False, mathematical_acceptance=False,
            interpretation="INERT_SELECTION_BOUNDARY_NOT_NATIVE_COMPATIBILITY_OR_GROWTH_EVIDENCE",
            observed_file_opens=len(opened), wall_seconds=time.monotonic()-started,
            controller_cpu_seconds=time.process_time()-cpu)
        write(output / "RESULT.json", canonical(result))
    print(canonical(result).decode("utf-8"))


if __name__ == "__main__":
    main()
