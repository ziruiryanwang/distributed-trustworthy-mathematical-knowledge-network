"""Focused inert operator controls. Root selects execution after source review.

Reads exact retained public fixtures and the 45 known package source roles.
Never imports product modules or opens protected state. Historical report
profiles remain historical; configuration preparation is not product execution.
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


PREFIX = "software/v5/ordinary_current_operator_kit/"
CHECKS = "experiments/v5-local-checks/"
PACKAGE = CHECKS + "frontier-launcher-package01/distribution/package"
CURRENT = "efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45"
FIND_PROFILE = "60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b"
QUERY_PROFILE = "bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346"
SOURCE_PINS = {
    "prepare.py": "359bd0e8bd6e5cabd0495bd25eb5a631f16edd92c12afb3b5a5b523434416247",
    "prepare_selected.py": "9881e2ada9742479ace253f44fff69bf809703e1538937a1b50fecfb8d77b3d3",
    "compatibility.json": "08129a60872238eb5dec174fb21a996fc7f5db69748ae623121fe3b51c4af719",
}
# These are preserved reports/source bytes, not generated successful reports.
FIXTURES = {
    "init": (CHECKS + "refinement-recipient-init01/public-launch/child/stdout.txt", 1612,
             "122caf5c89ee858dd8ba092854db0b1eb83835f8b9aec81a01d797cab6172bb6"),
    "intake": (CHECKS + "refinement-recipient-part-b01/public-launch/child/stdout.txt", 2983,
               "e06a0ab9f171868f2d9187ba5757a3d6a7408f2d54c5b79fa52981d0e01f713e"),
    "receive": (CHECKS + "refinement-recipient-receive-b01/peer/RESULT.json", 8036,
                "99cf799a2f0e5f22be49432b46df475afe577fbf8cf512189c7bc36a7ccee6b7"),
    "contribute": (CHECKS + "refinement-recipient-contribute-b01/public-launch/child/stdout.txt", 4999,
                   "4fa48a7ad144e474dde9e78531c4ee37c7547d87661ed688fe3824f00195841c"),
    "find": (CHECKS + "finite-map-discovery-find02/peer/RESULT.json", 59945,
             "69ed25ff27c46d6d56a70a821d5b1589151b318da8eb11374b4973a0600b2830"),
    "find_parent": (CHECKS + "std-kernel-suffix-b01/public-launch/child/stdout.txt", 2949,
                    "416e4184be9d6f97cb928a195f094d7ca37cb475db300d0b6ecf41e554d7ded8"),
    "query": (CHECKS + "received-query01/query/query/RESULT.json", 1642,
              "a578a6bff109b1db4a0d8ba60c17c414cd467b6449c8c27c393cfd1337d9e05c"),
    "native_type": (CHECKS + "received-query01/query/native/type.json", 1173,
                    "333415560e87565ec9a774baaa317ff9e96d0773530da341391b174a9c91c915"),
    "failed": (CHECKS + "finite-map-refinement-contribution01/command/stdout.txt", 1097,
               "21db5fc2b03ea1302a4e69c093c185c993f4a036b669386b327b835ca11d262e"),
    "manifest": (CHECKS + "std-kernel-suffix-inputs01/part-b-canonical.json", 106731,
                 "a0036d02cc15f0fb5a11d3b02a097870b12b81e963f10db26a9949d6b42b5c5c"),
    "source": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/Body.lean", 1077,
               "af055f8fb031383770e952fdd155bc1ef0280214d60f2724109695c62900aec0"),
    "project": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/project-authoring.json", 440,
                "578bb7bcb00531cd9e1da1811db6f1f011b23d1403c32d21a10d387e70ca2865"),
    "names": ("software/v5/ordinary_finite_map_refinement/fresh_recipient/output-names.json", 233,
              "9287a8c97fc6a8d425d5682208991b72fcafdae60e1068b8dde6918a67018061"),
}
CUSTODY = dict(objects=4096, exports=8192, logical_bytes=134217728, db_pages=65536)
INDEX = dict(max_objects=4096, max_postings=262144, max_features=65536,
             max_snapshots=4097, max_logical_bytes=67108864, max_db_pages=32768)
CONTACT = dict(host="127.0.0.1", port=38191, tls=False,
               server_name=None, ca_file=None, ca_sha256=None)


def need(ok, code):
    if not ok:
        raise AssertionError("OPERATOR_CONTROL_" + code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def write(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def load(path, raw, name):
    allowed = {"__future__", "argparse", "hashlib", "ipaddress", "json", "math",
               "os", "pathlib", "re", "stat", "importlib.util", "sys", "time"}
    for node in ast.walk(ast.parse(raw, filename=str(path))):
        if isinstance(node, ast.Import):
            need(all(alias.name in allowed for alias in node.names), "PRODUCT_IMPORT")
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0 and node.module in allowed, "PRODUCT_IMPORT")
    module = ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def refuses(fn, expected):
    try:
        fn()
    except ValueError as error:
        need(str(error) == expected, "WRONG_REFUSAL:" + str(error))
    else:
        raise AssertionError("OPERATOR_CONTROL_EXPECTED_REFUSAL:" + expected)


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
        raise AssertionError("OPERATOR_CONTROL_FORBIDDEN_PROCESS_NETWORK_OR_DB")

    with ExitStack() as stack:
        stack.enter_context(patch.object(Path, "open", checked_open))
        for obj, attr in ((subprocess, "Popen"), (subprocess, "call"),
                          (os, "system"), (socket, "socket"),
                          (socket, "create_connection"), (sqlite3, "connect")):
            stack.enter_context(patch.object(obj, attr, forbidden))
        yield opened


class Controls:
    def __init__(self, root, output, raws, sources, profile, mapping):
        self.root, self.output, self.raws = root, output, raws
        self.kit = load(root / PREFIX / "prepare.py", sources["prepare.py"], "_test_inert_kit")
        self.adapter = load(root / PREFIX / "prepare_selected.py", sources["prepare_selected.py"], "_test_inert_adapter")
        self.profile, self.mapping = profile, mapping
        self.kit.PROFILE = CURRENT
        self.counter, self.positives, self.negatives = 0, 0, 0
        self.groups = []

    def ref(self, label):
        relative, _, sha = FIXTURES[label]
        return dict(path=str(self.root / relative), sha256=sha)

    def doc(self, label):
        return json.loads(self.raws[label])

    def fixture(self, document):
        self.counter += 1
        path = self.output / ("negative-fixture-%03d.json" % self.counter)
        raw = canonical(document)
        write(path, raw)
        return dict(path=str(path), sha256=digest(raw))

    def base(self, action, parent="receive"):
        report = self.doc(parent)
        self.counter += 1
        request = dict(action=action,
                       state={key: report[key] for key in ("catalog", "custody", "store_id")},
                       custody_limits=deepcopy(CUSTODY))
        if action not in ("init", "intake-baseline"):
            request["operation_output"] = str(self.output / ("operation-%03d" % self.counter))
        return request

    def contribute(self):
        request = self.base("contribute")
        request.update(parent_report=self.ref("receive"), source=self.ref("source"),
                       approve_local_source=True, acquired=[dict(report=self.ref("receive"), target_indices=[0])],
                       output_names=self.doc("names"), project_authoring=self.ref("project"),
                       approve_local_project=True, authoring_frontier_report=self.ref("intake"))
        return request

    def find(self):
        self.counter += 1
        return dict(action="find", contacts={"peer-a": deepcopy(CONTACT)}, providers=["peer-a"],
                    specs=[dict(tag="object-kind", value="ordinary-lean-export-v2")],
                    limits=dict(providers=1, snapshots=4, requests=16, pages=12, examined=256,
                                candidates=16, bytes=4194304, wall_ms=20000, inflight=1),
                    offer=dict(max_bytes=262144, max_expanded_bytes=524288, max_age_ms=60000),
                    page=dict(scanned=64, matches=4, bytes=262144, timeout_ms=500,
                              record_probes=1024, node_reads=8192, hash_calls=65536, sql_vm_steps=200000),
                    operation_output=str(self.output / ("operation-%03d" % self.counter)))

    def run(self, request, error=None, selected=False):
        self.counter += 1
        request_path = self.output / ("request-%03d.json" % self.counter)
        prepared = self.output / ("prepared-%03d" % self.counter)
        write(request_path, canonical(request))
        call = (lambda: self.adapter.prepare_selected(self.root / PACKAGE, CURRENT, request_path, prepared)) if selected else (
            lambda: self.kit.prepare(request_path, prepared))
        if error:
            refuses(call, error)
            need(not prepared.exists(), "REFUSAL_WROTE_OUTPUT")
            self.negatives += 1
            return
        result = call()
        receipt = result["preparation"] if selected else result
        stored = json.loads((prepared / "RECEIPT.json").read_bytes())
        need(stored == receipt and receipt["commands_executed"] == 0 and
             receipt["protected_state_opened"] is False and receipt["mathematical_acceptance"] is False,
             "INERT_RECEIPT")
        need(set(path.name for path in prepared.iterdir()) == set(receipt["files"]) | {"RECEIPT.json"}, "OUTPUT_CENSUS")
        for filename, pin in receipt["files"].items():
            raw = (prepared / filename).read_bytes()
            need(pin == dict(bytes=len(raw), sha256=digest(raw)), "OUTPUT_PIN")
        for pin in receipt["inputs"]:
            raw = Path(pin["path"]).read_bytes()
            need(pin == dict(path=pin["path"], bytes=len(raw), sha256=digest(raw)), "INPUT_RECEIPT_PIN")
        arguments = json.loads((prepared / "arguments.json").read_bytes())
        need(arguments["profile_sha256"] == self.kit.PROFILE and
             arguments["requires_launcher"] is True and arguments["mathematical_acceptance"] is False,
             "ARGUMENT_BOUNDARY")
        if "operation_output" in request:
            need(not Path(request["operation_output"]).exists(), "OPERATION_OUTPUT_CREATED")
        self.positives += 1
        return prepared, arguments, result

    def arg(self, arguments, key):
        values = arguments["arguments"]
        need(values.count(key) == 1, "ARGUMENT_OCCURRENCE:" + key)
        return values[values.index(key)+1]

    def group(self, name):
        self.groups.append(dict(name=name, status="PASS"))

    def execute(self):
        # Adapter reads known noncompiled roles; it deliberately does not read
        # or approve generated native artifacts. Only data copies are changed.
        label, roles = self.adapter.known_layout(self.kit, self.profile, self.mapping)
        need(label == "current-frontier-sparse-multisource" and len(roles) == 45, "CURRENT_LAYOUT")
        changed = deepcopy(self.profile)
        direct = sorted(roles)[0]
        changed["files"][direct]["sha256"] = "0"*64
        refuses(lambda: self.adapter.known_layout(self.kit, changed, self.mapping), "KIT_SELECT_UNKNOWN_INTERFACE")
        changed = deepcopy(self.profile)
        changed["files"]["unknown.py"] = dict(bytes=1, sha256="0"*64)
        refuses(lambda: self.adapter.known_layout(self.kit, changed, self.mapping), "KIT_SELECT_UNKNOWN_INTERFACE")
        changed = deepcopy(self.profile)
        generated = self.mapping["generated_roles"][0]
        changed["files"][generated] = dict(bytes=1, sha256="0"*64)
        need(self.adapter.known_layout(self.kit, changed, self.mapping)[0] == label, "NATIVE_NOT_APPROVED")
        request = self.base("prepare-query")
        request.update(parent_report=self.ref("receive"), native_type=self.ref("native_type"))
        prepared, args, selected = self.run(request, selected=True)
        need(selected["native_artifacts_checked"] is False and selected["known_noncompiled_roles"] == 45,
             "SELECTED_INTERFACE_BOUNDARY")
        need(args["entry"] == "query" and args["arguments"][0].startswith("--") and
             "prepare-query" not in args["arguments"] and
             self.arg(args, "--context-root") == self.doc("receive")["result"]["admission"]["local_root"] and
             (prepared / "native-type.json").read_bytes() == self.raws["native_type"], "QUERY_ARGUMENTS")
        self.group("selected-current-interface-and-query-emission")

        request = self.contribute()
        prepared, args, _ = self.run(request)
        need(args["entry"] == "owner" and args["arguments"][0] == "contribute" and
             "--approve-local-project" not in args["arguments"] and
             self.arg(args, "--parent-root") == self.doc("receive")["result"]["admission"]["local_root"] and
             self.arg(args, "--authoring-frontier-root") == self.doc("intake")["result"]["local_root"] and
             self.arg(args, "--project-authoring-sha256") == FIXTURES["project"][2], "CONTRIBUTION_ARGUMENTS")
        need((prepared / "Body.lean").read_bytes() == self.raws["source"] and
             (prepared / "project-authoring.json").read_bytes() == self.raws["project"] and
             json.loads((prepared / "acquired-targets.json").read_bytes()) == [self.doc("receive")["result"]["target"]] and
             json.loads((prepared / "output-names.json").read_bytes()) == self.doc("names"), "CONTRIBUTION_EXACT_INPUTS")
        # Reuse the exact prepared request to test no overwrite, not a new run.
        before = {p.name: digest(p.read_bytes()) for p in prepared.iterdir()}
        refuses(lambda: self.kit.prepare(self.output / ("request-%03d.json" % self.counter), prepared), "KIT_OUTPUT_EXISTS")
        need(before == {p.name: digest(p.read_bytes()) for p in prepared.iterdir()}, "OVERWRITE_CHANGED_BYTES")
        self.group("received-target-to-contribution-with-protected-frontier")

        request = self.contribute()
        request.update(parent_report=self.ref("contribute"), acquired=[])
        for key in ("project_authoring", "approve_local_project", "authoring_frontier_report"):
            del request[key]
        prepared, args, _ = self.run(request)
        need(self.arg(args, "--parent-root") == self.doc("contribute")["result"]["local_root"] and
             json.loads((prepared / "acquired-targets.json").read_bytes()) == [] and
             "--project-authoring" not in args["arguments"], "CONTRIBUTION_AS_PARENT")
        self.group("checked-contribution-as-parent-and-empty-acquisition")

        for fixture in ("receive", "contribute"):
            request = self.base("publish")
            access = dict(pairs=[["1"*64, "2"*64]], limits=dict(max_rows=8, max_logical_bytes=8192))
            request.update(accepted_report=self.ref(fixture), target_indices=[0],
                           index=dict(path=str(self.output / ("index-" + fixture)), create=True,
                                      limits=deepcopy(INDEX), access_pairs=access),
                           max_unit_bytes=8388608, max_total_bytes=33554432)
            prepared, args, _ = self.run(request)
            config = json.loads((prepared / "config.json").read_bytes())
            result = self.doc(fixture)["result"]
            targets = [result["target"]] if fixture == "receive" else result["targets"]
            root = result["admission"]["local_root"]
            need(config["targets"] == targets and config["context_root"] == root and
                 config["index"]["access_pairs"] == access and args["entry"] == "peer" and
                 self.arg(args, "--config-sha256") == digest((prepared / "config.json").read_bytes()), "PUBLISH_HANDOFF")
            need(not Path(request["index"]["path"]).exists(), "INDEX_CREATED")
        self.group("accepted-receive-and-contribution-publication")

        request = self.find()
        del request["specs"]
        request.update(query_report=self.ref("query"), candidate_mode="sparse-v2")
        with patch.object(self.kit, "PROFILE", QUERY_PROFILE):
            prepared, _, _ = self.run(request)
            config = json.loads((prepared / "config.json").read_bytes())
            need(config["specs"] == self.doc("query")["specs"] and config["candidate_mode"] == "sparse-v2",
                 "GENUINE_HISTORICAL_QUERY")
        self.run(request, "KIT_SUCCESSFUL_QUERY_REPORT_REQUIRED")
        both = deepcopy(request)
        both["specs"] = self.find()["specs"]
        self.run(both, "KIT_FIND_EXACTLY_ONE_QUERY_MODE")
        neither = deepcopy(request)
        del neither["query_report"]
        self.run(neither, "KIT_FIND_EXACTLY_ONE_QUERY_MODE")
        self.group("historical-query-profile-and-exclusive-query-mode")

        request = self.base("receive", "find_parent")
        provider = self.doc("find")["result"]["matches"][0]["provider"]
        alternate = "kit-control-alternate"
        need(provider != alternate, "ALTERNATE_CONTACT_LABEL")
        request.update(contacts={provider: deepcopy(CONTACT), alternate: deepcopy(CONTACT)},
                       parent_report=self.ref("find_parent"), find_report=self.ref("find"), match_index=0,
                       dependency_policy="bounded-closure", acquisition_sources=[provider, alternate],
                       attempt_timeout_ms=500, finalization_reserve_ms=1000,
                       limits=dict(requests=128, reply_bytes=67108864, units=64, unit_bytes=8388608,
                                   total_bytes=33554432, missing=256, preflights=65, locator_bytes=1048576))
        with patch.object(self.kit, "PROFILE", FIND_PROFILE):
            prepared, _, _ = self.run(request)
            config = json.loads((prepared / "config.json").read_bytes())
            need(config["selection"] == self.doc("find")["result"]["matches"][0] and
                 config["parent_root"] == self.doc("find_parent")["result"]["local_root"] and
                 all(config[key] == request[key] for key in
                     ("acquisition_sources", "attempt_timeout_ms", "finalization_reserve_ms")), "MULTISOURCE_HANDOFF")
            for remove in ("attempt_timeout_ms", "finalization_reserve_ms", "acquisition_sources"):
                changed = deepcopy(request)
                del changed[remove]
                self.run(changed, "KIT_SOURCE_POLICY_FIELDS")
            for sources in ([provider, provider], ["unselected-contact"]):
                changed = deepcopy(request)
                changed["acquisition_sources"] = sources
                self.run(changed, "KIT_ACQUISITION_SOURCES")
        self.run(request, "KIT_SUCCESSFUL_SELECTED_REPORT_REQUIRED")
        self.group("historical-find-to-bounded-multisource-receive")

        request = self.base("intake-baseline")
        request.update(parent_report=self.ref("init"), manifest=self.ref("manifest"),
                       bundle_directory=str(self.root / CHECKS / "std-reconstruct01/materialized"))
        _, args, _ = self.run(request)
        need(self.arg(args, "--bundle-manifest") == self.ref("manifest")["path"] and
             self.arg(args, "--bundle-manifest-sha256") == FIXTURES["manifest"][2] and
             Path(self.ref("manifest")["path"]).name != "manifest.json" and
             not Path(self.ref("manifest")["path"]).is_relative_to(Path(request["bundle_directory"])),
             "DIRECT_MANIFEST_LOCATION")
        wrong = deepcopy(request)
        wrong["manifest"]["sha256"] = "0"*64
        self.run(wrong, "KIT_INPUT_PIN")
        self.group("explicit-manifest-intake-without-producer-metadata")

        mutations = [
            ("receive", lambda d: d.update(ok=False), "KIT_PARENT_SUCCESS"),
            ("receive", lambda d: d.update(profile_sha256=FIND_PROFILE), "KIT_PARENT_SUCCESS"),
            ("receive", lambda d: d.update(store_id="0"*64), "KIT_REPORT_STATE_MISMATCH"),
            ("receive", lambda d: d.update(close_errors=["test"]), "KIT_PARENT_SUCCESS"),
            ("receive", lambda d: d.update(final_budget_error="test"), "KIT_PARENT_SUCCESS"),
            ("receive", lambda d: d["result"].update(cleanup_errors=["test"]), "KIT_PARENT_RESULT"),
            ("receive", lambda d: d["result"]["target"].update(export_id="0"*64), "KIT_RECEIVE_EXPORT_BINDING"),
            ("contribute", lambda d: d["result"]["admission"].update(local_root="0"*64), "KIT_PARENT_CHECKED_CONTRIBUTION"),
            ("contribute", lambda d: d["result"]["targets"][0].update(export_id="0"*64), "KIT_CONTRIBUTION_EXPORT_BINDING"),
        ]
        for fixture, mutate, error in mutations:
            doc = self.doc(fixture)
            mutate(doc)
            request = self.contribute()
            request["parent_report"] = self.fixture(doc)
            self.run(request, error)
        request = self.contribute()
        request["parent_report"] = self.ref("failed")
        self.run(request, "KIT_PARENT_SUCCESS")
        request["parent_report"] = self.fixture(self.doc("receive")["result"])
        self.run(request, "KIT_PARENT_OPERATION")
        self.group("genuine-failure-and-mutated-report-refusals")

        variants = []
        def variant(error, change):
            request = self.contribute()
            change(request)
            variants.append((request, error))
        variant("KIT_EXPLICIT_LOCAL_SOURCE_APPROVAL", lambda r: r.update(approve_local_source=False))
        variant("KIT_EXPLICIT_LOCAL_PROJECT_APPROVAL", lambda r: r.update(approve_local_project=False))
        variant("KIT_PROJECT_APPROVAL_FIELDS", lambda r: r.pop("approve_local_project"))
        def remove_project(request):
            del request["project_authoring"], request["approve_local_project"]
        variant("KIT_FRONTIER_REQUIRES_PROJECT", remove_project)
        variant("KIT_DUPLICATE_TARGET", lambda r: r["acquired"][0].update(target_indices=[0, 0]))
        variant("KIT_INTEGER", lambda r: r["acquired"][0].update(target_indices=[1]))
        variant("KIT_DUPLICATE_OUTPUT_NAME", lambda r: r["output_names"].append(deepcopy(r["output_names"][0])))
        variant("KIT_DUPLICATE_TARGET_NAME", lambda r: r["acquired"].append(deepcopy(r["acquired"][0])))
        variant("KIT_OUTPUT_IS_ACQUIRED", lambda r: r.update(output_names=[self.doc("receive")["result"]["target"]["name"]]))
        variant("KIT_INPUT_PIN", lambda r: r["source"].update(sha256="0"*64))
        for request, error in variants:
            self.run(request, error)
        self.group("explicit-approval-target-selection-and-source-pin-refusals")


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
    sources = {name: (root / PREFIX / name).read_bytes() for name in SOURCE_PINS}
    need(all(digest(sources[name]) == pin for name, pin in SOURCE_PINS.items()), "SOURCE_PINS")
    mapping = json.loads(sources["compatibility.json"])
    profile_raw = (root / PACKAGE / "PROFILE.json").read_bytes()
    need(digest(profile_raw) == CURRENT, "ACTUAL_PROFILE_PIN")
    profile = json.loads(profile_raw)
    selected_inputs = {root / PREFIX / name: dict(bytes=len(raw), sha256=digest(raw))
                       for name, raw in sources.items()}
    selected_inputs[root / PACKAGE / "PROFILE.json"] = dict(bytes=len(profile_raw), sha256=CURRENT)
    for name, pin in mapping["direct_sources"].items():
        selected_inputs[root / PACKAGE / name] = pin
    raws = {}
    for label, (relative, size, sha) in FIXTURES.items():
        path = root / relative
        raw = path.read_bytes()
        need(len(raw) == size and digest(raw) == sha, "FIXTURE_PIN:" + label)
        raws[label] = raw
        selected_inputs[path] = dict(bytes=size, sha256=sha)
    need(len(selected_inputs) == 62, "SELECTED_INPUT_CENSUS")
    output.mkdir()
    with inert_boundary(set(selected_inputs), output) as opened:
        controls = Controls(root, output, raws, sources, profile, mapping)
        controls.execute()
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "COOPERATIVE_ALLOWANCE")
        for path, pin in selected_inputs.items():
            raw = path.read_bytes()
            need(pin == dict(bytes=len(raw), sha256=digest(raw)), "INPUT_CHANGED:" + str(path))
        controls.group("selected-input-integrity-and-no-side-effects")
        result = dict(schema="DMKN_CURRENT_OPERATOR_CONTROLS_V1", ok=True, groups=controls.groups,
                      positive_preparations=controls.positives, refused_preparations=controls.negatives,
                      selected_input_count=len(selected_inputs),
                      fixture_profiles=dict(current=CURRENT, historical_find=FIND_PROFILE, historical_query=QUERY_PROFILE),
                      commands_executed=0, protected_state_opened=False, product_modules_imported=False,
                      native_artifacts_checked=False, mathematical_acceptance=False,
                      interpretation="INERT_HANDOFF_CONTROLS_NOT_A_CURRENT_END_TO_END_QUERY_OR_NATIVE_RUN",
                      reads=sorted({path for path, mode in opened if "r" in mode}),
                      wall_seconds=time.monotonic()-started, controller_cpu_seconds=time.process_time()-cpu)
        write(output / "RESULT.json", canonical(result))
    print(canonical(result).decode("utf-8"))


if __name__ == "__main__":
    main()
